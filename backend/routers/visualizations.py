"""
Visualizations API Router
Handles chart generation using existing PyHammer visualization functions
"""
from fastapi import APIRouter, HTTPException
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from src.visualizations.charts import (
    plot_threat_matrix_interactive,
    plot_efficiency_curve_interactive,
    plot_strength_profile,
    plot_army_damage
)
from ..models import ChartRequest, ChartResponse, ChartType
from .calculator import weapon_to_dict, target_to_dict

router = APIRouter()

@router.post("/chart", response_model=ChartResponse)
async def generate_chart(request: ChartRequest):
    """
    Generate a Plotly chart

    Available chart types:
    - threat_matrix: Heatmap of all weapons vs all targets
    - efficiency_curve: CPK efficiency curves
    - ttk_heatmap: Time-to-kill heatmap
    - unit_comparison: Bar chart comparing unit performance
    """
    try:
        # Convert weapons to DataFrame
        weapon_dicts = [weapon_to_dict(w) for w in request.weapons]
        weapons_df = pd.DataFrame(weapon_dicts)

        # Convert targets to list of dicts
        targets_list = [target_to_dict(t) for t in request.targets]

        # Generate the appropriate chart
        if request.chart_type == ChartType.THREAT_MATRIX:
            fig = plot_threat_matrix_interactive(
                weapons_df=weapons_df,
                targets_list=targets_list,
                assume_cover=request.assume_cover,
                assume_half_range=request.assume_half_range,
                theme=request.theme
            )

        elif request.chart_type == ChartType.EFFICIENCY_CURVE:
            fig = plot_efficiency_curve_interactive(
                weapons_df=weapons_df,
                targets_list=targets_list,
                assume_cover=request.assume_cover,
                assume_half_range=request.assume_half_range,
                theme=request.theme
            )

        elif request.chart_type == ChartType.TTK_HEATMAP:
            fig = plot_strength_profile(
                weapons_df=weapons_df,
                targets_list=targets_list,
                assume_cover=request.assume_cover,
                assume_half_range=request.assume_half_range,
                theme=request.theme
            )

        elif request.chart_type == ChartType.UNIT_COMPARISON:
            fig = plot_army_damage(
                weapons_df=weapons_df,
                targets_list=targets_list,
                assume_cover=request.assume_cover,
                assume_half_range=request.assume_half_range,
                theme=request.theme
            )

        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown chart type: {request.chart_type}"
            )

        # Convert Plotly figure to JSON
        chart_json = fig.to_dict()

        return ChartResponse(
            chart_json=chart_json,
            chart_type=request.chart_type.value
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Chart generation error: {str(e)}"
        )

@router.get("/themes")
async def get_available_themes():
    """Get list of available Plotly themes"""
    try:
        # Read themes from themes.json
        themes_path = Path(__file__).parent.parent.parent / "src" / "visualizations" / "themes.json"

        if themes_path.exists():
            import json
            with open(themes_path, 'r') as f:
                themes = json.load(f)
            return {"themes": list(themes.keys())}
        else:
            # Return default Plotly themes
            return {
                "themes": [
                    "plotly",
                    "plotly_white",
                    "plotly_dark",
                    "ggplot2",
                    "seaborn",
                    "simple_white"
                ]
            }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error loading themes: {str(e)}"
        )
