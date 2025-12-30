import os
import hashlib
import shutil

# ================= SETTINGS =================
DRY_RUN = False               # True = no deletion/move
MOVE_DUPLICATES = False        # False = delete duplicates
DUPLICATE_FOLDER = "duplicates"
IGNORE_EXTENSIONS = {".exe", ".zip", ".iso"}
# ============================================

def file_hash(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

def progress_bar(current, total, width=40):
    percent = current / total
    filled = int(width * percent)
    bar = "█" * filled + "-" * (width - filled)
    print(f"\r[{bar}] {int(percent * 100)}%", end="")
    if current == total:
        print()

def get_files(folder, recursive):
    files = []
    if recursive:
        for root, _, fs in os.walk(folder):
            for f in fs:
                files.append(os.path.join(root, f))
    else:
        for f in os.listdir(folder):
            path = os.path.join(folder, f)
            if os.path.isfile(path):
                files.append(path)
    return files

def remove_duplicates(folder, recursive):
    files_list = get_files(folder, recursive)
    total = len(files_list)

    seen = {}
    handled = 0
    skipped = 0

    dup_dir = os.path.join(folder, DUPLICATE_FOLDER)
    if MOVE_DUPLICATES and not DRY_RUN:
        os.makedirs(dup_dir, exist_ok=True)

    for i, path in enumerate(files_list, 1):
        progress_bar(i, total)

        ext = os.path.splitext(path)[1].lower()
        if ext in IGNORE_EXTENSIONS:
            skipped += 1
            continue

        try:
            size = os.path.getsize(path)
            h = file_hash(path)
            key = (size, h)

            if key in seen:
                print(f"\nDuplicate: {path}")
                if not DRY_RUN:
                    if MOVE_DUPLICATES:
                        shutil.move(path, os.path.join(dup_dir, os.path.basename(path)))
                    else:
                        os.remove(path)
                handled += 1
            else:
                seen[key] = path

        except Exception:
            skipped += 1

    print("\n===== SUMMARY =====")
    print(f"Duplicates handled: {handled}")
    print(f"Files skipped: {skipped}")
    print("Mode:", "DRY RUN" if DRY_RUN else "LIVE")
    print("Subfolders:", "Yes" if recursive else "No")
    print("===================")

if __name__ == "__main__":
    folder = input("Enter folder path: ")
    choice = input("Scan subfolders? (y/n): ").lower()
    recursive = choice == "y"
    remove_duplicates(folder, recursive)
