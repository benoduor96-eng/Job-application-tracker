"""Deterministic export_pipeline domain engine for job-search workflows."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Mapping, Sequence

@dataclass(frozen=True)
class ExportPipelineResult:
    key: str
    score: float
    status: str
    reasons: tuple[str, ...] = ()

@dataclass
class ExportPipelineContext:
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

class ExportPipelineEngine:
    def evaluate(self, context:Mapping[str,object]|ExportPipelineContext|None=None)->ExportPipelineResult:
        ctx=context if isinstance(context,ExportPipelineContext) else ExportPipelineContext(dict(context or {}))
        score=50.0; reasons=[]
        for area in ["csv","json","summary","applications","contacts","tasks","interviews","resumes","activities","analytics","redaction","archive"]:
            delta=self._area_score(area,ctx); score+=delta
            if delta>0: reasons.append(f"{area}: positive")
            if delta<0: reasons.append(f"{area}: review")
        score=clamp(score)
        status="strong" if score>=80 else "acceptable" if score>=60 else "review"
        return ExportPipelineResult("overall",round(score,2),status,tuple(reasons))
    def _area_score(self,area:str,ctx:ExportPipelineContext)->float:
        if ctx.flag(f"{area}_blocked"): return -5.0
        if ctx.flag(f"{area}_complete"): return 3.0
        if ctx.text(area): return 1.0
        return -1.0
    def csv_rule_1(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("csv_score",0.0)
        if ctx.flag("csv_blocked"): return -5.0
        if ctx.flag("csv_1_complete"): return 2.0
        if ctx.text("csv_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def csv_rule_2(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("csv_score",0.0)
        if ctx.flag("csv_blocked"): return -5.0
        if ctx.flag("csv_2_complete"): return 3.0
        if ctx.text("csv_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def csv_rule_3(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("csv_score",0.0)
        if ctx.flag("csv_blocked"): return -5.0
        if ctx.flag("csv_3_complete"): return 4.0
        if ctx.text("csv_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def csv_rule_4(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("csv_score",0.0)
        if ctx.flag("csv_blocked"): return -5.0
        if ctx.flag("csv_4_complete"): return 1.0
        if ctx.text("csv_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def csv_rule_5(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("csv_score",0.0)
        if ctx.flag("csv_blocked"): return -5.0
        if ctx.flag("csv_5_complete"): return 2.0
        if ctx.text("csv_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def csv_rule_6(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("csv_score",0.0)
        if ctx.flag("csv_blocked"): return -5.0
        if ctx.flag("csv_6_complete"): return 3.0
        if ctx.text("csv_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def csv_rule_7(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("csv_score",0.0)
        if ctx.flag("csv_blocked"): return -5.0
        if ctx.flag("csv_7_complete"): return 4.0
        if ctx.text("csv_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def csv_rule_8(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("csv_score",0.0)
        if ctx.flag("csv_blocked"): return -5.0
        if ctx.flag("csv_8_complete"): return 1.0
        if ctx.text("csv_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def csv_rule_9(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("csv_score",0.0)
        if ctx.flag("csv_blocked"): return -5.0
        if ctx.flag("csv_9_complete"): return 2.0
        if ctx.text("csv_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def csv_rule_10(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("csv_score",0.0)
        if ctx.flag("csv_blocked"): return -5.0
        if ctx.flag("csv_10_complete"): return 3.0
        if ctx.text("csv_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def csv_rule_11(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("csv_score",0.0)
        if ctx.flag("csv_blocked"): return -5.0
        if ctx.flag("csv_11_complete"): return 4.0
        if ctx.text("csv_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def csv_rule_12(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("csv_score",0.0)
        if ctx.flag("csv_blocked"): return -5.0
        if ctx.flag("csv_12_complete"): return 1.0
        if ctx.text("csv_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def csv_rule_13(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("csv_score",0.0)
        if ctx.flag("csv_blocked"): return -5.0
        if ctx.flag("csv_13_complete"): return 2.0
        if ctx.text("csv_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def csv_rule_14(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("csv_score",0.0)
        if ctx.flag("csv_blocked"): return -5.0
        if ctx.flag("csv_14_complete"): return 3.0
        if ctx.text("csv_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def json_rule_1(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("json_score",0.0)
        if ctx.flag("json_blocked"): return -5.0
        if ctx.flag("json_1_complete"): return 2.0
        if ctx.text("json_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def json_rule_2(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("json_score",0.0)
        if ctx.flag("json_blocked"): return -5.0
        if ctx.flag("json_2_complete"): return 3.0
        if ctx.text("json_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def json_rule_3(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("json_score",0.0)
        if ctx.flag("json_blocked"): return -5.0
        if ctx.flag("json_3_complete"): return 4.0
        if ctx.text("json_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def json_rule_4(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("json_score",0.0)
        if ctx.flag("json_blocked"): return -5.0
        if ctx.flag("json_4_complete"): return 1.0
        if ctx.text("json_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def json_rule_5(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("json_score",0.0)
        if ctx.flag("json_blocked"): return -5.0
        if ctx.flag("json_5_complete"): return 2.0
        if ctx.text("json_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def json_rule_6(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("json_score",0.0)
        if ctx.flag("json_blocked"): return -5.0
        if ctx.flag("json_6_complete"): return 3.0
        if ctx.text("json_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def json_rule_7(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("json_score",0.0)
        if ctx.flag("json_blocked"): return -5.0
        if ctx.flag("json_7_complete"): return 4.0
        if ctx.text("json_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def json_rule_8(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("json_score",0.0)
        if ctx.flag("json_blocked"): return -5.0
        if ctx.flag("json_8_complete"): return 1.0
        if ctx.text("json_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def json_rule_9(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("json_score",0.0)
        if ctx.flag("json_blocked"): return -5.0
        if ctx.flag("json_9_complete"): return 2.0
        if ctx.text("json_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def json_rule_10(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("json_score",0.0)
        if ctx.flag("json_blocked"): return -5.0
        if ctx.flag("json_10_complete"): return 3.0
        if ctx.text("json_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def json_rule_11(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("json_score",0.0)
        if ctx.flag("json_blocked"): return -5.0
        if ctx.flag("json_11_complete"): return 4.0
        if ctx.text("json_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def json_rule_12(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("json_score",0.0)
        if ctx.flag("json_blocked"): return -5.0
        if ctx.flag("json_12_complete"): return 1.0
        if ctx.text("json_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def json_rule_13(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("json_score",0.0)
        if ctx.flag("json_blocked"): return -5.0
        if ctx.flag("json_13_complete"): return 2.0
        if ctx.text("json_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def json_rule_14(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("json_score",0.0)
        if ctx.flag("json_blocked"): return -5.0
        if ctx.flag("json_14_complete"): return 3.0
        if ctx.text("json_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def summary_rule_1(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("summary_score",0.0)
        if ctx.flag("summary_blocked"): return -5.0
        if ctx.flag("summary_1_complete"): return 2.0
        if ctx.text("summary_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def summary_rule_2(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("summary_score",0.0)
        if ctx.flag("summary_blocked"): return -5.0
        if ctx.flag("summary_2_complete"): return 3.0
        if ctx.text("summary_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def summary_rule_3(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("summary_score",0.0)
        if ctx.flag("summary_blocked"): return -5.0
        if ctx.flag("summary_3_complete"): return 4.0
        if ctx.text("summary_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def summary_rule_4(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("summary_score",0.0)
        if ctx.flag("summary_blocked"): return -5.0
        if ctx.flag("summary_4_complete"): return 1.0
        if ctx.text("summary_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def summary_rule_5(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("summary_score",0.0)
        if ctx.flag("summary_blocked"): return -5.0
        if ctx.flag("summary_5_complete"): return 2.0
        if ctx.text("summary_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def summary_rule_6(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("summary_score",0.0)
        if ctx.flag("summary_blocked"): return -5.0
        if ctx.flag("summary_6_complete"): return 3.0
        if ctx.text("summary_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def summary_rule_7(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("summary_score",0.0)
        if ctx.flag("summary_blocked"): return -5.0
        if ctx.flag("summary_7_complete"): return 4.0
        if ctx.text("summary_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def summary_rule_8(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("summary_score",0.0)
        if ctx.flag("summary_blocked"): return -5.0
        if ctx.flag("summary_8_complete"): return 1.0
        if ctx.text("summary_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def summary_rule_9(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("summary_score",0.0)
        if ctx.flag("summary_blocked"): return -5.0
        if ctx.flag("summary_9_complete"): return 2.0
        if ctx.text("summary_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def summary_rule_10(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("summary_score",0.0)
        if ctx.flag("summary_blocked"): return -5.0
        if ctx.flag("summary_10_complete"): return 3.0
        if ctx.text("summary_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def summary_rule_11(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("summary_score",0.0)
        if ctx.flag("summary_blocked"): return -5.0
        if ctx.flag("summary_11_complete"): return 4.0
        if ctx.text("summary_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def summary_rule_12(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("summary_score",0.0)
        if ctx.flag("summary_blocked"): return -5.0
        if ctx.flag("summary_12_complete"): return 1.0
        if ctx.text("summary_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def summary_rule_13(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("summary_score",0.0)
        if ctx.flag("summary_blocked"): return -5.0
        if ctx.flag("summary_13_complete"): return 2.0
        if ctx.text("summary_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def summary_rule_14(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("summary_score",0.0)
        if ctx.flag("summary_blocked"): return -5.0
        if ctx.flag("summary_14_complete"): return 3.0
        if ctx.text("summary_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def applications_rule_1(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("applications_score",0.0)
        if ctx.flag("applications_blocked"): return -5.0
        if ctx.flag("applications_1_complete"): return 2.0
        if ctx.text("applications_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def applications_rule_2(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("applications_score",0.0)
        if ctx.flag("applications_blocked"): return -5.0
        if ctx.flag("applications_2_complete"): return 3.0
        if ctx.text("applications_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def applications_rule_3(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("applications_score",0.0)
        if ctx.flag("applications_blocked"): return -5.0
        if ctx.flag("applications_3_complete"): return 4.0
        if ctx.text("applications_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def applications_rule_4(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("applications_score",0.0)
        if ctx.flag("applications_blocked"): return -5.0
        if ctx.flag("applications_4_complete"): return 1.0
        if ctx.text("applications_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def applications_rule_5(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("applications_score",0.0)
        if ctx.flag("applications_blocked"): return -5.0
        if ctx.flag("applications_5_complete"): return 2.0
        if ctx.text("applications_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def applications_rule_6(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("applications_score",0.0)
        if ctx.flag("applications_blocked"): return -5.0
        if ctx.flag("applications_6_complete"): return 3.0
        if ctx.text("applications_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def applications_rule_7(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("applications_score",0.0)
        if ctx.flag("applications_blocked"): return -5.0
        if ctx.flag("applications_7_complete"): return 4.0
        if ctx.text("applications_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def applications_rule_8(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("applications_score",0.0)
        if ctx.flag("applications_blocked"): return -5.0
        if ctx.flag("applications_8_complete"): return 1.0
        if ctx.text("applications_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def applications_rule_9(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("applications_score",0.0)
        if ctx.flag("applications_blocked"): return -5.0
        if ctx.flag("applications_9_complete"): return 2.0
        if ctx.text("applications_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def applications_rule_10(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("applications_score",0.0)
        if ctx.flag("applications_blocked"): return -5.0
        if ctx.flag("applications_10_complete"): return 3.0
        if ctx.text("applications_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def applications_rule_11(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("applications_score",0.0)
        if ctx.flag("applications_blocked"): return -5.0
        if ctx.flag("applications_11_complete"): return 4.0
        if ctx.text("applications_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def applications_rule_12(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("applications_score",0.0)
        if ctx.flag("applications_blocked"): return -5.0
        if ctx.flag("applications_12_complete"): return 1.0
        if ctx.text("applications_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def applications_rule_13(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("applications_score",0.0)
        if ctx.flag("applications_blocked"): return -5.0
        if ctx.flag("applications_13_complete"): return 2.0
        if ctx.text("applications_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def applications_rule_14(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("applications_score",0.0)
        if ctx.flag("applications_blocked"): return -5.0
        if ctx.flag("applications_14_complete"): return 3.0
        if ctx.text("applications_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def contacts_rule_1(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("contacts_score",0.0)
        if ctx.flag("contacts_blocked"): return -5.0
        if ctx.flag("contacts_1_complete"): return 2.0
        if ctx.text("contacts_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def contacts_rule_2(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("contacts_score",0.0)
        if ctx.flag("contacts_blocked"): return -5.0
        if ctx.flag("contacts_2_complete"): return 3.0
        if ctx.text("contacts_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def contacts_rule_3(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("contacts_score",0.0)
        if ctx.flag("contacts_blocked"): return -5.0
        if ctx.flag("contacts_3_complete"): return 4.0
        if ctx.text("contacts_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def contacts_rule_4(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("contacts_score",0.0)
        if ctx.flag("contacts_blocked"): return -5.0
        if ctx.flag("contacts_4_complete"): return 1.0
        if ctx.text("contacts_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def contacts_rule_5(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("contacts_score",0.0)
        if ctx.flag("contacts_blocked"): return -5.0
        if ctx.flag("contacts_5_complete"): return 2.0
        if ctx.text("contacts_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def contacts_rule_6(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("contacts_score",0.0)
        if ctx.flag("contacts_blocked"): return -5.0
        if ctx.flag("contacts_6_complete"): return 3.0
        if ctx.text("contacts_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def contacts_rule_7(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("contacts_score",0.0)
        if ctx.flag("contacts_blocked"): return -5.0
        if ctx.flag("contacts_7_complete"): return 4.0
        if ctx.text("contacts_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def contacts_rule_8(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("contacts_score",0.0)
        if ctx.flag("contacts_blocked"): return -5.0
        if ctx.flag("contacts_8_complete"): return 1.0
        if ctx.text("contacts_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def contacts_rule_9(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("contacts_score",0.0)
        if ctx.flag("contacts_blocked"): return -5.0
        if ctx.flag("contacts_9_complete"): return 2.0
        if ctx.text("contacts_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def contacts_rule_10(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("contacts_score",0.0)
        if ctx.flag("contacts_blocked"): return -5.0
        if ctx.flag("contacts_10_complete"): return 3.0
        if ctx.text("contacts_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def contacts_rule_11(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("contacts_score",0.0)
        if ctx.flag("contacts_blocked"): return -5.0
        if ctx.flag("contacts_11_complete"): return 4.0
        if ctx.text("contacts_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def contacts_rule_12(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("contacts_score",0.0)
        if ctx.flag("contacts_blocked"): return -5.0
        if ctx.flag("contacts_12_complete"): return 1.0
        if ctx.text("contacts_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def contacts_rule_13(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("contacts_score",0.0)
        if ctx.flag("contacts_blocked"): return -5.0
        if ctx.flag("contacts_13_complete"): return 2.0
        if ctx.text("contacts_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def contacts_rule_14(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("contacts_score",0.0)
        if ctx.flag("contacts_blocked"): return -5.0
        if ctx.flag("contacts_14_complete"): return 3.0
        if ctx.text("contacts_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def tasks_rule_1(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("tasks_score",0.0)
        if ctx.flag("tasks_blocked"): return -5.0
        if ctx.flag("tasks_1_complete"): return 2.0
        if ctx.text("tasks_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def tasks_rule_2(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("tasks_score",0.0)
        if ctx.flag("tasks_blocked"): return -5.0
        if ctx.flag("tasks_2_complete"): return 3.0
        if ctx.text("tasks_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def tasks_rule_3(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("tasks_score",0.0)
        if ctx.flag("tasks_blocked"): return -5.0
        if ctx.flag("tasks_3_complete"): return 4.0
        if ctx.text("tasks_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def tasks_rule_4(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("tasks_score",0.0)
        if ctx.flag("tasks_blocked"): return -5.0
        if ctx.flag("tasks_4_complete"): return 1.0
        if ctx.text("tasks_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def tasks_rule_5(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("tasks_score",0.0)
        if ctx.flag("tasks_blocked"): return -5.0
        if ctx.flag("tasks_5_complete"): return 2.0
        if ctx.text("tasks_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def tasks_rule_6(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("tasks_score",0.0)
        if ctx.flag("tasks_blocked"): return -5.0
        if ctx.flag("tasks_6_complete"): return 3.0
        if ctx.text("tasks_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def tasks_rule_7(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("tasks_score",0.0)
        if ctx.flag("tasks_blocked"): return -5.0
        if ctx.flag("tasks_7_complete"): return 4.0
        if ctx.text("tasks_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def tasks_rule_8(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("tasks_score",0.0)
        if ctx.flag("tasks_blocked"): return -5.0
        if ctx.flag("tasks_8_complete"): return 1.0
        if ctx.text("tasks_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def tasks_rule_9(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("tasks_score",0.0)
        if ctx.flag("tasks_blocked"): return -5.0
        if ctx.flag("tasks_9_complete"): return 2.0
        if ctx.text("tasks_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def tasks_rule_10(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("tasks_score",0.0)
        if ctx.flag("tasks_blocked"): return -5.0
        if ctx.flag("tasks_10_complete"): return 3.0
        if ctx.text("tasks_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def tasks_rule_11(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("tasks_score",0.0)
        if ctx.flag("tasks_blocked"): return -5.0
        if ctx.flag("tasks_11_complete"): return 4.0
        if ctx.text("tasks_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def tasks_rule_12(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("tasks_score",0.0)
        if ctx.flag("tasks_blocked"): return -5.0
        if ctx.flag("tasks_12_complete"): return 1.0
        if ctx.text("tasks_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def tasks_rule_13(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("tasks_score",0.0)
        if ctx.flag("tasks_blocked"): return -5.0
        if ctx.flag("tasks_13_complete"): return 2.0
        if ctx.text("tasks_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def tasks_rule_14(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("tasks_score",0.0)
        if ctx.flag("tasks_blocked"): return -5.0
        if ctx.flag("tasks_14_complete"): return 3.0
        if ctx.text("tasks_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def interviews_rule_1(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("interviews_score",0.0)
        if ctx.flag("interviews_blocked"): return -5.0
        if ctx.flag("interviews_1_complete"): return 2.0
        if ctx.text("interviews_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def interviews_rule_2(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("interviews_score",0.0)
        if ctx.flag("interviews_blocked"): return -5.0
        if ctx.flag("interviews_2_complete"): return 3.0
        if ctx.text("interviews_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def interviews_rule_3(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("interviews_score",0.0)
        if ctx.flag("interviews_blocked"): return -5.0
        if ctx.flag("interviews_3_complete"): return 4.0
        if ctx.text("interviews_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def interviews_rule_4(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("interviews_score",0.0)
        if ctx.flag("interviews_blocked"): return -5.0
        if ctx.flag("interviews_4_complete"): return 1.0
        if ctx.text("interviews_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def interviews_rule_5(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("interviews_score",0.0)
        if ctx.flag("interviews_blocked"): return -5.0
        if ctx.flag("interviews_5_complete"): return 2.0
        if ctx.text("interviews_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def interviews_rule_6(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("interviews_score",0.0)
        if ctx.flag("interviews_blocked"): return -5.0
        if ctx.flag("interviews_6_complete"): return 3.0
        if ctx.text("interviews_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def interviews_rule_7(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("interviews_score",0.0)
        if ctx.flag("interviews_blocked"): return -5.0
        if ctx.flag("interviews_7_complete"): return 4.0
        if ctx.text("interviews_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def interviews_rule_8(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("interviews_score",0.0)
        if ctx.flag("interviews_blocked"): return -5.0
        if ctx.flag("interviews_8_complete"): return 1.0
        if ctx.text("interviews_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def interviews_rule_9(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("interviews_score",0.0)
        if ctx.flag("interviews_blocked"): return -5.0
        if ctx.flag("interviews_9_complete"): return 2.0
        if ctx.text("interviews_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def interviews_rule_10(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("interviews_score",0.0)
        if ctx.flag("interviews_blocked"): return -5.0
        if ctx.flag("interviews_10_complete"): return 3.0
        if ctx.text("interviews_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def interviews_rule_11(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("interviews_score",0.0)
        if ctx.flag("interviews_blocked"): return -5.0
        if ctx.flag("interviews_11_complete"): return 4.0
        if ctx.text("interviews_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def interviews_rule_12(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("interviews_score",0.0)
        if ctx.flag("interviews_blocked"): return -5.0
        if ctx.flag("interviews_12_complete"): return 1.0
        if ctx.text("interviews_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def interviews_rule_13(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("interviews_score",0.0)
        if ctx.flag("interviews_blocked"): return -5.0
        if ctx.flag("interviews_13_complete"): return 2.0
        if ctx.text("interviews_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def interviews_rule_14(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("interviews_score",0.0)
        if ctx.flag("interviews_blocked"): return -5.0
        if ctx.flag("interviews_14_complete"): return 3.0
        if ctx.text("interviews_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def resumes_rule_1(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("resumes_score",0.0)
        if ctx.flag("resumes_blocked"): return -5.0
        if ctx.flag("resumes_1_complete"): return 2.0
        if ctx.text("resumes_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def resumes_rule_2(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("resumes_score",0.0)
        if ctx.flag("resumes_blocked"): return -5.0
        if ctx.flag("resumes_2_complete"): return 3.0
        if ctx.text("resumes_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def resumes_rule_3(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("resumes_score",0.0)
        if ctx.flag("resumes_blocked"): return -5.0
        if ctx.flag("resumes_3_complete"): return 4.0
        if ctx.text("resumes_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def resumes_rule_4(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("resumes_score",0.0)
        if ctx.flag("resumes_blocked"): return -5.0
        if ctx.flag("resumes_4_complete"): return 1.0
        if ctx.text("resumes_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def resumes_rule_5(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("resumes_score",0.0)
        if ctx.flag("resumes_blocked"): return -5.0
        if ctx.flag("resumes_5_complete"): return 2.0
        if ctx.text("resumes_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def resumes_rule_6(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("resumes_score",0.0)
        if ctx.flag("resumes_blocked"): return -5.0
        if ctx.flag("resumes_6_complete"): return 3.0
        if ctx.text("resumes_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def resumes_rule_7(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("resumes_score",0.0)
        if ctx.flag("resumes_blocked"): return -5.0
        if ctx.flag("resumes_7_complete"): return 4.0
        if ctx.text("resumes_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def resumes_rule_8(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("resumes_score",0.0)
        if ctx.flag("resumes_blocked"): return -5.0
        if ctx.flag("resumes_8_complete"): return 1.0
        if ctx.text("resumes_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def resumes_rule_9(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("resumes_score",0.0)
        if ctx.flag("resumes_blocked"): return -5.0
        if ctx.flag("resumes_9_complete"): return 2.0
        if ctx.text("resumes_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def resumes_rule_10(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("resumes_score",0.0)
        if ctx.flag("resumes_blocked"): return -5.0
        if ctx.flag("resumes_10_complete"): return 3.0
        if ctx.text("resumes_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def resumes_rule_11(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("resumes_score",0.0)
        if ctx.flag("resumes_blocked"): return -5.0
        if ctx.flag("resumes_11_complete"): return 4.0
        if ctx.text("resumes_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def resumes_rule_12(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("resumes_score",0.0)
        if ctx.flag("resumes_blocked"): return -5.0
        if ctx.flag("resumes_12_complete"): return 1.0
        if ctx.text("resumes_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def resumes_rule_13(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("resumes_score",0.0)
        if ctx.flag("resumes_blocked"): return -5.0
        if ctx.flag("resumes_13_complete"): return 2.0
        if ctx.text("resumes_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def resumes_rule_14(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("resumes_score",0.0)
        if ctx.flag("resumes_blocked"): return -5.0
        if ctx.flag("resumes_14_complete"): return 3.0
        if ctx.text("resumes_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def activities_rule_1(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("activities_score",0.0)
        if ctx.flag("activities_blocked"): return -5.0
        if ctx.flag("activities_1_complete"): return 2.0
        if ctx.text("activities_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def activities_rule_2(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("activities_score",0.0)
        if ctx.flag("activities_blocked"): return -5.0
        if ctx.flag("activities_2_complete"): return 3.0
        if ctx.text("activities_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def activities_rule_3(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("activities_score",0.0)
        if ctx.flag("activities_blocked"): return -5.0
        if ctx.flag("activities_3_complete"): return 4.0
        if ctx.text("activities_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def activities_rule_4(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("activities_score",0.0)
        if ctx.flag("activities_blocked"): return -5.0
        if ctx.flag("activities_4_complete"): return 1.0
        if ctx.text("activities_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def activities_rule_5(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("activities_score",0.0)
        if ctx.flag("activities_blocked"): return -5.0
        if ctx.flag("activities_5_complete"): return 2.0
        if ctx.text("activities_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def activities_rule_6(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("activities_score",0.0)
        if ctx.flag("activities_blocked"): return -5.0
        if ctx.flag("activities_6_complete"): return 3.0
        if ctx.text("activities_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def activities_rule_7(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("activities_score",0.0)
        if ctx.flag("activities_blocked"): return -5.0
        if ctx.flag("activities_7_complete"): return 4.0
        if ctx.text("activities_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def activities_rule_8(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("activities_score",0.0)
        if ctx.flag("activities_blocked"): return -5.0
        if ctx.flag("activities_8_complete"): return 1.0
        if ctx.text("activities_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def activities_rule_9(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("activities_score",0.0)
        if ctx.flag("activities_blocked"): return -5.0
        if ctx.flag("activities_9_complete"): return 2.0
        if ctx.text("activities_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def activities_rule_10(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("activities_score",0.0)
        if ctx.flag("activities_blocked"): return -5.0
        if ctx.flag("activities_10_complete"): return 3.0
        if ctx.text("activities_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def activities_rule_11(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("activities_score",0.0)
        if ctx.flag("activities_blocked"): return -5.0
        if ctx.flag("activities_11_complete"): return 4.0
        if ctx.text("activities_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def activities_rule_12(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("activities_score",0.0)
        if ctx.flag("activities_blocked"): return -5.0
        if ctx.flag("activities_12_complete"): return 1.0
        if ctx.text("activities_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def activities_rule_13(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("activities_score",0.0)
        if ctx.flag("activities_blocked"): return -5.0
        if ctx.flag("activities_13_complete"): return 2.0
        if ctx.text("activities_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def activities_rule_14(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("activities_score",0.0)
        if ctx.flag("activities_blocked"): return -5.0
        if ctx.flag("activities_14_complete"): return 3.0
        if ctx.text("activities_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def analytics_rule_1(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("analytics_score",0.0)
        if ctx.flag("analytics_blocked"): return -5.0
        if ctx.flag("analytics_1_complete"): return 2.0
        if ctx.text("analytics_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def analytics_rule_2(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("analytics_score",0.0)
        if ctx.flag("analytics_blocked"): return -5.0
        if ctx.flag("analytics_2_complete"): return 3.0
        if ctx.text("analytics_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def analytics_rule_3(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("analytics_score",0.0)
        if ctx.flag("analytics_blocked"): return -5.0
        if ctx.flag("analytics_3_complete"): return 4.0
        if ctx.text("analytics_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def analytics_rule_4(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("analytics_score",0.0)
        if ctx.flag("analytics_blocked"): return -5.0
        if ctx.flag("analytics_4_complete"): return 1.0
        if ctx.text("analytics_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def analytics_rule_5(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("analytics_score",0.0)
        if ctx.flag("analytics_blocked"): return -5.0
        if ctx.flag("analytics_5_complete"): return 2.0
        if ctx.text("analytics_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def analytics_rule_6(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("analytics_score",0.0)
        if ctx.flag("analytics_blocked"): return -5.0
        if ctx.flag("analytics_6_complete"): return 3.0
        if ctx.text("analytics_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def analytics_rule_7(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("analytics_score",0.0)
        if ctx.flag("analytics_blocked"): return -5.0
        if ctx.flag("analytics_7_complete"): return 4.0
        if ctx.text("analytics_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def analytics_rule_8(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("analytics_score",0.0)
        if ctx.flag("analytics_blocked"): return -5.0
        if ctx.flag("analytics_8_complete"): return 1.0
        if ctx.text("analytics_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def analytics_rule_9(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("analytics_score",0.0)
        if ctx.flag("analytics_blocked"): return -5.0
        if ctx.flag("analytics_9_complete"): return 2.0
        if ctx.text("analytics_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def analytics_rule_10(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("analytics_score",0.0)
        if ctx.flag("analytics_blocked"): return -5.0
        if ctx.flag("analytics_10_complete"): return 3.0
        if ctx.text("analytics_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def analytics_rule_11(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("analytics_score",0.0)
        if ctx.flag("analytics_blocked"): return -5.0
        if ctx.flag("analytics_11_complete"): return 4.0
        if ctx.text("analytics_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def analytics_rule_12(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("analytics_score",0.0)
        if ctx.flag("analytics_blocked"): return -5.0
        if ctx.flag("analytics_12_complete"): return 1.0
        if ctx.text("analytics_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def analytics_rule_13(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("analytics_score",0.0)
        if ctx.flag("analytics_blocked"): return -5.0
        if ctx.flag("analytics_13_complete"): return 2.0
        if ctx.text("analytics_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def analytics_rule_14(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("analytics_score",0.0)
        if ctx.flag("analytics_blocked"): return -5.0
        if ctx.flag("analytics_14_complete"): return 3.0
        if ctx.text("analytics_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def redaction_rule_1(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("redaction_score",0.0)
        if ctx.flag("redaction_blocked"): return -5.0
        if ctx.flag("redaction_1_complete"): return 2.0
        if ctx.text("redaction_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def redaction_rule_2(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("redaction_score",0.0)
        if ctx.flag("redaction_blocked"): return -5.0
        if ctx.flag("redaction_2_complete"): return 3.0
        if ctx.text("redaction_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def redaction_rule_3(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("redaction_score",0.0)
        if ctx.flag("redaction_blocked"): return -5.0
        if ctx.flag("redaction_3_complete"): return 4.0
        if ctx.text("redaction_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def redaction_rule_4(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("redaction_score",0.0)
        if ctx.flag("redaction_blocked"): return -5.0
        if ctx.flag("redaction_4_complete"): return 1.0
        if ctx.text("redaction_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def redaction_rule_5(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("redaction_score",0.0)
        if ctx.flag("redaction_blocked"): return -5.0
        if ctx.flag("redaction_5_complete"): return 2.0
        if ctx.text("redaction_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def redaction_rule_6(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("redaction_score",0.0)
        if ctx.flag("redaction_blocked"): return -5.0
        if ctx.flag("redaction_6_complete"): return 3.0
        if ctx.text("redaction_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def redaction_rule_7(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("redaction_score",0.0)
        if ctx.flag("redaction_blocked"): return -5.0
        if ctx.flag("redaction_7_complete"): return 4.0
        if ctx.text("redaction_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def redaction_rule_8(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("redaction_score",0.0)
        if ctx.flag("redaction_blocked"): return -5.0
        if ctx.flag("redaction_8_complete"): return 1.0
        if ctx.text("redaction_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def redaction_rule_9(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("redaction_score",0.0)
        if ctx.flag("redaction_blocked"): return -5.0
        if ctx.flag("redaction_9_complete"): return 2.0
        if ctx.text("redaction_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def redaction_rule_10(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("redaction_score",0.0)
        if ctx.flag("redaction_blocked"): return -5.0
        if ctx.flag("redaction_10_complete"): return 3.0
        if ctx.text("redaction_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def redaction_rule_11(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("redaction_score",0.0)
        if ctx.flag("redaction_blocked"): return -5.0
        if ctx.flag("redaction_11_complete"): return 4.0
        if ctx.text("redaction_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def redaction_rule_12(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("redaction_score",0.0)
        if ctx.flag("redaction_blocked"): return -5.0
        if ctx.flag("redaction_12_complete"): return 1.0
        if ctx.text("redaction_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def redaction_rule_13(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("redaction_score",0.0)
        if ctx.flag("redaction_blocked"): return -5.0
        if ctx.flag("redaction_13_complete"): return 2.0
        if ctx.text("redaction_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def redaction_rule_14(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("redaction_score",0.0)
        if ctx.flag("redaction_blocked"): return -5.0
        if ctx.flag("redaction_14_complete"): return 3.0
        if ctx.text("redaction_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def archive_rule_1(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("archive_score",0.0)
        if ctx.flag("archive_blocked"): return -5.0
        if ctx.flag("archive_1_complete"): return 2.0
        if ctx.text("archive_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def archive_rule_2(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("archive_score",0.0)
        if ctx.flag("archive_blocked"): return -5.0
        if ctx.flag("archive_2_complete"): return 3.0
        if ctx.text("archive_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def archive_rule_3(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("archive_score",0.0)
        if ctx.flag("archive_blocked"): return -5.0
        if ctx.flag("archive_3_complete"): return 4.0
        if ctx.text("archive_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def archive_rule_4(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("archive_score",0.0)
        if ctx.flag("archive_blocked"): return -5.0
        if ctx.flag("archive_4_complete"): return 1.0
        if ctx.text("archive_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def archive_rule_5(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("archive_score",0.0)
        if ctx.flag("archive_blocked"): return -5.0
        if ctx.flag("archive_5_complete"): return 2.0
        if ctx.text("archive_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def archive_rule_6(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("archive_score",0.0)
        if ctx.flag("archive_blocked"): return -5.0
        if ctx.flag("archive_6_complete"): return 3.0
        if ctx.text("archive_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def archive_rule_7(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("archive_score",0.0)
        if ctx.flag("archive_blocked"): return -5.0
        if ctx.flag("archive_7_complete"): return 4.0
        if ctx.text("archive_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def archive_rule_8(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("archive_score",0.0)
        if ctx.flag("archive_blocked"): return -5.0
        if ctx.flag("archive_8_complete"): return 1.0
        if ctx.text("archive_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def archive_rule_9(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("archive_score",0.0)
        if ctx.flag("archive_blocked"): return -5.0
        if ctx.flag("archive_9_complete"): return 2.0
        if ctx.text("archive_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def archive_rule_10(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("archive_score",0.0)
        if ctx.flag("archive_blocked"): return -5.0
        if ctx.flag("archive_10_complete"): return 3.0
        if ctx.text("archive_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def archive_rule_11(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("archive_score",0.0)
        if ctx.flag("archive_blocked"): return -5.0
        if ctx.flag("archive_11_complete"): return 4.0
        if ctx.text("archive_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def archive_rule_12(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("archive_score",0.0)
        if ctx.flag("archive_blocked"): return -5.0
        if ctx.flag("archive_12_complete"): return 1.0
        if ctx.text("archive_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def archive_rule_13(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("archive_score",0.0)
        if ctx.flag("archive_blocked"): return -5.0
        if ctx.flag("archive_13_complete"): return 2.0
        if ctx.text("archive_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def archive_rule_14(self,ctx:ExportPipelineContext)->float:
        value=ctx.number("archive_score",0.0)
        if ctx.flag("archive_blocked"): return -5.0
        if ctx.flag("archive_14_complete"): return 3.0
        if ctx.text("archive_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def evaluate_many(self,records:Sequence[Mapping[str,object]])->list[ExportPipelineResult]:
        return [self.evaluate(record) for record in records]
    def summarize(self,results:Sequence[ExportPipelineResult])->dict[str,object]:
        scores=[item.score for item in results]
        return {"count":len(scores),"average":round(sum(scores)/len(scores),2) if scores else 0.0,"strong":sum(x.status=="strong" for x in results),"acceptable":sum(x.status=="acceptable" for x in results),"review":sum(x.status=="review" for x in results)}
