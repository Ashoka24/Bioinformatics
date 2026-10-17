from pathlib import Path
import csv, math, re
root=Path('results_actual')
def read(p):
    with open(p,newline='') as f: return list(csv.reader(f,delimiter='\t'))
feat=read(root/'tables/feature-table.tsv'); tax=read(root/'tables/taxonomy.tsv')
counts={r[0]:int(float(r[1])) for r in feat[1:] if len(r)>1 and r[0] and not r[0].startswith('#')}
taxonomy={r[0]:r[1] for r in tax[1:] if len(r)>1}
total=sum(counts.values()); observed=len(counts); probs=[v/total for v in counts.values()] if total else []
shannon=-sum(p*math.log(p) for p in probs if p); simpson=1-sum(p*p for p in probs); invsimpson=(1/sum(p*p for p in probs)) if probs else 0; pielou=shannon/math.log(observed) if observed>1 else 0
def alpha(name):
    p=root/'tables'/name/'alpha-diversity.tsv'
    if not p.exists(): return 'NA'
    r=read(p); return r[1][1] if len(r)>1 and len(r[1])>1 else 'NA'
labels={2:'phylum',3:'class',4:'order',5:'family',6:'genus',7:'species'}
for level,name in labels.items():
    agg={}
    for fid,c in counts.items():
        parts=[x.strip() for x in taxonomy.get(fid,'Unclassified').split(';')]
        key=parts[level-1] if len(parts)>=level and parts[level-1] else 'Unclassified'
        agg[key]=agg.get(key,0)+c
    with open(root/f'tables/{name}_abundance.tsv','w') as f:
        f.write('taxon\tread_count\trelative_abundance_percent\n')
        for k,v in sorted(agg.items(),key=lambda z:z[1],reverse=True): f.write(f'{k}\t{v}\t{100*v/total if total else 0:.4f}\n')
def svg(name,title):
    data=[]
    with open(root/f'tables/{name}_abundance.tsv') as f:
        for r in list(csv.DictReader(f,delimiter='\t'))[:15]: data.append((r['taxon'],float(r['relative_abundance_percent'])))
    m=max([x[1] for x in data] or [1]); H=80+32*len(data); s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="{H}"><text x="20" y="30" font-size="20">{title}</text>']; y=55
    for k,v in data:
        w=480*v/m if m else 0; s += [f'<text x="20" y="{y+15}" font-size="12">{k[:70]}</text>',f'<rect x="450" y="{y}" width="{w:.1f}" height="20" fill="currentColor"/><text x="950" y="{y+15}" font-size="12">{v:.2f}%</text>']; y+=32
    s.append('</svg>'); (root/'figures').mkdir(exist_ok=True); (root/'figures'/f'{name}_relative_abundance.svg').write_text('\n'.join(s))
svg('phylum','SRR26534086 — relative abundance by Phylum'); svg('genus','SRR26534086 — relative abundance by Genus')
report=['# Actual outcome — SRR26534086','', 'Results generated from the public FASTQ; no private/company data. Single-run workflow validation, not cohort-level inference.','', '## Dataset','- BioSample: `SAMN37943185`','- BioProject: `PRJNA1031545`','- Experiment: `SRX22237515`','- Assay: 16S rRNA V3–V4','- Instrument: Illumina MiSeq','', '## Processing','- QIIME 2 2024.10 amplicon Docker image','- Cutadapt primer trimming with the study-reported V3–V4 primers','- DADA2 paired-end; truncation 280/260; max EE 2/2','- SILVA 138 99% full-length Naive Bayes classifier','- Classifier SHA256: `c08a1aa4d56b449b511f7215543a43249ae9c54b57491428a7e5548a62613616`','', '## Actual metrics',f'- Input/denoised table read count: **{total:,}**',f'- Observed ASVs: **{observed}**',f'- Shannon: **{shannon:.6f}**',f'- Simpson: **{simpson:.6f}**',f'- Inverse Simpson: **{invsimpson:.6f}**',f'- Pielou evenness: **{pielou:.6f}**',f'- QIIME observed_features: **{alpha("observed_features")}**',f'- QIIME Shannon: **{alpha("shannon")}**','', '## Taxonomy outputs','Phylum, class, order, family, genus and species abundance tables are generated from the ASV counts and assigned taxonomy.','', 'Beta diversity/PERMANOVA is intentionally omitted because only one sample is analyzed.','']
(root/'REPORT.md').write_text('\n'.join(report))