from mcp.server.fastmcp import FastMCP
import cpk_engine
import csv
import os

mcp = FastMCP("PyHammer")

TARGETS = {
    'MEQ': {'Name': 'MEQ (Marine)',   'Pts': 18, 'T': 4, 'W': 2, 'Sv': '3+', 'Inv': ''},
    'TEQ': {'Name': 'TEQ (Termi)',    'Pts': 40, 'T': 5, 'W': 3, 'Sv': '2+', 'Inv': '4+'},
    'VEQ-H': {'Name': 'VEQ-H (L-Raider)','Pts': 240,'T': 12, 'W': 16, 'Sv': '2+', 'Inv': ''},
    'KEQ': {'Name': 'KEQ (Knight)',   'Pts': 400, 'T': 11, 'W': 22, 'Sv': '3+', 'Inv': '5+'},
}

@mcp.tool()
def calculate_efficiency(
    pts: int, attacks: int, bs: str, strength: int, ap: int, damage: str, 
    target_type: str = "MEQ", 
    sustained: int = 0, lethal: bool = False, dev: bool = False, rr_h: str = "N", rr_w: str = "N"
) -> str:
    """
    Calculates CPK efficiency for a unit profile against a standard target.
    LOWER IS BETTER ( < 1.5 is excellent).
    """
    
    defender = TARGETS.get(target_type.upper())
    if not defender: return f"Target not found. Options: {list(TARGETS.keys())}"

    attacker = {
        'Pts': pts, 'A': attacks, 'BS': bs, 'S': strength, 'AP': ap, 'D': damage,
        'Sustained': sustained, 'Lethal': lethal, 'Dev': dev,
        'RR_H': rr_h, 'RR_W': rr_w
    }
    
    result = cpk_engine.calculate_cpk(attacker, defender)
    return f"CPK: {result} (vs {defender['Name']})"

@mcp.resource("pyhammer://roster")
def read_roster() -> str:
    """Reads the 'my_roster.csv' file from the current directory."""
    if os.path.exists("my_roster.csv"):
        with open("my_roster.csv", "r") as f:
            return f.read()
    return "No roster file found."

if __name__ == "__main__":
    mcp.run()
