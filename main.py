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
    pytesseract.pytesseract.tesseract_cmd = _path
else:
    # @TODO Should be in the env file
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
        'runs_limit': 2,
        'runs': [
            {
                'stage': 4,
                'team_preset': 1,
                'min_damage': 170,
                'skip': 0
            },
            {
                'stage': 3,
                'team_preset': 4,
                'min_damage': 50,
                'skip': 0
            },
            {
                'stage': 1,
                'team_preset': 3,
                'min_damage': 200,
                'skip': 0
            },
        ],
    }
    DUNGEON_PROPS = {
        "bank": False,
        "refill": False,
        "super_raid": False,
        "locations": [
            {"id": 6, "energy": 40},
            {"id": 3, "energy": 40},
        ]
    }

    app.load_config({
        'tasks': [
            {'name': 'dungeon', 'enable': 1, 'props': DUNGEON_PROPS},
            {'name': 'arena_live', 'enable': 0, 'props': ARENA_LIVE_PROPS},
            {'name': 'hydra', 'enable': 0, 'props': HYDRA_PROPS},
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
    # live_arena_props = list(filter(lambda x: x['name'] == 'arena_live', app.config['tasks']))[0]['props']

    # pool = [
    #     {'name': 'Arbiter', 'role': 's', 'priority': 1},
    #     {'name': 'Sun Wukong', 'role': 'a', 'priority': 1},
    #     {'name': 'Duchess Lilitu', 'role': 's', 'priority': 1},
    #     {'name': 'Cupidus', 'role': 'a', 'priority': 1},
    #     {'name': 'Venus', 'role': 's', 'priority': 1},
    #     {'name': 'Leorius the Proud', 'role': 'a'},
    #     {'name': 'Rotos', 'role': 'a'},
    #     {'name': 'Mortu-Macaab', 'role': 'a'},
    #     {'name': 'Ramantu Drakesblood', 'role': 'a'},
    #     {'name': 'Candraphon', 'role': 'a'},
    #     {'name': 'Lady Mikage', 'role': 's'},
    #     {'name': 'Pythion', 'role': 's'},
    #     {'name': 'Maulie Tankard', 'role': 's'},
    #     {'name': 'Lydia the Deathsiren', 'role': 's'},
    #     {'name': 'Mighty Ukko', 'role': 's'},
    # ]
    #
    # def is_available_with_probability():
    #     return random.random() < .3
    #
    # def find_closest_element(pool, target_role, taken_elements):
    #     while True:
    #         alternatives = []
    #         for element in pool:
    #             if element['role'] == target_role and element['name'] not in taken_elements:
    #                 alternatives.append(element)
    #
    #         if alternatives:
    #             closest_element = min(alternatives, key=lambda x: pool.index(x))
    #             taken_elements.add(closest_element['name'])  # Mark the element's name as taken
    #             return closest_element
    #         else:
    #             # If no alternatives are available, keep retrying
    #             return None
    #
    # pattern = ['s', 'a', 's', 'a', 's']
    # taken_elements = {'Arbiter', 'Cupidus', 'Venus'}
    #
    # team = list(map(lambda r: find_closest_element(pool, r, taken_elements), pattern))
    #
    # for i in range(len(team)):
    #     print(team[i])
    #
    # return

    # # Find and disable the closest 's' element with 50% probability
    # closest_s_element = find_closest_element(pool, 's')
    # if closest_s_element:
    #     print(f'Closest 's' element: {closest_s_element['name']}')
    # else:
    #     print('No available 's' element')
    #
    # # Find and disable the closest 'a' element with 50% probability
    # closest_a_element = find_closest_element(pool, 'a')
    # if closest_a_element:
    #     print(f'Closest 'a' element: {closest_a_element['name']}')
    # else:
    #     print('No available 'a' element')
    #
    # return

    # log(pyautogui.pixel(50, 470))

    # return
    # image = os.path.join(os.getcwd(), 'images/screens/' + 'live_arena_picking_characters.jpg')
    # show_image(image)
    # return
    #
    # original_list = [1,2,3,4,5]
    #
    # # # Archive into [[1], [2,3], [4,5]]
    # # result_1 = archive_list(original_list, [1, 2, 2])
    # # print(result_1)
    # #
    # # Archive into [[1,2], [3,4], [5]]
    # result_2 = archive_list(original_list, [2, 1])
    # print(result_2)
    # #
    # return

    # team = [
    #         'Arbiter',
    #         'Sun Wukong',
    #         'Duchess Lilitu',
    #         'Mighty Ukko',
    #         'Lydia the Deathsiren',
    #         'Pythion',
    #     ]
    #
    # old_leaders = [
    #     'Mortu-Macaab',
    #     'Pythion',
    #     'Mighty Ukko',
    # ]
    #
    # leaders = []
    #
    # counter = 0
    # while len(leaders) < 2:
    #     l = old_leaders[counter]
    #     if l in team:
    #         leaders.append(team.index(l))
    #     counter += 1
    #
    # leaders.reverse()
    #
    # return leaders
    #
    # log(leaders)

    # i, char = find(live_arena_props['pool'], lambda x: x.get('role') == 's')
    # log(char)
    # return

    # IS_FIRST = False
    # live_arena_props = list(filter(lambda x: x['name'] == 'arena_live', app.config['tasks']))[0]['props']

    # if False:
    #     # opponent_team = {'Sun Wukong', 'Duchess Lilitu', 'Lydia the Deathsiren'}
    #     # opponent_team = {'Arbiter', 'Rotos', 'Tormin', 'Sun Wukong', 'Duchess Lilitu', 'Lydia the Deathsiren'}
    #
    #     pool = live_arena_props['pool']
    #     leaders = live_arena_props['leaders']
    #     sorted_pool = sorted(pool, key=lambda x: (-x.get('priority', 0), x.get('priority', 0)))
    #     roles = list(map(lambda x: x['role'], sorted_pool[:5]))
    #     roles_counter = 0
    #     pattern = [1, 2, 2]
    #     team = []
    #     opponent_team = []
    #
    #     # test
    #     # enemy_team = sorted_pool
    #     def test_opponent_pick():
    #         picked_hero = None
    #
    #         while picked_hero is None:
    #             picked_hero = random.choice(sorted_pool)
    #             if picked_hero['name'] not in opponent_team:
    #                 opponent_team.append(picked_hero['name'])
    #
    #         # picked_hero = pop_random_element(sorted_pool)
    #         return picked_hero
    #
    #     def next_character(role):
    #         next_char = None
    #         counter = 0
    #
    #         while next_char is None:
    #             i, char = find(sorted_pool[counter:], lambda x: x.get('role') == role)
    #
    #             if char:
    #                 exists_my_team = find(team, lambda x: x.get('name') == char['name'])[1]
    #                 exists_opponent_team = find(opponent_team, lambda name: name == char['name'])[1]
    #                 if not exists_my_team and not exists_opponent_team:
    #                     next_char = char
    #
    #             counter += 1
    #
    #         return next_char
    #
    #     if not IS_FIRST:
    #         pattern.reverse()
    #
    #     for i in range(len(pattern)):
    #         # test
    #         for j in range(pattern[i]):
    #             test_opponent_pick()
    #
    #             unit = next_character(roles[roles_counter])
    #             team.append(unit)
    #             roles_counter += 1
    #
    #     # log(team)
    #
    #     print('***   TEAM   ***')
    #     for c in range(len(team)):
    #         print(team[c]['name'])
    #     print('==============================')
    #
    #     # print('***   Picked   ***')
    #     # for character in opponent_team:
    #     #     print(character)
    #
    #     return
    #
    #     # print(team)
    #
    #     # team_core = archive_list(sorted_pool, pattern)
    #     # team_rest = sorted_pool[5:len(pool)]
    #
    #     # selected_elements = []
    #     # for character in team_core:
    #     #     name = character['name']
    #     #     role = character['role']
    #     #
    #     #     # Check if the here is already picked by opponent
    #     #     free = name not in opponent_team
    #     #
    #     #     # Append the element only if it exists in the database
    #     #     if free:
    #     #         # pick from the priority pool
    #     #         selected_elements.append(name)
    #     #     else:
    #     #         # pick from the alternative set
    #     #         i, el = find(team_rest, lambda x: x['role'] == role)
    #     #         team_rest.pop(i)
    #     #         selected_elements.append(el['name'])
    #     #
    #     # filtered_leaders = list(filter(lambda x: x in team, leaders))[:2]

    # hydra_props = list(filter(lambda x: x['name'] == 'hydra', app.config['tasks']))[0]['props']
    # hydra = Hydra(hydra_props)
    # screens = hydra._certain_hydra_or_all_hydra_screens()
    #
    # if screens[0]:
    #     print('certain_hydra')
    # elif screens[1]:
    #     print('all_hydra_screens')
    #
    # return

    # hydra.current_stage = hydra._prepare_run_props(hydra.runs[0])
    # hydra.scan()

    # region = axis_to_region(820, 470, 870, 500)
    # screenshot = pyautogui.screenshot(region=region)
    # show_pyautogui_image(screenshot)

    # for i in range(10):
    # dmg = read_dealt_damage()
    # dmg = read_energy_cost()
    # log(dmg)

    #     swipe('top', 566, 80, 428, speed=.5)
    # swipe('bottom', 566, 508, 435, speed=1.5)
    # track_mouse_position()
    # return

    # dungeons_props = list(filter(lambda x: x['name'] == 'dungeon', app.config['tasks']))[0]['props']
    # print(dungeons_props)

    # check_image(axis_to_region(504, 32, 567, 64))
    # return

    # for i in range(10):
    #     log(read_energy_bank())
    # log(read_energy_bank())
    # bank = read_energy_bank()
    # log(bank)
    # return


    # show_pyautogui_image(pyautogui.screenshot(region=axis_to_region(332, 38, 414, 56)))
    # return

    # log(pyautogui.pixel(850, 475))
    # return

    # dungeons = Dungeons({
    #     "bank": 60,
    #     "locations": [
    #         {"id": 6},
    #         {"id": 3, "energy": 40, "super_raid": 1},
    #     ]
    # })
    # dungeons.run()
    # return

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
