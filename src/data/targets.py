# src/data/targets.py

# The Encyclopedia of Defensive Profiles
# UnitSize: The cap for maximum models killed per activation
# FNP: Feel No Pain value (e.g., '5+', '6+') or None

TARGETS = {
    'GEQ': {
        'Name': 'Guardsmen (T3 1W)',
        'Pts': 6, 'T': 3, 'W': 1, 'Sv': '5+', 'Inv': '', 'FNP': '', 'UnitSize': 20
    },
    'MEQ': {
        'Name': 'Marines (T4 2W)',
        'Pts': 18, 'T': 4, 'W': 2, 'Sv': '3+', 'Inv': '', 'FNP': '', 'UnitSize': 10
    },
    'TEQ': {
        'Name': 'Terminators (T5 3W)',
        'Pts': 38, 'T': 5, 'W': 3, 'Sv': '2+', 'Inv': '4+', 'FNP': '', 'UnitSize': 5
    },
    'CUST': {
        'Name': 'Custodes (T6 3W)',
        'Pts': 50, 'T': 6, 'W': 3, 'Sv': '2+', 'Inv': '4+', 'FNP': '4+', 'UnitSize': 5
    },
    'GRAV': {
        'Name': 'Gravis (T6 3W)',
        'Pts': 37, 'T': 6, 'W': 3, 'Sv': '3+', 'Inv': '', 'FNP': '', 'UnitSize': 6
    },
    'DG-PM': {
        'Name': 'Plague Marine (T5 2W)',
        'Pts': 18, 'T': 5, 'W': 2, 'Sv': '3+', 'Inv': '', 'FNP': '6+', 'UnitSize': 10
    },
    'CTAN': {
        'Name': 'C\'tan Shard (T11 12W)',
        'Pts': 255, 'T': 11, 'W': 12, 'Sv': '4+', 'Inv': '4+', 'FNP': '5+', 'UnitSize': 1
    },
    'VEQ-L': {
        'Name': 'Rhino (T9 10W)',
        'Pts': 75, 'T': 9, 'W': 10, 'Sv': '3+', 'Inv': '', 'FNP': '', 'UnitSize': 1
    },
    'VEQ-H': {
        'Name': 'Land Raider (T12 16W)',
        'Pts': 240, 'T': 12, 'W': 16, 'Sv': '2+', 'Inv': '', 'FNP': '', 'UnitSize': 1
    },
    'KEQ': {
        'Name': 'Knight (T12 22W)',
        'Pts': 425, 'T': 12, 'W': 22, 'Sv': '3+', 'Inv': '5+', 'FNP': '6+', 'UnitSize': 1
    },
}