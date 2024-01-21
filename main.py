import pyautogui
import sys
import random
import traceback
import pytesseract
from classes.app import *
from constants.index import IS_DEV
# from features.hydra.index import *

app = App()

if not IS_DEV and getattr(sys, 'frozen', False):
    _path = os.path.join(sys._MEIPASS, './vendor/tesseract/tesseract.exe')
    print(_path)
    pytesseract.pytesseract.tesseract_cmd =_path
else:
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

if IS_DEV:
    ARENA_LIVE_PROPS = {
        'pool': [
            {'name': 'Arbiter', 'role': 's', 'priority': 1},
            {'name': 'Sun Wukong', 'role': 'a', 'priority': 1},
            {'name': 'Duchess Lilitu', 'role': 's', 'priority': 1},
            {'name': 'Cupidus', 'role': 'a', 'priority': 1},
            {'name': 'Venus', 'role': 's', 'priority': 1},
            {'name': 'Leorius the Proud', 'role': 'a'},
            {'name': 'Rotos', 'role': 'a'},
            {'name': 'Mortu-Macaab', 'role': 'a'},
            {'name': 'Ramantu Drakesblood', 'role': 'a'},
            {'name': 'Candraphon', 'role': 'a'},
            {'name': 'Lady Mikage', 'role': 's'},
            {'name': 'Pythion', 'role': 's'},
            {'name': 'Maulie Tankard', 'role': 's'},
            {'name': 'Lydia the Deathsiren', 'role': 's'},
            {'name': 'Mighty Ukko', 'role': 's'},
        ],
        'leaders': [
            'Arbiter',
            'Sun Wukong',
            'Mortu-Macaab',
            'Duchess Lilitu',
            'Mighty Ukko',
            'Lydia the Deathsiren',
            'Pythion',
        ],
        'refill': 1
    }
    HYDRA_PROPS = {
        'runs_limit': 5,
        'runs': [
            {
                'stage': 4,
                'team_preset': 1,
                'min_damage': 170,
                'skip': 1
            },
            {
                'stage': 3,
                'team_preset': 4,
                'min_damage': 30,
                'skip': 0
            },
            {
                'stage': 1,
                'team_preset': 3,
                'min_damage': 200,
                'skip': 1
            },
        ],
    }
    DUNGEON_PROPS = {
        'location': "Sand Devil's Necropolis",
        'runs': 6,
        'allow_super_raid': 0
    }

    app.load_config({
        'tasks': [
            {'name': 'dungeon', 'enable': 0, 'props': DUNGEON_PROPS},
            {'name': 'arena_live', 'enable': 0, 'props': ARENA_LIVE_PROPS},
            {'name': 'hydra', 'enable': 1, 'props': HYDRA_PROPS},
            {'name': 'iron_twins', 'enable': 0},
            {'name': 'faction_wars', 'enable': 0},
            {'name': 'arena_classic', 'enable': 0, 'props': {'refill': 0}},
            {'name': 'arena_tag', 'enable': 0, 'props': {'refill': 0}},
            {'name': 'demon_lord', 'enable': 0},
        ],
        'after_each': [
            {'check_rewards': 1}
        ],
    })


def main():

    # hydra_props = list(filter(lambda x: x['name'] == 'hydra', app.config['tasks']))[0]['props']
    # hydra = Hydra(hydra_props)
    # hydra.current_stage = hydra._prepare_run_props(hydra.runs[0])
    # hydra.scan()

    if IS_DEV or app.validation():
        try:
            app.start()
            if is_index_page() is True:
                app.run()
            else:
                go_index_page()
                app.run()
        except KeyboardInterrupt as e:
            error = traceback.format_exc()
            log_save(error)
            return 0
        except Exception:
            error = traceback.format_exc()
            log_save(error)
            return 0
    else:
        log_save('An App is outdated')


if __name__ == '__main__':
    main()
