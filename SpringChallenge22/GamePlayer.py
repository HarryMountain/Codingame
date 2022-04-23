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
heroes_per_player = int(input())  # Always 3
heroes = {}
initialized = False


# game loop
while True:
    for i in range(2):
        # health: Each player's base health
        # mana: Ignore in the first league; Spend ten mana to cast a spell
        health, mana = [int(j) for j in input().split()]
    entity_count = int(input())  # Amount of heros and monsters you can see
    monsters = []
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
        if _type == TYPE_MONSTER and threat_for < 2:
            monsters.append({'pos': np.array((x, y)), 'vel': np.array((vx, vy)), 'health': health})
        elif _type == TYPE_MY_HERO:
            if initialized:
                heroes[_id]['pos'] = np.array((x, y))
            else:
                heroes[_id] = {'pos': np.array((x, y))}

    initialized = True

    for hero in heroes.values():
        target = None
        if len(monsters) > 0:
            monster_distances = [get_distance(hero['pos'] - m['pos'] - m['vel']) for m in monsters]
            closest_idx = monster_distances.index(min(monster_distances))
            target = monsters[closest_idx]['pos'] + monsters[closest_idx]['vel']
            if get_distance(target - base['pos']) > 5000:
                target = hero['pos'] + np.array([1000 * (x - 0.5) for x in np.random.random(2)])
        # In the first league: MOVE <x> <y> | WAIT; In later leagues: | SPELL <spellParams>;
        print('WAIT' if target is None else ' '.join(['MOVE', str(int(target[0])), str(int(target[1]))]))

