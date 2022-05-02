import sys
import math
import numpy as np
import random

from collections import namedtuple

Entity = namedtuple('Entity', [
    'id', 'type', 'x', 'y', 'shield_life', 'is_controlled', 'health', 'vx', 'vy', 'near_base', 'threat_for'
])

TYPE_MONSTER = 0
TYPE_MY_HERO = 1
TYPE_OP_HERO = 2

MONSTER_HEALTH_THRESHOLD = 10
EARLY_ROUND_THRESHOLD = 40

MODE_CONTROL = 0
MODE_SHIELD = 1


def get_distance(v):
    return round(math.sqrt(v.dot(v)))


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# base_x: The corner of the map representing your base
base_x, base_y = [int(i) for i in input().split()]
base = {'pos': np.array((base_x, base_y))}
my_base_at_zero = base['pos'][0] == 0
print(base, file=sys.stderr, flush=True)
enemy_base = {'pos': np.array((17630, 9000)) if my_base_at_zero else np.array((0, 0))}
centre = 0.5 * enemy_base['pos'] + 0.5 * base['pos']
shield_place = enemy_base['pos'] + np.array((4450, 2270)) * (-1 if my_base_at_zero else 1)
heroes_per_player = int(input())  # Always 3
heroes = []
op_heroes = []
initialized = False
# home_positions = [0.8 * base['pos'] + 0.2 * enemy_base['pos'], 0.7 * base['pos'] + 0.3 * enemy_base['pos']]
home_positions = [base['pos'] + offset * (1 if my_base_at_zero else -1) for offset in [np.array((5500, 2000)), np.array((3200, 4900))]]
#enemy_monster_target_offsets = [np.array((0, 4000)), np.array((4000, 0)), np.array((2000, 2000))]
enemy_monster_target_offsets = [np.array((0, 3000)), np.array((3000, 0)), np.array((0, 4000)), np.array((4000, 0))]
enemy_monster_targets = []
for offset in enemy_monster_target_offsets:
    enemy_monster_targets.append(enemy_base['pos'] + offset * (-1 if my_base_at_zero else 1))
print(enemy_monster_targets, file=sys.stderr, flush=True)
round_count = 0
controlled_monsters = 0
mode = MODE_CONTROL


def keyDistance(m):
    return m['dist']


def keyScore(m):
    return m['score']


# game loop
while True:
    round_count += 1
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
    shielded_enemy_monsters = 0
    heroes = []
    op_heroes = []
    number_controlled_monsters = 0
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
            elif near_base == 1 and threat_for == 2:
                if shield_life > 0:
                    shielded_enemy_monsters += 1
                else:
                    enemy_monsters.append({'id': _id, 'pos': np.array((x, y)), 'vel': np.array((vx, vy)), 'health': health, 'controlled': is_controlled, 'shield': shield_life})
        elif _type == TYPE_MY_HERO:
            heroes.append({'pos': np.array((x, y)), 'id': _id, 'shield': shield_life})
        elif _type == TYPE_OP_HERO:
            op_heroes.append({'pos': np.array((x, y)), 'id': _id})
            print(op_heroes[-1]['pos'], file=sys.stderr, flush=True)

    # Arrange monsters targeting us by distance
    for monster in monsters:
        monster['dist'] = get_distance(base['pos'] - monster['pos'])
    monsters.sort(key=keyDistance)
    print(monsters, file=sys.stderr, flush=True)

    # Arrange monsters targeting enemy by score
    for monster in enemy_monsters:
        #monster['score'] = monster['health'] / get_distance(enemy_base['pos'] - monster['pos'])
        monster['score'] = get_distance(enemy_base['pos'] - monster['pos']) - 200 * monster['health']
    enemy_monsters.sort(key=keyScore)
    print(enemy_monsters, file=sys.stderr, flush=True)

    # Arrange opponent heroes by distance from their base
    for opp_hero in op_heroes:
        opp_hero['dist'] = get_distance(enemy_base['pos'] - opp_hero['pos'])
    op_heroes.sort(key=keyDistance)
    print(op_heroes, file=sys.stderr, flush=True)

    print(neutral_monsters, file=sys.stderr, flush=True)
    has_winded = False
    for i in range(len(heroes)):
        hero = heroes[i]
        action = None
        target = None
        closest_op_hero = 999999 if len(op_heroes) == 0 else min([get_distance(hero['pos'] - op_hero['pos']) for op_hero in op_heroes])
        if hero['shield'] == 0 and round_count > 40 and mana > 10 and closest_op_hero < 2500:
            action = 'SPELL SHIELD ' + str(hero['id'])
        elif i != 2:
            if len(monsters) > 0:
                # print(monsters[0]['dist'], file=sys.stderr, flush=True)
                # print(get_distance(monsters[0]['pos'] - hero['pos']), file=sys.stderr, flush=True)
                if not has_winded and mana >= 10 and monsters[0]['dist'] < 800 and get_distance(monsters[0]['pos'] - hero['pos']) < 1280:
                    action = 'SPELL WIND'
                    # target = heroes[1]['pos'] - monsters[0]['pos']
                    target = enemy_base['pos']
                    has_winded = True
            if target is None and len(monsters) > 0:
                action = 'MOVE'
                target_monster = min(i, len(monsters) - 1)
                target = monsters[target_monster]['pos'] - 0 * monsters[target_monster]['vel']
            if target is None:
                action = 'MOVE'
                target = home_positions[i]
                # if get_distance(hero['pos'] - base['pos']) < 5000 * (i + 1):
                #     target = hero['pos'] + np.array([1000 * (x - 0.5) for x in np.random.random(2)])
        else:
            if len(neutral_monsters) > 0:
                for neutral in neutral_monsters:
                    neutral['dist'] = get_distance(neutral['pos'] - hero['pos'])
                neutral_monsters.sort(key=keyDistance)
                closest_monster = neutral_monsters[0]
                if round_count > EARLY_ROUND_THRESHOLD and mana > 10 and action is None:
                    if mode == MODE_CONTROL:
                        if get_distance(closest_monster['pos'] - hero['pos']) < 2200:
                            action = 'SPELL CONTROL ' + str(closest_monster['id'])
                            #target = enemy_base['pos']
                            target = random.choice(enemy_monster_targets)
                            controlled_monsters += 1
                            if controlled_monsters > 5:
                                mode = MODE_SHIELD
                        else:
                            action = 'MOVE'
                            target = closest_monster['pos'] - 2 * closest_monster['vel']
                    else:
                        if get_distance(enemy_base['pos'] - hero['pos']) > 5000:
                            # Go towards base
                            action = 'MOVE'
                            target = shield_place
                        else:
                            if shielded_enemy_monsters > 0:
                                # We have shielded monsters, target their heroes
                                if len(op_heroes) > 0:
                                    if get_distance(op_heroes[0]['pos'] - hero['pos']) < 2200:
                                        # Control opp hero
                                        action = 'SPELL CONTROL ' + str(op_heroes[0]['id'])
                                        target = base['pos']
                                else:
                                    # Move towards opp base
                                    action = 'MOVE'
                                    target = enemy_base['pos']
                            elif len(enemy_monsters) > 0:
                                # Look for monsters to shield
                                action = 'SPELL SHIELD ' + str(enemy_monsters[0]['id'])
                                # action = 'SPELL WIND ' + str(enemy_monsters[0]['id'])
                                # target = enemy_base['pos']
                            else:
                                # Back to control mode
                                mode = MODE_CONTROL
                                controlled_monsters = 0
                else:
                    action = 'MOVE'
                    target = closest_monster['pos'] + closest_monster['vel']
            if action is None:
                action = 'MOVE'
                target = centre
                # target = monsters[0]['pos'] + monsters[0]['vel']
                # np.array([1000 * x  for x in np.random.random(2)]) * (1 if other_base[0] == 0 else -1)

        # In the first league: MOVE <x> <y> | WAIT; In later leagues: | SPELL <spellParams>;
        if action is None:
            action = 'WAIT'
        if action[0] == 'S':
            mana -= 10
        if target is not None:
            action = ' '.join([action, str(int(target[0])), str(int(target[1]))])
        print(action, file=sys.stderr, flush=True)
        print(action)

