import math

NATURES = {
    "Hardy": {"plus": None, "minus": None},
    "Lonely": {"plus": "atk", "minus": "def"},
    "Brave": {"plus": "atk", "minus": "spe"},
    "Adamant": {"plus": "atk", "minus": "spa"},
    "Naughty": {"plus": "atk", "minus": "spd"},
    "Bold": {"plus": "def", "minus": "atk"},
    "Docile": {"plus": None, "minus": None},
    "Relaxed": {"plus": "def", "minus": "spe"},
    "Impish": {"plus": "def", "minus": "spa"},
    "Lax": {"plus": "def", "minus": "spd"},
    "Timid": {"plus": "spe", "minus": "atk"},
    "Hasty": {"plus": "spe", "minus": "def"},
    "Serious": {"plus": None, "minus": None},
    "Jolly": {"plus": "spe", "minus": "spa"},
    "Naive": {"plus": "spe", "minus": "spd"},
    "Modest": {"plus": "spa", "minus": "atk"},
    "Mild": {"plus": "spa", "minus": "def"},
    "Quiet": {"plus": "spa", "minus": "spe"},
    "Bashful": {"plus": None, "minus": None},
    "Rash": {"plus": "spa", "minus": "spd"},
    "Calm": {"plus": "spd", "minus": "atk"},
    "Gentle": {"plus": "spd", "minus": "def"},
    "Sassy": {"plus": "spd", "minus": "spe"},
    "Careful": {"plus": "spd", "minus": "spa"},
    "Quirky": {"plus": None, "minus": None},
}

TYPE_CHART = {
    "Normal": {"weak": ["Fighting"], "resist": [], "immune": ["Ghost"]},
    "Fire": {"weak": ["Water", "Ground", "Rock"], "resist": ["Fire", "Grass", "Ice", "Bug", "Steel", "Fairy"], "immune": []},
    "Water": {"weak": ["Grass", "Electric"], "resist": ["Fire", "Water", "Ice", "Steel"], "immune": []},
    "Electric": {"weak": ["Ground"], "resist": ["Electric", "Flying", "Steel"], "immune": []},
    "Grass": {"weak": ["Fire", "Ice", "Poison", "Flying", "Bug"], "resist": ["Water", "Electric", "Grass", "Ground"], "immune": []},
    "Ice": {"weak": ["Fire", "Fighting", "Rock", "Steel"], "resist": ["Ice"], "immune": []},
    "Fighting": {"weak": ["Flying", "Psychic", "Fairy"], "resist": ["Bug", "Rock", "Dark"], "immune": []},
    "Poison": {"weak": ["Ground", "Psychic"], "resist": ["Grass", "Fighting", "Poison", "Bug", "Fairy"], "immune": []},
    "Ground": {"weak": ["Water", "Grass", "Ice"], "resist": ["Poison", "Rock"], "immune": ["Electric"]},
    "Flying": {"weak": ["Electric", "Ice", "Rock"], "resist": ["Grass", "Fighting", "Bug"], "immune": ["Ground"]},
    "Psychic": {"weak": ["Bug", "Ghost", "Dark"], "resist": ["Fighting", "Psychic"], "immune": []},
    "Bug": {"weak": ["Fire", "Flying", "Rock"], "resist": ["Grass", "Fighting", "Ground"], "immune": []},
    "Rock": {"weak": ["Water", "Grass", "Fighting", "Ground", "Steel"], "resist": ["Normal", "Fire", "Poison", "Flying"], "immune": []},
    "Ghost": {"weak": ["Ghost", "Dark"], "resist": ["Poison", "Bug"], "immune": ["Normal", "Fighting"]},
    "Dragon": {"weak": ["Ice", "Dragon", "Fairy"], "resist": ["Fire", "Water", "Electric", "Grass"], "immune": []},
    "Dark": {"weak": ["Fighting", "Bug", "Fairy"], "resist": ["Ghost", "Dark"], "immune": ["Psychic"]},
    "Steel": {"weak": ["Fire", "Fighting", "Ground"], "resist": ["Normal", "Grass", "Ice", "Flying", "Psychic", "Bug", "Rock", "Dragon", "Steel", "Fairy"], "immune": ["Poison"]},
    "Fairy": {"weak": ["Poison", "Steel"], "resist": ["Fighting", "Bug", "Dark"], "immune": ["Dragon"]},
}

def calculate_stat(base, sp, nature_name, stat_name, level=50):
    iv = 31
    ev_bonus = (sp * 2 - 1) if sp > 0 else 0
    if stat_name == "hp":
        return math.floor((2 * base + iv + ev_bonus) * level / 100) + level + 10
    else:
        stat = math.floor((2 * base + iv + ev_bonus) * level / 100) + 5
        nature = NATURES.get(nature_name, {"plus": None, "minus": None})
        if nature["plus"] == stat_name:
            stat = math.floor(stat * 1.1)
        elif nature["minus"] == stat_name:
            stat = math.floor(stat * 0.9)
        return stat

def get_type_effectiveness(attack_type, defend_types):
    effectiveness = 1.0
    for dtype in defend_types:
        dtype = dtype.title()
        if dtype not in TYPE_CHART:
            continue
        if attack_type.title() in TYPE_CHART[dtype]["weak"]:
            effectiveness *= 2.0
        elif attack_type.title() in TYPE_CHART[dtype]["resist"]:
            effectiveness *= 0.5
        elif attack_type.title() in TYPE_CHART[dtype]["immune"]:
            effectiveness *= 0.0
    return effectiveness

def calculate_speed(speed_stat, stages, tailwind, trick_room):
    # Stages multiplier
    if stages > 0:
        multiplier = (2 + stages) / 2
    elif stages < 0:
        multiplier = 2 / (2 - stages)
    else:
        multiplier = 1.0
        
    speed = math.floor(speed_stat * multiplier)
    if tailwind:
        speed *= 2
        
    return speed # Note: Trick room inverses the turn order, it doesn't change the stat, but we can flag it in the UI.

def calculate_damage(level, power, a_stat, d_stat, modifiers):
    # simplified damage formula
    damage = math.floor(math.floor(math.floor(2 * level / 5 + 2) * power * a_stat / d_stat) / 50) + 2
    
    for mod in modifiers:
        damage = math.floor(damage * mod)
        
    return damage
