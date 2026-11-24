# R0原因定位：预先登记方案 / R0 cause diagnosis: registered protocol

2026-11-17。用户已授权。保持0.8B、原R0与既有模型不变，使用独立Colab L4。此文件是执行前方案，不是已获得的结论。 / Authorized protocol before new results; preserve all prior models.

问题：区分训练样本拟合不足、学习率/LoRA适配限制与保留样本泛化不足。此次不能证明0.8B的绝对SFT上限。 / Separate training-fit, optimization/adapter restrictions and held-out generalization; an absolute model ceiling is not identified by a small probe.

## 1. 固定数据 / Fixed data

训练32对来自上一轮通过质量复查且选中20万检查点确实见过的文对；本次运行前再次逐条阅读。全部在上一轮前5280次曝光内出现过一次，不代表基础模型或更早SFT只见过一次。另固定32对开发文对，排除既有G8难例，不参与训练。两批均8通用、4技术短、10中、10长。

Training32 are quality-reviewed pairs exposed in the selected checkpoint prefix, read again before this run. Each appeared once in that continuation, not necessarily once in earlier training. Held-out32 are a fixed random stratified development subset excluding knownG8 diagnostics, never used in updates. Both:8 general,4 short,10 medium,10 long.

选取种子2026111711/2026111712，仅按来源、分层、是否见过及质量状态选取，不按模型得分筛选。训练32对合计2322个目标token（含EOS）。保留集已在历史开发评估中使用，不是全新独立测试。 / Fixed seeds and eligibility, not outcome-based selection;2322 target tokens in training32;held-out data are reused development,not untouched test.

## 2. 第一阶段 / Phase1

原R0、选中20万、训练末期40万三个模型，对两批样本重新生成greedy译文，并逐句计算teacher-forced NLL。使用相同BF16舍入base再提升FP32，关闭TF32，max320。旧输出只用于逐token一致性核对，新对比使用本运行时重新生成的输出。

Regenerate train/held-out32 for original R0,SFT200 andSFT400. Report per-pair teacher NLL and greedy outputs on matched FP32 promotion of the same BF16-rounded base,TF32 off,max320. Prior outputs are parity checks,not mixed into the new comparison.

先核对完整logits显式移位损失与tail-logit目标损失，再核对左填充batch与逐句损失。若出现实质不一致，先中止拟合对照并定位，不把它误判为模型容量问题。 / Audit explicit shifted loss versus optimized tail loss and padded-batch versus individual losses;material discrepancy stops fitting.

## 3. 条件性小集合拟合 / Conditional fitting

若SFT200未达到描述性的近似记忆标准：训练NLL≤0.2、chrF++≥85、规范化参考精确匹配率≥50%，进入第二阶段。该标准是拟合诊断工具，不是翻译质量或DAPO合格门槛。 / The memorization-like trigger is descriptive,not a translation or DAPO qualification rule.

| Condition | Initial weights | Rank | Peak LR | Run condition |
| --- | --- | --- | --- | --- |
| A_lowLR | SFT200 | 16 | 1e-5 | If phase2 triggered |
| B_highLR | SFT200 | 16 | 1e-4 | If phase2 triggered |
| C_r64 | Function-preserving SFT200 | 64 | 1e-4 | Only if B fails registered fitting criterion |

每组独立fresh AdamW；相同样本顺序种子2026111713、有效batch8、micro2、dropout0、weight_decay0、前5步线性warmup后恒定学习率、clip1。每组上限150更新或15万目标token；固定32对实际约37.5遍。A/B只改变学习率；C增加rank并保持alpha/r=2，保留旧16列，新B列置零，逐模块校验初始有效增量不变。

Fresh AdamW per condition;identical stream,batch8,micro2,dropout0,weight_decay0,5-update warmup then constant LR,clip1. Cap150 updates/150k targets per condition. A/B vary only LR;C expands rank at alpha/r=2 while preserving the old delta,with random newA and zero newB. This is a fitting probe,not an exact repeat of the previous decay/dropout recipe.

在0/25/50/100/150步记录训练NLL曲线。最终以FP32对训练32及保留32生成译文。所有组都报告，不凭保留集重新挑选参数或追加预算；诊断adapter另存，不覆盖R0。 / Record curves and final matched greedy outputs for both sets. Report every condition;no held-out-driven tuning or budget extension;save separate diagnostic adapters.

## 4. 解释规则 / Interpretation

| Outcome | Supported direction | Not established |
| --- | --- | --- |
| Training fit already good,held-out poor | Prioritize generalization/coverage | Not proof of a unique data-only cause |
| B fits much better than A | Optimization strength affects fitting under matched budget | Not proof that higher LR gives broad held-out gains |
| C fits where B does not | Adapter capacity/subspace may be limiting | Not proof that the whole0.8B model has reached a ceiling |
| All short-budget conditions fit poorly | Continue implementation,optimization,data and representation audit | No absolute capacity-ceiling conclusion from this negative result |

语义判断使用G/P/B/U标准，记录每个候选，身份与分数尽量隐藏；同一AI助手、已知数值结果与熟悉数据限制盲法，不是独立母语认证。小集合记忆不能冒充泛化能力。 / Semantic review is AI-assisted with explicit limits;memorization is not generalization.

## 5. 预算、备份与完整性 / Budget and integrity

L4分配上限150分钟，主进程上限110分钟，预留备份和释放时间。每个完成条件保存adapter、AdamW、RNG、样本顺序和游标；持续镜像D盘并下载哈希校验快照。仅释放本轮自有GPU。未使用MetricX或DAPO。

Cap150 allocation minutes and110 worker minutes with backup reserve. Preserve adapter,optimizer,RNG and stream state;mirror and verify snapshots onD. Release only the owned runtime. NoMetricX orDAPO.

| Artifact | SHA256 |
| --- | --- |
| Source bundle | 65babb5c56dd93887a8828288bbe79c792daf4d14f04c5cae4d57e4d8aeece0a |
| Protocol | 066c84cb946dd7247f8aa13964bcf94315db5402774cf5a43e737bff159c6ff5 |

本地4项测试通过：rank扩展函数保持与新列梯度、固定曝光顺序、训练/保留隔离、拟合判断分支。源代码与固定输入在分配GPU前冻结。 / Four local checks passed;source and inputs frozen before allocation.

## 附录：全部固定文对 / All fixed pairs

<details><summary>train_seen32 00 OpenSubtitles18:683673 general</summary>

EN: -This is the last I'll see of him.

IS: -Ég sé hann aldrei aftur.

</details>

<details><summary>train_seen32 01 OpenSubtitles18:392505 general</summary>

EN: I'll prove it to you.

IS: Ég skal sanna það fyrir þér.

</details>

<details><summary>train_seen32 02 OpenSubtitles18:1418459 general</summary>

EN: I know you can do this.

IS: Ég veit að þið getið þetta.

</details>

<details><summary>train_seen32 03 OpenSubtitles18:76864 general</summary>

EN: And I'm not Dutch. I'm Swiss.

IS: Og ég er frá Sviss, ekki Hollandi.

</details>

<details><summary>train_seen32 04 OpenSubtitles18:59438 general</summary>

EN: No, it was here, this morning.

IS: Nei, hér, í morgun.

</details>

<details><summary>train_seen32 05 OpenSubtitles18:1527685 general</summary>

EN: But I think that is a great quality.

IS: En mér finnst það góður eiginleiki.

</details>

<details><summary>train_seen32 06 OpenSubtitles18:1254338 general</summary>

EN: Do you want to go grab a drink?

IS: Langar þig að fá þér drykk?

</details>

<details><summary>train_seen32 07 OpenSubtitles18:1384516 general</summary>

EN: - His name is Django.

IS: Hann heitir Django.

</details>

<details><summary>train_seen32 08 ParIce:987556 technical_short</summary>

EN: • The introductory part of Section 6.2 is replaced by the following:

IS: • Eftirfarandi komi í stað inngangsins í lið 6.2:

</details>

<details><summary>train_seen32 09 ParIce:700617 technical_short</summary>

EN: For the protection of non-target organisms, in particular honey bees:

IS: Til verndar lífvera utan markhóps, einkum býflugna:

</details>

<details><summary>train_seen32 10 ParIce:1603552 technical_short</summary>

EN: The fees are commensurate with the services provided.

IS: Þóknanirnar eru í réttu hlutfalli við veitta þjónustu.

</details>

<details><summary>train_seen32 11 ParIce:1537977 technical_short</summary>

EN: Part-time job is taken because:

IS: Ástæður þess að hlutastarf er tekið:

</details>

<details><summary>train_seen32 12 ParIce:1798779 technical_medium</summary>

EN: Each prolonged-release tablet contains 3.15 mg pramipexole (as 4.5 mg pramipexole dihydrochloride monohydrate).

IS: Hver forðatafla inniheldur 3,15 mg af pramipexóli (sem 4,5 mg af pramipexól tvíhýdróklóríð einhýdrati).

</details>

<details><summary>train_seen32 13 ParIce:1498640 technical_medium</summary>

EN: (3) the results of those inspections are relevant for the Commission to submit specific reports to the Standing Veterinary Committee based on Article 6(2) of Directive 98/58/EC;

IS: 3) Niðurstöður úr þessum skoðunum varða framkvæmdastjórnina, sem leggur sérstakar skýrslur fyrir fastanefndina um dýraheilbrigði, á grundvelli 2. mgr. 6. gr. tilskipunar 98/58/EB.

</details>

<details><summary>train_seen32 14 ParIce:1872893 technical_medium</summary>

EN: In pregnant rabbits, a maternal dose of 30 mg/kg that produced slight toxicity in the mothers showed a statistically significant increase in the incidence of litter malformations.

IS: Í ungafullum kanínum sýndu 30 mg/kg skammtar sem höfðu smávægileg skaðleg áhrif á móður marktæka aukningu á vansköpun afkvæma.

</details>

<details><summary>train_seen32 15 ParIce:508797 technical_medium</summary>

EN: • There are at present, no alternative methods validated by ECVAM, other than those listed in Annex V to Council Directive 67/548/EEC.

IS: • Eins og sakir standa hefur Evrópumiðstöð um fullgildingu nýrra aðferða ekki fullgilt aðrar aðferðir en þær sem eru skráðar í V. viðauka við tilskipun ráðsins 67/548/EBE.

</details>

<details><summary>train_seen32 16 ParIce:2014491 technical_medium</summary>

EN: The haemoglobin response varies between patients and may be impacted by iron stores and the presence of concurrent medical problems.

IS: Blóðrauðasvörun er mismunandi milli sjúklinga og kann að verða fyrir áhrifum af járnforða og sjúkdóma sem eru fyrir hendi á sama tíma.

</details>

<details><summary>train_seen32 17 ParIce:999143 technical_medium</summary>

EN: The Member States shall inform the Commission and the other Member States of the approval of such additional regions.

IS: Aðildarríkin skulu tilkynna framkvæmdastjórninni og hinum aðildarríkjunum um samþykki fyrir slíkum viðbótarsvæðum.

</details>

<details><summary>train_seen32 18 ParIce:1944560 technical_medium</summary>

EN: Patients with elevated liver enzymes (ALT/AST > 2 x ULN) or total bilirubin ≥ 1.5 x ULN were excluded in clinical trials.

IS: Sjúklingar með hækkuð lifrarensím (ALT/AST > 2 x eðlileg efri mörk) eða heildarbilirúbín ≥ 1,5 x eðlileg efri mörk, voru útilokaðir frá klínískum rannsóknum.

</details>

<details><summary>train_seen32 19 ParIce:1288360 technical_medium</summary>

EN: However, these products for which a certificate has been issued, duly completed and signed in accordance with national rules applicable before 31 October 2007 may be imported into the Community until 31 December 2007.

IS: Þó er heimilt að flytja þessar afurðir sem vottorð, sem eru útfyllt og undirrituð eins og vera ber í samræmi við landsreglur sem voru í gildi fyrir 31. október 2007, hafa verið gefin út fyrir, inn í Bandalagið til 31. desember 2007.“

</details>

<details><summary>train_seen32 20 ParIce:1999549 technical_medium</summary>

EN: Tell your doctor immediately if you experience rash and any of the other side effects of a hypersensitivity (allergic) reaction.

IS: Segðu lækninum strax frá því ef vart verður við útbrot og einhver önnur einkenni vegna ofnæmis.

</details>

<details><summary>train_seen32 21 ParIce:734865 technical_medium</summary>

EN: Coverage for the firms referred to in Article 3(1)(b)(iii) shall take one of the following forms:

IS: Varnir fyrirtækjanna, sem um getur í iii-lið b-liðar 1. mgr. 3. gr., gegn áhættu skulu vera á einhvern eftirfarandi hátt:

</details>

<details><summary>train_seen32 22 ParIce:114921 technical_long</summary>

EN: Whereas that mutual information procedure will not in any case replace the bilateral collaboration established by Article 7 of Directive 77/780/EEC; whereas the competent host Member State authorities can, without prejudice to their powers of control proper, continue either, in an emergency, on their own initiative or following the initiative of the competent home Member State authorities to verify that the activities of a credit institution established within their territories comply with the relevant laws and with the principles of sound administrative and accounting procedures and adequate internal control;

IS: Þessi gagnkvæmu upplýsingaskipti koma á engan hátt í stað þess tvíhliða samstarfs sem komið var á með 7. gr. tilskipunar 77/780/EBE. Lögbær yfirvöld í gistiríki geta, án þess að rýra valdsvið sitt, annaðhvort að eigin frumkvæði, ef mikið liggur við, eða að frumkvæði lögbærra yfirvalda í heimaríki, haldið áfram að hafa eftirlit með því að starfsemi lánastofnunar sem stofnuð hefur verið á yfirráðasvæði þeirra sé í samræmi við lög þar að lútandi og reglur um trausta stjórnun og bókhald og fullnægjandi innra eftirlit.

</details>

<details><summary>train_seen32 23 ParIce:476131 technical_long</summary>

EN: • For the purposes of this Article, ‘by electronic means shall mean that the information is sent initially and received at its destination by means of electronic equipment for the processing (including digital compression) and storage of data, and entirely transmitted, conveyed and received in a manner to be determined by Member States by wire, by radio, by optical means or by other electromagnetic means.

IS: • Að því er snertir þessa grein merkir hugtakið „með rafrænum hætti“ að upplýsingarnar eru upphaflega sendar og við þeim tekið á ákvörðunarstað með rafrænum búnaði fyrir vinnslu (þ.m.t. stafræn þjöppun) og geymslu gagna og eingöngu sendar, fluttar og mótteknar á þann hátt sem aðildarríkin ákveða, með rafþræði, þráðlaust, með ljóstæknilegum aðferðum eða með öðrum rafsegulaðferðum.

</details>

<details><summary>train_seen32 24 ParIce:1305459 technical_long</summary>

EN: • In ships of 60 metres in length and above, in addition there shall be provided, if the aggregate of the lengths of all passenger spaces and service spaces on the deck which carries such spaces is more than 80 metres, or, if there is more than one such deck, on the deck which has the largest aggregate of such lengths, two firefighters outfits and two sets of personal equipment for every 80 metres, or part thereof, of such aggregate of lengths.

IS: • Í skipum sem eru 60 metrar að lengd eða lengri skulu, ef heildarlengd allra farþegarýma og þjónusturýma á þilfarinu, sem slík rými eru á, er meira en 80 metrar, eða, ef slík þilför eru fleiri en eitt, þá á því þilfari þar sem þau ná mestri heildarlengd, auk þess vera tveir slökkvibúningar og tvö sett af persónuhlífum fyrir hverja 80 metra, eða hluta af þeim, af slíkri heildarlengd.

</details>

<details><summary>train_seen32 25 ParIce:1592226 technical_long</summary>

EN: • If points 2.4 and 2.5 apply and the further audit or check results are deemed not to be satisfactory in the opinion of the approval authority granting whole vehicle type-approval, the manufacturer shall ensure that conformity of production is restored as soon as possible by corrective actions to the satisfaction of the approval authority granting whole vehicle type-approval and to the satisfaction of the approval authority granting type-approval of the system, component or separate technical unit.

IS: • Ef ákvæði liða 2.4 og 2.5 eiga við og niðurstöður frekari úttektar eða skoðunar teljast ekki fullnægjandi að áliti viðurkenningaryfirvalds sem veitir heildargerðarviðurkenningu ökutækis skal framleiðandinn tryggja að samræmi framleiðslu sé komið á eins fljótt og auðið er með aðgerðum til úrbóta sem viðurkenningaryfirvaldið sem veitir heildargerðarviðurkenningu ökutækis og viðurkenningaryfirvaldið sem veitir gerðarviðurkenningu fyrir kerfi, íhlut eða aðskilda tæknieiningu telja fullnægjandi.

</details>

<details><summary>train_seen32 26 ParIce:1989245 technical_long</summary>

EN: Submission of the final clinical study report on a Post-Authorisation Safety (PAS) Observational Cohort Study to Quantify the Incidence and Comparative Safety of Selected Cardiovascular and Cerebrovascular Events in COPD Patients with Anoro compared with tiotropium (study 201038), according to a protocol agreed by the PRAC.

IS: Að leggja fram lokaskýrslu úr klínískri öryggisrannsókn (Post-Authorisation Safety (PAS) Observational Cohort Study to Quantify the Incidence and Comparative Safety of Selected Cardiovascular and Cerebrovascular Events) hjá sjúklingum með langvinna lungnateppu með Anoro samanborið við tíótrópíum (rannsókn 201038), samkvæmt rannsóknaráætlun sem samþykkt er af PRAC.

</details>

<details><summary>train_seen32 27 ParIce:312822 technical_long</summary>

EN: • a description of ordinary share transactions or potential ordinary share transactions, other than those accounted for in accordance with paragraph 64, that occur after the balance sheet date and that would have changed significantly the number of ordinary shares or potential ordinary shares outstanding at the end of the period if those transactions had occurred before the end of the reporting period.

IS: • lýsingu á viðskiptum með almenna hluti eða vænta hluti, aðra en þá sem gerð er grein fyrir í samræmi við 64. lið, sem fara fram eftir dagsetningu efnahagsreiknings og sem hefði breytt verulega fjölda almennra hluta eða væntra almennra hluta, sem eru virkir í lok tímabilsins, ef þessi viðskipti hefðu átt sér stað fyrir lok reikningsskilatímabilsins.

</details>

<details><summary>train_seen32 28 ParIce:593237 technical_long</summary>

EN: The purpose of this document is to give guidance on how the European Eco-management and Audit Scheme (EMAS) works for organisations operating with subsidiaries and sites located in several EU Member States and/or in third Countries, and to provide specific guidance to Member States, verifiers and organisations who can use it for registration purposes.

IS: Tilgangurinn með þessu skjali er að veita leiðbeiningar um hvernig evrópska umhverfisstjórnunarkerfið (EMAS) virkar fyrir fyrirtæki/stofnanir sem eru með dótturfyrirtæki og athafnasvæði í mörgum aðildarríkjum ESB og/eða í þriðju löndum, ásamt því að veita aðildarríkjunum, sannprófendum og fyrirtækjum/stofnunum sérstakar leiðbeiningar sem nota má við skráningu.

</details>

<details><summary>train_seen32 29 ParIce:1323460 technical_long</summary>

EN: • Manufacturers shall equip agricultural and forestry vehicles with systems, components and separate technical units affecting their braking performance that are designed, constructed and assembled so as to enable the vehicle in normal use and maintained according to the prescriptions of the manufacturer to comply with the detailed technical requirements and testing procedures laid down in Articles 4 to 17.

IS: • Framleiðendur skulu setja í ökutæki fyrir landbúnað og skógrækt kerfi, íhluti og aðskildar tæknieiningar sem hafa áhrif á hemlaafköst þeirra og eru hönnuð, smíðuð og sett saman þannig að ökutæki í eðlilegri notkun, sem viðhaldið er í samræmi við forskriftir framleiðanda, nái að uppfylla þær ítarlegu tæknilegu kröfur og prófunaraðferðir sem mælt er fyrir um í 4. til 17. gr.

</details>

<details><summary>train_seen32 30 ParIce:843684 technical_long</summary>

EN: 5. Before the general meeting referred to in paragraph 6, one or more independent experts appointed or approved, in accordance with the national provisions, by a judicial or administrative authority in the Member State to which the cooperative being converted into an SCE is subject shall certify mutatis mutandis that the rules of Article 22(1)(b) are respected.

IS: 5. Fyrir félagsfundinn, sem um getur í 6. mgr., skulu óháðir sérfræðingar, einn eða fleiri, sem hafa verið tilnefndir eða samþykktir af yfirvaldi á sviði dómgæslu eða stjórnsýslu í aðildarríkinu sem samvinnufélag, sem breyta á í evrópskt samvinnufélag, heyrir undir, votta, að breyttu breytanda, að reglurnar í b-lið 1. mgr. 22. gr. hafi verið virtar.

</details>

<details><summary>train_seen32 31 ParIce:63281 technical_long</summary>

EN: That certificate shall contain the name and address of the manufacturer, the conclusions of the examination, the aspects of the essential requirements covered by the examination, the conditions (if any) for its validity and the necessary data for identification of the approved type.

IS: Vottorðið skal innihalda nafn og heimilisfang framleiðandans, niðurstöður prófunarinnar, þá þætti í grunnkröfunum sem falla undir prófunina, skilyrði fyrir því að vottorðið sé gilt (ef einhver eru) og nauðsynlegar upplýsingar til að auðkenna samþykkta gerðareintakið.

</details>

<details><summary>heldout32 00 ParIce21:opensubtitles:dev:2119 general</summary>

EN: I just came from the liquor store.

IS: Ég var að koma úr vínbúðinni.

</details>

<details><summary>heldout32 01 ParIce21:opensubtitles:dev:543 general</summary>

EN: Me, a freshman, going with the most amazing girl at Sky High.

IS: Ég, businn, fer með glæsilegustu stúlkunni í Sky High.

</details>

<details><summary>heldout32 02 ParIce21:opensubtitles:dev:2151 general</summary>

EN: can I call you back?

IS: Má ég hringja til baka?

</details>

<details><summary>heldout32 03 ParIce21:opensubtitles:dev:2435 general</summary>

EN: Why, uttering the very name of Sparta or Leonidas will be punishable by death.

IS: Það verður dauðasök að minnast orði á Spörtu eða Leonídas.

</details>

<details><summary>heldout32 04 ParIce21:opensubtitles:dev:969 general</summary>

EN: We've got all these extra kids running around.

IS: Það eru allir þessir aukakrakkar á hlaupum.

</details>

<details><summary>heldout32 05 ParIce21:opensubtitles:dev:1368 general</summary>

EN: You want the long or short version?

IS: Viltu löngu eða stuttu söguna?

</details>

<details><summary>heldout32 06 ParIce21:opensubtitles:dev:1573 general</summary>

EN: To me, anything over 500 words is a novel.

IS: Mér finnst allt sem er lengra en 500 orð vera skáldsaga.

</details>

<details><summary>heldout32 07 ParIce21:opensubtitles:dev:3120 general</summary>

EN: I don't know what went wrong!

IS: Ég veit ekki hvað fór úrskeiðis.

</details>

<details><summary>heldout32 08 ParIce21:eea:dev:616 technical_short</summary>

EN: Annual days of vocational training (optional).

IS: Árlegur fjöldi daga nýttur til starfsnáms (valkvætt).

</details>

<details><summary>heldout32 09 ParIce21:ema:dev:2348 technical_short</summary>

EN: What is Memantine LEK used for

IS: Við hverju er Memantine LEK notað

</details>

<details><summary>heldout32 10 ParIce21:eso:dev:635 technical_short</summary>

EN: Complex Organic Molecules Discovered in Infant Star System

IS: Flókin lífræn efnasambönd finnast í ungu sólkerfi

</details>

<details><summary>heldout32 11 ParIce21:norden:dev:717 technical_short</summary>

EN: Cyber attacks and disinformation continue to be major threats.

IS: Enn sem fyrr stafar mikil ógn af netárásum og villandi upplýsingum.

</details>

<details><summary>heldout32 12 ParIce21:eso:dev:804 technical_medium</summary>

EN: “We uncovered 574 new massive galaxies - the largest sample of such hidden galaxies in the early Universe ever assembled,” explains Karina Caputi.

IS: „Við fundum 574 áður óséðar efnismiklar vetrarbrautir - stærsta safn slíkra vetrarbrauta sem fundist hefur svo snemma í sögu alheimsins,“ segir Karina Caputi.

</details>

<details><summary>heldout32 13 ParIce21:eea:dev:373 technical_medium</summary>

EN: Inspections for compliance with GLP principles may take place in any test facility generating health or environmental safety data for regulatory purposes.

IS: Skoðun til að kanna hvort meginreglum um góðar starfsvenjur við rannsóknir er fylgt getur farið fram í öllum prófunarstöðvum sem afla gagna um öryggi heilbrigðis og umhverfis samkvæmt gildandi reglum.

</details>

<details><summary>heldout32 14 ParIce21:eea:dev:2030 technical_medium</summary>

EN: For the proper functioning of the internal market and in order to facilitate cross-border trade within the Community it is essential that the charges for cross-border payments in euro are the same as for corresponding payments within a Member State.

IS: Til að starfsemi innri markaðarins sé með eðlilegum hætti og til að greiða fyrir viðskiptum yfir landamæri innan Bandalagsins er mikilvægt að gjöld vegna greiðslna yfir landamæri í evrum séu þau sömu og fyrir samsvarandi greiðslur innan aðildarríkis.

</details>

<details><summary>heldout32 15 ParIce21:norden:dev:25 technical_medium</summary>

EN: We also need to increase support for the UN and others bodies striving to create better conditions for refugees in areas bordering Syria,” Þórhallsson explains.

IS: Við verðum líka að auka stuðning við Sameinuðu þjóðirnar og aðrar stofnanir sem vinna að því að bæta lífsskilyrði flóttamanna á grannsvæðum Sýrlands,“ segir Höskuldur Þórhallsson.

</details>

<details><summary>heldout32 16 ParIce21:eso:dev:861 technical_medium</summary>

EN: As well as taking images of the object they also split the light up into its component colours to obtain information about the motions as well as the temperature and chemical composition of the central object.

IS: Samhliða því að taka myndir af fyrirbærinu, klufu þeir einnig ljós þess í liti sína til að fá upplýsingar um hreyfingu sem og hitastig og efnasamsetningu fyrirbærisins í miðjunni.

</details>

<details><summary>heldout32 17 ParIce21:eea:dev:2130 technical_medium</summary>

EN: The extent to which the data subject will have an effective choice will depend on the availability of reliable and recognised systems of mediation.

IS: Skráði aðilinn á kost á því að velja að því marki sem áreiðanlegt og viðurkennt kerfi sáttaumleitana er tiltækt.

</details>

<details><summary>heldout32 18 ParIce21:norden:dev:207 technical_medium</summary>

EN: It is an important step towards ensuring that Nordic startups can get the best possibilities for access and success in USA.

IS: Um er að ræða mikilvægt skref fyrir norræn sprotafyrirtæki sem fá hér einstakt tækifæri til að hasla sér völl og ná árangri í Bandaríkjunum.

</details>

<details><summary>heldout32 19 ParIce21:eea:dev:35 technical_medium</summary>

EN: An anaerobic degradation study must be reported unless it can be justified that exposure of the plant protection products containing the active substance to anaerobic conditions is unlikely to occur.

IS: Gera skal grein fyrir rannsókn á loftfirrtu niðurbroti, nema unnt sé að sýna fram á að ólíklegt sé að plöntuvarnarefnin, sem innihalda virka efnið, verði notuð við loftfirrt skilyrði.

</details>

<details><summary>heldout32 20 ParIce21:ema:dev:1057 technical_medium</summary>

EN: 14 ml of Perjeta concentrate should be withdrawn from the vial and diluted into a 250 ml PVC or non-PVC polyolefin infusion bag of sodium chloride 9 mg/ml (0.9%) solution for infusion.

IS: Draga á 14 ml af Perjeta þykkni úr hettuglasinu og þynna það í 250 ml innrennslispoka úr PVC eða pólýólefíni án PVC, sem inniheldur 9 mg/ml (0,9%) lausn af natríumklóríði til innrennslis.

</details>

<details><summary>heldout32 21 ParIce21:ema:dev:1351 technical_medium</summary>

EN: If the number of platelet (a type of blood cell that helps to clot blood) has decreased.

IS: Ef blóðflögum (tegund blóðfrumna sem tekur þátt í blóðstorknun) hefur fækkað.

</details>

<details><summary>heldout32 22 ParIce21:eea:dev:372 technical_long</summary>

EN: Further clarification of many of the points in this part of the Annex may be obtained by referring to the OECD consensus documents on GLP (on, e.g., the role and responsibilities of the study director).

IS: Frekari útskýringar á ýmsum atriðum í þessum hluta viðaukans er að finna í sammælisskjölum Efnahags- og framfarastofnunarinnar (OECD consensus documents) um góðar starfsvenjur við rannsóknir (t.d. um hlutverk og ábyrgðarsvið rannsóknarstjóra).

</details>

<details><summary>heldout32 23 ParIce21:eea:dev:937 technical_long</summary>

EN: Inspection and sampling scheme for the two-year control period which precedes achievement of approved status for VHS and/or IHN in zones and farms in non-approved zones with an officially recognised documented history of freedom from these diseases

IS: Skoðun og sýnatökuáætlun, sem fer fram á tveggja ára eftirlitstímabili áður en viðurkennd staða fæst að því er varðar veirublæðingu og/eða iðradrep, á svæðum og eldisstöðvum á svæði sem ekki er viðurkennt en skjalfest er að veirublæðing og/eða iðradrep hafi ekki komið þar upp áður

</details>

<details><summary>heldout32 24 ParIce21:eso:dev:471 technical_long</summary>

EN: It either grew by assembling the rocks that form the solid core and then slowly accumulated gas from the environment to form the heavy atmosphere, or started forming from a gaseous clump that arose from gravitational instabilities in the disc.” explains Anne-Marie Lagrange, another team member.

IS: Annað hvort óx hún með því að draga til sín berg sem myndaði fastan kjarna sem sópaði síðan að sér gas úr umhverfinu og myndaði þannig þykkan lofthjúp, eða hún hóf að myndast úr gasklumpi sem varð til vegna þyngdaróstöðugleika í skífunni,“ segir Anne-Marie Lagrange, meðlimur í rannsóknarteyminu.

</details>

<details><summary>heldout32 25 ParIce21:eso:dev:277 technical_long</summary>

EN: A new image of the centre of the distinctive galaxy Centaurus A, made with the Atacama Large Millimeter/submillimeter Array (ALMA), shows how the new observatory allows astronomers to see through the opaque dust lanes that obscure the galaxys centre, with unprecedented quality.

IS: Ný mynd Atacama Large Millimeter/submillimeter Telescope af miðju vetrarbrautarinnar Centaurus A, sýnir vel hvernig þessi nýi sjónauki gerir stjörnufræðingum kleift að sjá í gegnum ryk, sem alla jafna er ógegnsætt og hylur miðju vetrarbrautarinnar, í meiri smáatriðum en nokkru sinni fyrr.

</details>

<details><summary>heldout32 26 ParIce21:ema:dev:1873 technical_long</summary>

EN: In repeat dose studies in rodents, effects in a variety of tissues (bone, teeth, nail beds, reproductive organs, haematological tissues, kidney and pancreas) appear related to the pharmacology of VEGFR inhibition and/or disruption of VEGF signalling pathways with most effects occurring at plasma exposure levels below those observed in the clinic.

IS: Í rannsóknum með endurteknum skömmtum hjá nagdýrum virðast áhrif í ýmsum vefjum (beinum, tönnum, naglabeði, æxlunarfærum, blóðvefjum, nýrum og brisi) tengjast lyfjafræðilegum áhrifum VEGFR- hindrunar og/eða rofi VEGF-merkjaferla þar sem flest áhrifin koma fram við útsetningu í plasma sem var lægri en við klínískar aðstæður.

</details>

<details><summary>heldout32 27 ParIce21:ema:dev:2509 technical_long</summary>

EN: In a randomised, double-blind correction study (n = 358) comparing once every two week and once monthly dosing schedules in patients with CRF not on dialysis, darbepoetin alfa once monthly dosing was non-inferior to once every two week dosing for correcting anaemia.

IS: Í slembaðri, tvíblindri leiðréttingarrannsókn (n = 358) þar sem borin var saman gjöf lyfsins einu sinni á tveggja vikna fresti og gjöf lyfsins einu sinni í mánuði hjá sjúklingum með langvarandi nýrnabilun sem ekki voru í skilun, gaf darbepoetin alfa gefið einu sinni í mánuði ekki lakari niðurstöður en þegar það var gefið á tveggja vikna fresti til leiðréttingar á blóðleysi.

</details>

<details><summary>heldout32 28 ParIce21:eso:dev:801 technical_long</summary>

EN: It is further complicated by the fact that the brightest and easiest galaxies to observe - the most massive galaxies in the Universe - are rarer the further astronomers peer into the Universes past, whilst the more numerous less bright galaxies are even more difficult to find.

IS: Verkið verður enn erfiðara þegar sú staðreynd er höfð í huga að björtustu og auðfundnustu vetrarbrautirnar - efnismestu vetrarbrautirnar í alheiminum - verða sjaldséðari því lengra sem stjörnufræðingar skyggnast aftur í fortíð alheimsins. Á sama tíma verður jafnvel erfiðara að finna smærri og daufari vetrarbrautir, sem jafnframt eru mun algengari.

</details>

<details><summary>heldout32 29 ParIce21:eea:dev:803 technical_long</summary>

EN: In order to reinforce the added value of Community action, the Commission, in cooperation with the Member States, should ensure, at all levels, the coherence and complementarity of actions implemented in the framework of this Decision and other relevant Community policies, instruments and actions, in particular those concerning a coordinated employment strategy, social policy, the European Social Fund, education, vocational training and youth.

IS: Í því skyni að auka ávinning af aðgerðum bandalagsins ber framkvæmdastjórninni að tryggja, í samstarfi við aðildarríkin, að aðgerðir á öllum stigum innan ramma þessarar ákvörðunar séu í réttu samhengi við og til fyllingar öðrum viðeigandi stefnumálum , gerningum og aðgerðum bandalagsins, einkum þeim sem varða samræmda stefnu í atvinnumálum , félagsmálastefnu, Félagsmálasjóð Evrópu, menntun, starfsnám og æskulýðsmál.

</details>

<details><summary>heldout32 30 ParIce21:eea:dev:1729 technical_long</summary>

EN: The carrier presented a series of corrective actions which have been proposed to the competent authorities of the above mentioned Member States, as well as a plan of corrective actions designed to address in a systematic way deficiencies which affected various areas within the carrier responsibility.

IS: Flugrekandinn setti fram nokkrar aðgerðir til úrbóta, sem hafa verið lagðar til við lögbær yfirvöld framangreindra aðildarríkja, ásamt áætlun um aðgerðir til úrbóta sem er sniðin að því að taka á kerfisbundinn hátt á annmörkum sem hafa áhrif á ýmis svið sem eru á ábyrgð flugrekandans.

</details>

<details><summary>heldout32 31 ParIce21:eea:dev:1354 technical_long</summary>

EN: If new testing is necessary, and in the case of experimental problems in the screening test (for example, inhibition due to toxicity of test substance), repeat testing by using a low dosage of surfactant and monitor degradation by 14C measurements or chemical analyses.

IS: Ef nauðsynlegt reynist að láta nýjar prófanir fara fram, og ef upp kemur vandi í framkvæmd skimunarprófunarinnar (t.d. hömlun vegna eiturhrifa prófunarefnis), skal endurtaka prófunina með minni skammti yfirborðsvirka efnisins og fylgjast með niðurbrotinu með geislakolsmælingu (14C-mælingu) eða efnagreiningu.

</details>
