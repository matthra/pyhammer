"""
Target List Management Utilities

Handles loading, saving, and managing custom target lists.
Target lists are stored as JSON files in target_configs/ directory.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

# Get the directory where THIS file (target_manager.py) is located (src/data)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Navigate up TWO levels to get to project root (src/data -> src -> root)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, '..', '..'))

# Define the absolute path to the config folder
TARGET_CONFIG_DIR = os.path.join(PROJECT_ROOT, 'target_configs')

def ensure_target_configs_dir():
    """Ensure target_configs directory exists"""
    if not os.path.exists(TARGET_CONFIG_DIR):
        os.makedirs(TARGET_CONFIG_DIR)

def get_available_target_lists() -> List[str]:
    """
    Get list of available target list filenames.

    Returns:
        List of filenames (without .json extension)
    """
    ensure_target_configs_dir()

    files = []
    for filename in os.listdir(TARGET_CONFIG_DIR):
        if filename.endswith('.json'):
            files.append(filename[:-5])  # Remove .json extension

    # Sort with 'default' first
    files.sort(key=lambda x: (x != 'default', x.lower()))
    return files

def load_target_list(list_name: str) -> Dict:
    """
    Load a target list from JSON file.

    Args:
        list_name: Name of the target list (without .json)

    Returns:
        Dictionary with list metadata and targets
    """
    ensure_target_configs_dir()

    filepath = os.path.join(TARGET_CONFIG_DIR, f"{list_name}.json")

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Target list '{list_name}' not found")

    with open(filepath, 'r') as f:
        data = json.load(f)

    return data

def save_target_list(list_name: str, targets: Dict, description: str = "", overwrite: bool = False) -> str:
    """
    Save a target list to JSON file.

    Args:
        list_name: Name for the target list
        targets: Dictionary of target profiles
        description: Optional description of the target list
        overwrite: If True, overwrite existing file

    Returns:
        Filename that was saved
    """
    ensure_target_configs_dir()

    # Sanitize filename (replace spaces with underscores, lowercase)
    filename = list_name.lower().replace(' ', '_').replace('/', '_').replace('\\', '_')
    filepath = os.path.join(TARGET_CONFIG_DIR, f"{filename}.json")

    # Check if file exists and overwrite is False
    if os.path.exists(filepath) and not overwrite:
        raise FileExistsError(f"Target list '{filename}' already exists. Use overwrite=True to replace.")

    # Create the data structure
    data = {
        'name': list_name,
        'description': description,
        'version': '1.0',
        'created': datetime.now().isoformat(),
        'readonly': False,
        'targets': targets
    }

    # Save to file
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

    return filename

def delete_target_list(list_name: str) -> bool:
    """
    Delete a target list file.

    Args:
        list_name: Name of the target list to delete

    Returns:
        True if deleted, False if file not found or is readonly
    """
    ensure_target_configs_dir()

    # Don't allow deleting default
    if list_name == 'default':
        return False

    filepath = os.path.join(TARGET_CONFIG_DIR, f"{list_name}.json")

    if not os.path.exists(filepath):
        return False

    # Check if readonly
    try:
        data = load_target_list(list_name)
        if data.get('readonly', False):
            return False
    except:
        pass

    # Delete the file
    os.remove(filepath)
    return True

def get_target_list_metadata(list_name: str) -> Dict:
    """
    Get metadata about a target list without loading all targets.

    Args:
        list_name: Name of the target list

    Returns:
        Dictionary with name, description, version, etc.
    """
    data = load_target_list(list_name)

    metadata = {
        'name': data.get('name', list_name),
        'description': data.get('description', ''),
        'version': data.get('version', '1.0'),
        'created': data.get('created', ''),
        'readonly': data.get('readonly', False),
        'profile_count': len(data.get('targets', {}))
    }

    return metadata

def validate_target_profile(profile: Dict) -> tuple[bool, str]:
    """
    Validate that a target profile has all required fields.

    Args:
        profile: Target profile dictionary

    Returns:
        (is_valid, error_message)
    """
    required_fields = ['T', 'Sv', 'W', 'UnitSize', 'Pts']

    for field in required_fields:
        if field not in profile:
            return False, f"Missing required field: {field}"

        # Check that numeric fields are valid
        if field in ['T', 'W', 'UnitSize', 'Pts']:
            try:
                val = int(profile[field])
                if val <= 0:
                    return False, f"{field} must be positive"
            except (ValueError, TypeError):
                return False, f"{field} must be a number"

    # Validate save value format
    sv = str(profile['Sv'])
    if sv not in ['2+', '3+', '4+', '5+', '6+', '7+', 'N']:
        return False, f"Invalid save value: {sv}"

    return True, ""

def import_targets_from_csv(csv_content: str) -> Dict:
    """
    Import target profiles from CSV content.

    Expected CSV format:
    Name,T,Sv,W,UnitSize,Pts,Invuln,FNP
    MEQ,4,3+,2,10,20,N,N

    Args:
        csv_content: CSV file content as string

    Returns:
        Dictionary of target profiles
    """
    import csv
    from io import StringIO

    targets = {}
    reader = csv.DictReader(StringIO(csv_content))

    for row in reader:
        name = row.get('Name', '').strip()
        if not name:
            continue

        profile = {
            'T': int(row.get('T', 4)),
            'Sv': row.get('Sv', '3+'),
            'W': int(row.get('W', 2)),
            'UnitSize': int(row.get('UnitSize', 10)),
            'Pts': int(row.get('Pts', 20)),
            'Invuln': row.get('Invuln', 'N'),
            'FNP': row.get('FNP', 'N')
        }

        # Validate profile
        is_valid, error = validate_target_profile(profile)
        if not is_valid:
            print(f"Warning: Skipping invalid profile '{name}': {error}")
            continue

        targets[name] = profile

    return targets

def export_targets_to_csv(targets: Dict) -> str:
    """
    Export target profiles to CSV format.

    Args:
        targets: Dictionary of target profiles

    Returns:
        CSV content as string
    """
    import csv
    from io import StringIO

    output = StringIO()
    fieldnames = ['Name', 'T', 'Sv', 'W', 'UnitSize', 'Pts', 'Invuln', 'FNP']
    writer = csv.DictWriter(output, fieldnames=fieldnames)

    writer.writeheader()

    for name, profile in targets.items():
        row = {
            'Name': name,
            'T': profile.get('T', 4),
            'Sv': profile.get('Sv', '3+'),
            'W': profile.get('W', 2),
            'UnitSize': profile.get('UnitSize', 10),
            'Pts': profile.get('Pts', 20),
            'Invuln': profile.get('Invuln', 'N'),
            'FNP': profile.get('FNP', 'N')
        }
        writer.writerow(row)

    return output.getvalue()
