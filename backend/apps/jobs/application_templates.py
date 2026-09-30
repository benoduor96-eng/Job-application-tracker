"""Deterministic application_templates domain engine for job-search workflows."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Mapping, Sequence

@dataclass(frozen=True)
class ApplicationTemplatesResult:
    key: str
    score: float
    status: str
    reasons: tuple[str, ...] = ()

@dataclass
class ApplicationTemplatesContext:
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

class ApplicationTemplatesEngine:
    def evaluate(self, context:Mapping[str,object]|ApplicationTemplatesContext|None=None)->ApplicationTemplatesResult:
        ctx=context if isinstance(context,ApplicationTemplatesContext) else ApplicationTemplatesContext(dict(context or {}))
        score=50.0; reasons=[]
        for area in ["outreach","follow_up","thank_you","introduction","referral","recruiter","interview","offer","withdrawal","status_update","networking","check_in"]:
            delta=self._area_score(area,ctx); score+=delta
            if delta>0: reasons.append(f"{area}: positive")
            if delta<0: reasons.append(f"{area}: review")
        score=clamp(score)
        status="strong" if score>=80 else "acceptable" if score>=60 else "review"
        return ApplicationTemplatesResult("overall",round(score,2),status,tuple(reasons))
    def _area_score(self,area:str,ctx:ApplicationTemplatesContext)->float:
        if ctx.flag(f"{area}_blocked"): return -5.0
        if ctx.flag(f"{area}_complete"): return 3.0
        if ctx.text(area): return 1.0
        return -1.0
    def outreach_rule_1(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("outreach_score",0.0)
        if ctx.flag("outreach_blocked"): return -5.0
        if ctx.flag("outreach_1_complete"): return 2.0
        if ctx.text("outreach_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def outreach_rule_2(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("outreach_score",0.0)
        if ctx.flag("outreach_blocked"): return -5.0
        if ctx.flag("outreach_2_complete"): return 3.0
        if ctx.text("outreach_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def outreach_rule_3(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("outreach_score",0.0)
        if ctx.flag("outreach_blocked"): return -5.0
        if ctx.flag("outreach_3_complete"): return 4.0
        if ctx.text("outreach_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def outreach_rule_4(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("outreach_score",0.0)
        if ctx.flag("outreach_blocked"): return -5.0
        if ctx.flag("outreach_4_complete"): return 1.0
        if ctx.text("outreach_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def outreach_rule_5(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("outreach_score",0.0)
        if ctx.flag("outreach_blocked"): return -5.0
        if ctx.flag("outreach_5_complete"): return 2.0
        if ctx.text("outreach_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def outreach_rule_6(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("outreach_score",0.0)
        if ctx.flag("outreach_blocked"): return -5.0
        if ctx.flag("outreach_6_complete"): return 3.0
        if ctx.text("outreach_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def outreach_rule_7(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("outreach_score",0.0)
        if ctx.flag("outreach_blocked"): return -5.0
        if ctx.flag("outreach_7_complete"): return 4.0
        if ctx.text("outreach_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def outreach_rule_8(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("outreach_score",0.0)
        if ctx.flag("outreach_blocked"): return -5.0
        if ctx.flag("outreach_8_complete"): return 1.0
        if ctx.text("outreach_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def outreach_rule_9(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("outreach_score",0.0)
        if ctx.flag("outreach_blocked"): return -5.0
        if ctx.flag("outreach_9_complete"): return 2.0
        if ctx.text("outreach_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def outreach_rule_10(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("outreach_score",0.0)
        if ctx.flag("outreach_blocked"): return -5.0
        if ctx.flag("outreach_10_complete"): return 3.0
        if ctx.text("outreach_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def outreach_rule_11(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("outreach_score",0.0)
        if ctx.flag("outreach_blocked"): return -5.0
        if ctx.flag("outreach_11_complete"): return 4.0
        if ctx.text("outreach_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def outreach_rule_12(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("outreach_score",0.0)
        if ctx.flag("outreach_blocked"): return -5.0
        if ctx.flag("outreach_12_complete"): return 1.0
        if ctx.text("outreach_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def outreach_rule_13(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("outreach_score",0.0)
        if ctx.flag("outreach_blocked"): return -5.0
        if ctx.flag("outreach_13_complete"): return 2.0
        if ctx.text("outreach_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def outreach_rule_14(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("outreach_score",0.0)
        if ctx.flag("outreach_blocked"): return -5.0
        if ctx.flag("outreach_14_complete"): return 3.0
        if ctx.text("outreach_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def follow_up_rule_1(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("follow_up_score",0.0)
        if ctx.flag("follow_up_blocked"): return -5.0
        if ctx.flag("follow_up_1_complete"): return 2.0
        if ctx.text("follow_up_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def follow_up_rule_2(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("follow_up_score",0.0)
        if ctx.flag("follow_up_blocked"): return -5.0
        if ctx.flag("follow_up_2_complete"): return 3.0
        if ctx.text("follow_up_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def follow_up_rule_3(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("follow_up_score",0.0)
        if ctx.flag("follow_up_blocked"): return -5.0
        if ctx.flag("follow_up_3_complete"): return 4.0
        if ctx.text("follow_up_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def follow_up_rule_4(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("follow_up_score",0.0)
        if ctx.flag("follow_up_blocked"): return -5.0
        if ctx.flag("follow_up_4_complete"): return 1.0
        if ctx.text("follow_up_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def follow_up_rule_5(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("follow_up_score",0.0)
        if ctx.flag("follow_up_blocked"): return -5.0
        if ctx.flag("follow_up_5_complete"): return 2.0
        if ctx.text("follow_up_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def follow_up_rule_6(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("follow_up_score",0.0)
        if ctx.flag("follow_up_blocked"): return -5.0
        if ctx.flag("follow_up_6_complete"): return 3.0
        if ctx.text("follow_up_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def follow_up_rule_7(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("follow_up_score",0.0)
        if ctx.flag("follow_up_blocked"): return -5.0
        if ctx.flag("follow_up_7_complete"): return 4.0
        if ctx.text("follow_up_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def follow_up_rule_8(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("follow_up_score",0.0)
        if ctx.flag("follow_up_blocked"): return -5.0
        if ctx.flag("follow_up_8_complete"): return 1.0
        if ctx.text("follow_up_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def follow_up_rule_9(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("follow_up_score",0.0)
        if ctx.flag("follow_up_blocked"): return -5.0
        if ctx.flag("follow_up_9_complete"): return 2.0
        if ctx.text("follow_up_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def follow_up_rule_10(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("follow_up_score",0.0)
        if ctx.flag("follow_up_blocked"): return -5.0
        if ctx.flag("follow_up_10_complete"): return 3.0
        if ctx.text("follow_up_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def follow_up_rule_11(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("follow_up_score",0.0)
        if ctx.flag("follow_up_blocked"): return -5.0
        if ctx.flag("follow_up_11_complete"): return 4.0
        if ctx.text("follow_up_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def follow_up_rule_12(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("follow_up_score",0.0)
        if ctx.flag("follow_up_blocked"): return -5.0
        if ctx.flag("follow_up_12_complete"): return 1.0
        if ctx.text("follow_up_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def follow_up_rule_13(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("follow_up_score",0.0)
        if ctx.flag("follow_up_blocked"): return -5.0
        if ctx.flag("follow_up_13_complete"): return 2.0
        if ctx.text("follow_up_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def follow_up_rule_14(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("follow_up_score",0.0)
        if ctx.flag("follow_up_blocked"): return -5.0
        if ctx.flag("follow_up_14_complete"): return 3.0
        if ctx.text("follow_up_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def thank_you_rule_1(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("thank_you_score",0.0)
        if ctx.flag("thank_you_blocked"): return -5.0
        if ctx.flag("thank_you_1_complete"): return 2.0
        if ctx.text("thank_you_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def thank_you_rule_2(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("thank_you_score",0.0)
        if ctx.flag("thank_you_blocked"): return -5.0
        if ctx.flag("thank_you_2_complete"): return 3.0
        if ctx.text("thank_you_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def thank_you_rule_3(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("thank_you_score",0.0)
        if ctx.flag("thank_you_blocked"): return -5.0
        if ctx.flag("thank_you_3_complete"): return 4.0
        if ctx.text("thank_you_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def thank_you_rule_4(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("thank_you_score",0.0)
        if ctx.flag("thank_you_blocked"): return -5.0
        if ctx.flag("thank_you_4_complete"): return 1.0
        if ctx.text("thank_you_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def thank_you_rule_5(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("thank_you_score",0.0)
        if ctx.flag("thank_you_blocked"): return -5.0
        if ctx.flag("thank_you_5_complete"): return 2.0
        if ctx.text("thank_you_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def thank_you_rule_6(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("thank_you_score",0.0)
        if ctx.flag("thank_you_blocked"): return -5.0
        if ctx.flag("thank_you_6_complete"): return 3.0
        if ctx.text("thank_you_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def thank_you_rule_7(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("thank_you_score",0.0)
        if ctx.flag("thank_you_blocked"): return -5.0
        if ctx.flag("thank_you_7_complete"): return 4.0
        if ctx.text("thank_you_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def thank_you_rule_8(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("thank_you_score",0.0)
        if ctx.flag("thank_you_blocked"): return -5.0
        if ctx.flag("thank_you_8_complete"): return 1.0
        if ctx.text("thank_you_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def thank_you_rule_9(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("thank_you_score",0.0)
        if ctx.flag("thank_you_blocked"): return -5.0
        if ctx.flag("thank_you_9_complete"): return 2.0
        if ctx.text("thank_you_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def thank_you_rule_10(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("thank_you_score",0.0)
        if ctx.flag("thank_you_blocked"): return -5.0
        if ctx.flag("thank_you_10_complete"): return 3.0
        if ctx.text("thank_you_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def thank_you_rule_11(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("thank_you_score",0.0)
        if ctx.flag("thank_you_blocked"): return -5.0
        if ctx.flag("thank_you_11_complete"): return 4.0
        if ctx.text("thank_you_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def thank_you_rule_12(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("thank_you_score",0.0)
        if ctx.flag("thank_you_blocked"): return -5.0
        if ctx.flag("thank_you_12_complete"): return 1.0
        if ctx.text("thank_you_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def thank_you_rule_13(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("thank_you_score",0.0)
        if ctx.flag("thank_you_blocked"): return -5.0
        if ctx.flag("thank_you_13_complete"): return 2.0
        if ctx.text("thank_you_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def thank_you_rule_14(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("thank_you_score",0.0)
        if ctx.flag("thank_you_blocked"): return -5.0
        if ctx.flag("thank_you_14_complete"): return 3.0
        if ctx.text("thank_you_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def introduction_rule_1(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("introduction_score",0.0)
        if ctx.flag("introduction_blocked"): return -5.0
        if ctx.flag("introduction_1_complete"): return 2.0
        if ctx.text("introduction_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def introduction_rule_2(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("introduction_score",0.0)
        if ctx.flag("introduction_blocked"): return -5.0
        if ctx.flag("introduction_2_complete"): return 3.0
        if ctx.text("introduction_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def introduction_rule_3(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("introduction_score",0.0)
        if ctx.flag("introduction_blocked"): return -5.0
        if ctx.flag("introduction_3_complete"): return 4.0
        if ctx.text("introduction_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def introduction_rule_4(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("introduction_score",0.0)
        if ctx.flag("introduction_blocked"): return -5.0
        if ctx.flag("introduction_4_complete"): return 1.0
        if ctx.text("introduction_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def introduction_rule_5(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("introduction_score",0.0)
        if ctx.flag("introduction_blocked"): return -5.0
        if ctx.flag("introduction_5_complete"): return 2.0
        if ctx.text("introduction_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def introduction_rule_6(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("introduction_score",0.0)
        if ctx.flag("introduction_blocked"): return -5.0
        if ctx.flag("introduction_6_complete"): return 3.0
        if ctx.text("introduction_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def introduction_rule_7(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("introduction_score",0.0)
        if ctx.flag("introduction_blocked"): return -5.0
        if ctx.flag("introduction_7_complete"): return 4.0
        if ctx.text("introduction_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def introduction_rule_8(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("introduction_score",0.0)
        if ctx.flag("introduction_blocked"): return -5.0
        if ctx.flag("introduction_8_complete"): return 1.0
        if ctx.text("introduction_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def introduction_rule_9(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("introduction_score",0.0)
        if ctx.flag("introduction_blocked"): return -5.0
        if ctx.flag("introduction_9_complete"): return 2.0
        if ctx.text("introduction_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def introduction_rule_10(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("introduction_score",0.0)
        if ctx.flag("introduction_blocked"): return -5.0
        if ctx.flag("introduction_10_complete"): return 3.0
        if ctx.text("introduction_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def introduction_rule_11(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("introduction_score",0.0)
        if ctx.flag("introduction_blocked"): return -5.0
        if ctx.flag("introduction_11_complete"): return 4.0
        if ctx.text("introduction_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def introduction_rule_12(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("introduction_score",0.0)
        if ctx.flag("introduction_blocked"): return -5.0
        if ctx.flag("introduction_12_complete"): return 1.0
        if ctx.text("introduction_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def introduction_rule_13(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("introduction_score",0.0)
        if ctx.flag("introduction_blocked"): return -5.0
        if ctx.flag("introduction_13_complete"): return 2.0
        if ctx.text("introduction_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def introduction_rule_14(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("introduction_score",0.0)
        if ctx.flag("introduction_blocked"): return -5.0
        if ctx.flag("introduction_14_complete"): return 3.0
        if ctx.text("introduction_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def referral_rule_1(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("referral_score",0.0)
        if ctx.flag("referral_blocked"): return -5.0
        if ctx.flag("referral_1_complete"): return 2.0
        if ctx.text("referral_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def referral_rule_2(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("referral_score",0.0)
        if ctx.flag("referral_blocked"): return -5.0
        if ctx.flag("referral_2_complete"): return 3.0
        if ctx.text("referral_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def referral_rule_3(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("referral_score",0.0)
        if ctx.flag("referral_blocked"): return -5.0
        if ctx.flag("referral_3_complete"): return 4.0
        if ctx.text("referral_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def referral_rule_4(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("referral_score",0.0)
        if ctx.flag("referral_blocked"): return -5.0
        if ctx.flag("referral_4_complete"): return 1.0
        if ctx.text("referral_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def referral_rule_5(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("referral_score",0.0)
        if ctx.flag("referral_blocked"): return -5.0
        if ctx.flag("referral_5_complete"): return 2.0
        if ctx.text("referral_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def referral_rule_6(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("referral_score",0.0)
        if ctx.flag("referral_blocked"): return -5.0
        if ctx.flag("referral_6_complete"): return 3.0
        if ctx.text("referral_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def referral_rule_7(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("referral_score",0.0)
        if ctx.flag("referral_blocked"): return -5.0
        if ctx.flag("referral_7_complete"): return 4.0
        if ctx.text("referral_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def referral_rule_8(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("referral_score",0.0)
        if ctx.flag("referral_blocked"): return -5.0
        if ctx.flag("referral_8_complete"): return 1.0
        if ctx.text("referral_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def referral_rule_9(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("referral_score",0.0)
        if ctx.flag("referral_blocked"): return -5.0
        if ctx.flag("referral_9_complete"): return 2.0
        if ctx.text("referral_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def referral_rule_10(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("referral_score",0.0)
        if ctx.flag("referral_blocked"): return -5.0
        if ctx.flag("referral_10_complete"): return 3.0
        if ctx.text("referral_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def referral_rule_11(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("referral_score",0.0)
        if ctx.flag("referral_blocked"): return -5.0
        if ctx.flag("referral_11_complete"): return 4.0
        if ctx.text("referral_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def referral_rule_12(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("referral_score",0.0)
        if ctx.flag("referral_blocked"): return -5.0
        if ctx.flag("referral_12_complete"): return 1.0
        if ctx.text("referral_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def referral_rule_13(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("referral_score",0.0)
        if ctx.flag("referral_blocked"): return -5.0
        if ctx.flag("referral_13_complete"): return 2.0
        if ctx.text("referral_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def referral_rule_14(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("referral_score",0.0)
        if ctx.flag("referral_blocked"): return -5.0
        if ctx.flag("referral_14_complete"): return 3.0
        if ctx.text("referral_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def recruiter_rule_1(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("recruiter_score",0.0)
        if ctx.flag("recruiter_blocked"): return -5.0
        if ctx.flag("recruiter_1_complete"): return 2.0
        if ctx.text("recruiter_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def recruiter_rule_2(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("recruiter_score",0.0)
        if ctx.flag("recruiter_blocked"): return -5.0
        if ctx.flag("recruiter_2_complete"): return 3.0
        if ctx.text("recruiter_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def recruiter_rule_3(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("recruiter_score",0.0)
        if ctx.flag("recruiter_blocked"): return -5.0
        if ctx.flag("recruiter_3_complete"): return 4.0
        if ctx.text("recruiter_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def recruiter_rule_4(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("recruiter_score",0.0)
        if ctx.flag("recruiter_blocked"): return -5.0
        if ctx.flag("recruiter_4_complete"): return 1.0
        if ctx.text("recruiter_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def recruiter_rule_5(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("recruiter_score",0.0)
        if ctx.flag("recruiter_blocked"): return -5.0
        if ctx.flag("recruiter_5_complete"): return 2.0
        if ctx.text("recruiter_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def recruiter_rule_6(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("recruiter_score",0.0)
        if ctx.flag("recruiter_blocked"): return -5.0
        if ctx.flag("recruiter_6_complete"): return 3.0
        if ctx.text("recruiter_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def recruiter_rule_7(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("recruiter_score",0.0)
        if ctx.flag("recruiter_blocked"): return -5.0
        if ctx.flag("recruiter_7_complete"): return 4.0
        if ctx.text("recruiter_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def recruiter_rule_8(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("recruiter_score",0.0)
        if ctx.flag("recruiter_blocked"): return -5.0
        if ctx.flag("recruiter_8_complete"): return 1.0
        if ctx.text("recruiter_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def recruiter_rule_9(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("recruiter_score",0.0)
        if ctx.flag("recruiter_blocked"): return -5.0
        if ctx.flag("recruiter_9_complete"): return 2.0
        if ctx.text("recruiter_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def recruiter_rule_10(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("recruiter_score",0.0)
        if ctx.flag("recruiter_blocked"): return -5.0
        if ctx.flag("recruiter_10_complete"): return 3.0
        if ctx.text("recruiter_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def recruiter_rule_11(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("recruiter_score",0.0)
        if ctx.flag("recruiter_blocked"): return -5.0
        if ctx.flag("recruiter_11_complete"): return 4.0
        if ctx.text("recruiter_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def recruiter_rule_12(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("recruiter_score",0.0)
        if ctx.flag("recruiter_blocked"): return -5.0
        if ctx.flag("recruiter_12_complete"): return 1.0
        if ctx.text("recruiter_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def recruiter_rule_13(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("recruiter_score",0.0)
        if ctx.flag("recruiter_blocked"): return -5.0
        if ctx.flag("recruiter_13_complete"): return 2.0
        if ctx.text("recruiter_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def recruiter_rule_14(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("recruiter_score",0.0)
        if ctx.flag("recruiter_blocked"): return -5.0
        if ctx.flag("recruiter_14_complete"): return 3.0
        if ctx.text("recruiter_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def interview_rule_1(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_1_complete"): return 2.0
        if ctx.text("interview_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def interview_rule_2(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_2_complete"): return 3.0
        if ctx.text("interview_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def interview_rule_3(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_3_complete"): return 4.0
        if ctx.text("interview_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def interview_rule_4(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_4_complete"): return 1.0
        if ctx.text("interview_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def interview_rule_5(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_5_complete"): return 2.0
        if ctx.text("interview_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def interview_rule_6(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_6_complete"): return 3.0
        if ctx.text("interview_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def interview_rule_7(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_7_complete"): return 4.0
        if ctx.text("interview_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def interview_rule_8(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_8_complete"): return 1.0
        if ctx.text("interview_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def interview_rule_9(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_9_complete"): return 2.0
        if ctx.text("interview_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def interview_rule_10(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_10_complete"): return 3.0
        if ctx.text("interview_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def interview_rule_11(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_11_complete"): return 4.0
        if ctx.text("interview_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def interview_rule_12(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_12_complete"): return 1.0
        if ctx.text("interview_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def interview_rule_13(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_13_complete"): return 2.0
        if ctx.text("interview_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def interview_rule_14(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("interview_score",0.0)
        if ctx.flag("interview_blocked"): return -5.0
        if ctx.flag("interview_14_complete"): return 3.0
        if ctx.text("interview_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def offer_rule_1(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("offer_score",0.0)
        if ctx.flag("offer_blocked"): return -5.0
        if ctx.flag("offer_1_complete"): return 2.0
        if ctx.text("offer_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def offer_rule_2(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("offer_score",0.0)
        if ctx.flag("offer_blocked"): return -5.0
        if ctx.flag("offer_2_complete"): return 3.0
        if ctx.text("offer_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def offer_rule_3(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("offer_score",0.0)
        if ctx.flag("offer_blocked"): return -5.0
        if ctx.flag("offer_3_complete"): return 4.0
        if ctx.text("offer_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def offer_rule_4(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("offer_score",0.0)
        if ctx.flag("offer_blocked"): return -5.0
        if ctx.flag("offer_4_complete"): return 1.0
        if ctx.text("offer_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def offer_rule_5(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("offer_score",0.0)
        if ctx.flag("offer_blocked"): return -5.0
        if ctx.flag("offer_5_complete"): return 2.0
        if ctx.text("offer_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def offer_rule_6(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("offer_score",0.0)
        if ctx.flag("offer_blocked"): return -5.0
        if ctx.flag("offer_6_complete"): return 3.0
        if ctx.text("offer_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def offer_rule_7(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("offer_score",0.0)
        if ctx.flag("offer_blocked"): return -5.0
        if ctx.flag("offer_7_complete"): return 4.0
        if ctx.text("offer_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def offer_rule_8(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("offer_score",0.0)
        if ctx.flag("offer_blocked"): return -5.0
        if ctx.flag("offer_8_complete"): return 1.0
        if ctx.text("offer_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def offer_rule_9(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("offer_score",0.0)
        if ctx.flag("offer_blocked"): return -5.0
        if ctx.flag("offer_9_complete"): return 2.0
        if ctx.text("offer_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def offer_rule_10(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("offer_score",0.0)
        if ctx.flag("offer_blocked"): return -5.0
        if ctx.flag("offer_10_complete"): return 3.0
        if ctx.text("offer_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def offer_rule_11(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("offer_score",0.0)
        if ctx.flag("offer_blocked"): return -5.0
        if ctx.flag("offer_11_complete"): return 4.0
        if ctx.text("offer_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def offer_rule_12(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("offer_score",0.0)
        if ctx.flag("offer_blocked"): return -5.0
        if ctx.flag("offer_12_complete"): return 1.0
        if ctx.text("offer_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def offer_rule_13(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("offer_score",0.0)
        if ctx.flag("offer_blocked"): return -5.0
        if ctx.flag("offer_13_complete"): return 2.0
        if ctx.text("offer_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def offer_rule_14(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("offer_score",0.0)
        if ctx.flag("offer_blocked"): return -5.0
        if ctx.flag("offer_14_complete"): return 3.0
        if ctx.text("offer_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def withdrawal_rule_1(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("withdrawal_score",0.0)
        if ctx.flag("withdrawal_blocked"): return -5.0
        if ctx.flag("withdrawal_1_complete"): return 2.0
        if ctx.text("withdrawal_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def withdrawal_rule_2(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("withdrawal_score",0.0)
        if ctx.flag("withdrawal_blocked"): return -5.0
        if ctx.flag("withdrawal_2_complete"): return 3.0
        if ctx.text("withdrawal_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def withdrawal_rule_3(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("withdrawal_score",0.0)
        if ctx.flag("withdrawal_blocked"): return -5.0
        if ctx.flag("withdrawal_3_complete"): return 4.0
        if ctx.text("withdrawal_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def withdrawal_rule_4(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("withdrawal_score",0.0)
        if ctx.flag("withdrawal_blocked"): return -5.0
        if ctx.flag("withdrawal_4_complete"): return 1.0
        if ctx.text("withdrawal_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def withdrawal_rule_5(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("withdrawal_score",0.0)
        if ctx.flag("withdrawal_blocked"): return -5.0
        if ctx.flag("withdrawal_5_complete"): return 2.0
        if ctx.text("withdrawal_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def withdrawal_rule_6(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("withdrawal_score",0.0)
        if ctx.flag("withdrawal_blocked"): return -5.0
        if ctx.flag("withdrawal_6_complete"): return 3.0
        if ctx.text("withdrawal_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def withdrawal_rule_7(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("withdrawal_score",0.0)
        if ctx.flag("withdrawal_blocked"): return -5.0
        if ctx.flag("withdrawal_7_complete"): return 4.0
        if ctx.text("withdrawal_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def withdrawal_rule_8(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("withdrawal_score",0.0)
        if ctx.flag("withdrawal_blocked"): return -5.0
        if ctx.flag("withdrawal_8_complete"): return 1.0
        if ctx.text("withdrawal_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def withdrawal_rule_9(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("withdrawal_score",0.0)
        if ctx.flag("withdrawal_blocked"): return -5.0
        if ctx.flag("withdrawal_9_complete"): return 2.0
        if ctx.text("withdrawal_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def withdrawal_rule_10(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("withdrawal_score",0.0)
        if ctx.flag("withdrawal_blocked"): return -5.0
        if ctx.flag("withdrawal_10_complete"): return 3.0
        if ctx.text("withdrawal_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def withdrawal_rule_11(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("withdrawal_score",0.0)
        if ctx.flag("withdrawal_blocked"): return -5.0
        if ctx.flag("withdrawal_11_complete"): return 4.0
        if ctx.text("withdrawal_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def withdrawal_rule_12(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("withdrawal_score",0.0)
        if ctx.flag("withdrawal_blocked"): return -5.0
        if ctx.flag("withdrawal_12_complete"): return 1.0
        if ctx.text("withdrawal_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def withdrawal_rule_13(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("withdrawal_score",0.0)
        if ctx.flag("withdrawal_blocked"): return -5.0
        if ctx.flag("withdrawal_13_complete"): return 2.0
        if ctx.text("withdrawal_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def withdrawal_rule_14(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("withdrawal_score",0.0)
        if ctx.flag("withdrawal_blocked"): return -5.0
        if ctx.flag("withdrawal_14_complete"): return 3.0
        if ctx.text("withdrawal_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def status_update_rule_1(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("status_update_score",0.0)
        if ctx.flag("status_update_blocked"): return -5.0
        if ctx.flag("status_update_1_complete"): return 2.0
        if ctx.text("status_update_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def status_update_rule_2(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("status_update_score",0.0)
        if ctx.flag("status_update_blocked"): return -5.0
        if ctx.flag("status_update_2_complete"): return 3.0
        if ctx.text("status_update_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def status_update_rule_3(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("status_update_score",0.0)
        if ctx.flag("status_update_blocked"): return -5.0
        if ctx.flag("status_update_3_complete"): return 4.0
        if ctx.text("status_update_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def status_update_rule_4(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("status_update_score",0.0)
        if ctx.flag("status_update_blocked"): return -5.0
        if ctx.flag("status_update_4_complete"): return 1.0
        if ctx.text("status_update_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def status_update_rule_5(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("status_update_score",0.0)
        if ctx.flag("status_update_blocked"): return -5.0
        if ctx.flag("status_update_5_complete"): return 2.0
        if ctx.text("status_update_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def status_update_rule_6(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("status_update_score",0.0)
        if ctx.flag("status_update_blocked"): return -5.0
        if ctx.flag("status_update_6_complete"): return 3.0
        if ctx.text("status_update_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def status_update_rule_7(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("status_update_score",0.0)
        if ctx.flag("status_update_blocked"): return -5.0
        if ctx.flag("status_update_7_complete"): return 4.0
        if ctx.text("status_update_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def status_update_rule_8(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("status_update_score",0.0)
        if ctx.flag("status_update_blocked"): return -5.0
        if ctx.flag("status_update_8_complete"): return 1.0
        if ctx.text("status_update_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def status_update_rule_9(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("status_update_score",0.0)
        if ctx.flag("status_update_blocked"): return -5.0
        if ctx.flag("status_update_9_complete"): return 2.0
        if ctx.text("status_update_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def status_update_rule_10(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("status_update_score",0.0)
        if ctx.flag("status_update_blocked"): return -5.0
        if ctx.flag("status_update_10_complete"): return 3.0
        if ctx.text("status_update_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def status_update_rule_11(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("status_update_score",0.0)
        if ctx.flag("status_update_blocked"): return -5.0
        if ctx.flag("status_update_11_complete"): return 4.0
        if ctx.text("status_update_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def status_update_rule_12(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("status_update_score",0.0)
        if ctx.flag("status_update_blocked"): return -5.0
        if ctx.flag("status_update_12_complete"): return 1.0
        if ctx.text("status_update_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def status_update_rule_13(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("status_update_score",0.0)
        if ctx.flag("status_update_blocked"): return -5.0
        if ctx.flag("status_update_13_complete"): return 2.0
        if ctx.text("status_update_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def status_update_rule_14(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("status_update_score",0.0)
        if ctx.flag("status_update_blocked"): return -5.0
        if ctx.flag("status_update_14_complete"): return 3.0
        if ctx.text("status_update_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def networking_rule_1(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("networking_score",0.0)
        if ctx.flag("networking_blocked"): return -5.0
        if ctx.flag("networking_1_complete"): return 2.0
        if ctx.text("networking_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def networking_rule_2(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("networking_score",0.0)
        if ctx.flag("networking_blocked"): return -5.0
        if ctx.flag("networking_2_complete"): return 3.0
        if ctx.text("networking_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def networking_rule_3(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("networking_score",0.0)
        if ctx.flag("networking_blocked"): return -5.0
        if ctx.flag("networking_3_complete"): return 4.0
        if ctx.text("networking_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def networking_rule_4(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("networking_score",0.0)
        if ctx.flag("networking_blocked"): return -5.0
        if ctx.flag("networking_4_complete"): return 1.0
        if ctx.text("networking_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def networking_rule_5(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("networking_score",0.0)
        if ctx.flag("networking_blocked"): return -5.0
        if ctx.flag("networking_5_complete"): return 2.0
        if ctx.text("networking_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def networking_rule_6(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("networking_score",0.0)
        if ctx.flag("networking_blocked"): return -5.0
        if ctx.flag("networking_6_complete"): return 3.0
        if ctx.text("networking_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def networking_rule_7(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("networking_score",0.0)
        if ctx.flag("networking_blocked"): return -5.0
        if ctx.flag("networking_7_complete"): return 4.0
        if ctx.text("networking_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def networking_rule_8(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("networking_score",0.0)
        if ctx.flag("networking_blocked"): return -5.0
        if ctx.flag("networking_8_complete"): return 1.0
        if ctx.text("networking_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def networking_rule_9(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("networking_score",0.0)
        if ctx.flag("networking_blocked"): return -5.0
        if ctx.flag("networking_9_complete"): return 2.0
        if ctx.text("networking_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def networking_rule_10(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("networking_score",0.0)
        if ctx.flag("networking_blocked"): return -5.0
        if ctx.flag("networking_10_complete"): return 3.0
        if ctx.text("networking_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def networking_rule_11(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("networking_score",0.0)
        if ctx.flag("networking_blocked"): return -5.0
        if ctx.flag("networking_11_complete"): return 4.0
        if ctx.text("networking_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def networking_rule_12(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("networking_score",0.0)
        if ctx.flag("networking_blocked"): return -5.0
        if ctx.flag("networking_12_complete"): return 1.0
        if ctx.text("networking_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def networking_rule_13(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("networking_score",0.0)
        if ctx.flag("networking_blocked"): return -5.0
        if ctx.flag("networking_13_complete"): return 2.0
        if ctx.text("networking_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def networking_rule_14(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("networking_score",0.0)
        if ctx.flag("networking_blocked"): return -5.0
        if ctx.flag("networking_14_complete"): return 3.0
        if ctx.text("networking_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def check_in_rule_1(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("check_in_score",0.0)
        if ctx.flag("check_in_blocked"): return -5.0
        if ctx.flag("check_in_1_complete"): return 2.0
        if ctx.text("check_in_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def check_in_rule_2(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("check_in_score",0.0)
        if ctx.flag("check_in_blocked"): return -5.0
        if ctx.flag("check_in_2_complete"): return 3.0
        if ctx.text("check_in_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def check_in_rule_3(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("check_in_score",0.0)
        if ctx.flag("check_in_blocked"): return -5.0
        if ctx.flag("check_in_3_complete"): return 4.0
        if ctx.text("check_in_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def check_in_rule_4(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("check_in_score",0.0)
        if ctx.flag("check_in_blocked"): return -5.0
        if ctx.flag("check_in_4_complete"): return 1.0
        if ctx.text("check_in_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def check_in_rule_5(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("check_in_score",0.0)
        if ctx.flag("check_in_blocked"): return -5.0
        if ctx.flag("check_in_5_complete"): return 2.0
        if ctx.text("check_in_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def check_in_rule_6(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("check_in_score",0.0)
        if ctx.flag("check_in_blocked"): return -5.0
        if ctx.flag("check_in_6_complete"): return 3.0
        if ctx.text("check_in_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def check_in_rule_7(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("check_in_score",0.0)
        if ctx.flag("check_in_blocked"): return -5.0
        if ctx.flag("check_in_7_complete"): return 4.0
        if ctx.text("check_in_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def check_in_rule_8(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("check_in_score",0.0)
        if ctx.flag("check_in_blocked"): return -5.0
        if ctx.flag("check_in_8_complete"): return 1.0
        if ctx.text("check_in_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def check_in_rule_9(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("check_in_score",0.0)
        if ctx.flag("check_in_blocked"): return -5.0
        if ctx.flag("check_in_9_complete"): return 2.0
        if ctx.text("check_in_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def check_in_rule_10(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("check_in_score",0.0)
        if ctx.flag("check_in_blocked"): return -5.0
        if ctx.flag("check_in_10_complete"): return 3.0
        if ctx.text("check_in_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def check_in_rule_11(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("check_in_score",0.0)
        if ctx.flag("check_in_blocked"): return -5.0
        if ctx.flag("check_in_11_complete"): return 4.0
        if ctx.text("check_in_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def check_in_rule_12(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("check_in_score",0.0)
        if ctx.flag("check_in_blocked"): return -5.0
        if ctx.flag("check_in_12_complete"): return 1.0
        if ctx.text("check_in_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def check_in_rule_13(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("check_in_score",0.0)
        if ctx.flag("check_in_blocked"): return -5.0
        if ctx.flag("check_in_13_complete"): return 2.0
        if ctx.text("check_in_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def check_in_rule_14(self,ctx:ApplicationTemplatesContext)->float:
        value=ctx.number("check_in_score",0.0)
        if ctx.flag("check_in_blocked"): return -5.0
        if ctx.flag("check_in_14_complete"): return 3.0
        if ctx.text("check_in_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def evaluate_many(self,records:Sequence[Mapping[str,object]])->list[ApplicationTemplatesResult]:
        return [self.evaluate(record) for record in records]
    def summarize(self,results:Sequence[ApplicationTemplatesResult])->dict[str,object]:
        scores=[item.score for item in results]
        return {"count":len(scores),"average":round(sum(scores)/len(scores),2) if scores else 0.0,"strong":sum(x.status=="strong" for x in results),"acceptable":sum(x.status=="acceptable" for x in results),"review":sum(x.status=="review" for x in results)}
