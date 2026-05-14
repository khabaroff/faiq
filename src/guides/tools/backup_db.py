import os
import shutil
import subprocess
from datetime import datetime

from guides.settings import get_settings


def backup_db() -> None:
    s = get_settings()
    db_path = s.state_dir / "articles.db"
    if not db_path.exists():
        print("DB not found, skipping backup.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = s.state_dir / f"articles_backup_{timestamp}.db"

    shutil.copy2(db_path, backup_path)
    print(f"Backup created: {backup_path}")

    # Keep only last 7 local backups
    backups = sorted(s.state_dir.glob("articles_backup_*.db"))
    if len(backups) > 7:
        for old_backup in backups[:-7]:
            old_backup.unlink()
            print(f"Removed old backup: {old_backup}")

    # Off-site via rclone (optional — requires RCLONE_BACKUP_DEST in env)
    rclone_dest = os.environ.get("RCLONE_BACKUP_DEST")
    if rclone_dest:
        try:
            subprocess.run(
                ["rclone", "copy", str(backup_path), rclone_dest],
                check=True,
                timeout=120,
            )
            print(f"Off-site backup pushed to {rclone_dest}")
        except FileNotFoundError:
            print("rclone not found — skipping off-site backup")
        except subprocess.CalledProcessError as e:
            print(f"rclone failed (exit {e.returncode}) — local backup kept")


if __name__ == "__main__":
    backup_db()
