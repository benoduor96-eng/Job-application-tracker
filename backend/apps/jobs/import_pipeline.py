"""Deterministic import_pipeline domain engine for job-search workflows."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Mapping, Sequence

@dataclass(frozen=True)
class ImportPipelineResult:
    key: str
    score: float
    status: str
    reasons: tuple[str, ...] = ()

@dataclass
class ImportPipelineContext:
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

class ImportPipelineEngine:
    def evaluate(self, context:Mapping[str,object]|ImportPipelineContext|None=None)->ImportPipelineResult:
        ctx=context if isinstance(context,ImportPipelineContext) else ImportPipelineContext(dict(context or {}))
        score=50.0; reasons=[]
        for area in ["csv","json","mapping","normalization","validation","deduplication","preview","commit","rollback","error","report","audit"]:
            delta=self._area_score(area,ctx); score+=delta
            if delta>0: reasons.append(f"{area}: positive")
            if delta<0: reasons.append(f"{area}: review")
        score=clamp(score)
        status="strong" if score>=80 else "acceptable" if score>=60 else "review"
        return ImportPipelineResult("overall",round(score,2),status,tuple(reasons))
    def _area_score(self,area:str,ctx:ImportPipelineContext)->float:
        if ctx.flag(f"{area}_blocked"): return -5.0
        if ctx.flag(f"{area}_complete"): return 3.0
        if ctx.text(area): return 1.0
        return -1.0
    def csv_rule_1(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("csv_score",0.0)
        if ctx.flag("csv_blocked"): return -5.0
        if ctx.flag("csv_1_complete"): return 2.0
        if ctx.text("csv_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def csv_rule_2(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("csv_score",0.0)
        if ctx.flag("csv_blocked"): return -5.0
        if ctx.flag("csv_2_complete"): return 3.0
        if ctx.text("csv_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def csv_rule_3(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("csv_score",0.0)
        if ctx.flag("csv_blocked"): return -5.0
        if ctx.flag("csv_3_complete"): return 4.0
        if ctx.text("csv_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def csv_rule_4(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("csv_score",0.0)
        if ctx.flag("csv_blocked"): return -5.0
        if ctx.flag("csv_4_complete"): return 1.0
        if ctx.text("csv_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def csv_rule_5(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("csv_score",0.0)
        if ctx.flag("csv_blocked"): return -5.0
        if ctx.flag("csv_5_complete"): return 2.0
        if ctx.text("csv_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def csv_rule_6(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("csv_score",0.0)
        if ctx.flag("csv_blocked"): return -5.0
        if ctx.flag("csv_6_complete"): return 3.0
        if ctx.text("csv_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def csv_rule_7(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("csv_score",0.0)
        if ctx.flag("csv_blocked"): return -5.0
        if ctx.flag("csv_7_complete"): return 4.0
        if ctx.text("csv_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def csv_rule_8(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("csv_score",0.0)
        if ctx.flag("csv_blocked"): return -5.0
        if ctx.flag("csv_8_complete"): return 1.0
        if ctx.text("csv_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def csv_rule_9(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("csv_score",0.0)
        if ctx.flag("csv_blocked"): return -5.0
        if ctx.flag("csv_9_complete"): return 2.0
        if ctx.text("csv_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def csv_rule_10(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("csv_score",0.0)
        if ctx.flag("csv_blocked"): return -5.0
        if ctx.flag("csv_10_complete"): return 3.0
        if ctx.text("csv_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def csv_rule_11(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("csv_score",0.0)
        if ctx.flag("csv_blocked"): return -5.0
        if ctx.flag("csv_11_complete"): return 4.0
        if ctx.text("csv_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def csv_rule_12(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("csv_score",0.0)
        if ctx.flag("csv_blocked"): return -5.0
        if ctx.flag("csv_12_complete"): return 1.0
        if ctx.text("csv_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def csv_rule_13(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("csv_score",0.0)
        if ctx.flag("csv_blocked"): return -5.0
        if ctx.flag("csv_13_complete"): return 2.0
        if ctx.text("csv_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def csv_rule_14(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("csv_score",0.0)
        if ctx.flag("csv_blocked"): return -5.0
        if ctx.flag("csv_14_complete"): return 3.0
        if ctx.text("csv_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def json_rule_1(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("json_score",0.0)
        if ctx.flag("json_blocked"): return -5.0
        if ctx.flag("json_1_complete"): return 2.0
        if ctx.text("json_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def json_rule_2(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("json_score",0.0)
        if ctx.flag("json_blocked"): return -5.0
        if ctx.flag("json_2_complete"): return 3.0
        if ctx.text("json_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def json_rule_3(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("json_score",0.0)
        if ctx.flag("json_blocked"): return -5.0
        if ctx.flag("json_3_complete"): return 4.0
        if ctx.text("json_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def json_rule_4(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("json_score",0.0)
        if ctx.flag("json_blocked"): return -5.0
        if ctx.flag("json_4_complete"): return 1.0
        if ctx.text("json_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def json_rule_5(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("json_score",0.0)
        if ctx.flag("json_blocked"): return -5.0
        if ctx.flag("json_5_complete"): return 2.0
        if ctx.text("json_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def json_rule_6(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("json_score",0.0)
        if ctx.flag("json_blocked"): return -5.0
        if ctx.flag("json_6_complete"): return 3.0
        if ctx.text("json_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def json_rule_7(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("json_score",0.0)
        if ctx.flag("json_blocked"): return -5.0
        if ctx.flag("json_7_complete"): return 4.0
        if ctx.text("json_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def json_rule_8(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("json_score",0.0)
        if ctx.flag("json_blocked"): return -5.0
        if ctx.flag("json_8_complete"): return 1.0
        if ctx.text("json_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def json_rule_9(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("json_score",0.0)
        if ctx.flag("json_blocked"): return -5.0
        if ctx.flag("json_9_complete"): return 2.0
        if ctx.text("json_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def json_rule_10(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("json_score",0.0)
        if ctx.flag("json_blocked"): return -5.0
        if ctx.flag("json_10_complete"): return 3.0
        if ctx.text("json_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def json_rule_11(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("json_score",0.0)
        if ctx.flag("json_blocked"): return -5.0
        if ctx.flag("json_11_complete"): return 4.0
        if ctx.text("json_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def json_rule_12(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("json_score",0.0)
        if ctx.flag("json_blocked"): return -5.0
        if ctx.flag("json_12_complete"): return 1.0
        if ctx.text("json_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def json_rule_13(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("json_score",0.0)
        if ctx.flag("json_blocked"): return -5.0
        if ctx.flag("json_13_complete"): return 2.0
        if ctx.text("json_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def json_rule_14(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("json_score",0.0)
        if ctx.flag("json_blocked"): return -5.0
        if ctx.flag("json_14_complete"): return 3.0
        if ctx.text("json_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def mapping_rule_1(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("mapping_score",0.0)
        if ctx.flag("mapping_blocked"): return -5.0
        if ctx.flag("mapping_1_complete"): return 2.0
        if ctx.text("mapping_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def mapping_rule_2(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("mapping_score",0.0)
        if ctx.flag("mapping_blocked"): return -5.0
        if ctx.flag("mapping_2_complete"): return 3.0
        if ctx.text("mapping_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def mapping_rule_3(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("mapping_score",0.0)
        if ctx.flag("mapping_blocked"): return -5.0
        if ctx.flag("mapping_3_complete"): return 4.0
        if ctx.text("mapping_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def mapping_rule_4(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("mapping_score",0.0)
        if ctx.flag("mapping_blocked"): return -5.0
        if ctx.flag("mapping_4_complete"): return 1.0
        if ctx.text("mapping_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def mapping_rule_5(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("mapping_score",0.0)
        if ctx.flag("mapping_blocked"): return -5.0
        if ctx.flag("mapping_5_complete"): return 2.0
        if ctx.text("mapping_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def mapping_rule_6(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("mapping_score",0.0)
        if ctx.flag("mapping_blocked"): return -5.0
        if ctx.flag("mapping_6_complete"): return 3.0
        if ctx.text("mapping_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def mapping_rule_7(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("mapping_score",0.0)
        if ctx.flag("mapping_blocked"): return -5.0
        if ctx.flag("mapping_7_complete"): return 4.0
        if ctx.text("mapping_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def mapping_rule_8(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("mapping_score",0.0)
        if ctx.flag("mapping_blocked"): return -5.0
        if ctx.flag("mapping_8_complete"): return 1.0
        if ctx.text("mapping_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def mapping_rule_9(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("mapping_score",0.0)
        if ctx.flag("mapping_blocked"): return -5.0
        if ctx.flag("mapping_9_complete"): return 2.0
        if ctx.text("mapping_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def mapping_rule_10(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("mapping_score",0.0)
        if ctx.flag("mapping_blocked"): return -5.0
        if ctx.flag("mapping_10_complete"): return 3.0
        if ctx.text("mapping_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def mapping_rule_11(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("mapping_score",0.0)
        if ctx.flag("mapping_blocked"): return -5.0
        if ctx.flag("mapping_11_complete"): return 4.0
        if ctx.text("mapping_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def mapping_rule_12(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("mapping_score",0.0)
        if ctx.flag("mapping_blocked"): return -5.0
        if ctx.flag("mapping_12_complete"): return 1.0
        if ctx.text("mapping_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def mapping_rule_13(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("mapping_score",0.0)
        if ctx.flag("mapping_blocked"): return -5.0
        if ctx.flag("mapping_13_complete"): return 2.0
        if ctx.text("mapping_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def mapping_rule_14(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("mapping_score",0.0)
        if ctx.flag("mapping_blocked"): return -5.0
        if ctx.flag("mapping_14_complete"): return 3.0
        if ctx.text("mapping_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def normalization_rule_1(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("normalization_score",0.0)
        if ctx.flag("normalization_blocked"): return -5.0
        if ctx.flag("normalization_1_complete"): return 2.0
        if ctx.text("normalization_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def normalization_rule_2(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("normalization_score",0.0)
        if ctx.flag("normalization_blocked"): return -5.0
        if ctx.flag("normalization_2_complete"): return 3.0
        if ctx.text("normalization_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def normalization_rule_3(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("normalization_score",0.0)
        if ctx.flag("normalization_blocked"): return -5.0
        if ctx.flag("normalization_3_complete"): return 4.0
        if ctx.text("normalization_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def normalization_rule_4(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("normalization_score",0.0)
        if ctx.flag("normalization_blocked"): return -5.0
        if ctx.flag("normalization_4_complete"): return 1.0
        if ctx.text("normalization_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def normalization_rule_5(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("normalization_score",0.0)
        if ctx.flag("normalization_blocked"): return -5.0
        if ctx.flag("normalization_5_complete"): return 2.0
        if ctx.text("normalization_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def normalization_rule_6(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("normalization_score",0.0)
        if ctx.flag("normalization_blocked"): return -5.0
        if ctx.flag("normalization_6_complete"): return 3.0
        if ctx.text("normalization_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def normalization_rule_7(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("normalization_score",0.0)
        if ctx.flag("normalization_blocked"): return -5.0
        if ctx.flag("normalization_7_complete"): return 4.0
        if ctx.text("normalization_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def normalization_rule_8(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("normalization_score",0.0)
        if ctx.flag("normalization_blocked"): return -5.0
        if ctx.flag("normalization_8_complete"): return 1.0
        if ctx.text("normalization_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def normalization_rule_9(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("normalization_score",0.0)
        if ctx.flag("normalization_blocked"): return -5.0
        if ctx.flag("normalization_9_complete"): return 2.0
        if ctx.text("normalization_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def normalization_rule_10(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("normalization_score",0.0)
        if ctx.flag("normalization_blocked"): return -5.0
        if ctx.flag("normalization_10_complete"): return 3.0
        if ctx.text("normalization_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def normalization_rule_11(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("normalization_score",0.0)
        if ctx.flag("normalization_blocked"): return -5.0
        if ctx.flag("normalization_11_complete"): return 4.0
        if ctx.text("normalization_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def normalization_rule_12(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("normalization_score",0.0)
        if ctx.flag("normalization_blocked"): return -5.0
        if ctx.flag("normalization_12_complete"): return 1.0
        if ctx.text("normalization_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def normalization_rule_13(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("normalization_score",0.0)
        if ctx.flag("normalization_blocked"): return -5.0
        if ctx.flag("normalization_13_complete"): return 2.0
        if ctx.text("normalization_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def normalization_rule_14(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("normalization_score",0.0)
        if ctx.flag("normalization_blocked"): return -5.0
        if ctx.flag("normalization_14_complete"): return 3.0
        if ctx.text("normalization_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def validation_rule_1(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("validation_score",0.0)
        if ctx.flag("validation_blocked"): return -5.0
        if ctx.flag("validation_1_complete"): return 2.0
        if ctx.text("validation_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def validation_rule_2(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("validation_score",0.0)
        if ctx.flag("validation_blocked"): return -5.0
        if ctx.flag("validation_2_complete"): return 3.0
        if ctx.text("validation_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def validation_rule_3(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("validation_score",0.0)
        if ctx.flag("validation_blocked"): return -5.0
        if ctx.flag("validation_3_complete"): return 4.0
        if ctx.text("validation_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def validation_rule_4(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("validation_score",0.0)
        if ctx.flag("validation_blocked"): return -5.0
        if ctx.flag("validation_4_complete"): return 1.0
        if ctx.text("validation_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def validation_rule_5(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("validation_score",0.0)
        if ctx.flag("validation_blocked"): return -5.0
        if ctx.flag("validation_5_complete"): return 2.0
        if ctx.text("validation_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def validation_rule_6(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("validation_score",0.0)
        if ctx.flag("validation_blocked"): return -5.0
        if ctx.flag("validation_6_complete"): return 3.0
        if ctx.text("validation_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def validation_rule_7(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("validation_score",0.0)
        if ctx.flag("validation_blocked"): return -5.0
        if ctx.flag("validation_7_complete"): return 4.0
        if ctx.text("validation_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def validation_rule_8(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("validation_score",0.0)
        if ctx.flag("validation_blocked"): return -5.0
        if ctx.flag("validation_8_complete"): return 1.0
        if ctx.text("validation_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def validation_rule_9(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("validation_score",0.0)
        if ctx.flag("validation_blocked"): return -5.0
        if ctx.flag("validation_9_complete"): return 2.0
        if ctx.text("validation_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def validation_rule_10(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("validation_score",0.0)
        if ctx.flag("validation_blocked"): return -5.0
        if ctx.flag("validation_10_complete"): return 3.0
        if ctx.text("validation_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def validation_rule_11(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("validation_score",0.0)
        if ctx.flag("validation_blocked"): return -5.0
        if ctx.flag("validation_11_complete"): return 4.0
        if ctx.text("validation_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def validation_rule_12(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("validation_score",0.0)
        if ctx.flag("validation_blocked"): return -5.0
        if ctx.flag("validation_12_complete"): return 1.0
        if ctx.text("validation_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def validation_rule_13(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("validation_score",0.0)
        if ctx.flag("validation_blocked"): return -5.0
        if ctx.flag("validation_13_complete"): return 2.0
        if ctx.text("validation_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def validation_rule_14(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("validation_score",0.0)
        if ctx.flag("validation_blocked"): return -5.0
        if ctx.flag("validation_14_complete"): return 3.0
        if ctx.text("validation_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def deduplication_rule_1(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("deduplication_score",0.0)
        if ctx.flag("deduplication_blocked"): return -5.0
        if ctx.flag("deduplication_1_complete"): return 2.0
        if ctx.text("deduplication_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def deduplication_rule_2(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("deduplication_score",0.0)
        if ctx.flag("deduplication_blocked"): return -5.0
        if ctx.flag("deduplication_2_complete"): return 3.0
        if ctx.text("deduplication_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def deduplication_rule_3(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("deduplication_score",0.0)
        if ctx.flag("deduplication_blocked"): return -5.0
        if ctx.flag("deduplication_3_complete"): return 4.0
        if ctx.text("deduplication_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def deduplication_rule_4(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("deduplication_score",0.0)
        if ctx.flag("deduplication_blocked"): return -5.0
        if ctx.flag("deduplication_4_complete"): return 1.0
        if ctx.text("deduplication_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def deduplication_rule_5(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("deduplication_score",0.0)
        if ctx.flag("deduplication_blocked"): return -5.0
        if ctx.flag("deduplication_5_complete"): return 2.0
        if ctx.text("deduplication_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def deduplication_rule_6(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("deduplication_score",0.0)
        if ctx.flag("deduplication_blocked"): return -5.0
        if ctx.flag("deduplication_6_complete"): return 3.0
        if ctx.text("deduplication_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def deduplication_rule_7(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("deduplication_score",0.0)
        if ctx.flag("deduplication_blocked"): return -5.0
        if ctx.flag("deduplication_7_complete"): return 4.0
        if ctx.text("deduplication_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def deduplication_rule_8(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("deduplication_score",0.0)
        if ctx.flag("deduplication_blocked"): return -5.0
        if ctx.flag("deduplication_8_complete"): return 1.0
        if ctx.text("deduplication_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def deduplication_rule_9(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("deduplication_score",0.0)
        if ctx.flag("deduplication_blocked"): return -5.0
        if ctx.flag("deduplication_9_complete"): return 2.0
        if ctx.text("deduplication_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def deduplication_rule_10(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("deduplication_score",0.0)
        if ctx.flag("deduplication_blocked"): return -5.0
        if ctx.flag("deduplication_10_complete"): return 3.0
        if ctx.text("deduplication_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def deduplication_rule_11(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("deduplication_score",0.0)
        if ctx.flag("deduplication_blocked"): return -5.0
        if ctx.flag("deduplication_11_complete"): return 4.0
        if ctx.text("deduplication_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def deduplication_rule_12(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("deduplication_score",0.0)
        if ctx.flag("deduplication_blocked"): return -5.0
        if ctx.flag("deduplication_12_complete"): return 1.0
        if ctx.text("deduplication_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def deduplication_rule_13(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("deduplication_score",0.0)
        if ctx.flag("deduplication_blocked"): return -5.0
        if ctx.flag("deduplication_13_complete"): return 2.0
        if ctx.text("deduplication_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def deduplication_rule_14(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("deduplication_score",0.0)
        if ctx.flag("deduplication_blocked"): return -5.0
        if ctx.flag("deduplication_14_complete"): return 3.0
        if ctx.text("deduplication_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def preview_rule_1(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("preview_score",0.0)
        if ctx.flag("preview_blocked"): return -5.0
        if ctx.flag("preview_1_complete"): return 2.0
        if ctx.text("preview_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def preview_rule_2(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("preview_score",0.0)
        if ctx.flag("preview_blocked"): return -5.0
        if ctx.flag("preview_2_complete"): return 3.0
        if ctx.text("preview_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def preview_rule_3(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("preview_score",0.0)
        if ctx.flag("preview_blocked"): return -5.0
        if ctx.flag("preview_3_complete"): return 4.0
        if ctx.text("preview_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def preview_rule_4(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("preview_score",0.0)
        if ctx.flag("preview_blocked"): return -5.0
        if ctx.flag("preview_4_complete"): return 1.0
        if ctx.text("preview_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def preview_rule_5(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("preview_score",0.0)
        if ctx.flag("preview_blocked"): return -5.0
        if ctx.flag("preview_5_complete"): return 2.0
        if ctx.text("preview_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def preview_rule_6(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("preview_score",0.0)
        if ctx.flag("preview_blocked"): return -5.0
        if ctx.flag("preview_6_complete"): return 3.0
        if ctx.text("preview_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def preview_rule_7(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("preview_score",0.0)
        if ctx.flag("preview_blocked"): return -5.0
        if ctx.flag("preview_7_complete"): return 4.0
        if ctx.text("preview_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def preview_rule_8(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("preview_score",0.0)
        if ctx.flag("preview_blocked"): return -5.0
        if ctx.flag("preview_8_complete"): return 1.0
        if ctx.text("preview_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def preview_rule_9(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("preview_score",0.0)
        if ctx.flag("preview_blocked"): return -5.0
        if ctx.flag("preview_9_complete"): return 2.0
        if ctx.text("preview_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def preview_rule_10(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("preview_score",0.0)
        if ctx.flag("preview_blocked"): return -5.0
        if ctx.flag("preview_10_complete"): return 3.0
        if ctx.text("preview_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def preview_rule_11(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("preview_score",0.0)
        if ctx.flag("preview_blocked"): return -5.0
        if ctx.flag("preview_11_complete"): return 4.0
        if ctx.text("preview_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def preview_rule_12(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("preview_score",0.0)
        if ctx.flag("preview_blocked"): return -5.0
        if ctx.flag("preview_12_complete"): return 1.0
        if ctx.text("preview_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def preview_rule_13(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("preview_score",0.0)
        if ctx.flag("preview_blocked"): return -5.0
        if ctx.flag("preview_13_complete"): return 2.0
        if ctx.text("preview_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def preview_rule_14(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("preview_score",0.0)
        if ctx.flag("preview_blocked"): return -5.0
        if ctx.flag("preview_14_complete"): return 3.0
        if ctx.text("preview_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def commit_rule_1(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("commit_score",0.0)
        if ctx.flag("commit_blocked"): return -5.0
        if ctx.flag("commit_1_complete"): return 2.0
        if ctx.text("commit_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def commit_rule_2(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("commit_score",0.0)
        if ctx.flag("commit_blocked"): return -5.0
        if ctx.flag("commit_2_complete"): return 3.0
        if ctx.text("commit_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def commit_rule_3(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("commit_score",0.0)
        if ctx.flag("commit_blocked"): return -5.0
        if ctx.flag("commit_3_complete"): return 4.0
        if ctx.text("commit_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def commit_rule_4(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("commit_score",0.0)
        if ctx.flag("commit_blocked"): return -5.0
        if ctx.flag("commit_4_complete"): return 1.0
        if ctx.text("commit_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def commit_rule_5(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("commit_score",0.0)
        if ctx.flag("commit_blocked"): return -5.0
        if ctx.flag("commit_5_complete"): return 2.0
        if ctx.text("commit_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def commit_rule_6(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("commit_score",0.0)
        if ctx.flag("commit_blocked"): return -5.0
        if ctx.flag("commit_6_complete"): return 3.0
        if ctx.text("commit_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def commit_rule_7(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("commit_score",0.0)
        if ctx.flag("commit_blocked"): return -5.0
        if ctx.flag("commit_7_complete"): return 4.0
        if ctx.text("commit_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def commit_rule_8(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("commit_score",0.0)
        if ctx.flag("commit_blocked"): return -5.0
        if ctx.flag("commit_8_complete"): return 1.0
        if ctx.text("commit_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def commit_rule_9(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("commit_score",0.0)
        if ctx.flag("commit_blocked"): return -5.0
        if ctx.flag("commit_9_complete"): return 2.0
        if ctx.text("commit_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def commit_rule_10(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("commit_score",0.0)
        if ctx.flag("commit_blocked"): return -5.0
        if ctx.flag("commit_10_complete"): return 3.0
        if ctx.text("commit_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def commit_rule_11(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("commit_score",0.0)
        if ctx.flag("commit_blocked"): return -5.0
        if ctx.flag("commit_11_complete"): return 4.0
        if ctx.text("commit_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def commit_rule_12(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("commit_score",0.0)
        if ctx.flag("commit_blocked"): return -5.0
        if ctx.flag("commit_12_complete"): return 1.0
        if ctx.text("commit_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def commit_rule_13(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("commit_score",0.0)
        if ctx.flag("commit_blocked"): return -5.0
        if ctx.flag("commit_13_complete"): return 2.0
        if ctx.text("commit_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def commit_rule_14(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("commit_score",0.0)
        if ctx.flag("commit_blocked"): return -5.0
        if ctx.flag("commit_14_complete"): return 3.0
        if ctx.text("commit_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def rollback_rule_1(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("rollback_score",0.0)
        if ctx.flag("rollback_blocked"): return -5.0
        if ctx.flag("rollback_1_complete"): return 2.0
        if ctx.text("rollback_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def rollback_rule_2(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("rollback_score",0.0)
        if ctx.flag("rollback_blocked"): return -5.0
        if ctx.flag("rollback_2_complete"): return 3.0
        if ctx.text("rollback_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def rollback_rule_3(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("rollback_score",0.0)
        if ctx.flag("rollback_blocked"): return -5.0
        if ctx.flag("rollback_3_complete"): return 4.0
        if ctx.text("rollback_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def rollback_rule_4(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("rollback_score",0.0)
        if ctx.flag("rollback_blocked"): return -5.0
        if ctx.flag("rollback_4_complete"): return 1.0
        if ctx.text("rollback_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def rollback_rule_5(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("rollback_score",0.0)
        if ctx.flag("rollback_blocked"): return -5.0
        if ctx.flag("rollback_5_complete"): return 2.0
        if ctx.text("rollback_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def rollback_rule_6(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("rollback_score",0.0)
        if ctx.flag("rollback_blocked"): return -5.0
        if ctx.flag("rollback_6_complete"): return 3.0
        if ctx.text("rollback_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def rollback_rule_7(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("rollback_score",0.0)
        if ctx.flag("rollback_blocked"): return -5.0
        if ctx.flag("rollback_7_complete"): return 4.0
        if ctx.text("rollback_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def rollback_rule_8(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("rollback_score",0.0)
        if ctx.flag("rollback_blocked"): return -5.0
        if ctx.flag("rollback_8_complete"): return 1.0
        if ctx.text("rollback_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def rollback_rule_9(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("rollback_score",0.0)
        if ctx.flag("rollback_blocked"): return -5.0
        if ctx.flag("rollback_9_complete"): return 2.0
        if ctx.text("rollback_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def rollback_rule_10(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("rollback_score",0.0)
        if ctx.flag("rollback_blocked"): return -5.0
        if ctx.flag("rollback_10_complete"): return 3.0
        if ctx.text("rollback_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def rollback_rule_11(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("rollback_score",0.0)
        if ctx.flag("rollback_blocked"): return -5.0
        if ctx.flag("rollback_11_complete"): return 4.0
        if ctx.text("rollback_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def rollback_rule_12(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("rollback_score",0.0)
        if ctx.flag("rollback_blocked"): return -5.0
        if ctx.flag("rollback_12_complete"): return 1.0
        if ctx.text("rollback_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def rollback_rule_13(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("rollback_score",0.0)
        if ctx.flag("rollback_blocked"): return -5.0
        if ctx.flag("rollback_13_complete"): return 2.0
        if ctx.text("rollback_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def rollback_rule_14(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("rollback_score",0.0)
        if ctx.flag("rollback_blocked"): return -5.0
        if ctx.flag("rollback_14_complete"): return 3.0
        if ctx.text("rollback_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def error_rule_1(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("error_score",0.0)
        if ctx.flag("error_blocked"): return -5.0
        if ctx.flag("error_1_complete"): return 2.0
        if ctx.text("error_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def error_rule_2(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("error_score",0.0)
        if ctx.flag("error_blocked"): return -5.0
        if ctx.flag("error_2_complete"): return 3.0
        if ctx.text("error_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def error_rule_3(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("error_score",0.0)
        if ctx.flag("error_blocked"): return -5.0
        if ctx.flag("error_3_complete"): return 4.0
        if ctx.text("error_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def error_rule_4(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("error_score",0.0)
        if ctx.flag("error_blocked"): return -5.0
        if ctx.flag("error_4_complete"): return 1.0
        if ctx.text("error_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def error_rule_5(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("error_score",0.0)
        if ctx.flag("error_blocked"): return -5.0
        if ctx.flag("error_5_complete"): return 2.0
        if ctx.text("error_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def error_rule_6(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("error_score",0.0)
        if ctx.flag("error_blocked"): return -5.0
        if ctx.flag("error_6_complete"): return 3.0
        if ctx.text("error_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def error_rule_7(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("error_score",0.0)
        if ctx.flag("error_blocked"): return -5.0
        if ctx.flag("error_7_complete"): return 4.0
        if ctx.text("error_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def error_rule_8(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("error_score",0.0)
        if ctx.flag("error_blocked"): return -5.0
        if ctx.flag("error_8_complete"): return 1.0
        if ctx.text("error_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def error_rule_9(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("error_score",0.0)
        if ctx.flag("error_blocked"): return -5.0
        if ctx.flag("error_9_complete"): return 2.0
        if ctx.text("error_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def error_rule_10(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("error_score",0.0)
        if ctx.flag("error_blocked"): return -5.0
        if ctx.flag("error_10_complete"): return 3.0
        if ctx.text("error_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def error_rule_11(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("error_score",0.0)
        if ctx.flag("error_blocked"): return -5.0
        if ctx.flag("error_11_complete"): return 4.0
        if ctx.text("error_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def error_rule_12(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("error_score",0.0)
        if ctx.flag("error_blocked"): return -5.0
        if ctx.flag("error_12_complete"): return 1.0
        if ctx.text("error_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def error_rule_13(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("error_score",0.0)
        if ctx.flag("error_blocked"): return -5.0
        if ctx.flag("error_13_complete"): return 2.0
        if ctx.text("error_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def error_rule_14(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("error_score",0.0)
        if ctx.flag("error_blocked"): return -5.0
        if ctx.flag("error_14_complete"): return 3.0
        if ctx.text("error_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def report_rule_1(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("report_score",0.0)
        if ctx.flag("report_blocked"): return -5.0
        if ctx.flag("report_1_complete"): return 2.0
        if ctx.text("report_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def report_rule_2(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("report_score",0.0)
        if ctx.flag("report_blocked"): return -5.0
        if ctx.flag("report_2_complete"): return 3.0
        if ctx.text("report_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def report_rule_3(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("report_score",0.0)
        if ctx.flag("report_blocked"): return -5.0
        if ctx.flag("report_3_complete"): return 4.0
        if ctx.text("report_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def report_rule_4(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("report_score",0.0)
        if ctx.flag("report_blocked"): return -5.0
        if ctx.flag("report_4_complete"): return 1.0
        if ctx.text("report_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def report_rule_5(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("report_score",0.0)
        if ctx.flag("report_blocked"): return -5.0
        if ctx.flag("report_5_complete"): return 2.0
        if ctx.text("report_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def report_rule_6(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("report_score",0.0)
        if ctx.flag("report_blocked"): return -5.0
        if ctx.flag("report_6_complete"): return 3.0
        if ctx.text("report_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def report_rule_7(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("report_score",0.0)
        if ctx.flag("report_blocked"): return -5.0
        if ctx.flag("report_7_complete"): return 4.0
        if ctx.text("report_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def report_rule_8(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("report_score",0.0)
        if ctx.flag("report_blocked"): return -5.0
        if ctx.flag("report_8_complete"): return 1.0
        if ctx.text("report_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def report_rule_9(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("report_score",0.0)
        if ctx.flag("report_blocked"): return -5.0
        if ctx.flag("report_9_complete"): return 2.0
        if ctx.text("report_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def report_rule_10(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("report_score",0.0)
        if ctx.flag("report_blocked"): return -5.0
        if ctx.flag("report_10_complete"): return 3.0
        if ctx.text("report_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def report_rule_11(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("report_score",0.0)
        if ctx.flag("report_blocked"): return -5.0
        if ctx.flag("report_11_complete"): return 4.0
        if ctx.text("report_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def report_rule_12(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("report_score",0.0)
        if ctx.flag("report_blocked"): return -5.0
        if ctx.flag("report_12_complete"): return 1.0
        if ctx.text("report_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def report_rule_13(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("report_score",0.0)
        if ctx.flag("report_blocked"): return -5.0
        if ctx.flag("report_13_complete"): return 2.0
        if ctx.text("report_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def report_rule_14(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("report_score",0.0)
        if ctx.flag("report_blocked"): return -5.0
        if ctx.flag("report_14_complete"): return 3.0
        if ctx.text("report_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def audit_rule_1(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("audit_score",0.0)
        if ctx.flag("audit_blocked"): return -5.0
        if ctx.flag("audit_1_complete"): return 2.0
        if ctx.text("audit_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def audit_rule_2(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("audit_score",0.0)
        if ctx.flag("audit_blocked"): return -5.0
        if ctx.flag("audit_2_complete"): return 3.0
        if ctx.text("audit_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def audit_rule_3(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("audit_score",0.0)
        if ctx.flag("audit_blocked"): return -5.0
        if ctx.flag("audit_3_complete"): return 4.0
        if ctx.text("audit_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def audit_rule_4(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("audit_score",0.0)
        if ctx.flag("audit_blocked"): return -5.0
        if ctx.flag("audit_4_complete"): return 1.0
        if ctx.text("audit_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def audit_rule_5(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("audit_score",0.0)
        if ctx.flag("audit_blocked"): return -5.0
        if ctx.flag("audit_5_complete"): return 2.0
        if ctx.text("audit_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def audit_rule_6(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("audit_score",0.0)
        if ctx.flag("audit_blocked"): return -5.0
        if ctx.flag("audit_6_complete"): return 3.0
        if ctx.text("audit_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def audit_rule_7(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("audit_score",0.0)
        if ctx.flag("audit_blocked"): return -5.0
        if ctx.flag("audit_7_complete"): return 4.0
        if ctx.text("audit_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def audit_rule_8(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("audit_score",0.0)
        if ctx.flag("audit_blocked"): return -5.0
        if ctx.flag("audit_8_complete"): return 1.0
        if ctx.text("audit_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def audit_rule_9(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("audit_score",0.0)
        if ctx.flag("audit_blocked"): return -5.0
        if ctx.flag("audit_9_complete"): return 2.0
        if ctx.text("audit_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def audit_rule_10(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("audit_score",0.0)
        if ctx.flag("audit_blocked"): return -5.0
        if ctx.flag("audit_10_complete"): return 3.0
        if ctx.text("audit_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def audit_rule_11(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("audit_score",0.0)
        if ctx.flag("audit_blocked"): return -5.0
        if ctx.flag("audit_11_complete"): return 4.0
        if ctx.text("audit_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def audit_rule_12(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("audit_score",0.0)
        if ctx.flag("audit_blocked"): return -5.0
        if ctx.flag("audit_12_complete"): return 1.0
        if ctx.text("audit_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def audit_rule_13(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("audit_score",0.0)
        if ctx.flag("audit_blocked"): return -5.0
        if ctx.flag("audit_13_complete"): return 2.0
        if ctx.text("audit_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def audit_rule_14(self,ctx:ImportPipelineContext)->float:
        value=ctx.number("audit_score",0.0)
        if ctx.flag("audit_blocked"): return -5.0
        if ctx.flag("audit_14_complete"): return 3.0
        if ctx.text("audit_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def evaluate_many(self,records:Sequence[Mapping[str,object]])->list[ImportPipelineResult]:
        return [self.evaluate(record) for record in records]
    def summarize(self,results:Sequence[ImportPipelineResult])->dict[str,object]:
        scores=[item.score for item in results]
        return {"count":len(scores),"average":round(sum(scores)/len(scores),2) if scores else 0.0,"strong":sum(x.status=="strong" for x in results),"acceptable":sum(x.status=="acceptable" for x in results),"review":sum(x.status=="review" for x in results)}
