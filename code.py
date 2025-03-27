import os
import shutil
import hashlib

def calculate_hash(file):
    h = hashlib.md5()
    with open(file, 'rb') as f:
        while chunk := f.read(4096):
            h.update(chunk)
    return h.hexdigest()

def create_directory():
    name = input("Enter the directory name: ")
    path = input("Enter the location where you want to create it: ")
    full_path = os.path.join(path, name)
    os.makedirs(full_path, exist_ok=True)
    print(f"Directory '{name}' created at {path}")

def delete_directory():
    path = input("Enter the directory path to delete: ")
    if os.path.exists(path):
        shutil.rmtree(path)
        print(f"Directory '{path}' deleted")
    else:
        print("Directory does not exist")

def move_directory():
    src = input("Enter the source directory path: ")
    dest = input("Enter the destination directory path: ")
    if os.path.exists(src):
        shutil.move(src, dest)
        print(f"Directory moved from {src} to {dest}")
    else:
        print("Source directory does not exist")

def organize(directory):
    create_directory(f"{directory}/Images")
    create_directory(f"{directory}/Docs")
    
    for file in os.listdir(directory):
        path = os.path.join(directory, file)
        if os.path.isfile(path):
            if file.endswith(('.jpg', '.png')):
                shutil.move(path, f"{directory}/Images/{file}")
            elif file.endswith(('.pdf', '.txt')):
                shutil.move(path, f"{directory}/Docs/{file}")

def find_duplicates(directory):
    hashes = {}
    duplicates = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            h = calculate_hash(path)
            if h in hashes:
                duplicates.append(path)
            else:
                hashes[h] = path
    return duplicates

if __name__ == "__main__":
    while True:
        print("\nOptions:")
        print("1. Create Directory")
        print("2. Delete Directory")
        print("3. Move Directory")
        print("4. Organize Directory")
        print("5. Find Duplicates")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")
        
        if choice == "1":
            create_directory()
        elif choice == "2":
            delete_directory()
        elif choice == "3":
            move_directory()
        elif choice == "4":
            dir_path = input("Enter directory path to organize: ")
            organize(dir_path)
            print("Files organized")
        elif choice == "5":
            dir_path = input("Enter directory path to find duplicates: ")
            print("Duplicates:", find_duplicates(dir_path))
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")
