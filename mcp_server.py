from mcp.server.fastmcp import FastMCP
import os
import sys

# 1. Force Python to look in the current directory for modules
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.data.targets import TARGETS
from src.engine.calculator import resolve_weapon_profile
from src.engine.grading import get_cpk_grade, get_grade_description

# Define where your Streamlit app lives (Default is localhost:8501)
APP_URL = "http://localhost:8501"

mcp = FastMCP("PyHammer")

@mcp.tool()
def calculate_efficiency(
    pts: int, attacks: int, bs: str, strength: int, ap: int, damage: str, 
    range_val: str = "M", 
    target_type: str = "MEQ", 
    sustained: int = 0, lethal: bool = False, dev: bool = False, rr_h: str = "N", rr_w: str = "N"
) -> str:
    """
    Calculates CPK efficiency for a single unit profile against a standard target.
    """
    
    # 1. Get Target
    defender = TARGETS.get(target_type.upper())
    if not defender: 
        return f"Target not found. Options: {list(TARGETS.keys())}"

    # 2. Build Attacker Dict
    attacker = {
        'Pts': pts, 'A': attacks, 'BS': bs, 'S': strength, 'AP': ap, 'D': damage,
        'Sustained': sustained, 'Lethal': 'Y' if lethal else 'N', 'Dev': 'Y' if dev else 'N',
        'RR_H': rr_h, 'RR_W': rr_w
    }
    
    # 3. Calculate
    try:
        res = resolve_weapon_profile(attacker, defender)
        dead = res['dead_models']
        
        # Unit Cap Logic
        cap = defender.get('UnitSize', 99)
        dead = min(dead, cap)
        
        if dead <= 0:
            return "Ineffective (0 kills)."
            
        cpk = pts / (dead * defender['Pts'])
        ttk = 1.0 / dead

        # Get letter grade
        grade = get_cpk_grade(cpk)
        grade_desc = get_grade_description(grade)

        # 4. Return Formatted String with Link
        return (
            f"**VS {defender['Name']}**\n"
            f"- Dead Models: {dead:.2f}\n"
            f"- CPK: {cpk:.2f} ({grade}-tier)\n"
            f"- Efficiency: {grade_desc}\n"
            f"- Est. Activations to Kill: {ttk:.2f}\n\n"
            f"📊 [View Charts & Full Analysis]({APP_URL})"
        )
                
    except Exception as e:
        return f"Calculation Error: {e}"

@mcp.resource("pyhammer://roster")
def read_roster() -> str:
    """Reads the 'roster.csv' file if it exists."""
    if os.path.exists("roster.csv"):
        with open("roster.csv", "r") as f:
            return f.read()
    return "No roster.csv found in root directory."

if __name__ == "__main__":
    mcp.run()