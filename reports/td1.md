# TD 1 — Comparing five models that generate SQL

**Class: DIA1 · Sub-group: DIA1-G2**  
**Session: 21 October 2026 · Pack: 2026-10-18-students-1**  
**Members: Pierre-Olivier WAFO BAKAM, Oryssa Stella TALATALA, Hugo HOUPPE, Cecilia Sessi DOSSA, Tony THEBAUD-PERRIER, Jolan NALLET--PANG**

## Work done and method

We wrote the twenty reference queries C01 to C20 on the `boutique.sqlite` database (seed 20260925), then compared their amounts with an independent computation on the CSV files. All twenty SQL and CSV results agree. The script is [check_references.py](../check_references.py) and the references are in [reference-td1.csv](../TD1/reference-td1.csv). This agreement is our independent check; it does not replace a comparison with an official answer key, which we do not have here.

The queries compute revenue excluding VAT in cents as quantity × unit price, with periods whose start bound is included and end bound excluded, completed age on the given date, and 0 when the sum is empty. For example, being exactly 25 years old on 25 September 2026 corresponds to birth dates in ]2000-09-25; 2001-09-25]. For age at the time of the order, the reference date changes with each order.

We queried the five required models and kept every real attempt, including errors and retries, in [traces-td1.csv](../TD1/traces/traces-td1.csv). The file holds 106 calls for 100 model/question pairs plus six additional attempts. Every row carries `nature=real`. For each question, the same prompt fingerprint appears for all five models. The exact prompt text is in [prompts-en.md](../TD1/prompts-en.md): it is the kit prompt, used unchanged, and the twenty fingerprints in the traces match this text. The raw state files `state-A.jsonl` to `state-E.jsonl` and their merge `traces-td1.jsonl` are kept in [TD1/traces](../TD1/traces/).

For the final tables, we keep the last attempt of each pair, ordered by `attempts`, then `date_utc` and, on a tie, record order. Every attempt stays in the traces. The success rate always uses twenty questions per model; an API error or a rejected SQL query is not counted as a correct answer.

## Results

| Model | Correct / 20 | Rate | Wrong amounts | Invalid / rejected SQL | Not executed |
|---|---:|---:|---:|---:|---:|
| Groq GPT-OSS 120B | 20 | 100 % | 0 | 0 | 0 |
| Groq GPT-OSS 20B | 19 | 95 % | 1 | 0 | 0 |
| OpenRouter Cohere North Mini Code | 13 | 65 % | 6 | 1 | 0 |
| Groq Qwen3.8-27B | 14 | 70 % | 4 | 0 | 2 |
| OpenRouter Dots3-Note Preview | 12 | 60 % | 7 | 1 | 0 |

In total: 78 correct answers, 18 wrong amounts, one invalid SQL query, one rejected output and two questions not executed. The [detailed results](../TD1/results/model-question-comparison-en.csv) give the cell identifiers, trace pointers and one explanation per failure. The [pivot view](../TD1/results/pivot-view.md) eases comparison, and the [five-model summary](../TD1/results/five-model-summary-en.csv) documents results by family, public indices, access routes and prices.

| Model | Period (6) | Age (5) | Products (4) | Combined (5) |
|---|---:|---:|---:|---:|
| GPT-OSS 120B | 6/6 | 5/5 | 4/4 | 5/5 |
| GPT-OSS 20B | 6/6 | 4/5 | 4/4 | 5/5 |
| Cohere | 6/6 | 1/5 | 4/4 | 2/5 |
| Qwen | 5/6 | 5/5 | 4/4 | 0/5 |
| Dots | 6/6 | 0/5 | 4/4 | 2/5 |

Families follow the assignment table: period C01/C04/C05/C06/C07/C20; age C02/C08/C09/C10/C11; products C03/C12/C13/C14; combined C15–C19. Qwen's 0/5 includes four wrong amounts and one call not executed. Its 5/6 on periods includes one call not executed.

## Failures and observed causes

- **GPT-OSS 20B, C02:** the birth-date range selects children born in 2025–2026 instead of 25-year-old customers; result 0 against 590320 cents expected.
- **Cohere:** the six wrong amounts all involve age conditions, sometimes combined with a period or products. C09 contains `AS age` inside a `WHERE` expression, which causes a syntax error.
- **Qwen:** C15 imposes incompatible birthday conditions at the same time. C16 and C17 invert the inclusion of birthdays at the bounds of age 25; changing these two operators restores the reference amounts. C19 uses a wrong age condition mixing a year and a full date.
- **Dots:** several queries exclude customers who are still 25 but born in 2000, because they require a year difference of 25 and a birthday already passed. C02 adds restrictions that were not asked for, and C10 contains contradictory conditions. C11 returns Markdown, prose and several proposals instead of a single `SELECT`; the output is rejected as `not_select`.
- **API access:** the traces contain eight HTTP 429 responses. GPT-OSS 20B retries on C18/C19 succeed. Qwen stays blocked on C18/C20 after two attempts per question, with an output-tokens-per-minute limit reported at 1000. No amount is available for these two cells: they stay empty and do not prove a numerical error by the model.

Questions C02, C15 and C17 fail for three models out of five. The completed-age convention, in particular birthdays at the bounds and the difference between age on a fixed date and age at the time of the order, is therefore a priority for TD 2.

The 96 trace queries with a `correct` or `incorrect` verdict were re-executed read-only on the official database during the assisted analysis: the recorded amounts were reproduced. These additional checks triggered no new model call.

## Decisions, limits and uncertainties

On this batch, GPT-OSS 20B matches 120B on the period, product and combined families; 120B is the only model to answer all twenty questions correctly. All five models answer the four product-family questions correctly. This suggests studying, in TD 2, a selection by question family and explicit age checks, without replacing the routing rule required by the workshop.

These observations cover a single database, twenty questions and the attempts we kept. They are not a general ranking. An amount equal to the reference does not prove the query is valid on any other database, especially when the expected result is 0. Differences in parameters, quotas and variability may affect comparisons between sub-groups; this experiment does not isolate their effects.

The access routes used are free. The paid prices in the summary describe a documented route of the same model, when it was verified; they are not expenses of our experiment. Groq native costs are missing from the traces and stay empty. The forty OpenRouter calls report a native cost of zero. Public indices may correspond to different reasoning settings: they put the results in context without explaining them on their own. Unverified information is marked `N/A` with a reason.

No replayed or synthetic row enters the scores presented. We do not have a written official answer key to compare our references with. All the work is published in the sub-group's public repository and can be replayed without an API key using the README commands (`--replay` mode).

## AI assistance and contributions

AI assistance was used to prepare the queries and the CSV check, analyse the traces, produce the tables and write the documents. Members must review this material and be able to explain the choices. AI tools and uses: Claude for references check,trace analysis and some documentation.Every result was re-run and verified by the group

| Member | Actual contribution |
|---|---|
| Oryssa Stella TALATALA | Operator A: ran GPT-OSS 120B on the 20 questions (`state-A.jsonl`, `traces-A.csv`). Checked references C10–C12. |
| Jolan NALLET--PANG | Operator B: ran GPT-OSS 20B on the 20 questions (`state-B.jsonl`, `traces-B.csv`). Consolidated the traces: collected the raw files of the five operators (`state-A.jsonl` to `state-E.jsonl`, `traces-A.csv` to `traces-E.csv`), merged them into `traces-td1.csv` and published them in the repository. Checked references C04–C06 and C19. |
| Cecilia Sessi DOSSA | Operator C: ran Cohere North Mini Code on the 20 questions (`state-C.jsonl`, `traces-C.csv`). Checked references C13–C15. |
| Tony THEBAUD-PERRIER | Operator D: ran Qwen3.8-27B on the 20 questions (`state-D.jsonl`, `traces-D.csv`). Checked references C01–C03. |
| Hugo HOUPPE | Operator E: ran Dots3-Note Preview on the 20 questions (`state-E.jsonl`, `traces-E.csv`). Checked references C16–C18. |
| Pierre-Olivier WAFO BAKAM | Role F. Wrote references C04–C06; checked C07–C09 and C20. Created the public repository, published `reference-td1.csv` and `traces-td1.jsonl`, organised the repository by TD. |

## Next steps

- Present the pivot view and compare the traces behind the gaps with the other sub-groups.
- Name the member preparing TD 2: **Hugo**. Read `atelier-vote.py` and the expected routing rule.
- Check that the repository opens without signing in, and submit in Moodle the URL, the full commit hash and the link to this report at that commit before 25 October 2026, 23:59 Paris time.
