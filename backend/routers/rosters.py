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

from src.data.roster_manager import load_roster_file, save_roster_file, get_roster_metadata, delete_roster
from ..models import WeaponProfile, RosterSummary, SaveRosterRequest

router = APIRouter()

@router.get("/list", response_model=List[RosterSummary])
async def get_roster_list():
    """Get list of all available rosters"""
    try:
        roster_files = get_roster_metadata()
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
            weapon = WeaponProfile(
                UnitID=str(row.get('UnitID', '')),
                Name=str(row.get('Name', '')),
                Qty=int(row.get('Qty', 1)),
                Pts=int(row.get('Pts', 0)),
                Weapon=str(row.get('Weapon', '')),
                Range=row.get('Range', 24),
                A=row.get('A', 1),
                BS=int(row.get('BS', 4)),
                S=int(row.get('S', 4)),
                AP=int(row.get('AP', 0)),
                D=row.get('D', 1),
                Blast=str(row.get('Blast', 'N')),
                Melta=int(row.get('Melta', 0)),
                RapidFire=int(row.get('RapidFire', 0)),
                TwinLinked=str(row.get('TwinLinked', 'N')),
                Lethal=str(row.get('Lethal', 'N')),
                Dev=str(row.get('Dev', 'N')),
                Torrent=str(row.get('Torrent', 'N')),
                CritHit=int(row.get('CritHit', 6)),
                CritWound=int(row.get('CritWound', 6)),
                Sustained=int(row.get('Sustained', 0)),
                FNP=str(row.get('FNP', '')),
                ProfileID=str(row.get('Profile ID', ''))
            )
            weapons.append(weapon)

        return {
            "filename": filename,
            "weapons": weapons
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
        # Convert WeaponProfile models to DataFrame
        weapon_dicts = [w.model_dump() for w in request.weapons]
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
