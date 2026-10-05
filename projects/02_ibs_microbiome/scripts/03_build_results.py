from pathlib import Path
from collections import defaultdict
import numpy as np, pandas as pd
import matplotlib.pyplot as plt

ROOT=Path("results_actual"); T=ROOT/"tables"; F=ROOT/"figures"; ML=ROOT/"ml"
F.mkdir(parents=True,exist_ok=True); ML.mkdir(parents=True,exist_ok=True)

with open(T/"feature-table.tsv") as f:
    lines=[x.rstrip("\n") for x in f if not x.startswith("#")]
parts=lines[0].split("\t")
samples=parts[1:]
if samples and samples[-1]=="": samples=samples[:-1]
rows=[]
for line in lines[1:]:
    p=line.split("\t")
    if len(p)>1: rows.append([p[0]]+[float(x or 0) for x in p[1:1+len(samples)]])
counts=pd.DataFrame(rows,columns=["feature"]+samples).set_index("feature")

meta=pd.read_csv("metadata/sample-metadata.tsv",sep="\t").set_index("sample-id").loc[samples]
labels=meta.group.map({"HC":0,"IBS":1}).values

tax=pd.read_csv(T/"taxonomy.tsv",sep="\t").fillna("")
taxmap=dict(zip(tax["Feature ID"],tax["Taxon"]))

def genus(t):
    p=[x.strip() for x in t.split(";")]
    if len(p)<6: return "Unassigned"
    x=p[5]
    return x.split("__",1)[-1] if "__" in x else (x or "Unassigned")

rel=counts.div(counts.sum(axis=0),axis=1)
g=defaultdict(lambda:np.zeros(len(samples)))
for feat in rel.index: g[genus(taxmap.get(feat,""))]+=rel.loc[feat].values
X=pd.DataFrame(g,index=samples).T
X=X.loc[(X>0).mean(axis=1)>0.10]
X=X.loc[X.mean(axis=1)>0]
X=np.log(X+1e-6)
X=X.sub(X.mean(axis=0),axis=1).T

alpha=[]
for s in samples:
    x=counts[s].values; x=x[x>0]; p=x/x.sum()
    alpha.append([s,meta.loc[s,"group"],int((counts[s]>0).sum()),-np.sum(p*np.log(p)),1-np.sum(p*p)])
ad=pd.DataFrame(alpha,columns=["sample","group","observed_features","shannon","simpson"])
ad.to_csv(T/"alpha_diversity.tsv",sep="\t",index=False)

from sklearn.model_selection import StratifiedKFold,cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score,accuracy_score,precision_score,recall_score

cv=StratifiedKFold(n_splits=5,shuffle=True,random_state=42)
models={
"l1_logistic":Pipeline([("scale",StandardScaler()),("model",LogisticRegression(penalty="l1",solver="liblinear",max_iter=3000,class_weight="balanced"))]),
"random_forest":RandomForestClassifier(n_estimators=300,random_state=42,class_weight="balanced",n_jobs=-1,max_features="sqrt")
}
out=[]
for name,m in models.items():
    prob=cross_val_predict(m,X.values,labels,cv=cv,method="predict_proba")[:,1]
    pred=(prob>=0.5).astype(int)
    out.append([name,roc_auc_score(labels,prob),accuracy_score(labels,pred),precision_score(labels,pred),recall_score(labels,pred)])
pd.DataFrame(out,columns=["model","roc_auc","accuracy","precision","sensitivity"]).to_csv(ML/"cross_validation_metrics.tsv",sep="\t",index=False)

m=models["l1_logistic"].fit(X.values,labels)
coef=m.named_steps["model"].coef_[0]
pd.DataFrame({"genus":X.columns,"coefficient":coef,"abs_coefficient":np.abs(coef)}).query("abs_coefficient>0").sort_values("abs_coefficient",ascending=False).to_csv(ML/"l1_selected_genera.tsv",sep="\t",index=False)

mean_genus=rel.copy()
for feat in mean_genus.index: mean_genus.loc[feat]=mean_genus.loc[feat]
G=defaultdict(lambda:np.zeros(len(samples)))
for feat in rel.index: G[genus(taxmap.get(feat,""))]+=rel.loc[feat].values
gd=pd.DataFrame(G,index=samples).T
top=gd.mean(axis=1).sort_values(ascending=False).head(15).index
gd.loc[top].T.plot(kind="bar",stacked=True,figsize=(12,6))
plt.ylabel("Relative abundance"); plt.title("Top 15 genera"); plt.tight_layout(); plt.savefig(F/"genus_relative_abundance.png",dpi=180); plt.close()

report=["# Actual outcome — IBS microbiome cohort","",
"Public-data-only re-analysis of PRJNA637763.","",
"## Cohort",f"- Samples analyzed: {len(samples)}",f"- IBS: {sum(labels==1)}",f"- Healthy controls: {sum(labels==0)}",f"- Genus features after prevalence filtering: {X.shape[1]}","",
"## Alpha diversity",f"- Mean observed features, IBS: {ad.loc[ad.group=='IBS','observed_features'].mean():.2f}",f"- Mean observed features, HC: {ad.loc[ad.group=='HC','observed_features'].mean():.2f}",f"- Mean Shannon, IBS: {ad.loc[ad.group=='IBS','shannon'].mean():.4f}",f"- Mean Shannon, HC: {ad.loc[ad.group=='HC','shannon'].mean():.4f}","",
"## Classification","Five-fold stratified cross-validation."]
for r in out: report.append(f"- {r[0]}: ROC-AUC={r[1]:.4f}; accuracy={r[2]:.4f}; precision={r[3]:.4f}; sensitivity={r[4]:.4f}")
report += ["","These are independent re-analysis metrics, not clinical diagnostic validation."]
(ROOT/"REPORT.md").write_text("\n".join(report))
print("\n".join(report))
