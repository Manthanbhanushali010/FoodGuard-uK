from typing import Any, Dict
from pydantic import Field

from spoon_ai.chat import ChatBot
from spoon_ai.agents import ToolCallAgent
from spoon_ai.tools import ToolManager

from tools.food_risk_tool import FoodRiskTool
from tools.neo_voucher_tool import NeoVoucherTool
import json


class FoodGuardAgent(ToolCallAgent):
    """
    Main SpoonOS agent handling:
    - risk calculation
    - LLM reasoning
    - policy selection
    - conditional Neo voucher issuance
    """

    name: str = "foodguard_agent"
    description: str = (
        "Agent that processes food-supply signals, computes inflation risk, "
        "asks an LLM for the recommended welfare action, and optionally triggers "
        "a (simulated) Neo voucher issuance."
    )

    system_prompt: str = (
        "You are FoodGuard UK, an AI assistant for early-warning and welfare planning. "
        "Given signals and a risk score, pick one action: "
        "DO_NOTHING, WARN_COUNCILS, PRE_ALLOCATE_FUNDS, or ISSUE_VOUCHERS. "
        "Return JSON: {'action': '...', 'rationale': '...', 'suggested_amount': number}."
    )

    max_steps: int = 5

    # Register custom tools
    available_tools: ToolManager = Field(
        default_factory=lambda: ToolManager([
            FoodRiskTool(),
            NeoVoucherTool(),
        ])
    )

    async def run_with_signals(self, signals: Dict[str, Any]) -> Dict[str, Any]:
        """
        Full pipeline:
            1) Compute risk (FoodRiskTool)
            2) Ask LLM for policy
            3) If vouchers, call NeoVoucherTool
        """

        # STEP 1 — Calculate risk
        risk = await self.available_tools["food_risk_tool"].execute(
            commodity_index=signals["commodity_index"],
            export_ban_severity=signals["export_ban_severity"],
            crop_stress=signals["crop_stress"],
            retail_spike=signals["retail_spike"],
        )

        # STEP 2 — Ask LLM to choose an action
        lm = self.llm or ChatBot()
        prompt = (
            "Given:\n"
            f"Risk Score: {risk['risk_score']}\n"
            f"Risk Level: {risk['risk_level']}\n"
            f"Signals: {signals}\n\n"
            "Pick ONE action only: DO_NOTHING, WARN_COUNCILS, PRE_ALLOCATE_FUNDS, ISSUE_VOUCHERS.\n"
            "Return as JSON: {'action': '...', 'rationale': '...', 'suggested_amount': number}"
        )

        llm_res = await lm.chat(messages=[{"role": "user", "content": prompt}])
        try:
            policy = json.loads(llm_res.content)
        except Exception:
            policy = {
                "action": "WARN_COUNCILS",
                "rationale": "Failed to parse LLM JSON. Using fallback.",
                "suggested_amount": 0,
            }

        # STEP 3 — If vouchers, call Neo tool (simulated)
        action = policy.get("action", "WARN_COUNCILS")
        neo_tx = None

        if action == "ISSUE_VOUCHERS" and policy.get("suggested_amount", 0) > 0:
            neo_tx = await self.available_tools["neo_voucher_tool"].execute(
                recipient="UK_FOOD_BANK_NETWORK_SIM",
                amount=float(policy["suggested_amount"]),
                risk_level=risk["risk_level"],
            )

        return {
            "signals": signals,
            "risk": risk,
            "policy": policy,
            "neo_execution": neo_tx,
        }
