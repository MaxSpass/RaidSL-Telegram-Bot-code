import os
import shutil
import subprocess
import win32com.client

root_dir = os.path.normpath(os.path.normpath(os.path.join(os.getcwd(), 'dist')))
name = 'RaidSL-Telegram-Bot'
bot_path = root_dir


def find_occurrences(string, substrings):
    occurrences = []
    for sub in substrings:
        if sub in string:
            occurrences.append(sub)
    return occurrences


def remove_files_and_folders(folder_path, ignore=None):
    if ignore is None:
        ignore = []

    files_removed = 0
    folders_removed = 0

    for root, dirs, files in os.walk(folder_path, topdown=False):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if not len(find_occurrences(file_path, ignore)):
                os.remove(file_path)
                files_removed += 1

        for dir_name in dirs[:]:
            dir_path = os.path.join(root, dir_name)
            if not len(find_occurrences(dir_path, ignore)):
                remove_files_and_folders(dir_path, ignore)  # Recursively remove files and folders
                os.rmdir(dir_path)
                folders_removed += 1

    print(f"Files removed: {files_removed} | Folders removed: {folders_removed}")


def clear_dist():
    if os.path.isdir(root_dir):
        shutil.rmtree(root_dir)


def zipper():
    shutil.make_archive(os.path.join(bot_path, name), format='zip', root_dir=root_dir)


def git_commit_file(repo_path, commit_message, remote_name='origin', branch_name='master'):
    try:
        os.chdir(repo_path)

        # Add the file to the index
        subprocess.run(["git", "add", '.'])

        # Commit the file with the provided commit message
        subprocess.run(["git", "commit", "-m", commit_message])

        # Push the changes to the remote repository
        subprocess.run(["git", "push", remote_name, branch_name])

        print(f"Committed file '{repo_path}' successfully.")
    except Exception as e:
        print(f"Error: {e}")


def copy_images():
    shutil.copytree('images/needles', 'dist/images/needles')


def copy_config():
    shutil.copy('config.json', 'dist')


def build():
    # subprocess.call(r"pyinstaller --onefile --collect-submodules vendor main.py")
    # subprocess.call(fr"pyinstaller --distpath {bot_path} main.spec")
    # subprocess.call(r"pyinstaller --onedir --distpath ./dist main.py")
    # subprocess.call(r"pyinstaller main.py")
    # subprocess.call(r"pyinstaller --distpath ./test main-one-file.spec")
    # subprocess.call(r"pyinstaller --distpath ./dist main.spec")
    subprocess.call(r"pyinstaller main.spec")


def copy_files():
    shutil.copytree('images/needles', 'dist/main/images/needles')
    shutil.copytree('translations', 'dist/main/translations')
    shutil.copy('config.json', 'dist/main')


def create_symlink():
    file = f'{name}.lnk'
    original_file_path = os.path.join(root_dir, file)
    symlink_path = os.path.join(bot_path, 'main', 'bot.exe')

    # Create a shortcut object
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(original_file_path)

    # Set the target path for the shortcut
    shortcut.TargetPath = symlink_path

    # Save the shortcut
    shortcut.Save()


remove_files_and_folders(folder_path=root_dir, ignore=['.git', 'README.md', 'version.json'])
build()
copy_files()
# create_symlink()
git_commit_file(repo_path=bot_path, commit_message="Automatic build update")
