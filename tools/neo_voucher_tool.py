import time
from typing import Dict, Any
from spoon_ai.tools.base import BaseTool


class NeoVoucherTool(BaseTool):
    """
    Simulated Neo blockchain voucher issuance.
    Returns a fake tx object for demo.
    """

    name: str = "neo_voucher_tool"
    description: str = "Simulate issuing food support vouchers via Neo."

    parameters: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "recipient": {"type": "string"},
            "amount": {"type": "number"},
            "risk_level": {"type": "string"}
        },
        "required": ["recipient", "amount", "risk_level"]
    }

    async def execute(
        self,
        recipient: str,
        amount: float,
        risk_level: str,
    ) -> Dict[str, Any]:

        fake_tx = f"0xNEOFAKE{int(time.time())}"

        return {
            "status": "SIMULATED_EXECUTION",
            "network": "neo-testnet-simulated",
            "txid": fake_tx,
            "recipient": recipient,
            "amount": amount,
            "risk_level": risk_level,
        }
