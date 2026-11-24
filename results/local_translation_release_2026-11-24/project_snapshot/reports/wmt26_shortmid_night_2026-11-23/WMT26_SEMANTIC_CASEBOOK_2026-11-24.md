# WMT26逐例语义核查 / WMT26 source-fidelity casebook

2026-11-24 · Europe/Berlin

固定源单元24条，三个模型共72对，去重后盲化判断52对。标注先封存再查看模型映射。实际覆盖news/social/speech；软件域没有符合本次短中句条件的源单元，未在看完结果后补选。格式及计数单元单独统计，全部原始抽样仍保留。

24 frozen source units, 72 model/source pairs and 52 deduplicated blind judgments. Labels were sealed before identities were opened. Coverage is news/social/speech; no software unit met this short-medium audit's eligibility. No post-output replacements were added. Report formatting/counter units separately while retaining the full original selection.

**P**:核心意思保留，允许语法不完美 / core meaning retained; imperfect grammar allowed. **F**:可指出实质语义错误 / identifiable material error. **U**:保留不确定 / uncertainty retained. **同一助手核查，不是独立母语专家认证，不是总体正确率，不用于选checkpoint。 / Same-assistant audit, not independent native certification or a population correctness rate; not used for checkpoint selection.**

```json
{
  "UTC": "2026-11-24T02:27:51.989383+00:00",
  "source_units": 24,
  "unique_blind_pairs": 52,
  "arm_source_pairs": 72,
  "counts": {
    "all_preselected": {
      "R0": {
        "n": 24,
        "P": 9,
        "F": 13,
        "U": 2
      },
      "oldDAPO120": {
        "n": 24,
        "P": 9,
        "F": 11,
        "U": 4
      },
      "shortmidDAPO": {
        "n": 24,
        "P": 10,
        "F": 11,
        "U": 3
      }
    },
    "substantive_only": {
      "R0": {
        "n": 19,
        "P": 4,
        "F": 13,
        "U": 2
      },
      "oldDAPO120": {
        "n": 19,
        "P": 4,
        "F": 11,
        "U": 4
      },
      "shortmidDAPO": {
        "n": 19,
        "P": 5,
        "F": 11,
        "U": 3
      }
    },
    "formatting_only": {
      "R0": {
        "n": 5,
        "P": 5,
        "F": 0,
        "U": 0
      },
      "oldDAPO120": {
        "n": 5,
        "P": 5,
        "F": 0,
        "U": 0
      },
      "shortmidDAPO": {
        "n": 5,
        "P": 5,
        "F": 0,
        "U": 0
      }
    }
  },
  "transitions": {
    "all_preselected": {
      "oldDAPO120": {
        "P→P": 9,
        "F→F": 11,
        "U→U": 2,
        "F→U": 2
      },
      "shortmidDAPO": {
        "P→P": 9,
        "F→F": 11,
        "U→U": 2,
        "F→P": 1,
        "F→U": 1
      }
    },
    "substantive_only": {
      "oldDAPO120": {
        "P→P": 4,
        "F→F": 11,
        "U→U": 2,
        "F→U": 2
      },
      "shortmidDAPO": {
        "P→P": 4,
        "F→F": 11,
        "U→U": 2,
        "F→P": 1,
        "F→U": 1
      }
    },
    "formatting_only": {
      "oldDAPO120": {
        "P→P": 5
      },
      "shortmidDAPO": {
        "P→P": 5
      }
    }
  },
  "availability": {
    "news": {
      "short": {
        "available": 188,
        "selected": 4
      },
      "medium": {
        "available": 184,
        "selected": 4
      }
    },
    "social": {
      "short": {
        "available": 378,
        "selected": 4
      },
      "medium": {
        "available": 300,
        "selected": 4
      }
    },
    "software": {
      "short": {
        "available": 0,
        "selected": 0
      },
      "medium": {
        "available": 0,
        "selected": 0
      }
    },
    "speech": {
      "short": {
        "available": 1291,
        "selected": 4
      },
      "medium": {
        "available": 128,
        "selected": 4
      }
    }
  },
  "same_assistant_not_independent_or_native_certification": true,
  "not_population_correctness_rate": true,
  "source_only_fidelity_not_sentence_reference_alignment": true,
  "not_used_to_select_checkpoint": true,
  "software_not_covered_by_shortmedium_audit": true
}
```

## 1. news / 1 words / format only

Source ID: `8b93b20af87ca2180ccd:0003`

> &lt;/p&gt;


### R0 · P · B029

&lt;/p&gt;

格式标记原样保留 / Exact formatting-only preservation.


### oldDAPO120 · P · B029

&lt;/p&gt;

格式标记原样保留 / Exact formatting-only preservation.


### shortmidDAPO · P · B029

&lt;/p&gt;

格式标记原样保留 / Exact formatting-only preservation.


## 2. news / 1 words / format only

Source ID: `beb232c57e34326b7ba4:0016`

> &lt;/p&gt;


### R0 · P · B011

&lt;/p&gt;

格式标记原样保留 / Exact formatting-only preservation.


### oldDAPO120 · P · B011

&lt;/p&gt;

格式标记原样保留 / Exact formatting-only preservation.


### shortmidDAPO · P · B011

&lt;/p&gt;

格式标记原样保留 / Exact formatting-only preservation.


## 3. news / 1 words / format only

Source ID: `24edd9601e2912238379:0021`

> &lt;/p&gt;


### R0 · P · B031

&lt;/p&gt;

格式标记原样保留 / Exact formatting-only preservation.


### oldDAPO120 · P · B031

&lt;/p&gt;

格式标记原样保留 / Exact formatting-only preservation.


### shortmidDAPO · P · B031

&lt;/p&gt;

格式标记原样保留 / Exact formatting-only preservation.


## 4. news / 3 words / substantive text

Source ID: `88c219e9391e17a463bd:0022`

> Thanks for following.


### R0 · P · B035

Takk fyrir að fylgja.

感谢关注的含义保留 / Thanks for following is retained.


### oldDAPO120 · P · B035

Takk fyrir að fylgja.

感谢关注的含义保留 / Thanks for following is retained.


### shortmidDAPO · P · B035

Takk fyrir að fylgja.

感谢关注的含义保留 / Thanks for following is retained.


## 5. social / 8 words / substantive text

Source ID: `871d9fbcb62faa3a90e1:0017`

> &lt;p&gt;Crown fully pieced, with cloth covered.button at peak.


### R0 · F · B002

Crown fullað, klætt með klæði, með töflu á húðinni.

纽扣和顶部变成皮肤上的其他物体 / The covered button at the peak becomes an unrelated object on skin.


### oldDAPO120 · F · B024

Crown fullt samsett, klætt með klóti. Tangur á húðinni.

顶部覆布纽扣变为皮肤上的物体 / The covered button at the peak becomes an unrelated object on skin.


### shortmidDAPO · F · B043

Crown fullt tekið upp, með klæðu umlát. Knapp á húðinni.

顶部纽扣的位置被译到皮肤上，服装描述错误 / The button location becomes skin; the garment description is wrong.


## 6. social / 7 words / substantive text

Source ID: `bd68cbf019a831f60f05:0013`

> &lt;p&gt;Although, things don&#x27;t feel the same today.


### R0 · P · B050

Þó ekki séu hlutirnir líða sömu í dag.

今天感觉不同的核心含义保留 / The central meaning that things feel different today is retained.


### oldDAPO120 · P · B012

Þó ekki séu hlutirnir líða sama í dag.

虽然语法生硬，今天感觉不同的核心意思保留 / Despite rough grammar, the central meaning that things feel different today is retained.


### shortmidDAPO · P · B050

Þó ekki séu hlutirnir líða sömu í dag.

今天感觉不同的核心含义保留 / The central meaning that things feel different today is retained.


## 7. social / 1 words / format only

Source ID: `8b74f8c50b104cfd74e0:0022`

> &lt;/p&gt;


### R0 · P · B008

&lt;/p&gt;

格式标记原样保留，非自然语言翻译 / Exact formatting-only preservation, not natural-language translation.


### oldDAPO120 · P · B008

&lt;/p&gt;

格式标记原样保留，非自然语言翻译 / Exact formatting-only preservation, not natural-language translation.


### shortmidDAPO · P · B008

&lt;/p&gt;

格式标记原样保留，非自然语言翻译 / Exact formatting-only preservation, not natural-language translation.


## 8. social / 1 words / format only

Source ID: `5504f5bcf58e8d055226:0022`

> &lt;br&gt;5/n&lt;/p&gt;


### R0 · P · B019

&lt;br&gt;5/n&lt;/p&gt;

格式与序号原样保留，非自然语言翻译 / Exact markup/counter preservation, not natural-language translation.


### oldDAPO120 · P · B019

&lt;br&gt;5/n&lt;/p&gt;

格式与序号原样保留，非自然语言翻译 / Exact markup/counter preservation, not natural-language translation.


### shortmidDAPO · P · B019

&lt;br&gt;5/n&lt;/p&gt;

格式与序号原样保留，非自然语言翻译 / Exact markup/counter preservation, not natural-language translation.


## 9. speech / 2 words / substantive text

Source ID: `56f0ec42d453e0588959:0004`

> User manual.


### R0 · P · B015

Notendahandbók.

User manual正确译为Notendahandbók / User manual is faithfully rendered as Notendahandbók.


### oldDAPO120 · P · B015

Notendahandbók.

User manual正确译为Notendahandbók / User manual is faithfully rendered as Notendahandbók.


### shortmidDAPO · P · B015

Notendahandbók.

User manual正确译为Notendahandbók / User manual is faithfully rendered as Notendahandbók.


## 10. speech / 6 words / substantive text

Source ID: `6db03fc6f3a322fd7864:0000`

> I am standing in a volcano.


### R0 · F · B018

Ég er á standi í köklu.

火山没有被译为火山，位置意义错误 / Volcano is not translated as a volcano; the location is wrong.


### oldDAPO120 · F · B025

Ég er á standi í könnu.

火山被替换为kanna相关的容器词 / Volcano is replaced by a container-related kanna form.


### shortmidDAPO · F · B049

Ég er á standi í könnnum.

火山位置变为容器相关词，关键地点错误 / The volcano location becomes a container-related form.


## 11. speech / 11 words / substantive text

Source ID: `068c0dfbae0802f1de29:0003`

> I just can&#x27;t wait to to do this to you now.


### R0 · P · B041

Ég get ekki bíðað að gera þetta við þig núna.

迫不及待现在做这件事的意思保留，语法不完美 / Cannot wait to do this now is retained despite imperfect grammar.


### oldDAPO120 · P · B046

Ég get bara ekki bíðað að gera þetta við þig núna.

迫不及待现在做这件事的大意保留 / Cannot wait to do this now is retained.


### shortmidDAPO · P · B046

Ég get bara ekki bíðað að gera þetta við þig núna.

迫不及待现在做这件事的大意保留 / Cannot wait to do this now is retained.


## 12. speech / 12 words / substantive text

Source ID: `68c19f62778c8188007d:0006`

> I thought it would be best if I slipped out this way.


### R0 · U · B017

Ég hélt að það væri best ef ég flýti út þannig.

离开的核心可辨，但悄悄溜出与匆忙离开的差别不确定 / Leaving is recognizable, but slipped out versus hurried out remains uncertain.


### oldDAPO120 · U · B042

Ég hélt að það væri best ef ég slíp út þannig.

slíp这一表达不能确认保留悄悄溜出的含义 / The form slíp does not allow confident certification of slipped out.


### shortmidDAPO · U · B017

Ég hélt að það væri best ef ég flýti út þannig.

离开的核心可辨，但悄悄溜出与匆忙离开的差别不确定 / Leaving is recognizable, but slipped out versus hurried out remains uncertain.


## 13. news / 21 words / substantive text

Source ID: `9dbad5e0894379a5e96c:0019`

> &lt;p&gt;Gary Cooper made the role entirely his own, his integrity comparable only to Gregory Peck&#x27;s Atticus in To Kill a Mockingbird.


### R0 · F · B001

Gary Cooper náði hlutverki sínu að fullu sér sinni, hreintist honum aðeins sá heilbrigði og Gregory Peck í Atticus í To Kill a Mockingbird.

演员的完整性及与Atticus的比较被破坏 / Integrity and the comparison with Atticus are garbled.


### oldDAPO120 · F · B044

Gary Cooper náði hlutverki sínu að fullu sér sinni, hreint sér aðeins saman við Atticus í Atticus í To Kill a Mockingbird sem Gregory Peck gaf sér.

integrity比较关系损坏并出现Atticus重复 / The integrity comparison is garbled, with duplicated Atticus.


### shortmidDAPO · F · B040

Gary Cooper náði þáttinn í fullu sér sinn, hreintu hreinni hann aðeins í Gregory Peck hins Atticus í To Kill a Mockingbird.

integrity及角色比较的核心关系丢失 / Integrity and the role-comparison relationship are lost.


## 14. news / 39 words / substantive text

Source ID: `c1ba3b117b18185801f1:0040`

> &lt;p&gt;Hudson-Odoi took the tie into extra time in fantastic fashion, taking a touch on his chest and lofting a perfect volley over Okonkwo, but Wrexham were not to be denied their first top-flight FA Cup scalp for 26 years.


### R0 · F · B005

Hudson-Odoi tók víxliðið í viðbótartíma á frábæru hátt, tók tapp á brjóstina og hældi fullkomlega hólfu yfir Okonkwo, en Wrexham fengu ekki að hafa fengið fyrsta húð í FA kupsálinum í 26 árum.

足球动作、比赛结果及26年首次击败顶级球队的意义破坏 / Football actions and the first top-flight scalp in26 years are materially garbled.


### oldDAPO120 · F · B047

Hudson-Odoi tók týpu í viðbótartíma í frábæru hátt, tók tappa á brjóstina sína og hælt nákvæm tilvika hættu yfir Okonkwo, en Wrexham fengu ekki að missa fyrsta húð á FA kupsálinum í 26 árum.

足球动作、首次战绩与比赛结果表述破坏 / Football actions, the first scalp and result are materially garbled.


### shortmidDAPO · F · B022

Hudson-Odoi tók víxlan í viðbótartíma í frábæru hátt, tók tapp á brjóstina sína og hældi fullkominni hólf yfir Okonkwo, en Wrexham fengu ekki að missa fyrsta húð þeirra í FA-kupanum í 26 árum.

关键足球动作和首次战绩含义损坏 / Key football actions and the first top-flight scalp are materially garbled.


## 15. news / 31 words / substantive text

Source ID: `fda9531e50cdd1bb46e7:0005`

> &lt;p&gt;Robin Roefs was Sunderland&#x27;s hero as Everton&#x27;s FA Cup hopes came to a premature end once again after three woeful penalties in a shootout saw the Black Cats reach round four.


### R0 · F · B010

Robin Roefs var hringið Sunderland og endaði hamingja Everton í FA-kupsálinum á ný eftir þrjár skræfðar fyrirbæri í skrárinni þegar Svarta kettillin náðu fjórða kúpu.

英雄、点球和晋级轮次等关键比赛信息损坏 / Hero, penalties and progression to round four are materially garbled.


### oldDAPO120 · F · B014

Robin Roefs var hringi Sunderland og FA hóp Erlingarins létst á nýju leið eftir þrjár skræfum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andleg

严重无关重复且未完成关键比赛内容 / Severe irrelevant repetition and missing match information.


### shortmidDAPO · F · B036

Robin Roefs var hringið Sunderland og endurtekið hamingjusöngur Everton á fimmtípu ógildandi hátt á eftir þrjár skræfðar áreikningar í skrárásinni og Black Cats náðu fjórða kringlunni.

英雄、点球及比赛晋级信息损坏 / Hero, penalties and match progression are materially garbled.


## 16. news / 24 words / substantive text

Source ID: `6c52413a733e6513e96b:0012`

> &lt;p&gt;After two rounds of the FBD League, the top two progress to next week&#x27;s final, with Galway facing the winner of tomorrow&#x27;s Roscommon-Mayo tie.


### R0 · F · B039

Eftir tvö kringlunir í FBD-hópnum fá tveir stjörnustöðvar síðasta viku í endaáttunni, að því er Galway í viðræðuna við siglinginn í Roscommon-Mayo-áttunni á morgun.

下周变成上周，前两名和对阵信息也破坏 / Next week becomes last week, with additional ranking/opponent distortion.


### oldDAPO120 · F · B023

Eftir tvö lotu í FBD-hópnum fá tveir fyrsta stjörnurnar næsta viku í endaáttunni, að Galway í viðmiðunarmálið við siglinginn í Roscommon-Mayo- samanburðið á morgun.

晋级规则和胜者对阵关系被破坏 / Progression rules and the winner/opponent relation are garbled.


### shortmidDAPO · F · B013

Eftir tvö lotur í FBD-hópnum fá tveir fyrsta stjörnurnar næsta viku í endaáttunni, að Galway í viðræðuna með vinum sínum á morgunnar í Roscommon-Mayo.

前两名进决赛及对阵胜者的关系被改坏 / The top-two progression and opponent/winner relationships are garbled.


## 17. social / 18 words / substantive text

Source ID: `5d4ebce6bd448f4b42f2:0007`

> I&#x27;m FTTP/XGS-PON so I think just stuck with the 5x... not an insurmountable problem, just a little annoying.


### R0 · F · B006

Ég er FTTP/XGS-PON svo ég held að vera bara stökkvinn með 5x... ekki óhjákvæm vandamál, bara lítil þrálát.

insurmountable被错译，关键评价改变 / Insurmountable is mistranslated, changing the central assessment.


### oldDAPO120 · F · B003

Ég er FTTP/XGS-PON svo ég held að vera bara stökkvinn með 5x... ekki óhjákvæm vandamál, bara lítil skammvæn.

无法克服的问题与卡在5x的含义未保留 / The stuck/insurmountable-problem meanings are not retained.


### shortmidDAPO · F · B027

Ég er FTTP/XGS-PON svo ég held að vera bara stökkvinn með 5x... ekki óhjákvæm ámil, bara lítil óþægindi.

卡住及并非无法克服的问题未正确表达 / Being stuck and not having an insurmountable problem are mistranslated.


## 18. social / 22 words / substantive text

Source ID: `f658cc9d8d816e94c9c1:0005`

> It is too far away from any of my cameras to tell exactly what he was doing, but movement suggests sniffing around.


### R0 · F · B051

Það er of langt frá öllum myndavélum mínum til að vita nákvæmlega hvað hann var að gera en hreyfingar benda til sníðs.

sniffing的嗅闻行为变成sníðs相关的其他意义 / The olfactory action sniffing is not retained in sní­ðs.


### oldDAPO120 · U · B052

Það er of langt frá öllum myndavélum mínum til að vita nákvæmlega hvað hann var að gera en hreyfingar benda til sníkka.

末尾非标准词无法确认是嗅闻，其他观察内容大致保留 / The final nonstandard word cannot be certified as sniffing; the observation context is mostly retained.


### shortmidDAPO · U · B052

Það er of langt frá öllum myndavélum mínum til að vita nákvæmlega hvað hann var að gera en hreyfingar benda til sníkka.

末尾非标准词无法确认是嗅闻，其他观察内容大致保留 / The final nonstandard word cannot be certified as sniffing; the observation context is mostly retained.


## 19. social / 20 words / substantive text

Source ID: `98dc59f74f8a2087167f:0011`

> &lt;br&gt;Had a similar problem when working on my house where literally every datum you might think of using was wrong.


### R0 · U · B038

Hefði sérhverju svipaða vandamál þegar ég var að vinna heima mínu þar sem allar upplýsingarnar sem ég hugsaði að nota voru allar rangar.

施工datum及起始时态表达不确定，不能认证语义完整 / Construction datum and the opening tense are uncertain; complete fidelity cannot be certified.


### oldDAPO120 · U · B020

Hafði svipaða vandamál þegar ég var að vinna heima mínu þar sem allar upplýsingarnar sem ég hugsaði að nota voru allar rangar.

房屋施工中datum是否为测量基准存在歧义，候选只说信息 / Datum may mean a construction reference; the candidate says information, so technical fidelity is uncertain.


### shortmidDAPO · U · B020

Hafði svipaða vandamál þegar ég var að vinna heima mínu þar sem allar upplýsingarnar sem ég hugsaði að nota voru allar rangar.

房屋施工中datum是否为测量基准存在歧义，候选只说信息 / Datum may mean a construction reference; the candidate says information, so technical fidelity is uncertain.


## 20. social / 36 words / substantive text

Source ID: `1ba5402f736862a1747f:0002`

> &lt;br&gt;Assuming she took it from the veins around the elbow, theres a chance she went too deep and hit the back wall of the vein, and an underlying tendon then bruised it on the way out.


### R0 · F · B045

Hún tók það úr bláæðum í kringum eldið, þá er líkur á að hún hafi komið of djúp og hafi hett á bakverri bláæðarinnar og þá hefur vefjaþrengið það í gegnum ferðina.

假设语气丢失，肘部和肌腱受伤信息错误 / The assumption is asserted as fact, with elbow/tendon injury distortion.


### oldDAPO120 · F · B037

Hafi hún tekið það úr bláæðum í kringum eldið, er möguleiki á að hún hafi komið of djúp og hafi hett á bakverri bláæðarinnar og þá hefur tænur þá sáttstífla það á leiðinni út.

肘部、血管后壁及肌腱损伤信息破坏 / Elbow, vein-wall and tendon-injury details are materially garbled.


### shortmidDAPO · F · B034

Því að hún tók það úr bláæðinum í kringum eldið, er líkur á að hún hafi komið of djúp og hafi hett í bakverri bláæðarinnar og þá hefur vefið þar í þrengt það á leiðinni út.

肘部与肌腱受伤的解剖和因果信息破坏 / Elbow, tendon and injury/causation details are materially garbled.


## 21. speech / 14 words / substantive text

Source ID: `0b6ccedbcf9a7f1e8059:0000`

> She talked about how impossible it is to be a woman in today&#x27;s society.


### R0 · F · B048

Hún talaði um hversu óhjálegt er að vera konu í dagins félags.

impossible的中心含义未正确表达 / The central meaning of impossible is mistranslated.


### oldDAPO120 · F · B021

Hún talaði um hversu óhjálegt er að vera kona í dagins samfélags.

impossible的中心含义未正确表达 / The central meaning of impossible is mistranslated.


### shortmidDAPO · F · B004

Hún talaði um hversu óhjálegt er að vera kona í dagins félags.

中心谓语impossible没有得到正确表达 / The central predicate impossible is mistranslated.


## 22. speech / 17 words / substantive text

Source ID: `f5e3d55fe3de929d6cac:0000`

> Jade, if you want to get back together with Beck, then why don&#x27;t you just tell him?


### R0 · F · B032

Jade, ef þú vilt koma aftur saman með Beck, þá hvers vegna skaltu hann það ekki?

为什么不告诉他的关键动作谓语缺失 / The key predicate tell him is missing.


### oldDAPO120 · U · B009

Jade, ef þú vilt ná aftur saman með Beck, þá hvers vegna skaltu hann þá ekki segja?

复合与告诉对方的大意可辨，但代词和谓语结构不足以确认 / Reunion is recognizable, but the pronoun/predicate structure prevents confident fidelity certification.


### shortmidDAPO · P · B026

Jade, ef þú vilt fara aftur með Beck, þá hvers vegna skaltu þá ekki bara segja honum það?

与Beck复合并直接告诉他的核心含义保留 / Getting back together with Beck and telling him are retained.


## 23. speech / 18 words / substantive text

Source ID: `1ef44f7d70897cb5c9f2:0005`

> It&#x27;s one thing to fill his head with nonsense about the North Pole, but dial S for Santa.


### R0 · F · B016

Það er eitt og sama að fylla höfuð hans með óvísu um Norðurhvelið, en hringja S fyrir Santa.

北极被译为北半球，另有Santa表达错误 / North Pole becomes Northern Hemisphere, with additional Santa-related distortion.


### oldDAPO120 · F · B030

Það er eitt svið að fylla höfuð hans með óvísu um Norðurhvelið, en síðan hringdu S fyrir Jólafíkn.

北极与Santa均被误译 / Both North Pole and Santa are mistranslated.


### shortmidDAPO · F · B028

Það er eitt og sama að fylla höfuð hans með óvísu um Norðurhvelið, en hringja í S fyrir Jólafönginn.

北极变成北半球，Santa也被破坏 / North Pole becomes Northern Hemisphere, and Santa is also distorted.


## 24. speech / 19 words / substantive text

Source ID: `27f428d50b218fe48c52:0010`

> You don&#x27;t think they&#x27;d let me in the kitchen if they knew I was organizing the strike, do you?


### R0 · F · B007

Heldurðu að þeir myndu láta mig koma inn í eldhúsin ef þeir vissu að ég væri að skipuleggja stríðina, er það?

罢工被译为战争相关词stríð / Strike is rendered with the war-related word stríð.


### oldDAPO120 · F · B007

Heldurðu að þeir myndu láta mig koma inn í eldhúsin ef þeir vissu að ég væri að skipuleggja stríðina, er það?

罢工被译为战争相关词stríð / Strike is rendered with the war-related word stríð.


### shortmidDAPO · F · B033

Heldur þú að þeir myndu láta mig koma inn í eldhúsin ef þeir vissu að ég væri að skipuleggja stríðina, er það nokkuð?

罢工被译为战争相关词stríð / Strike is rendered with the war-related word stríð.
