"""Deterministic followup domain engine for job-search workflows."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Mapping, Sequence

@dataclass(frozen=True)
class FollowupResult:
    key: str
    score: float
    status: str
    reasons: tuple[str, ...] = ()

@dataclass
class FollowupContext:
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

class FollowupEngine:
    def evaluate(self, context:Mapping[str,object]|FollowupContext|None=None)->FollowupResult:
        ctx=context if isinstance(context,FollowupContext) else FollowupContext(dict(context or {}))
        score=50.0; reasons=[]
        for area in ["initial","screening","interview","post_interview","offer","rejection","no_response","recruiter","hiring_manager","referral","network","final"]:
            delta=self._area_score(area,ctx); score+=delta
            if delta>0: reasons.append(f"{area}: positive")
            if delta<0: reasons.append(f"{area}: review")
        score=clamp(score)
        status="strong" if score>=80 else "acceptable" if score>=60 else "review"
        return FollowupResult("overall",round(score,2),status,tuple(reasons))
    def _area_score(self,area:str,ctx:FollowupContext)->float:
        if ctx.flag(f"{area}_blocked"): return -5.0
        if ctx.flag(f"{area}_complete"): return 3.0
        if ctx.text(area): return 1.0
        return -1.0
    def initial_rule_1(self,ctx:FollowupContext)->float:
        value=ctx.number("initial_score",0.0)
        if ctx.flag("initial_blocked"): return -5.0
        if ctx.flag("initial_1_complete"): return 2.0
        if ctx.text("initial_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def initial_rule_2(self,ctx:FollowupContext)->float:
        value=ctx.number("initial_score",0.0)
        if ctx.flag("initial_blocked"): return -5.0
        if ctx.flag("initial_2_complete"): return 3.0
        if ctx.text("initial_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def initial_rule_3(self,ctx:FollowupContext)->float:
        value=ctx.number("initial_score",0.0)
        if ctx.flag("initial_blocked"): return -5.0
        if ctx.flag("initial_3_complete"): return 4.0
        if ctx.text("initial_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def initial_rule_4(self,ctx:FollowupContext)->float:
        value=ctx.number("initial_score",0.0)
        if ctx.flag("initial_blocked"): return -5.0
        if ctx.flag("initial_4_complete"): return 1.0
        if ctx.text("initial_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def initial_rule_5(self,ctx:FollowupContext)->float:
        value=ctx.number("initial_score",0.0)
        if ctx.flag("initial_blocked"): return -5.0
        if ctx.flag("initial_5_complete"): return 2.0
        if ctx.text("initial_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def initial_rule_6(self,ctx:FollowupContext)->float:
        value=ctx.number("initial_score",0.0)
        if ctx.flag("initial_blocked"): return -5.0
        if ctx.flag("initial_6_complete"): return 3.0
        if ctx.text("initial_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def initial_rule_7(self,ctx:FollowupContext)->float:
        value=ctx.number("initial_score",0.0)
        if ctx.flag("initial_blocked"): return -5.0
        if ctx.flag("initial_7_complete"): return 4.0
        if ctx.text("initial_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def initial_rule_8(self,ctx:FollowupContext)->float:
        value=ctx.number("initial_score",0.0)
        if ctx.flag("initial_blocked"): return -5.0
        if ctx.flag("initial_8_complete"): return 1.0
        if ctx.text("initial_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def initial_rule_9(self,ctx:FollowupContext)->float:
        value=ctx.number("initial_score",0.0)
        if ctx.flag("initial_blocked"): return -5.0
        if ctx.flag("initial_9_complete"): return 2.0
        if ctx.text("initial_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def initial_rule_10(self,ctx:FollowupContext)->float:
        value=ctx.number("initial_score",0.0)
        if ctx.flag("initial_blocked"): return -5.0
        if ctx.flag("initial_10_complete"): return 3.0
        if ctx.text("initial_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def initial_rule_11(self,ctx:FollowupContext)->float:
        value=ctx.number("initial_score",0.0)
        if ctx.flag("initial_blocked"): return -5.0
        if ctx.flag("initial_11_complete"): return 4.0
        if ctx.text("initial_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def initial_rule_12(self,ctx:FollowupContext)->float:
        value=ctx.number("initial_score",0.0)
        if ctx.flag("initial_blocked"): return -5.0
        if ctx.flag("initial_12_complete"): return 1.0
        if ctx.text("initial_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def initial_rule_13(self,ctx:FollowupContext)->float:
        value=ctx.number("initial_score",0.0)
        if ctx.flag("initial_blocked"): return -5.0
        if ctx.flag("initial_13_complete"): return 2.0
        if ctx.text("initial_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def initial_rule_14(self,ctx:FollowupContext)->float:
        value=ctx.number("initial_score",0.0)
        if ctx.flag("initial_blocked"): return -5.0
        if ctx.flag("initial_14_complete"): return 3.0
        if ctx.text("initial_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def screening_rule_1(self,ctx:FollowupContext)->float:
        value=ctx.number("screening_score",0.0)
        if ctx.flag("screening_blocked"): return -5.0
        if ctx.flag("screening_1_complete"): return 2.0
        if ctx.text("screening_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def screening_rule_2(self,ctx:FollowupContext)->float:
        value=ctx.number("screening_score",0.0)
        if ctx.flag("screening_blocked"): return -5.0
        if ctx.flag("screening_2_complete"): return 3.0
        if ctx.text("screening_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def screening_rule_3(self,ctx:FollowupContext)->float:
        value=ctx.number("screening_score",0.0)
        if ctx.flag("screening_blocked"): return -5.0
        if ctx.flag("screening_3_complete"): return 4.0
        if ctx.text("screening_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def screening_rule_4(self,ctx:FollowupContext)->float:
        value=ctx.number("screening_score",0.0)
        if ctx.flag("screening_blocked"): return -5.0
        if ctx.flag("screening_4_complete"): return 1.0
        if ctx.text("screening_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def screening_rule_5(self,ctx:FollowupContext)->float:
        value=ctx.number("screening_score",0.0)
        if ctx.flag("screening_blocked"): return -5.0
        if ctx.flag("screening_5_complete"): return 2.0
        if ctx.text("screening_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def screening_rule_6(self,ctx:FollowupContext)->float:
        value=ctx.number("screening_score",0.0)
        if ctx.flag("screening_blocked"): return -5.0
        if ctx.flag("screening_6_complete"): return 3.0
        if ctx.text("screening_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def screening_rule_7(self,ctx:FollowupContext)->float:
        value=ctx.number("screening_score",0.0)
        if ctx.flag("screening_blocked"): return -5.0
        if ctx.flag("screening_7_complete"): return 4.0
        if ctx.text("screening_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def screening_rule_8(self,ctx:FollowupContext)->float:
        value=ctx.number("screening_score",0.0)
        if ctx.flag("screening_blocked"): return -5.0
        if ctx.flag("screening_8_complete"): return 1.0
        if ctx.text("screening_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def screening_rule_9(self,ctx:FollowupContext)->float:
        value=ctx.number("screening_score",0.0)
        if ctx.flag("screening_blocked"): return -5.0
        if ctx.flag("screening_9_complete"): return 2.0
        if ctx.text("screening_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def screening_rule_10(self,ctx:FollowupContext)->float:
        value=ctx.number("screening_score",0.0)
        if ctx.flag("screening_blocked"): return -5.0
        if ctx.flag("screening_10_complete"): return 3.0
        if ctx.text("screening_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def screening_rule_11(self,ctx:FollowupContext)->float:
        value=ctx.number("screening_score",0.0)
        if ctx.flag("screening_blocked"): return -5.0
        if ctx.flag("screening_11_complete"): return 4.0
        if ctx.text("screening_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def screening_rule_12(self,ctx:FollowupContext)->float:
        value=ctx.number("screening_score",0.0)
        if ctx.flag("screening_blocked"): return -5.0
        if ctx.flag("screening_12_complete"): return 1.0
        if ctx.text("screening_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def screening_rule_13(self,ctx:FollowupContext)->float:
        value=ctx.number("screening_score",0.0)
        if ctx.flag("screening_blocked"): return -5.0
        if ctx.flag("screening_13_complete"): return 2.0
        if ctx.text("screening_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def screening_rule_14(self,ctx:FollowupContext)->float:
        value=ctx.number("screening_score",0.0)
        if ctx.flag("screening_blocked"): return -5.0
        if ctx.flag("screening_14_complete"): return 3.0
        if ctx.text("screening_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def interview_rule_1(self,ctx:FollowupContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_1_complete"): return 2.0
        if ctx.text("interview_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def interview_rule_2(self,ctx:FollowupContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_2_complete"): return 3.0
        if ctx.text("interview_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def interview_rule_3(self,ctx:FollowupContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_3_complete"): return 4.0
        if ctx.text("interview_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def interview_rule_4(self,ctx:FollowupContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_4_complete"): return 1.0
        if ctx.text("interview_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def interview_rule_5(self,ctx:FollowupContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_5_complete"): return 2.0
        if ctx.text("interview_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def interview_rule_6(self,ctx:FollowupContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_6_complete"): return 3.0
        if ctx.text("interview_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def interview_rule_7(self,ctx:FollowupContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_7_complete"): return 4.0
        if ctx.text("interview_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def interview_rule_8(self,ctx:FollowupContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_8_complete"): return 1.0
        if ctx.text("interview_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def interview_rule_9(self,ctx:FollowupContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_9_complete"): return 2.0
        if ctx.text("interview_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def interview_rule_10(self,ctx:FollowupContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_10_complete"): return 3.0
        if ctx.text("interview_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def interview_rule_11(self,ctx:FollowupContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_11_complete"): return 4.0
        if ctx.text("interview_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def interview_rule_12(self,ctx:FollowupContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_12_complete"): return 1.0
        if ctx.text("interview_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def interview_rule_13(self,ctx:FollowupContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_13_complete"): return 2.0
        if ctx.text("interview_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def interview_rule_14(self,ctx:FollowupContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_14_complete"): return 3.0
        if ctx.text("interview_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def post_interview_rule_1(self,ctx:FollowupContext)->float:
        value=ctx.number("post_interview_score",0.0)
        if ctx.flag("post_interview_blocked"): return -5.0
        if ctx.flag("post_interview_1_complete"): return 2.0
        if ctx.text("post_interview_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def post_interview_rule_2(self,ctx:FollowupContext)->float:
        value=ctx.number("post_interview_score",0.0)
        if ctx.flag("post_interview_blocked"): return -5.0
        if ctx.flag("post_interview_2_complete"): return 3.0
        if ctx.text("post_interview_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def post_interview_rule_3(self,ctx:FollowupContext)->float:
        value=ctx.number("post_interview_score",0.0)
        if ctx.flag("post_interview_blocked"): return -5.0
        if ctx.flag("post_interview_3_complete"): return 4.0
        if ctx.text("post_interview_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def post_interview_rule_4(self,ctx:FollowupContext)->float:
        value=ctx.number("post_interview_score",0.0)
        if ctx.flag("post_interview_blocked"): return -5.0
        if ctx.flag("post_interview_4_complete"): return 1.0
        if ctx.text("post_interview_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def post_interview_rule_5(self,ctx:FollowupContext)->float:
        value=ctx.number("post_interview_score",0.0)
        if ctx.flag("post_interview_blocked"): return -5.0
        if ctx.flag("post_interview_5_complete"): return 2.0
        if ctx.text("post_interview_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def post_interview_rule_6(self,ctx:FollowupContext)->float:
        value=ctx.number("post_interview_score",0.0)
        if ctx.flag("post_interview_blocked"): return -5.0
        if ctx.flag("post_interview_6_complete"): return 3.0
        if ctx.text("post_interview_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def post_interview_rule_7(self,ctx:FollowupContext)->float:
        value=ctx.number("post_interview_score",0.0)
        if ctx.flag("post_interview_blocked"): return -5.0
        if ctx.flag("post_interview_7_complete"): return 4.0
        if ctx.text("post_interview_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def post_interview_rule_8(self,ctx:FollowupContext)->float:
        value=ctx.number("post_interview_score",0.0)
        if ctx.flag("post_interview_blocked"): return -5.0
        if ctx.flag("post_interview_8_complete"): return 1.0
        if ctx.text("post_interview_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def post_interview_rule_9(self,ctx:FollowupContext)->float:
        value=ctx.number("post_interview_score",0.0)
        if ctx.flag("post_interview_blocked"): return -5.0
        if ctx.flag("post_interview_9_complete"): return 2.0
        if ctx.text("post_interview_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def post_interview_rule_10(self,ctx:FollowupContext)->float:
        value=ctx.number("post_interview_score",0.0)
        if ctx.flag("post_interview_blocked"): return -5.0
        if ctx.flag("post_interview_10_complete"): return 3.0
        if ctx.text("post_interview_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def post_interview_rule_11(self,ctx:FollowupContext)->float:
        value=ctx.number("post_interview_score",0.0)
        if ctx.flag("post_interview_blocked"): return -5.0
        if ctx.flag("post_interview_11_complete"): return 4.0
        if ctx.text("post_interview_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def post_interview_rule_12(self,ctx:FollowupContext)->float:
        value=ctx.number("post_interview_score",0.0)
        if ctx.flag("post_interview_blocked"): return -5.0
        if ctx.flag("post_interview_12_complete"): return 1.0
        if ctx.text("post_interview_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def post_interview_rule_13(self,ctx:FollowupContext)->float:
        value=ctx.number("post_interview_score",0.0)
        if ctx.flag("post_interview_blocked"): return -5.0
        if ctx.flag("post_interview_13_complete"): return 2.0
        if ctx.text("post_interview_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def post_interview_rule_14(self,ctx:FollowupContext)->float:
        value=ctx.number("post_interview_score",0.0)
        if ctx.flag("post_interview_blocked"): return -5.0
        if ctx.flag("post_interview_14_complete"): return 3.0
        if ctx.text("post_interview_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def offer_rule_1(self,ctx:FollowupContext)->float:
        value=ctx.number("offer_score",0.0)
        if ctx.flag("offer_blocked"): return -5.0
        if ctx.flag("offer_1_complete"): return 2.0
        if ctx.text("offer_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def offer_rule_2(self,ctx:FollowupContext)->float:
        value=ctx.number("offer_score",0.0)
        if ctx.flag("offer_blocked"): return -5.0
        if ctx.flag("offer_2_complete"): return 3.0
        if ctx.text("offer_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def offer_rule_3(self,ctx:FollowupContext)->float:
        value=ctx.number("offer_score",0.0)
        if ctx.flag("offer_blocked"): return -5.0
        if ctx.flag("offer_3_complete"): return 4.0
        if ctx.text("offer_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def offer_rule_4(self,ctx:FollowupContext)->float:
        value=ctx.number("offer_score",0.0)
        if ctx.flag("offer_blocked"): return -5.0
        if ctx.flag("offer_4_complete"): return 1.0
        if ctx.text("offer_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def offer_rule_5(self,ctx:FollowupContext)->float:
        value=ctx.number("offer_score",0.0)
        if ctx.flag("offer_blocked"): return -5.0
        if ctx.flag("offer_5_complete"): return 2.0
        if ctx.text("offer_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def offer_rule_6(self,ctx:FollowupContext)->float:
        value=ctx.number("offer_score",0.0)
        if ctx.flag("offer_blocked"): return -5.0
        if ctx.flag("offer_6_complete"): return 3.0
        if ctx.text("offer_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def offer_rule_7(self,ctx:FollowupContext)->float:
        value=ctx.number("offer_score",0.0)
        if ctx.flag("offer_blocked"): return -5.0
        if ctx.flag("offer_7_complete"): return 4.0
        if ctx.text("offer_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def offer_rule_8(self,ctx:FollowupContext)->float:
        value=ctx.number("offer_score",0.0)
        if ctx.flag("offer_blocked"): return -5.0
        if ctx.flag("offer_8_complete"): return 1.0
        if ctx.text("offer_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def offer_rule_9(self,ctx:FollowupContext)->float:
        value=ctx.number("offer_score",0.0)
        if ctx.flag("offer_blocked"): return -5.0
        if ctx.flag("offer_9_complete"): return 2.0
        if ctx.text("offer_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def offer_rule_10(self,ctx:FollowupContext)->float:
        value=ctx.number("offer_score",0.0)
        if ctx.flag("offer_blocked"): return -5.0
        if ctx.flag("offer_10_complete"): return 3.0
        if ctx.text("offer_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def offer_rule_11(self,ctx:FollowupContext)->float:
        value=ctx.number("offer_score",0.0)
        if ctx.flag("offer_blocked"): return -5.0
        if ctx.flag("offer_11_complete"): return 4.0
        if ctx.text("offer_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def offer_rule_12(self,ctx:FollowupContext)->float:
        value=ctx.number("offer_score",0.0)
        if ctx.flag("offer_blocked"): return -5.0
        if ctx.flag("offer_12_complete"): return 1.0
        if ctx.text("offer_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def offer_rule_13(self,ctx:FollowupContext)->float:
        value=ctx.number("offer_score",0.0)
        if ctx.flag("offer_blocked"): return -5.0
        if ctx.flag("offer_13_complete"): return 2.0
        if ctx.text("offer_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def offer_rule_14(self,ctx:FollowupContext)->float:
        value=ctx.number("offer_score",0.0)
        if ctx.flag("offer_blocked"): return -5.0
        if ctx.flag("offer_14_complete"): return 3.0
        if ctx.text("offer_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def rejection_rule_1(self,ctx:FollowupContext)->float:
        value=ctx.number("rejection_score",0.0)
        if ctx.flag("rejection_blocked"): return -5.0
        if ctx.flag("rejection_1_complete"): return 2.0
        if ctx.text("rejection_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def rejection_rule_2(self,ctx:FollowupContext)->float:
        value=ctx.number("rejection_score",0.0)
        if ctx.flag("rejection_blocked"): return -5.0
        if ctx.flag("rejection_2_complete"): return 3.0
        if ctx.text("rejection_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def rejection_rule_3(self,ctx:FollowupContext)->float:
        value=ctx.number("rejection_score",0.0)
        if ctx.flag("rejection_blocked"): return -5.0
        if ctx.flag("rejection_3_complete"): return 4.0
        if ctx.text("rejection_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def rejection_rule_4(self,ctx:FollowupContext)->float:
        value=ctx.number("rejection_score",0.0)
        if ctx.flag("rejection_blocked"): return -5.0
        if ctx.flag("rejection_4_complete"): return 1.0
        if ctx.text("rejection_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def rejection_rule_5(self,ctx:FollowupContext)->float:
        value=ctx.number("rejection_score",0.0)
        if ctx.flag("rejection_blocked"): return -5.0
        if ctx.flag("rejection_5_complete"): return 2.0
        if ctx.text("rejection_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def rejection_rule_6(self,ctx:FollowupContext)->float:
        value=ctx.number("rejection_score",0.0)
        if ctx.flag("rejection_blocked"): return -5.0
        if ctx.flag("rejection_6_complete"): return 3.0
        if ctx.text("rejection_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def rejection_rule_7(self,ctx:FollowupContext)->float:
        value=ctx.number("rejection_score",0.0)
        if ctx.flag("rejection_blocked"): return -5.0
        if ctx.flag("rejection_7_complete"): return 4.0
        if ctx.text("rejection_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def rejection_rule_8(self,ctx:FollowupContext)->float:
        value=ctx.number("rejection_score",0.0)
        if ctx.flag("rejection_blocked"): return -5.0
        if ctx.flag("rejection_8_complete"): return 1.0
        if ctx.text("rejection_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def rejection_rule_9(self,ctx:FollowupContext)->float:
        value=ctx.number("rejection_score",0.0)
        if ctx.flag("rejection_blocked"): return -5.0
        if ctx.flag("rejection_9_complete"): return 2.0
        if ctx.text("rejection_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def rejection_rule_10(self,ctx:FollowupContext)->float:
        value=ctx.number("rejection_score",0.0)
        if ctx.flag("rejection_blocked"): return -5.0
        if ctx.flag("rejection_10_complete"): return 3.0
        if ctx.text("rejection_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def rejection_rule_11(self,ctx:FollowupContext)->float:
        value=ctx.number("rejection_score",0.0)
        if ctx.flag("rejection_blocked"): return -5.0
        if ctx.flag("rejection_11_complete"): return 4.0
        if ctx.text("rejection_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def rejection_rule_12(self,ctx:FollowupContext)->float:
        value=ctx.number("rejection_score",0.0)
        if ctx.flag("rejection_blocked"): return -5.0
        if ctx.flag("rejection_12_complete"): return 1.0
        if ctx.text("rejection_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def rejection_rule_13(self,ctx:FollowupContext)->float:
        value=ctx.number("rejection_score",0.0)
        if ctx.flag("rejection_blocked"): return -5.0
        if ctx.flag("rejection_13_complete"): return 2.0
        if ctx.text("rejection_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def rejection_rule_14(self,ctx:FollowupContext)->float:
        value=ctx.number("rejection_score",0.0)
        if ctx.flag("rejection_blocked"): return -5.0
        if ctx.flag("rejection_14_complete"): return 3.0
        if ctx.text("rejection_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def no_response_rule_1(self,ctx:FollowupContext)->float:
        value=ctx.number("no_response_score",0.0)
        if ctx.flag("no_response_blocked"): return -5.0
        if ctx.flag("no_response_1_complete"): return 2.0
        if ctx.text("no_response_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def no_response_rule_2(self,ctx:FollowupContext)->float:
        value=ctx.number("no_response_score",0.0)
        if ctx.flag("no_response_blocked"): return -5.0
        if ctx.flag("no_response_2_complete"): return 3.0
        if ctx.text("no_response_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def no_response_rule_3(self,ctx:FollowupContext)->float:
        value=ctx.number("no_response_score",0.0)
        if ctx.flag("no_response_blocked"): return -5.0
        if ctx.flag("no_response_3_complete"): return 4.0
        if ctx.text("no_response_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def no_response_rule_4(self,ctx:FollowupContext)->float:
        value=ctx.number("no_response_score",0.0)
        if ctx.flag("no_response_blocked"): return -5.0
        if ctx.flag("no_response_4_complete"): return 1.0
        if ctx.text("no_response_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def no_response_rule_5(self,ctx:FollowupContext)->float:
        value=ctx.number("no_response_score",0.0)
        if ctx.flag("no_response_blocked"): return -5.0
        if ctx.flag("no_response_5_complete"): return 2.0
        if ctx.text("no_response_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def no_response_rule_6(self,ctx:FollowupContext)->float:
        value=ctx.number("no_response_score",0.0)
        if ctx.flag("no_response_blocked"): return -5.0
        if ctx.flag("no_response_6_complete"): return 3.0
        if ctx.text("no_response_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def no_response_rule_7(self,ctx:FollowupContext)->float:
        value=ctx.number("no_response_score",0.0)
        if ctx.flag("no_response_blocked"): return -5.0
        if ctx.flag("no_response_7_complete"): return 4.0
        if ctx.text("no_response_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def no_response_rule_8(self,ctx:FollowupContext)->float:
        value=ctx.number("no_response_score",0.0)
        if ctx.flag("no_response_blocked"): return -5.0
        if ctx.flag("no_response_8_complete"): return 1.0
        if ctx.text("no_response_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def no_response_rule_9(self,ctx:FollowupContext)->float:
        value=ctx.number("no_response_score",0.0)
        if ctx.flag("no_response_blocked"): return -5.0
        if ctx.flag("no_response_9_complete"): return 2.0
        if ctx.text("no_response_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def no_response_rule_10(self,ctx:FollowupContext)->float:
        value=ctx.number("no_response_score",0.0)
        if ctx.flag("no_response_blocked"): return -5.0
        if ctx.flag("no_response_10_complete"): return 3.0
        if ctx.text("no_response_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def no_response_rule_11(self,ctx:FollowupContext)->float:
        value=ctx.number("no_response_score",0.0)
        if ctx.flag("no_response_blocked"): return -5.0
        if ctx.flag("no_response_11_complete"): return 4.0
        if ctx.text("no_response_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def no_response_rule_12(self,ctx:FollowupContext)->float:
        value=ctx.number("no_response_score",0.0)
        if ctx.flag("no_response_blocked"): return -5.0
        if ctx.flag("no_response_12_complete"): return 1.0
        if ctx.text("no_response_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def no_response_rule_13(self,ctx:FollowupContext)->float:
        value=ctx.number("no_response_score",0.0)
        if ctx.flag("no_response_blocked"): return -5.0
        if ctx.flag("no_response_13_complete"): return 2.0
        if ctx.text("no_response_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def no_response_rule_14(self,ctx:FollowupContext)->float:
        value=ctx.number("no_response_score",0.0)
        if ctx.flag("no_response_blocked"): return -5.0
        if ctx.flag("no_response_14_complete"): return 3.0
        if ctx.text("no_response_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def recruiter_rule_1(self,ctx:FollowupContext)->float:
        value=ctx.number("recruiter_score",0.0)
        if ctx.flag("recruiter_blocked"): return -5.0
        if ctx.flag("recruiter_1_complete"): return 2.0
        if ctx.text("recruiter_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def recruiter_rule_2(self,ctx:FollowupContext)->float:
        value=ctx.number("recruiter_score",0.0)
        if ctx.flag("recruiter_blocked"): return -5.0
        if ctx.flag("recruiter_2_complete"): return 3.0
        if ctx.text("recruiter_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def recruiter_rule_3(self,ctx:FollowupContext)->float:
        value=ctx.number("recruiter_score",0.0)
        if ctx.flag("recruiter_blocked"): return -5.0
        if ctx.flag("recruiter_3_complete"): return 4.0
        if ctx.text("recruiter_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def recruiter_rule_4(self,ctx:FollowupContext)->float:
        value=ctx.number("recruiter_score",0.0)
        if ctx.flag("recruiter_blocked"): return -5.0
        if ctx.flag("recruiter_4_complete"): return 1.0
        if ctx.text("recruiter_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def recruiter_rule_5(self,ctx:FollowupContext)->float:
        value=ctx.number("recruiter_score",0.0)
        if ctx.flag("recruiter_blocked"): return -5.0
        if ctx.flag("recruiter_5_complete"): return 2.0
        if ctx.text("recruiter_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def recruiter_rule_6(self,ctx:FollowupContext)->float:
        value=ctx.number("recruiter_score",0.0)
        if ctx.flag("recruiter_blocked"): return -5.0
        if ctx.flag("recruiter_6_complete"): return 3.0
        if ctx.text("recruiter_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def recruiter_rule_7(self,ctx:FollowupContext)->float:
        value=ctx.number("recruiter_score",0.0)
        if ctx.flag("recruiter_blocked"): return -5.0
        if ctx.flag("recruiter_7_complete"): return 4.0
        if ctx.text("recruiter_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def recruiter_rule_8(self,ctx:FollowupContext)->float:
        value=ctx.number("recruiter_score",0.0)
        if ctx.flag("recruiter_blocked"): return -5.0
        if ctx.flag("recruiter_8_complete"): return 1.0
        if ctx.text("recruiter_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def recruiter_rule_9(self,ctx:FollowupContext)->float:
        value=ctx.number("recruiter_score",0.0)
        if ctx.flag("recruiter_blocked"): return -5.0
        if ctx.flag("recruiter_9_complete"): return 2.0
        if ctx.text("recruiter_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def recruiter_rule_10(self,ctx:FollowupContext)->float:
        value=ctx.number("recruiter_score",0.0)
        if ctx.flag("recruiter_blocked"): return -5.0
        if ctx.flag("recruiter_10_complete"): return 3.0
        if ctx.text("recruiter_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def recruiter_rule_11(self,ctx:FollowupContext)->float:
        value=ctx.number("recruiter_score",0.0)
        if ctx.flag("recruiter_blocked"): return -5.0
        if ctx.flag("recruiter_11_complete"): return 4.0
        if ctx.text("recruiter_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def recruiter_rule_12(self,ctx:FollowupContext)->float:
        value=ctx.number("recruiter_score",0.0)
        if ctx.flag("recruiter_blocked"): return -5.0
        if ctx.flag("recruiter_12_complete"): return 1.0
        if ctx.text("recruiter_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def recruiter_rule_13(self,ctx:FollowupContext)->float:
        value=ctx.number("recruiter_score",0.0)
        if ctx.flag("recruiter_blocked"): return -5.0
        if ctx.flag("recruiter_13_complete"): return 2.0
        if ctx.text("recruiter_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def recruiter_rule_14(self,ctx:FollowupContext)->float:
        value=ctx.number("recruiter_score",0.0)
        if ctx.flag("recruiter_blocked"): return -5.0
        if ctx.flag("recruiter_14_complete"): return 3.0
        if ctx.text("recruiter_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def hiring_manager_rule_1(self,ctx:FollowupContext)->float:
        value=ctx.number("hiring_manager_score",0.0)
        if ctx.flag("hiring_manager_blocked"): return -5.0
        if ctx.flag("hiring_manager_1_complete"): return 2.0
        if ctx.text("hiring_manager_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def hiring_manager_rule_2(self,ctx:FollowupContext)->float:
        value=ctx.number("hiring_manager_score",0.0)
        if ctx.flag("hiring_manager_blocked"): return -5.0
        if ctx.flag("hiring_manager_2_complete"): return 3.0
        if ctx.text("hiring_manager_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def hiring_manager_rule_3(self,ctx:FollowupContext)->float:
        value=ctx.number("hiring_manager_score",0.0)
        if ctx.flag("hiring_manager_blocked"): return -5.0
        if ctx.flag("hiring_manager_3_complete"): return 4.0
        if ctx.text("hiring_manager_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def hiring_manager_rule_4(self,ctx:FollowupContext)->float:
        value=ctx.number("hiring_manager_score",0.0)
        if ctx.flag("hiring_manager_blocked"): return -5.0
        if ctx.flag("hiring_manager_4_complete"): return 1.0
        if ctx.text("hiring_manager_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def hiring_manager_rule_5(self,ctx:FollowupContext)->float:
        value=ctx.number("hiring_manager_score",0.0)
        if ctx.flag("hiring_manager_blocked"): return -5.0
        if ctx.flag("hiring_manager_5_complete"): return 2.0
        if ctx.text("hiring_manager_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def hiring_manager_rule_6(self,ctx:FollowupContext)->float:
        value=ctx.number("hiring_manager_score",0.0)
        if ctx.flag("hiring_manager_blocked"): return -5.0
        if ctx.flag("hiring_manager_6_complete"): return 3.0
        if ctx.text("hiring_manager_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def hiring_manager_rule_7(self,ctx:FollowupContext)->float:
        value=ctx.number("hiring_manager_score",0.0)
        if ctx.flag("hiring_manager_blocked"): return -5.0
        if ctx.flag("hiring_manager_7_complete"): return 4.0
        if ctx.text("hiring_manager_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def hiring_manager_rule_8(self,ctx:FollowupContext)->float:
        value=ctx.number("hiring_manager_score",0.0)
        if ctx.flag("hiring_manager_blocked"): return -5.0
        if ctx.flag("hiring_manager_8_complete"): return 1.0
        if ctx.text("hiring_manager_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def hiring_manager_rule_9(self,ctx:FollowupContext)->float:
        value=ctx.number("hiring_manager_score",0.0)
        if ctx.flag("hiring_manager_blocked"): return -5.0
        if ctx.flag("hiring_manager_9_complete"): return 2.0
        if ctx.text("hiring_manager_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def hiring_manager_rule_10(self,ctx:FollowupContext)->float:
        value=ctx.number("hiring_manager_score",0.0)
        if ctx.flag("hiring_manager_blocked"): return -5.0
        if ctx.flag("hiring_manager_10_complete"): return 3.0
        if ctx.text("hiring_manager_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def hiring_manager_rule_11(self,ctx:FollowupContext)->float:
        value=ctx.number("hiring_manager_score",0.0)
        if ctx.flag("hiring_manager_blocked"): return -5.0
        if ctx.flag("hiring_manager_11_complete"): return 4.0
        if ctx.text("hiring_manager_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def hiring_manager_rule_12(self,ctx:FollowupContext)->float:
        value=ctx.number("hiring_manager_score",0.0)
        if ctx.flag("hiring_manager_blocked"): return -5.0
        if ctx.flag("hiring_manager_12_complete"): return 1.0
        if ctx.text("hiring_manager_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def hiring_manager_rule_13(self,ctx:FollowupContext)->float:
        value=ctx.number("hiring_manager_score",0.0)
        if ctx.flag("hiring_manager_blocked"): return -5.0
        if ctx.flag("hiring_manager_13_complete"): return 2.0
        if ctx.text("hiring_manager_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def hiring_manager_rule_14(self,ctx:FollowupContext)->float:
        value=ctx.number("hiring_manager_score",0.0)
        if ctx.flag("hiring_manager_blocked"): return -5.0
        if ctx.flag("hiring_manager_14_complete"): return 3.0
        if ctx.text("hiring_manager_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def referral_rule_1(self,ctx:FollowupContext)->float:
        value=ctx.number("referral_score",0.0)
        if ctx.flag("referral_blocked"): return -5.0
        if ctx.flag("referral_1_complete"): return 2.0
        if ctx.text("referral_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def referral_rule_2(self,ctx:FollowupContext)->float:
        value=ctx.number("referral_score",0.0)
        if ctx.flag("referral_blocked"): return -5.0
        if ctx.flag("referral_2_complete"): return 3.0
        if ctx.text("referral_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def referral_rule_3(self,ctx:FollowupContext)->float:
        value=ctx.number("referral_score",0.0)
        if ctx.flag("referral_blocked"): return -5.0
        if ctx.flag("referral_3_complete"): return 4.0
        if ctx.text("referral_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def referral_rule_4(self,ctx:FollowupContext)->float:
        value=ctx.number("referral_score",0.0)
        if ctx.flag("referral_blocked"): return -5.0
        if ctx.flag("referral_4_complete"): return 1.0
        if ctx.text("referral_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def referral_rule_5(self,ctx:FollowupContext)->float:
        value=ctx.number("referral_score",0.0)
        if ctx.flag("referral_blocked"): return -5.0
        if ctx.flag("referral_5_complete"): return 2.0
        if ctx.text("referral_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def referral_rule_6(self,ctx:FollowupContext)->float:
        value=ctx.number("referral_score",0.0)
        if ctx.flag("referral_blocked"): return -5.0
        if ctx.flag("referral_6_complete"): return 3.0
        if ctx.text("referral_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def referral_rule_7(self,ctx:FollowupContext)->float:
        value=ctx.number("referral_score",0.0)
        if ctx.flag("referral_blocked"): return -5.0
        if ctx.flag("referral_7_complete"): return 4.0
        if ctx.text("referral_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def referral_rule_8(self,ctx:FollowupContext)->float:
        value=ctx.number("referral_score",0.0)
        if ctx.flag("referral_blocked"): return -5.0
        if ctx.flag("referral_8_complete"): return 1.0
        if ctx.text("referral_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def referral_rule_9(self,ctx:FollowupContext)->float:
        value=ctx.number("referral_score",0.0)
        if ctx.flag("referral_blocked"): return -5.0
        if ctx.flag("referral_9_complete"): return 2.0
        if ctx.text("referral_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def referral_rule_10(self,ctx:FollowupContext)->float:
        value=ctx.number("referral_score",0.0)
        if ctx.flag("referral_blocked"): return -5.0
        if ctx.flag("referral_10_complete"): return 3.0
        if ctx.text("referral_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def referral_rule_11(self,ctx:FollowupContext)->float:
        value=ctx.number("referral_score",0.0)
        if ctx.flag("referral_blocked"): return -5.0
        if ctx.flag("referral_11_complete"): return 4.0
        if ctx.text("referral_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def referral_rule_12(self,ctx:FollowupContext)->float:
        value=ctx.number("referral_score",0.0)
        if ctx.flag("referral_blocked"): return -5.0
        if ctx.flag("referral_12_complete"): return 1.0
        if ctx.text("referral_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def referral_rule_13(self,ctx:FollowupContext)->float:
        value=ctx.number("referral_score",0.0)
        if ctx.flag("referral_blocked"): return -5.0
        if ctx.flag("referral_13_complete"): return 2.0
        if ctx.text("referral_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def referral_rule_14(self,ctx:FollowupContext)->float:
        value=ctx.number("referral_score",0.0)
        if ctx.flag("referral_blocked"): return -5.0
        if ctx.flag("referral_14_complete"): return 3.0
        if ctx.text("referral_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def network_rule_1(self,ctx:FollowupContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_1_complete"): return 2.0
        if ctx.text("network_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def network_rule_2(self,ctx:FollowupContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_2_complete"): return 3.0
        if ctx.text("network_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def network_rule_3(self,ctx:FollowupContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_3_complete"): return 4.0
        if ctx.text("network_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def network_rule_4(self,ctx:FollowupContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_4_complete"): return 1.0
        if ctx.text("network_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def network_rule_5(self,ctx:FollowupContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_5_complete"): return 2.0
        if ctx.text("network_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def network_rule_6(self,ctx:FollowupContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_6_complete"): return 3.0
        if ctx.text("network_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def network_rule_7(self,ctx:FollowupContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_7_complete"): return 4.0
        if ctx.text("network_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def network_rule_8(self,ctx:FollowupContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_8_complete"): return 1.0
        if ctx.text("network_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def network_rule_9(self,ctx:FollowupContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_9_complete"): return 2.0
        if ctx.text("network_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def network_rule_10(self,ctx:FollowupContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_10_complete"): return 3.0
        if ctx.text("network_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def network_rule_11(self,ctx:FollowupContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_11_complete"): return 4.0
        if ctx.text("network_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def network_rule_12(self,ctx:FollowupContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_12_complete"): return 1.0
        if ctx.text("network_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def network_rule_13(self,ctx:FollowupContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_13_complete"): return 2.0
        if ctx.text("network_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def network_rule_14(self,ctx:FollowupContext)->float:
        value=ctx.number("network_score",0.0)
        if ctx.flag("network_blocked"): return -5.0
        if ctx.flag("network_14_complete"): return 3.0
        if ctx.text("network_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def final_rule_1(self,ctx:FollowupContext)->float:
        value=ctx.number("final_score",0.0)
        if ctx.flag("final_blocked"): return -5.0
        if ctx.flag("final_1_complete"): return 2.0
        if ctx.text("final_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def final_rule_2(self,ctx:FollowupContext)->float:
        value=ctx.number("final_score",0.0)
        if ctx.flag("final_blocked"): return -5.0
        if ctx.flag("final_2_complete"): return 3.0
        if ctx.text("final_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def final_rule_3(self,ctx:FollowupContext)->float:
        value=ctx.number("final_score",0.0)
        if ctx.flag("final_blocked"): return -5.0
        if ctx.flag("final_3_complete"): return 4.0
        if ctx.text("final_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def final_rule_4(self,ctx:FollowupContext)->float:
        value=ctx.number("final_score",0.0)
        if ctx.flag("final_blocked"): return -5.0
        if ctx.flag("final_4_complete"): return 1.0
        if ctx.text("final_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def final_rule_5(self,ctx:FollowupContext)->float:
        value=ctx.number("final_score",0.0)
        if ctx.flag("final_blocked"): return -5.0
        if ctx.flag("final_5_complete"): return 2.0
        if ctx.text("final_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def final_rule_6(self,ctx:FollowupContext)->float:
        value=ctx.number("final_score",0.0)
        if ctx.flag("final_blocked"): return -5.0
        if ctx.flag("final_6_complete"): return 3.0
        if ctx.text("final_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def final_rule_7(self,ctx:FollowupContext)->float:
        value=ctx.number("final_score",0.0)
        if ctx.flag("final_blocked"): return -5.0
        if ctx.flag("final_7_complete"): return 4.0
        if ctx.text("final_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def final_rule_8(self,ctx:FollowupContext)->float:
        value=ctx.number("final_score",0.0)
        if ctx.flag("final_blocked"): return -5.0
        if ctx.flag("final_8_complete"): return 1.0
        if ctx.text("final_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def final_rule_9(self,ctx:FollowupContext)->float:
        value=ctx.number("final_score",0.0)
        if ctx.flag("final_blocked"): return -5.0
        if ctx.flag("final_9_complete"): return 2.0
        if ctx.text("final_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def final_rule_10(self,ctx:FollowupContext)->float:
        value=ctx.number("final_score",0.0)
        if ctx.flag("final_blocked"): return -5.0
        if ctx.flag("final_10_complete"): return 3.0
        if ctx.text("final_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def final_rule_11(self,ctx:FollowupContext)->float:
        value=ctx.number("final_score",0.0)
        if ctx.flag("final_blocked"): return -5.0
        if ctx.flag("final_11_complete"): return 4.0
        if ctx.text("final_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def final_rule_12(self,ctx:FollowupContext)->float:
        value=ctx.number("final_score",0.0)
        if ctx.flag("final_blocked"): return -5.0
        if ctx.flag("final_12_complete"): return 1.0
        if ctx.text("final_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def final_rule_13(self,ctx:FollowupContext)->float:
        value=ctx.number("final_score",0.0)
        if ctx.flag("final_blocked"): return -5.0
        if ctx.flag("final_13_complete"): return 2.0
        if ctx.text("final_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def final_rule_14(self,ctx:FollowupContext)->float:
        value=ctx.number("final_score",0.0)
        if ctx.flag("final_blocked"): return -5.0
        if ctx.flag("final_14_complete"): return 3.0
        if ctx.text("final_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def evaluate_many(self,records:Sequence[Mapping[str,object]])->list[FollowupResult]:
        return [self.evaluate(record) for record in records]
    def summarize(self,results:Sequence[FollowupResult])->dict[str,object]:
        scores=[item.score for item in results]
        return {"count":len(scores),"average":round(sum(scores)/len(scores),2) if scores else 0.0,"strong":sum(x.status=="strong" for x in results),"acceptable":sum(x.status=="acceptable" for x in results),"review":sum(x.status=="review" for x in results)}
