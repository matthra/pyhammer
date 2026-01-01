"""
Roster Management Utilities

Handles loading, saving, and managing custom rosters.
Rosters are stored as JSON files in roster_configs/ directory.
"""

import json
import os
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Get the directory where THIS file (roster_manager.py) is located (src/data)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Navigate up TWO levels to get to project root (src/data -> src -> root)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, '..', '..'))

# Define the absolute path to the config folder
ROSTER_CONFIG_DIR = os.path.join(PROJECT_ROOT, 'roster_configs')

# Required columns for roster validation
REQUIRED_COLUMNS = [
    'UnitID', 'Qty', 'Name', 'Pts', 'Weapon', 'Loadout Group',
    'Range', 'A', 'BS', 'S', 'AP', 'D',
    'CritHit', 'CritWound', 'Sustained', 'Lethal', 'Dev',
    'Torrent', 'TwinLinked', 'Blast', 'Melta', 'RapidFire',
    'Profile ID', 'Keywords', 'RR_H', 'RR_W'
]

# Columns that should remain as strings
STRING_COLUMNS = ['Name', 'Weapon', 'Loadout Group', 'Keywords', 'Profile ID', 'UnitID']

# Columns that can be strings or numbers (like 'D6', 'M', etc.)
MIXED_TYPE_COLUMNS = ['A', 'D', 'Range']


def ensure_roster_configs_dir():
    """Ensure roster_configs directory exists"""
    if not os.path.exists(ROSTER_CONFIG_DIR):
        os.makedirs(ROSTER_CONFIG_DIR)


def get_available_rosters() -> List[str]:
    """
    Get list of available roster filenames.

    Returns:
        List of filenames (without .json extension)
    """
    ensure_roster_configs_dir()

    files = []
    for filename in os.listdir(ROSTER_CONFIG_DIR):
        if filename.endswith('.json'):
            files.append(filename[:-5])  # Remove .json extension

    # Sort with 'default_roster' first
    files.sort(key=lambda x: (x != 'default_roster', x.lower()))
    return files


def validate_roster_data(roster_df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate that a roster DataFrame has all required columns and valid data.

    Args:
        roster_df: Roster DataFrame to validate

    Returns:
        (is_valid, error_message)
    """
    # Check if DataFrame is empty
    if roster_df.empty:
        return False, "Roster is empty"

    # Check for required columns
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in roster_df.columns]
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"

    # Check that UnitID exists and is not all null
    if roster_df['UnitID'].isna().all():
        return False, "UnitID column cannot be empty"

    # Check that Name exists and is not all null
    if roster_df['Name'].isna().all():
        return False, "Name column cannot be empty"

    # Validate numeric columns where applicable
    numeric_columns = ['Qty', 'Pts', 'BS', 'S', 'AP', 'CritHit', 'CritWound', 'Sustained']
    for col in numeric_columns:
        if col in roster_df.columns:
            # Check that non-null values can be coerced to numeric
            non_null_vals = roster_df[col].dropna()
            if len(non_null_vals) > 0:
                try:
                    pd.to_numeric(non_null_vals, errors='raise')
                except (ValueError, TypeError):
                    return False, f"Column '{col}' contains non-numeric values"

    return True, ""


def load_roster_file(roster_name: str) -> pd.DataFrame:
    """
    Load a roster from JSON file.

    Args:
        roster_name: Name of the roster (without .json)

    Returns:
        DataFrame containing roster data
    """
    ensure_roster_configs_dir()

    filepath = os.path.join(ROSTER_CONFIG_DIR, f"{roster_name}.json")

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Roster '{roster_name}' not found")

    with open(filepath, 'r') as f:
        data = json.load(f)

    # Extract roster list from JSON
    roster_list = data.get('roster', [])

    if not roster_list:
        raise ValueError(f"Roster '{roster_name}' contains no data")

    # Convert to DataFrame
    roster_df = pd.DataFrame(roster_list)

    # Ensure string columns stay as strings
    for col in STRING_COLUMNS:
        if col in roster_df.columns:
            roster_df[col] = roster_df[col].astype(str)

    # Validate the loaded roster
    is_valid, error_msg = validate_roster_data(roster_df)
    if not is_valid:
        raise ValueError(f"Invalid roster data in '{roster_name}': {error_msg}")

    return roster_df


def save_roster_file(roster_df: pd.DataFrame, roster_name: str, description: str = "", overwrite: bool = True) -> str:
    """
    Save a roster to JSON file.

    Args:
        roster_df: DataFrame containing roster data
        roster_name: Name for the roster
        description: Optional description of the roster
        overwrite: If True, overwrite existing file

    Returns:
        Filename that was saved
    """
    ensure_roster_configs_dir()

    # Validate roster data before saving
    is_valid, error_msg = validate_roster_data(roster_df)
    if not is_valid:
        raise ValueError(f"Cannot save invalid roster: {error_msg}")

    # Sanitize filename (replace spaces with underscores, lowercase)
    filename = roster_name.lower().replace(' ', '_').replace('/', '_').replace('\\', '_')
    filepath = os.path.join(ROSTER_CONFIG_DIR, f"{filename}.json")

    # Check if file exists and overwrite is False
    if os.path.exists(filepath) and not overwrite:
        raise FileExistsError(f"Roster '{filename}' already exists. Use overwrite=True to replace.")

    # Convert DataFrame to list of dicts
    # Replace NaN with None for proper JSON serialization
    roster_list = roster_df.where(pd.notna(roster_df), None).to_dict('records')

    # Create the data structure
    data = {
        'name': roster_name,
        'description': description,
        'version': '1.0',
        'created': datetime.now().isoformat(),
        'readonly': False,
        'roster': roster_list
    }

    # Save to file
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

    return filename


def delete_roster(roster_name: str) -> bool:
    """
    Delete a roster file.

    Args:
        roster_name: Name of the roster to delete

    Returns:
        True if deleted, False if file not found or is readonly/default
    """
    ensure_roster_configs_dir()

    # Don't allow deleting default_roster
    if roster_name == 'default_roster':
        return False

    filepath = os.path.join(ROSTER_CONFIG_DIR, f"{roster_name}.json")

    if not os.path.exists(filepath):
        return False

    # Check if readonly
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            if data.get('readonly', False):
                return False
    except:
        pass

    # Delete the file
    os.remove(filepath)
    return True


def get_roster_metadata(roster_name: str) -> Dict:
    """
    Get metadata about a roster without loading all data.

    Args:
        roster_name: Name of the roster

    Returns:
        Dictionary with name, description, version, etc.
    """
    ensure_roster_configs_dir()

    filepath = os.path.join(ROSTER_CONFIG_DIR, f"{roster_name}.json")

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Roster '{roster_name}' not found")

    with open(filepath, 'r') as f:
        data = json.load(f)

    metadata = {
        'name': data.get('name', roster_name),
        'description': data.get('description', ''),
        'version': data.get('version', '1.0'),
        'created': data.get('created', ''),
        'readonly': data.get('readonly', False),
        'unit_count': len(data.get('roster', []))
    }

    return metadata


def create_empty_roster() -> pd.DataFrame:
    """
    Create an empty roster DataFrame with all required columns.

    Returns:
        Empty DataFrame with proper column structure
    """
    import uuid

    # Create a single template row
    template_row = {
        'UnitID': str(uuid.uuid4()),
        'Qty': 1,
        'Name': 'New Unit',
        'Pts': 100,
        'Weapon': 'New Weapon',
        'Loadout Group': 'Ranged',
        'Range': 24,
        'Profile ID': '',
        'Keywords': '',
        'A': 1,
        'BS': 3,
        'S': 4,
        'AP': 0,
        'D': 1,
        'CritHit': 6,
        'CritWound': 6,
        'Sustained': 0,
        'Lethal': 'N',
        'Dev': 'N',
        'Torrent': 'N',
        'TwinLinked': 'N',
        'Blast': 'N',
        'Melta': 'N',
        'RapidFire': 'N',
        'RR_H': 'N',
        'RR_W': 'N'
    }

    roster_df = pd.DataFrame([template_row])

    # Ensure string columns are strings
    for col in STRING_COLUMNS:
        if col in roster_df.columns:
            roster_df[col] = roster_df[col].astype(str)

    return roster_df
