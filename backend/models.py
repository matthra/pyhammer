"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Union, Dict, Any
from enum import Enum

# --- Request/Response Models ---

class WeaponProfile(BaseModel):
    """Individual weapon profile"""
    model_config = {
        "extra": "allow",
        "populate_by_name": True,  # Allow both field name and alias
        "by_alias": True  # Use aliases when serializing
    }

    UnitID: str
    Name: str
    Qty: int
    Pts: int
    Weapon: str
    Range: Union[str, float]  # Can be "M" for melee or numeric
    A: Union[str, int]  # Attacks (can be "D6", "2D6", etc.)
    BS: int = Field(ge=2, le=6)  # Ballistic/Weapon Skill 2-6
    S: int = Field(ge=1, le=14)  # Strength
    AP: int = Field(ge=-6, le=0)  # Armor Penetration
    D: Union[str, int]  # Damage (can be "D6", "D6+3", etc.)
    Blast: str = Field(default="N", pattern="^[YN]$")
    Melta: int = Field(default=0, ge=0, le=6)
    RapidFire: int = Field(default=0, ge=0, le=6)
    TwinLinked: str = Field(default="N", pattern="^[YN]$")
    Lethal: str = Field(default="N", pattern="^[YN]$")
    Dev: str = Field(default="N", pattern="^[YN]$")
    Torrent: str = Field(default="N", pattern="^[YN]$")
    IgnoresCover: str = Field(default="N", pattern="^[YN]$")
    CritHit: int = Field(default=6, ge=2, le=6)
    CritWound: int = Field(default=6, ge=2, le=6)
    Sustained: int = Field(default=0, ge=0, le=6)
    FNP: str = Field(default="")  # "4+", "5+", "6+", or ""
    ProfileID: Optional[str] = None  # For exclusive weapon modes
    LoadoutGroup: Optional[str] = Field(default="Standard", alias="Loadout Group")  # Loadout grouping
    Keywords: Optional[str] = Field(default="")  # Unit keywords
    RR_H: Optional[str] = Field(default="N", pattern="^[YN]$")  # Reroll hits
    RR_W: Optional[str] = Field(default="N", pattern="^[YN]$")  # Reroll wounds

class TargetProfile(BaseModel):
    """Defensive target profile"""
    Name: str
    Pts: int
    T: int = Field(ge=1, le=14)  # Toughness
    W: int = Field(ge=1, le=30)  # Wounds
    Sv: str = Field(pattern=r"^[2-7]\+$")  # Armor save "2+" through "7+"
    Inv: str = Field(default="")  # Invuln save "4+", "5+", "6+", or ""
    FNP: str = Field(default="")  # Feel No Pain
    Stealth: str = Field(default="N", pattern="^[YN]$")
    UnitSize: int = Field(default=1, ge=1)  # For Blast calculations

class CalculateRequest(BaseModel):
    """Request to calculate metrics for weapons against a target"""
    weapons: List[WeaponProfile]
    target: TargetProfile
    assume_cover: bool = False
    assume_half_range: bool = False
    deduplicate_exclusive: bool = True

class MetricResult(BaseModel):
    """Single weapon's calculated metrics"""
    UnitID: str
    Name: str
    Weapon: str
    Qty: int
    Pts: int
    Kills: float
    Damage: float
    CPK: float  # Cost per kill
    TTK: float  # Time to kill (activations)
    CPK_Grade: str  # S, A, B, C, D, F
    ProfileID: Optional[str] = None

class CalculateResponse(BaseModel):
    """Response with calculated metrics"""
    metrics: List[MetricResult]
    target_name: str
    total_points: int
    total_kills: float
    avg_cpk: float

class RosterSummary(BaseModel):
    """Summary of available rosters"""
    filename: str
    name: str
    total_points: int
    unit_count: int
    weapon_count: int

class TargetListSummary(BaseModel):
    """Summary of available target lists"""
    filename: str
    name: str
    target_count: int
    targets: List[str]  # List of target names

class SaveRosterRequest(BaseModel):
    """Request to save a roster"""
    filename: str
    weapons: List[WeaponProfile]

class SaveTargetListRequest(BaseModel):
    """Request to save a target list"""
    filename: str
    targets: List[TargetProfile]

class ChartType(str, Enum):
    """Available chart types"""
    THREAT_MATRIX = "threat_matrix"
    EFFICIENCY_CURVE = "efficiency_curve"
    TTK_HEATMAP = "ttk_heatmap"
    UNIT_COMPARISON = "unit_comparison"

class ChartRequest(BaseModel):
    """Request to generate a chart"""
    chart_type: ChartType
    weapons: List[WeaponProfile]
    targets: List[TargetProfile]
    assume_cover: bool = False
    assume_half_range: bool = False
    theme: str = "plotly"  # Theme name from themes.json

class ChartResponse(BaseModel):
    """Response with Plotly chart JSON"""
    chart_json: Dict[str, Any]  # Plotly figure as JSON
    chart_type: str
