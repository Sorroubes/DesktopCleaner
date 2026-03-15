import os
import sys
import shutil
import json
from datetime import datetime, timedelta
from plyer import notification
from plyer.platforms.win.notification import WindowsNotification
import ctypes


def get_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


BASE_DIR = get_base_dir()
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")


def get_desktop():
    buf = ctypes.create_unicode_buffer(260)
    ctypes.windll.shell32.SHGetFolderPathW(None, 0x10, None, 0, buf)
    return buf.value


def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {"days": 30, "folder": "OldFiles"}

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"days": 30, "folder": "OldFiles"}


def notify(message):
    notification.notify(
        title="Desktop Cleaner",
        message=message,
        app_name="Cleaner",
        timeout=5
    )


def safe_move(src, dst_folder):
    name = os.path.basename(src)
    dst = os.path.join(dst_folder, name)

    if os.path.exists(dst):
        base, ext = os.path.splitext(name)
        i = 1
        while True:
            new_name = f"{base}_{i}{ext}"
            new_dst = os.path.join(dst_folder, new_name)
            if not os.path.exists(new_dst):
                dst = new_dst
                break
            i += 1

    shutil.move(src, dst)


def clean():
    config = load_config()

    days = config.get("days", 30)
    folder = config.get("folder", "OldFiles")

    desktop = get_desktop()
    target = os.path.join(desktop, folder)

    os.makedirs(target, exist_ok=True)

    limit = datetime.now() - timedelta(days=days)
    moved = 0

    for file in os.listdir(desktop):
        path = os.path.join(desktop, file)

        if os.path.isdir(path):
            continue

        if file.lower().endswith((".lnk", ".url")):
            continue

        try:
            modified = datetime.fromtimestamp(os.path.getmtime(path))
        except Exception:
            continue

        if modified < limit:
            try:
                safe_move(path, target)
                moved += 1
            except Exception:
                pass

    if moved == 0:
        notify("Старих файлів не знайдено")
    else:
        notify(f"Переміщено файлів: {moved}")


if __name__ == "__main__":
    clean()