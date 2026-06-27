import os
import sys
import traceback
from pathlib import Path


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    data_dir = Path(os.environ.get("MHEIBOS_DATA_DIR") or Path.home() / "AppData" / "Local" / "Mheibos Suite")
    data_dir.mkdir(parents=True, exist_ok=True)
    if sys.stdout is None or sys.stderr is None:
        log_file = (data_dir / "backend.log").open("a", encoding="utf-8")
        sys.stdout = log_file
        sys.stderr = log_file

    import django
    from django.core.management import call_command, execute_from_command_line

    django.setup()
    call_command("migrate", interactive=False, verbosity=0)
    try:
        call_command("preparar_financeiro", verbosity=0)
    except Exception:
        pass

    args = sys.argv[1:] or ["runserver", "127.0.0.1:8765", "--noreload"]
    execute_from_command_line([sys.argv[0], *args])


if __name__ == "__main__":
    try:
        main()
    except Exception:
        data_dir = Path(os.environ.get("MHEIBOS_DATA_DIR") or Path.home() / "AppData" / "Local" / "Mheibos Suite")
        data_dir.mkdir(parents=True, exist_ok=True)
        (data_dir / "backend-error.log").write_text(traceback.format_exc(), encoding="utf-8")
        raise
