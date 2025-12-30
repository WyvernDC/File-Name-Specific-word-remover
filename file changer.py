import os

# Ask user
folder = input("Enter folder path: ").strip()
extension = input("Enter file type (e.g. .mp3 or ALL): ").strip().lower()
remove_text = input("Text to remove from filename: ").strip()

print("\nPreview:")
changes = []

for filename in os.listdir(folder):
    if extension != "all" and not filename.lower().endswith(extension):
        continue

    if remove_text in filename:
        new_name = filename.replace(remove_text, "")
        changes.append((filename, new_name))
        print(f"{filename} → {new_name}")

if not changes:
    print("No files matched.")
    exit()

confirm = input("\nApply changes? (y/n): ").lower()
if confirm != "y":
    print("Cancelled.")
    exit()

# Rename
for old, new in changes:
    os.rename(
        os.path.join(folder, old),
        os.path.join(folder, new)
    )

print("Done ✔")
