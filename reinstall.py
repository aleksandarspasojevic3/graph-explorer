"""Skripta za reinstalaciju komponenti i pokretanje servera

Radi sledece:
    1. pravi virtuelno okruzenje (venv) ako ne postoji,
    2. deinstalira sve komponente projekta iz venv-a,
    3. brise build fajlove komponenti (build/, *.egg-info),
    4. instalira pakete iz requirements.txt i sve komponente,
    5. pokrece Django server

Pokretanje (iz korena projekta, venv ne mora biti aktiviran):
    python reinstall.py              reinstalacija i pokretanje servera
    python reinstall.py --no-server  samo reinstalacija
"""

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VENV = ROOT / "venv"

# Folder komponente -> ime paketa iz njenog pyproject.toml
COMPONENTS = {
    "api": "sok-api",
    "platform": "sok-core",
    "json_datasource": "sok-json-datasource",
    "xml_datasource": "sok-xml-datasource",
    "simple_visualizer": "sok-simple-visualizer",
    "block_visualizer": "sok-block-visualizer",
}


def venv_python() -> Path:
    """Vraca putanju do Python-a iz venv-a (razlikuje se na Windows-u i Linux-u)"""
    if sys.platform == "win32":
        return VENV / "Scripts" / "python.exe"
    return VENV / "bin" / "python"


def run(*args: str, cwd: Path = ROOT) -> None:
    """Pokrece komandu i prekida skriptu ako komanda ne uspe"""
    result = subprocess.run(args, cwd=cwd)
    if result.returncode != 0:
        print(f"\nGreska pri izvrsavanju: {' '.join(args)}")
        sys.exit(result.returncode)


def main() -> None:
    start_server = "--no-server" not in sys.argv

    if not venv_python().exists():
        print("[1/5] Pravim virtuelno okruzenje...")
        run(sys.executable, "-m", "venv", str(VENV))
    else:
        print("[1/5] Virtuelno okruzenje vec postoji.")
    python = str(venv_python())

    print("[2/5] Deinstaliram komponente...")
    subprocess.run([python, "-m", "pip", "uninstall", "-y", "-q", *COMPONENTS.values()],
                   cwd=ROOT, stderr=subprocess.DEVNULL)

    print("[3/5] Brisem build fajlove...")
    for folder in COMPONENTS:
        component = ROOT / folder
        shutil.rmtree(component / "build", ignore_errors=True)
        for egg_info in component.glob("*.egg-info"):
            shutil.rmtree(egg_info, ignore_errors=True)

    print("[4/5] Instaliram pakete i komponente...")
    run(python, "-m", "pip", "install", "-q", "-r", "requirements.txt")
    editable = [arg for folder in COMPONENTS for arg in ("-e", f"./{folder}")]
    run(python, "-m", "pip", "install", "-q", *editable)

    if start_server:
        print("[5/5] Pokrecem server na http://127.0.0.1:8000 (zaustavljanje: Ctrl+C)...")
        try:
            run(python, "manage.py", "runserver", cwd=ROOT / "graph_explorer")
        except KeyboardInterrupt:
            print("\nServer zaustavljen.")
    else:
        print("[5/5] Gotovo. Server nije pokrenut (--no-server).")


if __name__ == "__main__":
    main()