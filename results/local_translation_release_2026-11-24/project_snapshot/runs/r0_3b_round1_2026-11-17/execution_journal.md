# FINAL — OWNED GPU RELEASED

# First3B round complete — 2026-11-17

The first 3B training and diagnostic round is complete, but it has not produced a reliable broad R0 that replaces the old 0.8B checkpoint. Preserve it as an experimental candidate without promotion or formal DAPO efficiency comparisons.

Report: D:\deep learning project\reports\r0_3b_round1_2026-11-17\R0_3B_ROUND1_RESULTS_2026-11-17.html

GPU released; observed usage4.5975CU.


Historical notes below are stale.

# Latest15:46UTC — TRAINING COMPLETE926updates999931targets, FP32 GREEDY96/128, STREAM REVIEW ACTIVE

Selectedt1000000;dev64weighted36.47643,general35.54763,short49.24024,medium33.22675,long38.29560,NLL1.58604,techNLL1.58541,failures0. OldSFT200same64weighted39.77750,gen46.78002,long32.66917. Trainingfinished~15:32UTC;nowfinalFP32generation96/128 at15:45. Main14065foreground&68848observerhealthy. Originaldeadline16:22:53UTC unchanged.

D/review/judgements.jsonl has23cardsgraded inavailabilityorder already. No aggregate/rankingcomputed. DO NOT repeatgradedcards. Use review.py live thenavailable thencardsIDs. Append via b3_append_ratings.py fromW/b3_rating_batch.json;all288labelsneedlockbeforeanalysis. Currentgreedymostlymajorlexical/semanticdefects,notqualifiedconclusionyetuntilallG8. GradeGallowminorgrammaronly,notmajorroles/numbers/clauses;13greedyGbutawkwardregulatorywording,othersrecordednotes. SingleAIreviewnotnativecertification.

CheapCPUrewardcomparatorsregistered beforeselectedoutputs;analyzerappendsplanandactualmixture/exposurecounts;CountergroupIDauditfixpreservesmultiplicity. W/b3_history_context.py generatedD/training_history_context.json:oldV3continuedpriorSFTandadded1.400474m+SFT200.200770m,olderwarmstartunknown;new3BfreshLoRA1m,differenttokenizer,no equalexposure causalclaim. Report updatedallthis.

IMPORTANT remainingGPU sequence:waitmaincomplete and14065returns;EXEC `b3_cli.py exec work/b3_aux_foreground_remote.py foreground` (NOTcontrol90sectimeout). AuxalreadyCPUdownloadedMetricXwaitingforpolicyexit,scorermoduleabsoluteimportsFIXEDbeforeexecution;runactual8mincappedauditandpurefinalrepack. Finaltransferrequiresflagtrue. Then b3_safe.py b3_transfer.py final, b3_safe.py b3_verify_before_release.py, b3_cli.py release, b3_safe.py b3_accounting.py. Allfourhelpersready;finalpreverifychecks57oldunchangedandfullstates. Don'treleasebeforedurablecurrentexportsha.

Finish288labels+reviewlock;Dvenv b3_analyze;Anaconda b3_plots&view;manualW/b3_interpretation.json REQUIRED;buildreport;make_repro+Dvenvreplay;HTMLQA160details3images&view;finalize. UserexpectsfullfirstresultsBerlin17:00–17:15(~16:00–16:15UTC);communicatehonestlyifQAneedsmore. DoNOTpromoteonchrFalone;noautomaticmoreGPUtraining. Allold57preserved,newweightsD. Noagents.

# Latest15:00UTC — 609k TRAINED,500k QUALITY, CHEAP REWARD COMPARATOR REGISTERED

B565updates609284targets at14:59UTC,203targettok/s,healthy. 500kdev64 weighted32.83128,general32.31881,short45.12324,medium29.25009,long34.45022,NLL1.79648,failures2. OldSFT200same64 weighted39.77750,long32.66917:longimprovedbutoverallstillbelowold;noqualificationyet. Userinformed.

Registered CPU-only exploratory rawchrF++/normalized+samegates/length ranking beforeselectedoutputs atD/review/cheap_reward_comparator_plan.json. No additionalGPU/training/rewardselection. b3_analyze.py computes old/new comparatorrankings ONLYafterall288lockedlabels;report explains limits. Plan includedinCPUreplayfixtures automatically.

IMPORTANT aftermaincompletion:run `b3_cli.py exec work/b3_aux_foreground_remote.py foreground` (NOT control) becausecontroltimeout90s canexpirebefore8min audit. Reuseforegroundkernel onlyAFTERmainforegroundfinished. This observesactualauxwork,repacksonly,no newtraining. Allprevioussourcehashesunchanged.

Added b3_append_ratings.py tovalidate&append W/b3_rating_batch.json toD/review/judgements.jsonl;no metricsprinted. No selectedoutputs orlabels yet. OriginalGPUdeadline16:22:53UTC unchanged. Finish/release/analysis/report/QA asbelow.

# Latest14:37UTC — ~420k, next500k quality; STREAM REVIEW READY

Bactual390updates419773targets at14:37UTC,~202.6targets/s,stillhealthy. t0250000FULLsnapshotDverified332603398B. Firstdev64quality:initialweighted20.06658→250k28.67410;gen18.1929→29.8035,short37.9112,med26.8152,long27.1779,NLL2.08347/tech2.10562,fail1. Thisis SFTimprovementvsraw3B,NOTyetold0.8BsuperiorityorDAPOqualification. UserinformedandtimeforecastBerlin16:30–16:40trainingend,17:00–17:15fullfirstresults (~16:00–16:15UTC). OriginalGPUabsolute16:22:53UTC deadlineunchanged.

IMPORTANT CPUreview now supports STREAMING tofinishwithin3h:cards/keyprecreatedEMPTYbeforeselectedoutputs(64fixedcards,no labels). DO NOT use `make` (cardsalreadyexists). Use:
- Python313 work/b3_review.py live : refresh completed actualselectedgreedy/G8fromD/live_mirror (orfinalexportwhenpresent),assertpreviousavailablecardsunchanged
- ... available : listunreviewedcompletecardIDs
- ... cards 1,4,7 : displayarbitraryavailablecards (noMetricXscores)
- appendjudgementsJSONLtoD/review/judgements.jsonl withcard,ratings(GPBU onecharforgreedy/eightforG8),note_zh,note_en.
MayreviewinAVAILABILITYORDER duringfinalGPUinference. All32greedy(allT7fixedheldIDs)andall32G8/all256candidatesmusteventuallyreview. `lock` requires64uniquecards/all288labels,preservesentryorderlogandSORTS solelycardIDbeforefinalhashlock. No semantic/rewardaggregatesbeforelock. `live`afterfinaltransfercrosschecksactualunchangedcards;analyzerassertsreviewhypothesesmatchfinalexport. Singlemodelpartialblindingknown,numericdevresultsseen,AIreviewnotnativecertified. D/review/streaming_process_plan.json registeredbeforeselectedoutputs. ThisoverlapsCPUreviewwithGPUgeneration;donotwaituntilGPUreleaseforALLlabelsifcanreviewlive.

SuppauditreadyCPUdownloadsdonewaitingforpolicyexit. MustaftermaincompletionexecW/b3_aux_foreground_remote.py control (sourcealreadyuploadedROOT) towaitactualauditandPURErepack. Finalb3_transferassertsexport_info.supplemental_reward_audit_includedtrue;DO NOTtransferfirstmainexportbeforethis. Source/reward_model_fileshashesarchived. Read-onlymT5scoresONLYafterpolicyprocessclosed,cap8min/min20reserve,registeredbeforeselectedoutputs,noSFT/modeselectionchanges. Scorerreadoutsnotonreviewcards.

Code b3_analyze.py,b3_build_report.py,b3_finalize.py updatedforreward_supplement/rankingstatus andtworuntimeattempts. FinalformalDAPO_readyfalsebecauseoldglobalcalibfailurestillnotrepaired;translationactorpromotionmanualbasedallactualevidence. ManualW/b3_interpretation.json STILLNOTCREATED. Needsource/directreportIaftergradingall288. Syntaxcompileallhelperspassedbeforemostrecentharmlesspresentationpatch;cancompilelaterasneeded. Primarysource34immutable.

E/supplemental_control_bundle.zip+matchingmanifest(savedzipnames),E/data_provenance/T6_candidate_pool_before_3B_selection.jsonl(20.85MB SHA13393429...) nowD;fullsourcepoolprovenancepreservedwithoutchangingactual27krows/1mstream. Local3Bbase6.18GBofflineD. W/b3_report_lib.py finalbannerfixed3BR0; staticEnglishparagraphspacingpolishedONLYpresentation,notrawoutputs.

Currentactive sessions:14065realforeground,68848read-onlyIOPubobserver,75226immutablewatch,58793live mirror,10185rollingwatch. 8896supplementlaunchDONE0. OldAallarchivedD/attempt_A,fullinitandbaselinesreusedwithchecks;Bfrom0sameseed/order butnotbitwise. AccountingTOTALA+Balreadyfixed;firstAknown28updates29762targets lowerbound. PrefixRNGall4equal,lossmaxdiff.01014/norm.11462causeunisolated.

Finalremaining:finishSFT/selectedFP32greedy128/G8,STREAMlabelswhilegenerating;runauxforeground/repack,transferall&preverify/release/account;finishlabel lock;Dvenvanalyze;Anacondaplots&view;manualI;buildreportMDHTML;CPUreplayverified;HTMLQA160details/3images+view;finalize&clearansweruserwithtime/cost/actorqualification/checkpointlinks. NOAGENTS. No newGPUrun/autoextension.

# Latest — IMPORTANT SUPPLEMENTAL RANK AUDIT, WAIT FOR FINAL REPACK

Additive read-only MetricX ranking diagnostic registered BEFORE selectedSFT/G8 outputs (after initial model outputs partlyseen). User informed incommentary. E/reward_audit_plan.json has timestamp,sourceSHA,same oldT6 scorer/pinned GoogleMetricX-v2p6revision51e875... and MT5tokenizer63fc... . No SFT/modelchoice changes,no rewardmode/weight tuning. Original mainprogramMetricX_calls=0 remains true;roundadds up to256FP32forwards/512candidate readouts. Cannoterase known failed globalcontrols;not T=1actualDAPOvalidation.

Supplementworker ROOT/b3_reward_audit.py LAUNCHED already,session8896 launchDONE0. It CPUdownloaded scorer/tokenizer andstatus waiting_for_SFT_process_exit verified (unix1794924969). No GPU useuntil mainpolicyprocessfullyexits. Atleast20minremainingrequired,max8min scoring,originaldeadlineunchanged. Scoresall32selected G8banks reference+QE,source2batch,classcopiedexactT6Scorer to ROOT/b3_scorer.py. Allnumericalgrades lockedbefore rankingaggregate;doNOTprint rawrewardswhilelabeling.

CRITICAL after SFT mainjob completes:its first export DOES NOT necessarilyincludecompleteaudit. Run:
Python313 work/b3_cli.py exec work/b3_aux_foreground_remote.py control
This monitorsactualaudit,hashesscorer/tokenizerfiles,records4sourcehashes,andPURELYREPACKS originalworkerpackagingtail. Then export_info.json gets supplemental_reward_audit_included=true and reward_repack_done.json. b3_aux_foreground_remote.py ALREADY UPLOADED toROOT. MUST WAIT FOR THIS REPACK BEFOREFINALTRANSFER. b3_transfer.py finalnowassertsflagtrue. No newpolicytraining/generationinrepack. Ifaudit skipped/partialduebudget,itstillrepackageshonestly;analyzerdoesnotaggregatepartialranking. DoNOTreleaseuntildurablefinalcurrentSHAverified.

Codeupdates: b3_analyze.py nowattachesMetricX toselectedG8andcomputesrankpairG>P>B,activeG top1,rawref/QE/fullfrozenreference reward witholdtextgate&256softlengthpenalty. Adds result.reward_supplement. OldSFTscorescomefromlockedT6rawdata;currentafter-scorerdoesnotrescoreoldbank. b3_build_report.py updatedseparatecallcounts,supplementtable&limitations. b3_verify_before_release.py verifyssupplementsource manifest andcomplete32ifdone. Needupdatefinalizer rewardstatusfieldtoacknowledgerankingexecutedbutglobalcalibnotpassed. No extraactor/DPexperiment.

Current14:17ish SFTquartermillionREACHED; selection_t0250000decode24/64 observed. Pendingreadonlypollsession38089 mayreturnmetricswhenready. Foreground14065 andobserver68848bothactualchannelsconnected,continue. First realdevqualityavailableafter64outputs,doNOTinferqualityfromtrainloss. Last knownB~233updates250ktokens;updatesloopbriefpauseforregistereddev64. Current3Brawbaselinefull128chrF20.9566;oldSFT20036.03695. 3B firstdev0weighted20.0666,gen18.1929. Usergoalreliableactor,notnecessarilynewgenrawstronger.

Otherremainingworkunchanged:finish1m(max100minloop)andgreedy128/G8, runauxforeground/repack, transfer/verify/release/accountTOTALA+B,288semanticlabels,CPUanalysis/plots/manualI/report/replayHTMLQA(finaldetails160,images3)/finalize. Current source34 frozen unchanged; recoverymanifest+rollinghelper hash+auxmanifest separatelyaudited. Noagents,no autoextensionbeyond16:22:53UTC.

# Latest14:04UTC — B CONNECTED, >100k TRAINED, FULL RECOVERY57 ON D

Actual B95updates102316targets by14:04UTC;~202targettok/s. First250kqualityexpected~14:17UTC,1m~15:25UTC with intermediateevals. Originaldeadline16:22:53UTC remains. Foreground14065 and read-only observer68848 bothCONNECTED printing actualprogress,not lost. No need rerun or reallocate. Immutablewatch75226,live58793 active.

Added CPU-onlyrolling archival helper ROOT/b3_rolling_backup_worker.py,launchedvia b3_launch_rolling_remote.py,sourceSHA recordedrolling_backup_pid.json;doesNOTchange frozen numericalsource. It archives first5min recoverythen~10min intervals toseparaterolling_snapshot_index.json,no sharedindexrace. Localwatchsession10185(b3_rolling_watch.py) transfers eachtagviaextendedb3_transfer regex acceptingrecovery_###### andACKs. Firsttrainedrecovery_000057 FULLstate archivedD/snapshots/recovery_000057,60988targets,332782449B,SHA95cd39519d19683b67e7585645ee592eaa5dba76b259469417ed6ee5eb281722,7filesverified. Mainb3workerincludesexternalACKs forrollingtoo. SnapshotdiskD~830GBfree;C~61GBfree,newbigartifactsallD.

RestartprefixauditD/restart_prefix_audit.json:28Aknownupdates29762targets;matchinggrouporder/tokenbudgets/initialadapterSHA;initialRNGPython/NumPy/CPU/CUDAequal;maxmeanlossdiff.0101405,gradnormdiff.114624. ExactcauseofnumericdifferenceNOTisolated,no bitwiseweightreplayclaim,unmirroredAfinalworkunknown. B iscurrentonecontinuousrun;A prefixnotadditionaltrainingonBweights. Accountbothattempts.

Verified historicalLOCALsft_round1/best(step250):original50-case/max96logchrF++30.0028837(step20030.3031),NOTestablished50points. Addedquickreference&aliasJSONintransitionreportdir;doNOTstateuser'sremembered50equalscount50 asfact,onlyactualcount/scoreread. Priorapprox50cannotbemappedtoexactprotocolhere. OldR0SELECTneeds_more_sft=truehistoricaloverabsoluteinterpretation;newdocclarifiesnotcurrentcausalproof. CurrentoldR0all128chrF34.5671/BLEU15.7005;SFT20036.03695/16.03149.

ExtraCPUtoolsalreadywritten;manualinterpretation/semanticlabelsNOTdone. Needfinishthisauthorizedrun,notstopafterlaunch. Noagents. Nextmeaningfuleventquartermilliondevquality. Source/recov/rollinghelperhashverificationreadybeforeGPUrelease. Finalreporttextcorrectedtwoattempts/prefixvariance/rollingbackup. Notebookreplaysoriginalunbrokenplan;recoverysupplementE/recovery_bundle.zip+tools.

# LATEST — ATTEMPT B ACTIVE, A LOST (13:56UTC)

A assignment disappeared;status0 confirmed13:47–13:48UTC. Exact cause unknown. Durable t0 snapshot and full baseline128/selection64 retained,mirrored28updates. A artifacts copied D/attempt_A (immutable archive). No trained A weights beyond0 recovered. B is a restart from verified t0,same seed/order,NOT an independent seed,not last-update resume.

Current CLI private path=work/colab_cli_private/r0_3b_round1_2026-11-17_attempt_B;old path retains A ownership. New L4 allocated~13:51UTC;ORIGINAL deadline1794932573.643 unchanged(16:22:53UTC). Do NOT allocate again or autoextend.

Recovery: E/recovery_bundle.zip(27675247B,5chunks),E/recovery_bundle_info.json, E/recovery_stage. Frozen original34 files unchanged. Actual wrapper b3_recover_train.py imports frozen b3_train and overrides only initial adapter load,initial128decode reuse with2 full-token anchor checks,and selection0 reuse with recomputed NLL. Original update loop unchanged. b3_recovery_worker.py dispatches wrapper and archives. Additional recovery_manifest.json records all helper/cache hashes. Initial adapter SHA033dd30456eb2352fbd04ee98e89a13e547195375aa0546ced755be62297bc74. B anchor parity passed,actualinitial_baseline_reused_verified output observed.

B foreground handshake VERIFIED_FOREGROUND beforelongjob. Sessions:
-14065 actualforeground supervisor:CONNECTED andprinting actualprogress,not lost;keepactive
-68848 read-only observer of same real supervisor IOPub,session_id=None(fresh client);ATTACHED true,doesNOT execute anycode or fakeactivity
-75226 B snapshotwatcher ACTIVE
-58793 B live mirror ACTIVE
Old A sessions68061/15777 may finishfailed;ignore theirstale data. Old66089WSfailed. Currentsupervisor launchesrecoveryworker once.

b3_accounting.py UPDATED to include globalbalance from Ainitial271.6436531111 and both attempts; A durationboundedlastsuccess1794923044.191..firstabsentupper1794923303; Bexactrelease. Need prefixaudit once≥28Bupdates:get authoritative remote updates,compare groupIDs/loss/norm with A28records;keepcostknownworklowerbound since Aunobserved finalupdatesunknown.

Additional32pair referenceauditD/additional_data_audit:31no clearmajordefect,1context-dependent omission;no numericalinputchange. Local3Bbase fullysavedD/models/qwen2.5-3b-instruct,6183463416B;manifest present. TransitionHTML QApassed,firstpagevisuallyreadable. Notebook8cells generatedE/R0_3B_ROUND1_2026-11-17.ipynb (replays original unbrokenprotocol,notrecovery);needdocumentrecovery separately.

CPU tools ready W:b3_review.py(planregistered;make/show/lock afterfinal;288labels),b3_analyze.py,b3_plots.py,b3_build_report.py,b3_make_repro.py,b3_html_qa.py,b3_verify_before_release.py,b3_finalize.py. Manual b3_interpretation.json NOT created;dependsactualresults. AllWb3scriptscompiled before recovery;compileagain asneeded. ReporttextUPDATED for2attempts (doNOTsay no reallocation). Pre-releasechecksnowverifyrecovery_manifest too. Need possiblyupdatefinalizer toincludeinterruptionledger. Stillcomplete GPUwork/backup/release thenCPUreview/replay/reportQA/finalize. No newexperiments beyondthisround.

Historical notes below are stale for runtime status:

# Active 3B round — 2026-11-17

User authorized switching to3B,first archive causes/checkpoints,Colab workflow,first round target3hours. No agents.

Roots:
- E=D:/deep learning project/experiments/r0_3b_round1_2026-11-17
- S=E/source (34 frozen files;do not edit once executing)
- D=D:/deep learning project/runs/r0_3b_round1_2026-11-17
- Rtransition=D:/deep learning project/reports/r0_3b_transition_2026-11-17
- Results report planned=D:/deep learning project/reports/r0_3b_round1_2026-11-17
- Remote=/content/b3_project
- Private CLI state=work/colab_cli_private/r0_3b_round1_2026-11-17 (do NOT print/copy credentials/endpoints)

Model Qwen/Qwen2.5-3B-Instruct,3.0859B,revision aa8e72537993ba99e69dfaafa59ed015b17504d1. Different generation/tokenizer from oldQwen3.5;not parameter-only causal ablation. Public ungated research model. Icelandic quality not guaranteed by model card.

Data:27743 unique pairs,29625 exposures,max2 perpair,999931 target tokens,895573 unique target tokens. Mixture40%general,5%technicalshort,25%medium,30%long. Full cleaned T6 candidate pool38640 after31semantic exclusions,re-encoded using3B tokenizer,max1024/target384,no truncation. Heuristic source/reference exclusions,not full document separation. Old dev/eval/G8 are reused diagnostics,NOT untouchedtest.

Recipe:fresh LoRA rank16/alpha32,all q/k/v/o/gate/up/down,dropout.05,AdamW1e-4,5%warmup cosine to20%,wd.01,clip1,batch32 micro4fallback2/1. Frozen BF16 base,FP32 adapter. Final generation matchedFP32 fromBF16-roundedbase,TF32off,max320. Selection0/250k/500k/1m existingdev64,weights=.4/.05/.25/.3,general floor−1.5/failures≤baseline+2;initialfallback. Full128 before/aftergreedy,selectedG8same32T6sources withsame seed/T.7/top_p1/top_k0. No MetricX orDAPO thisround.

4 local meaningful tests passed7.29sec. Sourcebundle9631702B,SHA62cf6ee5eb125dfc3b984374ecf44ffbe4f581cfebbcaee5299c507de4f40573 (2chunks);E/bundle_info.json. Numericalsource frozen beforeGPU.

L4 allocated unix1794921773.6432676 (~13:22:53UTC);absolute deadline1794932573.6432676 (~16:22:53UTC),180min;trainloop100min max and stops≥40min beforedeadline. Initial account271.6436531111127CU. Torch2.14.1+cu130,L4VRAM23659151360. Initial setup/foreground WS streaming lost,contents checks confirm same runtime actually running;DO NOT allocate/restart. Setup completeunix1794921923.068 (~13:25:23UTC),actual jobpid1251 launched1926,baselineFP32progress1951. No numerical failure observed.

Sessions:
-74190 upload/bootstrap,source verified/setup actually started despite WSerror;likely finished
-66089 foreground supervisor stream ended1 dueWS but remote code actually continues;do NOT rerun worker
-68061 snapshot watcher active (b3_safe.py b3_snapshot_watch.py),writes full immutablecheckpointsD/snapshots and ACKs
-15777 live mirror active (b3_safe.py b3_live_mirror.py),D/live_mirror
-9576 readonlypoll active/latest;no actualerror
-31809 preparationDONE0;97609freezeDONE0

CLI scripts work/b3_cli.py,status/exec/upload/download/release. Python313=C:/Users/andre/AppData/Local/Programs/Python/Python313/python.exe. Wrap network helpers with work/b3_safe.py. Always UTF8. Dwrites/network require exec require_escalated;alreadyuserauthorized. Client uses prior official OAuth,no relogin needed. release requires work/b3_verified_export.json withtwo durablefilehashes matching currentremoteexport. b3_transfer.py snapshot TAG supports t6/7digits orstopped_step;final stores allbigfilesD (notC). b3_accounting.py afterrelease.

Important currentcode:worker bundles initialadapter+frozeninputs+run,skipsmodels/cache,verifiedold snapshots referenced externally,keepsfull laststateandselectedadapter. Periodicrecovery every5min,immutable evalsnapshots. Training cannot silently restart. Error partial archive still exported;mustinspect worker_exit/error before claiming completed. Snapshot watcher10800sec. Keep meaningful userupdates≈60sec,do not stop afterlaunch.

0.8B preservation:57canonical checkpointpaths scanned with readable safetensorheaders/SHA;alloriginalinplace. Rtransition/TRANSITION_AND_CHECKPOINTS_2026-11-17.md/html plus CHECKPOINTS_08B_2026-11-17.json/csv complete. PrimaryoldR0=nll_adapter shaebb4575f...;SFT200sha89c874...;SFT400sha32dd79... . Tinyfit probes explicitlynotstrongerR0. No cause-attributionrankproved;workingprioritycandidates,MetricXalsoflawed. T6G8tech3/24G,21nogood;long0/10. SelectedSFTcovered3allrankG but63/247discordantcross-tierpairs. R5matchedFP32chrFdelta−1.367CI[−3.742,+.862]. T7tinyfitallexact32,butheldout35.41→26.20/24.64. No absolute0.8Bceiling.

Remaining:monitor untilfinal,backupallstates+finalZIP,verify/releaseownedL4,account. CPUanalyze greedyvsinitialandoldR0/SFT200,pairedsourceCIs,referencequalityexclusions,reviewallnewG8candidates and selectedgreedy keysemantics,locklabelsbeforeaggregate;doNOTauto-promote. FullMDHTMLandrawstep/resultsD,notebookreplay,QA,finalclearwhether3BfirstR0usable;actualtime/cost. No moreGPUbeyondregisteredround orautobudgetextension.
