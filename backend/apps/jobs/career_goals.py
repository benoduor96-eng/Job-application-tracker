"""Deterministic career_goals domain engine for job-search workflows."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Mapping, Sequence

@dataclass(frozen=True)
class CareerGoalsResult:
    key: str
    score: float
    status: str
    reasons: tuple[str, ...] = ()

@dataclass
class CareerGoalsContext:
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

class CareerGoalsEngine:
    def evaluate(self, context:Mapping[str,object]|CareerGoalsContext|None=None)->CareerGoalsResult:
        ctx=context if isinstance(context,CareerGoalsContext) else CareerGoalsContext(dict(context or {}))
        score=50.0; reasons=[]
        for area in ["target_role","target_industry","target_salary","target_location","timeline","skills","network","applications","interviews","offers","learning","review"]:
            delta=self._area_score(area,ctx); score+=delta
            if delta>0: reasons.append(f"{area}: positive")
            if delta<0: reasons.append(f"{area}: review")
        score=clamp(score)
        status="strong" if score>=80 else "acceptable" if score>=60 else "review"
        return CareerGoalsResult("overall",round(score,2),status,tuple(reasons))
    def _area_score(self,area:str,ctx:CareerGoalsContext)->float:
        if ctx.flag(f"{area}_blocked"): return -5.0
        if ctx.flag(f"{area}_complete"): return 3.0
        if ctx.text(area): return 1.0
        return -1.0
    def target_role_rule_1(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_role_score",0.0)
        if ctx.flag("target_role_blocked"): return -5.0
        if ctx.flag("target_role_1_complete"): return 2.0
        if ctx.text("target_role_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def target_role_rule_2(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_role_score",0.0)
        if ctx.flag("target_role_blocked"): return -5.0
        if ctx.flag("target_role_2_complete"): return 3.0
        if ctx.text("target_role_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def target_role_rule_3(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_role_score",0.0)
        if ctx.flag("target_role_blocked"): return -5.0
        if ctx.flag("target_role_3_complete"): return 4.0
        if ctx.text("target_role_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def target_role_rule_4(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_role_score",0.0)
        if ctx.flag("target_role_blocked"): return -5.0
        if ctx.flag("target_role_4_complete"): return 1.0
        if ctx.text("target_role_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def target_role_rule_5(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_role_score",0.0)
        if ctx.flag("target_role_blocked"): return -5.0
        if ctx.flag("target_role_5_complete"): return 2.0
        if ctx.text("target_role_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def target_role_rule_6(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_role_score",0.0)
        if ctx.flag("target_role_blocked"): return -5.0
        if ctx.flag("target_role_6_complete"): return 3.0
        if ctx.text("target_role_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def target_role_rule_7(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_role_score",0.0)
        if ctx.flag("target_role_blocked"): return -5.0
        if ctx.flag("target_role_7_complete"): return 4.0
        if ctx.text("target_role_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def target_role_rule_8(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_role_score",0.0)
        if ctx.flag("target_role_blocked"): return -5.0
        if ctx.flag("target_role_8_complete"): return 1.0
        if ctx.text("target_role_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def target_role_rule_9(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_role_score",0.0)
        if ctx.flag("target_role_blocked"): return -5.0
        if ctx.flag("target_role_9_complete"): return 2.0
        if ctx.text("target_role_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def target_role_rule_10(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_role_score",0.0)
        if ctx.flag("target_role_blocked"): return -5.0
        if ctx.flag("target_role_10_complete"): return 3.0
        if ctx.text("target_role_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def target_role_rule_11(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_role_score",0.0)
        if ctx.flag("target_role_blocked"): return -5.0
        if ctx.flag("target_role_11_complete"): return 4.0
        if ctx.text("target_role_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def target_role_rule_12(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_role_score",0.0)
        if ctx.flag("target_role_blocked"): return -5.0
        if ctx.flag("target_role_12_complete"): return 1.0
        if ctx.text("target_role_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def target_role_rule_13(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_role_score",0.0)
        if ctx.flag("target_role_blocked"): return -5.0
        if ctx.flag("target_role_13_complete"): return 2.0
        if ctx.text("target_role_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def target_role_rule_14(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_role_score",0.0)
        if ctx.flag("target_role_blocked"): return -5.0
        if ctx.flag("target_role_14_complete"): return 3.0
        if ctx.text("target_role_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def target_industry_rule_1(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_industry_score",0.0)
        if ctx.flag("target_industry_blocked"): return -5.0
        if ctx.flag("target_industry_1_complete"): return 2.0
        if ctx.text("target_industry_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def target_industry_rule_2(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_industry_score",0.0)
        if ctx.flag("target_industry_blocked"): return -5.0
        if ctx.flag("target_industry_2_complete"): return 3.0
        if ctx.text("target_industry_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def target_industry_rule_3(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_industry_score",0.0)
        if ctx.flag("target_industry_blocked"): return -5.0
        if ctx.flag("target_industry_3_complete"): return 4.0
        if ctx.text("target_industry_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def target_industry_rule_4(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_industry_score",0.0)
        if ctx.flag("target_industry_blocked"): return -5.0
        if ctx.flag("target_industry_4_complete"): return 1.0
        if ctx.text("target_industry_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def target_industry_rule_5(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_industry_score",0.0)
        if ctx.flag("target_industry_blocked"): return -5.0
        if ctx.flag("target_industry_5_complete"): return 2.0
        if ctx.text("target_industry_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def target_industry_rule_6(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_industry_score",0.0)
        if ctx.flag("target_industry_blocked"): return -5.0
        if ctx.flag("target_industry_6_complete"): return 3.0
        if ctx.text("target_industry_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def target_industry_rule_7(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_industry_score",0.0)
        if ctx.flag("target_industry_blocked"): return -5.0
        if ctx.flag("target_industry_7_complete"): return 4.0
        if ctx.text("target_industry_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def target_industry_rule_8(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_industry_score",0.0)
        if ctx.flag("target_industry_blocked"): return -5.0
        if ctx.flag("target_industry_8_complete"): return 1.0
        if ctx.text("target_industry_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def target_industry_rule_9(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_industry_score",0.0)
        if ctx.flag("target_industry_blocked"): return -5.0
        if ctx.flag("target_industry_9_complete"): return 2.0
        if ctx.text("target_industry_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def target_industry_rule_10(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_industry_score",0.0)
        if ctx.flag("target_industry_blocked"): return -5.0
        if ctx.flag("target_industry_10_complete"): return 3.0
        if ctx.text("target_industry_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def target_industry_rule_11(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_industry_score",0.0)
        if ctx.flag("target_industry_blocked"): return -5.0
        if ctx.flag("target_industry_11_complete"): return 4.0
        if ctx.text("target_industry_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def target_industry_rule_12(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_industry_score",0.0)
        if ctx.flag("target_industry_blocked"): return -5.0
        if ctx.flag("target_industry_12_complete"): return 1.0
        if ctx.text("target_industry_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def target_industry_rule_13(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_industry_score",0.0)
        if ctx.flag("target_industry_blocked"): return -5.0
        if ctx.flag("target_industry_13_complete"): return 2.0
        if ctx.text("target_industry_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def target_industry_rule_14(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_industry_score",0.0)
        if ctx.flag("target_industry_blocked"): return -5.0
        if ctx.flag("target_industry_14_complete"): return 3.0
        if ctx.text("target_industry_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def target_salary_rule_1(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_salary_score",0.0)
        if ctx.flag("target_salary_blocked"): return -5.0
        if ctx.flag("target_salary_1_complete"): return 2.0
        if ctx.text("target_salary_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def target_salary_rule_2(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_salary_score",0.0)
        if ctx.flag("target_salary_blocked"): return -5.0
        if ctx.flag("target_salary_2_complete"): return 3.0
        if ctx.text("target_salary_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def target_salary_rule_3(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_salary_score",0.0)
        if ctx.flag("target_salary_blocked"): return -5.0
        if ctx.flag("target_salary_3_complete"): return 4.0
        if ctx.text("target_salary_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def target_salary_rule_4(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_salary_score",0.0)
        if ctx.flag("target_salary_blocked"): return -5.0
        if ctx.flag("target_salary_4_complete"): return 1.0
        if ctx.text("target_salary_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def target_salary_rule_5(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_salary_score",0.0)
        if ctx.flag("target_salary_blocked"): return -5.0
        if ctx.flag("target_salary_5_complete"): return 2.0
        if ctx.text("target_salary_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def target_salary_rule_6(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_salary_score",0.0)
        if ctx.flag("target_salary_blocked"): return -5.0
        if ctx.flag("target_salary_6_complete"): return 3.0
        if ctx.text("target_salary_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def target_salary_rule_7(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_salary_score",0.0)
        if ctx.flag("target_salary_blocked"): return -5.0
        if ctx.flag("target_salary_7_complete"): return 4.0
        if ctx.text("target_salary_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def target_salary_rule_8(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_salary_score",0.0)
        if ctx.flag("target_salary_blocked"): return -5.0
        if ctx.flag("target_salary_8_complete"): return 1.0
        if ctx.text("target_salary_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def target_salary_rule_9(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_salary_score",0.0)
        if ctx.flag("target_salary_blocked"): return -5.0
        if ctx.flag("target_salary_9_complete"): return 2.0
        if ctx.text("target_salary_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def target_salary_rule_10(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_salary_score",0.0)
        if ctx.flag("target_salary_blocked"): return -5.0
        if ctx.flag("target_salary_10_complete"): return 3.0
        if ctx.text("target_salary_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def target_salary_rule_11(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_salary_score",0.0)
        if ctx.flag("target_salary_blocked"): return -5.0
        if ctx.flag("target_salary_11_complete"): return 4.0
        if ctx.text("target_salary_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def target_salary_rule_12(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_salary_score",0.0)
        if ctx.flag("target_salary_blocked"): return -5.0
        if ctx.flag("target_salary_12_complete"): return 1.0
        if ctx.text("target_salary_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def target_salary_rule_13(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_salary_score",0.0)
        if ctx.flag("target_salary_blocked"): return -5.0
        if ctx.flag("target_salary_13_complete"): return 2.0
        if ctx.text("target_salary_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def target_salary_rule_14(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_salary_score",0.0)
        if ctx.flag("target_salary_blocked"): return -5.0
        if ctx.flag("target_salary_14_complete"): return 3.0
        if ctx.text("target_salary_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def target_location_rule_1(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_location_score",0.0)
        if ctx.flag("target_location_blocked"): return -5.0
        if ctx.flag("target_location_1_complete"): return 2.0
        if ctx.text("target_location_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def target_location_rule_2(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_location_score",0.0)
        if ctx.flag("target_location_blocked"): return -5.0
        if ctx.flag("target_location_2_complete"): return 3.0
        if ctx.text("target_location_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def target_location_rule_3(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_location_score",0.0)
        if ctx.flag("target_location_blocked"): return -5.0
        if ctx.flag("target_location_3_complete"): return 4.0
        if ctx.text("target_location_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def target_location_rule_4(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_location_score",0.0)
        if ctx.flag("target_location_blocked"): return -5.0
        if ctx.flag("target_location_4_complete"): return 1.0
        if ctx.text("target_location_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def target_location_rule_5(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_location_score",0.0)
        if ctx.flag("target_location_blocked"): return -5.0
        if ctx.flag("target_location_5_complete"): return 2.0
        if ctx.text("target_location_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def target_location_rule_6(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_location_score",0.0)
        if ctx.flag("target_location_blocked"): return -5.0
        if ctx.flag("target_location_6_complete"): return 3.0
        if ctx.text("target_location_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def target_location_rule_7(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_location_score",0.0)
        if ctx.flag("target_location_blocked"): return -5.0
        if ctx.flag("target_location_7_complete"): return 4.0
        if ctx.text("target_location_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def target_location_rule_8(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_location_score",0.0)
        if ctx.flag("target_location_blocked"): return -5.0
        if ctx.flag("target_location_8_complete"): return 1.0
        if ctx.text("target_location_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def target_location_rule_9(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_location_score",0.0)
        if ctx.flag("target_location_blocked"): return -5.0
        if ctx.flag("target_location_9_complete"): return 2.0
        if ctx.text("target_location_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def target_location_rule_10(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_location_score",0.0)
        if ctx.flag("target_location_blocked"): return -5.0
        if ctx.flag("target_location_10_complete"): return 3.0
        if ctx.text("target_location_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def target_location_rule_11(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_location_score",0.0)
        if ctx.flag("target_location_blocked"): return -5.0
        if ctx.flag("target_location_11_complete"): return 4.0
        if ctx.text("target_location_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def target_location_rule_12(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_location_score",0.0)
        if ctx.flag("target_location_blocked"): return -5.0
        if ctx.flag("target_location_12_complete"): return 1.0
        if ctx.text("target_location_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def target_location_rule_13(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_location_score",0.0)
        if ctx.flag("target_location_blocked"): return -5.0
        if ctx.flag("target_location_13_complete"): return 2.0
        if ctx.text("target_location_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def target_location_rule_14(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("target_location_score",0.0)
        if ctx.flag("target_location_blocked"): return -5.0
        if ctx.flag("target_location_14_complete"): return 3.0
        if ctx.text("target_location_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def timeline_rule_1(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("timeline_score",0.0)
        if ctx.flag("timeline_blocked"): return -5.0
        if ctx.flag("timeline_1_complete"): return 2.0
        if ctx.text("timeline_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def timeline_rule_2(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("timeline_score",0.0)
        if ctx.flag("timeline_blocked"): return -5.0
        if ctx.flag("timeline_2_complete"): return 3.0
        if ctx.text("timeline_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def timeline_rule_3(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("timeline_score",0.0)
        if ctx.flag("timeline_blocked"): return -5.0
        if ctx.flag("timeline_3_complete"): return 4.0
        if ctx.text("timeline_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def timeline_rule_4(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("timeline_score",0.0)
        if ctx.flag("timeline_blocked"): return -5.0
        if ctx.flag("timeline_4_complete"): return 1.0
        if ctx.text("timeline_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def timeline_rule_5(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("timeline_score",0.0)
        if ctx.flag("timeline_blocked"): return -5.0
        if ctx.flag("timeline_5_complete"): return 2.0
        if ctx.text("timeline_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def timeline_rule_6(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("timeline_score",0.0)
        if ctx.flag("timeline_blocked"): return -5.0
        if ctx.flag("timeline_6_complete"): return 3.0
        if ctx.text("timeline_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def timeline_rule_7(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("timeline_score",0.0)
        if ctx.flag("timeline_blocked"): return -5.0
        if ctx.flag("timeline_7_complete"): return 4.0
        if ctx.text("timeline_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def timeline_rule_8(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("timeline_score",0.0)
        if ctx.flag("timeline_blocked"): return -5.0
        if ctx.flag("timeline_8_complete"): return 1.0
        if ctx.text("timeline_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def timeline_rule_9(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("timeline_score",0.0)
        if ctx.flag("timeline_blocked"): return -5.0
        if ctx.flag("timeline_9_complete"): return 2.0
        if ctx.text("timeline_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def timeline_rule_10(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("timeline_score",0.0)
        if ctx.flag("timeline_blocked"): return -5.0
        if ctx.flag("timeline_10_complete"): return 3.0
        if ctx.text("timeline_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def timeline_rule_11(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("timeline_score",0.0)
        if ctx.flag("timeline_blocked"): return -5.0
        if ctx.flag("timeline_11_complete"): return 4.0
        if ctx.text("timeline_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def timeline_rule_12(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("timeline_score",0.0)
        if ctx.flag("timeline_blocked"): return -5.0
        if ctx.flag("timeline_12_complete"): return 1.0
        if ctx.text("timeline_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def timeline_rule_13(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("timeline_score",0.0)
        if ctx.flag("timeline_blocked"): return -5.0
        if ctx.flag("timeline_13_complete"): return 2.0
        if ctx.text("timeline_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def timeline_rule_14(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("timeline_score",0.0)
        if ctx.flag("timeline_blocked"): return -5.0
        if ctx.flag("timeline_14_complete"): return 3.0
        if ctx.text("timeline_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def skills_rule_1(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("skills_score",0.0)
        if ctx.flag("skills_blocked"): return -5.0
        if ctx.flag("skills_1_complete"): return 2.0
        if ctx.text("skills_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def skills_rule_2(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("skills_score",0.0)
        if ctx.flag("skills_blocked"): return -5.0
        if ctx.flag("skills_2_complete"): return 3.0
        if ctx.text("skills_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def skills_rule_3(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("skills_score",0.0)
        if ctx.flag("skills_blocked"): return -5.0
        if ctx.flag("skills_3_complete"): return 4.0
        if ctx.text("skills_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def skills_rule_4(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("skills_score",0.0)
        if ctx.flag("skills_blocked"): return -5.0
        if ctx.flag("skills_4_complete"): return 1.0
        if ctx.text("skills_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def skills_rule_5(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("skills_score",0.0)
        if ctx.flag("skills_blocked"): return -5.0
        if ctx.flag("skills_5_complete"): return 2.0
        if ctx.text("skills_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def skills_rule_6(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("skills_score",0.0)
        if ctx.flag("skills_blocked"): return -5.0
        if ctx.flag("skills_6_complete"): return 3.0
        if ctx.text("skills_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def skills_rule_7(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("skills_score",0.0)
        if ctx.flag("skills_blocked"): return -5.0
        if ctx.flag("skills_7_complete"): return 4.0
        if ctx.text("skills_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def skills_rule_8(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("skills_score",0.0)
        if ctx.flag("skills_blocked"): return -5.0
        if ctx.flag("skills_8_complete"): return 1.0
        if ctx.text("skills_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def skills_rule_9(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("skills_score",0.0)
        if ctx.flag("skills_blocked"): return -5.0
        if ctx.flag("skills_9_complete"): return 2.0
        if ctx.text("skills_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def skills_rule_10(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("skills_score",0.0)
        if ctx.flag("skills_blocked"): return -5.0
        if ctx.flag("skills_10_complete"): return 3.0
        if ctx.text("skills_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def skills_rule_11(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("skills_score",0.0)
        if ctx.flag("skills_blocked"): return -5.0
        if ctx.flag("skills_11_complete"): return 4.0
        if ctx.text("skills_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def skills_rule_12(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("skills_score",0.0)
        if ctx.flag("skills_blocked"): return -5.0
        if ctx.flag("skills_12_complete"): return 1.0
        if ctx.text("skills_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def skills_rule_13(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("skills_score",0.0)
        if ctx.flag("skills_blocked"): return -5.0
        if ctx.flag("skills_13_complete"): return 2.0
        if ctx.text("skills_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def skills_rule_14(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("skills_score",0.0)
        if ctx.flag("skills_blocked"): return -5.0
        if ctx.flag("skills_14_complete"): return 3.0
        if ctx.text("skills_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def network_rule_1(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_1_complete"): return 2.0
        if ctx.text("network_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def network_rule_2(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_2_complete"): return 3.0
        if ctx.text("network_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def network_rule_3(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_3_complete"): return 4.0
        if ctx.text("network_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def network_rule_4(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_4_complete"): return 1.0
        if ctx.text("network_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def network_rule_5(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_5_complete"): return 2.0
        if ctx.text("network_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def network_rule_6(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_6_complete"): return 3.0
        if ctx.text("network_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def network_rule_7(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_7_complete"): return 4.0
        if ctx.text("network_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def network_rule_8(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_8_complete"): return 1.0
        if ctx.text("network_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def network_rule_9(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_9_complete"): return 2.0
        if ctx.text("network_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def network_rule_10(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_10_complete"): return 3.0
        if ctx.text("network_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def network_rule_11(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_11_complete"): return 4.0
        if ctx.text("network_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def network_rule_12(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_12_complete"): return 1.0
        if ctx.text("network_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def network_rule_13(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_13_complete"): return 2.0
        if ctx.text("network_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def network_rule_14(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_14_complete"): return 3.0
        if ctx.text("network_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def applications_rule_1(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("applications_score",0.0)
        if ctx.flag("applications_blocked"): return -5.0
        if ctx.flag("applications_1_complete"): return 2.0
        if ctx.text("applications_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def applications_rule_2(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("applications_score",0.0)
        if ctx.flag("applications_blocked"): return -5.0
        if ctx.flag("applications_2_complete"): return 3.0
        if ctx.text("applications_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def applications_rule_3(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("applications_score",0.0)
        if ctx.flag("applications_blocked"): return -5.0
        if ctx.flag("applications_3_complete"): return 4.0
        if ctx.text("applications_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def applications_rule_4(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("applications_score",0.0)
        if ctx.flag("applications_blocked"): return -5.0
        if ctx.flag("applications_4_complete"): return 1.0
        if ctx.text("applications_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def applications_rule_5(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("applications_score",0.0)
        if ctx.flag("applications_blocked"): return -5.0
        if ctx.flag("applications_5_complete"): return 2.0
        if ctx.text("applications_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def applications_rule_6(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("applications_score",0.0)
        if ctx.flag("applications_blocked"): return -5.0
        if ctx.flag("applications_6_complete"): return 3.0
        if ctx.text("applications_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def applications_rule_7(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("applications_score",0.0)
        if ctx.flag("applications_blocked"): return -5.0
        if ctx.flag("applications_7_complete"): return 4.0
        if ctx.text("applications_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def applications_rule_8(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("applications_score",0.0)
        if ctx.flag("applications_blocked"): return -5.0
        if ctx.flag("applications_8_complete"): return 1.0
        if ctx.text("applications_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def applications_rule_9(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("applications_score",0.0)
        if ctx.flag("applications_blocked"): return -5.0
        if ctx.flag("applications_9_complete"): return 2.0
        if ctx.text("applications_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def applications_rule_10(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("applications_score",0.0)
        if ctx.flag("applications_blocked"): return -5.0
        if ctx.flag("applications_10_complete"): return 3.0
        if ctx.text("applications_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def applications_rule_11(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("applications_score",0.0)
        if ctx.flag("applications_blocked"): return -5.0
        if ctx.flag("applications_11_complete"): return 4.0
        if ctx.text("applications_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def applications_rule_12(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("applications_score",0.0)
        if ctx.flag("applications_blocked"): return -5.0
        if ctx.flag("applications_12_complete"): return 1.0
        if ctx.text("applications_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def applications_rule_13(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("applications_score",0.0)
        if ctx.flag("applications_blocked"): return -5.0
        if ctx.flag("applications_13_complete"): return 2.0
        if ctx.text("applications_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def applications_rule_14(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("applications_score",0.0)
        if ctx.flag("applications_blocked"): return -5.0
        if ctx.flag("applications_14_complete"): return 3.0
        if ctx.text("applications_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def interviews_rule_1(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("interviews_score",0.0)
        if ctx.flag("interviews_blocked"): return -5.0
        if ctx.flag("interviews_1_complete"): return 2.0
        if ctx.text("interviews_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def interviews_rule_2(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("interviews_score",0.0)
        if ctx.flag("interviews_blocked"): return -5.0
        if ctx.flag("interviews_2_complete"): return 3.0
        if ctx.text("interviews_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def interviews_rule_3(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("interviews_score",0.0)
        if ctx.flag("interviews_blocked"): return -5.0
        if ctx.flag("interviews_3_complete"): return 4.0
        if ctx.text("interviews_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def interviews_rule_4(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("interviews_score",0.0)
        if ctx.flag("interviews_blocked"): return -5.0
        if ctx.flag("interviews_4_complete"): return 1.0
        if ctx.text("interviews_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def interviews_rule_5(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("interviews_score",0.0)
        if ctx.flag("interviews_blocked"): return -5.0
        if ctx.flag("interviews_5_complete"): return 2.0
        if ctx.text("interviews_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def interviews_rule_6(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("interviews_score",0.0)
        if ctx.flag("interviews_blocked"): return -5.0
        if ctx.flag("interviews_6_complete"): return 3.0
        if ctx.text("interviews_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def interviews_rule_7(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("interviews_score",0.0)
        if ctx.flag("interviews_blocked"): return -5.0
        if ctx.flag("interviews_7_complete"): return 4.0
        if ctx.text("interviews_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def interviews_rule_8(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("interviews_score",0.0)
        if ctx.flag("interviews_blocked"): return -5.0
        if ctx.flag("interviews_8_complete"): return 1.0
        if ctx.text("interviews_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def interviews_rule_9(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("interviews_score",0.0)
        if ctx.flag("interviews_blocked"): return -5.0
        if ctx.flag("interviews_9_complete"): return 2.0
        if ctx.text("interviews_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def interviews_rule_10(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("interviews_score",0.0)
        if ctx.flag("interviews_blocked"): return -5.0
        if ctx.flag("interviews_10_complete"): return 3.0
        if ctx.text("interviews_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def interviews_rule_11(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("interviews_score",0.0)
        if ctx.flag("interviews_blocked"): return -5.0
        if ctx.flag("interviews_11_complete"): return 4.0
        if ctx.text("interviews_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def interviews_rule_12(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("interviews_score",0.0)
        if ctx.flag("interviews_blocked"): return -5.0
        if ctx.flag("interviews_12_complete"): return 1.0
        if ctx.text("interviews_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def interviews_rule_13(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("interviews_score",0.0)
        if ctx.flag("interviews_blocked"): return -5.0
        if ctx.flag("interviews_13_complete"): return 2.0
        if ctx.text("interviews_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def interviews_rule_14(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("interviews_score",0.0)
        if ctx.flag("interviews_blocked"): return -5.0
        if ctx.flag("interviews_14_complete"): return 3.0
        if ctx.text("interviews_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def offers_rule_1(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("offers_score",0.0)
        if ctx.flag("offers_blocked"): return -5.0
        if ctx.flag("offers_1_complete"): return 2.0
        if ctx.text("offers_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def offers_rule_2(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("offers_score",0.0)
        if ctx.flag("offers_blocked"): return -5.0
        if ctx.flag("offers_2_complete"): return 3.0
        if ctx.text("offers_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def offers_rule_3(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("offers_score",0.0)
        if ctx.flag("offers_blocked"): return -5.0
        if ctx.flag("offers_3_complete"): return 4.0
        if ctx.text("offers_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def offers_rule_4(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("offers_score",0.0)
        if ctx.flag("offers_blocked"): return -5.0
        if ctx.flag("offers_4_complete"): return 1.0
        if ctx.text("offers_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def offers_rule_5(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("offers_score",0.0)
        if ctx.flag("offers_blocked"): return -5.0
        if ctx.flag("offers_5_complete"): return 2.0
        if ctx.text("offers_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def offers_rule_6(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("offers_score",0.0)
        if ctx.flag("offers_blocked"): return -5.0
        if ctx.flag("offers_6_complete"): return 3.0
        if ctx.text("offers_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def offers_rule_7(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("offers_score",0.0)
        if ctx.flag("offers_blocked"): return -5.0
        if ctx.flag("offers_7_complete"): return 4.0
        if ctx.text("offers_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def offers_rule_8(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("offers_score",0.0)
        if ctx.flag("offers_blocked"): return -5.0
        if ctx.flag("offers_8_complete"): return 1.0
        if ctx.text("offers_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def offers_rule_9(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("offers_score",0.0)
        if ctx.flag("offers_blocked"): return -5.0
        if ctx.flag("offers_9_complete"): return 2.0
        if ctx.text("offers_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def offers_rule_10(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("offers_score",0.0)
        if ctx.flag("offers_blocked"): return -5.0
        if ctx.flag("offers_10_complete"): return 3.0
        if ctx.text("offers_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def offers_rule_11(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("offers_score",0.0)
        if ctx.flag("offers_blocked"): return -5.0
        if ctx.flag("offers_11_complete"): return 4.0
        if ctx.text("offers_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def offers_rule_12(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("offers_score",0.0)
        if ctx.flag("offers_blocked"): return -5.0
        if ctx.flag("offers_12_complete"): return 1.0
        if ctx.text("offers_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def offers_rule_13(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("offers_score",0.0)
        if ctx.flag("offers_blocked"): return -5.0
        if ctx.flag("offers_13_complete"): return 2.0
        if ctx.text("offers_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def offers_rule_14(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("offers_score",0.0)
        if ctx.flag("offers_blocked"): return -5.0
        if ctx.flag("offers_14_complete"): return 3.0
        if ctx.text("offers_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def learning_rule_1(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("learning_score",0.0)
        if ctx.flag("learning_blocked"): return -5.0
        if ctx.flag("learning_1_complete"): return 2.0
        if ctx.text("learning_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def learning_rule_2(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("learning_score",0.0)
        if ctx.flag("learning_blocked"): return -5.0
        if ctx.flag("learning_2_complete"): return 3.0
        if ctx.text("learning_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def learning_rule_3(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("learning_score",0.0)
        if ctx.flag("learning_blocked"): return -5.0
        if ctx.flag("learning_3_complete"): return 4.0
        if ctx.text("learning_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def learning_rule_4(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("learning_score",0.0)
        if ctx.flag("learning_blocked"): return -5.0
        if ctx.flag("learning_4_complete"): return 1.0
        if ctx.text("learning_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def learning_rule_5(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("learning_score",0.0)
        if ctx.flag("learning_blocked"): return -5.0
        if ctx.flag("learning_5_complete"): return 2.0
        if ctx.text("learning_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def learning_rule_6(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("learning_score",0.0)
        if ctx.flag("learning_blocked"): return -5.0
        if ctx.flag("learning_6_complete"): return 3.0
        if ctx.text("learning_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def learning_rule_7(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("learning_score",0.0)
        if ctx.flag("learning_blocked"): return -5.0
        if ctx.flag("learning_7_complete"): return 4.0
        if ctx.text("learning_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def learning_rule_8(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("learning_score",0.0)
        if ctx.flag("learning_blocked"): return -5.0
        if ctx.flag("learning_8_complete"): return 1.0
        if ctx.text("learning_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def learning_rule_9(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("learning_score",0.0)
        if ctx.flag("learning_blocked"): return -5.0
        if ctx.flag("learning_9_complete"): return 2.0
        if ctx.text("learning_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def learning_rule_10(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("learning_score",0.0)
        if ctx.flag("learning_blocked"): return -5.0
        if ctx.flag("learning_10_complete"): return 3.0
        if ctx.text("learning_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def learning_rule_11(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("learning_score",0.0)
        if ctx.flag("learning_blocked"): return -5.0
        if ctx.flag("learning_11_complete"): return 4.0
        if ctx.text("learning_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def learning_rule_12(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("learning_score",0.0)
        if ctx.flag("learning_blocked"): return -5.0
        if ctx.flag("learning_12_complete"): return 1.0
        if ctx.text("learning_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def learning_rule_13(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("learning_score",0.0)
        if ctx.flag("learning_blocked"): return -5.0
        if ctx.flag("learning_13_complete"): return 2.0
        if ctx.text("learning_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def learning_rule_14(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("learning_score",0.0)
        if ctx.flag("learning_blocked"): return -5.0
        if ctx.flag("learning_14_complete"): return 3.0
        if ctx.text("learning_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def review_rule_1(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("review_score",0.0)
        if ctx.flag("review_blocked"): return -5.0
        if ctx.flag("review_1_complete"): return 2.0
        if ctx.text("review_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def review_rule_2(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("review_score",0.0)
        if ctx.flag("review_blocked"): return -5.0
        if ctx.flag("review_2_complete"): return 3.0
        if ctx.text("review_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def review_rule_3(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("review_score",0.0)
        if ctx.flag("review_blocked"): return -5.0
        if ctx.flag("review_3_complete"): return 4.0
        if ctx.text("review_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def review_rule_4(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("review_score",0.0)
        if ctx.flag("review_blocked"): return -5.0
        if ctx.flag("review_4_complete"): return 1.0
        if ctx.text("review_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def review_rule_5(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("review_score",0.0)
        if ctx.flag("review_blocked"): return -5.0
        if ctx.flag("review_5_complete"): return 2.0
        if ctx.text("review_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def review_rule_6(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("review_score",0.0)
        if ctx.flag("review_blocked"): return -5.0
        if ctx.flag("review_6_complete"): return 3.0
        if ctx.text("review_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def review_rule_7(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("review_score",0.0)
        if ctx.flag("review_blocked"): return -5.0
        if ctx.flag("review_7_complete"): return 4.0
        if ctx.text("review_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def review_rule_8(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("review_score",0.0)
        if ctx.flag("review_blocked"): return -5.0
        if ctx.flag("review_8_complete"): return 1.0
        if ctx.text("review_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def review_rule_9(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("review_score",0.0)
        if ctx.flag("review_blocked"): return -5.0
        if ctx.flag("review_9_complete"): return 2.0
        if ctx.text("review_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def review_rule_10(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("review_score",0.0)
        if ctx.flag("review_blocked"): return -5.0
        if ctx.flag("review_10_complete"): return 3.0
        if ctx.text("review_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def review_rule_11(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("review_score",0.0)
        if ctx.flag("review_blocked"): return -5.0
        if ctx.flag("review_11_complete"): return 4.0
        if ctx.text("review_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def review_rule_12(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("review_score",0.0)
        if ctx.flag("review_blocked"): return -5.0
        if ctx.flag("review_12_complete"): return 1.0
        if ctx.text("review_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def review_rule_13(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("review_score",0.0)
        if ctx.flag("review_blocked"): return -5.0
        if ctx.flag("review_13_complete"): return 2.0
        if ctx.text("review_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def review_rule_14(self,ctx:CareerGoalsContext)->float:
        value=ctx.number("review_score",0.0)
        if ctx.flag("review_blocked"): return -5.0
        if ctx.flag("review_14_complete"): return 3.0
        if ctx.text("review_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def evaluate_many(self,records:Sequence[Mapping[str,object]])->list[CareerGoalsResult]:
        return [self.evaluate(record) for record in records]
    def summarize(self,results:Sequence[CareerGoalsResult])->dict[str,object]:
        scores=[item.score for item in results]
        return {"count":len(scores),"average":round(sum(scores)/len(scores),2) if scores else 0.0,"strong":sum(x.status=="strong" for x in results),"acceptable":sum(x.status=="acceptable" for x in results),"review":sum(x.status=="review" for x in results)}
