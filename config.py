#ekrāna parametri
WIDTH = 1280    #32*40
HEIGHT = 640    #32*20
TILESIZE = 32
FPS = 60
LEVEL_UP_DELAY = 15000 #15sekundes skaitlis ir milisekundēs
ENEmy_SPAWN_DELAY = 2500 #ik pēc 2.5 sekundes parādās jauni pretinieki

#Slāņu izvietojums
PLAYER_LAYER = 4
ENEMY_LAYER = 3
BLOCK_LAYER = 2
GROUND_LAYER = 1

PLAYER_STATS = {"mage": {"damage" : 6, "speed": 3, "hp": 20, "range": 3, "shotspeed": 0.5, "level": 0},
                "peasant": {"damage" : 2, "speed": 4, "hp": 30, "range": 2, "shotspeed": 0.5, "level": 0},
                "soldier": {"damage" : 4, "speed": 2, "hp": 45, "range": 1,"shotspeed": 0.5, "level": 0}}

ENEMY_STATS = {"basic": {"damage" : 2, "speed": 1, "hp": 10},
               "lowhp": {"damage" : 8, "speed": 2, "hp": 5},
               "lowdmg": {"damage" : 2, "speed": 3, "hp": 15},
               "lowspeed": {"damage" : 5, "speed": 1, "hp": 30},}


PLAYER_LEVELS = {"mage": {"1": {"damage" : 7, "speed": 3, "hp": 20, "range": 3, "shotspeed": 0.5, "level": 1},
                          "2": {"damage" : 7, "speed": 3, "hp": 25, "range": 3, "shotspeed": 0.5, "level": 2},
                          "3": {"damage" : 7, "speed": 3, "hp": 30, "range": 3, "shotspeed": 0.5, "level": 3},
                          "4": {"damage" : 7, "speed": 3, "hp": 35, "range": 3, "shotspeed": 0.5, "level": 4},
                          "5": {"damage" : 8, "speed": 3, "hp": 35, "range": 3, "shotspeed": 0.45, "level": 5},
                          "6": {"damage" : 8, "speed": 4, "hp": 35, "range": 3, "shotspeed": 0.45, "level": 6},
                          "7": {"damage" : 8, "speed": 5, "hp": 35, "range": 3, "shotspeed": 0.45, "level": 7},
                          "8": {"damage" : 8, "speed": 5, "hp": 35, "range": 3, "shotspeed": 0.45, "level": 8},
                          "9": {"damage" : 8, "speed": 5, "hp": 35, "range": 3, "shotspeed": 0.45, "level": 9},
                          "10": {"damage" : 10, "speed": 5, "hp": 45, "range": 3, "shotspeed": 0.4, "level": 10},
                          "11": {"damage" : 10, "speed": 5, "hp": 45, "range": 3, "shotspeed": 0.4, "level": 11},
                          "12": {"damage" : 12, "speed": 5, "hp": 45, "range": 3, "shotspeed": 0.4, "level": 12},
                          "13": {"damage" : 12, "speed": 5, "hp": 45, "range": 3, "shotspeed": 0.4, "level": 13},
                          "14": {"damage" : 14, "speed": 5, "hp": 45, "range": 3, "shotspeed": 0.4, "level": 14},
                          "15": {"damage" : 15, "speed": 6, "hp": 50, "range": 3, "shotspeed": 0.3, "level": 15},
                          "16": {"damage" : 16, "speed": 6, "hp": 50, "range": 3, "shotspeed": 0.3, "level": 16},
                          "17": {"damage" : 17, "speed": 6, "hp": 50, "range": 3, "shotspeed": 0.3, "level": 17},
                          "18": {"damage" : 18, "speed": 6, "hp": 50, "range": 3, "shotspeed": 0.3, "level": 18},
                          "19": {"damage" : 19, "speed": 6, "hp": 50, "range": 3, "shotspeed": 0.3, "level": 19},
                          "20": {"damage" : 20, "speed": 6, "hp": 50, "range": 3, "shotspeed": 0.25, "level": 20},
                          },
                 "peasant": {"1": {"damage" : 3, "speed": 4, "hp": 30, "range": 2, "shotspeed": 0.5, "level": 1},
                          "2": {"damage" : 3, "speed": 4, "hp": 35, "range": 2, "shotspeed": 0.5, "level": 2},
                          "3": {"damage" : 3, "speed": 4, "hp": 35, "range": 2, "shotspeed": 0.5, "level": 3},
                          "4": {"damage" : 3, "speed": 4, "hp": 35, "range": 2, "shotspeed": 0.5, "level": 4},
                          "5": {"damage" : 5, "speed": 4, "hp": 40, "range": 2, "shotspeed": 0.45, "level": 5},
                          "6": {"damage" : 5, "speed": 4, "hp": 40, "range": 2, "shotspeed": 0.45, "level": 6},
                          "7": {"damage" : 5, "speed": 5, "hp": 40, "range": 3, "shotspeed": 0.45, "level": 7},
                          "8": {"damage" : 5, "speed": 5, "hp": 40, "range": 3, "shotspeed": 0.45, "level": 8},
                          "9": {"damage" : 5, "speed": 5, "hp": 40, "range": 3, "shotspeed": 0.45, "level": 9},
                          "10": {"damage" : 5, "speed": 5, "hp": 45, "range": 3, "shotspeed": 0.4, "level": 10},
                          "11": {"damage" : 8, "speed": 5, "hp": 45, "range": 3, "shotspeed": 0.4, "level": 11},
                          "12": {"damage" : 8, "speed": 5, "hp": 45, "range": 3, "shotspeed": 0.4, "level": 12},
                          "13": {"damage" : 8, "speed": 5, "hp": 45, "range": 3, "shotspeed": 0.4, "level": 13},
                          "14": {"damage" : 8, "speed": 5, "hp": 45, "range": 3, "shotspeed": 0.4, "level": 14},
                          "15": {"damage" : 8, "speed": 6, "hp": 55, "range": 3, "shotspeed": 0.3, "level": 15},
                          "16": {"damage" : 8, "speed": 6, "hp": 55, "range": 3, "shotspeed": 0.3, "level": 16},
                          "17": {"damage" : 10, "speed": 6, "hp": 55, "range": 3, "shotspeed": 0.25, "level": 17},
                          "18": {"damage" : 10, "speed": 8, "hp": 65, "range": 3, "shotspeed": 0.25, "level": 18},
                          "19": {"damage" : 10, "speed": 8, "hp": 65, "range": 3, "shotspeed": 0.25, "level": 19},
                          "20": {"damage" : 15, "speed": 8, "hp": 65, "range": 3, "shotspeed": 0.2, "level": 20},
                          },
                 "soldier": {"1": {"damage" : 4, "speed": 2, "hp": 45, "range": 1, "shotspeed": 0.5, "level": 1},
                          "2": {"damage" : 4, "speed": 2, "hp": 55, "range": 3, "shotspeed": 0.5, "level": 2},
                          "3": {"damage" : 4, "speed": 2, "hp": 60, "range": 3, "shotspeed": 0.5, "level": 3},
                          "4": {"damage" : 4, "speed": 2, "hp": 65, "range": 3, "shotspeed": 0.5, "level": 4},
                          "5": {"damage" : 6, "speed": 2, "hp": 70, "range": 3, "shotspeed": 0.45, "level": 5},
                          "6": {"damage" : 6, "speed": 3, "hp": 75, "range": 3, "shotspeed": 0.45, "level": 6},
                          "7": {"damage" : 6, "speed": 3, "hp": 80, "range": 3, "shotspeed": 0.45, "level": 7},
                          "8": {"damage" : 6, "speed": 3, "hp": 85, "range": 3, "shotspeed": 0.45, "level": 8},
                          "9": {"damage" : 8, "speed": 3, "hp": 90, "range": 3, "shotspeed": 0.45, "level": 9},
                          "10": {"damage" : 8, "speed": 4, "hp": 95, "range": 3, "shotspeed": 0.4, "level": 10},
                          "11": {"damage" : 8, "speed": 4, "hp": 100, "range": 3, "shotspeed": 0.4, "level": 11},
                          "12": {"damage" : 8, "speed": 4, "hp": 105, "range": 3, "shotspeed": 0.4, "level": 12},
                          "13": {"damage" : 8, "speed": 4, "hp": 110, "range": 3, "shotspeed": 0.4, "level": 13},
                          "14": {"damage" : 8, "speed": 4, "hp": 115, "range": 3, "shotspeed": 0.4, "level": 14},
                          "15": {"damage" : 8, "speed": 4, "hp": 115, "range": 3, "shotspeed": 0.35, "level": 15},
                          "16": {"damage" : 8, "speed": 4, "hp": 115, "range": 3, "shotspeed": 0.35, "level": 16},
                          "17": {"damage" : 10, "speed": 4, "hp": 115, "range": 3, "shotspeed": 0.35, "level": 17},
                          "18": {"damage" : 10, "speed": 4, "hp": 115, "range": 3, "shotspeed": 0.35, "level": 18},
                          "19": {"damage" : 10, "speed": 5, "hp": 150, "range": 3, "shotspeed": 0.35, "level": 19},
                          "20": {"damage" : 10, "speed": 5, "hp": 200, "range": 3, "shotspeed": 0.35, "level": 20},
                          },}

DAMAGE_COOLDOWN = 1

#Krāsa
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#karte
tilemap = [
    '########################################',
    '#.E..................................E.#',
    '#E......####..........................E#',
    '#...........#..........................#',
    '#..........................E...........#',
    '#......................................#',
    '#.....S..........................S.....#',
    '#......................................#',
    '#..........................E...........#',
    '#...............................##.....#',
    '#................................#.....#',
    '#.................P..............#.....#',
    '#......................................#',
    '#.....S..........................S.....#',
    '#...........E..............E...........#',
    '#......................................#',
    '#......................................#',
    '#ES...................................E#',
    '#.E..................................E.#',
    '########################################',           
]