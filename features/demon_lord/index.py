from helpers.common import *

# demon lord | levels for attack
DEMON_LORD_LEVELS_FOR_ATTACK = [6, 5]
# demon lord | clicking areas for obtaining rewards
DEMON_LORD_REWARD_COORDINATES = {
    3: (580, 120),
    4: (580, 200),
    5: (580, 300),
    6: (580, 380),
}


# @TODO Must be reworked by following new standard
def demon_lord():
    def enter():
        # moving to the Demon Lord
        # click on the red button "Battles"
        battles_click()
        sleep(1)
        # click on the clan boss
        click(890, 300)
        sleep(1)
        # click on the Demon Lord
        click(320, 290)
        sleep(1)

        # swapping to the bottom @TODO
        pyautogui.moveTo(580, 400, 1)
        pyautogui.dragTo(580, 120, duration=1)
        sleep(2)

    def obtain():
        global DEMON_LORD_LEVELS_FOR_ATTACK
        global DEMON_LORD_REWARD_COORDINATES
        # obtain rewards
        for lvl in DEMON_LORD_REWARD_COORDINATES:
            x = DEMON_LORD_REWARD_COORDINATES[lvl][0]
            y = DEMON_LORD_REWARD_COORDINATES[lvl][1]
            click(x, y)
            sleep(0.5)
            str_lvl = str(lvl)
            if pixel_check_old(870, 457, [246, 0, 0]):
                # click on the "Claim reward button"
                click(870, 457)
                sleep(1)
                # click on the "Obtain reward button"
                click(460, 444)
                sleep(1)
                # click on the "Obtain reward button"
                click(460, 444)
                log('Obtained reward from Demon Lord ' + str_lvl)
            else:
                log('No reward found from Demon Lord ' + str_lvl)
            sleep(2)

    def attack():
        global DEMON_LORD_LEVELS_FOR_ATTACK
        global DEMON_LORD_REWARD_COORDINATES
        # attack
        for i in range(len(DEMON_LORD_LEVELS_FOR_ATTACK)):
            # zero-indexed Demon Lord level is always next
            lvl = DEMON_LORD_LEVELS_FOR_ATTACK[0]
            x = DEMON_LORD_REWARD_COORDINATES[lvl][0]
            y = DEMON_LORD_REWARD_COORDINATES[lvl][1]
            # click on the certain demon lord
            click(x, y)
            # pyautogui.moveTo(x, y, 1)
            # DEMON_LORD_LEVELS_FOR_ATTACK.remove(lvl)
            sleep(.5)
            # prepare to battle
            click(860, 480)
            sleep(.5)
            # start battle
            click(860, 480)
            if pixel_wait('End of the battle with Demon Lord: ' + str(lvl) + ' level', 20, 112, [255, 255, 255], 3):
                # return to the demon lord menu
                click(420, 490)
                close_popup()
                sleep(2)
                # removing already attacked Demon Lord from the array
                DEMON_LORD_LEVELS_FOR_ATTACK.remove(lvl)

    def finish():
        go_index_page()
        log('DONE - Demon Lord')

    enter()
    obtain()
    attack()
    finish()
