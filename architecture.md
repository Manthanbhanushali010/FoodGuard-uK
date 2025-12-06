```mermaid
flowchart TD

A[Input Signals<br>(commodity index,<br>export bans,<br>crop stress,<br>retail spike)]
    --> B[FoodRiskTool<br>(Custom Spoon Tool)]
B --> C[Risk Score + Level]

C --> D[LLM Policy Decision<br>(via SpoonOS ChatBot)]
D -->|Action: DO_NOTHING / WARN / PRE_ALLOCATE| E[Return Policy Only]

D -->|Action: ISSUE_VOUCHERS| F[NeoVoucherTool<br>(Simulated Neo tx)]

E --> G[Final JSON Output]
F --> G[Final JSON Output]



