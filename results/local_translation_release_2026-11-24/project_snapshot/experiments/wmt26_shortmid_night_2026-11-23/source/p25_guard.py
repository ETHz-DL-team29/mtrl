"""Conservative invariant checks,not a semantic oracle. No negation-by-keyword rule."""
import re,unicodedata,collections,decimal
def fold(x):return ''.join(c for c in unicodedata.normalize('NFKD',x).casefold() if not unicodedata.combining(c))
def number(x):return format(decimal.Decimal(x.replace(',','.')).normalize(),'f')
DOSE=re.compile(r'(?<![\w.,])(\d+(?:[.,]\d+)?)\s*(mg|μg|µg|mcg|ug|g|ml|mL|l|L|%)(?:\s*/\s*(kg|m2|m²))?(?!\w)',re.I)
NUM=re.compile(r'(?<!\w)\d+(?:[.,]\d+)?(?!\w)')
WORDS=re.compile(r'\b(einn|ein|eitt|tveir|tvær|tvö|þrír|þrjár|þrjú|fjórir|fjórar|fjögur|fimm|sex|sjö|átta|níu|tíu|tuttugu|þrjátíu|hundrað|þúsund)\b',re.I)
def quantities(text):
 if re.search(r'\b\d{1,3}[.,]\d{3}(?:\b|[.,])',text):return None
 dose=[]
 for m in DOSE.finditer(text):
  unit=m[2].casefold().replace('µ','μ');value=decimal.Decimal(m[1].replace(',','.'));base='mass' if unit in ['g','mg','μg','mcg','ug'] else 'volume' if unit in ['ml','l'] else '%'
  scale={'g':1000,'mg':1,'μg':decimal.Decimal('.001'),'mcg':decimal.Decimal('.001'),'ug':decimal.Decimal('.001'),'l':1000,'ml':1,'%':1}[unit]
  dose.append((base,(m[3] or '').replace('²','2'),format((value*scale).normalize(),'f')))
 rest=DOSE.sub(' ',text);nums=[number(m.group()) for m in NUM.finditer(rest)]
 return collections.Counter(dose),collections.Counter(nums)
def check(row,hyp):
 reasons=[];a,b=row['source'],row['reference'];x,y,z=quantities(a),quantities(b),quantities(hyp)
 if x is not None and y is not None and z is not None and x==y and not WORDS.search(hyp):
  if x!=z:reasons.append('source_reference_agree_numeric_or_unit_mismatch')
 if row.get('subcorpus')=='ema':
  anchors=[s for s in re.findall(r'\b[A-Z][A-Za-z0-9-]{4,}\b',a) if any(fold(t).startswith(fold(s)) for t in re.findall(r'[\w-]+',b))]
  missing=[s for s in anchors if not any(fold(t).startswith(fold(s)) for t in re.findall(r'[\w-]+',hyp))]
  if missing:reasons.append('reference_confirmed_EMA_anchor_missing:'+','.join(sorted(set(missing))))
 words=hyp.casefold().split();grams=list(zip(words,words[1:],words[2:]));repeated=len(words)>=20 and len(set(grams))/max(1,len(grams))<.4
 if not hyp.strip():reasons.append('empty')
 if fold(hyp.strip())==fold(a.strip()) and len(a.split())>=8:reasons.append('exact_source_copy')
 if repeated:reasons.append('severe_repetition_heuristic')
 return reasons
def reward(row,hyp,error,recipe):
 reasons=check(row,hyp);value=1-min(25,max(0,error))/25
 if recipe=='guarded':
  value-=.25*int(any('numeric_or_unit' in s for s in reasons));value-=.25*int(any('EMA_anchor' in s for s in reasons))
  if any(s in reasons for s in ['empty','exact_source_copy','severe_repetition_heuristic']):value=0
 return float(value),reasons
