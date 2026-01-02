"""
Calculator API Router
Wraps the existing PyHammer calculation engine
"""
from fastapi import APIRouter, HTTPException
from typing import List
import pandas as pd
import sys
from pathlib import Path

# Add src to path to import existing calculator
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from engine.calculator import calculate_group_metrics
from engine.grading import get_cpk_grade
from ..models import (
    CalculateRequest,
    CalculateResponse,
    MetricResult,
    WeaponProfile,
    TargetProfile
)

router = APIRouter()

def weapon_to_dict(weapon: WeaponProfile) -> dict:
    """Convert Pydantic WeaponProfile to dict for calculator"""
    return weapon.model_dump()

def target_to_dict(target: TargetProfile) -> dict:
    """Convert Pydantic TargetProfile to dict for calculator"""
    return target.model_dump()

@router.post("/calculate", response_model=CalculateResponse)
async def calculate_metrics(request: CalculateRequest):
    """
    Calculate efficiency metrics for weapons against a target

    This endpoint wraps the existing calculate_group_metrics() function
    from src/engine/calculator.py

    Parameters:
    - weapons: List of weapon profiles to analyze
    - target: Defensive profile to calculate against
    - assume_cover: Apply +1 armor save modifier
    - assume_half_range: Apply range-dependent bonuses (Melta, Rapid Fire)
    - deduplicate_exclusive: Apply Profile ID optimization

    Returns:
    - metrics: Per-weapon efficiency calculations (CPK, TTK, Kills, etc.)
    - summary statistics
    """
    try:
        # Convert Pydantic models to DataFrame for calculator
        weapon_dicts = [weapon_to_dict(w) for w in request.weapons]
        df = pd.DataFrame(weapon_dicts)

        # Convert target to dict
        target_dict = target_to_dict(request.target)

        # Apply cover modifier if requested
        if request.assume_cover and target_dict.get('Sv'):
            # Convert "3+" to 2+, "4+" to 3+, etc.
            current_save = int(target_dict['Sv'].replace('+', ''))
            if current_save > 2:  # Can't improve past 2+
                improved_save = current_save - 1
                target_dict['Sv'] = f"{improved_save}+"

        # Call existing calculator function
        metrics_list = calculate_group_metrics(
            df=df,
            target_profile=target_dict,
            deduplicate=request.deduplicate_exclusive,
            assume_half_range=request.assume_half_range
        )

        # Convert results to Pydantic models
        metric_results = []
        total_kills = 0.0
        total_points = 0

        for metric in metrics_list:
            metric_result = MetricResult(
                UnitID=metric.get('UnitID', ''),
                Name=metric.get('Name', ''),
                Weapon=metric.get('Weapon', ''),
                Qty=metric.get('Qty', 1),
                Pts=metric.get('Pts', 0),
                Kills=metric.get('Kills', 0.0),
                Damage=metric.get('Damage', 0.0),
                CPK=metric.get('CPK', 999.0),
                TTK=metric.get('TTK', 999.0),
                CPK_Grade=metric.get('CPK_Grade', 'F'),
                ProfileID=metric.get('Profile ID', None)
            )
            metric_results.append(metric_result)
            total_kills += metric_result.Kills
            total_points += metric_result.Pts

        # Calculate average CPK
        avg_cpk = total_points / total_kills if total_kills > 0 else 999.0

        return CalculateResponse(
            metrics=metric_results,
            target_name=request.target.Name,
            total_points=total_points,
            total_kills=total_kills,
            avg_cpk=avg_cpk
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Calculation error: {str(e)}"
        )

@router.post("/calculate-multi-target")
async def calculate_multi_target(
    weapons: List[WeaponProfile],
    targets: List[TargetProfile],
    assume_cover: bool = False,
    assume_half_range: bool = False
):
    """
    Calculate metrics against multiple targets (threat matrix)

    Returns a matrix of results for each weapon against each target
    """
    try:
        results = {}

        for target in targets:
            request = CalculateRequest(
                weapons=weapons,
                target=target,
                assume_cover=assume_cover,
                assume_half_range=assume_half_range
            )

            response = await calculate_metrics(request)
            results[target.Name] = response.model_dump()

        return {
            "targets": [t.Name for t in targets],
            "results": results
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Multi-target calculation error: {str(e)}"
        )

@router.get("/health")
async def calculator_health():
    """Health check for calculator engine"""
    return {
        "status": "operational",
        "engine": "PyHammer Calculator v2.0"
    }
