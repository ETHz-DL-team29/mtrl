# WMT26 source-fidelity casebook

2026-11-24 · Europe/Berlin

24 frozen source units, 72 model/source pairs and 52 deduplicated blind judgments. Labels were sealed before identities were opened. Coverage is news/social/speech; no software unit met this short-medium audit's eligibility. No post-output replacements were added. Report formatting/counter units separately while retaining the full original selection.

**P**: core meaning retained; imperfect grammar allowed. **F**: identifiable material semantic error. **U**: uncertainty retained. **Same-assistant audit, not independent native-expert certification or a population correctness estimate; not used for checkpoint selection.**

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

Exact formatting-only preservation.


### oldDAPO120 · P · B029

&lt;/p&gt;

Exact formatting-only preservation.


### shortmidDAPO · P · B029

&lt;/p&gt;

Exact formatting-only preservation.


## 2. news / 1 words / format only

Source ID: `beb232c57e34326b7ba4:0016`

> &lt;/p&gt;


### R0 · P · B011

&lt;/p&gt;

Exact formatting-only preservation.


### oldDAPO120 · P · B011

&lt;/p&gt;

Exact formatting-only preservation.


### shortmidDAPO · P · B011

&lt;/p&gt;

Exact formatting-only preservation.


## 3. news / 1 words / format only

Source ID: `24edd9601e2912238379:0021`

> &lt;/p&gt;


### R0 · P · B031

&lt;/p&gt;

Exact formatting-only preservation.


### oldDAPO120 · P · B031

&lt;/p&gt;

Exact formatting-only preservation.


### shortmidDAPO · P · B031

&lt;/p&gt;

Exact formatting-only preservation.


## 4. news / 3 words / substantive text

Source ID: `88c219e9391e17a463bd:0022`

> Thanks for following.


### R0 · P · B035

Takk fyrir að fylgja.

Thanks for following is retained.


### oldDAPO120 · P · B035

Takk fyrir að fylgja.

Thanks for following is retained.


### shortmidDAPO · P · B035

Takk fyrir að fylgja.

Thanks for following is retained.


## 5. social / 8 words / substantive text

Source ID: `871d9fbcb62faa3a90e1:0017`

> &lt;p&gt;Crown fully pieced, with cloth covered.button at peak.


### R0 · F · B002

Crown fullað, klætt með klæði, með töflu á húðinni.

The covered button at the peak becomes an unrelated object on skin.


### oldDAPO120 · F · B024

Crown fullt samsett, klætt með klóti. Tangur á húðinni.

The covered button at the peak becomes an unrelated object on skin.


### shortmidDAPO · F · B043

Crown fullt tekið upp, með klæðu umlát. Knapp á húðinni.

The button location becomes skin; the garment description is wrong.


## 6. social / 7 words / substantive text

Source ID: `bd68cbf019a831f60f05:0013`

> &lt;p&gt;Although, things don&#x27;t feel the same today.


### R0 · P · B050

Þó ekki séu hlutirnir líða sömu í dag.

The central meaning that things feel different today is retained.


### oldDAPO120 · P · B012

Þó ekki séu hlutirnir líða sama í dag.

Despite rough grammar, the central meaning that things feel different today is retained.


### shortmidDAPO · P · B050

Þó ekki séu hlutirnir líða sömu í dag.

The central meaning that things feel different today is retained.


## 7. social / 1 words / format only

Source ID: `8b74f8c50b104cfd74e0:0022`

> &lt;/p&gt;


### R0 · P · B008

&lt;/p&gt;

Exact formatting-only preservation, not natural-language translation.


### oldDAPO120 · P · B008

&lt;/p&gt;

Exact formatting-only preservation, not natural-language translation.


### shortmidDAPO · P · B008

&lt;/p&gt;

Exact formatting-only preservation, not natural-language translation.


## 8. social / 1 words / format only

Source ID: `5504f5bcf58e8d055226:0022`

> &lt;br&gt;5/n&lt;/p&gt;


### R0 · P · B019

&lt;br&gt;5/n&lt;/p&gt;

Exact markup/counter preservation, not natural-language translation.


### oldDAPO120 · P · B019

&lt;br&gt;5/n&lt;/p&gt;

Exact markup/counter preservation, not natural-language translation.


### shortmidDAPO · P · B019

&lt;br&gt;5/n&lt;/p&gt;

Exact markup/counter preservation, not natural-language translation.


## 9. speech / 2 words / substantive text

Source ID: `56f0ec42d453e0588959:0004`

> User manual.


### R0 · P · B015

Notendahandbók.

User manual is faithfully rendered as Notendahandbók.


### oldDAPO120 · P · B015

Notendahandbók.

User manual is faithfully rendered as Notendahandbók.


### shortmidDAPO · P · B015

Notendahandbók.

User manual is faithfully rendered as Notendahandbók.


## 10. speech / 6 words / substantive text

Source ID: `6db03fc6f3a322fd7864:0000`

> I am standing in a volcano.


### R0 · F · B018

Ég er á standi í köklu.

Volcano is not translated as a volcano; the location is wrong.


### oldDAPO120 · F · B025

Ég er á standi í könnu.

Volcano is replaced by a container-related kanna form.


### shortmidDAPO · F · B049

Ég er á standi í könnnum.

The volcano location becomes a container-related form.


## 11. speech / 11 words / substantive text

Source ID: `068c0dfbae0802f1de29:0003`

> I just can&#x27;t wait to to do this to you now.


### R0 · P · B041

Ég get ekki bíðað að gera þetta við þig núna.

Cannot wait to do this now is retained despite imperfect grammar.


### oldDAPO120 · P · B046

Ég get bara ekki bíðað að gera þetta við þig núna.

Cannot wait to do this now is retained.


### shortmidDAPO · P · B046

Ég get bara ekki bíðað að gera þetta við þig núna.

Cannot wait to do this now is retained.


## 12. speech / 12 words / substantive text

Source ID: `68c19f62778c8188007d:0006`

> I thought it would be best if I slipped out this way.


### R0 · U · B017

Ég hélt að það væri best ef ég flýti út þannig.

Leaving is recognizable, but slipped out versus hurried out remains uncertain.


### oldDAPO120 · U · B042

Ég hélt að það væri best ef ég slíp út þannig.

The form slíp does not allow confident certification of slipped out.


### shortmidDAPO · U · B017

Ég hélt að það væri best ef ég flýti út þannig.

Leaving is recognizable, but slipped out versus hurried out remains uncertain.


## 13. news / 21 words / substantive text

Source ID: `9dbad5e0894379a5e96c:0019`

> &lt;p&gt;Gary Cooper made the role entirely his own, his integrity comparable only to Gregory Peck&#x27;s Atticus in To Kill a Mockingbird.


### R0 · F · B001

Gary Cooper náði hlutverki sínu að fullu sér sinni, hreintist honum aðeins sá heilbrigði og Gregory Peck í Atticus í To Kill a Mockingbird.

Integrity and the comparison with Atticus are garbled.


### oldDAPO120 · F · B044

Gary Cooper náði hlutverki sínu að fullu sér sinni, hreint sér aðeins saman við Atticus í Atticus í To Kill a Mockingbird sem Gregory Peck gaf sér.

The integrity comparison is garbled, with duplicated Atticus.


### shortmidDAPO · F · B040

Gary Cooper náði þáttinn í fullu sér sinn, hreintu hreinni hann aðeins í Gregory Peck hins Atticus í To Kill a Mockingbird.

Integrity and the role-comparison relationship are lost.


## 14. news / 39 words / substantive text

Source ID: `c1ba3b117b18185801f1:0040`

> &lt;p&gt;Hudson-Odoi took the tie into extra time in fantastic fashion, taking a touch on his chest and lofting a perfect volley over Okonkwo, but Wrexham were not to be denied their first top-flight FA Cup scalp for 26 years.


### R0 · F · B005

Hudson-Odoi tók víxliðið í viðbótartíma á frábæru hátt, tók tapp á brjóstina og hældi fullkomlega hólfu yfir Okonkwo, en Wrexham fengu ekki að hafa fengið fyrsta húð í FA kupsálinum í 26 árum.

Football actions and the first top-flight scalp in26 years are materially garbled.


### oldDAPO120 · F · B047

Hudson-Odoi tók týpu í viðbótartíma í frábæru hátt, tók tappa á brjóstina sína og hælt nákvæm tilvika hættu yfir Okonkwo, en Wrexham fengu ekki að missa fyrsta húð á FA kupsálinum í 26 árum.

Football actions, the first scalp and result are materially garbled.


### shortmidDAPO · F · B022

Hudson-Odoi tók víxlan í viðbótartíma í frábæru hátt, tók tapp á brjóstina sína og hældi fullkominni hólf yfir Okonkwo, en Wrexham fengu ekki að missa fyrsta húð þeirra í FA-kupanum í 26 árum.

Key football actions and the first top-flight scalp are materially garbled.


## 15. news / 31 words / substantive text

Source ID: `fda9531e50cdd1bb46e7:0005`

> &lt;p&gt;Robin Roefs was Sunderland&#x27;s hero as Everton&#x27;s FA Cup hopes came to a premature end once again after three woeful penalties in a shootout saw the Black Cats reach round four.


### R0 · F · B010

Robin Roefs var hringið Sunderland og endaði hamingja Everton í FA-kupsálinum á ný eftir þrjár skræfðar fyrirbæri í skrárinni þegar Svarta kettillin náðu fjórða kúpu.

Hero, penalties and progression to round four are materially garbled.


### oldDAPO120 · F · B014

Robin Roefs var hringi Sunderland og FA hóp Erlingarins létst á nýju leið eftir þrjár skræfum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andlegum andleg

Severe irrelevant repetition and missing match information.


### shortmidDAPO · F · B036

Robin Roefs var hringið Sunderland og endurtekið hamingjusöngur Everton á fimmtípu ógildandi hátt á eftir þrjár skræfðar áreikningar í skrárásinni og Black Cats náðu fjórða kringlunni.

Hero, penalties and match progression are materially garbled.


## 16. news / 24 words / substantive text

Source ID: `6c52413a733e6513e96b:0012`

> &lt;p&gt;After two rounds of the FBD League, the top two progress to next week&#x27;s final, with Galway facing the winner of tomorrow&#x27;s Roscommon-Mayo tie.


### R0 · F · B039

Eftir tvö kringlunir í FBD-hópnum fá tveir stjörnustöðvar síðasta viku í endaáttunni, að því er Galway í viðræðuna við siglinginn í Roscommon-Mayo-áttunni á morgun.

Next week becomes last week, with additional ranking/opponent distortion.


### oldDAPO120 · F · B023

Eftir tvö lotu í FBD-hópnum fá tveir fyrsta stjörnurnar næsta viku í endaáttunni, að Galway í viðmiðunarmálið við siglinginn í Roscommon-Mayo- samanburðið á morgun.

Progression rules and the winner/opponent relation are garbled.


### shortmidDAPO · F · B013

Eftir tvö lotur í FBD-hópnum fá tveir fyrsta stjörnurnar næsta viku í endaáttunni, að Galway í viðræðuna með vinum sínum á morgunnar í Roscommon-Mayo.

The top-two progression and opponent/winner relationships are garbled.


## 17. social / 18 words / substantive text

Source ID: `5d4ebce6bd448f4b42f2:0007`

> I&#x27;m FTTP/XGS-PON so I think just stuck with the 5x... not an insurmountable problem, just a little annoying.


### R0 · F · B006

Ég er FTTP/XGS-PON svo ég held að vera bara stökkvinn með 5x... ekki óhjákvæm vandamál, bara lítil þrálát.

Insurmountable is mistranslated, changing the central assessment.


### oldDAPO120 · F · B003

Ég er FTTP/XGS-PON svo ég held að vera bara stökkvinn með 5x... ekki óhjákvæm vandamál, bara lítil skammvæn.

The stuck/insurmountable-problem meanings are not retained.


### shortmidDAPO · F · B027

Ég er FTTP/XGS-PON svo ég held að vera bara stökkvinn með 5x... ekki óhjákvæm ámil, bara lítil óþægindi.

Being stuck and not having an insurmountable problem are mistranslated.


## 18. social / 22 words / substantive text

Source ID: `f658cc9d8d816e94c9c1:0005`

> It is too far away from any of my cameras to tell exactly what he was doing, but movement suggests sniffing around.


### R0 · F · B051

Það er of langt frá öllum myndavélum mínum til að vita nákvæmlega hvað hann var að gera en hreyfingar benda til sníðs.

The olfactory action sniffing is not retained in sní­ðs.


### oldDAPO120 · U · B052

Það er of langt frá öllum myndavélum mínum til að vita nákvæmlega hvað hann var að gera en hreyfingar benda til sníkka.

The final nonstandard word cannot be certified as sniffing; the observation context is mostly retained.


### shortmidDAPO · U · B052

Það er of langt frá öllum myndavélum mínum til að vita nákvæmlega hvað hann var að gera en hreyfingar benda til sníkka.

The final nonstandard word cannot be certified as sniffing; the observation context is mostly retained.


## 19. social / 20 words / substantive text

Source ID: `98dc59f74f8a2087167f:0011`

> &lt;br&gt;Had a similar problem when working on my house where literally every datum you might think of using was wrong.


### R0 · U · B038

Hefði sérhverju svipaða vandamál þegar ég var að vinna heima mínu þar sem allar upplýsingarnar sem ég hugsaði að nota voru allar rangar.

Construction datum and the opening tense are uncertain; complete fidelity cannot be certified.


### oldDAPO120 · U · B020

Hafði svipaða vandamál þegar ég var að vinna heima mínu þar sem allar upplýsingarnar sem ég hugsaði að nota voru allar rangar.

Datum may mean a construction reference; the candidate says information, so technical fidelity is uncertain.


### shortmidDAPO · U · B020

Hafði svipaða vandamál þegar ég var að vinna heima mínu þar sem allar upplýsingarnar sem ég hugsaði að nota voru allar rangar.

Datum may mean a construction reference; the candidate says information, so technical fidelity is uncertain.


## 20. social / 36 words / substantive text

Source ID: `1ba5402f736862a1747f:0002`

> &lt;br&gt;Assuming she took it from the veins around the elbow, theres a chance she went too deep and hit the back wall of the vein, and an underlying tendon then bruised it on the way out.


### R0 · F · B045

Hún tók það úr bláæðum í kringum eldið, þá er líkur á að hún hafi komið of djúp og hafi hett á bakverri bláæðarinnar og þá hefur vefjaþrengið það í gegnum ferðina.

The assumption is asserted as fact, with elbow/tendon injury distortion.


### oldDAPO120 · F · B037

Hafi hún tekið það úr bláæðum í kringum eldið, er möguleiki á að hún hafi komið of djúp og hafi hett á bakverri bláæðarinnar og þá hefur tænur þá sáttstífla það á leiðinni út.

Elbow, vein-wall and tendon-injury details are materially garbled.


### shortmidDAPO · F · B034

Því að hún tók það úr bláæðinum í kringum eldið, er líkur á að hún hafi komið of djúp og hafi hett í bakverri bláæðarinnar og þá hefur vefið þar í þrengt það á leiðinni út.

Elbow, tendon and injury/causation details are materially garbled.


## 21. speech / 14 words / substantive text

Source ID: `0b6ccedbcf9a7f1e8059:0000`

> She talked about how impossible it is to be a woman in today&#x27;s society.


### R0 · F · B048

Hún talaði um hversu óhjálegt er að vera konu í dagins félags.

The central meaning of impossible is mistranslated.


### oldDAPO120 · F · B021

Hún talaði um hversu óhjálegt er að vera kona í dagins samfélags.

The central meaning of impossible is mistranslated.


### shortmidDAPO · F · B004

Hún talaði um hversu óhjálegt er að vera kona í dagins félags.

The central predicate impossible is mistranslated.


## 22. speech / 17 words / substantive text

Source ID: `f5e3d55fe3de929d6cac:0000`

> Jade, if you want to get back together with Beck, then why don&#x27;t you just tell him?


### R0 · F · B032

Jade, ef þú vilt koma aftur saman með Beck, þá hvers vegna skaltu hann það ekki?

The key predicate tell him is missing.


### oldDAPO120 · U · B009

Jade, ef þú vilt ná aftur saman með Beck, þá hvers vegna skaltu hann þá ekki segja?

Reunion is recognizable, but the pronoun/predicate structure prevents confident fidelity certification.


### shortmidDAPO · P · B026

Jade, ef þú vilt fara aftur með Beck, þá hvers vegna skaltu þá ekki bara segja honum það?

Getting back together with Beck and telling him are retained.


## 23. speech / 18 words / substantive text

Source ID: `1ef44f7d70897cb5c9f2:0005`

> It&#x27;s one thing to fill his head with nonsense about the North Pole, but dial S for Santa.


### R0 · F · B016

Það er eitt og sama að fylla höfuð hans með óvísu um Norðurhvelið, en hringja S fyrir Santa.

North Pole becomes Northern Hemisphere, with additional Santa-related distortion.


### oldDAPO120 · F · B030

Það er eitt svið að fylla höfuð hans með óvísu um Norðurhvelið, en síðan hringdu S fyrir Jólafíkn.

Both North Pole and Santa are mistranslated.


### shortmidDAPO · F · B028

Það er eitt og sama að fylla höfuð hans með óvísu um Norðurhvelið, en hringja í S fyrir Jólafönginn.

North Pole becomes Northern Hemisphere, and Santa is also distorted.


## 24. speech / 19 words / substantive text

Source ID: `27f428d50b218fe48c52:0010`

> You don&#x27;t think they&#x27;d let me in the kitchen if they knew I was organizing the strike, do you?


### R0 · F · B007

Heldurðu að þeir myndu láta mig koma inn í eldhúsin ef þeir vissu að ég væri að skipuleggja stríðina, er það?

Strike is rendered with the war-related word stríð.


### oldDAPO120 · F · B007

Heldurðu að þeir myndu láta mig koma inn í eldhúsin ef þeir vissu að ég væri að skipuleggja stríðina, er það?

Strike is rendered with the war-related word stríð.


### shortmidDAPO · F · B033

Heldur þú að þeir myndu láta mig koma inn í eldhúsin ef þeir vissu að ég væri að skipuleggja stríðina, er það nokkuð?

Strike is rendered with the war-related word stríð.
