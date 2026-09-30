"""Deterministic company_research domain engine for job-search workflows."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Mapping, Sequence

@dataclass(frozen=True)
class CompanyResearchResult:
    key: str
    score: float
    status: str
    reasons: tuple[str, ...] = ()

@dataclass
class CompanyResearchContext:
    values: dict[str, object] = field(default_factory=dict)
    def text(self,key:str,default:str="")->str:
        value=self.values.get(key,default)
        return str(value).strip() if value is not None else default
    def number(self,key:str,default:float=0.0)->float:
        try: return float(self.values.get(key,default))
        except (TypeError,ValueError): return default
    def flag(self,key:str,default:bool=False)->bool:
        value=self.values.get(key,default)
        return value.lower() in {"1","true","yes","on"} if isinstance(value,str) else bool(value)

def clamp(value:float,low:float=0.0,high:float=100.0)->float:
    return max(low,min(high,value))

class CompanyResearchEngine:
    def evaluate(self, context:Mapping[str,object]|CompanyResearchContext|None=None)->CompanyResearchResult:
        ctx=context if isinstance(context,CompanyResearchContext) else CompanyResearchContext(dict(context or {}))
        score=50.0; reasons=[]
        for area in ["mission","industry","size","location","culture","technology","leadership","growth","stability","role","news","questions"]:
            delta=self._area_score(area,ctx); score+=delta
            if delta>0: reasons.append(f"{area}: positive")
            if delta<0: reasons.append(f"{area}: review")
        score=clamp(score)
        status="strong" if score>=80 else "acceptable" if score>=60 else "review"
        return CompanyResearchResult("overall",round(score,2),status,tuple(reasons))
    def _area_score(self,area:str,ctx:CompanyResearchContext)->float:
        if ctx.flag(f"{area}_blocked"): return -5.0
        if ctx.flag(f"{area}_complete"): return 3.0
        if ctx.text(area): return 1.0
        return -1.0
    def mission_rule_1(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("mission_score",0.0)
        if ctx.flag("mission_blocked"): return -5.0
        if ctx.flag("mission_1_complete"): return 2.0
        if ctx.text("mission_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def mission_rule_2(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("mission_score",0.0)
        if ctx.flag("mission_blocked"): return -5.0
        if ctx.flag("mission_2_complete"): return 3.0
        if ctx.text("mission_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def mission_rule_3(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("mission_score",0.0)
        if ctx.flag("mission_blocked"): return -5.0
        if ctx.flag("mission_3_complete"): return 4.0
        if ctx.text("mission_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def mission_rule_4(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("mission_score",0.0)
        if ctx.flag("mission_blocked"): return -5.0
        if ctx.flag("mission_4_complete"): return 1.0
        if ctx.text("mission_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def mission_rule_5(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("mission_score",0.0)
        if ctx.flag("mission_blocked"): return -5.0
        if ctx.flag("mission_5_complete"): return 2.0
        if ctx.text("mission_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def mission_rule_6(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("mission_score",0.0)
        if ctx.flag("mission_blocked"): return -5.0
        if ctx.flag("mission_6_complete"): return 3.0
        if ctx.text("mission_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def mission_rule_7(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("mission_score",0.0)
        if ctx.flag("mission_blocked"): return -5.0
        if ctx.flag("mission_7_complete"): return 4.0
        if ctx.text("mission_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def mission_rule_8(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("mission_score",0.0)
        if ctx.flag("mission_blocked"): return -5.0
        if ctx.flag("mission_8_complete"): return 1.0
        if ctx.text("mission_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def mission_rule_9(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("mission_score",0.0)
        if ctx.flag("mission_blocked"): return -5.0
        if ctx.flag("mission_9_complete"): return 2.0
        if ctx.text("mission_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def mission_rule_10(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("mission_score",0.0)
        if ctx.flag("mission_blocked"): return -5.0
        if ctx.flag("mission_10_complete"): return 3.0
        if ctx.text("mission_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def mission_rule_11(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("mission_score",0.0)
        if ctx.flag("mission_blocked"): return -5.0
        if ctx.flag("mission_11_complete"): return 4.0
        if ctx.text("mission_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def mission_rule_12(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("mission_score",0.0)
        if ctx.flag("mission_blocked"): return -5.0
        if ctx.flag("mission_12_complete"): return 1.0
        if ctx.text("mission_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def mission_rule_13(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("mission_score",0.0)
        if ctx.flag("mission_blocked"): return -5.0
        if ctx.flag("mission_13_complete"): return 2.0
        if ctx.text("mission_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def mission_rule_14(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("mission_score",0.0)
        if ctx.flag("mission_blocked"): return -5.0
        if ctx.flag("mission_14_complete"): return 3.0
        if ctx.text("mission_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def industry_rule_1(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("industry_score",0.0)
        if ctx.flag("industry_blocked"): return -5.0
        if ctx.flag("industry_1_complete"): return 2.0
        if ctx.text("industry_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def industry_rule_2(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("industry_score",0.0)
        if ctx.flag("industry_blocked"): return -5.0
        if ctx.flag("industry_2_complete"): return 3.0
        if ctx.text("industry_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def industry_rule_3(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("industry_score",0.0)
        if ctx.flag("industry_blocked"): return -5.0
        if ctx.flag("industry_3_complete"): return 4.0
        if ctx.text("industry_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def industry_rule_4(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("industry_score",0.0)
        if ctx.flag("industry_blocked"): return -5.0
        if ctx.flag("industry_4_complete"): return 1.0
        if ctx.text("industry_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def industry_rule_5(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("industry_score",0.0)
        if ctx.flag("industry_blocked"): return -5.0
        if ctx.flag("industry_5_complete"): return 2.0
        if ctx.text("industry_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def industry_rule_6(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("industry_score",0.0)
        if ctx.flag("industry_blocked"): return -5.0
        if ctx.flag("industry_6_complete"): return 3.0
        if ctx.text("industry_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def industry_rule_7(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("industry_score",0.0)
        if ctx.flag("industry_blocked"): return -5.0
        if ctx.flag("industry_7_complete"): return 4.0
        if ctx.text("industry_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def industry_rule_8(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("industry_score",0.0)
        if ctx.flag("industry_blocked"): return -5.0
        if ctx.flag("industry_8_complete"): return 1.0
        if ctx.text("industry_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def industry_rule_9(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("industry_score",0.0)
        if ctx.flag("industry_blocked"): return -5.0
        if ctx.flag("industry_9_complete"): return 2.0
        if ctx.text("industry_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def industry_rule_10(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("industry_score",0.0)
        if ctx.flag("industry_blocked"): return -5.0
        if ctx.flag("industry_10_complete"): return 3.0
        if ctx.text("industry_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def industry_rule_11(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("industry_score",0.0)
        if ctx.flag("industry_blocked"): return -5.0
        if ctx.flag("industry_11_complete"): return 4.0
        if ctx.text("industry_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def industry_rule_12(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("industry_score",0.0)
        if ctx.flag("industry_blocked"): return -5.0
        if ctx.flag("industry_12_complete"): return 1.0
        if ctx.text("industry_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def industry_rule_13(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("industry_score",0.0)
        if ctx.flag("industry_blocked"): return -5.0
        if ctx.flag("industry_13_complete"): return 2.0
        if ctx.text("industry_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def industry_rule_14(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("industry_score",0.0)
        if ctx.flag("industry_blocked"): return -5.0
        if ctx.flag("industry_14_complete"): return 3.0
        if ctx.text("industry_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def size_rule_1(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("size_score",0.0)
        if ctx.flag("size_blocked"): return -5.0
        if ctx.flag("size_1_complete"): return 2.0
        if ctx.text("size_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def size_rule_2(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("size_score",0.0)
        if ctx.flag("size_blocked"): return -5.0
        if ctx.flag("size_2_complete"): return 3.0
        if ctx.text("size_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def size_rule_3(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("size_score",0.0)
        if ctx.flag("size_blocked"): return -5.0
        if ctx.flag("size_3_complete"): return 4.0
        if ctx.text("size_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def size_rule_4(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("size_score",0.0)
        if ctx.flag("size_blocked"): return -5.0
        if ctx.flag("size_4_complete"): return 1.0
        if ctx.text("size_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def size_rule_5(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("size_score",0.0)
        if ctx.flag("size_blocked"): return -5.0
        if ctx.flag("size_5_complete"): return 2.0
        if ctx.text("size_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def size_rule_6(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("size_score",0.0)
        if ctx.flag("size_blocked"): return -5.0
        if ctx.flag("size_6_complete"): return 3.0
        if ctx.text("size_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def size_rule_7(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("size_score",0.0)
        if ctx.flag("size_blocked"): return -5.0
        if ctx.flag("size_7_complete"): return 4.0
        if ctx.text("size_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def size_rule_8(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("size_score",0.0)
        if ctx.flag("size_blocked"): return -5.0
        if ctx.flag("size_8_complete"): return 1.0
        if ctx.text("size_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def size_rule_9(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("size_score",0.0)
        if ctx.flag("size_blocked"): return -5.0
        if ctx.flag("size_9_complete"): return 2.0
        if ctx.text("size_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def size_rule_10(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("size_score",0.0)
        if ctx.flag("size_blocked"): return -5.0
        if ctx.flag("size_10_complete"): return 3.0
        if ctx.text("size_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def size_rule_11(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("size_score",0.0)
        if ctx.flag("size_blocked"): return -5.0
        if ctx.flag("size_11_complete"): return 4.0
        if ctx.text("size_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def size_rule_12(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("size_score",0.0)
        if ctx.flag("size_blocked"): return -5.0
        if ctx.flag("size_12_complete"): return 1.0
        if ctx.text("size_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def size_rule_13(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("size_score",0.0)
        if ctx.flag("size_blocked"): return -5.0
        if ctx.flag("size_13_complete"): return 2.0
        if ctx.text("size_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def size_rule_14(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("size_score",0.0)
        if ctx.flag("size_blocked"): return -5.0
        if ctx.flag("size_14_complete"): return 3.0
        if ctx.text("size_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def location_rule_1(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_1_complete"): return 2.0
        if ctx.text("location_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def location_rule_2(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_2_complete"): return 3.0
        if ctx.text("location_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def location_rule_3(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_3_complete"): return 4.0
        if ctx.text("location_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def location_rule_4(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_4_complete"): return 1.0
        if ctx.text("location_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def location_rule_5(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_5_complete"): return 2.0
        if ctx.text("location_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def location_rule_6(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_6_complete"): return 3.0
        if ctx.text("location_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def location_rule_7(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_7_complete"): return 4.0
        if ctx.text("location_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def location_rule_8(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_8_complete"): return 1.0
        if ctx.text("location_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def location_rule_9(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_9_complete"): return 2.0
        if ctx.text("location_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def location_rule_10(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_10_complete"): return 3.0
        if ctx.text("location_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def location_rule_11(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_11_complete"): return 4.0
        if ctx.text("location_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def location_rule_12(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_12_complete"): return 1.0
        if ctx.text("location_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def location_rule_13(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_13_complete"): return 2.0
        if ctx.text("location_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def location_rule_14(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_14_complete"): return 3.0
        if ctx.text("location_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def culture_rule_1(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("culture_score",0.0)
        if ctx.flag("culture_blocked"): return -5.0
        if ctx.flag("culture_1_complete"): return 2.0
        if ctx.text("culture_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def culture_rule_2(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("culture_score",0.0)
        if ctx.flag("culture_blocked"): return -5.0
        if ctx.flag("culture_2_complete"): return 3.0
        if ctx.text("culture_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def culture_rule_3(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("culture_score",0.0)
        if ctx.flag("culture_blocked"): return -5.0
        if ctx.flag("culture_3_complete"): return 4.0
        if ctx.text("culture_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def culture_rule_4(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("culture_score",0.0)
        if ctx.flag("culture_blocked"): return -5.0
        if ctx.flag("culture_4_complete"): return 1.0
        if ctx.text("culture_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def culture_rule_5(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("culture_score",0.0)
        if ctx.flag("culture_blocked"): return -5.0
        if ctx.flag("culture_5_complete"): return 2.0
        if ctx.text("culture_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def culture_rule_6(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("culture_score",0.0)
        if ctx.flag("culture_blocked"): return -5.0
        if ctx.flag("culture_6_complete"): return 3.0
        if ctx.text("culture_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def culture_rule_7(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("culture_score",0.0)
        if ctx.flag("culture_blocked"): return -5.0
        if ctx.flag("culture_7_complete"): return 4.0
        if ctx.text("culture_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def culture_rule_8(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("culture_score",0.0)
        if ctx.flag("culture_blocked"): return -5.0
        if ctx.flag("culture_8_complete"): return 1.0
        if ctx.text("culture_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def culture_rule_9(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("culture_score",0.0)
        if ctx.flag("culture_blocked"): return -5.0
        if ctx.flag("culture_9_complete"): return 2.0
        if ctx.text("culture_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def culture_rule_10(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("culture_score",0.0)
        if ctx.flag("culture_blocked"): return -5.0
        if ctx.flag("culture_10_complete"): return 3.0
        if ctx.text("culture_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def culture_rule_11(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("culture_score",0.0)
        if ctx.flag("culture_blocked"): return -5.0
        if ctx.flag("culture_11_complete"): return 4.0
        if ctx.text("culture_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def culture_rule_12(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("culture_score",0.0)
        if ctx.flag("culture_blocked"): return -5.0
        if ctx.flag("culture_12_complete"): return 1.0
        if ctx.text("culture_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def culture_rule_13(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("culture_score",0.0)
        if ctx.flag("culture_blocked"): return -5.0
        if ctx.flag("culture_13_complete"): return 2.0
        if ctx.text("culture_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def culture_rule_14(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("culture_score",0.0)
        if ctx.flag("culture_blocked"): return -5.0
        if ctx.flag("culture_14_complete"): return 3.0
        if ctx.text("culture_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def technology_rule_1(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("technology_score",0.0)
        if ctx.flag("technology_blocked"): return -5.0
        if ctx.flag("technology_1_complete"): return 2.0
        if ctx.text("technology_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def technology_rule_2(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("technology_score",0.0)
        if ctx.flag("technology_blocked"): return -5.0
        if ctx.flag("technology_2_complete"): return 3.0
        if ctx.text("technology_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def technology_rule_3(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("technology_score",0.0)
        if ctx.flag("technology_blocked"): return -5.0
        if ctx.flag("technology_3_complete"): return 4.0
        if ctx.text("technology_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def technology_rule_4(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("technology_score",0.0)
        if ctx.flag("technology_blocked"): return -5.0
        if ctx.flag("technology_4_complete"): return 1.0
        if ctx.text("technology_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def technology_rule_5(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("technology_score",0.0)
        if ctx.flag("technology_blocked"): return -5.0
        if ctx.flag("technology_5_complete"): return 2.0
        if ctx.text("technology_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def technology_rule_6(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("technology_score",0.0)
        if ctx.flag("technology_blocked"): return -5.0
        if ctx.flag("technology_6_complete"): return 3.0
        if ctx.text("technology_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def technology_rule_7(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("technology_score",0.0)
        if ctx.flag("technology_blocked"): return -5.0
        if ctx.flag("technology_7_complete"): return 4.0
        if ctx.text("technology_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def technology_rule_8(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("technology_score",0.0)
        if ctx.flag("technology_blocked"): return -5.0
        if ctx.flag("technology_8_complete"): return 1.0
        if ctx.text("technology_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def technology_rule_9(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("technology_score",0.0)
        if ctx.flag("technology_blocked"): return -5.0
        if ctx.flag("technology_9_complete"): return 2.0
        if ctx.text("technology_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def technology_rule_10(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("technology_score",0.0)
        if ctx.flag("technology_blocked"): return -5.0
        if ctx.flag("technology_10_complete"): return 3.0
        if ctx.text("technology_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def technology_rule_11(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("technology_score",0.0)
        if ctx.flag("technology_blocked"): return -5.0
        if ctx.flag("technology_11_complete"): return 4.0
        if ctx.text("technology_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def technology_rule_12(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("technology_score",0.0)
        if ctx.flag("technology_blocked"): return -5.0
        if ctx.flag("technology_12_complete"): return 1.0
        if ctx.text("technology_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def technology_rule_13(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("technology_score",0.0)
        if ctx.flag("technology_blocked"): return -5.0
        if ctx.flag("technology_13_complete"): return 2.0
        if ctx.text("technology_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def technology_rule_14(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("technology_score",0.0)
        if ctx.flag("technology_blocked"): return -5.0
        if ctx.flag("technology_14_complete"): return 3.0
        if ctx.text("technology_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def leadership_rule_1(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("leadership_score",0.0)
        if ctx.flag("leadership_blocked"): return -5.0
        if ctx.flag("leadership_1_complete"): return 2.0
        if ctx.text("leadership_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def leadership_rule_2(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("leadership_score",0.0)
        if ctx.flag("leadership_blocked"): return -5.0
        if ctx.flag("leadership_2_complete"): return 3.0
        if ctx.text("leadership_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def leadership_rule_3(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("leadership_score",0.0)
        if ctx.flag("leadership_blocked"): return -5.0
        if ctx.flag("leadership_3_complete"): return 4.0
        if ctx.text("leadership_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def leadership_rule_4(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("leadership_score",0.0)
        if ctx.flag("leadership_blocked"): return -5.0
        if ctx.flag("leadership_4_complete"): return 1.0
        if ctx.text("leadership_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def leadership_rule_5(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("leadership_score",0.0)
        if ctx.flag("leadership_blocked"): return -5.0
        if ctx.flag("leadership_5_complete"): return 2.0
        if ctx.text("leadership_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def leadership_rule_6(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("leadership_score",0.0)
        if ctx.flag("leadership_blocked"): return -5.0
        if ctx.flag("leadership_6_complete"): return 3.0
        if ctx.text("leadership_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def leadership_rule_7(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("leadership_score",0.0)
        if ctx.flag("leadership_blocked"): return -5.0
        if ctx.flag("leadership_7_complete"): return 4.0
        if ctx.text("leadership_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def leadership_rule_8(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("leadership_score",0.0)
        if ctx.flag("leadership_blocked"): return -5.0
        if ctx.flag("leadership_8_complete"): return 1.0
        if ctx.text("leadership_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def leadership_rule_9(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("leadership_score",0.0)
        if ctx.flag("leadership_blocked"): return -5.0
        if ctx.flag("leadership_9_complete"): return 2.0
        if ctx.text("leadership_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def leadership_rule_10(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("leadership_score",0.0)
        if ctx.flag("leadership_blocked"): return -5.0
        if ctx.flag("leadership_10_complete"): return 3.0
        if ctx.text("leadership_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def leadership_rule_11(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("leadership_score",0.0)
        if ctx.flag("leadership_blocked"): return -5.0
        if ctx.flag("leadership_11_complete"): return 4.0
        if ctx.text("leadership_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def leadership_rule_12(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("leadership_score",0.0)
        if ctx.flag("leadership_blocked"): return -5.0
        if ctx.flag("leadership_12_complete"): return 1.0
        if ctx.text("leadership_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def leadership_rule_13(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("leadership_score",0.0)
        if ctx.flag("leadership_blocked"): return -5.0
        if ctx.flag("leadership_13_complete"): return 2.0
        if ctx.text("leadership_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def leadership_rule_14(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("leadership_score",0.0)
        if ctx.flag("leadership_blocked"): return -5.0
        if ctx.flag("leadership_14_complete"): return 3.0
        if ctx.text("leadership_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def growth_rule_1(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("growth_score",0.0)
        if ctx.flag("growth_blocked"): return -5.0
        if ctx.flag("growth_1_complete"): return 2.0
        if ctx.text("growth_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def growth_rule_2(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("growth_score",0.0)
        if ctx.flag("growth_blocked"): return -5.0
        if ctx.flag("growth_2_complete"): return 3.0
        if ctx.text("growth_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def growth_rule_3(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("growth_score",0.0)
        if ctx.flag("growth_blocked"): return -5.0
        if ctx.flag("growth_3_complete"): return 4.0
        if ctx.text("growth_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def growth_rule_4(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("growth_score",0.0)
        if ctx.flag("growth_blocked"): return -5.0
        if ctx.flag("growth_4_complete"): return 1.0
        if ctx.text("growth_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def growth_rule_5(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("growth_score",0.0)
        if ctx.flag("growth_blocked"): return -5.0
        if ctx.flag("growth_5_complete"): return 2.0
        if ctx.text("growth_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def growth_rule_6(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("growth_score",0.0)
        if ctx.flag("growth_blocked"): return -5.0
        if ctx.flag("growth_6_complete"): return 3.0
        if ctx.text("growth_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def growth_rule_7(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("growth_score",0.0)
        if ctx.flag("growth_blocked"): return -5.0
        if ctx.flag("growth_7_complete"): return 4.0
        if ctx.text("growth_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def growth_rule_8(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("growth_score",0.0)
        if ctx.flag("growth_blocked"): return -5.0
        if ctx.flag("growth_8_complete"): return 1.0
        if ctx.text("growth_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def growth_rule_9(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("growth_score",0.0)
        if ctx.flag("growth_blocked"): return -5.0
        if ctx.flag("growth_9_complete"): return 2.0
        if ctx.text("growth_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def growth_rule_10(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("growth_score",0.0)
        if ctx.flag("growth_blocked"): return -5.0
        if ctx.flag("growth_10_complete"): return 3.0
        if ctx.text("growth_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def growth_rule_11(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("growth_score",0.0)
        if ctx.flag("growth_blocked"): return -5.0
        if ctx.flag("growth_11_complete"): return 4.0
        if ctx.text("growth_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def growth_rule_12(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("growth_score",0.0)
        if ctx.flag("growth_blocked"): return -5.0
        if ctx.flag("growth_12_complete"): return 1.0
        if ctx.text("growth_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def growth_rule_13(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("growth_score",0.0)
        if ctx.flag("growth_blocked"): return -5.0
        if ctx.flag("growth_13_complete"): return 2.0
        if ctx.text("growth_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def growth_rule_14(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("growth_score",0.0)
        if ctx.flag("growth_blocked"): return -5.0
        if ctx.flag("growth_14_complete"): return 3.0
        if ctx.text("growth_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def stability_rule_1(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("stability_score",0.0)
        if ctx.flag("stability_blocked"): return -5.0
        if ctx.flag("stability_1_complete"): return 2.0
        if ctx.text("stability_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def stability_rule_2(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("stability_score",0.0)
        if ctx.flag("stability_blocked"): return -5.0
        if ctx.flag("stability_2_complete"): return 3.0
        if ctx.text("stability_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def stability_rule_3(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("stability_score",0.0)
        if ctx.flag("stability_blocked"): return -5.0
        if ctx.flag("stability_3_complete"): return 4.0
        if ctx.text("stability_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def stability_rule_4(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("stability_score",0.0)
        if ctx.flag("stability_blocked"): return -5.0
        if ctx.flag("stability_4_complete"): return 1.0
        if ctx.text("stability_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def stability_rule_5(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("stability_score",0.0)
        if ctx.flag("stability_blocked"): return -5.0
        if ctx.flag("stability_5_complete"): return 2.0
        if ctx.text("stability_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def stability_rule_6(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("stability_score",0.0)
        if ctx.flag("stability_blocked"): return -5.0
        if ctx.flag("stability_6_complete"): return 3.0
        if ctx.text("stability_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def stability_rule_7(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("stability_score",0.0)
        if ctx.flag("stability_blocked"): return -5.0
        if ctx.flag("stability_7_complete"): return 4.0
        if ctx.text("stability_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def stability_rule_8(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("stability_score",0.0)
        if ctx.flag("stability_blocked"): return -5.0
        if ctx.flag("stability_8_complete"): return 1.0
        if ctx.text("stability_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def stability_rule_9(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("stability_score",0.0)
        if ctx.flag("stability_blocked"): return -5.0
        if ctx.flag("stability_9_complete"): return 2.0
        if ctx.text("stability_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def stability_rule_10(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("stability_score",0.0)
        if ctx.flag("stability_blocked"): return -5.0
        if ctx.flag("stability_10_complete"): return 3.0
        if ctx.text("stability_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def stability_rule_11(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("stability_score",0.0)
        if ctx.flag("stability_blocked"): return -5.0
        if ctx.flag("stability_11_complete"): return 4.0
        if ctx.text("stability_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def stability_rule_12(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("stability_score",0.0)
        if ctx.flag("stability_blocked"): return -5.0
        if ctx.flag("stability_12_complete"): return 1.0
        if ctx.text("stability_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def stability_rule_13(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("stability_score",0.0)
        if ctx.flag("stability_blocked"): return -5.0
        if ctx.flag("stability_13_complete"): return 2.0
        if ctx.text("stability_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def stability_rule_14(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("stability_score",0.0)
        if ctx.flag("stability_blocked"): return -5.0
        if ctx.flag("stability_14_complete"): return 3.0
        if ctx.text("stability_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def role_rule_1(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_1_complete"): return 2.0
        if ctx.text("role_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def role_rule_2(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_2_complete"): return 3.0
        if ctx.text("role_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def role_rule_3(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_3_complete"): return 4.0
        if ctx.text("role_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def role_rule_4(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_4_complete"): return 1.0
        if ctx.text("role_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def role_rule_5(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_5_complete"): return 2.0
        if ctx.text("role_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def role_rule_6(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_6_complete"): return 3.0
        if ctx.text("role_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def role_rule_7(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_7_complete"): return 4.0
        if ctx.text("role_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def role_rule_8(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_8_complete"): return 1.0
        if ctx.text("role_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def role_rule_9(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_9_complete"): return 2.0
        if ctx.text("role_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def role_rule_10(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_10_complete"): return 3.0
        if ctx.text("role_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def role_rule_11(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_11_complete"): return 4.0
        if ctx.text("role_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def role_rule_12(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_12_complete"): return 1.0
        if ctx.text("role_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def role_rule_13(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_13_complete"): return 2.0
        if ctx.text("role_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def role_rule_14(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_14_complete"): return 3.0
        if ctx.text("role_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def news_rule_1(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("news_score",0.0)
        if ctx.flag("news_blocked"): return -5.0
        if ctx.flag("news_1_complete"): return 2.0
        if ctx.text("news_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def news_rule_2(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("news_score",0.0)
        if ctx.flag("news_blocked"): return -5.0
        if ctx.flag("news_2_complete"): return 3.0
        if ctx.text("news_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def news_rule_3(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("news_score",0.0)
        if ctx.flag("news_blocked"): return -5.0
        if ctx.flag("news_3_complete"): return 4.0
        if ctx.text("news_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def news_rule_4(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("news_score",0.0)
        if ctx.flag("news_blocked"): return -5.0
        if ctx.flag("news_4_complete"): return 1.0
        if ctx.text("news_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def news_rule_5(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("news_score",0.0)
        if ctx.flag("news_blocked"): return -5.0
        if ctx.flag("news_5_complete"): return 2.0
        if ctx.text("news_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def news_rule_6(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("news_score",0.0)
        if ctx.flag("news_blocked"): return -5.0
        if ctx.flag("news_6_complete"): return 3.0
        if ctx.text("news_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def news_rule_7(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("news_score",0.0)
        if ctx.flag("news_blocked"): return -5.0
        if ctx.flag("news_7_complete"): return 4.0
        if ctx.text("news_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def news_rule_8(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("news_score",0.0)
        if ctx.flag("news_blocked"): return -5.0
        if ctx.flag("news_8_complete"): return 1.0
        if ctx.text("news_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def news_rule_9(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("news_score",0.0)
        if ctx.flag("news_blocked"): return -5.0
        if ctx.flag("news_9_complete"): return 2.0
        if ctx.text("news_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def news_rule_10(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("news_score",0.0)
        if ctx.flag("news_blocked"): return -5.0
        if ctx.flag("news_10_complete"): return 3.0
        if ctx.text("news_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def news_rule_11(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("news_score",0.0)
        if ctx.flag("news_blocked"): return -5.0
        if ctx.flag("news_11_complete"): return 4.0
        if ctx.text("news_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def news_rule_12(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("news_score",0.0)
        if ctx.flag("news_blocked"): return -5.0
        if ctx.flag("news_12_complete"): return 1.0
        if ctx.text("news_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def news_rule_13(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("news_score",0.0)
        if ctx.flag("news_blocked"): return -5.0
        if ctx.flag("news_13_complete"): return 2.0
        if ctx.text("news_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def news_rule_14(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("news_score",0.0)
        if ctx.flag("news_blocked"): return -5.0
        if ctx.flag("news_14_complete"): return 3.0
        if ctx.text("news_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def questions_rule_1(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("questions_score",0.0)
        if ctx.flag("questions_blocked"): return -5.0
        if ctx.flag("questions_1_complete"): return 2.0
        if ctx.text("questions_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def questions_rule_2(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("questions_score",0.0)
        if ctx.flag("questions_blocked"): return -5.0
        if ctx.flag("questions_2_complete"): return 3.0
        if ctx.text("questions_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def questions_rule_3(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("questions_score",0.0)
        if ctx.flag("questions_blocked"): return -5.0
        if ctx.flag("questions_3_complete"): return 4.0
        if ctx.text("questions_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def questions_rule_4(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("questions_score",0.0)
        if ctx.flag("questions_blocked"): return -5.0
        if ctx.flag("questions_4_complete"): return 1.0
        if ctx.text("questions_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def questions_rule_5(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("questions_score",0.0)
        if ctx.flag("questions_blocked"): return -5.0
        if ctx.flag("questions_5_complete"): return 2.0
        if ctx.text("questions_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def questions_rule_6(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("questions_score",0.0)
        if ctx.flag("questions_blocked"): return -5.0
        if ctx.flag("questions_6_complete"): return 3.0
        if ctx.text("questions_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def questions_rule_7(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("questions_score",0.0)
        if ctx.flag("questions_blocked"): return -5.0
        if ctx.flag("questions_7_complete"): return 4.0
        if ctx.text("questions_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def questions_rule_8(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("questions_score",0.0)
        if ctx.flag("questions_blocked"): return -5.0
        if ctx.flag("questions_8_complete"): return 1.0
        if ctx.text("questions_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def questions_rule_9(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("questions_score",0.0)
        if ctx.flag("questions_blocked"): return -5.0
        if ctx.flag("questions_9_complete"): return 2.0
        if ctx.text("questions_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def questions_rule_10(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("questions_score",0.0)
        if ctx.flag("questions_blocked"): return -5.0
        if ctx.flag("questions_10_complete"): return 3.0
        if ctx.text("questions_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def questions_rule_11(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("questions_score",0.0)
        if ctx.flag("questions_blocked"): return -5.0
        if ctx.flag("questions_11_complete"): return 4.0
        if ctx.text("questions_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def questions_rule_12(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("questions_score",0.0)
        if ctx.flag("questions_blocked"): return -5.0
        if ctx.flag("questions_12_complete"): return 1.0
        if ctx.text("questions_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def questions_rule_13(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("questions_score",0.0)
        if ctx.flag("questions_blocked"): return -5.0
        if ctx.flag("questions_13_complete"): return 2.0
        if ctx.text("questions_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def questions_rule_14(self,ctx:CompanyResearchContext)->float:
        value=ctx.number("questions_score",0.0)
        if ctx.flag("questions_blocked"): return -5.0
        if ctx.flag("questions_14_complete"): return 3.0
        if ctx.text("questions_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def evaluate_many(self,records:Sequence[Mapping[str,object]])->list[CompanyResearchResult]:
        return [self.evaluate(record) for record in records]
    def summarize(self,results:Sequence[CompanyResearchResult])->dict[str,object]:
        scores=[item.score for item in results]
        return {"count":len(scores),"average":round(sum(scores)/len(scores),2) if scores else 0.0,"strong":sum(x.status=="strong" for x in results),"acceptable":sum(x.status=="acceptable" for x in results),"review":sum(x.status=="review" for x in results)}
