import os
import shutil
import subprocess

root_dir = os.path.join(os.getcwd(), 'dist')
name = 'RAID-stop-routine-BOT'

def clear_dist():
    if os.path.isdir(root_dir):
        shutil.rmtree(root_dir)

def zipper():
    shutil.make_archive(name, format='zip', root_dir=root_dir)

def copy_images():
    shutil.copytree('images/needles', 'dist/images/needles')

def copy_config():
    shutil.copy('config.json', 'dist')

def build():
    subprocess.call(r"pyinstaller main.spec")
    # subprocess.call(r"pyinstaller --onefile main.py")

clear_dist()
build()
copy_images()
copy_config()
zipper()