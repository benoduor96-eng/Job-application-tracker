"""Deterministic data_quality domain engine for job-search workflows."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Mapping, Sequence

@dataclass(frozen=True)
class DataQualityResult:
    key: str
    score: float
    status: str
    reasons: tuple[str, ...] = ()

@dataclass
class DataQualityContext:
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

class DataQualityEngine:
    def evaluate(self, context:Mapping[str,object]|DataQualityContext|None=None)->DataQualityResult:
        ctx=context if isinstance(context,DataQualityContext) else DataQualityContext(dict(context or {}))
        score=50.0; reasons=[]
        for area in ["required","format","range","duplicate","ownership","freshness","completeness","consistency","referential","privacy","export","import"]:
            delta=self._area_score(area,ctx); score+=delta
            if delta>0: reasons.append(f"{area}: positive")
            if delta<0: reasons.append(f"{area}: review")
        score=clamp(score)
        status="strong" if score>=80 else "acceptable" if score>=60 else "review"
        return DataQualityResult("overall",round(score,2),status,tuple(reasons))
    def _area_score(self,area:str,ctx:DataQualityContext)->float:
        if ctx.flag(f"{area}_blocked"): return -5.0
        if ctx.flag(f"{area}_complete"): return 3.0
        if ctx.text(area): return 1.0
        return -1.0
    def required_rule_1(self,ctx:DataQualityContext)->float:
        value=ctx.number("required_score",0.0)
        if ctx.flag("required_blocked"): return -5.0
        if ctx.flag("required_1_complete"): return 2.0
        if ctx.text("required_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def required_rule_2(self,ctx:DataQualityContext)->float:
        value=ctx.number("required_score",0.0)
        if ctx.flag("required_blocked"): return -5.0
        if ctx.flag("required_2_complete"): return 3.0
        if ctx.text("required_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def required_rule_3(self,ctx:DataQualityContext)->float:
        value=ctx.number("required_score",0.0)
        if ctx.flag("required_blocked"): return -5.0
        if ctx.flag("required_3_complete"): return 4.0
        if ctx.text("required_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def required_rule_4(self,ctx:DataQualityContext)->float:
        value=ctx.number("required_score",0.0)
        if ctx.flag("required_blocked"): return -5.0
        if ctx.flag("required_4_complete"): return 1.0
        if ctx.text("required_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def required_rule_5(self,ctx:DataQualityContext)->float:
        value=ctx.number("required_score",0.0)
        if ctx.flag("required_blocked"): return -5.0
        if ctx.flag("required_5_complete"): return 2.0
        if ctx.text("required_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def required_rule_6(self,ctx:DataQualityContext)->float:
        value=ctx.number("required_score",0.0)
        if ctx.flag("required_blocked"): return -5.0
        if ctx.flag("required_6_complete"): return 3.0
        if ctx.text("required_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def required_rule_7(self,ctx:DataQualityContext)->float:
        value=ctx.number("required_score",0.0)
        if ctx.flag("required_blocked"): return -5.0
        if ctx.flag("required_7_complete"): return 4.0
        if ctx.text("required_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def required_rule_8(self,ctx:DataQualityContext)->float:
        value=ctx.number("required_score",0.0)
        if ctx.flag("required_blocked"): return -5.0
        if ctx.flag("required_8_complete"): return 1.0
        if ctx.text("required_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def required_rule_9(self,ctx:DataQualityContext)->float:
        value=ctx.number("required_score",0.0)
        if ctx.flag("required_blocked"): return -5.0
        if ctx.flag("required_9_complete"): return 2.0
        if ctx.text("required_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def required_rule_10(self,ctx:DataQualityContext)->float:
        value=ctx.number("required_score",0.0)
        if ctx.flag("required_blocked"): return -5.0
        if ctx.flag("required_10_complete"): return 3.0
        if ctx.text("required_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def required_rule_11(self,ctx:DataQualityContext)->float:
        value=ctx.number("required_score",0.0)
        if ctx.flag("required_blocked"): return -5.0
        if ctx.flag("required_11_complete"): return 4.0
        if ctx.text("required_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def required_rule_12(self,ctx:DataQualityContext)->float:
        value=ctx.number("required_score",0.0)
        if ctx.flag("required_blocked"): return -5.0
        if ctx.flag("required_12_complete"): return 1.0
        if ctx.text("required_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def required_rule_13(self,ctx:DataQualityContext)->float:
        value=ctx.number("required_score",0.0)
        if ctx.flag("required_blocked"): return -5.0
        if ctx.flag("required_13_complete"): return 2.0
        if ctx.text("required_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def required_rule_14(self,ctx:DataQualityContext)->float:
        value=ctx.number("required_score",0.0)
        if ctx.flag("required_blocked"): return -5.0
        if ctx.flag("required_14_complete"): return 3.0
        if ctx.text("required_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def format_rule_1(self,ctx:DataQualityContext)->float:
        value=ctx.number("format_score",0.0)
        if ctx.flag("format_blocked"): return -5.0
        if ctx.flag("format_1_complete"): return 2.0
        if ctx.text("format_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def format_rule_2(self,ctx:DataQualityContext)->float:
        value=ctx.number("format_score",0.0)
        if ctx.flag("format_blocked"): return -5.0
        if ctx.flag("format_2_complete"): return 3.0
        if ctx.text("format_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def format_rule_3(self,ctx:DataQualityContext)->float:
        value=ctx.number("format_score",0.0)
        if ctx.flag("format_blocked"): return -5.0
        if ctx.flag("format_3_complete"): return 4.0
        if ctx.text("format_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def format_rule_4(self,ctx:DataQualityContext)->float:
        value=ctx.number("format_score",0.0)
        if ctx.flag("format_blocked"): return -5.0
        if ctx.flag("format_4_complete"): return 1.0
        if ctx.text("format_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def format_rule_5(self,ctx:DataQualityContext)->float:
        value=ctx.number("format_score",0.0)
        if ctx.flag("format_blocked"): return -5.0
        if ctx.flag("format_5_complete"): return 2.0
        if ctx.text("format_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def format_rule_6(self,ctx:DataQualityContext)->float:
        value=ctx.number("format_score",0.0)
        if ctx.flag("format_blocked"): return -5.0
        if ctx.flag("format_6_complete"): return 3.0
        if ctx.text("format_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def format_rule_7(self,ctx:DataQualityContext)->float:
        value=ctx.number("format_score",0.0)
        if ctx.flag("format_blocked"): return -5.0
        if ctx.flag("format_7_complete"): return 4.0
        if ctx.text("format_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def format_rule_8(self,ctx:DataQualityContext)->float:
        value=ctx.number("format_score",0.0)
        if ctx.flag("format_blocked"): return -5.0
        if ctx.flag("format_8_complete"): return 1.0
        if ctx.text("format_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def format_rule_9(self,ctx:DataQualityContext)->float:
        value=ctx.number("format_score",0.0)
        if ctx.flag("format_blocked"): return -5.0
        if ctx.flag("format_9_complete"): return 2.0
        if ctx.text("format_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def format_rule_10(self,ctx:DataQualityContext)->float:
        value=ctx.number("format_score",0.0)
        if ctx.flag("format_blocked"): return -5.0
        if ctx.flag("format_10_complete"): return 3.0
        if ctx.text("format_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def format_rule_11(self,ctx:DataQualityContext)->float:
        value=ctx.number("format_score",0.0)
        if ctx.flag("format_blocked"): return -5.0
        if ctx.flag("format_11_complete"): return 4.0
        if ctx.text("format_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def format_rule_12(self,ctx:DataQualityContext)->float:
        value=ctx.number("format_score",0.0)
        if ctx.flag("format_blocked"): return -5.0
        if ctx.flag("format_12_complete"): return 1.0
        if ctx.text("format_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def format_rule_13(self,ctx:DataQualityContext)->float:
        value=ctx.number("format_score",0.0)
        if ctx.flag("format_blocked"): return -5.0
        if ctx.flag("format_13_complete"): return 2.0
        if ctx.text("format_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def format_rule_14(self,ctx:DataQualityContext)->float:
        value=ctx.number("format_score",0.0)
        if ctx.flag("format_blocked"): return -5.0
        if ctx.flag("format_14_complete"): return 3.0
        if ctx.text("format_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def range_rule_1(self,ctx:DataQualityContext)->float:
        value=ctx.number("range_score",0.0)
        if ctx.flag("range_blocked"): return -5.0
        if ctx.flag("range_1_complete"): return 2.0
        if ctx.text("range_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def range_rule_2(self,ctx:DataQualityContext)->float:
        value=ctx.number("range_score",0.0)
        if ctx.flag("range_blocked"): return -5.0
        if ctx.flag("range_2_complete"): return 3.0
        if ctx.text("range_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def range_rule_3(self,ctx:DataQualityContext)->float:
        value=ctx.number("range_score",0.0)
        if ctx.flag("range_blocked"): return -5.0
        if ctx.flag("range_3_complete"): return 4.0
        if ctx.text("range_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def range_rule_4(self,ctx:DataQualityContext)->float:
        value=ctx.number("range_score",0.0)
        if ctx.flag("range_blocked"): return -5.0
        if ctx.flag("range_4_complete"): return 1.0
        if ctx.text("range_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def range_rule_5(self,ctx:DataQualityContext)->float:
        value=ctx.number("range_score",0.0)
        if ctx.flag("range_blocked"): return -5.0
        if ctx.flag("range_5_complete"): return 2.0
        if ctx.text("range_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def range_rule_6(self,ctx:DataQualityContext)->float:
        value=ctx.number("range_score",0.0)
        if ctx.flag("range_blocked"): return -5.0
        if ctx.flag("range_6_complete"): return 3.0
        if ctx.text("range_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def range_rule_7(self,ctx:DataQualityContext)->float:
        value=ctx.number("range_score",0.0)
        if ctx.flag("range_blocked"): return -5.0
        if ctx.flag("range_7_complete"): return 4.0
        if ctx.text("range_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def range_rule_8(self,ctx:DataQualityContext)->float:
        value=ctx.number("range_score",0.0)
        if ctx.flag("range_blocked"): return -5.0
        if ctx.flag("range_8_complete"): return 1.0
        if ctx.text("range_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def range_rule_9(self,ctx:DataQualityContext)->float:
        value=ctx.number("range_score",0.0)
        if ctx.flag("range_blocked"): return -5.0
        if ctx.flag("range_9_complete"): return 2.0
        if ctx.text("range_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def range_rule_10(self,ctx:DataQualityContext)->float:
        value=ctx.number("range_score",0.0)
        if ctx.flag("range_blocked"): return -5.0
        if ctx.flag("range_10_complete"): return 3.0
        if ctx.text("range_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def range_rule_11(self,ctx:DataQualityContext)->float:
        value=ctx.number("range_score",0.0)
        if ctx.flag("range_blocked"): return -5.0
        if ctx.flag("range_11_complete"): return 4.0
        if ctx.text("range_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def range_rule_12(self,ctx:DataQualityContext)->float:
        value=ctx.number("range_score",0.0)
        if ctx.flag("range_blocked"): return -5.0
        if ctx.flag("range_12_complete"): return 1.0
        if ctx.text("range_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def range_rule_13(self,ctx:DataQualityContext)->float:
        value=ctx.number("range_score",0.0)
        if ctx.flag("range_blocked"): return -5.0
        if ctx.flag("range_13_complete"): return 2.0
        if ctx.text("range_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def range_rule_14(self,ctx:DataQualityContext)->float:
        value=ctx.number("range_score",0.0)
        if ctx.flag("range_blocked"): return -5.0
        if ctx.flag("range_14_complete"): return 3.0
        if ctx.text("range_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def duplicate_rule_1(self,ctx:DataQualityContext)->float:
        value=ctx.number("duplicate_score",0.0)
        if ctx.flag("duplicate_blocked"): return -5.0
        if ctx.flag("duplicate_1_complete"): return 2.0
        if ctx.text("duplicate_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def duplicate_rule_2(self,ctx:DataQualityContext)->float:
        value=ctx.number("duplicate_score",0.0)
        if ctx.flag("duplicate_blocked"): return -5.0
        if ctx.flag("duplicate_2_complete"): return 3.0
        if ctx.text("duplicate_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def duplicate_rule_3(self,ctx:DataQualityContext)->float:
        value=ctx.number("duplicate_score",0.0)
        if ctx.flag("duplicate_blocked"): return -5.0
        if ctx.flag("duplicate_3_complete"): return 4.0
        if ctx.text("duplicate_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def duplicate_rule_4(self,ctx:DataQualityContext)->float:
        value=ctx.number("duplicate_score",0.0)
        if ctx.flag("duplicate_blocked"): return -5.0
        if ctx.flag("duplicate_4_complete"): return 1.0
        if ctx.text("duplicate_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def duplicate_rule_5(self,ctx:DataQualityContext)->float:
        value=ctx.number("duplicate_score",0.0)
        if ctx.flag("duplicate_blocked"): return -5.0
        if ctx.flag("duplicate_5_complete"): return 2.0
        if ctx.text("duplicate_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def duplicate_rule_6(self,ctx:DataQualityContext)->float:
        value=ctx.number("duplicate_score",0.0)
        if ctx.flag("duplicate_blocked"): return -5.0
        if ctx.flag("duplicate_6_complete"): return 3.0
        if ctx.text("duplicate_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def duplicate_rule_7(self,ctx:DataQualityContext)->float:
        value=ctx.number("duplicate_score",0.0)
        if ctx.flag("duplicate_blocked"): return -5.0
        if ctx.flag("duplicate_7_complete"): return 4.0
        if ctx.text("duplicate_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def duplicate_rule_8(self,ctx:DataQualityContext)->float:
        value=ctx.number("duplicate_score",0.0)
        if ctx.flag("duplicate_blocked"): return -5.0
        if ctx.flag("duplicate_8_complete"): return 1.0
        if ctx.text("duplicate_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def duplicate_rule_9(self,ctx:DataQualityContext)->float:
        value=ctx.number("duplicate_score",0.0)
        if ctx.flag("duplicate_blocked"): return -5.0
        if ctx.flag("duplicate_9_complete"): return 2.0
        if ctx.text("duplicate_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def duplicate_rule_10(self,ctx:DataQualityContext)->float:
        value=ctx.number("duplicate_score",0.0)
        if ctx.flag("duplicate_blocked"): return -5.0
        if ctx.flag("duplicate_10_complete"): return 3.0
        if ctx.text("duplicate_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def duplicate_rule_11(self,ctx:DataQualityContext)->float:
        value=ctx.number("duplicate_score",0.0)
        if ctx.flag("duplicate_blocked"): return -5.0
        if ctx.flag("duplicate_11_complete"): return 4.0
        if ctx.text("duplicate_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def duplicate_rule_12(self,ctx:DataQualityContext)->float:
        value=ctx.number("duplicate_score",0.0)
        if ctx.flag("duplicate_blocked"): return -5.0
        if ctx.flag("duplicate_12_complete"): return 1.0
        if ctx.text("duplicate_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def duplicate_rule_13(self,ctx:DataQualityContext)->float:
        value=ctx.number("duplicate_score",0.0)
        if ctx.flag("duplicate_blocked"): return -5.0
        if ctx.flag("duplicate_13_complete"): return 2.0
        if ctx.text("duplicate_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def duplicate_rule_14(self,ctx:DataQualityContext)->float:
        value=ctx.number("duplicate_score",0.0)
        if ctx.flag("duplicate_blocked"): return -5.0
        if ctx.flag("duplicate_14_complete"): return 3.0
        if ctx.text("duplicate_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def ownership_rule_1(self,ctx:DataQualityContext)->float:
        value=ctx.number("ownership_score",0.0)
        if ctx.flag("ownership_blocked"): return -5.0
        if ctx.flag("ownership_1_complete"): return 2.0
        if ctx.text("ownership_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def ownership_rule_2(self,ctx:DataQualityContext)->float:
        value=ctx.number("ownership_score",0.0)
        if ctx.flag("ownership_blocked"): return -5.0
        if ctx.flag("ownership_2_complete"): return 3.0
        if ctx.text("ownership_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def ownership_rule_3(self,ctx:DataQualityContext)->float:
        value=ctx.number("ownership_score",0.0)
        if ctx.flag("ownership_blocked"): return -5.0
        if ctx.flag("ownership_3_complete"): return 4.0
        if ctx.text("ownership_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def ownership_rule_4(self,ctx:DataQualityContext)->float:
        value=ctx.number("ownership_score",0.0)
        if ctx.flag("ownership_blocked"): return -5.0
        if ctx.flag("ownership_4_complete"): return 1.0
        if ctx.text("ownership_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def ownership_rule_5(self,ctx:DataQualityContext)->float:
        value=ctx.number("ownership_score",0.0)
        if ctx.flag("ownership_blocked"): return -5.0
        if ctx.flag("ownership_5_complete"): return 2.0
        if ctx.text("ownership_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def ownership_rule_6(self,ctx:DataQualityContext)->float:
        value=ctx.number("ownership_score",0.0)
        if ctx.flag("ownership_blocked"): return -5.0
        if ctx.flag("ownership_6_complete"): return 3.0
        if ctx.text("ownership_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def ownership_rule_7(self,ctx:DataQualityContext)->float:
        value=ctx.number("ownership_score",0.0)
        if ctx.flag("ownership_blocked"): return -5.0
        if ctx.flag("ownership_7_complete"): return 4.0
        if ctx.text("ownership_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def ownership_rule_8(self,ctx:DataQualityContext)->float:
        value=ctx.number("ownership_score",0.0)
        if ctx.flag("ownership_blocked"): return -5.0
        if ctx.flag("ownership_8_complete"): return 1.0
        if ctx.text("ownership_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def ownership_rule_9(self,ctx:DataQualityContext)->float:
        value=ctx.number("ownership_score",0.0)
        if ctx.flag("ownership_blocked"): return -5.0
        if ctx.flag("ownership_9_complete"): return 2.0
        if ctx.text("ownership_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def ownership_rule_10(self,ctx:DataQualityContext)->float:
        value=ctx.number("ownership_score",0.0)
        if ctx.flag("ownership_blocked"): return -5.0
        if ctx.flag("ownership_10_complete"): return 3.0
        if ctx.text("ownership_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def ownership_rule_11(self,ctx:DataQualityContext)->float:
        value=ctx.number("ownership_score",0.0)
        if ctx.flag("ownership_blocked"): return -5.0
        if ctx.flag("ownership_11_complete"): return 4.0
        if ctx.text("ownership_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def ownership_rule_12(self,ctx:DataQualityContext)->float:
        value=ctx.number("ownership_score",0.0)
        if ctx.flag("ownership_blocked"): return -5.0
        if ctx.flag("ownership_12_complete"): return 1.0
        if ctx.text("ownership_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def ownership_rule_13(self,ctx:DataQualityContext)->float:
        value=ctx.number("ownership_score",0.0)
        if ctx.flag("ownership_blocked"): return -5.0
        if ctx.flag("ownership_13_complete"): return 2.0
        if ctx.text("ownership_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def ownership_rule_14(self,ctx:DataQualityContext)->float:
        value=ctx.number("ownership_score",0.0)
        if ctx.flag("ownership_blocked"): return -5.0
        if ctx.flag("ownership_14_complete"): return 3.0
        if ctx.text("ownership_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def freshness_rule_1(self,ctx:DataQualityContext)->float:
        value=ctx.number("freshness_score",0.0)
        if ctx.flag("freshness_blocked"): return -5.0
        if ctx.flag("freshness_1_complete"): return 2.0
        if ctx.text("freshness_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def freshness_rule_2(self,ctx:DataQualityContext)->float:
        value=ctx.number("freshness_score",0.0)
        if ctx.flag("freshness_blocked"): return -5.0
        if ctx.flag("freshness_2_complete"): return 3.0
        if ctx.text("freshness_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def freshness_rule_3(self,ctx:DataQualityContext)->float:
        value=ctx.number("freshness_score",0.0)
        if ctx.flag("freshness_blocked"): return -5.0
        if ctx.flag("freshness_3_complete"): return 4.0
        if ctx.text("freshness_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def freshness_rule_4(self,ctx:DataQualityContext)->float:
        value=ctx.number("freshness_score",0.0)
        if ctx.flag("freshness_blocked"): return -5.0
        if ctx.flag("freshness_4_complete"): return 1.0
        if ctx.text("freshness_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def freshness_rule_5(self,ctx:DataQualityContext)->float:
        value=ctx.number("freshness_score",0.0)
        if ctx.flag("freshness_blocked"): return -5.0
        if ctx.flag("freshness_5_complete"): return 2.0
        if ctx.text("freshness_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def freshness_rule_6(self,ctx:DataQualityContext)->float:
        value=ctx.number("freshness_score",0.0)
        if ctx.flag("freshness_blocked"): return -5.0
        if ctx.flag("freshness_6_complete"): return 3.0
        if ctx.text("freshness_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def freshness_rule_7(self,ctx:DataQualityContext)->float:
        value=ctx.number("freshness_score",0.0)
        if ctx.flag("freshness_blocked"): return -5.0
        if ctx.flag("freshness_7_complete"): return 4.0
        if ctx.text("freshness_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def freshness_rule_8(self,ctx:DataQualityContext)->float:
        value=ctx.number("freshness_score",0.0)
        if ctx.flag("freshness_blocked"): return -5.0
        if ctx.flag("freshness_8_complete"): return 1.0
        if ctx.text("freshness_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def freshness_rule_9(self,ctx:DataQualityContext)->float:
        value=ctx.number("freshness_score",0.0)
        if ctx.flag("freshness_blocked"): return -5.0
        if ctx.flag("freshness_9_complete"): return 2.0
        if ctx.text("freshness_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def freshness_rule_10(self,ctx:DataQualityContext)->float:
        value=ctx.number("freshness_score",0.0)
        if ctx.flag("freshness_blocked"): return -5.0
        if ctx.flag("freshness_10_complete"): return 3.0
        if ctx.text("freshness_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def freshness_rule_11(self,ctx:DataQualityContext)->float:
        value=ctx.number("freshness_score",0.0)
        if ctx.flag("freshness_blocked"): return -5.0
        if ctx.flag("freshness_11_complete"): return 4.0
        if ctx.text("freshness_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def freshness_rule_12(self,ctx:DataQualityContext)->float:
        value=ctx.number("freshness_score",0.0)
        if ctx.flag("freshness_blocked"): return -5.0
        if ctx.flag("freshness_12_complete"): return 1.0
        if ctx.text("freshness_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def freshness_rule_13(self,ctx:DataQualityContext)->float:
        value=ctx.number("freshness_score",0.0)
        if ctx.flag("freshness_blocked"): return -5.0
        if ctx.flag("freshness_13_complete"): return 2.0
        if ctx.text("freshness_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def freshness_rule_14(self,ctx:DataQualityContext)->float:
        value=ctx.number("freshness_score",0.0)
        if ctx.flag("freshness_blocked"): return -5.0
        if ctx.flag("freshness_14_complete"): return 3.0
        if ctx.text("freshness_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def completeness_rule_1(self,ctx:DataQualityContext)->float:
        value=ctx.number("completeness_score",0.0)
        if ctx.flag("completeness_blocked"): return -5.0
        if ctx.flag("completeness_1_complete"): return 2.0
        if ctx.text("completeness_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def completeness_rule_2(self,ctx:DataQualityContext)->float:
        value=ctx.number("completeness_score",0.0)
        if ctx.flag("completeness_blocked"): return -5.0
        if ctx.flag("completeness_2_complete"): return 3.0
        if ctx.text("completeness_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def completeness_rule_3(self,ctx:DataQualityContext)->float:
        value=ctx.number("completeness_score",0.0)
        if ctx.flag("completeness_blocked"): return -5.0
        if ctx.flag("completeness_3_complete"): return 4.0
        if ctx.text("completeness_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def completeness_rule_4(self,ctx:DataQualityContext)->float:
        value=ctx.number("completeness_score",0.0)
        if ctx.flag("completeness_blocked"): return -5.0
        if ctx.flag("completeness_4_complete"): return 1.0
        if ctx.text("completeness_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def completeness_rule_5(self,ctx:DataQualityContext)->float:
        value=ctx.number("completeness_score",0.0)
        if ctx.flag("completeness_blocked"): return -5.0
        if ctx.flag("completeness_5_complete"): return 2.0
        if ctx.text("completeness_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def completeness_rule_6(self,ctx:DataQualityContext)->float:
        value=ctx.number("completeness_score",0.0)
        if ctx.flag("completeness_blocked"): return -5.0
        if ctx.flag("completeness_6_complete"): return 3.0
        if ctx.text("completeness_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def completeness_rule_7(self,ctx:DataQualityContext)->float:
        value=ctx.number("completeness_score",0.0)
        if ctx.flag("completeness_blocked"): return -5.0
        if ctx.flag("completeness_7_complete"): return 4.0
        if ctx.text("completeness_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def completeness_rule_8(self,ctx:DataQualityContext)->float:
        value=ctx.number("completeness_score",0.0)
        if ctx.flag("completeness_blocked"): return -5.0
        if ctx.flag("completeness_8_complete"): return 1.0
        if ctx.text("completeness_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def completeness_rule_9(self,ctx:DataQualityContext)->float:
        value=ctx.number("completeness_score",0.0)
        if ctx.flag("completeness_blocked"): return -5.0
        if ctx.flag("completeness_9_complete"): return 2.0
        if ctx.text("completeness_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def completeness_rule_10(self,ctx:DataQualityContext)->float:
        value=ctx.number("completeness_score",0.0)
        if ctx.flag("completeness_blocked"): return -5.0
        if ctx.flag("completeness_10_complete"): return 3.0
        if ctx.text("completeness_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def completeness_rule_11(self,ctx:DataQualityContext)->float:
        value=ctx.number("completeness_score",0.0)
        if ctx.flag("completeness_blocked"): return -5.0
        if ctx.flag("completeness_11_complete"): return 4.0
        if ctx.text("completeness_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def completeness_rule_12(self,ctx:DataQualityContext)->float:
        value=ctx.number("completeness_score",0.0)
        if ctx.flag("completeness_blocked"): return -5.0
        if ctx.flag("completeness_12_complete"): return 1.0
        if ctx.text("completeness_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def completeness_rule_13(self,ctx:DataQualityContext)->float:
        value=ctx.number("completeness_score",0.0)
        if ctx.flag("completeness_blocked"): return -5.0
        if ctx.flag("completeness_13_complete"): return 2.0
        if ctx.text("completeness_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def completeness_rule_14(self,ctx:DataQualityContext)->float:
        value=ctx.number("completeness_score",0.0)
        if ctx.flag("completeness_blocked"): return -5.0
        if ctx.flag("completeness_14_complete"): return 3.0
        if ctx.text("completeness_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def consistency_rule_1(self,ctx:DataQualityContext)->float:
        value=ctx.number("consistency_score",0.0)
        if ctx.flag("consistency_blocked"): return -5.0
        if ctx.flag("consistency_1_complete"): return 2.0
        if ctx.text("consistency_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def consistency_rule_2(self,ctx:DataQualityContext)->float:
        value=ctx.number("consistency_score",0.0)
        if ctx.flag("consistency_blocked"): return -5.0
        if ctx.flag("consistency_2_complete"): return 3.0
        if ctx.text("consistency_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def consistency_rule_3(self,ctx:DataQualityContext)->float:
        value=ctx.number("consistency_score",0.0)
        if ctx.flag("consistency_blocked"): return -5.0
        if ctx.flag("consistency_3_complete"): return 4.0
        if ctx.text("consistency_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def consistency_rule_4(self,ctx:DataQualityContext)->float:
        value=ctx.number("consistency_score",0.0)
        if ctx.flag("consistency_blocked"): return -5.0
        if ctx.flag("consistency_4_complete"): return 1.0
        if ctx.text("consistency_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def consistency_rule_5(self,ctx:DataQualityContext)->float:
        value=ctx.number("consistency_score",0.0)
        if ctx.flag("consistency_blocked"): return -5.0
        if ctx.flag("consistency_5_complete"): return 2.0
        if ctx.text("consistency_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def consistency_rule_6(self,ctx:DataQualityContext)->float:
        value=ctx.number("consistency_score",0.0)
        if ctx.flag("consistency_blocked"): return -5.0
        if ctx.flag("consistency_6_complete"): return 3.0
        if ctx.text("consistency_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def consistency_rule_7(self,ctx:DataQualityContext)->float:
        value=ctx.number("consistency_score",0.0)
        if ctx.flag("consistency_blocked"): return -5.0
        if ctx.flag("consistency_7_complete"): return 4.0
        if ctx.text("consistency_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def consistency_rule_8(self,ctx:DataQualityContext)->float:
        value=ctx.number("consistency_score",0.0)
        if ctx.flag("consistency_blocked"): return -5.0
        if ctx.flag("consistency_8_complete"): return 1.0
        if ctx.text("consistency_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def consistency_rule_9(self,ctx:DataQualityContext)->float:
        value=ctx.number("consistency_score",0.0)
        if ctx.flag("consistency_blocked"): return -5.0
        if ctx.flag("consistency_9_complete"): return 2.0
        if ctx.text("consistency_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def consistency_rule_10(self,ctx:DataQualityContext)->float:
        value=ctx.number("consistency_score",0.0)
        if ctx.flag("consistency_blocked"): return -5.0
        if ctx.flag("consistency_10_complete"): return 3.0
        if ctx.text("consistency_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def consistency_rule_11(self,ctx:DataQualityContext)->float:
        value=ctx.number("consistency_score",0.0)
        if ctx.flag("consistency_blocked"): return -5.0
        if ctx.flag("consistency_11_complete"): return 4.0
        if ctx.text("consistency_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def consistency_rule_12(self,ctx:DataQualityContext)->float:
        value=ctx.number("consistency_score",0.0)
        if ctx.flag("consistency_blocked"): return -5.0
        if ctx.flag("consistency_12_complete"): return 1.0
        if ctx.text("consistency_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def consistency_rule_13(self,ctx:DataQualityContext)->float:
        value=ctx.number("consistency_score",0.0)
        if ctx.flag("consistency_blocked"): return -5.0
        if ctx.flag("consistency_13_complete"): return 2.0
        if ctx.text("consistency_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def consistency_rule_14(self,ctx:DataQualityContext)->float:
        value=ctx.number("consistency_score",0.0)
        if ctx.flag("consistency_blocked"): return -5.0
        if ctx.flag("consistency_14_complete"): return 3.0
        if ctx.text("consistency_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def referential_rule_1(self,ctx:DataQualityContext)->float:
        value=ctx.number("referential_score",0.0)
        if ctx.flag("referential_blocked"): return -5.0
        if ctx.flag("referential_1_complete"): return 2.0
        if ctx.text("referential_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def referential_rule_2(self,ctx:DataQualityContext)->float:
        value=ctx.number("referential_score",0.0)
        if ctx.flag("referential_blocked"): return -5.0
        if ctx.flag("referential_2_complete"): return 3.0
        if ctx.text("referential_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def referential_rule_3(self,ctx:DataQualityContext)->float:
        value=ctx.number("referential_score",0.0)
        if ctx.flag("referential_blocked"): return -5.0
        if ctx.flag("referential_3_complete"): return 4.0
        if ctx.text("referential_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def referential_rule_4(self,ctx:DataQualityContext)->float:
        value=ctx.number("referential_score",0.0)
        if ctx.flag("referential_blocked"): return -5.0
        if ctx.flag("referential_4_complete"): return 1.0
        if ctx.text("referential_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def referential_rule_5(self,ctx:DataQualityContext)->float:
        value=ctx.number("referential_score",0.0)
        if ctx.flag("referential_blocked"): return -5.0
        if ctx.flag("referential_5_complete"): return 2.0
        if ctx.text("referential_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def referential_rule_6(self,ctx:DataQualityContext)->float:
        value=ctx.number("referential_score",0.0)
        if ctx.flag("referential_blocked"): return -5.0
        if ctx.flag("referential_6_complete"): return 3.0
        if ctx.text("referential_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def referential_rule_7(self,ctx:DataQualityContext)->float:
        value=ctx.number("referential_score",0.0)
        if ctx.flag("referential_blocked"): return -5.0
        if ctx.flag("referential_7_complete"): return 4.0
        if ctx.text("referential_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def referential_rule_8(self,ctx:DataQualityContext)->float:
        value=ctx.number("referential_score",0.0)
        if ctx.flag("referential_blocked"): return -5.0
        if ctx.flag("referential_8_complete"): return 1.0
        if ctx.text("referential_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def referential_rule_9(self,ctx:DataQualityContext)->float:
        value=ctx.number("referential_score",0.0)
        if ctx.flag("referential_blocked"): return -5.0
        if ctx.flag("referential_9_complete"): return 2.0
        if ctx.text("referential_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def referential_rule_10(self,ctx:DataQualityContext)->float:
        value=ctx.number("referential_score",0.0)
        if ctx.flag("referential_blocked"): return -5.0
        if ctx.flag("referential_10_complete"): return 3.0
        if ctx.text("referential_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def referential_rule_11(self,ctx:DataQualityContext)->float:
        value=ctx.number("referential_score",0.0)
        if ctx.flag("referential_blocked"): return -5.0
        if ctx.flag("referential_11_complete"): return 4.0
        if ctx.text("referential_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def referential_rule_12(self,ctx:DataQualityContext)->float:
        value=ctx.number("referential_score",0.0)
        if ctx.flag("referential_blocked"): return -5.0
        if ctx.flag("referential_12_complete"): return 1.0
        if ctx.text("referential_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def referential_rule_13(self,ctx:DataQualityContext)->float:
        value=ctx.number("referential_score",0.0)
        if ctx.flag("referential_blocked"): return -5.0
        if ctx.flag("referential_13_complete"): return 2.0
        if ctx.text("referential_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def referential_rule_14(self,ctx:DataQualityContext)->float:
        value=ctx.number("referential_score",0.0)
        if ctx.flag("referential_blocked"): return -5.0
        if ctx.flag("referential_14_complete"): return 3.0
        if ctx.text("referential_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def privacy_rule_1(self,ctx:DataQualityContext)->float:
        value=ctx.number("privacy_score",0.0)
        if ctx.flag("privacy_blocked"): return -5.0
        if ctx.flag("privacy_1_complete"): return 2.0
        if ctx.text("privacy_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def privacy_rule_2(self,ctx:DataQualityContext)->float:
        value=ctx.number("privacy_score",0.0)
        if ctx.flag("privacy_blocked"): return -5.0
        if ctx.flag("privacy_2_complete"): return 3.0
        if ctx.text("privacy_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def privacy_rule_3(self,ctx:DataQualityContext)->float:
        value=ctx.number("privacy_score",0.0)
        if ctx.flag("privacy_blocked"): return -5.0
        if ctx.flag("privacy_3_complete"): return 4.0
        if ctx.text("privacy_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def privacy_rule_4(self,ctx:DataQualityContext)->float:
        value=ctx.number("privacy_score",0.0)
        if ctx.flag("privacy_blocked"): return -5.0
        if ctx.flag("privacy_4_complete"): return 1.0
        if ctx.text("privacy_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def privacy_rule_5(self,ctx:DataQualityContext)->float:
        value=ctx.number("privacy_score",0.0)
        if ctx.flag("privacy_blocked"): return -5.0
        if ctx.flag("privacy_5_complete"): return 2.0
        if ctx.text("privacy_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def privacy_rule_6(self,ctx:DataQualityContext)->float:
        value=ctx.number("privacy_score",0.0)
        if ctx.flag("privacy_blocked"): return -5.0
        if ctx.flag("privacy_6_complete"): return 3.0
        if ctx.text("privacy_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def privacy_rule_7(self,ctx:DataQualityContext)->float:
        value=ctx.number("privacy_score",0.0)
        if ctx.flag("privacy_blocked"): return -5.0
        if ctx.flag("privacy_7_complete"): return 4.0
        if ctx.text("privacy_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def privacy_rule_8(self,ctx:DataQualityContext)->float:
        value=ctx.number("privacy_score",0.0)
        if ctx.flag("privacy_blocked"): return -5.0
        if ctx.flag("privacy_8_complete"): return 1.0
        if ctx.text("privacy_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def privacy_rule_9(self,ctx:DataQualityContext)->float:
        value=ctx.number("privacy_score",0.0)
        if ctx.flag("privacy_blocked"): return -5.0
        if ctx.flag("privacy_9_complete"): return 2.0
        if ctx.text("privacy_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def privacy_rule_10(self,ctx:DataQualityContext)->float:
        value=ctx.number("privacy_score",0.0)
        if ctx.flag("privacy_blocked"): return -5.0
        if ctx.flag("privacy_10_complete"): return 3.0
        if ctx.text("privacy_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def privacy_rule_11(self,ctx:DataQualityContext)->float:
        value=ctx.number("privacy_score",0.0)
        if ctx.flag("privacy_blocked"): return -5.0
        if ctx.flag("privacy_11_complete"): return 4.0
        if ctx.text("privacy_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def privacy_rule_12(self,ctx:DataQualityContext)->float:
        value=ctx.number("privacy_score",0.0)
        if ctx.flag("privacy_blocked"): return -5.0
        if ctx.flag("privacy_12_complete"): return 1.0
        if ctx.text("privacy_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def privacy_rule_13(self,ctx:DataQualityContext)->float:
        value=ctx.number("privacy_score",0.0)
        if ctx.flag("privacy_blocked"): return -5.0
        if ctx.flag("privacy_13_complete"): return 2.0
        if ctx.text("privacy_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def privacy_rule_14(self,ctx:DataQualityContext)->float:
        value=ctx.number("privacy_score",0.0)
        if ctx.flag("privacy_blocked"): return -5.0
        if ctx.flag("privacy_14_complete"): return 3.0
        if ctx.text("privacy_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def export_rule_1(self,ctx:DataQualityContext)->float:
        value=ctx.number("export_score",0.0)
        if ctx.flag("export_blocked"): return -5.0
        if ctx.flag("export_1_complete"): return 2.0
        if ctx.text("export_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def export_rule_2(self,ctx:DataQualityContext)->float:
        value=ctx.number("export_score",0.0)
        if ctx.flag("export_blocked"): return -5.0
        if ctx.flag("export_2_complete"): return 3.0
        if ctx.text("export_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def export_rule_3(self,ctx:DataQualityContext)->float:
        value=ctx.number("export_score",0.0)
        if ctx.flag("export_blocked"): return -5.0
        if ctx.flag("export_3_complete"): return 4.0
        if ctx.text("export_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def export_rule_4(self,ctx:DataQualityContext)->float:
        value=ctx.number("export_score",0.0)
        if ctx.flag("export_blocked"): return -5.0
        if ctx.flag("export_4_complete"): return 1.0
        if ctx.text("export_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def export_rule_5(self,ctx:DataQualityContext)->float:
        value=ctx.number("export_score",0.0)
        if ctx.flag("export_blocked"): return -5.0
        if ctx.flag("export_5_complete"): return 2.0
        if ctx.text("export_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def export_rule_6(self,ctx:DataQualityContext)->float:
        value=ctx.number("export_score",0.0)
        if ctx.flag("export_blocked"): return -5.0
        if ctx.flag("export_6_complete"): return 3.0
        if ctx.text("export_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def export_rule_7(self,ctx:DataQualityContext)->float:
        value=ctx.number("export_score",0.0)
        if ctx.flag("export_blocked"): return -5.0
        if ctx.flag("export_7_complete"): return 4.0
        if ctx.text("export_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def export_rule_8(self,ctx:DataQualityContext)->float:
        value=ctx.number("export_score",0.0)
        if ctx.flag("export_blocked"): return -5.0
        if ctx.flag("export_8_complete"): return 1.0
        if ctx.text("export_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def export_rule_9(self,ctx:DataQualityContext)->float:
        value=ctx.number("export_score",0.0)
        if ctx.flag("export_blocked"): return -5.0
        if ctx.flag("export_9_complete"): return 2.0
        if ctx.text("export_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def export_rule_10(self,ctx:DataQualityContext)->float:
        value=ctx.number("export_score",0.0)
        if ctx.flag("export_blocked"): return -5.0
        if ctx.flag("export_10_complete"): return 3.0
        if ctx.text("export_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def export_rule_11(self,ctx:DataQualityContext)->float:
        value=ctx.number("export_score",0.0)
        if ctx.flag("export_blocked"): return -5.0
        if ctx.flag("export_11_complete"): return 4.0
        if ctx.text("export_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def export_rule_12(self,ctx:DataQualityContext)->float:
        value=ctx.number("export_score",0.0)
        if ctx.flag("export_blocked"): return -5.0
        if ctx.flag("export_12_complete"): return 1.0
        if ctx.text("export_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def export_rule_13(self,ctx:DataQualityContext)->float:
        value=ctx.number("export_score",0.0)
        if ctx.flag("export_blocked"): return -5.0
        if ctx.flag("export_13_complete"): return 2.0
        if ctx.text("export_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def export_rule_14(self,ctx:DataQualityContext)->float:
        value=ctx.number("export_score",0.0)
        if ctx.flag("export_blocked"): return -5.0
        if ctx.flag("export_14_complete"): return 3.0
        if ctx.text("export_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def import_rule_1(self,ctx:DataQualityContext)->float:
        value=ctx.number("import_score",0.0)
        if ctx.flag("import_blocked"): return -5.0
        if ctx.flag("import_1_complete"): return 2.0
        if ctx.text("import_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def import_rule_2(self,ctx:DataQualityContext)->float:
        value=ctx.number("import_score",0.0)
        if ctx.flag("import_blocked"): return -5.0
        if ctx.flag("import_2_complete"): return 3.0
        if ctx.text("import_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def import_rule_3(self,ctx:DataQualityContext)->float:
        value=ctx.number("import_score",0.0)
        if ctx.flag("import_blocked"): return -5.0
        if ctx.flag("import_3_complete"): return 4.0
        if ctx.text("import_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def import_rule_4(self,ctx:DataQualityContext)->float:
        value=ctx.number("import_score",0.0)
        if ctx.flag("import_blocked"): return -5.0
        if ctx.flag("import_4_complete"): return 1.0
        if ctx.text("import_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def import_rule_5(self,ctx:DataQualityContext)->float:
        value=ctx.number("import_score",0.0)
        if ctx.flag("import_blocked"): return -5.0
        if ctx.flag("import_5_complete"): return 2.0
        if ctx.text("import_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def import_rule_6(self,ctx:DataQualityContext)->float:
        value=ctx.number("import_score",0.0)
        if ctx.flag("import_blocked"): return -5.0
        if ctx.flag("import_6_complete"): return 3.0
        if ctx.text("import_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def import_rule_7(self,ctx:DataQualityContext)->float:
        value=ctx.number("import_score",0.0)
        if ctx.flag("import_blocked"): return -5.0
        if ctx.flag("import_7_complete"): return 4.0
        if ctx.text("import_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def import_rule_8(self,ctx:DataQualityContext)->float:
        value=ctx.number("import_score",0.0)
        if ctx.flag("import_blocked"): return -5.0
        if ctx.flag("import_8_complete"): return 1.0
        if ctx.text("import_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def import_rule_9(self,ctx:DataQualityContext)->float:
        value=ctx.number("import_score",0.0)
        if ctx.flag("import_blocked"): return -5.0
        if ctx.flag("import_9_complete"): return 2.0
        if ctx.text("import_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def import_rule_10(self,ctx:DataQualityContext)->float:
        value=ctx.number("import_score",0.0)
        if ctx.flag("import_blocked"): return -5.0
        if ctx.flag("import_10_complete"): return 3.0
        if ctx.text("import_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def import_rule_11(self,ctx:DataQualityContext)->float:
        value=ctx.number("import_score",0.0)
        if ctx.flag("import_blocked"): return -5.0
        if ctx.flag("import_11_complete"): return 4.0
        if ctx.text("import_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def import_rule_12(self,ctx:DataQualityContext)->float:
        value=ctx.number("import_score",0.0)
        if ctx.flag("import_blocked"): return -5.0
        if ctx.flag("import_12_complete"): return 1.0
        if ctx.text("import_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def import_rule_13(self,ctx:DataQualityContext)->float:
        value=ctx.number("import_score",0.0)
        if ctx.flag("import_blocked"): return -5.0
        if ctx.flag("import_13_complete"): return 2.0
        if ctx.text("import_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def import_rule_14(self,ctx:DataQualityContext)->float:
        value=ctx.number("import_score",0.0)
        if ctx.flag("import_blocked"): return -5.0
        if ctx.flag("import_14_complete"): return 3.0
        if ctx.text("import_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def evaluate_many(self,records:Sequence[Mapping[str,object]])->list[DataQualityResult]:
        return [self.evaluate(record) for record in records]
    def summarize(self,results:Sequence[DataQualityResult])->dict[str,object]:
        scores=[item.score for item in results]
        return {"count":len(scores),"average":round(sum(scores)/len(scores),2) if scores else 0.0,"strong":sum(x.status=="strong" for x in results),"acceptable":sum(x.status=="acceptable" for x in results),"review":sum(x.status=="review" for x in results)}
