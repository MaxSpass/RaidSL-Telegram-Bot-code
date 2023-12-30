import shutil
import subprocess
import os

root_dir = os.path.join(os.getcwd(), 'dist')

def clear_dist():
    if os.path.isdir(root_dir):
        shutil.rmtree(root_dir)

def zipper():
    shutil.make_archive('RAID-Without_Routine_BOT', format='zip', root_dir=root_dir)

def copy_images():
    shutil.copytree('images/needles', 'dist/images/needles')

def copy_config():
    shutil.copy('config.json', 'dist')

def build():
    subprocess.call(r"pyinstaller --onefile main.py")

clear_dist()
build()
copy_images()
copy_config()
zipper()