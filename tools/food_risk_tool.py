from typing import Dict, Any
from spoon_ai.tools.base import BaseTool


class FoodRiskTool(BaseTool):
    """
    Simple heuristic-based risk calculator for food inflation.
    Computes a 0-100 score + category.
    """

    name: str = "food_risk_tool"
    description: str = "Compute food inflation risk score from global supply signals."

    parameters: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "commodity_index": {"type": "number"},
            "export_ban_severity": {"type": "number"},
            "crop_stress": {"type": "number"},
            "retail_spike": {"type": "number"},
        },
        "required": [
            "commodity_index",
            "export_ban_severity",
            "crop_stress",
            "retail_spike",
        ],
    }

    async def execute(
        self,
        commodity_index: float,
        export_ban_severity: float,
        crop_stress: float,
        retail_spike: float,
    ) -> Dict[str, Any]:

        score = (
            commodity_index * 0.4 +
            export_ban_severity * 100 * 0.3 +
            crop_stress * 100 * 0.2 +
            retail_spike * 100 * 0.1
        )
        score = max(0, min(100, score))

        if score < 30:
            level = "CALM"
        elif score < 55:
            level = "ELEVATED"
        elif score < 80:
            level = "HIGH"
        else:
            level = "CRISIS"

        return {"risk_score": round(score, 1), "risk_level": level}
