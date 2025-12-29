# PyHammer ⚡🔨

> *A python math hammer project for calculating probabilities in the grim darkness of the far future.*

**PyHammer** is an open-source, deterministic Mathhammer engine for Warhammer 40k. It calculates **Cost Per Kill (CPK)** efficiency, accounting for complex rules like Sustained Hits, Lethal Hits, and Damage Wastage (Overkill).

Designed for:
1.  **Players:** A local, privacy-focused Streamlit app.
2.  **AI Agents:** An MCP Server to give Claude/Cursor perfect math skills.

---

## 🚀 Usage

### Option 1: The App (For Players)
Run the calculator locally on your machine. No internet required, no data tracking.

1.  Install requirements:
    ```bash
    pip install streamlit pandas
    ```

2.  Run the app:
    ```bash
    streamlit run app.py
    ```

3.  The calculator will open in your browser automatically.

### Option 2: The AI Skill (MCP)
Give Claude (or any MCP-compliant AI) a calculator watch. Stop the hallucinations.

1.  Install the MCP SDK:
    ```bash
    pip install mcp
    ```

2.  Add this to your `claude_desktop_config.json`:
    * **Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`
    * **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

    ```json
    "pyhammer": {
      "command": "python",
      "args": ["/ABSOLUTE/PATH/TO/mcp_server.py"]
    }
    ```

3.  Restart Claude. You can now drag your list CSV into the chat and ask:
    > *"Analyze my roster efficiency against Custodes."*

---

## 📜 License: AGPLv3

This project is licensed under the **GNU Affero General Public License v3 (AGPLv3)**.

**What this means:**
* ✅ **You may:** Use this tool for free. Fork it. Modify it.
* ✅ **You may:** Use it commercially (e.g., on an ad-supported website).
* ⚠️ **BUT:** If you host this software for users to interact with over a network (like a website), you **MUST** provide the full source code to your users.

*If you profit from the machine spirit, you must share your schematics.*
