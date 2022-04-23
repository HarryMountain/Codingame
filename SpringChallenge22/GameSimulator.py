import math


def get_distance_squared(v):
    return round(v.dot(v))


def get_normalized_vector(v, length):
    current_length = math.sqrt(v.dot(v))
    return math.floor(v * length / current_length)


def evolve_game_step(base, other_base, monsters, heroes, hero_moves):
    for monster in monsters:
        monster['pos'] += monster['vel']
        distance_base = get_distance_squared(monster['pos'] - base['pos'])
        distance_other_base = get_distance_squared(monster['pos'] - other_base['pos'])
        if monster['nearBase'] == 0:
            if distance_base < 25000000:
                monster['nearBase'] = 1
                monster['vel'] = get_normalized_vector(base['pos'] - monster['pos'])
            elif distance_other_base < 25000000:
                monster['nearBase'] = 1
                monster['vel'] = get_normalized_vector(other_base['pos'] - monster['pos'])
        else:
            if distance_base < 90000:
                base['damage'] += 1
            elif distance_other_base < 90000:
                other_base['damage'] += 1
    for hero in heroes:
        if hero['move'] is not None:
            hero['pos'] += hero['move']
        for monster in monsters:
            if get_distance_squared(hero['pos'] - monster['pos']) < 160000:
                monster['health'] -= 2

    monsters = [m for m in monsters if m['health'] > 0]








