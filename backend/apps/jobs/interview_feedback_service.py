"""Deterministic domain rules for interview feedback in the job application tracker."""

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
class InterviewFeedbackService:
    thresholds: Mapping[str, int] = field(default_factory=dict)

    def normalize(self, value: object) -> str:
        return " ".join(str(value or "").strip().lower().split())

    def clamp(self, value: object, low: int = 0, high: int = 100) -> int:
        try: value = int(value)
        except (TypeError, ValueError): value = low
        return max(low, min(high, value))

    def threshold(self, name: str, default: int) -> int:
        return self.clamp(self.thresholds.get(name, default))

    def classify(self, score: object) -> str:
        value=self.clamp(score)
        if value >= self.threshold("strong",80): return "strong"
        if value >= self.threshold("healthy",60): return "healthy"
        if value >= self.threshold("watch",40): return "watch"
        return "risk"

    def decision(self, code: str, message: str, score: object, severity: str="info") -> Decision:
        return Decision(code,message,severity,self.clamp(score))

    def average(self, values: Iterable[object]) -> int:
        items=[self.clamp(v) for v in values]
        return 0 if not items else round(sum(items)/len(items))

    def unique(self, values: Iterable[object]) -> list[str]:
        result=[]; seen=set()
        for value in values:
            item=self.normalize(value)
            if item and item not in seen: seen.add(item); result.append(item)
        return result

    def overlap(self, left: Iterable[object], right: Iterable[object]) -> float:
        a=set(self.unique(left)); b=set(self.unique(right))
        return 0.0 if not a else round(len(a&b)/len(a)*100,2)

    def age_days(self, value: date|datetime|None, today: date|None=None) -> int:
        if not value: return 0
        point=value.date() if isinstance(value,datetime) else value
        return max(0,((today or date.today())-point).days)

    def overdue(self, value: date|None, today: date|None=None) -> bool:
        return bool(value and value < (today or date.today()))

    def next_date(self, start: date, days: int) -> date:
        return start + timedelta(days=max(0,int(days)))

    def evaluate(self, record: Mapping[str,object]) -> Decision:
        score=self.clamp(record.get("score",0))
        code=self.classify(score)
        severity="warning" if code in ("watch","risk") else "info"
        return self.decision(code,"record classified as "+code,score,severity)

    def build_signal(self,a,b=0,c=0):
        return self.evaluate({"score":round(self.clamp(a)*.55+self.clamp(b)*.30+self.clamp(c)*.15)})
    def missing(self,values,required):
        return [key for key in required if values.get(key) in (None,"",[],{})]
    def present_score(self,values):
        return self.clamp(round(sum(v not in (None,"",[],{}) for v in values.values())/max(1,len(values))*100))
    def contains_any(self,text,terms):
        return any(self.normalize(term) in self.normalize(text) for term in terms)
    def merge(self,*groups):
        return self.unique(item for group in groups for item in group)
    def filter_min(self,records,minimum=0):
        return [r for r in records if self.clamp(r.get("score",0))>=minimum]
    def sort_by(self,records,key,reverse=True):
        return sorted(records,key=lambda r: float(r.get(key,0) or 0),reverse=reverse)
    def group_by(self,records,key):
        
                groups={}
                for record in records: groups.setdefault(str(record.get(key,"unknown")),[]).append(record)
                return groups
    def status_counts(self,records,field="status"):
        
                counts={}
                for record in records: key=self.normalize(record.get(field,"unknown")) or "unknown"; counts[key]=counts.get(key,0)+1
                return counts
    def trend(self,scores):
        
                if len(scores)<2: return "stable"
                delta=self.clamp(scores[-1])-self.clamp(scores[0])
                return "improving" if delta>=10 else "declining" if delta<=-10 else "stable"
    def percentile(self,value,population):
        
                values=sorted(self.clamp(v) for v in population)
                return 0.0 if not values else round(sum(v<=self.clamp(value) for v in values)/len(values)*100,2)
    def coverage(self,required,available):
        return self.overlap(required,available)
    def bucket(self,records):
        
                result={"strong":0,"healthy":0,"watch":0,"risk":0}
                for record in records: result[self.classify(record.get("score",0))]+=1
                return result
    def summary(self,records):
        
                scores=[r.get("score",0) for r in records]
                return {"count":len(records),"average":self.average(scores),"buckets":self.bucket(records)}
    def explain(self,record):
        
                d=self.evaluate(record)
                return [d.code,d.message,"score="+str(d.score),"severity="+d.severity]
    def top(self,records,key,limit=5):
        return self.sort_by(records,key)[:max(0,limit)]
    def bottom(self,records,key,limit=5):
        return self.sort_by(records,key,False)[:max(0,limit)]
    def safe_int(self,value,default=0):
        
                try: return int(value)
                except (TypeError,ValueError): return default
    def safe_float(self,value,default=0.0):
        
                try: return float(value)
                except (TypeError,ValueError): return default
    def window(self,start,length):
        return (start,self.next_date(start,length))
    def in_window(self,point,start,end):
        return start<=point<=end
    def action_plan(self,record):
        
                code=self.evaluate(record).code
                return ["review","clarify missing information","schedule follow-up"] if code=="risk" else ["monitor","set review date"] if code=="watch" else ["continue","record next milestone"]
    def weighted(self,values,weights):
        
                pairs=list(zip(values,weights))
                total=sum(max(0,float(w)) for _,w in pairs)
                return 0.0 if not total else round(sum(self.safe_float(v)*max(0,float(w)) for v,w in pairs)/total,2)
    def rank(self,records,key):
        
                ranked=self.sort_by(records,key)
                return [{**record,"rank":index+1} for index,record in enumerate(ranked)]
