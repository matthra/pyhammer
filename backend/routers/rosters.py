"""
Roster Management API Router
Handles loading, saving, and managing army rosters
"""
from fastapi import APIRouter, HTTPException
from typing import List
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from src.data.roster_manager import (
    get_available_rosters,
    load_roster_file,
    save_roster_file,
    delete_roster,
    get_roster_metadata
)
from ..models import WeaponProfile, RosterSummary, SaveRosterRequest

router = APIRouter()

@router.get("/list", response_model=List[RosterSummary])
async def get_roster_list():
    """Get list of all available rosters"""
    try:
        roster_files = get_available_rosters()
        summaries = []

        for filename in roster_files:
            try:
                df = load_roster_file(filename)

                # Calculate summary stats
                unit_ids = df['UnitID'].unique() if 'UnitID' in df.columns else []
                total_points = df['Pts'].sum() if 'Pts' in df.columns else 0

                summaries.append(RosterSummary(
                    filename=filename,
                    name=filename.replace('.json', ''),
                    total_points=int(total_points),
                    unit_count=len(unit_ids),
                    weapon_count=len(df)
                ))
            except Exception as e:
                # Skip invalid rosters
                continue

        return summaries

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error listing rosters: {str(e)}"
        )

@router.get("/load/{filename}")
async def load_roster_by_name(filename: str):
    """Load a specific roster by filename"""
    try:
        df = load_roster_file(filename)

        # Convert DataFrame to list of WeaponProfile models
        weapons = []
        for _, row in df.iterrows():
            # Helper to safely convert to int, handling string values
            def safe_int(value, default):
                try:
                    return int(value)
                except (ValueError, TypeError):
                    return default

            # Create base weapon data
            weapon_data = {
                'UnitID': str(row.get('UnitID', '')),
                'Name': str(row.get('Name', '')),
                'Qty': safe_int(row.get('Qty'), 1),
                'Pts': safe_int(row.get('Pts'), 0),
                'Weapon': str(row.get('Weapon', '')),
                'Range': row.get('Range', 24),
                'A': row.get('A', 1),
                'BS': safe_int(row.get('BS'), 4),
                'S': safe_int(row.get('S'), 4),
                'AP': safe_int(row.get('AP'), 0),
                'D': row.get('D', 1),
                'Blast': str(row.get('Blast', 'N')),
                'Melta': safe_int(row.get('Melta'), 0),
                'RapidFire': safe_int(row.get('RapidFire'), 0),
                'TwinLinked': str(row.get('TwinLinked', 'N')),
                'Lethal': str(row.get('Lethal', 'N')),
                'Dev': str(row.get('Dev', 'N')),
                'Torrent': str(row.get('Torrent', 'N')),
                'IgnoresCover': str(row.get('IgnoresCover', 'N')),
                'CritHit': safe_int(row.get('CritHit'), 6),
                'CritWound': safe_int(row.get('CritWound'), 6),
                'Sustained': safe_int(row.get('Sustained'), 0),
                'FNP': str(row.get('FNP', '')),
                'ProfileID': str(row.get('Profile ID', ''))
            }

            # Add optional fields if they exist
            if 'Loadout Group' in row:
                weapon_data['Loadout Group'] = str(row.get('Loadout Group', ''))
            if 'Keywords' in row:
                weapon_data['Keywords'] = str(row.get('Keywords', ''))
            if 'RR_H' in row:
                weapon_data['RR_H'] = str(row.get('RR_H', 'N'))
            if 'RR_W' in row:
                weapon_data['RR_W'] = str(row.get('RR_W', 'N'))

            weapon = WeaponProfile(**weapon_data)
            weapons.append(weapon)

        # Serialize weapons with aliases to ensure "Loadout Group" is included
        weapons_serialized = [w.model_dump(by_alias=True) for w in weapons]

        return {
            "filename": filename,
            "weapons": weapons_serialized
        }

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Roster '{filename}' not found"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error loading roster: {str(e)}"
        )

@router.post("/save")
async def save_roster_endpoint(request: SaveRosterRequest):
    """Save a roster to disk"""
    try:
        # Convert WeaponProfile models to DataFrame with aliases
        weapon_dicts = [w.model_dump(by_alias=True) for w in request.weapons]
        df = pd.DataFrame(weapon_dicts)

        # Rename ProfileID column to match expected format
        if 'ProfileID' in df.columns:
            df.rename(columns={'ProfileID': 'Profile ID'}, inplace=True)

        # Save using existing roster_manager
        save_roster_file(df, request.filename)

        return {
            "status": "success",
            "filename": request.filename,
            "weapon_count": len(request.weapons)
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error saving roster: {str(e)}"
        )

@router.delete("/delete/{filename}")
async def delete_roster_endpoint(filename: str):
    """Delete a roster file"""
    try:
        delete_roster(filename)
        return {
            "status": "success",
            "message": f"Roster '{filename}' deleted"
        }

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Roster '{filename}' not found"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting roster: {str(e)}"
        )
