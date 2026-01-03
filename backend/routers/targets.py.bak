"""
Target Management API Router
Handles loading, saving, and managing defensive target profiles
"""
from fastapi import APIRouter, HTTPException
from typing import List
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from src.data.target_manager import load_target_list, save_target_list, get_available_target_lists, delete_target_list
from ..models import TargetProfile, TargetListSummary, SaveTargetListRequest

router = APIRouter()

@router.get("/list", response_model=List[TargetListSummary])
async def get_target_lists():
    """Get list of all available target lists"""
    try:
        target_files = get_available_target_lists()
        summaries = []

        for filename in target_files:
            try:
                targets = load_target_list(filename)

                summaries.append(TargetListSummary(
                    filename=filename,
                    name=filename.replace('.json', ''),
                    target_count=len(targets),
                    targets=[t['Name'] for t in targets]
                ))
            except Exception:
                continue

        return summaries

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error listing target lists: {str(e)}"
        )

@router.get("/load/{filename}")
async def load_target_list_by_name(filename: str):
    """Load a specific target list by filename"""
    try:
        targets_data = load_target_list(filename)

        # Convert to TargetProfile models
        targets = []
        for target_dict in targets_data:
            target = TargetProfile(
                Name=target_dict.get('Name', ''),
                Pts=int(target_dict.get('Pts', 0)),
                T=int(target_dict.get('T', 4)),
                W=int(target_dict.get('W', 1)),
                Sv=str(target_dict.get('Sv', '4+')),
                Inv=str(target_dict.get('Inv', '')),
                FNP=str(target_dict.get('FNP', '')),
                Stealth=str(target_dict.get('Stealth', 'N')),
                UnitSize=int(target_dict.get('UnitSize', 1))
            )
            targets.append(target)

        return {
            "filename": filename,
            "targets": targets
        }

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Target list '{filename}' not found"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error loading target list: {str(e)}"
        )

@router.post("/save")
async def save_target_list_endpoint(request: SaveTargetListRequest):
    """Save a target list to disk"""
    try:
        # Convert TargetProfile models to list of dicts
        target_dicts = [t.model_dump() for t in request.targets]

        # Save using existing target_manager
        save_target_list(target_dicts, request.filename)

        return {
            "status": "success",
            "filename": request.filename,
            "target_count": len(request.targets)
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error saving target list: {str(e)}"
        )

@router.delete("/delete/{filename}")
async def delete_target_list_endpoint(filename: str):
    """Delete a target list file"""
    try:
        delete_target_list(filename)
        return {
            "status": "success",
            "message": f"Target list '{filename}' deleted"
        }

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Target list '{filename}' not found"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting target list: {str(e)}"
        )
