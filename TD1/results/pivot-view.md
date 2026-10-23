# Pivot view — DIA1-G2

Last attempt of each model/question pair. Every attempt remains in [traces-td1.csv](../traces/traces-td1.csv).

**OK**: correct · **WRG**: wrong amount · **INV**: invalid SQL · **REJ**: rejected output · **NE**: not executed.

| Model | C01 | C02 | C03 | C04 | C05 | C06 | C07 | C08 | C09 | C10 |
|---|---|---|---|---|---|---|---|---|---|---|
| GPT-OSS 120B | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK |
| GPT-OSS 20B | OK | WRG | OK | OK | OK | OK | OK | OK | OK | OK |
| Cohere | OK | WRG | OK | OK | OK | OK | OK | OK | INV | WRG |
| Qwen | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK |
| Dots | OK | WRG | OK | OK | OK | OK | OK | WRG | WRG | WRG |

| Model | C11 | C12 | C13 | C14 | C15 | C16 | C17 | C18 | C19 | C20 |
|---|---|---|---|---|---|---|---|---|---|---|
| GPT-OSS 120B | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK |
| GPT-OSS 20B | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK |
| Cohere | WRG | OK | OK | OK | WRG | OK | WRG | OK | WRG | OK |
| Qwen | OK | OK | OK | OK | WRG | WRG | WRG | NE | WRG | NE |
| Dots | REJ | OK | OK | OK | WRG | WRG | WRG | OK | OK | OK |

C02, C15 and C17 fail for three models out of five. Qwen C18/C20 are blocked by HTTP 429; no amount is available. See the [explanations and trace pointers](model-question-comparison-en.csv).
