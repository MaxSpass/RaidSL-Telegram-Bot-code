# Prepare your Windows
- install [Python 3.7](https://www.python.org/downloads/release/python-370/)
- install [OpenCV](https://github.com/opencv/opencv/releases), ([Install OpenCV-Python in Windows](https://docs.opencv.org/4.x/d5/de5/tutorial_py_setup_in_windows.html))
- install [Tesseract](https://tesseract-ocr.github.io/tessdoc/Downloads.html)

# Setting up the project
- clone the repository
- rename `.env.example` to `.env` and provide necessary variables
- run `python -m venv venv`
- run `venv\Scripts\activate` (on Windows only)
- run `pip install -r requirements.txt`

# Dev Tips
- new package installation `pip install [PACKAGE_NAME] | pip freeze > requirements.txt`
- make sure that your IDEA is already configured for using interpreter form the venv
- [pyenv](https://github.com/pyenv-win/pyenv-win/blob/master/docs/installation.md#add-system-settings) is a handy package for managing different python versions


# Useful Links

[Tasks](https://trello.com/b/qdmlcWUO/main-board)

[Notes](https://docs.google.com/document/d/1C7tJGxA2pyR1sg199nGUARYVfYpPSZ3VN1rhYFKvM1E/edit?usp=sharing)

[Packaging Python](https://packaging.python.org/en/latest/tutorials/installing-packages/#requirements-files)

[PyGetWindow-DOCS](https://github.com/asweigart/PyGetWindow)

# TODO
  - [x] Arena Live
  - [x] Arena Classic
  - [x] Arena Tag
  - [x] Demon lord
  - [x] Dungeons
  - [x] Doom tower
  - [x] Hydra
  - [x] Faction wars
  - [x] Twin Fortress guard
  - [x] Rewards
  - [x] Report
  - [x] Screen
  - [x] Restart/Launch
  - [x] Quests "Daily"
  - [ ] Quests "Weekly"
  - [ ] Quests "Monthly"
  - [x] Telegram Bot :: Integration
  - [x] Telegram Bot :: Async commands
  - [ ] GUI