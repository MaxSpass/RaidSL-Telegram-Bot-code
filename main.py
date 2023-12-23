from features.live_arena.index import *
from features.arena.index import *
from features.demon_lord.index import *
from features.iron_twins_fortress.index import *
from features.faction_wars.index import *
from features.rewards.index import *
from features.hero_filter.index import *
from features.dungeons.core import *
from helpers.common import *
from constants.index import *
import sys
import itertools


def prepare():
    prepare_window()
    sleep(.5)


rewards = Rewards()
hero_filter = HeroFilter()
# @TODO Should be moved to the .env config file
arena_live = ArenaLive(
    pool=[
        'Arbiter',
        'Sun Wukong',
        'Cupidus',
        'Venus',
        'Duchess Lilitu',
    ],
    leaders=[
        'Arbiter',
        'Sun Wukong',
    ],
    # pool=[
    #     'Warlord',
    #     'Sun Wukong',
    #     'Arbiter',
    #     'Trunda',
    #     'Duchess Lilitu',
    # ],
    # leaders=[
    #     'Arbiter',
    #     'Sun Wukong',
    # ],
)

# def flat(arr):
#     return list(itertools.chain.from_iterable(arr))

def start():
    log('Executing automatic scenarios...')
    start_time = datetime.now()

    # arena_classic._show_results([])

    # demon_lord()
    arena_live.run()
    # arena_classic.run()
    # arena_tag.run()
    # rewards.quests_run()
    # faction_wars()
    # iron_twins_fortress()
    # rewards.quests_run()
    # arena_tag.run()
    #
    # DungeonCore(DUNGEON_FIRE, [65], props={
    #     'allow_super_raid': True
    # }).run()

    arena_live.report()
    arena_classic.report()
    arena_tag.report()

    log('All scenarios are done!')
    print('Duration: {}'.format(datetime.now() - start_time))


# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# noise removal
def remove_noise(image):
    return cv2.medianBlur(image, 5)


# thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


# dilation
def dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)


# erosion
def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations=1)


# opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


# canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)


# skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)

    else:
        angle = -angle
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return rotated


# template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)


def main():
    # pyautogui.FAILSAFE = True
    # r = []
    # l = [True]
    # r.append(l)
    # log(flat(l))
    # log(flatten([l]))
    # log(flatten(r))
    # return

    try:
        prepare()
        if is_index_page() is True:
            start()
        else:
            go_index_page()
            start()
    except KeyboardInterrupt:
        sys.exit()


if __name__ == "__main__":
    main()
