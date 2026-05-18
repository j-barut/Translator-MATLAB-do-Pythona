import subprocess
import tempfile
import os


def run_python_code(code: str):
    temp_file = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8"
        ) as f:
            f.write(code)
            temp_file = f.name
        result = subprocess.run(
            ["python", temp_file],
            capture_output=True,
            text=True,
            timeout=30
        )

        return {
            "success": True,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Execution timeout"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
    finally:
        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)