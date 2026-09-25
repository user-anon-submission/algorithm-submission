import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def on_startup(command, dirty):
    stub = ROOT / "anonlib.pyi"
    if not stub.exists():
        raise FileNotFoundError("anonlib.pyi not found — run `make stubs` first")
    dest = ROOT / ".docs-stub"
    dest.mkdir(exist_ok=True)
    text = stub.read_text()
    text = re.sub(
        r"def __new__\(cls(.*)\) -> [\w.]+:( \.\.\.)?$",
        r"def __init__(self\1) -> None:\2",
        text,
        flags=re.M,
    )
    (dest / "anonlib.py").write_text(text)

