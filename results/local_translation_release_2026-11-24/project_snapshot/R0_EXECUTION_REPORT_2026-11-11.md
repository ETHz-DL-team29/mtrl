# Actual execution results

Record date: 2026-11-11; generated: 2026-11-12T00:07:04+01:00

**R0 screen not passed; diagnostic candidate only。**

The formal run optimized 199,856 target tokens against a requested budget of 200,000. The dev-selected checkpoint has chrF++ 25.92, structural failure 16.28%, and wrong-language rate 0.00%. This is a single-seed SFT result. No DAPO updates or novel-method gains are claimed.

On the same formal dev pool, the original base scores **13.43 chrF++**, with **38.37% structural failure**. This provides a matched descriptive comparison for this run.

## Protocol

Original model `Qwen/Qwen3.5-0.8B`, pinned revision `2fc06364715b967f1860aea9cf38778875588b17`; LoRA r16/alpha32/dropout0.05. Tesla T4 uses FP16, initial loss scale512 and SDPA, falling back to reference implementations when FLA/causal_conv1d is absent. Microbatch2, effective batch16. CE includes target tokens and EOS, excludes prompt/padding, normalizes by actual target tokens and never truncates labels.

Both equal-budget pilots and the formal run start from the same original base. The formal 300k-token LR schedule was frozen before formal updates. Any continuation retains optimizer, scaler, RNG, data cursor and schedule. Pilot scores use 32 prompts; formal scores use 86 prompts. They are separate evaluation pools.

`formal_100k`The directory name `formal_100k` denotes the initial stop; the summary and this report record the actual continued budget and token count.

Generation uses greedy decoding with thinking disabled. Dev allows 768 prompt and 256 new tokens; final sentences allow 128 new tokens and documents 512, with the same 768-prompt-token cap. Document input/output limits constrain interpretation; this is a bounded transfer diagnostic, not a length-complete document benchmark.

## Data and limitations

The data are aligned sentences/short spans, not full-document training examples. Exact deduplication and automatic filtering do not establish semantic gold quality or document-level independence. The 60-pair AI-assisted audit is not native-speaker certification.

A 100k budget covers about 0.312 epoch; 300k covers about 0.936 epoch. Longer targets yield fewer complete-example/EOS exposures for the same token budget, so equal tokens do not imply equal convergence to the historical short-sentence run.

## Learning-rate pilots


### pilot_lr5e-5

| Target tokens | NLL | chrF++ | Failure | Wrong language | Eval s |
|---:|---:|---:|---:|---:|---:|
| 0 | 2.9754 | 12.55 | 34.38% | 0.00% | 321.8 |
| 11,043 | 2.8189 | 12.16 | 46.88% | 12.50% | 411.4 |
| 19,983 | 2.7418 | 14.03 | 40.62% | 0.00% | 358.4 |


### pilot_lr1e-4

| Target tokens | NLL | chrF++ | Failure | Wrong language | Eval s |
|---:|---:|---:|---:|---:|---:|
| 0 | 2.9754 | 12.55 | 34.38% | 0.00% | 319.6 |
| 11,043 | 2.7680 | 14.22 | 43.75% | 3.12% | 381.8 |
| 19,983 | 2.6755 | 13.80 | 34.38% | 3.12% | 350.4 |


Pilot learning-rate selection follows the prespecified constraints→chrF++→NLL rule. Best scores differ little and use one seed; statistical significance is not established. Constraint-failing pilots are not qualified R0 models.

## Formal development curve

| Target tokens | NLL | chrF++ | Failure | Wrong language | Eval s |
|---:|---:|---:|---:|---:|---:|
| 0 | 2.9754 | 13.43 | 38.37% | 5.81% | 903.0 |
| 25,522 | 2.6494 | 15.24 | 39.53% | 1.16% | 1004.9 |
| 50,064 | 2.5047 | 17.53 | 27.91% | 1.16% | 822.5 |
| 75,966 | 2.4095 | 17.85 | 32.56% | 1.16% | 876.3 |
| 99,977 | 2.3340 | 24.16 | 15.12% | 0.00% | 631.3 |
| 100,791 | 2.3312 | 23.83 | 20.93% | 0.00% | 703.4 |
| 125,451 | 2.2747 | 21.31 | 25.58% | 1.16% | 750.2 |
| 150,066 | 2.2250 | 23.20 | 20.93% | 1.16% | 688.9 |
| 175,027 | 2.1788 | 25.92 | 16.28% | 0.00% | 630.0 |
| 199,856 | 2.1424 | 25.23 | 17.44% | 2.33% | 611.5 |

![Learning curves: pilot and formal pools are separate](R0_learning_curves_2026-11-11.png)

The selection rule prefers structurally eligible checkpoints, then higher chrF++ and lower NLL. Eligibility is necessary, not sufficient for semantic quality. Lower NLL alone does not justify readiness for RL.

### Selected-checkpoint dev source groups

| Dataset | Count | chrF++ | Failure |
|---|---:|---:|---:|

| OPUS-tatoeba-v20230412-eng-isl | 32 | 19.85 | 3.12% |

| ParIce | 54 | 26.59 | 24.07% |

## Translation examples

**OPUS-tatoeba-v20230412-eng-isl:42** — gate=True, repetition=False, wrong_language=False

<pre><code>English: You know the phrase, we reap what we sow. I have sown the wind and this is my storm.
Reference: Þið þekkir orðatiltækið: „Við yrkjum það sem við höfum sáð.“ Ég hef sáð vindinum og þetta er stormurinn minn.
Model: Þú veitir að þessi sýnir er að við ræpa þér sem við sýr. Ég sýr þung og þessi er minn.</code></pre>

**ParIce:596349** — gate=True, repetition=False, wrong_language=False

<pre><code>English: That notification shall comprise the documentation and information set out in Annex IV.
Reference: Sú tilkynning skal taka til gagna og upplýsinga sem settar eru fram í IV. viðauka.
Model: Þessi upplýsingar skal innihalda skráningu og upplýsingar sem mælt er fyrir um í IV. viðauka.</code></pre>

**ParIce:407070** — gate=True, repetition=False, wrong_language=False

<pre><code>English: disease sometimes refractory to treatment with pyrimethamine, and therefore an alternative is required.
Reference: meðferð með pýrimetamíni nægir stundum ekki til að ráða niðurlögum sjúkdómsins og því er þörf á öðrum valkosti.
Model: hættur eðlið oft ekki meðferð með pyrimetamína og þar með er nauðsynlegt að taka viðeigandi aðferð.</code></pre>

**OPUS-tatoeba-v20230412-eng-isl:6206** — gate=True, repetition=False, wrong_language=False

<pre><code>English: It&#x27;s nothing to worry about.
Reference: Það er ekkert til að hafa áhyggjur af.
Model: Það er ekki að hafa áhættu við.</code></pre>

**ParIce:509289** — gate=False, repetition=False, wrong_language=False

<pre><code>English: (13) In accordance with the UNFCCC, the Kyoto Protocol and subsequent decisions adopted for their implementation, the Commission and the Member States should support capacity building activities in developing countries and countries with economies in transition in order to help them take full advantage of JI and the CDM in a manner that supports their sustainable development strategies.
Reference: 13) Í samræmi við rammasamning Sameinuðu þjóðanna um loftslagsbreytingar, Kýótóbókunina og síðari ákvarðanir, sem hafa verið samþykktar til framkvæmdar þeim, skulu framkvæmdastjórnin og aðildarríkin styðja aðgerðir til uppbyggingar færni í þróunarlöndum og löndum með umbreytingarhagkerfi í því skyni að aðstoða þau við að nýta sér kerfi sameiginlegrar framkvæmdar og kerfi hreinleikaþróunar til fulls á þann hátt sem hæfir áætlunum þeirra um sjálfbæra þróun.
Model: 13) Í samræmi við aðildarríkiþinginu, viðyrim ákvæði Evrópusambandsins og framkvæmdarákvæðum sem þeirra hefur verið átt við að framkvæma þau skal framkvæmdastjórnin og aðildarríkið stjórnast með því að stjórnast með þeim aðgerðum sem þeirra hefur verið átt við að gera aðgerðir í aðgerðarþingum aðildarríkja og aðgerðir í aðgerðarþingum aðildarríkja með aðgerðum í aðgerðarþingum aðildarríkja með aðgerðum í aðgerðarþingum aðildarríkja með aðgerðum í aðgerðarþingum aðildarríkja með aðgerðum í aðgerðarþingum aðildarríkja með aðgerðum í aðgerðarþingum aðildarríkja með aðgerðum í aðgerðarþingum aðildarríkja með aðgerðum í</code></pre>

**ParIce:804526** — gate=False, repetition=True, wrong_language=False

<pre><code>English: A pensioner who is entitled to draw pensions under the legislation of two or more Member States, of which one is that of the Member State in whose territory he resides, and who is entitled to benefits under the legislation of the latter Member State, taking account where appropriate of the provisions of Article 18 and Annex VI, shall, with the members of his family, receive such benefits from the institution of the place of residence and at the expense of that institution as though the person concerned were a pensioner whose pension was payable solely under the legislation of the latter Member State.
Reference: Lífeyrisþegi sem á rétt á lífeyri samkvæmt löggjöf tveggja eða fleiri aðildarríkja, að meðtalinni löggjöf þess aðildarríkis sem hann er búsettur í, þar sem hann á rétt á bótum samkvæmt löggjöf þess ríkis, með tilliti til ákvæða 18. gr. og VI. viðauka eftir því sem við á, skal, ásamt aðstandendum, fá bætur frá stofnun á búsetustaðnum og á kostnað hennar eins og sá sem í hlut á væri lífeyrisþegi sem ætti eingöngu rétt á lífeyri samkvæmt löggjöf þess ríkis.
Model: Aðildarríki, sem er aðildarríki þeirra aðildarríkjanna sem þeir eru aðildarríki, sem er aðildarríki þeirra aðildarríkjanna sem þeir eru aðildarríki, og sem er aðildarríki þeirra aðildarríkjanna sem þeir eru aðildarríki, sem er aðildarríki þeirra aðildarríkjanna sem þeir eru aðildarríki, sem er aðildarríki þeirra aðildarríkjanna sem þeir eru aðildarríki, sem er aðildarríki þeirra aðildarríkjanna sem þeir eru aðildarríki, sem er aðildarríki þeirra aðildarríkjanna sem þeir eru aðildarríki, sem er aðildarríki þeirra aðildarríkjanna sem þeir eru aðildarríki, sem er aðildarríki þeirra aðildarríkjanna sem þeir eru aðildarríki, sem er aðildarríki þeirra aðildarrí</code></pre>

**ParIce:1697793** — gate=False, repetition=False, wrong_language=False

<pre><code>English: • The European Food Safety Authority (‘the Authority) concluded in its opinion of 27 January 2015 (2) that, under the proposed conditions of use, the preparation of carvacrol, cinnamaldehyde and capsicum oleoresin does not have an adverse effect on animal health, human health or the environment, and that it has a potential to improve the feed to gain ratio in chickens for fattening.
Reference: • Matvælaöryggisstofnun Evrópu (hér á eftir nefnd Matvælaöryggisstofnunin) komst að þeirri niðurstöðu í áliti sínu frá 27. janúar 2015 (2) að við tillögð notkunarskilyrði hafi blanda með karvakróli, sinnamaldehýði og óleóresíni úr Capsicum ekki skaðleg áhrif á heilbrigði dýra eða manna eða á umhverfið og að hún geti bætt fóðurstuðul hjá eldiskjúklingum.
Model: • Evrópskið húðvæðisvísindasjúkdóttur („vísindasjúkdótturinn“) samþykkti í þeirri ófyrirtæku ákvæði frá 27. janúar 2015 (2) að, í samræmi við ákvæðum um notkun, ekki hafi áhrif á þjónustu þjóðar, þjónustu þjóðar eða umhverfið á vegna framleiðslu ácarvórls, cinnamáldeýls og capsicum ólersins og að það hafi mögulega áhrif á fræðilega skilgreiningu fræðilega skilgreiningu fræðilega skilgreiningu fræðilega skilgreiningu fræðilega skilgreiningu fræðilega skilgreiningu fræðilega skilgreiningu fræðilega skilgreiningu fræðilega skilgreiningu fræðilega skilgreining</code></pre>

**ParIce:168696** — gate=False, repetition=True, wrong_language=False

<pre><code>English: • Following the suspension of operations of the Zambian flag carrier Zambian Airways in January 2009 and the publication by ICAO of a significant safety concern in February 2009 after the USOAP Audit visit regarding aircraft operations, certification and supervision exercised by the Civil Aviation Authority of Zambia, the Commission requested information from these auth orities in April 2009 to verify the implementation of corrective actions to redress this concern.
Reference: • Í kjölfar tímabundinnar ógildingar á starfrækslu sambíska flugrekandans Zambian Airways, sem tilnefndur er fánaberi (flag carrier) Sambíu, í janúar 2009, og þess að Alþjóðaflugmálastofnunin birti áhyggjur sínar af alvarlegum öryggisvandamálum í febrúar 2009 að lokinni úttektarheimsókn í tengslum við alþjóðlegt eftirlit með öryggismálum, að því er varðar flugrekstur, vottun og eftirlit flugmálayfirvalda í Sambíu, krafðist framkvæmdastjórnin upplýsinga frá þessum yfirvöldum, í apríl 2009, til að sannreyna framkvæmd aðgerða til úrbóta sem eiga að ráða bót á þessum öryggisvandamálum.
Model: • Þar sem Zambíusflugfélagið Zambíusíðar, sem flugfélag Zambíusíðar, varðarðar Zambíusíðar, varðaði Zambíusíðar, varðaði Zambíusíðar, varðaði Zambíusíðar, varðaði Zambíusíðar, varðaði Zambíusíðar, varðaði Zambíusíðar, varðaði Zambíusíðar, varðaði Zambíusíðar, varðaði Zambíusíðar, varðaði Zambíusíðar, varðaði Zambíusíðar, varðaði Zambíusíðar, varðaði Zambíusíðar, varðaði Zambíusíðar, varðaði Zambíusíðar, varðaði Zambíusíðar, varðaði Zambíusíðar, varðaði Z</code></pre>

Fluency and language-ID success do not establish faithful translation.

The first four fixed dev outputs still show lexical, grammatical and information-preservation problems. The wind/storm imagery is not clearly retained, and worry is rendered as a risk-related concept. Passing the structural gate and language ID does not establish faithful translation.

No corpus-wide semantic error rate is estimated. This is an AI screen, not a blind evaluation or native-speaker gold adjudication.

## Frozen held-out diagnostics

| Group | Count | chrF++ | Gate failures | Truncated | Generation seconds |
|---|---:|---:|---:|---:|---:|

| legacy_sentence_probes | 12 | 29.39 | 1 | 1 | 29.9 |

| wmt_document_transfer | 3 | 14.28 | 2 | 1 | 80.7 |


Held-out gate failures follow the final evaluator's output rules. Dev structural failures also include repetition; readiness strict validity additionally includes language ID. These definitions differ and do not cover all semantic errors.

The historical probes are small and previously viewed. They are not a full WMT benchmark or a fresh blind test. Historical comparisons are descriptive because inference settings differ.

## RL readiness


No G=8 diagnostic was run; address SFT quality before RL if the dev screen fails.


Even an 8-prompt×G8 run is only a small diagnostic. Without actual MetricX ranking validation, it cannot replace the planned 64-prompt readiness audit or be presented as DAPO training.

## Time and compute


Recorded cumulative pipeline wall time: **3.60 hours**. It includes recovery and some controller overhead, not just GPU training or CU billing. The four-hour limit is checked at update boundaries, so a long evaluation can overrun it. Actual CU balance/billing was unavailable; no additional quota was purchased.

| Stage | Recorded update seconds | Completed evaluation seconds | Physical target tokens in raw logs | Recovery replay/retry tokens |
|---|---:|---:|---:|---:|

| pilot_lr5e-5 | 170.8 | 1091.6 | 28,923 | 8,940 |

| pilot_lr1e-4 | 120.9 | 1051.9 | 19,983 | 0 |

| formal_100k | 1275.2 | 7622.1 | 200,613 | 757 |

Wall time from pipeline start to cloud export: **3.66 hours**, including final diagnostics and recovery; local transfer/report work is separate.

Formal committed update throughput: 156.73target tokens/s; peak recorded allocated VRAM: 3.800GB; recorded overflow retries: 1.


Raw logs retain repeated steps after recovery and may omit interrupted, unpersisted work. Completed-evaluation time sums saved metric files and excludes some interrupted evaluations. The ledger separates verifiable update/evaluation time from unclassified wall time. Short probes of 178.20 target tokens/s and 235.11 tokens/s after recovery are not end-to-end throughput or a fair speedup over older Windows hardware.

The recorded wall time excludes data auditing, login, initial environment/model preparation and failed preflights before the original pipeline start. A full study must account for those common preparation costs separately; no complete CU or energy bill was obtained.

Recorded wall time includes recovery. Raw logs preserve replayed updates, while interrupted unlogged work may be missing. Completed-evaluation timings exclude incomplete evaluations. No Colab compute-unit bill was obtained. This SFT run contains no reward-model timing and cannot establish the MetricX fraction of a future RL pipeline.

## Artifacts, reproduction and next decision

- Original workspace:`D:\deep learning project`; original`runs/sft_round1`is preserved in full.
- [Runnable Colab notebook](R0_Qwen35_08B_2026-11-11.ipynb)；[Frozen source and data](R0_colab_bundle_2026-11-11.zip)。
- [Selected adapter and complete evaluation evidence](R0_best_adapter_2026-11-11.zip)；[Machine-readable results](R0_RESULTS_2026-11-11.json)。
- Drive `MyDrive/deep learning project/r0_2026-11-11`Complete recovery checkpoints are preserved; the local inference export excludes AdamW/RNG state.
- [Complete research plan](EFFICIENT_ML_RESEARCH_PLAN_2026-11-11.html)；[Implementation notes](R0_IMPLEMENTATION_2026-11-11.md)。

Load the pinned original base together with`best_adapter`. Do not resolve the local base from the temporary Colab path in adapter_config alone. Original models were neither merged nor overwritten.

If screening fails, the outcome is a reproducible diagnostic candidate rather than an accepted RL baseline. If it passes, semantic and reward-order review still remain. Future efficiency claims require a common frozen R0 and matched end-to-end compute accounting; the SFT implementation itself is not the proposed novelty.
