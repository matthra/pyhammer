⚡ PyHammer
The Advanced Mathhammer Analysis Suite

PyHammer is a local web application designed to be the "post-game analysis" for your Warhammer 40k list building. It doesn't tell you what to take—it tells you how well it works.

By auditing your roster against standard defensive profiles (MEQ, TEQ, Vehicles, Knights), PyHammer exposes your list's efficiency gaps, threat ranges, and single points of failure before you ever put models on the table.

🚀 Key Features
Roster Manager: Import/Export CSV lists. Manage unit profiles with an abstraction layer focused on output, not just points.

Deep Efficiency Metrics:

CPK (Cost Per Kill): Are you paying too much to kill a Guard squad?

TTK (Time To Kill): How many activations does it actually take to drop a Knight?

Interactive Visualizations (Plotly):

Threat Matrix: Bubble chart comparing Range vs. Strength vs. Volume of Fire.

Efficiency Curves: "Guitar String" charts showing how unit performance degrades as targets get tougher.

Army Output: Stacked analysis of your total damage potential per phase.

Theming Engine: Switch between "Midnight", "Grimdark (CRT)", and "Scientific" modes via themes.json.

AI Ready: Includes an MCP Server (mcp_server.py) to let AI agents (like Claude or ChatGPT) run calculations on your roster.

🛠️ Installation
PyHammer is a Python application built on Streamlit.

Prerequisites
Python 3.10 or higher.

Quick Start
Clone the repository:

Bash

git clone https://github.com/yourusername/pyhammer.git
cd pyhammer
Install dependencies:

Bash

pip install -r requirements.txt
Run the App:

Bash

streamlit run app.py
This will automatically open the dashboard in your default web browser (usually http://localhost:8501).

📊 How to Use
Roster Manager Tab:

Add units manually or import a CSV.

Tip: Use the "Loadout Group" column to split units with mixed weapons (e.g., "Crisis Team [Plasma]" vs "Crisis Team [Missiles]").

For Melee weapons, enter M or 0 in the Range column.

Analysis Tabs:

Efficiency (CPK): Look for Green cells (< 2.0). These are your efficient traders.

Time To Kill: Look for values > 1.0. If a unit takes 1.2 activations to kill a tank, you effectively need two units to ensure the kill.

Interactive Charts:

Hover over any data point to see specific unit details.

Use the Theme Selector to switch visual styles.

🎨 Customization
Creating Custom Themes
You can add your own faction colors (e.g., Ultramarine Blue, Necron Green) by editing src/visualizations/themes.json.

JSON

"My Custom Faction": {
  "template": "plotly_dark",
  "background_color": "#0E1117",
  "colors": ["#YOUR_HEX_CODE_1", "#YOUR_HEX_CODE_2", "..."]
}
The app will automatically detect new themes upon restart.

Modifying Targets
Want to test against a specific enemy unit? Edit src/data/targets.py. You can add custom profiles (e.g., "Mortarion", "Avatar") to the TARGETS dictionary.

🤖 AI Integration (MCP)
PyHammer includes a Model Context Protocol (MCP) server, allowing AI assistants to "talk" to your math engine.

To run the MCP Server:

Bash

python mcp_server.py
This allows compatible AI clients to query your roster's efficiency and receive direct links to specific charts in the dashboard.

📖 Documentation

Comprehensive feature documentation available in the `docs/` folder:

- **[Target Manager](docs/TARGET_MANAGER.md)** - 🆕 Custom target lists for different metas (v0.3.10)
- **[UX Refactor v0.3.9](docs/UX_REFACTOR_V0.3.9.md)** - Latest UI improvements and global settings
- **[Grading System](docs/GRADING_SYSTEM.md)** - CPK efficiency letter grades (S to F tier)
- **[Blast Keyword](docs/BLAST_KEYWORD.md)** - Area-of-effect weapons implementation
- **[Cover Toggle](docs/COVER_TOGGLE.md)** - Global cover mechanics (+1 save)
- **[Keywords Implementation](docs/NEW_KEYWORDS_IMPLEMENTATION.md)** - Torrent, Twin-Linked, FNP

See **[docs/README.md](docs/README.md)** for full documentation index.

🧪 Testing

PyHammer has comprehensive test coverage with 26 tests across 6 test suites.

**Run All Tests:**
```bash
python tests/run_all_tests.py
```

**Run Individual Tests:**
```bash
python tests/test_blast.py
python tests/test_cover.py
python tests/test_range_weapons.py
```

**Test Coverage:**
- ✅ Blast keyword (8 tests)
- ✅ Cover toggle (3 tests)
- ✅ Melta/Rapid Fire (5 tests)
- ✅ Multi-mode corner cases (3 tests)
- ✅ Half range toggle (3 tests)
- ✅ Keyword integration (4 tests)

See **[tests/README.md](tests/README.md)** for detailed test documentation.

📂 Project Structure
Plaintext

pyhammer/
├── app.py                   # Main UI Controller (Streamlit)
├── mcp_server.py            # AI Integration Server
├── requirements.txt         # Dependencies
├── roster.csv               # Default/Saved Roster
├── docs/                    # Documentation (9 feature docs)
│   ├── README.md            # Documentation index
│   ├── UX_REFACTOR_V0.3.9.md
│   ├── GRADING_SYSTEM.md
│   └── *.md                 # Feature documentation
├── tests/                   # Test Suite (26 tests, 100% passing)
│   ├── run_all_tests.py     # Test runner
│   └── test_*.py            # Individual test files
└── src/                     # Source Code
    ├── data/                # Target Profiles (MEQ, TEQ, etc.)
    ├── engine/              # Core Mathhammer Logic (Probabilities)
    └── visualizations/      # Plotly Charts & Theme Logic
        ├── charts.py        # Chart definitions
        ├── theme_utils.py   # JSON loaders
        └── themes.json      # Color configurations

⚠️ Disclaimer
PyHammer is an unofficial fan tool. All Warhammer 40,000 terminology is © Games Workshop Limited. This tool is for statistical analysis only and is not a substitute for the official rules or codexes.