import json
import os
import subprocess
import sys
import time
from pathlib import Path

from flask import Flask, jsonify, render_template, send_from_directory


# AI-GENERATED COMMENT:
# This backend was generated/updated with AI assistance to provide a web UI,
# launch session processing, and expose pose catalog totals.
BASE_DIR = Path(__file__).resolve().parent
STATS_FILE = BASE_DIR / "pose_stats.json"
SESSION_LOG_FILE = BASE_DIR / "session_runtime.log"
STOCK_IMAGE_DIR = BASE_DIR / "stock_image"
POSE_HOLD_SECONDS = float(os.getenv("POSE_HOLD_SECONDS", "4.0"))
DEFAULT_CONDA_ENV = os.getenv("YOGAMER_CONDA_ENV", "yogamer_cv")

app = Flask(__name__, template_folder="templates", static_folder="static")
SESSION_PROCESS = None
SESSION_LAST_EXIT = None


def get_runtime_python():
    # AI-GENERATED COMMENT:
    # This allows forcing the webcam runtime to a specific env interpreter.
    return os.getenv("YOGAMER_RUNTIME_PYTHON", sys.executable)


def build_runtime_command():
    explicit_python = os.getenv("YOGAMER_RUNTIME_PYTHON")
    if explicit_python:
        return [explicit_python], f"python:{explicit_python}"

    conda_exe = os.getenv("CONDA_EXE")
    if not conda_exe:
        user_home = Path.home()
        candidates = [
            user_home / "anaconda3" / "Scripts" / "conda.exe",
            user_home / "miniconda3" / "Scripts" / "conda.exe",
        ]
        for candidate in candidates:
            if candidate.exists():
                conda_exe = str(candidate)
                break
    if conda_exe:
        return [conda_exe, "run", "-n", DEFAULT_CONDA_ENV, "python"], f"conda_env:{DEFAULT_CONDA_ENV}"

    return [sys.executable], f"python:{sys.executable}"


def missing_runtime_dependencies(runtime_command):
    required_modules = ["cv2", "mediapipe", "ai_edge_litert", "numpy"]
    module_expr = ", ".join([f"'{name}'" for name in required_modules])
    check_script = (
        "import importlib.util; "
        f"mods=[{module_expr}]; "
        "missing=[m for m in mods if importlib.util.find_spec(m) is None]; "
        "print('|'.join(missing))"
    )
    result = subprocess.run(
        runtime_command + ["-c", check_script],
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return required_modules, result.stderr.strip() or result.stdout.strip()
    missing_line = result.stdout.strip()
    missing = missing_line.split("|") if missing_line else []
    return missing, ""


def read_stats():
    if not STATS_FILE.exists():
        return {}
    with STATS_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/catalog")
def catalog_page():
    return render_template("catalog.html")


@app.route("/stock-image/<path:filename>")
def serve_stock_image(filename):
    return send_from_directory(STOCK_IMAGE_DIR, filename)


@app.route("/api/session/start", methods=["POST"])
def start_session():
    global SESSION_PROCESS, SESSION_LAST_EXIT
    if SESSION_PROCESS and SESSION_PROCESS.poll() is None:
        return jsonify({"ok": True, "status": "already_running"})

    runtime_command, runtime_source = build_runtime_command()
    missing, check_error = missing_runtime_dependencies(runtime_command)
    if missing:
        return (
            jsonify(
                {
                    "ok": False,
                    "status": "missing_dependencies",
                    "missing_modules": missing,
                    "runtime_command": runtime_command,
                    "runtime_source": runtime_source,
                    "dependency_check_error": check_error,
                    "message": "Install missing packages in the runtime Python used for yogamer_app.py.",
                }
            ),
            400,
        )

    env = os.environ.copy()
    env["POSE_HOLD_SECONDS"] = str(POSE_HOLD_SECONDS)
    env["POSE_STATS_FILE"] = str(STATS_FILE)

    SESSION_LOG_FILE.write_text("", encoding="utf-8")
    log_file = SESSION_LOG_FILE.open("a", encoding="utf-8")

    SESSION_PROCESS = subprocess.Popen(
        runtime_command + ["yogamer_app.py"],
        cwd=BASE_DIR,
        env=env,
        stdout=log_file,
        stderr=log_file,
        text=True,
    )
    time.sleep(1.2)
    if SESSION_PROCESS.poll() is not None:
        log_tail = SESSION_LOG_FILE.read_text(encoding="utf-8")[-1000:] if SESSION_LOG_FILE.exists() else ""
        SESSION_LAST_EXIT = {"exit_code": SESSION_PROCESS.returncode, "log_tail": log_tail}
        return (
            jsonify(
                {
                    "ok": False,
                    "status": "startup_failed",
                    "runtime_command": runtime_command,
                    "runtime_source": runtime_source,
                    "exit_code": SESSION_PROCESS.returncode,
                    "log_tail": log_tail,
                }
            ),
            500,
        )

    SESSION_LAST_EXIT = None
    return jsonify({"ok": True, "status": "started", "runtime_command": runtime_command, "runtime_source": runtime_source})


@app.route("/api/session/status", methods=["GET"])
def session_status():
    global SESSION_LAST_EXIT
    running = SESSION_PROCESS is not None and SESSION_PROCESS.poll() is None
    if SESSION_PROCESS is not None and not running and SESSION_LAST_EXIT is None:
        log_tail = SESSION_LOG_FILE.read_text(encoding="utf-8")[-1000:] if SESSION_LOG_FILE.exists() else ""
        SESSION_LAST_EXIT = {"exit_code": SESSION_PROCESS.returncode, "log_tail": log_tail}
    runtime_command, runtime_source = build_runtime_command()
    return jsonify(
        {
            "running": running,
            "pose_hold_seconds": POSE_HOLD_SECONDS,
            "backend_python": sys.executable,
            "runtime_command": runtime_command,
            "runtime_source": runtime_source,
            "last_exit": SESSION_LAST_EXIT,
        }
    )


@app.route("/api/poses", methods=["GET"])
def pose_catalog():
    raw_stats = read_stats()
    poses = [{"pose": pose, "total_seconds": float(seconds)} for pose, seconds in sorted(raw_stats.items())]
    return jsonify({"poses": poses})


@app.route("/api/poses/reset", methods=["POST"])
def reset_catalog():
    # AI-GENERATED COMMENT:
    # Keep pose names but reset totals so users can start a new session slate.
    stats = read_stats()
    reset_stats = {pose: 0.0 for pose in stats}
    with STATS_FILE.open("w", encoding="utf-8") as file:
        json.dump(reset_stats, file, indent=2)
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
