import sys
import math
import numpy as np

from collections import namedtuple

Entity = namedtuple('Entity', [
    'id', 'type', 'x', 'y', 'shield_life', 'is_controlled', 'health', 'vx', 'vy', 'near_base', 'threat_for'
])

TYPE_MONSTER = 0
TYPE_MY_HERO = 1
TYPE_OP_HERO = 2


def get_distance(v):
    return round(math.sqrt(v.dot(v)))


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# base_x: The corner of the map representing your base
base_x, base_y = [int(i) for i in input().split()]
base = {'pos': np.array((base_x, base_y))}
print(base, file=sys.stderr, flush=True)
enemy_base = {'pos': np.array((17630, 9000)) if base['pos'][0] == 0 else np.array((0, 0))}
heroes_per_player = int(input())  # Always 3
heroes = []
op_heroes = []
initialized = False
home_positions = [0.8 * base['pos'] + 0.2 * enemy_base['pos'], 0.7 * base['pos'] + 0.3 * enemy_base['pos']]


def keyDistance(m):
    return m['dist']


def keyScore(m):
    return m['score']


# game loop
while True:
    our_mana = 0
    for i in range(2):
        # health: Each player's base health
        # mana: Ignore in the first league; Spend ten mana to cast a spell
        _health, _mana = [int(j) for j in input().split()]
        if i == 0:
            base['health'] = _health
            base['mana'] = _mana
        else:
            enemy_base['health'] = _health
            enemy_base['mana'] = _mana
    mana = base['mana']
    entity_count = int(input())  # Amount of heros and monsters you can see
    monsters = []
    enemy_monsters = []
    neutral_monsters = []
    heroes = []
    op_heroes = []
    for i in range(entity_count):
        # _id: Unique identifier
        # _type: 0=monster, 1=your hero, 2=opponent hero
        # x: Position of this entity
        # shield_life: Ignore for this league; Count down until shield spell fades
        # is_controlled: Ignore for this league; Equals 1 when this entity is under a control spell
        # health: Remaining health of this monster
        # vx: Trajectory of this monster
        # near_base: 0=monster with no target yet, 1=monster targeting a base
        # threat_for: Given this monster's trajectory, is it a threat to 1=your base, 2=your opponent's base, 0=neither
        _id, _type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for = [int(j) for j in input().split()]
        if _type == TYPE_MONSTER:
            if near_base == 0 and threat_for != 2 and shield_life == 0 and is_controlled == 0:
                neutral_monsters.append({'id': _id, 'pos': np.array((x, y)), 'vel': np.array((vx, vy)), 'health': health})
            if threat_for == 1:
                monsters.append({'pos': np.array((x, y)), 'vel': np.array((vx, vy)), 'health': health})
            elif threat_for == 2:
                enemy_monsters.append({'id': _id, 'pos': np.array((x, y)), 'vel': np.array((vx, vy)), 'health': health, 'controlled': is_controlled, 'shield': shield_life})
        elif _type == TYPE_MY_HERO:
            heroes.append({'pos': np.array((x, y))})
        elif _type == TYPE_OP_HERO:
            op_heroes.append({'pos': np.array((x, y)), 'id': _id})
            print(op_heroes[-1]['pos'], file=sys.stderr, flush=True)

    # Arrange monsters targeting us by distance
    for monster in monsters:
        monster['dist'] = get_distance(base['pos'] - monster['pos'])
    monsters.sort(key=keyDistance)
    # print(monsters, file=sys.stderr, flush=True)

    # Arrange monsters targeting enemy by score
    for monster in enemy_monsters:
        monster['score'] = monster['health'] / get_distance(enemy_base['pos'] - monster['pos'])
    enemy_monsters.sort(key=keyScore, reverse=True)
    print(enemy_monsters, file=sys.stderr, flush=True)

    for i in range(len(heroes)):
        hero = heroes[i]
        action = None
        target = None
        if i != 2:
            if len(monsters) > 2:
                if i == 0 and mana >= 10 and monsters[2]['dist'] < 4000:
                    action = 'SPELL WIND'
                    mana -= 10
                    # target = heroes[1]['pos'] - monsters[0]['pos']
                    target = enemy_base['pos']
            if target is None:
                action = 'MOVE'
                if len(monsters) > i:
                    target = monsters[i]['pos'] + monsters[i]['vel']
                else:
                    target = home_positions[i]
                # if get_distance(hero['pos'] - base['pos']) < 5000 * (i + 1):
                #     target = hero['pos'] + np.array([1000 * (x - 0.5) for x in np.random.random(2)])
        else:
            if len(neutral_monsters) > 0:
                if mana > 10 and action is None:
                    for neutral in neutral_monsters:
                        neutral['dist'] = get_distance(neutral['pos'] - hero['pos'])
                    neutral_monsters.sort(key=keyDistance)
                    closest_monster = neutral_monsters[0]
                    if get_distance(closest_monster['pos'] - hero['pos']) < 2200:
                        action = 'SPELL CONTROL ' + str(closest_monster['id'])
                        target = enemy_base['pos']
                        mana -= 10
                    else:
                        action = 'MOVE'
                        target = closest_monster['pos'] - 2 * closest_monster['vel']
            if action is None:
                action = 'MOVE'
                target = 0.5 * enemy_base['pos'] + 0.5 * base['pos']
                # target = monsters[0]['pos'] + monsters[0]['vel']
                # np.array([1000 * x  for x in np.random.random(2)]) * (1 if other_base[0] == 0 else -1)

        # In the first league: MOVE <x> <y> | WAIT; In later leagues: | SPELL <spellParams>;
        if action is None:
            action = 'WAIT'
        if target is not None:
            action = ' '.join([action, str(int(target[0])), str(int(target[1]))])
        print(action, file=sys.stderr, flush=True)
        print(action)

