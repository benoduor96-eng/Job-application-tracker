"""Business rules for skill profiles."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Iterable, Mapping, Sequence

@dataclass(frozen=True)
class Decision:
    code: str
    message: str
    severity: str = "info"
    score: int = 0

@dataclass(frozen=True)
class SkillProfileService:
    thresholds: Mapping[str,int] = field(default_factory=dict)
    def normalize(self,v): return " ".join(str(v or "").strip().lower().split())
    def clamp(self,v,lo=0,hi=100):
        try: v=int(v)
        except (TypeError,ValueError): v=lo
        return max(lo,min(hi,v))
    def avg(self,values):
        xs=[self.clamp(v) for v in values]; return 0 if not xs else round(sum(xs)/len(xs))
    def classify(self,v):
        n=self.clamp(v); a=self.thresholds.get("strong",80); b=self.thresholds.get("healthy",60); c=self.thresholds.get("watch",40)
        return "strong" if n>=a else "healthy" if n>=b else "watch" if n>=c else "risk"
    def evaluate(self,record):
        n=self.clamp(record.get("score",0)); code=self.classify(n); sev="warning" if code in ("watch","risk") else "info"
        return Decision(code,"record classified as "+code,sev,n)
    def unique(self,values):
        out=[]; seen=set()
        for v in values:
            x=self.normalize(v)
            if x and x not in seen: seen.add(x); out.append(x)
        return out
    def overlap(self,left,right):
        a=set(self.unique(left)); b=set(self.unique(right)); return 0.0 if not a else round(len(a&b)/len(a)*100,2)
    def age_days(self,value,today=None):
        if not value: return 0
        point=value.date() if isinstance(value,datetime) else value; return max(0,((today or date.today())-point).days)
    def overdue(self,value,today=None): return bool(value and value<(today or date.today()))
    def next_date(self,start,days): return start+timedelta(days=max(0,int(days)))
    def missing(self,values,required): return [k for k in required if values.get(k) in (None,"",[],{})]
    def present_score(self,values): return self.clamp(round(sum(v not in (None,"",[],{}) for v in values.values())/max(1,len(values))*100))
    def contains_any(self,text,terms): return any(self.normalize(t) in self.normalize(text) for t in terms)
    def merge(self,*groups): return self.unique(x for group in groups for x in group)
    def filter_min(self,records,minimum=0): return [r for r in records if self.clamp(r.get("score",0))>=minimum]
    def sort_by(self,records,key,reverse=True): return sorted(records,key=lambda r:float(r.get(key,0) or 0),reverse=reverse)
    def group_by(self,records,key):
        groups={}
        for r in records: groups.setdefault(str(r.get(key,"unknown")),[]).append(r)
        return groups
    def status_counts(self,records,field="status"):
        out={}
        for r in records:
            k=self.normalize(r.get(field,"unknown")) or "unknown"; out[k]=out.get(k,0)+1
        return out
    def trend(self,scores):
        if len(scores)<2: return "stable"
        d=self.clamp(scores[-1])-self.clamp(scores[0]); return "improving" if d>=10 else "declining" if d<=-10 else "stable"
    def bucket(self,records):
        out={"strong":0,"healthy":0,"watch":0,"risk":0}
        for r in records: out[self.classify(r.get("score",0))]+=1
        return out
    def summary(self,records):
        scores=[r.get("score",0) for r in records]; return {"count":len(records),"average":self.avg(scores),"buckets":self.bucket(records)}
    def explain(self,record):
        d=self.evaluate(record); return [d.code,d.message,"score="+str(d.score),"severity="+d.severity]
    def top(self,records,key,limit=5): return self.sort_by(records,key)[:max(0,limit)]
    def bottom(self,records,key,limit=5): return self.sort_by(records,key,False)[:max(0,limit)]
    def safe_int(self,value,default=0):
        try: return int(value)
        except (TypeError,ValueError): return default
    def safe_float(self,value,default=0.0):
        try: return float(value)
        except (TypeError,ValueError): return default
    def coverage(self,required,available): return self.overlap(required,available)
    def window(self,start,length): return (start,self.next_date(start,length))
    def in_window(self,point,start,end): return start<=point<=end
    def action_plan(self,record):
        code=self.evaluate(record).code
        return ["review","clarify missing information","schedule follow-up"] if code=="risk" else ["monitor","set review date"] if code=="watch" else ["continue","record next milestone"]
    def weighted(self,values,weights):
        pairs=list(zip(values,weights)); total=sum(max(0,float(w)) for _,w in pairs)
        return 0.0 if not total else round(sum(self.safe_float(v)*max(0,float(w)) for v,w in pairs)/total,2)
    def rank(self,records,key): return [{**r,"rank":i+1} for i,r in enumerate(self.sort_by(records,key))]
