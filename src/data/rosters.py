# src/data/rosters.py
import uuid

# We assign static IDs here so the defaults are grouped correctly on startup.
DEFAULT_ROSTER = [
    {
        'UnitID': 'd1b2c3a4-1111-1111-1111-111111111111',
        'Qty': 1,
        'Name': 'War Dog Brigand', 'Loadout Group': 'Ranged', 'Pts': 170, 'Range': 24,
        'Profile ID': '', 'Keywords': '',
        'Weapon': 'Demonbreath Spear',
        'A': 2, 'BS': 2, 'S': 12, 'AP': -4, 'D': 'D6+4',
        'CritHit': 6, 'CritWound': 6, 'Sustained':0, 'Lethal':'N', 'Dev':'N',
        'Torrent':'N', 'TwinLinked':'N', 'Blast':'N', 'Melta':'N', 'RapidFire':'N', 'RR_H':'N', 'RR_W':'N'
    },
    {
        'UnitID': 'd1b2c3a4-1111-1111-1111-111111111111', # Same ID = Same Unit
        'Qty': 1,
        'Name': 'War Dog Brigand', 'Loadout Group': 'Ranged', 'Pts': 170, 'Range': 36,
        'Profile ID': '', 'Keywords': '',
        'Weapon': 'Avenger Chaincannon',
        'A': 12, 'BS': 2, 'S': 6, 'AP': -1, 'D': '1',
        'CritHit': 6, 'CritWound': 6, 'Sustained':0, 'Lethal':'N', 'Dev':'N',
        'Torrent':'N', 'TwinLinked':'N', 'Blast':'N', 'Melta':'N', 'RapidFire':'N', 'RR_H':'N', 'RR_W':'N'
    },
    {
        'UnitID': 'k9x8y7z6-2222-2222-2222-222222222222', # Different ID = Different Unit
        'Qty': 1,
        'Name': 'War Dog Karnivore', 'Loadout Group': 'Melee', 'Pts': 140, 'Range': 'M',
        'Profile ID': 'Claw', 'Keywords': '',
        'Weapon': 'Reaper Chaintalon (Strike)',
        'A': 6, 'BS': 2, 'S': 12, 'AP': -3, 'D': 'D6+2',
        'CritHit': 6, 'CritWound': 6, 'Sustained':1, 'Lethal':'N', 'Dev':'N',
        'Torrent':'N', 'TwinLinked':'N', 'RR_H':'N', 'RR_W':'N'
    },
    {
        'UnitID': 'k9x8y7z6-2222-2222-2222-222222222222',
        'Qty': 1,
        'Name': 'War Dog Karnivore', 'Loadout Group': 'Melee', 'Pts': 140, 'Range': 'M',
        'Profile ID': 'Claw', 'Keywords': '',
        'Weapon': 'Reaper Chaintalon (Sweep)',
        'A': 12, 'BS': 2, 'S': 8, 'AP': -2, 'D': 1,
        'CritHit': 6, 'CritWound': 6, 'Sustained':1, 'Lethal':'N', 'Dev':'N',
        'Torrent':'N', 'TwinLinked':'N', 'RR_H':'N', 'RR_W':'N'
    }
]