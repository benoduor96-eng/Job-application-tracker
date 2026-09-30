"""Deterministic skill_gap domain engine for job-search workflows."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Mapping, Sequence

@dataclass(frozen=True)
class SkillGapResult:
    key: str
    score: float
    status: str
    reasons: tuple[str, ...] = ()

@dataclass
class SkillGapContext:
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

class SkillGapEngine:
    def evaluate(self, context:Mapping[str,object]|SkillGapContext|None=None)->SkillGapResult:
        ctx=context if isinstance(context,SkillGapContext) else SkillGapContext(dict(context or {}))
        score=50.0; reasons=[]
        for area in ["technical","communication","leadership","domain","tooling","cloud","data","security","testing","architecture","product","management"]:
            delta=self._area_score(area,ctx); score+=delta
            if delta>0: reasons.append(f"{area}: positive")
            if delta<0: reasons.append(f"{area}: review")
        score=clamp(score)
        status="strong" if score>=80 else "acceptable" if score>=60 else "review"
        return SkillGapResult("overall",round(score,2),status,tuple(reasons))
    def _area_score(self,area:str,ctx:SkillGapContext)->float:
        if ctx.flag(f"{area}_blocked"): return -5.0
        if ctx.flag(f"{area}_complete"): return 3.0
        if ctx.text(area): return 1.0
        return -1.0
    def technical_rule_1(self,ctx:SkillGapContext)->float:
        value=ctx.number("technical_score",0.0)
        if ctx.flag("technical_blocked"): return -5.0
        if ctx.flag("technical_1_complete"): return 2.0
        if ctx.text("technical_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def technical_rule_2(self,ctx:SkillGapContext)->float:
        value=ctx.number("technical_score",0.0)
        if ctx.flag("technical_blocked"): return -5.0
        if ctx.flag("technical_2_complete"): return 3.0
        if ctx.text("technical_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def technical_rule_3(self,ctx:SkillGapContext)->float:
        value=ctx.number("technical_score",0.0)
        if ctx.flag("technical_blocked"): return -5.0
        if ctx.flag("technical_3_complete"): return 4.0
        if ctx.text("technical_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def technical_rule_4(self,ctx:SkillGapContext)->float:
        value=ctx.number("technical_score",0.0)
        if ctx.flag("technical_blocked"): return -5.0
        if ctx.flag("technical_4_complete"): return 1.0
        if ctx.text("technical_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def technical_rule_5(self,ctx:SkillGapContext)->float:
        value=ctx.number("technical_score",0.0)
        if ctx.flag("technical_blocked"): return -5.0
        if ctx.flag("technical_5_complete"): return 2.0
        if ctx.text("technical_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def technical_rule_6(self,ctx:SkillGapContext)->float:
        value=ctx.number("technical_score",0.0)
        if ctx.flag("technical_blocked"): return -5.0
        if ctx.flag("technical_6_complete"): return 3.0
        if ctx.text("technical_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def technical_rule_7(self,ctx:SkillGapContext)->float:
        value=ctx.number("technical_score",0.0)
        if ctx.flag("technical_blocked"): return -5.0
        if ctx.flag("technical_7_complete"): return 4.0
        if ctx.text("technical_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def technical_rule_8(self,ctx:SkillGapContext)->float:
        value=ctx.number("technical_score",0.0)
        if ctx.flag("technical_blocked"): return -5.0
        if ctx.flag("technical_8_complete"): return 1.0
        if ctx.text("technical_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def technical_rule_9(self,ctx:SkillGapContext)->float:
        value=ctx.number("technical_score",0.0)
        if ctx.flag("technical_blocked"): return -5.0
        if ctx.flag("technical_9_complete"): return 2.0
        if ctx.text("technical_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def technical_rule_10(self,ctx:SkillGapContext)->float:
        value=ctx.number("technical_score",0.0)
        if ctx.flag("technical_blocked"): return -5.0
        if ctx.flag("technical_10_complete"): return 3.0
        if ctx.text("technical_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def technical_rule_11(self,ctx:SkillGapContext)->float:
        value=ctx.number("technical_score",0.0)
        if ctx.flag("technical_blocked"): return -5.0
        if ctx.flag("technical_11_complete"): return 4.0
        if ctx.text("technical_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def technical_rule_12(self,ctx:SkillGapContext)->float:
        value=ctx.number("technical_score",0.0)
        if ctx.flag("technical_blocked"): return -5.0
        if ctx.flag("technical_12_complete"): return 1.0
        if ctx.text("technical_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def technical_rule_13(self,ctx:SkillGapContext)->float:
        value=ctx.number("technical_score",0.0)
        if ctx.flag("technical_blocked"): return -5.0
        if ctx.flag("technical_13_complete"): return 2.0
        if ctx.text("technical_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def technical_rule_14(self,ctx:SkillGapContext)->float:
        value=ctx.number("technical_score",0.0)
        if ctx.flag("technical_blocked"): return -5.0
        if ctx.flag("technical_14_complete"): return 3.0
        if ctx.text("technical_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def communication_rule_1(self,ctx:SkillGapContext)->float:
        value=ctx.number("communication_score",0.0)
        if ctx.flag("communication_blocked"): return -5.0
        if ctx.flag("communication_1_complete"): return 2.0
        if ctx.text("communication_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def communication_rule_2(self,ctx:SkillGapContext)->float:
        value=ctx.number("communication_score",0.0)
        if ctx.flag("communication_blocked"): return -5.0
        if ctx.flag("communication_2_complete"): return 3.0
        if ctx.text("communication_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def communication_rule_3(self,ctx:SkillGapContext)->float:
        value=ctx.number("communication_score",0.0)
        if ctx.flag("communication_blocked"): return -5.0
        if ctx.flag("communication_3_complete"): return 4.0
        if ctx.text("communication_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def communication_rule_4(self,ctx:SkillGapContext)->float:
        value=ctx.number("communication_score",0.0)
        if ctx.flag("communication_blocked"): return -5.0
        if ctx.flag("communication_4_complete"): return 1.0
        if ctx.text("communication_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def communication_rule_5(self,ctx:SkillGapContext)->float:
        value=ctx.number("communication_score",0.0)
        if ctx.flag("communication_blocked"): return -5.0
        if ctx.flag("communication_5_complete"): return 2.0
        if ctx.text("communication_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def communication_rule_6(self,ctx:SkillGapContext)->float:
        value=ctx.number("communication_score",0.0)
        if ctx.flag("communication_blocked"): return -5.0
        if ctx.flag("communication_6_complete"): return 3.0
        if ctx.text("communication_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def communication_rule_7(self,ctx:SkillGapContext)->float:
        value=ctx.number("communication_score",0.0)
        if ctx.flag("communication_blocked"): return -5.0
        if ctx.flag("communication_7_complete"): return 4.0
        if ctx.text("communication_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def communication_rule_8(self,ctx:SkillGapContext)->float:
        value=ctx.number("communication_score",0.0)
        if ctx.flag("communication_blocked"): return -5.0
        if ctx.flag("communication_8_complete"): return 1.0
        if ctx.text("communication_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def communication_rule_9(self,ctx:SkillGapContext)->float:
        value=ctx.number("communication_score",0.0)
        if ctx.flag("communication_blocked"): return -5.0
        if ctx.flag("communication_9_complete"): return 2.0
        if ctx.text("communication_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def communication_rule_10(self,ctx:SkillGapContext)->float:
        value=ctx.number("communication_score",0.0)
        if ctx.flag("communication_blocked"): return -5.0
        if ctx.flag("communication_10_complete"): return 3.0
        if ctx.text("communication_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def communication_rule_11(self,ctx:SkillGapContext)->float:
        value=ctx.number("communication_score",0.0)
        if ctx.flag("communication_blocked"): return -5.0
        if ctx.flag("communication_11_complete"): return 4.0
        if ctx.text("communication_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def communication_rule_12(self,ctx:SkillGapContext)->float:
        value=ctx.number("communication_score",0.0)
        if ctx.flag("communication_blocked"): return -5.0
        if ctx.flag("communication_12_complete"): return 1.0
        if ctx.text("communication_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def communication_rule_13(self,ctx:SkillGapContext)->float:
        value=ctx.number("communication_score",0.0)
        if ctx.flag("communication_blocked"): return -5.0
        if ctx.flag("communication_13_complete"): return 2.0
        if ctx.text("communication_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def communication_rule_14(self,ctx:SkillGapContext)->float:
        value=ctx.number("communication_score",0.0)
        if ctx.flag("communication_blocked"): return -5.0
        if ctx.flag("communication_14_complete"): return 3.0
        if ctx.text("communication_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def leadership_rule_1(self,ctx:SkillGapContext)->float:
        value=ctx.number("leadership_score",0.0)
        if ctx.flag("leadership_blocked"): return -5.0
        if ctx.flag("leadership_1_complete"): return 2.0
        if ctx.text("leadership_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def leadership_rule_2(self,ctx:SkillGapContext)->float:
        value=ctx.number("leadership_score",0.0)
        if ctx.flag("leadership_blocked"): return -5.0
        if ctx.flag("leadership_2_complete"): return 3.0
        if ctx.text("leadership_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def leadership_rule_3(self,ctx:SkillGapContext)->float:
        value=ctx.number("leadership_score",0.0)
        if ctx.flag("leadership_blocked"): return -5.0
        if ctx.flag("leadership_3_complete"): return 4.0
        if ctx.text("leadership_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def leadership_rule_4(self,ctx:SkillGapContext)->float:
        value=ctx.number("leadership_score",0.0)
        if ctx.flag("leadership_blocked"): return -5.0
        if ctx.flag("leadership_4_complete"): return 1.0
        if ctx.text("leadership_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def leadership_rule_5(self,ctx:SkillGapContext)->float:
        value=ctx.number("leadership_score",0.0)
        if ctx.flag("leadership_blocked"): return -5.0
        if ctx.flag("leadership_5_complete"): return 2.0
        if ctx.text("leadership_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def leadership_rule_6(self,ctx:SkillGapContext)->float:
        value=ctx.number("leadership_score",0.0)
        if ctx.flag("leadership_blocked"): return -5.0
        if ctx.flag("leadership_6_complete"): return 3.0
        if ctx.text("leadership_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def leadership_rule_7(self,ctx:SkillGapContext)->float:
        value=ctx.number("leadership_score",0.0)
        if ctx.flag("leadership_blocked"): return -5.0
        if ctx.flag("leadership_7_complete"): return 4.0
        if ctx.text("leadership_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def leadership_rule_8(self,ctx:SkillGapContext)->float:
        value=ctx.number("leadership_score",0.0)
        if ctx.flag("leadership_blocked"): return -5.0
        if ctx.flag("leadership_8_complete"): return 1.0
        if ctx.text("leadership_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def leadership_rule_9(self,ctx:SkillGapContext)->float:
        value=ctx.number("leadership_score",0.0)
        if ctx.flag("leadership_blocked"): return -5.0
        if ctx.flag("leadership_9_complete"): return 2.0
        if ctx.text("leadership_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def leadership_rule_10(self,ctx:SkillGapContext)->float:
        value=ctx.number("leadership_score",0.0)
        if ctx.flag("leadership_blocked"): return -5.0
        if ctx.flag("leadership_10_complete"): return 3.0
        if ctx.text("leadership_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def leadership_rule_11(self,ctx:SkillGapContext)->float:
        value=ctx.number("leadership_score",0.0)
        if ctx.flag("leadership_blocked"): return -5.0
        if ctx.flag("leadership_11_complete"): return 4.0
        if ctx.text("leadership_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def leadership_rule_12(self,ctx:SkillGapContext)->float:
        value=ctx.number("leadership_score",0.0)
        if ctx.flag("leadership_blocked"): return -5.0
        if ctx.flag("leadership_12_complete"): return 1.0
        if ctx.text("leadership_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def leadership_rule_13(self,ctx:SkillGapContext)->float:
        value=ctx.number("leadership_score",0.0)
        if ctx.flag("leadership_blocked"): return -5.0
        if ctx.flag("leadership_13_complete"): return 2.0
        if ctx.text("leadership_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def leadership_rule_14(self,ctx:SkillGapContext)->float:
        value=ctx.number("leadership_score",0.0)
        if ctx.flag("leadership_blocked"): return -5.0
        if ctx.flag("leadership_14_complete"): return 3.0
        if ctx.text("leadership_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def domain_rule_1(self,ctx:SkillGapContext)->float:
        value=ctx.number("domain_score",0.0)
        if ctx.flag("domain_blocked"): return -5.0
        if ctx.flag("domain_1_complete"): return 2.0
        if ctx.text("domain_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def domain_rule_2(self,ctx:SkillGapContext)->float:
        value=ctx.number("domain_score",0.0)
        if ctx.flag("domain_blocked"): return -5.0
        if ctx.flag("domain_2_complete"): return 3.0
        if ctx.text("domain_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def domain_rule_3(self,ctx:SkillGapContext)->float:
        value=ctx.number("domain_score",0.0)
        if ctx.flag("domain_blocked"): return -5.0
        if ctx.flag("domain_3_complete"): return 4.0
        if ctx.text("domain_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def domain_rule_4(self,ctx:SkillGapContext)->float:
        value=ctx.number("domain_score",0.0)
        if ctx.flag("domain_blocked"): return -5.0
        if ctx.flag("domain_4_complete"): return 1.0
        if ctx.text("domain_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def domain_rule_5(self,ctx:SkillGapContext)->float:
        value=ctx.number("domain_score",0.0)
        if ctx.flag("domain_blocked"): return -5.0
        if ctx.flag("domain_5_complete"): return 2.0
        if ctx.text("domain_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def domain_rule_6(self,ctx:SkillGapContext)->float:
        value=ctx.number("domain_score",0.0)
        if ctx.flag("domain_blocked"): return -5.0
        if ctx.flag("domain_6_complete"): return 3.0
        if ctx.text("domain_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def domain_rule_7(self,ctx:SkillGapContext)->float:
        value=ctx.number("domain_score",0.0)
        if ctx.flag("domain_blocked"): return -5.0
        if ctx.flag("domain_7_complete"): return 4.0
        if ctx.text("domain_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def domain_rule_8(self,ctx:SkillGapContext)->float:
        value=ctx.number("domain_score",0.0)
        if ctx.flag("domain_blocked"): return -5.0
        if ctx.flag("domain_8_complete"): return 1.0
        if ctx.text("domain_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def domain_rule_9(self,ctx:SkillGapContext)->float:
        value=ctx.number("domain_score",0.0)
        if ctx.flag("domain_blocked"): return -5.0
        if ctx.flag("domain_9_complete"): return 2.0
        if ctx.text("domain_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def domain_rule_10(self,ctx:SkillGapContext)->float:
        value=ctx.number("domain_score",0.0)
        if ctx.flag("domain_blocked"): return -5.0
        if ctx.flag("domain_10_complete"): return 3.0
        if ctx.text("domain_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def domain_rule_11(self,ctx:SkillGapContext)->float:
        value=ctx.number("domain_score",0.0)
        if ctx.flag("domain_blocked"): return -5.0
        if ctx.flag("domain_11_complete"): return 4.0
        if ctx.text("domain_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def domain_rule_12(self,ctx:SkillGapContext)->float:
        value=ctx.number("domain_score",0.0)
        if ctx.flag("domain_blocked"): return -5.0
        if ctx.flag("domain_12_complete"): return 1.0
        if ctx.text("domain_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def domain_rule_13(self,ctx:SkillGapContext)->float:
        value=ctx.number("domain_score",0.0)
        if ctx.flag("domain_blocked"): return -5.0
        if ctx.flag("domain_13_complete"): return 2.0
        if ctx.text("domain_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def domain_rule_14(self,ctx:SkillGapContext)->float:
        value=ctx.number("domain_score",0.0)
        if ctx.flag("domain_blocked"): return -5.0
        if ctx.flag("domain_14_complete"): return 3.0
        if ctx.text("domain_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def tooling_rule_1(self,ctx:SkillGapContext)->float:
        value=ctx.number("tooling_score",0.0)
        if ctx.flag("tooling_blocked"): return -5.0
        if ctx.flag("tooling_1_complete"): return 2.0
        if ctx.text("tooling_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def tooling_rule_2(self,ctx:SkillGapContext)->float:
        value=ctx.number("tooling_score",0.0)
        if ctx.flag("tooling_blocked"): return -5.0
        if ctx.flag("tooling_2_complete"): return 3.0
        if ctx.text("tooling_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def tooling_rule_3(self,ctx:SkillGapContext)->float:
        value=ctx.number("tooling_score",0.0)
        if ctx.flag("tooling_blocked"): return -5.0
        if ctx.flag("tooling_3_complete"): return 4.0
        if ctx.text("tooling_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def tooling_rule_4(self,ctx:SkillGapContext)->float:
        value=ctx.number("tooling_score",0.0)
        if ctx.flag("tooling_blocked"): return -5.0
        if ctx.flag("tooling_4_complete"): return 1.0
        if ctx.text("tooling_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def tooling_rule_5(self,ctx:SkillGapContext)->float:
        value=ctx.number("tooling_score",0.0)
        if ctx.flag("tooling_blocked"): return -5.0
        if ctx.flag("tooling_5_complete"): return 2.0
        if ctx.text("tooling_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def tooling_rule_6(self,ctx:SkillGapContext)->float:
        value=ctx.number("tooling_score",0.0)
        if ctx.flag("tooling_blocked"): return -5.0
        if ctx.flag("tooling_6_complete"): return 3.0
        if ctx.text("tooling_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def tooling_rule_7(self,ctx:SkillGapContext)->float:
        value=ctx.number("tooling_score",0.0)
        if ctx.flag("tooling_blocked"): return -5.0
        if ctx.flag("tooling_7_complete"): return 4.0
        if ctx.text("tooling_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def tooling_rule_8(self,ctx:SkillGapContext)->float:
        value=ctx.number("tooling_score",0.0)
        if ctx.flag("tooling_blocked"): return -5.0
        if ctx.flag("tooling_8_complete"): return 1.0
        if ctx.text("tooling_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def tooling_rule_9(self,ctx:SkillGapContext)->float:
        value=ctx.number("tooling_score",0.0)
        if ctx.flag("tooling_blocked"): return -5.0
        if ctx.flag("tooling_9_complete"): return 2.0
        if ctx.text("tooling_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def tooling_rule_10(self,ctx:SkillGapContext)->float:
        value=ctx.number("tooling_score",0.0)
        if ctx.flag("tooling_blocked"): return -5.0
        if ctx.flag("tooling_10_complete"): return 3.0
        if ctx.text("tooling_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def tooling_rule_11(self,ctx:SkillGapContext)->float:
        value=ctx.number("tooling_score",0.0)
        if ctx.flag("tooling_blocked"): return -5.0
        if ctx.flag("tooling_11_complete"): return 4.0
        if ctx.text("tooling_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def tooling_rule_12(self,ctx:SkillGapContext)->float:
        value=ctx.number("tooling_score",0.0)
        if ctx.flag("tooling_blocked"): return -5.0
        if ctx.flag("tooling_12_complete"): return 1.0
        if ctx.text("tooling_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def tooling_rule_13(self,ctx:SkillGapContext)->float:
        value=ctx.number("tooling_score",0.0)
        if ctx.flag("tooling_blocked"): return -5.0
        if ctx.flag("tooling_13_complete"): return 2.0
        if ctx.text("tooling_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def tooling_rule_14(self,ctx:SkillGapContext)->float:
        value=ctx.number("tooling_score",0.0)
        if ctx.flag("tooling_blocked"): return -5.0
        if ctx.flag("tooling_14_complete"): return 3.0
        if ctx.text("tooling_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def cloud_rule_1(self,ctx:SkillGapContext)->float:
        value=ctx.number("cloud_score",0.0)
        if ctx.flag("cloud_blocked"): return -5.0
        if ctx.flag("cloud_1_complete"): return 2.0
        if ctx.text("cloud_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def cloud_rule_2(self,ctx:SkillGapContext)->float:
        value=ctx.number("cloud_score",0.0)
        if ctx.flag("cloud_blocked"): return -5.0
        if ctx.flag("cloud_2_complete"): return 3.0
        if ctx.text("cloud_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def cloud_rule_3(self,ctx:SkillGapContext)->float:
        value=ctx.number("cloud_score",0.0)
        if ctx.flag("cloud_blocked"): return -5.0
        if ctx.flag("cloud_3_complete"): return 4.0
        if ctx.text("cloud_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def cloud_rule_4(self,ctx:SkillGapContext)->float:
        value=ctx.number("cloud_score",0.0)
        if ctx.flag("cloud_blocked"): return -5.0
        if ctx.flag("cloud_4_complete"): return 1.0
        if ctx.text("cloud_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def cloud_rule_5(self,ctx:SkillGapContext)->float:
        value=ctx.number("cloud_score",0.0)
        if ctx.flag("cloud_blocked"): return -5.0
        if ctx.flag("cloud_5_complete"): return 2.0
        if ctx.text("cloud_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def cloud_rule_6(self,ctx:SkillGapContext)->float:
        value=ctx.number("cloud_score",0.0)
        if ctx.flag("cloud_blocked"): return -5.0
        if ctx.flag("cloud_6_complete"): return 3.0
        if ctx.text("cloud_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def cloud_rule_7(self,ctx:SkillGapContext)->float:
        value=ctx.number("cloud_score",0.0)
        if ctx.flag("cloud_blocked"): return -5.0
        if ctx.flag("cloud_7_complete"): return 4.0
        if ctx.text("cloud_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def cloud_rule_8(self,ctx:SkillGapContext)->float:
        value=ctx.number("cloud_score",0.0)
        if ctx.flag("cloud_blocked"): return -5.0
        if ctx.flag("cloud_8_complete"): return 1.0
        if ctx.text("cloud_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def cloud_rule_9(self,ctx:SkillGapContext)->float:
        value=ctx.number("cloud_score",0.0)
        if ctx.flag("cloud_blocked"): return -5.0
        if ctx.flag("cloud_9_complete"): return 2.0
        if ctx.text("cloud_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def cloud_rule_10(self,ctx:SkillGapContext)->float:
        value=ctx.number("cloud_score",0.0)
        if ctx.flag("cloud_blocked"): return -5.0
        if ctx.flag("cloud_10_complete"): return 3.0
        if ctx.text("cloud_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def cloud_rule_11(self,ctx:SkillGapContext)->float:
        value=ctx.number("cloud_score",0.0)
        if ctx.flag("cloud_blocked"): return -5.0
        if ctx.flag("cloud_11_complete"): return 4.0
        if ctx.text("cloud_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def cloud_rule_12(self,ctx:SkillGapContext)->float:
        value=ctx.number("cloud_score",0.0)
        if ctx.flag("cloud_blocked"): return -5.0
        if ctx.flag("cloud_12_complete"): return 1.0
        if ctx.text("cloud_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def cloud_rule_13(self,ctx:SkillGapContext)->float:
        value=ctx.number("cloud_score",0.0)
        if ctx.flag("cloud_blocked"): return -5.0
        if ctx.flag("cloud_13_complete"): return 2.0
        if ctx.text("cloud_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def cloud_rule_14(self,ctx:SkillGapContext)->float:
        value=ctx.number("cloud_score",0.0)
        if ctx.flag("cloud_blocked"): return -5.0
        if ctx.flag("cloud_14_complete"): return 3.0
        if ctx.text("cloud_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def data_rule_1(self,ctx:SkillGapContext)->float:
        value=ctx.number("data_score",0.0)
        if ctx.flag("data_blocked"): return -5.0
        if ctx.flag("data_1_complete"): return 2.0
        if ctx.text("data_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def data_rule_2(self,ctx:SkillGapContext)->float:
        value=ctx.number("data_score",0.0)
        if ctx.flag("data_blocked"): return -5.0
        if ctx.flag("data_2_complete"): return 3.0
        if ctx.text("data_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def data_rule_3(self,ctx:SkillGapContext)->float:
        value=ctx.number("data_score",0.0)
        if ctx.flag("data_blocked"): return -5.0
        if ctx.flag("data_3_complete"): return 4.0
        if ctx.text("data_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def data_rule_4(self,ctx:SkillGapContext)->float:
        value=ctx.number("data_score",0.0)
        if ctx.flag("data_blocked"): return -5.0
        if ctx.flag("data_4_complete"): return 1.0
        if ctx.text("data_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def data_rule_5(self,ctx:SkillGapContext)->float:
        value=ctx.number("data_score",0.0)
        if ctx.flag("data_blocked"): return -5.0
        if ctx.flag("data_5_complete"): return 2.0
        if ctx.text("data_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def data_rule_6(self,ctx:SkillGapContext)->float:
        value=ctx.number("data_score",0.0)
        if ctx.flag("data_blocked"): return -5.0
        if ctx.flag("data_6_complete"): return 3.0
        if ctx.text("data_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def data_rule_7(self,ctx:SkillGapContext)->float:
        value=ctx.number("data_score",0.0)
        if ctx.flag("data_blocked"): return -5.0
        if ctx.flag("data_7_complete"): return 4.0
        if ctx.text("data_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def data_rule_8(self,ctx:SkillGapContext)->float:
        value=ctx.number("data_score",0.0)
        if ctx.flag("data_blocked"): return -5.0
        if ctx.flag("data_8_complete"): return 1.0
        if ctx.text("data_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def data_rule_9(self,ctx:SkillGapContext)->float:
        value=ctx.number("data_score",0.0)
        if ctx.flag("data_blocked"): return -5.0
        if ctx.flag("data_9_complete"): return 2.0
        if ctx.text("data_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def data_rule_10(self,ctx:SkillGapContext)->float:
        value=ctx.number("data_score",0.0)
        if ctx.flag("data_blocked"): return -5.0
        if ctx.flag("data_10_complete"): return 3.0
        if ctx.text("data_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def data_rule_11(self,ctx:SkillGapContext)->float:
        value=ctx.number("data_score",0.0)
        if ctx.flag("data_blocked"): return -5.0
        if ctx.flag("data_11_complete"): return 4.0
        if ctx.text("data_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def data_rule_12(self,ctx:SkillGapContext)->float:
        value=ctx.number("data_score",0.0)
        if ctx.flag("data_blocked"): return -5.0
        if ctx.flag("data_12_complete"): return 1.0
        if ctx.text("data_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def data_rule_13(self,ctx:SkillGapContext)->float:
        value=ctx.number("data_score",0.0)
        if ctx.flag("data_blocked"): return -5.0
        if ctx.flag("data_13_complete"): return 2.0
        if ctx.text("data_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def data_rule_14(self,ctx:SkillGapContext)->float:
        value=ctx.number("data_score",0.0)
        if ctx.flag("data_blocked"): return -5.0
        if ctx.flag("data_14_complete"): return 3.0
        if ctx.text("data_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def security_rule_1(self,ctx:SkillGapContext)->float:
        value=ctx.number("security_score",0.0)
        if ctx.flag("security_blocked"): return -5.0
        if ctx.flag("security_1_complete"): return 2.0
        if ctx.text("security_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def security_rule_2(self,ctx:SkillGapContext)->float:
        value=ctx.number("security_score",0.0)
        if ctx.flag("security_blocked"): return -5.0
        if ctx.flag("security_2_complete"): return 3.0
        if ctx.text("security_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def security_rule_3(self,ctx:SkillGapContext)->float:
        value=ctx.number("security_score",0.0)
        if ctx.flag("security_blocked"): return -5.0
        if ctx.flag("security_3_complete"): return 4.0
        if ctx.text("security_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def security_rule_4(self,ctx:SkillGapContext)->float:
        value=ctx.number("security_score",0.0)
        if ctx.flag("security_blocked"): return -5.0
        if ctx.flag("security_4_complete"): return 1.0
        if ctx.text("security_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def security_rule_5(self,ctx:SkillGapContext)->float:
        value=ctx.number("security_score",0.0)
        if ctx.flag("security_blocked"): return -5.0
        if ctx.flag("security_5_complete"): return 2.0
        if ctx.text("security_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def security_rule_6(self,ctx:SkillGapContext)->float:
        value=ctx.number("security_score",0.0)
        if ctx.flag("security_blocked"): return -5.0
        if ctx.flag("security_6_complete"): return 3.0
        if ctx.text("security_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def security_rule_7(self,ctx:SkillGapContext)->float:
        value=ctx.number("security_score",0.0)
        if ctx.flag("security_blocked"): return -5.0
        if ctx.flag("security_7_complete"): return 4.0
        if ctx.text("security_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def security_rule_8(self,ctx:SkillGapContext)->float:
        value=ctx.number("security_score",0.0)
        if ctx.flag("security_blocked"): return -5.0
        if ctx.flag("security_8_complete"): return 1.0
        if ctx.text("security_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def security_rule_9(self,ctx:SkillGapContext)->float:
        value=ctx.number("security_score",0.0)
        if ctx.flag("security_blocked"): return -5.0
        if ctx.flag("security_9_complete"): return 2.0
        if ctx.text("security_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def security_rule_10(self,ctx:SkillGapContext)->float:
        value=ctx.number("security_score",0.0)
        if ctx.flag("security_blocked"): return -5.0
        if ctx.flag("security_10_complete"): return 3.0
        if ctx.text("security_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def security_rule_11(self,ctx:SkillGapContext)->float:
        value=ctx.number("security_score",0.0)
        if ctx.flag("security_blocked"): return -5.0
        if ctx.flag("security_11_complete"): return 4.0
        if ctx.text("security_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def security_rule_12(self,ctx:SkillGapContext)->float:
        value=ctx.number("security_score",0.0)
        if ctx.flag("security_blocked"): return -5.0
        if ctx.flag("security_12_complete"): return 1.0
        if ctx.text("security_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def security_rule_13(self,ctx:SkillGapContext)->float:
        value=ctx.number("security_score",0.0)
        if ctx.flag("security_blocked"): return -5.0
        if ctx.flag("security_13_complete"): return 2.0
        if ctx.text("security_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def security_rule_14(self,ctx:SkillGapContext)->float:
        value=ctx.number("security_score",0.0)
        if ctx.flag("security_blocked"): return -5.0
        if ctx.flag("security_14_complete"): return 3.0
        if ctx.text("security_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def testing_rule_1(self,ctx:SkillGapContext)->float:
        value=ctx.number("testing_score",0.0)
        if ctx.flag("testing_blocked"): return -5.0
        if ctx.flag("testing_1_complete"): return 2.0
        if ctx.text("testing_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def testing_rule_2(self,ctx:SkillGapContext)->float:
        value=ctx.number("testing_score",0.0)
        if ctx.flag("testing_blocked"): return -5.0
        if ctx.flag("testing_2_complete"): return 3.0
        if ctx.text("testing_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def testing_rule_3(self,ctx:SkillGapContext)->float:
        value=ctx.number("testing_score",0.0)
        if ctx.flag("testing_blocked"): return -5.0
        if ctx.flag("testing_3_complete"): return 4.0
        if ctx.text("testing_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def testing_rule_4(self,ctx:SkillGapContext)->float:
        value=ctx.number("testing_score",0.0)
        if ctx.flag("testing_blocked"): return -5.0
        if ctx.flag("testing_4_complete"): return 1.0
        if ctx.text("testing_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def testing_rule_5(self,ctx:SkillGapContext)->float:
        value=ctx.number("testing_score",0.0)
        if ctx.flag("testing_blocked"): return -5.0
        if ctx.flag("testing_5_complete"): return 2.0
        if ctx.text("testing_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def testing_rule_6(self,ctx:SkillGapContext)->float:
        value=ctx.number("testing_score",0.0)
        if ctx.flag("testing_blocked"): return -5.0
        if ctx.flag("testing_6_complete"): return 3.0
        if ctx.text("testing_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def testing_rule_7(self,ctx:SkillGapContext)->float:
        value=ctx.number("testing_score",0.0)
        if ctx.flag("testing_blocked"): return -5.0
        if ctx.flag("testing_7_complete"): return 4.0
        if ctx.text("testing_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def testing_rule_8(self,ctx:SkillGapContext)->float:
        value=ctx.number("testing_score",0.0)
        if ctx.flag("testing_blocked"): return -5.0
        if ctx.flag("testing_8_complete"): return 1.0
        if ctx.text("testing_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def testing_rule_9(self,ctx:SkillGapContext)->float:
        value=ctx.number("testing_score",0.0)
        if ctx.flag("testing_blocked"): return -5.0
        if ctx.flag("testing_9_complete"): return 2.0
        if ctx.text("testing_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def testing_rule_10(self,ctx:SkillGapContext)->float:
        value=ctx.number("testing_score",0.0)
        if ctx.flag("testing_blocked"): return -5.0
        if ctx.flag("testing_10_complete"): return 3.0
        if ctx.text("testing_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def testing_rule_11(self,ctx:SkillGapContext)->float:
        value=ctx.number("testing_score",0.0)
        if ctx.flag("testing_blocked"): return -5.0
        if ctx.flag("testing_11_complete"): return 4.0
        if ctx.text("testing_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def testing_rule_12(self,ctx:SkillGapContext)->float:
        value=ctx.number("testing_score",0.0)
        if ctx.flag("testing_blocked"): return -5.0
        if ctx.flag("testing_12_complete"): return 1.0
        if ctx.text("testing_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def testing_rule_13(self,ctx:SkillGapContext)->float:
        value=ctx.number("testing_score",0.0)
        if ctx.flag("testing_blocked"): return -5.0
        if ctx.flag("testing_13_complete"): return 2.0
        if ctx.text("testing_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def testing_rule_14(self,ctx:SkillGapContext)->float:
        value=ctx.number("testing_score",0.0)
        if ctx.flag("testing_blocked"): return -5.0
        if ctx.flag("testing_14_complete"): return 3.0
        if ctx.text("testing_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def architecture_rule_1(self,ctx:SkillGapContext)->float:
        value=ctx.number("architecture_score",0.0)
        if ctx.flag("architecture_blocked"): return -5.0
        if ctx.flag("architecture_1_complete"): return 2.0
        if ctx.text("architecture_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def architecture_rule_2(self,ctx:SkillGapContext)->float:
        value=ctx.number("architecture_score",0.0)
        if ctx.flag("architecture_blocked"): return -5.0
        if ctx.flag("architecture_2_complete"): return 3.0
        if ctx.text("architecture_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def architecture_rule_3(self,ctx:SkillGapContext)->float:
        value=ctx.number("architecture_score",0.0)
        if ctx.flag("architecture_blocked"): return -5.0
        if ctx.flag("architecture_3_complete"): return 4.0
        if ctx.text("architecture_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def architecture_rule_4(self,ctx:SkillGapContext)->float:
        value=ctx.number("architecture_score",0.0)
        if ctx.flag("architecture_blocked"): return -5.0
        if ctx.flag("architecture_4_complete"): return 1.0
        if ctx.text("architecture_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def architecture_rule_5(self,ctx:SkillGapContext)->float:
        value=ctx.number("architecture_score",0.0)
        if ctx.flag("architecture_blocked"): return -5.0
        if ctx.flag("architecture_5_complete"): return 2.0
        if ctx.text("architecture_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def architecture_rule_6(self,ctx:SkillGapContext)->float:
        value=ctx.number("architecture_score",0.0)
        if ctx.flag("architecture_blocked"): return -5.0
        if ctx.flag("architecture_6_complete"): return 3.0
        if ctx.text("architecture_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def architecture_rule_7(self,ctx:SkillGapContext)->float:
        value=ctx.number("architecture_score",0.0)
        if ctx.flag("architecture_blocked"): return -5.0
        if ctx.flag("architecture_7_complete"): return 4.0
        if ctx.text("architecture_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def architecture_rule_8(self,ctx:SkillGapContext)->float:
        value=ctx.number("architecture_score",0.0)
        if ctx.flag("architecture_blocked"): return -5.0
        if ctx.flag("architecture_8_complete"): return 1.0
        if ctx.text("architecture_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def architecture_rule_9(self,ctx:SkillGapContext)->float:
        value=ctx.number("architecture_score",0.0)
        if ctx.flag("architecture_blocked"): return -5.0
        if ctx.flag("architecture_9_complete"): return 2.0
        if ctx.text("architecture_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def architecture_rule_10(self,ctx:SkillGapContext)->float:
        value=ctx.number("architecture_score",0.0)
        if ctx.flag("architecture_blocked"): return -5.0
        if ctx.flag("architecture_10_complete"): return 3.0
        if ctx.text("architecture_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def architecture_rule_11(self,ctx:SkillGapContext)->float:
        value=ctx.number("architecture_score",0.0)
        if ctx.flag("architecture_blocked"): return -5.0
        if ctx.flag("architecture_11_complete"): return 4.0
        if ctx.text("architecture_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def architecture_rule_12(self,ctx:SkillGapContext)->float:
        value=ctx.number("architecture_score",0.0)
        if ctx.flag("architecture_blocked"): return -5.0
        if ctx.flag("architecture_12_complete"): return 1.0
        if ctx.text("architecture_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def architecture_rule_13(self,ctx:SkillGapContext)->float:
        value=ctx.number("architecture_score",0.0)
        if ctx.flag("architecture_blocked"): return -5.0
        if ctx.flag("architecture_13_complete"): return 2.0
        if ctx.text("architecture_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def architecture_rule_14(self,ctx:SkillGapContext)->float:
        value=ctx.number("architecture_score",0.0)
        if ctx.flag("architecture_blocked"): return -5.0
        if ctx.flag("architecture_14_complete"): return 3.0
        if ctx.text("architecture_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def product_rule_1(self,ctx:SkillGapContext)->float:
        value=ctx.number("product_score",0.0)
        if ctx.flag("product_blocked"): return -5.0
        if ctx.flag("product_1_complete"): return 2.0
        if ctx.text("product_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def product_rule_2(self,ctx:SkillGapContext)->float:
        value=ctx.number("product_score",0.0)
        if ctx.flag("product_blocked"): return -5.0
        if ctx.flag("product_2_complete"): return 3.0
        if ctx.text("product_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def product_rule_3(self,ctx:SkillGapContext)->float:
        value=ctx.number("product_score",0.0)
        if ctx.flag("product_blocked"): return -5.0
        if ctx.flag("product_3_complete"): return 4.0
        if ctx.text("product_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def product_rule_4(self,ctx:SkillGapContext)->float:
        value=ctx.number("product_score",0.0)
        if ctx.flag("product_blocked"): return -5.0
        if ctx.flag("product_4_complete"): return 1.0
        if ctx.text("product_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def product_rule_5(self,ctx:SkillGapContext)->float:
        value=ctx.number("product_score",0.0)
        if ctx.flag("product_blocked"): return -5.0
        if ctx.flag("product_5_complete"): return 2.0
        if ctx.text("product_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def product_rule_6(self,ctx:SkillGapContext)->float:
        value=ctx.number("product_score",0.0)
        if ctx.flag("product_blocked"): return -5.0
        if ctx.flag("product_6_complete"): return 3.0
        if ctx.text("product_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def product_rule_7(self,ctx:SkillGapContext)->float:
        value=ctx.number("product_score",0.0)
        if ctx.flag("product_blocked"): return -5.0
        if ctx.flag("product_7_complete"): return 4.0
        if ctx.text("product_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def product_rule_8(self,ctx:SkillGapContext)->float:
        value=ctx.number("product_score",0.0)
        if ctx.flag("product_blocked"): return -5.0
        if ctx.flag("product_8_complete"): return 1.0
        if ctx.text("product_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def product_rule_9(self,ctx:SkillGapContext)->float:
        value=ctx.number("product_score",0.0)
        if ctx.flag("product_blocked"): return -5.0
        if ctx.flag("product_9_complete"): return 2.0
        if ctx.text("product_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def product_rule_10(self,ctx:SkillGapContext)->float:
        value=ctx.number("product_score",0.0)
        if ctx.flag("product_blocked"): return -5.0
        if ctx.flag("product_10_complete"): return 3.0
        if ctx.text("product_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def product_rule_11(self,ctx:SkillGapContext)->float:
        value=ctx.number("product_score",0.0)
        if ctx.flag("product_blocked"): return -5.0
        if ctx.flag("product_11_complete"): return 4.0
        if ctx.text("product_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def product_rule_12(self,ctx:SkillGapContext)->float:
        value=ctx.number("product_score",0.0)
        if ctx.flag("product_blocked"): return -5.0
        if ctx.flag("product_12_complete"): return 1.0
        if ctx.text("product_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def product_rule_13(self,ctx:SkillGapContext)->float:
        value=ctx.number("product_score",0.0)
        if ctx.flag("product_blocked"): return -5.0
        if ctx.flag("product_13_complete"): return 2.0
        if ctx.text("product_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def product_rule_14(self,ctx:SkillGapContext)->float:
        value=ctx.number("product_score",0.0)
        if ctx.flag("product_blocked"): return -5.0
        if ctx.flag("product_14_complete"): return 3.0
        if ctx.text("product_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def management_rule_1(self,ctx:SkillGapContext)->float:
        value=ctx.number("management_score",0.0)
        if ctx.flag("management_blocked"): return -5.0
        if ctx.flag("management_1_complete"): return 2.0
        if ctx.text("management_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def management_rule_2(self,ctx:SkillGapContext)->float:
        value=ctx.number("management_score",0.0)
        if ctx.flag("management_blocked"): return -5.0
        if ctx.flag("management_2_complete"): return 3.0
        if ctx.text("management_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def management_rule_3(self,ctx:SkillGapContext)->float:
        value=ctx.number("management_score",0.0)
        if ctx.flag("management_blocked"): return -5.0
        if ctx.flag("management_3_complete"): return 4.0
        if ctx.text("management_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def management_rule_4(self,ctx:SkillGapContext)->float:
        value=ctx.number("management_score",0.0)
        if ctx.flag("management_blocked"): return -5.0
        if ctx.flag("management_4_complete"): return 1.0
        if ctx.text("management_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def management_rule_5(self,ctx:SkillGapContext)->float:
        value=ctx.number("management_score",0.0)
        if ctx.flag("management_blocked"): return -5.0
        if ctx.flag("management_5_complete"): return 2.0
        if ctx.text("management_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def management_rule_6(self,ctx:SkillGapContext)->float:
        value=ctx.number("management_score",0.0)
        if ctx.flag("management_blocked"): return -5.0
        if ctx.flag("management_6_complete"): return 3.0
        if ctx.text("management_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def management_rule_7(self,ctx:SkillGapContext)->float:
        value=ctx.number("management_score",0.0)
        if ctx.flag("management_blocked"): return -5.0
        if ctx.flag("management_7_complete"): return 4.0
        if ctx.text("management_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def management_rule_8(self,ctx:SkillGapContext)->float:
        value=ctx.number("management_score",0.0)
        if ctx.flag("management_blocked"): return -5.0
        if ctx.flag("management_8_complete"): return 1.0
        if ctx.text("management_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def management_rule_9(self,ctx:SkillGapContext)->float:
        value=ctx.number("management_score",0.0)
        if ctx.flag("management_blocked"): return -5.0
        if ctx.flag("management_9_complete"): return 2.0
        if ctx.text("management_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def management_rule_10(self,ctx:SkillGapContext)->float:
        value=ctx.number("management_score",0.0)
        if ctx.flag("management_blocked"): return -5.0
        if ctx.flag("management_10_complete"): return 3.0
        if ctx.text("management_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def management_rule_11(self,ctx:SkillGapContext)->float:
        value=ctx.number("management_score",0.0)
        if ctx.flag("management_blocked"): return -5.0
        if ctx.flag("management_11_complete"): return 4.0
        if ctx.text("management_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def management_rule_12(self,ctx:SkillGapContext)->float:
        value=ctx.number("management_score",0.0)
        if ctx.flag("management_blocked"): return -5.0
        if ctx.flag("management_12_complete"): return 1.0
        if ctx.text("management_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def management_rule_13(self,ctx:SkillGapContext)->float:
        value=ctx.number("management_score",0.0)
        if ctx.flag("management_blocked"): return -5.0
        if ctx.flag("management_13_complete"): return 2.0
        if ctx.text("management_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def management_rule_14(self,ctx:SkillGapContext)->float:
        value=ctx.number("management_score",0.0)
        if ctx.flag("management_blocked"): return -5.0
        if ctx.flag("management_14_complete"): return 3.0
        if ctx.text("management_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def evaluate_many(self,records:Sequence[Mapping[str,object]])->list[SkillGapResult]:
        return [self.evaluate(record) for record in records]
    def summarize(self,results:Sequence[SkillGapResult])->dict[str,object]:
        scores=[item.score for item in results]
        return {"count":len(scores),"average":round(sum(scores)/len(scores),2) if scores else 0.0,"strong":sum(x.status=="strong" for x in results),"acceptable":sum(x.status=="acceptable" for x in results),"review":sum(x.status=="review" for x in results)}
