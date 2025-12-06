FoodGuard UK — Early Warning Agent for Food Inflation (SpoonOS + Neo)

FoodGuard UK is a small prototype exploring whether an autonomous agent can spot early signs of food-price pressure, reason about possible outcomes, and prepare support before households feel the impact.

It uses SpoonOS for agent orchestration and Neo (simulated) for transparent voucher issuance.
The goal is not perfect prediction — it’s to demonstrate a clear, end-to-end autonomous loop:

signals → risk scoring → LLM policy → optional voucher action → audit output

This mirrors the type of workflow public-sector systems struggle with today.

🔧 How the Prototype Works
1. Input Signals (mocked for now)

The agent reads a few high-level indicators related to food supply stress:

commodity index

export ban severity

crop stress

supermarket retail spike

These are passed to the first custom tool.


2. FoodRiskTool → Inflation Risk Score

A custom SpoonOS tool converts the above signals into a 0–100 inflation-risk score using a simple weighted heuristic.

Output includes:

risk_score: 0–100
risk_level: CALM / ELEVATED / HIGH / CRISIS


. LLM Decision via SpoonOS

The agent then asks an LLM (invoked through SpoonOS's ChatBot):

“Given this risk level, what action should be taken?”

The LLM must choose exactly one:

DO_NOTHING

WARN_COUNCILS

PRE_ALLOCATE_FUNDS

ISSUE_VOUCHERS

It also returns a short explanation and (optionally) a suggested amount.

This demonstrates the required SpoonOS pattern:
Agent → LLM → structured policy output.


NeoVoucherTool → Simulated Voucher Action

If the LLM recommends issuing vouchers, the agent calls the second custom tool, which simulates a Neo blockchain transaction.

A realistic testnet-style object is returned (txid, recipient, amount, network).

This provides a transparent trace of agent reasoning → on-chain action.


5. Final Output

Running the prototype prints:

the input signals

computed risk

policy selected by LLM

simulated Neo transaction (or no action)

All together, this forms a fully observable decision pipeline


Project Structure
FoodGuard-UK/
 ├─ README.md
 ├─ requirements.txt
 ├─ .env.example
 ├─ config.json
 ├─ main.py
 ├─ agents/
 │   └─ foodguard_agent.py
 └─ tools/
     ├─ food_risk_tool.py
     └─ neo_voucher_tool.py


Running the Prototype
1. Install dependencies
pip install -r requirements.txt

2.Create your local environment file
cp .env.example .env

3.Run the agent
python main.py


Environment Variables & Security Note:

This repository contains a .env.example file with placeholder variables.

Real API keys have not been committed for security reasons.

Anyone running the prototype locally should create their own .env.
Judges do not need real keys to evaluate the code — the Neo component is simulated, and the SpoonOS LLM interface is configured generically.
