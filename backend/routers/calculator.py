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
    TargetProfile,
    MultiTargetRequest
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

        # Store cover setting in DataFrame for per-weapon handling
        # We'll handle cover application in the calculator per-weapon
        df['__assume_cover__'] = request.assume_cover

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
async def calculate_multi_target(request: MultiTargetRequest):
    """
    Calculate metrics against multiple targets (threat matrix)

    Returns a matrix of results for each weapon against each target
    """
    # DEBUG: Log received parameters
    print(f"=== CALCULATE MULTI TARGET DEBUG ===")
    print(f"assume_cover: {request.assume_cover}")
    print(f"assume_half_range: {request.assume_half_range}")
    print(f"num_weapons: {len(request.weapons)}")
    print(f"num_targets: {len(request.targets)}")
    print(f"====================================")

    try:
        results = {}

        for target in request.targets:
            calc_request = CalculateRequest(
                weapons=request.weapons,
                target=target,
                assume_cover=request.assume_cover,
                assume_half_range=request.assume_half_range
            )

            response = await calculate_metrics(calc_request)
            results[target.Name] = response.model_dump()

        return {
            "targets": [t.Name for t in request.targets],
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
