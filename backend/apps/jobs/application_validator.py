"""Deterministic application_validator domain engine for job-search workflows."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Mapping, Sequence

@dataclass(frozen=True)
class ApplicationValidatorResult:
    key: str
    score: float
    status: str
    reasons: tuple[str, ...] = ()

@dataclass
class ApplicationValidatorContext:
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

class ApplicationValidatorEngine:
    def evaluate(self, context:Mapping[str,object]|ApplicationValidatorContext|None=None)->ApplicationValidatorResult:
        ctx=context if isinstance(context,ApplicationValidatorContext) else ApplicationValidatorContext(dict(context or {}))
        score=50.0; reasons=[]
        for area in ["identity","company","role","url","salary","location","status","dates","notes","contact","resume","consistency"]:
            delta=self._area_score(area,ctx); score+=delta
            if delta>0: reasons.append(f"{area}: positive")
            if delta<0: reasons.append(f"{area}: review")
        score=clamp(score)
        status="strong" if score>=80 else "acceptable" if score>=60 else "review"
        return ApplicationValidatorResult("overall",round(score,2),status,tuple(reasons))
    def _area_score(self,area:str,ctx:ApplicationValidatorContext)->float:
        if ctx.flag(f"{area}_blocked"): return -5.0
        if ctx.flag(f"{area}_complete"): return 3.0
        if ctx.text(area): return 1.0
        return -1.0
    def identity_rule_1(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("identity_score",0.0)
        if ctx.flag("identity_blocked"): return -5.0
        if ctx.flag("identity_1_complete"): return 2.0
        if ctx.text("identity_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def identity_rule_2(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("identity_score",0.0)
        if ctx.flag("identity_blocked"): return -5.0
        if ctx.flag("identity_2_complete"): return 3.0
        if ctx.text("identity_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def identity_rule_3(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("identity_score",0.0)
        if ctx.flag("identity_blocked"): return -5.0
        if ctx.flag("identity_3_complete"): return 4.0
        if ctx.text("identity_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def identity_rule_4(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("identity_score",0.0)
        if ctx.flag("identity_blocked"): return -5.0
        if ctx.flag("identity_4_complete"): return 1.0
        if ctx.text("identity_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def identity_rule_5(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("identity_score",0.0)
        if ctx.flag("identity_blocked"): return -5.0
        if ctx.flag("identity_5_complete"): return 2.0
        if ctx.text("identity_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def identity_rule_6(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("identity_score",0.0)
        if ctx.flag("identity_blocked"): return -5.0
        if ctx.flag("identity_6_complete"): return 3.0
        if ctx.text("identity_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def identity_rule_7(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("identity_score",0.0)
        if ctx.flag("identity_blocked"): return -5.0
        if ctx.flag("identity_7_complete"): return 4.0
        if ctx.text("identity_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def identity_rule_8(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("identity_score",0.0)
        if ctx.flag("identity_blocked"): return -5.0
        if ctx.flag("identity_8_complete"): return 1.0
        if ctx.text("identity_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def identity_rule_9(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("identity_score",0.0)
        if ctx.flag("identity_blocked"): return -5.0
        if ctx.flag("identity_9_complete"): return 2.0
        if ctx.text("identity_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def identity_rule_10(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("identity_score",0.0)
        if ctx.flag("identity_blocked"): return -5.0
        if ctx.flag("identity_10_complete"): return 3.0
        if ctx.text("identity_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def identity_rule_11(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("identity_score",0.0)
        if ctx.flag("identity_blocked"): return -5.0
        if ctx.flag("identity_11_complete"): return 4.0
        if ctx.text("identity_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def identity_rule_12(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("identity_score",0.0)
        if ctx.flag("identity_blocked"): return -5.0
        if ctx.flag("identity_12_complete"): return 1.0
        if ctx.text("identity_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def identity_rule_13(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("identity_score",0.0)
        if ctx.flag("identity_blocked"): return -5.0
        if ctx.flag("identity_13_complete"): return 2.0
        if ctx.text("identity_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def identity_rule_14(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("identity_score",0.0)
        if ctx.flag("identity_blocked"): return -5.0
        if ctx.flag("identity_14_complete"): return 3.0
        if ctx.text("identity_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def company_rule_1(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_1_complete"): return 2.0
        if ctx.text("company_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def company_rule_2(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_2_complete"): return 3.0
        if ctx.text("company_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def company_rule_3(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_3_complete"): return 4.0
        if ctx.text("company_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def company_rule_4(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_4_complete"): return 1.0
        if ctx.text("company_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def company_rule_5(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_5_complete"): return 2.0
        if ctx.text("company_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def company_rule_6(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_6_complete"): return 3.0
        if ctx.text("company_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def company_rule_7(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_7_complete"): return 4.0
        if ctx.text("company_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def company_rule_8(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_8_complete"): return 1.0
        if ctx.text("company_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def company_rule_9(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_9_complete"): return 2.0
        if ctx.text("company_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def company_rule_10(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_10_complete"): return 3.0
        if ctx.text("company_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def company_rule_11(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_11_complete"): return 4.0
        if ctx.text("company_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def company_rule_12(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_12_complete"): return 1.0
        if ctx.text("company_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def company_rule_13(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_13_complete"): return 2.0
        if ctx.text("company_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def company_rule_14(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_14_complete"): return 3.0
        if ctx.text("company_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def role_rule_1(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_1_complete"): return 2.0
        if ctx.text("role_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def role_rule_2(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_2_complete"): return 3.0
        if ctx.text("role_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def role_rule_3(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_3_complete"): return 4.0
        if ctx.text("role_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def role_rule_4(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_4_complete"): return 1.0
        if ctx.text("role_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def role_rule_5(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_5_complete"): return 2.0
        if ctx.text("role_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def role_rule_6(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_6_complete"): return 3.0
        if ctx.text("role_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def role_rule_7(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_7_complete"): return 4.0
        if ctx.text("role_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def role_rule_8(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_8_complete"): return 1.0
        if ctx.text("role_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def role_rule_9(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_9_complete"): return 2.0
        if ctx.text("role_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def role_rule_10(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_10_complete"): return 3.0
        if ctx.text("role_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def role_rule_11(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_11_complete"): return 4.0
        if ctx.text("role_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def role_rule_12(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_12_complete"): return 1.0
        if ctx.text("role_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def role_rule_13(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_13_complete"): return 2.0
        if ctx.text("role_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def role_rule_14(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_14_complete"): return 3.0
        if ctx.text("role_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def url_rule_1(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("url_score",0.0)
        if ctx.flag("url_blocked"): return -5.0
        if ctx.flag("url_1_complete"): return 2.0
        if ctx.text("url_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def url_rule_2(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("url_score",0.0)
        if ctx.flag("url_blocked"): return -5.0
        if ctx.flag("url_2_complete"): return 3.0
        if ctx.text("url_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def url_rule_3(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("url_score",0.0)
        if ctx.flag("url_blocked"): return -5.0
        if ctx.flag("url_3_complete"): return 4.0
        if ctx.text("url_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def url_rule_4(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("url_score",0.0)
        if ctx.flag("url_blocked"): return -5.0
        if ctx.flag("url_4_complete"): return 1.0
        if ctx.text("url_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def url_rule_5(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("url_score",0.0)
        if ctx.flag("url_blocked"): return -5.0
        if ctx.flag("url_5_complete"): return 2.0
        if ctx.text("url_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def url_rule_6(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("url_score",0.0)
        if ctx.flag("url_blocked"): return -5.0
        if ctx.flag("url_6_complete"): return 3.0
        if ctx.text("url_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def url_rule_7(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("url_score",0.0)
        if ctx.flag("url_blocked"): return -5.0
        if ctx.flag("url_7_complete"): return 4.0
        if ctx.text("url_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def url_rule_8(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("url_score",0.0)
        if ctx.flag("url_blocked"): return -5.0
        if ctx.flag("url_8_complete"): return 1.0
        if ctx.text("url_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def url_rule_9(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("url_score",0.0)
        if ctx.flag("url_blocked"): return -5.0
        if ctx.flag("url_9_complete"): return 2.0
        if ctx.text("url_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def url_rule_10(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("url_score",0.0)
        if ctx.flag("url_blocked"): return -5.0
        if ctx.flag("url_10_complete"): return 3.0
        if ctx.text("url_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def url_rule_11(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("url_score",0.0)
        if ctx.flag("url_blocked"): return -5.0
        if ctx.flag("url_11_complete"): return 4.0
        if ctx.text("url_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def url_rule_12(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("url_score",0.0)
        if ctx.flag("url_blocked"): return -5.0
        if ctx.flag("url_12_complete"): return 1.0
        if ctx.text("url_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def url_rule_13(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("url_score",0.0)
        if ctx.flag("url_blocked"): return -5.0
        if ctx.flag("url_13_complete"): return 2.0
        if ctx.text("url_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def url_rule_14(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("url_score",0.0)
        if ctx.flag("url_blocked"): return -5.0
        if ctx.flag("url_14_complete"): return 3.0
        if ctx.text("url_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def salary_rule_1(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("salary_score",0.0)
        if ctx.flag("salary_blocked"): return -5.0
        if ctx.flag("salary_1_complete"): return 2.0
        if ctx.text("salary_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def salary_rule_2(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("salary_score",0.0)
        if ctx.flag("salary_blocked"): return -5.0
        if ctx.flag("salary_2_complete"): return 3.0
        if ctx.text("salary_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def salary_rule_3(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("salary_score",0.0)
        if ctx.flag("salary_blocked"): return -5.0
        if ctx.flag("salary_3_complete"): return 4.0
        if ctx.text("salary_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def salary_rule_4(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("salary_score",0.0)
        if ctx.flag("salary_blocked"): return -5.0
        if ctx.flag("salary_4_complete"): return 1.0
        if ctx.text("salary_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def salary_rule_5(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("salary_score",0.0)
        if ctx.flag("salary_blocked"): return -5.0
        if ctx.flag("salary_5_complete"): return 2.0
        if ctx.text("salary_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def salary_rule_6(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("salary_score",0.0)
        if ctx.flag("salary_blocked"): return -5.0
        if ctx.flag("salary_6_complete"): return 3.0
        if ctx.text("salary_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def salary_rule_7(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("salary_score",0.0)
        if ctx.flag("salary_blocked"): return -5.0
        if ctx.flag("salary_7_complete"): return 4.0
        if ctx.text("salary_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def salary_rule_8(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("salary_score",0.0)
        if ctx.flag("salary_blocked"): return -5.0
        if ctx.flag("salary_8_complete"): return 1.0
        if ctx.text("salary_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def salary_rule_9(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("salary_score",0.0)
        if ctx.flag("salary_blocked"): return -5.0
        if ctx.flag("salary_9_complete"): return 2.0
        if ctx.text("salary_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def salary_rule_10(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("salary_score",0.0)
        if ctx.flag("salary_blocked"): return -5.0
        if ctx.flag("salary_10_complete"): return 3.0
        if ctx.text("salary_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def salary_rule_11(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("salary_score",0.0)
        if ctx.flag("salary_blocked"): return -5.0
        if ctx.flag("salary_11_complete"): return 4.0
        if ctx.text("salary_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def salary_rule_12(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("salary_score",0.0)
        if ctx.flag("salary_blocked"): return -5.0
        if ctx.flag("salary_12_complete"): return 1.0
        if ctx.text("salary_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def salary_rule_13(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("salary_score",0.0)
        if ctx.flag("salary_blocked"): return -5.0
        if ctx.flag("salary_13_complete"): return 2.0
        if ctx.text("salary_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def salary_rule_14(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("salary_score",0.0)
        if ctx.flag("salary_blocked"): return -5.0
        if ctx.flag("salary_14_complete"): return 3.0
        if ctx.text("salary_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def location_rule_1(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_1_complete"): return 2.0
        if ctx.text("location_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def location_rule_2(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_2_complete"): return 3.0
        if ctx.text("location_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def location_rule_3(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_3_complete"): return 4.0
        if ctx.text("location_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def location_rule_4(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_4_complete"): return 1.0
        if ctx.text("location_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def location_rule_5(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_5_complete"): return 2.0
        if ctx.text("location_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def location_rule_6(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_6_complete"): return 3.0
        if ctx.text("location_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def location_rule_7(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_7_complete"): return 4.0
        if ctx.text("location_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def location_rule_8(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_8_complete"): return 1.0
        if ctx.text("location_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def location_rule_9(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_9_complete"): return 2.0
        if ctx.text("location_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def location_rule_10(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_10_complete"): return 3.0
        if ctx.text("location_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def location_rule_11(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_11_complete"): return 4.0
        if ctx.text("location_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def location_rule_12(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_12_complete"): return 1.0
        if ctx.text("location_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def location_rule_13(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_13_complete"): return 2.0
        if ctx.text("location_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def location_rule_14(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("location_score",0.0)
        if ctx.flag("location_blocked"): return -5.0
        if ctx.flag("location_14_complete"): return 3.0
        if ctx.text("location_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def status_rule_1(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("status_score",0.0)
        if ctx.flag("status_blocked"): return -5.0
        if ctx.flag("status_1_complete"): return 2.0
        if ctx.text("status_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def status_rule_2(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("status_score",0.0)
        if ctx.flag("status_blocked"): return -5.0
        if ctx.flag("status_2_complete"): return 3.0
        if ctx.text("status_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def status_rule_3(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("status_score",0.0)
        if ctx.flag("status_blocked"): return -5.0
        if ctx.flag("status_3_complete"): return 4.0
        if ctx.text("status_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def status_rule_4(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("status_score",0.0)
        if ctx.flag("status_blocked"): return -5.0
        if ctx.flag("status_4_complete"): return 1.0
        if ctx.text("status_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def status_rule_5(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("status_score",0.0)
        if ctx.flag("status_blocked"): return -5.0
        if ctx.flag("status_5_complete"): return 2.0
        if ctx.text("status_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def status_rule_6(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("status_score",0.0)
        if ctx.flag("status_blocked"): return -5.0
        if ctx.flag("status_6_complete"): return 3.0
        if ctx.text("status_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def status_rule_7(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("status_score",0.0)
        if ctx.flag("status_blocked"): return -5.0
        if ctx.flag("status_7_complete"): return 4.0
        if ctx.text("status_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def status_rule_8(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("status_score",0.0)
        if ctx.flag("status_blocked"): return -5.0
        if ctx.flag("status_8_complete"): return 1.0
        if ctx.text("status_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def status_rule_9(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("status_score",0.0)
        if ctx.flag("status_blocked"): return -5.0
        if ctx.flag("status_9_complete"): return 2.0
        if ctx.text("status_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def status_rule_10(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("status_score",0.0)
        if ctx.flag("status_blocked"): return -5.0
        if ctx.flag("status_10_complete"): return 3.0
        if ctx.text("status_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def status_rule_11(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("status_score",0.0)
        if ctx.flag("status_blocked"): return -5.0
        if ctx.flag("status_11_complete"): return 4.0
        if ctx.text("status_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def status_rule_12(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("status_score",0.0)
        if ctx.flag("status_blocked"): return -5.0
        if ctx.flag("status_12_complete"): return 1.0
        if ctx.text("status_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def status_rule_13(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("status_score",0.0)
        if ctx.flag("status_blocked"): return -5.0
        if ctx.flag("status_13_complete"): return 2.0
        if ctx.text("status_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def status_rule_14(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("status_score",0.0)
        if ctx.flag("status_blocked"): return -5.0
        if ctx.flag("status_14_complete"): return 3.0
        if ctx.text("status_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def dates_rule_1(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("dates_score",0.0)
        if ctx.flag("dates_blocked"): return -5.0
        if ctx.flag("dates_1_complete"): return 2.0
        if ctx.text("dates_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def dates_rule_2(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("dates_score",0.0)
        if ctx.flag("dates_blocked"): return -5.0
        if ctx.flag("dates_2_complete"): return 3.0
        if ctx.text("dates_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def dates_rule_3(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("dates_score",0.0)
        if ctx.flag("dates_blocked"): return -5.0
        if ctx.flag("dates_3_complete"): return 4.0
        if ctx.text("dates_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def dates_rule_4(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("dates_score",0.0)
        if ctx.flag("dates_blocked"): return -5.0
        if ctx.flag("dates_4_complete"): return 1.0
        if ctx.text("dates_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def dates_rule_5(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("dates_score",0.0)
        if ctx.flag("dates_blocked"): return -5.0
        if ctx.flag("dates_5_complete"): return 2.0
        if ctx.text("dates_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def dates_rule_6(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("dates_score",0.0)
        if ctx.flag("dates_blocked"): return -5.0
        if ctx.flag("dates_6_complete"): return 3.0
        if ctx.text("dates_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def dates_rule_7(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("dates_score",0.0)
        if ctx.flag("dates_blocked"): return -5.0
        if ctx.flag("dates_7_complete"): return 4.0
        if ctx.text("dates_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def dates_rule_8(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("dates_score",0.0)
        if ctx.flag("dates_blocked"): return -5.0
        if ctx.flag("dates_8_complete"): return 1.0
        if ctx.text("dates_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def dates_rule_9(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("dates_score",0.0)
        if ctx.flag("dates_blocked"): return -5.0
        if ctx.flag("dates_9_complete"): return 2.0
        if ctx.text("dates_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def dates_rule_10(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("dates_score",0.0)
        if ctx.flag("dates_blocked"): return -5.0
        if ctx.flag("dates_10_complete"): return 3.0
        if ctx.text("dates_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def dates_rule_11(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("dates_score",0.0)
        if ctx.flag("dates_blocked"): return -5.0
        if ctx.flag("dates_11_complete"): return 4.0
        if ctx.text("dates_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def dates_rule_12(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("dates_score",0.0)
        if ctx.flag("dates_blocked"): return -5.0
        if ctx.flag("dates_12_complete"): return 1.0
        if ctx.text("dates_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def dates_rule_13(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("dates_score",0.0)
        if ctx.flag("dates_blocked"): return -5.0
        if ctx.flag("dates_13_complete"): return 2.0
        if ctx.text("dates_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def dates_rule_14(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("dates_score",0.0)
        if ctx.flag("dates_blocked"): return -5.0
        if ctx.flag("dates_14_complete"): return 3.0
        if ctx.text("dates_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def notes_rule_1(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("notes_score",0.0)
        if ctx.flag("notes_blocked"): return -5.0
        if ctx.flag("notes_1_complete"): return 2.0
        if ctx.text("notes_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def notes_rule_2(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("notes_score",0.0)
        if ctx.flag("notes_blocked"): return -5.0
        if ctx.flag("notes_2_complete"): return 3.0
        if ctx.text("notes_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def notes_rule_3(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("notes_score",0.0)
        if ctx.flag("notes_blocked"): return -5.0
        if ctx.flag("notes_3_complete"): return 4.0
        if ctx.text("notes_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def notes_rule_4(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("notes_score",0.0)
        if ctx.flag("notes_blocked"): return -5.0
        if ctx.flag("notes_4_complete"): return 1.0
        if ctx.text("notes_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def notes_rule_5(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("notes_score",0.0)
        if ctx.flag("notes_blocked"): return -5.0
        if ctx.flag("notes_5_complete"): return 2.0
        if ctx.text("notes_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def notes_rule_6(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("notes_score",0.0)
        if ctx.flag("notes_blocked"): return -5.0
        if ctx.flag("notes_6_complete"): return 3.0
        if ctx.text("notes_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def notes_rule_7(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("notes_score",0.0)
        if ctx.flag("notes_blocked"): return -5.0
        if ctx.flag("notes_7_complete"): return 4.0
        if ctx.text("notes_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def notes_rule_8(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("notes_score",0.0)
        if ctx.flag("notes_blocked"): return -5.0
        if ctx.flag("notes_8_complete"): return 1.0
        if ctx.text("notes_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def notes_rule_9(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("notes_score",0.0)
        if ctx.flag("notes_blocked"): return -5.0
        if ctx.flag("notes_9_complete"): return 2.0
        if ctx.text("notes_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def notes_rule_10(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("notes_score",0.0)
        if ctx.flag("notes_blocked"): return -5.0
        if ctx.flag("notes_10_complete"): return 3.0
        if ctx.text("notes_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def notes_rule_11(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("notes_score",0.0)
        if ctx.flag("notes_blocked"): return -5.0
        if ctx.flag("notes_11_complete"): return 4.0
        if ctx.text("notes_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def notes_rule_12(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("notes_score",0.0)
        if ctx.flag("notes_blocked"): return -5.0
        if ctx.flag("notes_12_complete"): return 1.0
        if ctx.text("notes_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def notes_rule_13(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("notes_score",0.0)
        if ctx.flag("notes_blocked"): return -5.0
        if ctx.flag("notes_13_complete"): return 2.0
        if ctx.text("notes_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def notes_rule_14(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("notes_score",0.0)
        if ctx.flag("notes_blocked"): return -5.0
        if ctx.flag("notes_14_complete"): return 3.0
        if ctx.text("notes_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def contact_rule_1(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("contact_score",0.0)
        if ctx.flag("contact_blocked"): return -5.0
        if ctx.flag("contact_1_complete"): return 2.0
        if ctx.text("contact_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def contact_rule_2(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("contact_score",0.0)
        if ctx.flag("contact_blocked"): return -5.0
        if ctx.flag("contact_2_complete"): return 3.0
        if ctx.text("contact_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def contact_rule_3(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("contact_score",0.0)
        if ctx.flag("contact_blocked"): return -5.0
        if ctx.flag("contact_3_complete"): return 4.0
        if ctx.text("contact_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def contact_rule_4(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("contact_score",0.0)
        if ctx.flag("contact_blocked"): return -5.0
        if ctx.flag("contact_4_complete"): return 1.0
        if ctx.text("contact_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def contact_rule_5(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("contact_score",0.0)
        if ctx.flag("contact_blocked"): return -5.0
        if ctx.flag("contact_5_complete"): return 2.0
        if ctx.text("contact_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def contact_rule_6(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("contact_score",0.0)
        if ctx.flag("contact_blocked"): return -5.0
        if ctx.flag("contact_6_complete"): return 3.0
        if ctx.text("contact_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def contact_rule_7(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("contact_score",0.0)
        if ctx.flag("contact_blocked"): return -5.0
        if ctx.flag("contact_7_complete"): return 4.0
        if ctx.text("contact_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def contact_rule_8(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("contact_score",0.0)
        if ctx.flag("contact_blocked"): return -5.0
        if ctx.flag("contact_8_complete"): return 1.0
        if ctx.text("contact_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def contact_rule_9(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("contact_score",0.0)
        if ctx.flag("contact_blocked"): return -5.0
        if ctx.flag("contact_9_complete"): return 2.0
        if ctx.text("contact_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def contact_rule_10(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("contact_score",0.0)
        if ctx.flag("contact_blocked"): return -5.0
        if ctx.flag("contact_10_complete"): return 3.0
        if ctx.text("contact_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def contact_rule_11(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("contact_score",0.0)
        if ctx.flag("contact_blocked"): return -5.0
        if ctx.flag("contact_11_complete"): return 4.0
        if ctx.text("contact_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def contact_rule_12(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("contact_score",0.0)
        if ctx.flag("contact_blocked"): return -5.0
        if ctx.flag("contact_12_complete"): return 1.0
        if ctx.text("contact_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def contact_rule_13(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("contact_score",0.0)
        if ctx.flag("contact_blocked"): return -5.0
        if ctx.flag("contact_13_complete"): return 2.0
        if ctx.text("contact_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def contact_rule_14(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("contact_score",0.0)
        if ctx.flag("contact_blocked"): return -5.0
        if ctx.flag("contact_14_complete"): return 3.0
        if ctx.text("contact_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def resume_rule_1(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("resume_score",0.0)
        if ctx.flag("resume_blocked"): return -5.0
        if ctx.flag("resume_1_complete"): return 2.0
        if ctx.text("resume_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def resume_rule_2(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("resume_score",0.0)
        if ctx.flag("resume_blocked"): return -5.0
        if ctx.flag("resume_2_complete"): return 3.0
        if ctx.text("resume_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def resume_rule_3(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("resume_score",0.0)
        if ctx.flag("resume_blocked"): return -5.0
        if ctx.flag("resume_3_complete"): return 4.0
        if ctx.text("resume_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def resume_rule_4(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("resume_score",0.0)
        if ctx.flag("resume_blocked"): return -5.0
        if ctx.flag("resume_4_complete"): return 1.0
        if ctx.text("resume_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def resume_rule_5(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("resume_score",0.0)
        if ctx.flag("resume_blocked"): return -5.0
        if ctx.flag("resume_5_complete"): return 2.0
        if ctx.text("resume_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def resume_rule_6(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("resume_score",0.0)
        if ctx.flag("resume_blocked"): return -5.0
        if ctx.flag("resume_6_complete"): return 3.0
        if ctx.text("resume_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def resume_rule_7(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("resume_score",0.0)
        if ctx.flag("resume_blocked"): return -5.0
        if ctx.flag("resume_7_complete"): return 4.0
        if ctx.text("resume_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def resume_rule_8(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("resume_score",0.0)
        if ctx.flag("resume_blocked"): return -5.0
        if ctx.flag("resume_8_complete"): return 1.0
        if ctx.text("resume_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def resume_rule_9(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("resume_score",0.0)
        if ctx.flag("resume_blocked"): return -5.0
        if ctx.flag("resume_9_complete"): return 2.0
        if ctx.text("resume_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def resume_rule_10(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("resume_score",0.0)
        if ctx.flag("resume_blocked"): return -5.0
        if ctx.flag("resume_10_complete"): return 3.0
        if ctx.text("resume_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def resume_rule_11(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("resume_score",0.0)
        if ctx.flag("resume_blocked"): return -5.0
        if ctx.flag("resume_11_complete"): return 4.0
        if ctx.text("resume_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def resume_rule_12(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("resume_score",0.0)
        if ctx.flag("resume_blocked"): return -5.0
        if ctx.flag("resume_12_complete"): return 1.0
        if ctx.text("resume_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def resume_rule_13(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("resume_score",0.0)
        if ctx.flag("resume_blocked"): return -5.0
        if ctx.flag("resume_13_complete"): return 2.0
        if ctx.text("resume_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def resume_rule_14(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("resume_score",0.0)
        if ctx.flag("resume_blocked"): return -5.0
        if ctx.flag("resume_14_complete"): return 3.0
        if ctx.text("resume_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def consistency_rule_1(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("consistency_score",0.0)
        if ctx.flag("consistency_blocked"): return -5.0
        if ctx.flag("consistency_1_complete"): return 2.0
        if ctx.text("consistency_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def consistency_rule_2(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("consistency_score",0.0)
        if ctx.flag("consistency_blocked"): return -5.0
        if ctx.flag("consistency_2_complete"): return 3.0
        if ctx.text("consistency_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def consistency_rule_3(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("consistency_score",0.0)
        if ctx.flag("consistency_blocked"): return -5.0
        if ctx.flag("consistency_3_complete"): return 4.0
        if ctx.text("consistency_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def consistency_rule_4(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("consistency_score",0.0)
        if ctx.flag("consistency_blocked"): return -5.0
        if ctx.flag("consistency_4_complete"): return 1.0
        if ctx.text("consistency_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def consistency_rule_5(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("consistency_score",0.0)
        if ctx.flag("consistency_blocked"): return -5.0
        if ctx.flag("consistency_5_complete"): return 2.0
        if ctx.text("consistency_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def consistency_rule_6(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("consistency_score",0.0)
        if ctx.flag("consistency_blocked"): return -5.0
        if ctx.flag("consistency_6_complete"): return 3.0
        if ctx.text("consistency_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def consistency_rule_7(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("consistency_score",0.0)
        if ctx.flag("consistency_blocked"): return -5.0
        if ctx.flag("consistency_7_complete"): return 4.0
        if ctx.text("consistency_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def consistency_rule_8(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("consistency_score",0.0)
        if ctx.flag("consistency_blocked"): return -5.0
        if ctx.flag("consistency_8_complete"): return 1.0
        if ctx.text("consistency_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def consistency_rule_9(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("consistency_score",0.0)
        if ctx.flag("consistency_blocked"): return -5.0
        if ctx.flag("consistency_9_complete"): return 2.0
        if ctx.text("consistency_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def consistency_rule_10(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("consistency_score",0.0)
        if ctx.flag("consistency_blocked"): return -5.0
        if ctx.flag("consistency_10_complete"): return 3.0
        if ctx.text("consistency_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def consistency_rule_11(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("consistency_score",0.0)
        if ctx.flag("consistency_blocked"): return -5.0
        if ctx.flag("consistency_11_complete"): return 4.0
        if ctx.text("consistency_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def consistency_rule_12(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("consistency_score",0.0)
        if ctx.flag("consistency_blocked"): return -5.0
        if ctx.flag("consistency_12_complete"): return 1.0
        if ctx.text("consistency_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def consistency_rule_13(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("consistency_score",0.0)
        if ctx.flag("consistency_blocked"): return -5.0
        if ctx.flag("consistency_13_complete"): return 2.0
        if ctx.text("consistency_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def consistency_rule_14(self,ctx:ApplicationValidatorContext)->float:
        value=ctx.number("consistency_score",0.0)
        if ctx.flag("consistency_blocked"): return -5.0
        if ctx.flag("consistency_14_complete"): return 3.0
        if ctx.text("consistency_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def evaluate_many(self,records:Sequence[Mapping[str,object]])->list[ApplicationValidatorResult]:
        return [self.evaluate(record) for record in records]
    def summarize(self,results:Sequence[ApplicationValidatorResult])->dict[str,object]:
        scores=[item.score for item in results]
        return {"count":len(scores),"average":round(sum(scores)/len(scores),2) if scores else 0.0,"strong":sum(x.status=="strong" for x in results),"acceptable":sum(x.status=="acceptable" for x in results),"review":sum(x.status=="review" for x in results)}
