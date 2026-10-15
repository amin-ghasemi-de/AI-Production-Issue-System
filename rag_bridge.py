import json
import os
import subprocess
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent


def run_rag(input_text):
    if os.name == "nt":
        rag_python = PROJECT_ROOT / ".venv-rag" / "Scripts" / "python.exe"
        rag_script = PROJECT_ROOT / "rag" / "rag_cli.py"

        process = subprocess.run(
            [str(rag_python), str(rag_script)],
            input=json.dumps({"input_text": input_text}),
            text=True,
            capture_output=True,
            cwd=str(PROJECT_ROOT)
        )

        if process.returncode != 0:
            raise RuntimeError(process.stderr)

        return json.loads(process.stdout)

    from rag.rag_answer import ask_rag

    return ask_rag(input_text)