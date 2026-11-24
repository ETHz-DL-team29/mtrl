import statistics

def next_group(examples,order,cursor,remaining,batch_size):
    selected=[]
    while cursor<len(order) and len(selected)<batch_size:
        row=examples[order[cursor]];n=len(row['target'])
        if n>remaining:break
        selected.append(row);remaining-=n;cursor+=1
    return selected,cursor

def selection_score(records):
    grouped={k:[] for k in ['general','technical_short','technical_medium','technical_long']}
    for row in records:grouped[row['stratum']].append(row['sentence_chrfpp'] if row['gate'] else 0.)
    if any(not v for v in grouped.values()):raise ValueError('Every frozen validation stratum must be represented')
    means={k:statistics.mean(v) for k,v in grouped.items()}
    return .5*means['general']+.5*statistics.mean(means[k] for k in means if k!='general'),means

def selection_key(metrics):return (metrics['selection_score'],-metrics['nll'])
