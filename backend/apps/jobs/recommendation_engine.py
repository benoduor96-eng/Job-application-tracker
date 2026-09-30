"""Deterministic recommendation domain engine for job-search workflows."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Mapping, Sequence

@dataclass(frozen=True)
class RecommendationResult:
    key: str
    score: float
    status: str
    reasons: tuple[str, ...] = ()

@dataclass
class RecommendationContext:
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

class RecommendationEngine:
    def evaluate(self, context:Mapping[str,object]|RecommendationContext|None=None)->RecommendationResult:
        ctx=context if isinstance(context,RecommendationContext) else RecommendationContext(dict(context or {}))
        score=50.0; reasons=[]
        for area in ["next_action","role","skill","application","follow_up","task","interview","resume","network","learning","company","search"]:
            delta=self._area_score(area,ctx); score+=delta
            if delta>0: reasons.append(f"{area}: positive")
            if delta<0: reasons.append(f"{area}: review")
        score=clamp(score)
        status="strong" if score>=80 else "acceptable" if score>=60 else "review"
        return RecommendationResult("overall",round(score,2),status,tuple(reasons))
    def _area_score(self,area:str,ctx:RecommendationContext)->float:
        if ctx.flag(f"{area}_blocked"): return -5.0
        if ctx.flag(f"{area}_complete"): return 3.0
        if ctx.text(area): return 1.0
        return -1.0
    def next_action_rule_1(self,ctx:RecommendationContext)->float:
        value=ctx.number("next_action_score",0.0)
        if ctx.flag("next_action_blocked"): return -5.0
        if ctx.flag("next_action_1_complete"): return 2.0
        if ctx.text("next_action_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def next_action_rule_2(self,ctx:RecommendationContext)->float:
        value=ctx.number("next_action_score",0.0)
        if ctx.flag("next_action_blocked"): return -5.0
        if ctx.flag("next_action_2_complete"): return 3.0
        if ctx.text("next_action_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def next_action_rule_3(self,ctx:RecommendationContext)->float:
        value=ctx.number("next_action_score",0.0)
        if ctx.flag("next_action_blocked"): return -5.0
        if ctx.flag("next_action_3_complete"): return 4.0
        if ctx.text("next_action_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def next_action_rule_4(self,ctx:RecommendationContext)->float:
        value=ctx.number("next_action_score",0.0)
        if ctx.flag("next_action_blocked"): return -5.0
        if ctx.flag("next_action_4_complete"): return 1.0
        if ctx.text("next_action_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def next_action_rule_5(self,ctx:RecommendationContext)->float:
        value=ctx.number("next_action_score",0.0)
        if ctx.flag("next_action_blocked"): return -5.0
        if ctx.flag("next_action_5_complete"): return 2.0
        if ctx.text("next_action_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def next_action_rule_6(self,ctx:RecommendationContext)->float:
        value=ctx.number("next_action_score",0.0)
        if ctx.flag("next_action_blocked"): return -5.0
        if ctx.flag("next_action_6_complete"): return 3.0
        if ctx.text("next_action_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def next_action_rule_7(self,ctx:RecommendationContext)->float:
        value=ctx.number("next_action_score",0.0)
        if ctx.flag("next_action_blocked"): return -5.0
        if ctx.flag("next_action_7_complete"): return 4.0
        if ctx.text("next_action_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def next_action_rule_8(self,ctx:RecommendationContext)->float:
        value=ctx.number("next_action_score",0.0)
        if ctx.flag("next_action_blocked"): return -5.0
        if ctx.flag("next_action_8_complete"): return 1.0
        if ctx.text("next_action_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def next_action_rule_9(self,ctx:RecommendationContext)->float:
        value=ctx.number("next_action_score",0.0)
        if ctx.flag("next_action_blocked"): return -5.0
        if ctx.flag("next_action_9_complete"): return 2.0
        if ctx.text("next_action_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def next_action_rule_10(self,ctx:RecommendationContext)->float:
        value=ctx.number("next_action_score",0.0)
        if ctx.flag("next_action_blocked"): return -5.0
        if ctx.flag("next_action_10_complete"): return 3.0
        if ctx.text("next_action_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def next_action_rule_11(self,ctx:RecommendationContext)->float:
        value=ctx.number("next_action_score",0.0)
        if ctx.flag("next_action_blocked"): return -5.0
        if ctx.flag("next_action_11_complete"): return 4.0
        if ctx.text("next_action_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def next_action_rule_12(self,ctx:RecommendationContext)->float:
        value=ctx.number("next_action_score",0.0)
        if ctx.flag("next_action_blocked"): return -5.0
        if ctx.flag("next_action_12_complete"): return 1.0
        if ctx.text("next_action_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def next_action_rule_13(self,ctx:RecommendationContext)->float:
        value=ctx.number("next_action_score",0.0)
        if ctx.flag("next_action_blocked"): return -5.0
        if ctx.flag("next_action_13_complete"): return 2.0
        if ctx.text("next_action_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def next_action_rule_14(self,ctx:RecommendationContext)->float:
        value=ctx.number("next_action_score",0.0)
        if ctx.flag("next_action_blocked"): return -5.0
        if ctx.flag("next_action_14_complete"): return 3.0
        if ctx.text("next_action_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def role_rule_1(self,ctx:RecommendationContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_1_complete"): return 2.0
        if ctx.text("role_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def role_rule_2(self,ctx:RecommendationContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_2_complete"): return 3.0
        if ctx.text("role_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def role_rule_3(self,ctx:RecommendationContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_3_complete"): return 4.0
        if ctx.text("role_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def role_rule_4(self,ctx:RecommendationContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_4_complete"): return 1.0
        if ctx.text("role_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def role_rule_5(self,ctx:RecommendationContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_5_complete"): return 2.0
        if ctx.text("role_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def role_rule_6(self,ctx:RecommendationContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_6_complete"): return 3.0
        if ctx.text("role_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def role_rule_7(self,ctx:RecommendationContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_7_complete"): return 4.0
        if ctx.text("role_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def role_rule_8(self,ctx:RecommendationContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_8_complete"): return 1.0
        if ctx.text("role_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def role_rule_9(self,ctx:RecommendationContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_9_complete"): return 2.0
        if ctx.text("role_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def role_rule_10(self,ctx:RecommendationContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_10_complete"): return 3.0
        if ctx.text("role_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def role_rule_11(self,ctx:RecommendationContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_11_complete"): return 4.0
        if ctx.text("role_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def role_rule_12(self,ctx:RecommendationContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_12_complete"): return 1.0
        if ctx.text("role_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def role_rule_13(self,ctx:RecommendationContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_13_complete"): return 2.0
        if ctx.text("role_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def role_rule_14(self,ctx:RecommendationContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_14_complete"): return 3.0
        if ctx.text("role_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def skill_rule_1(self,ctx:RecommendationContext)->float:
        value=ctx.number("skill_score",0.0)
        if ctx.flag("skill_blocked"): return -5.0
        if ctx.flag("skill_1_complete"): return 2.0
        if ctx.text("skill_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def skill_rule_2(self,ctx:RecommendationContext)->float:
        value=ctx.number("skill_score",0.0)
        if ctx.flag("skill_blocked"): return -5.0
        if ctx.flag("skill_2_complete"): return 3.0
        if ctx.text("skill_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def skill_rule_3(self,ctx:RecommendationContext)->float:
        value=ctx.number("skill_score",0.0)
        if ctx.flag("skill_blocked"): return -5.0
        if ctx.flag("skill_3_complete"): return 4.0
        if ctx.text("skill_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def skill_rule_4(self,ctx:RecommendationContext)->float:
        value=ctx.number("skill_score",0.0)
        if ctx.flag("skill_blocked"): return -5.0
        if ctx.flag("skill_4_complete"): return 1.0
        if ctx.text("skill_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def skill_rule_5(self,ctx:RecommendationContext)->float:
        value=ctx.number("skill_score",0.0)
        if ctx.flag("skill_blocked"): return -5.0
        if ctx.flag("skill_5_complete"): return 2.0
        if ctx.text("skill_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def skill_rule_6(self,ctx:RecommendationContext)->float:
        value=ctx.number("skill_score",0.0)
        if ctx.flag("skill_blocked"): return -5.0
        if ctx.flag("skill_6_complete"): return 3.0
        if ctx.text("skill_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def skill_rule_7(self,ctx:RecommendationContext)->float:
        value=ctx.number("skill_score",0.0)
        if ctx.flag("skill_blocked"): return -5.0
        if ctx.flag("skill_7_complete"): return 4.0
        if ctx.text("skill_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def skill_rule_8(self,ctx:RecommendationContext)->float:
        value=ctx.number("skill_score",0.0)
        if ctx.flag("skill_blocked"): return -5.0
        if ctx.flag("skill_8_complete"): return 1.0
        if ctx.text("skill_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def skill_rule_9(self,ctx:RecommendationContext)->float:
        value=ctx.number("skill_score",0.0)
        if ctx.flag("skill_blocked"): return -5.0
        if ctx.flag("skill_9_complete"): return 2.0
        if ctx.text("skill_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def skill_rule_10(self,ctx:RecommendationContext)->float:
        value=ctx.number("skill_score",0.0)
        if ctx.flag("skill_blocked"): return -5.0
        if ctx.flag("skill_10_complete"): return 3.0
        if ctx.text("skill_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def skill_rule_11(self,ctx:RecommendationContext)->float:
        value=ctx.number("skill_score",0.0)
        if ctx.flag("skill_blocked"): return -5.0
        if ctx.flag("skill_11_complete"): return 4.0
        if ctx.text("skill_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def skill_rule_12(self,ctx:RecommendationContext)->float:
        value=ctx.number("skill_score",0.0)
        if ctx.flag("skill_blocked"): return -5.0
        if ctx.flag("skill_12_complete"): return 1.0
        if ctx.text("skill_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def skill_rule_13(self,ctx:RecommendationContext)->float:
        value=ctx.number("skill_score",0.0)
        if ctx.flag("skill_blocked"): return -5.0
        if ctx.flag("skill_13_complete"): return 2.0
        if ctx.text("skill_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def skill_rule_14(self,ctx:RecommendationContext)->float:
        value=ctx.number("skill_score",0.0)
        if ctx.flag("skill_blocked"): return -5.0
        if ctx.flag("skill_14_complete"): return 3.0
        if ctx.text("skill_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def application_rule_1(self,ctx:RecommendationContext)->float:
        value=ctx.number("application_score",0.0)
        if ctx.flag("application_blocked"): return -5.0
        if ctx.flag("application_1_complete"): return 2.0
        if ctx.text("application_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def application_rule_2(self,ctx:RecommendationContext)->float:
        value=ctx.number("application_score",0.0)
        if ctx.flag("application_blocked"): return -5.0
        if ctx.flag("application_2_complete"): return 3.0
        if ctx.text("application_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def application_rule_3(self,ctx:RecommendationContext)->float:
        value=ctx.number("application_score",0.0)
        if ctx.flag("application_blocked"): return -5.0
        if ctx.flag("application_3_complete"): return 4.0
        if ctx.text("application_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def application_rule_4(self,ctx:RecommendationContext)->float:
        value=ctx.number("application_score",0.0)
        if ctx.flag("application_blocked"): return -5.0
        if ctx.flag("application_4_complete"): return 1.0
        if ctx.text("application_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def application_rule_5(self,ctx:RecommendationContext)->float:
        value=ctx.number("application_score",0.0)
        if ctx.flag("application_blocked"): return -5.0
        if ctx.flag("application_5_complete"): return 2.0
        if ctx.text("application_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def application_rule_6(self,ctx:RecommendationContext)->float:
        value=ctx.number("application_score",0.0)
        if ctx.flag("application_blocked"): return -5.0
        if ctx.flag("application_6_complete"): return 3.0
        if ctx.text("application_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def application_rule_7(self,ctx:RecommendationContext)->float:
        value=ctx.number("application_score",0.0)
        if ctx.flag("application_blocked"): return -5.0
        if ctx.flag("application_7_complete"): return 4.0
        if ctx.text("application_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def application_rule_8(self,ctx:RecommendationContext)->float:
        value=ctx.number("application_score",0.0)
        if ctx.flag("application_blocked"): return -5.0
        if ctx.flag("application_8_complete"): return 1.0
        if ctx.text("application_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def application_rule_9(self,ctx:RecommendationContext)->float:
        value=ctx.number("application_score",0.0)
        if ctx.flag("application_blocked"): return -5.0
        if ctx.flag("application_9_complete"): return 2.0
        if ctx.text("application_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def application_rule_10(self,ctx:RecommendationContext)->float:
        value=ctx.number("application_score",0.0)
        if ctx.flag("application_blocked"): return -5.0
        if ctx.flag("application_10_complete"): return 3.0
        if ctx.text("application_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def application_rule_11(self,ctx:RecommendationContext)->float:
        value=ctx.number("application_score",0.0)
        if ctx.flag("application_blocked"): return -5.0
        if ctx.flag("application_11_complete"): return 4.0
        if ctx.text("application_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def application_rule_12(self,ctx:RecommendationContext)->float:
        value=ctx.number("application_score",0.0)
        if ctx.flag("application_blocked"): return -5.0
        if ctx.flag("application_12_complete"): return 1.0
        if ctx.text("application_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def application_rule_13(self,ctx:RecommendationContext)->float:
        value=ctx.number("application_score",0.0)
        if ctx.flag("application_blocked"): return -5.0
        if ctx.flag("application_13_complete"): return 2.0
        if ctx.text("application_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def application_rule_14(self,ctx:RecommendationContext)->float:
        value=ctx.number("application_score",0.0)
        if ctx.flag("application_blocked"): return -5.0
        if ctx.flag("application_14_complete"): return 3.0
        if ctx.text("application_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def follow_up_rule_1(self,ctx:RecommendationContext)->float:
        value=ctx.number("follow_up_score",0.0)
        if ctx.flag("follow_up_blocked"): return -5.0
        if ctx.flag("follow_up_1_complete"): return 2.0
        if ctx.text("follow_up_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def follow_up_rule_2(self,ctx:RecommendationContext)->float:
        value=ctx.number("follow_up_score",0.0)
        if ctx.flag("follow_up_blocked"): return -5.0
        if ctx.flag("follow_up_2_complete"): return 3.0
        if ctx.text("follow_up_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def follow_up_rule_3(self,ctx:RecommendationContext)->float:
        value=ctx.number("follow_up_score",0.0)
        if ctx.flag("follow_up_blocked"): return -5.0
        if ctx.flag("follow_up_3_complete"): return 4.0
        if ctx.text("follow_up_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def follow_up_rule_4(self,ctx:RecommendationContext)->float:
        value=ctx.number("follow_up_score",0.0)
        if ctx.flag("follow_up_blocked"): return -5.0
        if ctx.flag("follow_up_4_complete"): return 1.0
        if ctx.text("follow_up_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def follow_up_rule_5(self,ctx:RecommendationContext)->float:
        value=ctx.number("follow_up_score",0.0)
        if ctx.flag("follow_up_blocked"): return -5.0
        if ctx.flag("follow_up_5_complete"): return 2.0
        if ctx.text("follow_up_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def follow_up_rule_6(self,ctx:RecommendationContext)->float:
        value=ctx.number("follow_up_score",0.0)
        if ctx.flag("follow_up_blocked"): return -5.0
        if ctx.flag("follow_up_6_complete"): return 3.0
        if ctx.text("follow_up_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def follow_up_rule_7(self,ctx:RecommendationContext)->float:
        value=ctx.number("follow_up_score",0.0)
        if ctx.flag("follow_up_blocked"): return -5.0
        if ctx.flag("follow_up_7_complete"): return 4.0
        if ctx.text("follow_up_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def follow_up_rule_8(self,ctx:RecommendationContext)->float:
        value=ctx.number("follow_up_score",0.0)
        if ctx.flag("follow_up_blocked"): return -5.0
        if ctx.flag("follow_up_8_complete"): return 1.0
        if ctx.text("follow_up_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def follow_up_rule_9(self,ctx:RecommendationContext)->float:
        value=ctx.number("follow_up_score",0.0)
        if ctx.flag("follow_up_blocked"): return -5.0
        if ctx.flag("follow_up_9_complete"): return 2.0
        if ctx.text("follow_up_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def follow_up_rule_10(self,ctx:RecommendationContext)->float:
        value=ctx.number("follow_up_score",0.0)
        if ctx.flag("follow_up_blocked"): return -5.0
        if ctx.flag("follow_up_10_complete"): return 3.0
        if ctx.text("follow_up_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def follow_up_rule_11(self,ctx:RecommendationContext)->float:
        value=ctx.number("follow_up_score",0.0)
        if ctx.flag("follow_up_blocked"): return -5.0
        if ctx.flag("follow_up_11_complete"): return 4.0
        if ctx.text("follow_up_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def follow_up_rule_12(self,ctx:RecommendationContext)->float:
        value=ctx.number("follow_up_score",0.0)
        if ctx.flag("follow_up_blocked"): return -5.0
        if ctx.flag("follow_up_12_complete"): return 1.0
        if ctx.text("follow_up_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def follow_up_rule_13(self,ctx:RecommendationContext)->float:
        value=ctx.number("follow_up_score",0.0)
        if ctx.flag("follow_up_blocked"): return -5.0
        if ctx.flag("follow_up_13_complete"): return 2.0
        if ctx.text("follow_up_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def follow_up_rule_14(self,ctx:RecommendationContext)->float:
        value=ctx.number("follow_up_score",0.0)
        if ctx.flag("follow_up_blocked"): return -5.0
        if ctx.flag("follow_up_14_complete"): return 3.0
        if ctx.text("follow_up_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def task_rule_1(self,ctx:RecommendationContext)->float:
        value=ctx.number("task_score",0.0)
        if ctx.flag("task_blocked"): return -5.0
        if ctx.flag("task_1_complete"): return 2.0
        if ctx.text("task_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def task_rule_2(self,ctx:RecommendationContext)->float:
        value=ctx.number("task_score",0.0)
        if ctx.flag("task_blocked"): return -5.0
        if ctx.flag("task_2_complete"): return 3.0
        if ctx.text("task_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def task_rule_3(self,ctx:RecommendationContext)->float:
        value=ctx.number("task_score",0.0)
        if ctx.flag("task_blocked"): return -5.0
        if ctx.flag("task_3_complete"): return 4.0
        if ctx.text("task_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def task_rule_4(self,ctx:RecommendationContext)->float:
        value=ctx.number("task_score",0.0)
        if ctx.flag("task_blocked"): return -5.0
        if ctx.flag("task_4_complete"): return 1.0
        if ctx.text("task_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def task_rule_5(self,ctx:RecommendationContext)->float:
        value=ctx.number("task_score",0.0)
        if ctx.flag("task_blocked"): return -5.0
        if ctx.flag("task_5_complete"): return 2.0
        if ctx.text("task_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def task_rule_6(self,ctx:RecommendationContext)->float:
        value=ctx.number("task_score",0.0)
        if ctx.flag("task_blocked"): return -5.0
        if ctx.flag("task_6_complete"): return 3.0
        if ctx.text("task_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def task_rule_7(self,ctx:RecommendationContext)->float:
        value=ctx.number("task_score",0.0)
        if ctx.flag("task_blocked"): return -5.0
        if ctx.flag("task_7_complete"): return 4.0
        if ctx.text("task_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def task_rule_8(self,ctx:RecommendationContext)->float:
        value=ctx.number("task_score",0.0)
        if ctx.flag("task_blocked"): return -5.0
        if ctx.flag("task_8_complete"): return 1.0
        if ctx.text("task_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def task_rule_9(self,ctx:RecommendationContext)->float:
        value=ctx.number("task_score",0.0)
        if ctx.flag("task_blocked"): return -5.0
        if ctx.flag("task_9_complete"): return 2.0
        if ctx.text("task_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def task_rule_10(self,ctx:RecommendationContext)->float:
        value=ctx.number("task_score",0.0)
        if ctx.flag("task_blocked"): return -5.0
        if ctx.flag("task_10_complete"): return 3.0
        if ctx.text("task_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def task_rule_11(self,ctx:RecommendationContext)->float:
        value=ctx.number("task_score",0.0)
        if ctx.flag("task_blocked"): return -5.0
        if ctx.flag("task_11_complete"): return 4.0
        if ctx.text("task_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def task_rule_12(self,ctx:RecommendationContext)->float:
        value=ctx.number("task_score",0.0)
        if ctx.flag("task_blocked"): return -5.0
        if ctx.flag("task_12_complete"): return 1.0
        if ctx.text("task_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def task_rule_13(self,ctx:RecommendationContext)->float:
        value=ctx.number("task_score",0.0)
        if ctx.flag("task_blocked"): return -5.0
        if ctx.flag("task_13_complete"): return 2.0
        if ctx.text("task_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def task_rule_14(self,ctx:RecommendationContext)->float:
        value=ctx.number("task_score",0.0)
        if ctx.flag("task_blocked"): return -5.0
        if ctx.flag("task_14_complete"): return 3.0
        if ctx.text("task_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def interview_rule_1(self,ctx:RecommendationContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_1_complete"): return 2.0
        if ctx.text("interview_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def interview_rule_2(self,ctx:RecommendationContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_2_complete"): return 3.0
        if ctx.text("interview_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def interview_rule_3(self,ctx:RecommendationContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_3_complete"): return 4.0
        if ctx.text("interview_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def interview_rule_4(self,ctx:RecommendationContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_4_complete"): return 1.0
        if ctx.text("interview_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def interview_rule_5(self,ctx:RecommendationContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_5_complete"): return 2.0
        if ctx.text("interview_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def interview_rule_6(self,ctx:RecommendationContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_6_complete"): return 3.0
        if ctx.text("interview_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def interview_rule_7(self,ctx:RecommendationContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_7_complete"): return 4.0
        if ctx.text("interview_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def interview_rule_8(self,ctx:RecommendationContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_8_complete"): return 1.0
        if ctx.text("interview_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def interview_rule_9(self,ctx:RecommendationContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_9_complete"): return 2.0
        if ctx.text("interview_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def interview_rule_10(self,ctx:RecommendationContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_10_complete"): return 3.0
        if ctx.text("interview_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def interview_rule_11(self,ctx:RecommendationContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_11_complete"): return 4.0
        if ctx.text("interview_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def interview_rule_12(self,ctx:RecommendationContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_12_complete"): return 1.0
        if ctx.text("interview_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def interview_rule_13(self,ctx:RecommendationContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_13_complete"): return 2.0
        if ctx.text("interview_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def interview_rule_14(self,ctx:RecommendationContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_14_complete"): return 3.0
        if ctx.text("interview_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def resume_rule_1(self,ctx:RecommendationContext)->float:
        value=ctx.number("resume_score",0.0)
        if ctx.flag("resume_blocked"): return -5.0
        if ctx.flag("resume_1_complete"): return 2.0
        if ctx.text("resume_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def resume_rule_2(self,ctx:RecommendationContext)->float:
        value=ctx.number("resume_score",0.0)
        if ctx.flag("resume_blocked"): return -5.0
        if ctx.flag("resume_2_complete"): return 3.0
        if ctx.text("resume_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def resume_rule_3(self,ctx:RecommendationContext)->float:
        value=ctx.number("resume_score",0.0)
        if ctx.flag("resume_blocked"): return -5.0
        if ctx.flag("resume_3_complete"): return 4.0
        if ctx.text("resume_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def resume_rule_4(self,ctx:RecommendationContext)->float:
        value=ctx.number("resume_score",0.0)
        if ctx.flag("resume_blocked"): return -5.0
        if ctx.flag("resume_4_complete"): return 1.0
        if ctx.text("resume_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def resume_rule_5(self,ctx:RecommendationContext)->float:
        value=ctx.number("resume_score",0.0)
        if ctx.flag("resume_blocked"): return -5.0
        if ctx.flag("resume_5_complete"): return 2.0
        if ctx.text("resume_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def resume_rule_6(self,ctx:RecommendationContext)->float:
        value=ctx.number("resume_score",0.0)
        if ctx.flag("resume_blocked"): return -5.0
        if ctx.flag("resume_6_complete"): return 3.0
        if ctx.text("resume_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def resume_rule_7(self,ctx:RecommendationContext)->float:
        value=ctx.number("resume_score",0.0)
        if ctx.flag("resume_blocked"): return -5.0
        if ctx.flag("resume_7_complete"): return 4.0
        if ctx.text("resume_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def resume_rule_8(self,ctx:RecommendationContext)->float:
        value=ctx.number("resume_score",0.0)
        if ctx.flag("resume_blocked"): return -5.0
        if ctx.flag("resume_8_complete"): return 1.0
        if ctx.text("resume_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def resume_rule_9(self,ctx:RecommendationContext)->float:
        value=ctx.number("resume_score",0.0)
        if ctx.flag("resume_blocked"): return -5.0
        if ctx.flag("resume_9_complete"): return 2.0
        if ctx.text("resume_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def resume_rule_10(self,ctx:RecommendationContext)->float:
        value=ctx.number("resume_score",0.0)
        if ctx.flag("resume_blocked"): return -5.0
        if ctx.flag("resume_10_complete"): return 3.0
        if ctx.text("resume_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def resume_rule_11(self,ctx:RecommendationContext)->float:
        value=ctx.number("resume_score",0.0)
        if ctx.flag("resume_blocked"): return -5.0
        if ctx.flag("resume_11_complete"): return 4.0
        if ctx.text("resume_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def resume_rule_12(self,ctx:RecommendationContext)->float:
        value=ctx.number("resume_score",0.0)
        if ctx.flag("resume_blocked"): return -5.0
        if ctx.flag("resume_12_complete"): return 1.0
        if ctx.text("resume_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def resume_rule_13(self,ctx:RecommendationContext)->float:
        value=ctx.number("resume_score",0.0)
        if ctx.flag("resume_blocked"): return -5.0
        if ctx.flag("resume_13_complete"): return 2.0
        if ctx.text("resume_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def resume_rule_14(self,ctx:RecommendationContext)->float:
        value=ctx.number("resume_score",0.0)
        if ctx.flag("resume_blocked"): return -5.0
        if ctx.flag("resume_14_complete"): return 3.0
        if ctx.text("resume_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def network_rule_1(self,ctx:RecommendationContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_1_complete"): return 2.0
        if ctx.text("network_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def network_rule_2(self,ctx:RecommendationContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_2_complete"): return 3.0
        if ctx.text("network_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def network_rule_3(self,ctx:RecommendationContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_3_complete"): return 4.0
        if ctx.text("network_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def network_rule_4(self,ctx:RecommendationContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_4_complete"): return 1.0
        if ctx.text("network_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def network_rule_5(self,ctx:RecommendationContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_5_complete"): return 2.0
        if ctx.text("network_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def network_rule_6(self,ctx:RecommendationContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_6_complete"): return 3.0
        if ctx.text("network_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def network_rule_7(self,ctx:RecommendationContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_7_complete"): return 4.0
        if ctx.text("network_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def network_rule_8(self,ctx:RecommendationContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_8_complete"): return 1.0
        if ctx.text("network_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def network_rule_9(self,ctx:RecommendationContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_9_complete"): return 2.0
        if ctx.text("network_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def network_rule_10(self,ctx:RecommendationContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_10_complete"): return 3.0
        if ctx.text("network_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def network_rule_11(self,ctx:RecommendationContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_11_complete"): return 4.0
        if ctx.text("network_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def network_rule_12(self,ctx:RecommendationContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_12_complete"): return 1.0
        if ctx.text("network_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def network_rule_13(self,ctx:RecommendationContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_13_complete"): return 2.0
        if ctx.text("network_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def network_rule_14(self,ctx:RecommendationContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_14_complete"): return 3.0
        if ctx.text("network_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def learning_rule_1(self,ctx:RecommendationContext)->float:
        value=ctx.number("learning_score",0.0)
        if ctx.flag("learning_blocked"): return -5.0
        if ctx.flag("learning_1_complete"): return 2.0
        if ctx.text("learning_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def learning_rule_2(self,ctx:RecommendationContext)->float:
        value=ctx.number("learning_score",0.0)
        if ctx.flag("learning_blocked"): return -5.0
        if ctx.flag("learning_2_complete"): return 3.0
        if ctx.text("learning_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def learning_rule_3(self,ctx:RecommendationContext)->float:
        value=ctx.number("learning_score",0.0)
        if ctx.flag("learning_blocked"): return -5.0
        if ctx.flag("learning_3_complete"): return 4.0
        if ctx.text("learning_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def learning_rule_4(self,ctx:RecommendationContext)->float:
        value=ctx.number("learning_score",0.0)
        if ctx.flag("learning_blocked"): return -5.0
        if ctx.flag("learning_4_complete"): return 1.0
        if ctx.text("learning_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def learning_rule_5(self,ctx:RecommendationContext)->float:
        value=ctx.number("learning_score",0.0)
        if ctx.flag("learning_blocked"): return -5.0
        if ctx.flag("learning_5_complete"): return 2.0
        if ctx.text("learning_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def learning_rule_6(self,ctx:RecommendationContext)->float:
        value=ctx.number("learning_score",0.0)
        if ctx.flag("learning_blocked"): return -5.0
        if ctx.flag("learning_6_complete"): return 3.0
        if ctx.text("learning_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def learning_rule_7(self,ctx:RecommendationContext)->float:
        value=ctx.number("learning_score",0.0)
        if ctx.flag("learning_blocked"): return -5.0
        if ctx.flag("learning_7_complete"): return 4.0
        if ctx.text("learning_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def learning_rule_8(self,ctx:RecommendationContext)->float:
        value=ctx.number("learning_score",0.0)
        if ctx.flag("learning_blocked"): return -5.0
        if ctx.flag("learning_8_complete"): return 1.0
        if ctx.text("learning_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def learning_rule_9(self,ctx:RecommendationContext)->float:
        value=ctx.number("learning_score",0.0)
        if ctx.flag("learning_blocked"): return -5.0
        if ctx.flag("learning_9_complete"): return 2.0
        if ctx.text("learning_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def learning_rule_10(self,ctx:RecommendationContext)->float:
        value=ctx.number("learning_score",0.0)
        if ctx.flag("learning_blocked"): return -5.0
        if ctx.flag("learning_10_complete"): return 3.0
        if ctx.text("learning_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def learning_rule_11(self,ctx:RecommendationContext)->float:
        value=ctx.number("learning_score",0.0)
        if ctx.flag("learning_blocked"): return -5.0
        if ctx.flag("learning_11_complete"): return 4.0
        if ctx.text("learning_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def learning_rule_12(self,ctx:RecommendationContext)->float:
        value=ctx.number("learning_score",0.0)
        if ctx.flag("learning_blocked"): return -5.0
        if ctx.flag("learning_12_complete"): return 1.0
        if ctx.text("learning_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def learning_rule_13(self,ctx:RecommendationContext)->float:
        value=ctx.number("learning_score",0.0)
        if ctx.flag("learning_blocked"): return -5.0
        if ctx.flag("learning_13_complete"): return 2.0
        if ctx.text("learning_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def learning_rule_14(self,ctx:RecommendationContext)->float:
        value=ctx.number("learning_score",0.0)
        if ctx.flag("learning_blocked"): return -5.0
        if ctx.flag("learning_14_complete"): return 3.0
        if ctx.text("learning_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def company_rule_1(self,ctx:RecommendationContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_1_complete"): return 2.0
        if ctx.text("company_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def company_rule_2(self,ctx:RecommendationContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_2_complete"): return 3.0
        if ctx.text("company_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def company_rule_3(self,ctx:RecommendationContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_3_complete"): return 4.0
        if ctx.text("company_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def company_rule_4(self,ctx:RecommendationContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_4_complete"): return 1.0
        if ctx.text("company_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def company_rule_5(self,ctx:RecommendationContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_5_complete"): return 2.0
        if ctx.text("company_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def company_rule_6(self,ctx:RecommendationContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_6_complete"): return 3.0
        if ctx.text("company_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def company_rule_7(self,ctx:RecommendationContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_7_complete"): return 4.0
        if ctx.text("company_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def company_rule_8(self,ctx:RecommendationContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_8_complete"): return 1.0
        if ctx.text("company_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def company_rule_9(self,ctx:RecommendationContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_9_complete"): return 2.0
        if ctx.text("company_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def company_rule_10(self,ctx:RecommendationContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_10_complete"): return 3.0
        if ctx.text("company_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def company_rule_11(self,ctx:RecommendationContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_11_complete"): return 4.0
        if ctx.text("company_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def company_rule_12(self,ctx:RecommendationContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_12_complete"): return 1.0
        if ctx.text("company_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def company_rule_13(self,ctx:RecommendationContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_13_complete"): return 2.0
        if ctx.text("company_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def company_rule_14(self,ctx:RecommendationContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_14_complete"): return 3.0
        if ctx.text("company_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def search_rule_1(self,ctx:RecommendationContext)->float:
        value=ctx.number("search_score",0.0)
        if ctx.flag("search_blocked"): return -5.0
        if ctx.flag("search_1_complete"): return 2.0
        if ctx.text("search_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def search_rule_2(self,ctx:RecommendationContext)->float:
        value=ctx.number("search_score",0.0)
        if ctx.flag("search_blocked"): return -5.0
        if ctx.flag("search_2_complete"): return 3.0
        if ctx.text("search_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def search_rule_3(self,ctx:RecommendationContext)->float:
        value=ctx.number("search_score",0.0)
        if ctx.flag("search_blocked"): return -5.0
        if ctx.flag("search_3_complete"): return 4.0
        if ctx.text("search_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def search_rule_4(self,ctx:RecommendationContext)->float:
        value=ctx.number("search_score",0.0)
        if ctx.flag("search_blocked"): return -5.0
        if ctx.flag("search_4_complete"): return 1.0
        if ctx.text("search_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def search_rule_5(self,ctx:RecommendationContext)->float:
        value=ctx.number("search_score",0.0)
        if ctx.flag("search_blocked"): return -5.0
        if ctx.flag("search_5_complete"): return 2.0
        if ctx.text("search_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def search_rule_6(self,ctx:RecommendationContext)->float:
        value=ctx.number("search_score",0.0)
        if ctx.flag("search_blocked"): return -5.0
        if ctx.flag("search_6_complete"): return 3.0
        if ctx.text("search_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def search_rule_7(self,ctx:RecommendationContext)->float:
        value=ctx.number("search_score",0.0)
        if ctx.flag("search_blocked"): return -5.0
        if ctx.flag("search_7_complete"): return 4.0
        if ctx.text("search_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def search_rule_8(self,ctx:RecommendationContext)->float:
        value=ctx.number("search_score",0.0)
        if ctx.flag("search_blocked"): return -5.0
        if ctx.flag("search_8_complete"): return 1.0
        if ctx.text("search_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def search_rule_9(self,ctx:RecommendationContext)->float:
        value=ctx.number("search_score",0.0)
        if ctx.flag("search_blocked"): return -5.0
        if ctx.flag("search_9_complete"): return 2.0
        if ctx.text("search_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def search_rule_10(self,ctx:RecommendationContext)->float:
        value=ctx.number("search_score",0.0)
        if ctx.flag("search_blocked"): return -5.0
        if ctx.flag("search_10_complete"): return 3.0
        if ctx.text("search_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def search_rule_11(self,ctx:RecommendationContext)->float:
        value=ctx.number("search_score",0.0)
        if ctx.flag("search_blocked"): return -5.0
        if ctx.flag("search_11_complete"): return 4.0
        if ctx.text("search_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def search_rule_12(self,ctx:RecommendationContext)->float:
        value=ctx.number("search_score",0.0)
        if ctx.flag("search_blocked"): return -5.0
        if ctx.flag("search_12_complete"): return 1.0
        if ctx.text("search_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def search_rule_13(self,ctx:RecommendationContext)->float:
        value=ctx.number("search_score",0.0)
        if ctx.flag("search_blocked"): return -5.0
        if ctx.flag("search_13_complete"): return 2.0
        if ctx.text("search_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def search_rule_14(self,ctx:RecommendationContext)->float:
        value=ctx.number("search_score",0.0)
        if ctx.flag("search_blocked"): return -5.0
        if ctx.flag("search_14_complete"): return 3.0
        if ctx.text("search_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def evaluate_many(self,records:Sequence[Mapping[str,object]])->list[RecommendationResult]:
        return [self.evaluate(record) for record in records]
    def summarize(self,results:Sequence[RecommendationResult])->dict[str,object]:
        scores=[item.score for item in results]
        return {"count":len(scores),"average":round(sum(scores)/len(scores),2) if scores else 0.0,"strong":sum(x.status=="strong" for x in results),"acceptable":sum(x.status=="acceptable" for x in results),"review":sum(x.status=="review" for x in results)}
