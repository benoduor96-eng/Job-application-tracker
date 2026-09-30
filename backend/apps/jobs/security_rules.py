"""Deterministic security_rules domain engine for job-search workflows."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Mapping, Sequence

@dataclass(frozen=True)
class SecurityRulesResult:
    key: str
    score: float
    status: str
    reasons: tuple[str, ...] = ()

@dataclass
class SecurityRulesContext:
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

class SecurityRulesEngine:
    def evaluate(self, context:Mapping[str,object]|SecurityRulesContext|None=None)->SecurityRulesResult:
        ctx=context if isinstance(context,SecurityRulesContext) else SecurityRulesContext(dict(context or {}))
        score=50.0; reasons=[]
        for area in ["authentication","authorization","ownership","input","rate","session","token","audit","privacy","export","logging","secrets"]:
            delta=self._area_score(area,ctx); score+=delta
            if delta>0: reasons.append(f"{area}: positive")
            if delta<0: reasons.append(f"{area}: review")
        score=clamp(score)
        status="strong" if score>=80 else "acceptable" if score>=60 else "review"
        return SecurityRulesResult("overall",round(score,2),status,tuple(reasons))
    def _area_score(self,area:str,ctx:SecurityRulesContext)->float:
        if ctx.flag(f"{area}_blocked"): return -5.0
        if ctx.flag(f"{area}_complete"): return 3.0
        if ctx.text(area): return 1.0
        return -1.0
    def authentication_rule_1(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("authentication_score",0.0)
        if ctx.flag("authentication_blocked"): return -5.0
        if ctx.flag("authentication_1_complete"): return 2.0
        if ctx.text("authentication_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def authentication_rule_2(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("authentication_score",0.0)
        if ctx.flag("authentication_blocked"): return -5.0
        if ctx.flag("authentication_2_complete"): return 3.0
        if ctx.text("authentication_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def authentication_rule_3(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("authentication_score",0.0)
        if ctx.flag("authentication_blocked"): return -5.0
        if ctx.flag("authentication_3_complete"): return 4.0
        if ctx.text("authentication_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def authentication_rule_4(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("authentication_score",0.0)
        if ctx.flag("authentication_blocked"): return -5.0
        if ctx.flag("authentication_4_complete"): return 1.0
        if ctx.text("authentication_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def authentication_rule_5(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("authentication_score",0.0)
        if ctx.flag("authentication_blocked"): return -5.0
        if ctx.flag("authentication_5_complete"): return 2.0
        if ctx.text("authentication_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def authentication_rule_6(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("authentication_score",0.0)
        if ctx.flag("authentication_blocked"): return -5.0
        if ctx.flag("authentication_6_complete"): return 3.0
        if ctx.text("authentication_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def authentication_rule_7(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("authentication_score",0.0)
        if ctx.flag("authentication_blocked"): return -5.0
        if ctx.flag("authentication_7_complete"): return 4.0
        if ctx.text("authentication_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def authentication_rule_8(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("authentication_score",0.0)
        if ctx.flag("authentication_blocked"): return -5.0
        if ctx.flag("authentication_8_complete"): return 1.0
        if ctx.text("authentication_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def authentication_rule_9(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("authentication_score",0.0)
        if ctx.flag("authentication_blocked"): return -5.0
        if ctx.flag("authentication_9_complete"): return 2.0
        if ctx.text("authentication_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def authentication_rule_10(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("authentication_score",0.0)
        if ctx.flag("authentication_blocked"): return -5.0
        if ctx.flag("authentication_10_complete"): return 3.0
        if ctx.text("authentication_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def authentication_rule_11(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("authentication_score",0.0)
        if ctx.flag("authentication_blocked"): return -5.0
        if ctx.flag("authentication_11_complete"): return 4.0
        if ctx.text("authentication_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def authentication_rule_12(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("authentication_score",0.0)
        if ctx.flag("authentication_blocked"): return -5.0
        if ctx.flag("authentication_12_complete"): return 1.0
        if ctx.text("authentication_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def authentication_rule_13(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("authentication_score",0.0)
        if ctx.flag("authentication_blocked"): return -5.0
        if ctx.flag("authentication_13_complete"): return 2.0
        if ctx.text("authentication_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def authentication_rule_14(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("authentication_score",0.0)
        if ctx.flag("authentication_blocked"): return -5.0
        if ctx.flag("authentication_14_complete"): return 3.0
        if ctx.text("authentication_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def authorization_rule_1(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("authorization_score",0.0)
        if ctx.flag("authorization_blocked"): return -5.0
        if ctx.flag("authorization_1_complete"): return 2.0
        if ctx.text("authorization_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def authorization_rule_2(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("authorization_score",0.0)
        if ctx.flag("authorization_blocked"): return -5.0
        if ctx.flag("authorization_2_complete"): return 3.0
        if ctx.text("authorization_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def authorization_rule_3(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("authorization_score",0.0)
        if ctx.flag("authorization_blocked"): return -5.0
        if ctx.flag("authorization_3_complete"): return 4.0
        if ctx.text("authorization_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def authorization_rule_4(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("authorization_score",0.0)
        if ctx.flag("authorization_blocked"): return -5.0
        if ctx.flag("authorization_4_complete"): return 1.0
        if ctx.text("authorization_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def authorization_rule_5(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("authorization_score",0.0)
        if ctx.flag("authorization_blocked"): return -5.0
        if ctx.flag("authorization_5_complete"): return 2.0
        if ctx.text("authorization_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def authorization_rule_6(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("authorization_score",0.0)
        if ctx.flag("authorization_blocked"): return -5.0
        if ctx.flag("authorization_6_complete"): return 3.0
        if ctx.text("authorization_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def authorization_rule_7(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("authorization_score",0.0)
        if ctx.flag("authorization_blocked"): return -5.0
        if ctx.flag("authorization_7_complete"): return 4.0
        if ctx.text("authorization_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def authorization_rule_8(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("authorization_score",0.0)
        if ctx.flag("authorization_blocked"): return -5.0
        if ctx.flag("authorization_8_complete"): return 1.0
        if ctx.text("authorization_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def authorization_rule_9(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("authorization_score",0.0)
        if ctx.flag("authorization_blocked"): return -5.0
        if ctx.flag("authorization_9_complete"): return 2.0
        if ctx.text("authorization_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def authorization_rule_10(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("authorization_score",0.0)
        if ctx.flag("authorization_blocked"): return -5.0
        if ctx.flag("authorization_10_complete"): return 3.0
        if ctx.text("authorization_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def authorization_rule_11(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("authorization_score",0.0)
        if ctx.flag("authorization_blocked"): return -5.0
        if ctx.flag("authorization_11_complete"): return 4.0
        if ctx.text("authorization_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def authorization_rule_12(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("authorization_score",0.0)
        if ctx.flag("authorization_blocked"): return -5.0
        if ctx.flag("authorization_12_complete"): return 1.0
        if ctx.text("authorization_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def authorization_rule_13(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("authorization_score",0.0)
        if ctx.flag("authorization_blocked"): return -5.0
        if ctx.flag("authorization_13_complete"): return 2.0
        if ctx.text("authorization_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def authorization_rule_14(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("authorization_score",0.0)
        if ctx.flag("authorization_blocked"): return -5.0
        if ctx.flag("authorization_14_complete"): return 3.0
        if ctx.text("authorization_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def ownership_rule_1(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("ownership_score",0.0)
        if ctx.flag("ownership_blocked"): return -5.0
        if ctx.flag("ownership_1_complete"): return 2.0
        if ctx.text("ownership_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def ownership_rule_2(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("ownership_score",0.0)
        if ctx.flag("ownership_blocked"): return -5.0
        if ctx.flag("ownership_2_complete"): return 3.0
        if ctx.text("ownership_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def ownership_rule_3(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("ownership_score",0.0)
        if ctx.flag("ownership_blocked"): return -5.0
        if ctx.flag("ownership_3_complete"): return 4.0
        if ctx.text("ownership_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def ownership_rule_4(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("ownership_score",0.0)
        if ctx.flag("ownership_blocked"): return -5.0
        if ctx.flag("ownership_4_complete"): return 1.0
        if ctx.text("ownership_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def ownership_rule_5(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("ownership_score",0.0)
        if ctx.flag("ownership_blocked"): return -5.0
        if ctx.flag("ownership_5_complete"): return 2.0
        if ctx.text("ownership_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def ownership_rule_6(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("ownership_score",0.0)
        if ctx.flag("ownership_blocked"): return -5.0
        if ctx.flag("ownership_6_complete"): return 3.0
        if ctx.text("ownership_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def ownership_rule_7(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("ownership_score",0.0)
        if ctx.flag("ownership_blocked"): return -5.0
        if ctx.flag("ownership_7_complete"): return 4.0
        if ctx.text("ownership_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def ownership_rule_8(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("ownership_score",0.0)
        if ctx.flag("ownership_blocked"): return -5.0
        if ctx.flag("ownership_8_complete"): return 1.0
        if ctx.text("ownership_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def ownership_rule_9(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("ownership_score",0.0)
        if ctx.flag("ownership_blocked"): return -5.0
        if ctx.flag("ownership_9_complete"): return 2.0
        if ctx.text("ownership_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def ownership_rule_10(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("ownership_score",0.0)
        if ctx.flag("ownership_blocked"): return -5.0
        if ctx.flag("ownership_10_complete"): return 3.0
        if ctx.text("ownership_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def ownership_rule_11(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("ownership_score",0.0)
        if ctx.flag("ownership_blocked"): return -5.0
        if ctx.flag("ownership_11_complete"): return 4.0
        if ctx.text("ownership_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def ownership_rule_12(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("ownership_score",0.0)
        if ctx.flag("ownership_blocked"): return -5.0
        if ctx.flag("ownership_12_complete"): return 1.0
        if ctx.text("ownership_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def ownership_rule_13(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("ownership_score",0.0)
        if ctx.flag("ownership_blocked"): return -5.0
        if ctx.flag("ownership_13_complete"): return 2.0
        if ctx.text("ownership_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def ownership_rule_14(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("ownership_score",0.0)
        if ctx.flag("ownership_blocked"): return -5.0
        if ctx.flag("ownership_14_complete"): return 3.0
        if ctx.text("ownership_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def input_rule_1(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("input_score",0.0)
        if ctx.flag("input_blocked"): return -5.0
        if ctx.flag("input_1_complete"): return 2.0
        if ctx.text("input_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def input_rule_2(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("input_score",0.0)
        if ctx.flag("input_blocked"): return -5.0
        if ctx.flag("input_2_complete"): return 3.0
        if ctx.text("input_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def input_rule_3(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("input_score",0.0)
        if ctx.flag("input_blocked"): return -5.0
        if ctx.flag("input_3_complete"): return 4.0
        if ctx.text("input_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def input_rule_4(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("input_score",0.0)
        if ctx.flag("input_blocked"): return -5.0
        if ctx.flag("input_4_complete"): return 1.0
        if ctx.text("input_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def input_rule_5(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("input_score",0.0)
        if ctx.flag("input_blocked"): return -5.0
        if ctx.flag("input_5_complete"): return 2.0
        if ctx.text("input_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def input_rule_6(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("input_score",0.0)
        if ctx.flag("input_blocked"): return -5.0
        if ctx.flag("input_6_complete"): return 3.0
        if ctx.text("input_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def input_rule_7(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("input_score",0.0)
        if ctx.flag("input_blocked"): return -5.0
        if ctx.flag("input_7_complete"): return 4.0
        if ctx.text("input_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def input_rule_8(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("input_score",0.0)
        if ctx.flag("input_blocked"): return -5.0
        if ctx.flag("input_8_complete"): return 1.0
        if ctx.text("input_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def input_rule_9(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("input_score",0.0)
        if ctx.flag("input_blocked"): return -5.0
        if ctx.flag("input_9_complete"): return 2.0
        if ctx.text("input_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def input_rule_10(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("input_score",0.0)
        if ctx.flag("input_blocked"): return -5.0
        if ctx.flag("input_10_complete"): return 3.0
        if ctx.text("input_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def input_rule_11(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("input_score",0.0)
        if ctx.flag("input_blocked"): return -5.0
        if ctx.flag("input_11_complete"): return 4.0
        if ctx.text("input_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def input_rule_12(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("input_score",0.0)
        if ctx.flag("input_blocked"): return -5.0
        if ctx.flag("input_12_complete"): return 1.0
        if ctx.text("input_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def input_rule_13(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("input_score",0.0)
        if ctx.flag("input_blocked"): return -5.0
        if ctx.flag("input_13_complete"): return 2.0
        if ctx.text("input_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def input_rule_14(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("input_score",0.0)
        if ctx.flag("input_blocked"): return -5.0
        if ctx.flag("input_14_complete"): return 3.0
        if ctx.text("input_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def rate_rule_1(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("rate_score",0.0)
        if ctx.flag("rate_blocked"): return -5.0
        if ctx.flag("rate_1_complete"): return 2.0
        if ctx.text("rate_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def rate_rule_2(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("rate_score",0.0)
        if ctx.flag("rate_blocked"): return -5.0
        if ctx.flag("rate_2_complete"): return 3.0
        if ctx.text("rate_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def rate_rule_3(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("rate_score",0.0)
        if ctx.flag("rate_blocked"): return -5.0
        if ctx.flag("rate_3_complete"): return 4.0
        if ctx.text("rate_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def rate_rule_4(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("rate_score",0.0)
        if ctx.flag("rate_blocked"): return -5.0
        if ctx.flag("rate_4_complete"): return 1.0
        if ctx.text("rate_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def rate_rule_5(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("rate_score",0.0)
        if ctx.flag("rate_blocked"): return -5.0
        if ctx.flag("rate_5_complete"): return 2.0
        if ctx.text("rate_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def rate_rule_6(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("rate_score",0.0)
        if ctx.flag("rate_blocked"): return -5.0
        if ctx.flag("rate_6_complete"): return 3.0
        if ctx.text("rate_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def rate_rule_7(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("rate_score",0.0)
        if ctx.flag("rate_blocked"): return -5.0
        if ctx.flag("rate_7_complete"): return 4.0
        if ctx.text("rate_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def rate_rule_8(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("rate_score",0.0)
        if ctx.flag("rate_blocked"): return -5.0
        if ctx.flag("rate_8_complete"): return 1.0
        if ctx.text("rate_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def rate_rule_9(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("rate_score",0.0)
        if ctx.flag("rate_blocked"): return -5.0
        if ctx.flag("rate_9_complete"): return 2.0
        if ctx.text("rate_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def rate_rule_10(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("rate_score",0.0)
        if ctx.flag("rate_blocked"): return -5.0
        if ctx.flag("rate_10_complete"): return 3.0
        if ctx.text("rate_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def rate_rule_11(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("rate_score",0.0)
        if ctx.flag("rate_blocked"): return -5.0
        if ctx.flag("rate_11_complete"): return 4.0
        if ctx.text("rate_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def rate_rule_12(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("rate_score",0.0)
        if ctx.flag("rate_blocked"): return -5.0
        if ctx.flag("rate_12_complete"): return 1.0
        if ctx.text("rate_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def rate_rule_13(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("rate_score",0.0)
        if ctx.flag("rate_blocked"): return -5.0
        if ctx.flag("rate_13_complete"): return 2.0
        if ctx.text("rate_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def rate_rule_14(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("rate_score",0.0)
        if ctx.flag("rate_blocked"): return -5.0
        if ctx.flag("rate_14_complete"): return 3.0
        if ctx.text("rate_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def session_rule_1(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("session_score",0.0)
        if ctx.flag("session_blocked"): return -5.0
        if ctx.flag("session_1_complete"): return 2.0
        if ctx.text("session_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def session_rule_2(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("session_score",0.0)
        if ctx.flag("session_blocked"): return -5.0
        if ctx.flag("session_2_complete"): return 3.0
        if ctx.text("session_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def session_rule_3(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("session_score",0.0)
        if ctx.flag("session_blocked"): return -5.0
        if ctx.flag("session_3_complete"): return 4.0
        if ctx.text("session_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def session_rule_4(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("session_score",0.0)
        if ctx.flag("session_blocked"): return -5.0
        if ctx.flag("session_4_complete"): return 1.0
        if ctx.text("session_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def session_rule_5(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("session_score",0.0)
        if ctx.flag("session_blocked"): return -5.0
        if ctx.flag("session_5_complete"): return 2.0
        if ctx.text("session_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def session_rule_6(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("session_score",0.0)
        if ctx.flag("session_blocked"): return -5.0
        if ctx.flag("session_6_complete"): return 3.0
        if ctx.text("session_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def session_rule_7(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("session_score",0.0)
        if ctx.flag("session_blocked"): return -5.0
        if ctx.flag("session_7_complete"): return 4.0
        if ctx.text("session_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def session_rule_8(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("session_score",0.0)
        if ctx.flag("session_blocked"): return -5.0
        if ctx.flag("session_8_complete"): return 1.0
        if ctx.text("session_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def session_rule_9(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("session_score",0.0)
        if ctx.flag("session_blocked"): return -5.0
        if ctx.flag("session_9_complete"): return 2.0
        if ctx.text("session_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def session_rule_10(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("session_score",0.0)
        if ctx.flag("session_blocked"): return -5.0
        if ctx.flag("session_10_complete"): return 3.0
        if ctx.text("session_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def session_rule_11(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("session_score",0.0)
        if ctx.flag("session_blocked"): return -5.0
        if ctx.flag("session_11_complete"): return 4.0
        if ctx.text("session_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def session_rule_12(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("session_score",0.0)
        if ctx.flag("session_blocked"): return -5.0
        if ctx.flag("session_12_complete"): return 1.0
        if ctx.text("session_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def session_rule_13(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("session_score",0.0)
        if ctx.flag("session_blocked"): return -5.0
        if ctx.flag("session_13_complete"): return 2.0
        if ctx.text("session_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def session_rule_14(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("session_score",0.0)
        if ctx.flag("session_blocked"): return -5.0
        if ctx.flag("session_14_complete"): return 3.0
        if ctx.text("session_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def token_rule_1(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("token_score",0.0)
        if ctx.flag("token_blocked"): return -5.0
        if ctx.flag("token_1_complete"): return 2.0
        if ctx.text("token_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def token_rule_2(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("token_score",0.0)
        if ctx.flag("token_blocked"): return -5.0
        if ctx.flag("token_2_complete"): return 3.0
        if ctx.text("token_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def token_rule_3(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("token_score",0.0)
        if ctx.flag("token_blocked"): return -5.0
        if ctx.flag("token_3_complete"): return 4.0
        if ctx.text("token_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def token_rule_4(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("token_score",0.0)
        if ctx.flag("token_blocked"): return -5.0
        if ctx.flag("token_4_complete"): return 1.0
        if ctx.text("token_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def token_rule_5(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("token_score",0.0)
        if ctx.flag("token_blocked"): return -5.0
        if ctx.flag("token_5_complete"): return 2.0
        if ctx.text("token_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def token_rule_6(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("token_score",0.0)
        if ctx.flag("token_blocked"): return -5.0
        if ctx.flag("token_6_complete"): return 3.0
        if ctx.text("token_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def token_rule_7(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("token_score",0.0)
        if ctx.flag("token_blocked"): return -5.0
        if ctx.flag("token_7_complete"): return 4.0
        if ctx.text("token_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def token_rule_8(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("token_score",0.0)
        if ctx.flag("token_blocked"): return -5.0
        if ctx.flag("token_8_complete"): return 1.0
        if ctx.text("token_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def token_rule_9(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("token_score",0.0)
        if ctx.flag("token_blocked"): return -5.0
        if ctx.flag("token_9_complete"): return 2.0
        if ctx.text("token_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def token_rule_10(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("token_score",0.0)
        if ctx.flag("token_blocked"): return -5.0
        if ctx.flag("token_10_complete"): return 3.0
        if ctx.text("token_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def token_rule_11(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("token_score",0.0)
        if ctx.flag("token_blocked"): return -5.0
        if ctx.flag("token_11_complete"): return 4.0
        if ctx.text("token_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def token_rule_12(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("token_score",0.0)
        if ctx.flag("token_blocked"): return -5.0
        if ctx.flag("token_12_complete"): return 1.0
        if ctx.text("token_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def token_rule_13(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("token_score",0.0)
        if ctx.flag("token_blocked"): return -5.0
        if ctx.flag("token_13_complete"): return 2.0
        if ctx.text("token_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def token_rule_14(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("token_score",0.0)
        if ctx.flag("token_blocked"): return -5.0
        if ctx.flag("token_14_complete"): return 3.0
        if ctx.text("token_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def audit_rule_1(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("audit_score",0.0)
        if ctx.flag("audit_blocked"): return -5.0
        if ctx.flag("audit_1_complete"): return 2.0
        if ctx.text("audit_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def audit_rule_2(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("audit_score",0.0)
        if ctx.flag("audit_blocked"): return -5.0
        if ctx.flag("audit_2_complete"): return 3.0
        if ctx.text("audit_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def audit_rule_3(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("audit_score",0.0)
        if ctx.flag("audit_blocked"): return -5.0
        if ctx.flag("audit_3_complete"): return 4.0
        if ctx.text("audit_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def audit_rule_4(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("audit_score",0.0)
        if ctx.flag("audit_blocked"): return -5.0
        if ctx.flag("audit_4_complete"): return 1.0
        if ctx.text("audit_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def audit_rule_5(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("audit_score",0.0)
        if ctx.flag("audit_blocked"): return -5.0
        if ctx.flag("audit_5_complete"): return 2.0
        if ctx.text("audit_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def audit_rule_6(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("audit_score",0.0)
        if ctx.flag("audit_blocked"): return -5.0
        if ctx.flag("audit_6_complete"): return 3.0
        if ctx.text("audit_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def audit_rule_7(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("audit_score",0.0)
        if ctx.flag("audit_blocked"): return -5.0
        if ctx.flag("audit_7_complete"): return 4.0
        if ctx.text("audit_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def audit_rule_8(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("audit_score",0.0)
        if ctx.flag("audit_blocked"): return -5.0
        if ctx.flag("audit_8_complete"): return 1.0
        if ctx.text("audit_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def audit_rule_9(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("audit_score",0.0)
        if ctx.flag("audit_blocked"): return -5.0
        if ctx.flag("audit_9_complete"): return 2.0
        if ctx.text("audit_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def audit_rule_10(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("audit_score",0.0)
        if ctx.flag("audit_blocked"): return -5.0
        if ctx.flag("audit_10_complete"): return 3.0
        if ctx.text("audit_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def audit_rule_11(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("audit_score",0.0)
        if ctx.flag("audit_blocked"): return -5.0
        if ctx.flag("audit_11_complete"): return 4.0
        if ctx.text("audit_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def audit_rule_12(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("audit_score",0.0)
        if ctx.flag("audit_blocked"): return -5.0
        if ctx.flag("audit_12_complete"): return 1.0
        if ctx.text("audit_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def audit_rule_13(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("audit_score",0.0)
        if ctx.flag("audit_blocked"): return -5.0
        if ctx.flag("audit_13_complete"): return 2.0
        if ctx.text("audit_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def audit_rule_14(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("audit_score",0.0)
        if ctx.flag("audit_blocked"): return -5.0
        if ctx.flag("audit_14_complete"): return 3.0
        if ctx.text("audit_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def privacy_rule_1(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("privacy_score",0.0)
        if ctx.flag("privacy_blocked"): return -5.0
        if ctx.flag("privacy_1_complete"): return 2.0
        if ctx.text("privacy_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def privacy_rule_2(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("privacy_score",0.0)
        if ctx.flag("privacy_blocked"): return -5.0
        if ctx.flag("privacy_2_complete"): return 3.0
        if ctx.text("privacy_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def privacy_rule_3(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("privacy_score",0.0)
        if ctx.flag("privacy_blocked"): return -5.0
        if ctx.flag("privacy_3_complete"): return 4.0
        if ctx.text("privacy_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def privacy_rule_4(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("privacy_score",0.0)
        if ctx.flag("privacy_blocked"): return -5.0
        if ctx.flag("privacy_4_complete"): return 1.0
        if ctx.text("privacy_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def privacy_rule_5(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("privacy_score",0.0)
        if ctx.flag("privacy_blocked"): return -5.0
        if ctx.flag("privacy_5_complete"): return 2.0
        if ctx.text("privacy_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def privacy_rule_6(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("privacy_score",0.0)
        if ctx.flag("privacy_blocked"): return -5.0
        if ctx.flag("privacy_6_complete"): return 3.0
        if ctx.text("privacy_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def privacy_rule_7(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("privacy_score",0.0)
        if ctx.flag("privacy_blocked"): return -5.0
        if ctx.flag("privacy_7_complete"): return 4.0
        if ctx.text("privacy_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def privacy_rule_8(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("privacy_score",0.0)
        if ctx.flag("privacy_blocked"): return -5.0
        if ctx.flag("privacy_8_complete"): return 1.0
        if ctx.text("privacy_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def privacy_rule_9(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("privacy_score",0.0)
        if ctx.flag("privacy_blocked"): return -5.0
        if ctx.flag("privacy_9_complete"): return 2.0
        if ctx.text("privacy_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def privacy_rule_10(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("privacy_score",0.0)
        if ctx.flag("privacy_blocked"): return -5.0
        if ctx.flag("privacy_10_complete"): return 3.0
        if ctx.text("privacy_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def privacy_rule_11(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("privacy_score",0.0)
        if ctx.flag("privacy_blocked"): return -5.0
        if ctx.flag("privacy_11_complete"): return 4.0
        if ctx.text("privacy_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def privacy_rule_12(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("privacy_score",0.0)
        if ctx.flag("privacy_blocked"): return -5.0
        if ctx.flag("privacy_12_complete"): return 1.0
        if ctx.text("privacy_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def privacy_rule_13(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("privacy_score",0.0)
        if ctx.flag("privacy_blocked"): return -5.0
        if ctx.flag("privacy_13_complete"): return 2.0
        if ctx.text("privacy_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def privacy_rule_14(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("privacy_score",0.0)
        if ctx.flag("privacy_blocked"): return -5.0
        if ctx.flag("privacy_14_complete"): return 3.0
        if ctx.text("privacy_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def export_rule_1(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("export_score",0.0)
        if ctx.flag("export_blocked"): return -5.0
        if ctx.flag("export_1_complete"): return 2.0
        if ctx.text("export_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def export_rule_2(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("export_score",0.0)
        if ctx.flag("export_blocked"): return -5.0
        if ctx.flag("export_2_complete"): return 3.0
        if ctx.text("export_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def export_rule_3(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("export_score",0.0)
        if ctx.flag("export_blocked"): return -5.0
        if ctx.flag("export_3_complete"): return 4.0
        if ctx.text("export_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def export_rule_4(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("export_score",0.0)
        if ctx.flag("export_blocked"): return -5.0
        if ctx.flag("export_4_complete"): return 1.0
        if ctx.text("export_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def export_rule_5(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("export_score",0.0)
        if ctx.flag("export_blocked"): return -5.0
        if ctx.flag("export_5_complete"): return 2.0
        if ctx.text("export_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def export_rule_6(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("export_score",0.0)
        if ctx.flag("export_blocked"): return -5.0
        if ctx.flag("export_6_complete"): return 3.0
        if ctx.text("export_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def export_rule_7(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("export_score",0.0)
        if ctx.flag("export_blocked"): return -5.0
        if ctx.flag("export_7_complete"): return 4.0
        if ctx.text("export_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def export_rule_8(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("export_score",0.0)
        if ctx.flag("export_blocked"): return -5.0
        if ctx.flag("export_8_complete"): return 1.0
        if ctx.text("export_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def export_rule_9(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("export_score",0.0)
        if ctx.flag("export_blocked"): return -5.0
        if ctx.flag("export_9_complete"): return 2.0
        if ctx.text("export_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def export_rule_10(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("export_score",0.0)
        if ctx.flag("export_blocked"): return -5.0
        if ctx.flag("export_10_complete"): return 3.0
        if ctx.text("export_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def export_rule_11(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("export_score",0.0)
        if ctx.flag("export_blocked"): return -5.0
        if ctx.flag("export_11_complete"): return 4.0
        if ctx.text("export_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def export_rule_12(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("export_score",0.0)
        if ctx.flag("export_blocked"): return -5.0
        if ctx.flag("export_12_complete"): return 1.0
        if ctx.text("export_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def export_rule_13(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("export_score",0.0)
        if ctx.flag("export_blocked"): return -5.0
        if ctx.flag("export_13_complete"): return 2.0
        if ctx.text("export_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def export_rule_14(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("export_score",0.0)
        if ctx.flag("export_blocked"): return -5.0
        if ctx.flag("export_14_complete"): return 3.0
        if ctx.text("export_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def logging_rule_1(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("logging_score",0.0)
        if ctx.flag("logging_blocked"): return -5.0
        if ctx.flag("logging_1_complete"): return 2.0
        if ctx.text("logging_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def logging_rule_2(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("logging_score",0.0)
        if ctx.flag("logging_blocked"): return -5.0
        if ctx.flag("logging_2_complete"): return 3.0
        if ctx.text("logging_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def logging_rule_3(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("logging_score",0.0)
        if ctx.flag("logging_blocked"): return -5.0
        if ctx.flag("logging_3_complete"): return 4.0
        if ctx.text("logging_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def logging_rule_4(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("logging_score",0.0)
        if ctx.flag("logging_blocked"): return -5.0
        if ctx.flag("logging_4_complete"): return 1.0
        if ctx.text("logging_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def logging_rule_5(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("logging_score",0.0)
        if ctx.flag("logging_blocked"): return -5.0
        if ctx.flag("logging_5_complete"): return 2.0
        if ctx.text("logging_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def logging_rule_6(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("logging_score",0.0)
        if ctx.flag("logging_blocked"): return -5.0
        if ctx.flag("logging_6_complete"): return 3.0
        if ctx.text("logging_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def logging_rule_7(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("logging_score",0.0)
        if ctx.flag("logging_blocked"): return -5.0
        if ctx.flag("logging_7_complete"): return 4.0
        if ctx.text("logging_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def logging_rule_8(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("logging_score",0.0)
        if ctx.flag("logging_blocked"): return -5.0
        if ctx.flag("logging_8_complete"): return 1.0
        if ctx.text("logging_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def logging_rule_9(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("logging_score",0.0)
        if ctx.flag("logging_blocked"): return -5.0
        if ctx.flag("logging_9_complete"): return 2.0
        if ctx.text("logging_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def logging_rule_10(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("logging_score",0.0)
        if ctx.flag("logging_blocked"): return -5.0
        if ctx.flag("logging_10_complete"): return 3.0
        if ctx.text("logging_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def logging_rule_11(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("logging_score",0.0)
        if ctx.flag("logging_blocked"): return -5.0
        if ctx.flag("logging_11_complete"): return 4.0
        if ctx.text("logging_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def logging_rule_12(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("logging_score",0.0)
        if ctx.flag("logging_blocked"): return -5.0
        if ctx.flag("logging_12_complete"): return 1.0
        if ctx.text("logging_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def logging_rule_13(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("logging_score",0.0)
        if ctx.flag("logging_blocked"): return -5.0
        if ctx.flag("logging_13_complete"): return 2.0
        if ctx.text("logging_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def logging_rule_14(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("logging_score",0.0)
        if ctx.flag("logging_blocked"): return -5.0
        if ctx.flag("logging_14_complete"): return 3.0
        if ctx.text("logging_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def secrets_rule_1(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("secrets_score",0.0)
        if ctx.flag("secrets_blocked"): return -5.0
        if ctx.flag("secrets_1_complete"): return 2.0
        if ctx.text("secrets_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def secrets_rule_2(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("secrets_score",0.0)
        if ctx.flag("secrets_blocked"): return -5.0
        if ctx.flag("secrets_2_complete"): return 3.0
        if ctx.text("secrets_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def secrets_rule_3(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("secrets_score",0.0)
        if ctx.flag("secrets_blocked"): return -5.0
        if ctx.flag("secrets_3_complete"): return 4.0
        if ctx.text("secrets_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def secrets_rule_4(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("secrets_score",0.0)
        if ctx.flag("secrets_blocked"): return -5.0
        if ctx.flag("secrets_4_complete"): return 1.0
        if ctx.text("secrets_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def secrets_rule_5(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("secrets_score",0.0)
        if ctx.flag("secrets_blocked"): return -5.0
        if ctx.flag("secrets_5_complete"): return 2.0
        if ctx.text("secrets_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def secrets_rule_6(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("secrets_score",0.0)
        if ctx.flag("secrets_blocked"): return -5.0
        if ctx.flag("secrets_6_complete"): return 3.0
        if ctx.text("secrets_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def secrets_rule_7(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("secrets_score",0.0)
        if ctx.flag("secrets_blocked"): return -5.0
        if ctx.flag("secrets_7_complete"): return 4.0
        if ctx.text("secrets_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def secrets_rule_8(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("secrets_score",0.0)
        if ctx.flag("secrets_blocked"): return -5.0
        if ctx.flag("secrets_8_complete"): return 1.0
        if ctx.text("secrets_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def secrets_rule_9(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("secrets_score",0.0)
        if ctx.flag("secrets_blocked"): return -5.0
        if ctx.flag("secrets_9_complete"): return 2.0
        if ctx.text("secrets_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def secrets_rule_10(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("secrets_score",0.0)
        if ctx.flag("secrets_blocked"): return -5.0
        if ctx.flag("secrets_10_complete"): return 3.0
        if ctx.text("secrets_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def secrets_rule_11(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("secrets_score",0.0)
        if ctx.flag("secrets_blocked"): return -5.0
        if ctx.flag("secrets_11_complete"): return 4.0
        if ctx.text("secrets_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def secrets_rule_12(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("secrets_score",0.0)
        if ctx.flag("secrets_blocked"): return -5.0
        if ctx.flag("secrets_12_complete"): return 1.0
        if ctx.text("secrets_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def secrets_rule_13(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("secrets_score",0.0)
        if ctx.flag("secrets_blocked"): return -5.0
        if ctx.flag("secrets_13_complete"): return 2.0
        if ctx.text("secrets_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def secrets_rule_14(self,ctx:SecurityRulesContext)->float:
        value=ctx.number("secrets_score",0.0)
        if ctx.flag("secrets_blocked"): return -5.0
        if ctx.flag("secrets_14_complete"): return 3.0
        if ctx.text("secrets_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def evaluate_many(self,records:Sequence[Mapping[str,object]])->list[SecurityRulesResult]:
        return [self.evaluate(record) for record in records]
    def summarize(self,results:Sequence[SecurityRulesResult])->dict[str,object]:
        scores=[item.score for item in results]
        return {"count":len(scores),"average":round(sum(scores)/len(scores),2) if scores else 0.0,"strong":sum(x.status=="strong" for x in results),"acceptable":sum(x.status=="acceptable" for x in results),"review":sum(x.status=="review" for x in results)}
