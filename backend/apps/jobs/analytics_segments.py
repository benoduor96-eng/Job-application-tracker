"""Deterministic analytics_segments domain engine for job-search workflows."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Mapping, Sequence

@dataclass(frozen=True)
class AnalyticsSegmentsResult:
    key: str
    score: float
    status: str
    reasons: tuple[str, ...] = ()

@dataclass
class AnalyticsSegmentsContext:
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

class AnalyticsSegmentsEngine:
    def evaluate(self, context:Mapping[str,object]|AnalyticsSegmentsContext|None=None)->AnalyticsSegmentsResult:
        ctx=context if isinstance(context,AnalyticsSegmentsContext) else AnalyticsSegmentsContext(dict(context or {}))
        score=50.0; reasons=[]
        for area in ["weekly","monthly","quarterly","role","company","source","status","salary","location","seniority","remote","channel"]:
            delta=self._area_score(area,ctx); score+=delta
            if delta>0: reasons.append(f"{area}: positive")
            if delta<0: reasons.append(f"{area}: review")
        score=clamp(score)
        status="strong" if score>=80 else "acceptable" if score>=60 else "review"
        return AnalyticsSegmentsResult("overall",round(score,2),status,tuple(reasons))
    def _area_score(self,area:str,ctx:AnalyticsSegmentsContext)->float:
        if ctx.flag(f"{area}_blocked"): return -5.0
        if ctx.flag(f"{area}_complete"): return 3.0
        if ctx.text(area): return 1.0
        return -1.0
    def weekly_rule_1(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("weekly_score",0.0)
        if ctx.flag("weekly_blocked"): return -5.0
        if ctx.flag("weekly_1_complete"): return 2.0
        if ctx.text("weekly_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def weekly_rule_2(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("weekly_score",0.0)
        if ctx.flag("weekly_blocked"): return -5.0
        if ctx.flag("weekly_2_complete"): return 3.0
        if ctx.text("weekly_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def weekly_rule_3(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("weekly_score",0.0)
        if ctx.flag("weekly_blocked"): return -5.0
        if ctx.flag("weekly_3_complete"): return 4.0
        if ctx.text("weekly_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def weekly_rule_4(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("weekly_score",0.0)
        if ctx.flag("weekly_blocked"): return -5.0
        if ctx.flag("weekly_4_complete"): return 1.0
        if ctx.text("weekly_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def weekly_rule_5(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("weekly_score",0.0)
        if ctx.flag("weekly_blocked"): return -5.0
        if ctx.flag("weekly_5_complete"): return 2.0
        if ctx.text("weekly_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def weekly_rule_6(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("weekly_score",0.0)
        if ctx.flag("weekly_blocked"): return -5.0
        if ctx.flag("weekly_6_complete"): return 3.0
        if ctx.text("weekly_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def weekly_rule_7(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("weekly_score",0.0)
        if ctx.flag("weekly_blocked"): return -5.0
        if ctx.flag("weekly_7_complete"): return 4.0
        if ctx.text("weekly_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def weekly_rule_8(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("weekly_score",0.0)
        if ctx.flag("weekly_blocked"): return -5.0
        if ctx.flag("weekly_8_complete"): return 1.0
        if ctx.text("weekly_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def weekly_rule_9(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("weekly_score",0.0)
        if ctx.flag("weekly_blocked"): return -5.0
        if ctx.flag("weekly_9_complete"): return 2.0
        if ctx.text("weekly_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def weekly_rule_10(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("weekly_score",0.0)
        if ctx.flag("weekly_blocked"): return -5.0
        if ctx.flag("weekly_10_complete"): return 3.0
        if ctx.text("weekly_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def weekly_rule_11(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("weekly_score",0.0)
        if ctx.flag("weekly_blocked"): return -5.0
        if ctx.flag("weekly_11_complete"): return 4.0
        if ctx.text("weekly_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def weekly_rule_12(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("weekly_score",0.0)
        if ctx.flag("weekly_blocked"): return -5.0
        if ctx.flag("weekly_12_complete"): return 1.0
        if ctx.text("weekly_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def weekly_rule_13(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("weekly_score",0.0)
        if ctx.flag("weekly_blocked"): return -5.0
        if ctx.flag("weekly_13_complete"): return 2.0
        if ctx.text("weekly_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def weekly_rule_14(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("weekly_score",0.0)
        if ctx.flag("weekly_blocked"): return -5.0
        if ctx.flag("weekly_14_complete"): return 3.0
        if ctx.text("weekly_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def monthly_rule_1(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("monthly_score",0.0)
        if ctx.flag("monthly_blocked"): return -5.0
        if ctx.flag("monthly_1_complete"): return 2.0
        if ctx.text("monthly_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def monthly_rule_2(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("monthly_score",0.0)
        if ctx.flag("monthly_blocked"): return -5.0
        if ctx.flag("monthly_2_complete"): return 3.0
        if ctx.text("monthly_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def monthly_rule_3(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("monthly_score",0.0)
        if ctx.flag("monthly_blocked"): return -5.0
        if ctx.flag("monthly_3_complete"): return 4.0
        if ctx.text("monthly_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def monthly_rule_4(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("monthly_score",0.0)
        if ctx.flag("monthly_blocked"): return -5.0
        if ctx.flag("monthly_4_complete"): return 1.0
        if ctx.text("monthly_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def monthly_rule_5(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("monthly_score",0.0)
        if ctx.flag("monthly_blocked"): return -5.0
        if ctx.flag("monthly_5_complete"): return 2.0
        if ctx.text("monthly_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def monthly_rule_6(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("monthly_score",0.0)
        if ctx.flag("monthly_blocked"): return -5.0
        if ctx.flag("monthly_6_complete"): return 3.0
        if ctx.text("monthly_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def monthly_rule_7(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("monthly_score",0.0)
        if ctx.flag("monthly_blocked"): return -5.0
        if ctx.flag("monthly_7_complete"): return 4.0
        if ctx.text("monthly_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def monthly_rule_8(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("monthly_score",0.0)
        if ctx.flag("monthly_blocked"): return -5.0
        if ctx.flag("monthly_8_complete"): return 1.0
        if ctx.text("monthly_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def monthly_rule_9(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("monthly_score",0.0)
        if ctx.flag("monthly_blocked"): return -5.0
        if ctx.flag("monthly_9_complete"): return 2.0
        if ctx.text("monthly_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def monthly_rule_10(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("monthly_score",0.0)
        if ctx.flag("monthly_blocked"): return -5.0
        if ctx.flag("monthly_10_complete"): return 3.0
        if ctx.text("monthly_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def monthly_rule_11(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("monthly_score",0.0)
        if ctx.flag("monthly_blocked"): return -5.0
        if ctx.flag("monthly_11_complete"): return 4.0
        if ctx.text("monthly_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def monthly_rule_12(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("monthly_score",0.0)
        if ctx.flag("monthly_blocked"): return -5.0
        if ctx.flag("monthly_12_complete"): return 1.0
        if ctx.text("monthly_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def monthly_rule_13(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("monthly_score",0.0)
        if ctx.flag("monthly_blocked"): return -5.0
        if ctx.flag("monthly_13_complete"): return 2.0
        if ctx.text("monthly_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def monthly_rule_14(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("monthly_score",0.0)
        if ctx.flag("monthly_blocked"): return -5.0
        if ctx.flag("monthly_14_complete"): return 3.0
        if ctx.text("monthly_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def quarterly_rule_1(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("quarterly_score",0.0)
        if ctx.flag("quarterly_blocked"): return -5.0
        if ctx.flag("quarterly_1_complete"): return 2.0
        if ctx.text("quarterly_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def quarterly_rule_2(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("quarterly_score",0.0)
        if ctx.flag("quarterly_blocked"): return -5.0
        if ctx.flag("quarterly_2_complete"): return 3.0
        if ctx.text("quarterly_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def quarterly_rule_3(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("quarterly_score",0.0)
        if ctx.flag("quarterly_blocked"): return -5.0
        if ctx.flag("quarterly_3_complete"): return 4.0
        if ctx.text("quarterly_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def quarterly_rule_4(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("quarterly_score",0.0)
        if ctx.flag("quarterly_blocked"): return -5.0
        if ctx.flag("quarterly_4_complete"): return 1.0
        if ctx.text("quarterly_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def quarterly_rule_5(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("quarterly_score",0.0)
        if ctx.flag("quarterly_blocked"): return -5.0
        if ctx.flag("quarterly_5_complete"): return 2.0
        if ctx.text("quarterly_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def quarterly_rule_6(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("quarterly_score",0.0)
        if ctx.flag("quarterly_blocked"): return -5.0
        if ctx.flag("quarterly_6_complete"): return 3.0
        if ctx.text("quarterly_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def quarterly_rule_7(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("quarterly_score",0.0)
        if ctx.flag("quarterly_blocked"): return -5.0
        if ctx.flag("quarterly_7_complete"): return 4.0
        if ctx.text("quarterly_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def quarterly_rule_8(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("quarterly_score",0.0)
        if ctx.flag("quarterly_blocked"): return -5.0
        if ctx.flag("quarterly_8_complete"): return 1.0
        if ctx.text("quarterly_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def quarterly_rule_9(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("quarterly_score",0.0)
        if ctx.flag("quarterly_blocked"): return -5.0
        if ctx.flag("quarterly_9_complete"): return 2.0
        if ctx.text("quarterly_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def quarterly_rule_10(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("quarterly_score",0.0)
        if ctx.flag("quarterly_blocked"): return -5.0
        if ctx.flag("quarterly_10_complete"): return 3.0
        if ctx.text("quarterly_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def quarterly_rule_11(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("quarterly_score",0.0)
        if ctx.flag("quarterly_blocked"): return -5.0
        if ctx.flag("quarterly_11_complete"): return 4.0
        if ctx.text("quarterly_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def quarterly_rule_12(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("quarterly_score",0.0)
        if ctx.flag("quarterly_blocked"): return -5.0
        if ctx.flag("quarterly_12_complete"): return 1.0
        if ctx.text("quarterly_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def quarterly_rule_13(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("quarterly_score",0.0)
        if ctx.flag("quarterly_blocked"): return -5.0
        if ctx.flag("quarterly_13_complete"): return 2.0
        if ctx.text("quarterly_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def quarterly_rule_14(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("quarterly_score",0.0)
        if ctx.flag("quarterly_blocked"): return -5.0
        if ctx.flag("quarterly_14_complete"): return 3.0
        if ctx.text("quarterly_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def role_rule_1(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_1_complete"): return 2.0
        if ctx.text("role_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def role_rule_2(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_2_complete"): return 3.0
        if ctx.text("role_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def role_rule_3(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_3_complete"): return 4.0
        if ctx.text("role_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def role_rule_4(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_4_complete"): return 1.0
        if ctx.text("role_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def role_rule_5(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_5_complete"): return 2.0
        if ctx.text("role_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def role_rule_6(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_6_complete"): return 3.0
        if ctx.text("role_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def role_rule_7(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_7_complete"): return 4.0
        if ctx.text("role_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def role_rule_8(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_8_complete"): return 1.0
        if ctx.text("role_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def role_rule_9(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_9_complete"): return 2.0
        if ctx.text("role_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def role_rule_10(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_10_complete"): return 3.0
        if ctx.text("role_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def role_rule_11(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_11_complete"): return 4.0
        if ctx.text("role_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def role_rule_12(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_12_complete"): return 1.0
        if ctx.text("role_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def role_rule_13(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_13_complete"): return 2.0
        if ctx.text("role_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def role_rule_14(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_14_complete"): return 3.0
        if ctx.text("role_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def company_rule_1(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_1_complete"): return 2.0
        if ctx.text("company_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def company_rule_2(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_2_complete"): return 3.0
        if ctx.text("company_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def company_rule_3(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_3_complete"): return 4.0
        if ctx.text("company_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def company_rule_4(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_4_complete"): return 1.0
        if ctx.text("company_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def company_rule_5(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_5_complete"): return 2.0
        if ctx.text("company_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def company_rule_6(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_6_complete"): return 3.0
        if ctx.text("company_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def company_rule_7(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_7_complete"): return 4.0
        if ctx.text("company_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def company_rule_8(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_8_complete"): return 1.0
        if ctx.text("company_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def company_rule_9(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_9_complete"): return 2.0
        if ctx.text("company_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def company_rule_10(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_10_complete"): return 3.0
        if ctx.text("company_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def company_rule_11(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_11_complete"): return 4.0
        if ctx.text("company_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def company_rule_12(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_12_complete"): return 1.0
        if ctx.text("company_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def company_rule_13(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_13_complete"): return 2.0
        if ctx.text("company_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def company_rule_14(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_14_complete"): return 3.0
        if ctx.text("company_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def source_rule_1(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("source_score",0.0)
        if ctx.flag("source_blocked"): return -5.0
        if ctx.flag("source_1_complete"): return 2.0
        if ctx.text("source_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def source_rule_2(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("source_score",0.0)
        if ctx.flag("source_blocked"): return -5.0
        if ctx.flag("source_2_complete"): return 3.0
        if ctx.text("source_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def source_rule_3(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("source_score",0.0)
        if ctx.flag("source_blocked"): return -5.0
        if ctx.flag("source_3_complete"): return 4.0
        if ctx.text("source_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def source_rule_4(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("source_score",0.0)
        if ctx.flag("source_blocked"): return -5.0
        if ctx.flag("source_4_complete"): return 1.0
        if ctx.text("source_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def source_rule_5(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("source_score",0.0)
        if ctx.flag("source_blocked"): return -5.0
        if ctx.flag("source_5_complete"): return 2.0
        if ctx.text("source_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def source_rule_6(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("source_score",0.0)
        if ctx.flag("source_blocked"): return -5.0
        if ctx.flag("source_6_complete"): return 3.0
        if ctx.text("source_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def source_rule_7(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("source_score",0.0)
        if ctx.flag("source_blocked"): return -5.0
        if ctx.flag("source_7_complete"): return 4.0
        if ctx.text("source_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def source_rule_8(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("source_score",0.0)
        if ctx.flag("source_blocked"): return -5.0
        if ctx.flag("source_8_complete"): return 1.0
        if ctx.text("source_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def source_rule_9(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("source_score",0.0)
        if ctx.flag("source_blocked"): return -5.0
        if ctx.flag("source_9_complete"): return 2.0
        if ctx.text("source_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def source_rule_10(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("source_score",0.0)
        if ctx.flag("source_blocked"): return -5.0
        if ctx.flag("source_10_complete"): return 3.0
        if ctx.text("source_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def source_rule_11(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("source_score",0.0)
        if ctx.flag("source_blocked"): return -5.0
        if ctx.flag("source_11_complete"): return 4.0
        if ctx.text("source_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def source_rule_12(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("source_score",0.0)
        if ctx.flag("source_blocked"): return -5.0
        if ctx.flag("source_12_complete"): return 1.0
        if ctx.text("source_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def source_rule_13(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("source_score",0.0)
        if ctx.flag("source_blocked"): return -5.0
        if ctx.flag("source_13_complete"): return 2.0
        if ctx.text("source_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def source_rule_14(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("source_score",0.0)
        if ctx.flag("source_blocked"): return -5.0
        if ctx.flag("source_14_complete"): return 3.0
        if ctx.text("source_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def status_rule_1(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("status_score",0.0)
        if ctx.flag("status_blocked"): return -5.0
        if ctx.flag("status_1_complete"): return 2.0
        if ctx.text("status_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def status_rule_2(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("status_score",0.0)
        if ctx.flag("status_blocked"): return -5.0
        if ctx.flag("status_2_complete"): return 3.0
        if ctx.text("status_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def status_rule_3(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("status_score",0.0)
        if ctx.flag("status_blocked"): return -5.0
        if ctx.flag("status_3_complete"): return 4.0
        if ctx.text("status_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def status_rule_4(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("status_score",0.0)
        if ctx.flag("status_blocked"): return -5.0
        if ctx.flag("status_4_complete"): return 1.0
        if ctx.text("status_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def status_rule_5(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("status_score",0.0)
        if ctx.flag("status_blocked"): return -5.0
        if ctx.flag("status_5_complete"): return 2.0
        if ctx.text("status_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def status_rule_6(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("status_score",0.0)
        if ctx.flag("status_blocked"): return -5.0
        if ctx.flag("status_6_complete"): return 3.0
        if ctx.text("status_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def status_rule_7(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("status_score",0.0)
        if ctx.flag("status_blocked"): return -5.0
        if ctx.flag("status_7_complete"): return 4.0
        if ctx.text("status_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def status_rule_8(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("status_score",0.0)
        if ctx.flag("status_blocked"): return -5.0
        if ctx.flag("status_8_complete"): return 1.0
        if ctx.text("status_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def status_rule_9(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("status_score",0.0)
        if ctx.flag("status_blocked"): return -5.0
        if ctx.flag("status_9_complete"): return 2.0
        if ctx.text("status_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def status_rule_10(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("status_score",0.0)
        if ctx.flag("status_blocked"): return -5.0
        if ctx.flag("status_10_complete"): return 3.0
        if ctx.text("status_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def status_rule_11(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("status_score",0.0)
        if ctx.flag("status_blocked"): return -5.0
        if ctx.flag("status_11_complete"): return 4.0
        if ctx.text("status_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def status_rule_12(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("status_score",0.0)
        if ctx.flag("status_blocked"): return -5.0
        if ctx.flag("status_12_complete"): return 1.0
        if ctx.text("status_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def status_rule_13(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("status_score",0.0)
        if ctx.flag("status_blocked"): return -5.0
        if ctx.flag("status_13_complete"): return 2.0
        if ctx.text("status_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def status_rule_14(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("status_score",0.0)
        if ctx.flag("status_blocked"): return -5.0
        if ctx.flag("status_14_complete"): return 3.0
        if ctx.text("status_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def salary_rule_1(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("salary_score",0.0)
        if ctx.flag("salary_blocked"): return -5.0
        if ctx.flag("salary_1_complete"): return 2.0
        if ctx.text("salary_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def salary_rule_2(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("salary_score",0.0)
        if ctx.flag("salary_blocked"): return -5.0
        if ctx.flag("salary_2_complete"): return 3.0
        if ctx.text("salary_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def salary_rule_3(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("salary_score",0.0)
        if ctx.flag("salary_blocked"): return -5.0
        if ctx.flag("salary_3_complete"): return 4.0
        if ctx.text("salary_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def salary_rule_4(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("salary_score",0.0)
        if ctx.flag("salary_blocked"): return -5.0
        if ctx.flag("salary_4_complete"): return 1.0
        if ctx.text("salary_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def salary_rule_5(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("salary_score",0.0)
        if ctx.flag("salary_blocked"): return -5.0
        if ctx.flag("salary_5_complete"): return 2.0
        if ctx.text("salary_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def salary_rule_6(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("salary_score",0.0)
        if ctx.flag("salary_blocked"): return -5.0
        if ctx.flag("salary_6_complete"): return 3.0
        if ctx.text("salary_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def salary_rule_7(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("salary_score",0.0)
        if ctx.flag("salary_blocked"): return -5.0
        if ctx.flag("salary_7_complete"): return 4.0
        if ctx.text("salary_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def salary_rule_8(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("salary_score",0.0)
        if ctx.flag("salary_blocked"): return -5.0
        if ctx.flag("salary_8_complete"): return 1.0
        if ctx.text("salary_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def salary_rule_9(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("salary_score",0.0)
        if ctx.flag("salary_blocked"): return -5.0
        if ctx.flag("salary_9_complete"): return 2.0
        if ctx.text("salary_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def salary_rule_10(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("salary_score",0.0)
        if ctx.flag("salary_blocked"): return -5.0
        if ctx.flag("salary_10_complete"): return 3.0
        if ctx.text("salary_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def salary_rule_11(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("salary_score",0.0)
        if ctx.flag("salary_blocked"): return -5.0
        if ctx.flag("salary_11_complete"): return 4.0
        if ctx.text("salary_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def salary_rule_12(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("salary_score",0.0)
        if ctx.flag("salary_blocked"): return -5.0
        if ctx.flag("salary_12_complete"): return 1.0
        if ctx.text("salary_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def salary_rule_13(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("salary_score",0.0)
        if ctx.flag("salary_blocked"): return -5.0
        if ctx.flag("salary_13_complete"): return 2.0
        if ctx.text("salary_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def salary_rule_14(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("salary_score",0.0)
        if ctx.flag("salary_blocked"): return -5.0
        if ctx.flag("salary_14_complete"): return 3.0
        if ctx.text("salary_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def location_rule_1(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_1_complete"): return 2.0
        if ctx.text("location_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def location_rule_2(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_2_complete"): return 3.0
        if ctx.text("location_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def location_rule_3(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_3_complete"): return 4.0
        if ctx.text("location_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def location_rule_4(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_4_complete"): return 1.0
        if ctx.text("location_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def location_rule_5(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_5_complete"): return 2.0
        if ctx.text("location_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def location_rule_6(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_6_complete"): return 3.0
        if ctx.text("location_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def location_rule_7(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_7_complete"): return 4.0
        if ctx.text("location_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def location_rule_8(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_8_complete"): return 1.0
        if ctx.text("location_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def location_rule_9(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_9_complete"): return 2.0
        if ctx.text("location_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def location_rule_10(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_10_complete"): return 3.0
        if ctx.text("location_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def location_rule_11(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_11_complete"): return 4.0
        if ctx.text("location_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def location_rule_12(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_12_complete"): return 1.0
        if ctx.text("location_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def location_rule_13(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_13_complete"): return 2.0
        if ctx.text("location_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def location_rule_14(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_14_complete"): return 3.0
        if ctx.text("location_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def seniority_rule_1(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("seniority_score",0.0)
        if ctx.flag("seniority_blocked"): return -5.0
        if ctx.flag("seniority_1_complete"): return 2.0
        if ctx.text("seniority_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def seniority_rule_2(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("seniority_score",0.0)
        if ctx.flag("seniority_blocked"): return -5.0
        if ctx.flag("seniority_2_complete"): return 3.0
        if ctx.text("seniority_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def seniority_rule_3(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("seniority_score",0.0)
        if ctx.flag("seniority_blocked"): return -5.0
        if ctx.flag("seniority_3_complete"): return 4.0
        if ctx.text("seniority_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def seniority_rule_4(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("seniority_score",0.0)
        if ctx.flag("seniority_blocked"): return -5.0
        if ctx.flag("seniority_4_complete"): return 1.0
        if ctx.text("seniority_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def seniority_rule_5(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("seniority_score",0.0)
        if ctx.flag("seniority_blocked"): return -5.0
        if ctx.flag("seniority_5_complete"): return 2.0
        if ctx.text("seniority_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def seniority_rule_6(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("seniority_score",0.0)
        if ctx.flag("seniority_blocked"): return -5.0
        if ctx.flag("seniority_6_complete"): return 3.0
        if ctx.text("seniority_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def seniority_rule_7(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("seniority_score",0.0)
        if ctx.flag("seniority_blocked"): return -5.0
        if ctx.flag("seniority_7_complete"): return 4.0
        if ctx.text("seniority_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def seniority_rule_8(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("seniority_score",0.0)
        if ctx.flag("seniority_blocked"): return -5.0
        if ctx.flag("seniority_8_complete"): return 1.0
        if ctx.text("seniority_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def seniority_rule_9(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("seniority_score",0.0)
        if ctx.flag("seniority_blocked"): return -5.0
        if ctx.flag("seniority_9_complete"): return 2.0
        if ctx.text("seniority_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def seniority_rule_10(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("seniority_score",0.0)
        if ctx.flag("seniority_blocked"): return -5.0
        if ctx.flag("seniority_10_complete"): return 3.0
        if ctx.text("seniority_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def seniority_rule_11(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("seniority_score",0.0)
        if ctx.flag("seniority_blocked"): return -5.0
        if ctx.flag("seniority_11_complete"): return 4.0
        if ctx.text("seniority_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def seniority_rule_12(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("seniority_score",0.0)
        if ctx.flag("seniority_blocked"): return -5.0
        if ctx.flag("seniority_12_complete"): return 1.0
        if ctx.text("seniority_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def seniority_rule_13(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("seniority_score",0.0)
        if ctx.flag("seniority_blocked"): return -5.0
        if ctx.flag("seniority_13_complete"): return 2.0
        if ctx.text("seniority_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def seniority_rule_14(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("seniority_score",0.0)
        if ctx.flag("seniority_blocked"): return -5.0
        if ctx.flag("seniority_14_complete"): return 3.0
        if ctx.text("seniority_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def remote_rule_1(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("remote_score",0.0)
        if ctx.flag("remote_blocked"): return -5.0
        if ctx.flag("remote_1_complete"): return 2.0
        if ctx.text("remote_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def remote_rule_2(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("remote_score",0.0)
        if ctx.flag("remote_blocked"): return -5.0
        if ctx.flag("remote_2_complete"): return 3.0
        if ctx.text("remote_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def remote_rule_3(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("remote_score",0.0)
        if ctx.flag("remote_blocked"): return -5.0
        if ctx.flag("remote_3_complete"): return 4.0
        if ctx.text("remote_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def remote_rule_4(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("remote_score",0.0)
        if ctx.flag("remote_blocked"): return -5.0
        if ctx.flag("remote_4_complete"): return 1.0
        if ctx.text("remote_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def remote_rule_5(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("remote_score",0.0)
        if ctx.flag("remote_blocked"): return -5.0
        if ctx.flag("remote_5_complete"): return 2.0
        if ctx.text("remote_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def remote_rule_6(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("remote_score",0.0)
        if ctx.flag("remote_blocked"): return -5.0
        if ctx.flag("remote_6_complete"): return 3.0
        if ctx.text("remote_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def remote_rule_7(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("remote_score",0.0)
        if ctx.flag("remote_blocked"): return -5.0
        if ctx.flag("remote_7_complete"): return 4.0
        if ctx.text("remote_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def remote_rule_8(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("remote_score",0.0)
        if ctx.flag("remote_blocked"): return -5.0
        if ctx.flag("remote_8_complete"): return 1.0
        if ctx.text("remote_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def remote_rule_9(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("remote_score",0.0)
        if ctx.flag("remote_blocked"): return -5.0
        if ctx.flag("remote_9_complete"): return 2.0
        if ctx.text("remote_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def remote_rule_10(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("remote_score",0.0)
        if ctx.flag("remote_blocked"): return -5.0
        if ctx.flag("remote_10_complete"): return 3.0
        if ctx.text("remote_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def remote_rule_11(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("remote_score",0.0)
        if ctx.flag("remote_blocked"): return -5.0
        if ctx.flag("remote_11_complete"): return 4.0
        if ctx.text("remote_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def remote_rule_12(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("remote_score",0.0)
        if ctx.flag("remote_blocked"): return -5.0
        if ctx.flag("remote_12_complete"): return 1.0
        if ctx.text("remote_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def remote_rule_13(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("remote_score",0.0)
        if ctx.flag("remote_blocked"): return -5.0
        if ctx.flag("remote_13_complete"): return 2.0
        if ctx.text("remote_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def remote_rule_14(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("remote_score",0.0)
        if ctx.flag("remote_blocked"): return -5.0
        if ctx.flag("remote_14_complete"): return 3.0
        if ctx.text("remote_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def channel_rule_1(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("channel_score",0.0)
        if ctx.flag("channel_blocked"): return -5.0
        if ctx.flag("channel_1_complete"): return 2.0
        if ctx.text("channel_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def channel_rule_2(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("channel_score",0.0)
        if ctx.flag("channel_blocked"): return -5.0
        if ctx.flag("channel_2_complete"): return 3.0
        if ctx.text("channel_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def channel_rule_3(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("channel_score",0.0)
        if ctx.flag("channel_blocked"): return -5.0
        if ctx.flag("channel_3_complete"): return 4.0
        if ctx.text("channel_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def channel_rule_4(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("channel_score",0.0)
        if ctx.flag("channel_blocked"): return -5.0
        if ctx.flag("channel_4_complete"): return 1.0
        if ctx.text("channel_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def channel_rule_5(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("channel_score",0.0)
        if ctx.flag("channel_blocked"): return -5.0
        if ctx.flag("channel_5_complete"): return 2.0
        if ctx.text("channel_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def channel_rule_6(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("channel_score",0.0)
        if ctx.flag("channel_blocked"): return -5.0
        if ctx.flag("channel_6_complete"): return 3.0
        if ctx.text("channel_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def channel_rule_7(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("channel_score",0.0)
        if ctx.flag("channel_blocked"): return -5.0
        if ctx.flag("channel_7_complete"): return 4.0
        if ctx.text("channel_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def channel_rule_8(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("channel_score",0.0)
        if ctx.flag("channel_blocked"): return -5.0
        if ctx.flag("channel_8_complete"): return 1.0
        if ctx.text("channel_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def channel_rule_9(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("channel_score",0.0)
        if ctx.flag("channel_blocked"): return -5.0
        if ctx.flag("channel_9_complete"): return 2.0
        if ctx.text("channel_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def channel_rule_10(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("channel_score",0.0)
        if ctx.flag("channel_blocked"): return -5.0
        if ctx.flag("channel_10_complete"): return 3.0
        if ctx.text("channel_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def channel_rule_11(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("channel_score",0.0)
        if ctx.flag("channel_blocked"): return -5.0
        if ctx.flag("channel_11_complete"): return 4.0
        if ctx.text("channel_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def channel_rule_12(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("channel_score",0.0)
        if ctx.flag("channel_blocked"): return -5.0
        if ctx.flag("channel_12_complete"): return 1.0
        if ctx.text("channel_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def channel_rule_13(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("channel_score",0.0)
        if ctx.flag("channel_blocked"): return -5.0
        if ctx.flag("channel_13_complete"): return 2.0
        if ctx.text("channel_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def channel_rule_14(self,ctx:AnalyticsSegmentsContext)->float:
        value=ctx.number("channel_score",0.0)
        if ctx.flag("channel_blocked"): return -5.0
        if ctx.flag("channel_14_complete"): return 3.0
        if ctx.text("channel_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def evaluate_many(self,records:Sequence[Mapping[str,object]])->list[AnalyticsSegmentsResult]:
        return [self.evaluate(record) for record in records]
    def summarize(self,results:Sequence[AnalyticsSegmentsResult])->dict[str,object]:
        scores=[item.score for item in results]
        return {"count":len(scores),"average":round(sum(scores)/len(scores),2) if scores else 0.0,"strong":sum(x.status=="strong" for x in results),"acceptable":sum(x.status=="acceptable" for x in results),"review":sum(x.status=="review" for x in results)}
