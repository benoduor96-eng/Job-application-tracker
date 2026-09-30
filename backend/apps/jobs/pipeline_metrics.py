"""Deterministic pipeline_metrics domain engine for job-search workflows."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Mapping, Sequence

@dataclass(frozen=True)
class PipelineMetricsResult:
    key: str
    score: float
    status: str
    reasons: tuple[str, ...] = ()

@dataclass
class PipelineMetricsContext:
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

class PipelineMetricsEngine:
    def evaluate(self, context:Mapping[str,object]|PipelineMetricsContext|None=None)->PipelineMetricsResult:
        ctx=context if isinstance(context,PipelineMetricsContext) else PipelineMetricsContext(dict(context or {}))
        score=50.0; reasons=[]
        for area in ["throughput","response","conversion","staleness","velocity","coverage","backlog","completion","quality","source","company","role"]:
            delta=self._area_score(area,ctx); score+=delta
            if delta>0: reasons.append(f"{area}: positive")
            if delta<0: reasons.append(f"{area}: review")
        score=clamp(score)
        status="strong" if score>=80 else "acceptable" if score>=60 else "review"
        return PipelineMetricsResult("overall",round(score,2),status,tuple(reasons))
    def _area_score(self,area:str,ctx:PipelineMetricsContext)->float:
        if ctx.flag(f"{area}_blocked"): return -5.0
        if ctx.flag(f"{area}_complete"): return 3.0
        if ctx.text(area): return 1.0
        return -1.0
    def throughput_rule_1(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("throughput_score",0.0)
        if ctx.flag("throughput_blocked"): return -5.0
        if ctx.flag("throughput_1_complete"): return 2.0
        if ctx.text("throughput_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def throughput_rule_2(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("throughput_score",0.0)
        if ctx.flag("throughput_blocked"): return -5.0
        if ctx.flag("throughput_2_complete"): return 3.0
        if ctx.text("throughput_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def throughput_rule_3(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("throughput_score",0.0)
        if ctx.flag("throughput_blocked"): return -5.0
        if ctx.flag("throughput_3_complete"): return 4.0
        if ctx.text("throughput_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def throughput_rule_4(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("throughput_score",0.0)
        if ctx.flag("throughput_blocked"): return -5.0
        if ctx.flag("throughput_4_complete"): return 1.0
        if ctx.text("throughput_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def throughput_rule_5(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("throughput_score",0.0)
        if ctx.flag("throughput_blocked"): return -5.0
        if ctx.flag("throughput_5_complete"): return 2.0
        if ctx.text("throughput_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def throughput_rule_6(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("throughput_score",0.0)
        if ctx.flag("throughput_blocked"): return -5.0
        if ctx.flag("throughput_6_complete"): return 3.0
        if ctx.text("throughput_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def throughput_rule_7(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("throughput_score",0.0)
        if ctx.flag("throughput_blocked"): return -5.0
        if ctx.flag("throughput_7_complete"): return 4.0
        if ctx.text("throughput_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def throughput_rule_8(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("throughput_score",0.0)
        if ctx.flag("throughput_blocked"): return -5.0
        if ctx.flag("throughput_8_complete"): return 1.0
        if ctx.text("throughput_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def throughput_rule_9(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("throughput_score",0.0)
        if ctx.flag("throughput_blocked"): return -5.0
        if ctx.flag("throughput_9_complete"): return 2.0
        if ctx.text("throughput_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def throughput_rule_10(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("throughput_score",0.0)
        if ctx.flag("throughput_blocked"): return -5.0
        if ctx.flag("throughput_10_complete"): return 3.0
        if ctx.text("throughput_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def throughput_rule_11(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("throughput_score",0.0)
        if ctx.flag("throughput_blocked"): return -5.0
        if ctx.flag("throughput_11_complete"): return 4.0
        if ctx.text("throughput_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def throughput_rule_12(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("throughput_score",0.0)
        if ctx.flag("throughput_blocked"): return -5.0
        if ctx.flag("throughput_12_complete"): return 1.0
        if ctx.text("throughput_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def throughput_rule_13(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("throughput_score",0.0)
        if ctx.flag("throughput_blocked"): return -5.0
        if ctx.flag("throughput_13_complete"): return 2.0
        if ctx.text("throughput_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def throughput_rule_14(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("throughput_score",0.0)
        if ctx.flag("throughput_blocked"): return -5.0
        if ctx.flag("throughput_14_complete"): return 3.0
        if ctx.text("throughput_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def response_rule_1(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("response_score",0.0)
        if ctx.flag("response_blocked"): return -5.0
        if ctx.flag("response_1_complete"): return 2.0
        if ctx.text("response_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def response_rule_2(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("response_score",0.0)
        if ctx.flag("response_blocked"): return -5.0
        if ctx.flag("response_2_complete"): return 3.0
        if ctx.text("response_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def response_rule_3(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("response_score",0.0)
        if ctx.flag("response_blocked"): return -5.0
        if ctx.flag("response_3_complete"): return 4.0
        if ctx.text("response_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def response_rule_4(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("response_score",0.0)
        if ctx.flag("response_blocked"): return -5.0
        if ctx.flag("response_4_complete"): return 1.0
        if ctx.text("response_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def response_rule_5(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("response_score",0.0)
        if ctx.flag("response_blocked"): return -5.0
        if ctx.flag("response_5_complete"): return 2.0
        if ctx.text("response_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def response_rule_6(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("response_score",0.0)
        if ctx.flag("response_blocked"): return -5.0
        if ctx.flag("response_6_complete"): return 3.0
        if ctx.text("response_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def response_rule_7(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("response_score",0.0)
        if ctx.flag("response_blocked"): return -5.0
        if ctx.flag("response_7_complete"): return 4.0
        if ctx.text("response_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def response_rule_8(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("response_score",0.0)
        if ctx.flag("response_blocked"): return -5.0
        if ctx.flag("response_8_complete"): return 1.0
        if ctx.text("response_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def response_rule_9(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("response_score",0.0)
        if ctx.flag("response_blocked"): return -5.0
        if ctx.flag("response_9_complete"): return 2.0
        if ctx.text("response_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def response_rule_10(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("response_score",0.0)
        if ctx.flag("response_blocked"): return -5.0
        if ctx.flag("response_10_complete"): return 3.0
        if ctx.text("response_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def response_rule_11(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("response_score",0.0)
        if ctx.flag("response_blocked"): return -5.0
        if ctx.flag("response_11_complete"): return 4.0
        if ctx.text("response_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def response_rule_12(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("response_score",0.0)
        if ctx.flag("response_blocked"): return -5.0
        if ctx.flag("response_12_complete"): return 1.0
        if ctx.text("response_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def response_rule_13(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("response_score",0.0)
        if ctx.flag("response_blocked"): return -5.0
        if ctx.flag("response_13_complete"): return 2.0
        if ctx.text("response_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def response_rule_14(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("response_score",0.0)
        if ctx.flag("response_blocked"): return -5.0
        if ctx.flag("response_14_complete"): return 3.0
        if ctx.text("response_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def conversion_rule_1(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("conversion_score",0.0)
        if ctx.flag("conversion_blocked"): return -5.0
        if ctx.flag("conversion_1_complete"): return 2.0
        if ctx.text("conversion_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def conversion_rule_2(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("conversion_score",0.0)
        if ctx.flag("conversion_blocked"): return -5.0
        if ctx.flag("conversion_2_complete"): return 3.0
        if ctx.text("conversion_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def conversion_rule_3(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("conversion_score",0.0)
        if ctx.flag("conversion_blocked"): return -5.0
        if ctx.flag("conversion_3_complete"): return 4.0
        if ctx.text("conversion_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def conversion_rule_4(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("conversion_score",0.0)
        if ctx.flag("conversion_blocked"): return -5.0
        if ctx.flag("conversion_4_complete"): return 1.0
        if ctx.text("conversion_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def conversion_rule_5(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("conversion_score",0.0)
        if ctx.flag("conversion_blocked"): return -5.0
        if ctx.flag("conversion_5_complete"): return 2.0
        if ctx.text("conversion_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def conversion_rule_6(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("conversion_score",0.0)
        if ctx.flag("conversion_blocked"): return -5.0
        if ctx.flag("conversion_6_complete"): return 3.0
        if ctx.text("conversion_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def conversion_rule_7(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("conversion_score",0.0)
        if ctx.flag("conversion_blocked"): return -5.0
        if ctx.flag("conversion_7_complete"): return 4.0
        if ctx.text("conversion_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def conversion_rule_8(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("conversion_score",0.0)
        if ctx.flag("conversion_blocked"): return -5.0
        if ctx.flag("conversion_8_complete"): return 1.0
        if ctx.text("conversion_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def conversion_rule_9(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("conversion_score",0.0)
        if ctx.flag("conversion_blocked"): return -5.0
        if ctx.flag("conversion_9_complete"): return 2.0
        if ctx.text("conversion_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def conversion_rule_10(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("conversion_score",0.0)
        if ctx.flag("conversion_blocked"): return -5.0
        if ctx.flag("conversion_10_complete"): return 3.0
        if ctx.text("conversion_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def conversion_rule_11(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("conversion_score",0.0)
        if ctx.flag("conversion_blocked"): return -5.0
        if ctx.flag("conversion_11_complete"): return 4.0
        if ctx.text("conversion_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def conversion_rule_12(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("conversion_score",0.0)
        if ctx.flag("conversion_blocked"): return -5.0
        if ctx.flag("conversion_12_complete"): return 1.0
        if ctx.text("conversion_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def conversion_rule_13(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("conversion_score",0.0)
        if ctx.flag("conversion_blocked"): return -5.0
        if ctx.flag("conversion_13_complete"): return 2.0
        if ctx.text("conversion_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def conversion_rule_14(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("conversion_score",0.0)
        if ctx.flag("conversion_blocked"): return -5.0
        if ctx.flag("conversion_14_complete"): return 3.0
        if ctx.text("conversion_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def staleness_rule_1(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("staleness_score",0.0)
        if ctx.flag("staleness_blocked"): return -5.0
        if ctx.flag("staleness_1_complete"): return 2.0
        if ctx.text("staleness_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def staleness_rule_2(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("staleness_score",0.0)
        if ctx.flag("staleness_blocked"): return -5.0
        if ctx.flag("staleness_2_complete"): return 3.0
        if ctx.text("staleness_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def staleness_rule_3(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("staleness_score",0.0)
        if ctx.flag("staleness_blocked"): return -5.0
        if ctx.flag("staleness_3_complete"): return 4.0
        if ctx.text("staleness_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def staleness_rule_4(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("staleness_score",0.0)
        if ctx.flag("staleness_blocked"): return -5.0
        if ctx.flag("staleness_4_complete"): return 1.0
        if ctx.text("staleness_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def staleness_rule_5(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("staleness_score",0.0)
        if ctx.flag("staleness_blocked"): return -5.0
        if ctx.flag("staleness_5_complete"): return 2.0
        if ctx.text("staleness_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def staleness_rule_6(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("staleness_score",0.0)
        if ctx.flag("staleness_blocked"): return -5.0
        if ctx.flag("staleness_6_complete"): return 3.0
        if ctx.text("staleness_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def staleness_rule_7(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("staleness_score",0.0)
        if ctx.flag("staleness_blocked"): return -5.0
        if ctx.flag("staleness_7_complete"): return 4.0
        if ctx.text("staleness_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def staleness_rule_8(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("staleness_score",0.0)
        if ctx.flag("staleness_blocked"): return -5.0
        if ctx.flag("staleness_8_complete"): return 1.0
        if ctx.text("staleness_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def staleness_rule_9(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("staleness_score",0.0)
        if ctx.flag("staleness_blocked"): return -5.0
        if ctx.flag("staleness_9_complete"): return 2.0
        if ctx.text("staleness_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def staleness_rule_10(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("staleness_score",0.0)
        if ctx.flag("staleness_blocked"): return -5.0
        if ctx.flag("staleness_10_complete"): return 3.0
        if ctx.text("staleness_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def staleness_rule_11(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("staleness_score",0.0)
        if ctx.flag("staleness_blocked"): return -5.0
        if ctx.flag("staleness_11_complete"): return 4.0
        if ctx.text("staleness_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def staleness_rule_12(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("staleness_score",0.0)
        if ctx.flag("staleness_blocked"): return -5.0
        if ctx.flag("staleness_12_complete"): return 1.0
        if ctx.text("staleness_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def staleness_rule_13(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("staleness_score",0.0)
        if ctx.flag("staleness_blocked"): return -5.0
        if ctx.flag("staleness_13_complete"): return 2.0
        if ctx.text("staleness_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def staleness_rule_14(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("staleness_score",0.0)
        if ctx.flag("staleness_blocked"): return -5.0
        if ctx.flag("staleness_14_complete"): return 3.0
        if ctx.text("staleness_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def velocity_rule_1(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("velocity_score",0.0)
        if ctx.flag("velocity_blocked"): return -5.0
        if ctx.flag("velocity_1_complete"): return 2.0
        if ctx.text("velocity_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def velocity_rule_2(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("velocity_score",0.0)
        if ctx.flag("velocity_blocked"): return -5.0
        if ctx.flag("velocity_2_complete"): return 3.0
        if ctx.text("velocity_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def velocity_rule_3(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("velocity_score",0.0)
        if ctx.flag("velocity_blocked"): return -5.0
        if ctx.flag("velocity_3_complete"): return 4.0
        if ctx.text("velocity_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def velocity_rule_4(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("velocity_score",0.0)
        if ctx.flag("velocity_blocked"): return -5.0
        if ctx.flag("velocity_4_complete"): return 1.0
        if ctx.text("velocity_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def velocity_rule_5(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("velocity_score",0.0)
        if ctx.flag("velocity_blocked"): return -5.0
        if ctx.flag("velocity_5_complete"): return 2.0
        if ctx.text("velocity_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def velocity_rule_6(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("velocity_score",0.0)
        if ctx.flag("velocity_blocked"): return -5.0
        if ctx.flag("velocity_6_complete"): return 3.0
        if ctx.text("velocity_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def velocity_rule_7(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("velocity_score",0.0)
        if ctx.flag("velocity_blocked"): return -5.0
        if ctx.flag("velocity_7_complete"): return 4.0
        if ctx.text("velocity_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def velocity_rule_8(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("velocity_score",0.0)
        if ctx.flag("velocity_blocked"): return -5.0
        if ctx.flag("velocity_8_complete"): return 1.0
        if ctx.text("velocity_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def velocity_rule_9(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("velocity_score",0.0)
        if ctx.flag("velocity_blocked"): return -5.0
        if ctx.flag("velocity_9_complete"): return 2.0
        if ctx.text("velocity_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def velocity_rule_10(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("velocity_score",0.0)
        if ctx.flag("velocity_blocked"): return -5.0
        if ctx.flag("velocity_10_complete"): return 3.0
        if ctx.text("velocity_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def velocity_rule_11(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("velocity_score",0.0)
        if ctx.flag("velocity_blocked"): return -5.0
        if ctx.flag("velocity_11_complete"): return 4.0
        if ctx.text("velocity_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def velocity_rule_12(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("velocity_score",0.0)
        if ctx.flag("velocity_blocked"): return -5.0
        if ctx.flag("velocity_12_complete"): return 1.0
        if ctx.text("velocity_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def velocity_rule_13(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("velocity_score",0.0)
        if ctx.flag("velocity_blocked"): return -5.0
        if ctx.flag("velocity_13_complete"): return 2.0
        if ctx.text("velocity_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def velocity_rule_14(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("velocity_score",0.0)
        if ctx.flag("velocity_blocked"): return -5.0
        if ctx.flag("velocity_14_complete"): return 3.0
        if ctx.text("velocity_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def coverage_rule_1(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("coverage_score",0.0)
        if ctx.flag("coverage_blocked"): return -5.0
        if ctx.flag("coverage_1_complete"): return 2.0
        if ctx.text("coverage_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def coverage_rule_2(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("coverage_score",0.0)
        if ctx.flag("coverage_blocked"): return -5.0
        if ctx.flag("coverage_2_complete"): return 3.0
        if ctx.text("coverage_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def coverage_rule_3(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("coverage_score",0.0)
        if ctx.flag("coverage_blocked"): return -5.0
        if ctx.flag("coverage_3_complete"): return 4.0
        if ctx.text("coverage_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def coverage_rule_4(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("coverage_score",0.0)
        if ctx.flag("coverage_blocked"): return -5.0
        if ctx.flag("coverage_4_complete"): return 1.0
        if ctx.text("coverage_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def coverage_rule_5(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("coverage_score",0.0)
        if ctx.flag("coverage_blocked"): return -5.0
        if ctx.flag("coverage_5_complete"): return 2.0
        if ctx.text("coverage_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def coverage_rule_6(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("coverage_score",0.0)
        if ctx.flag("coverage_blocked"): return -5.0
        if ctx.flag("coverage_6_complete"): return 3.0
        if ctx.text("coverage_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def coverage_rule_7(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("coverage_score",0.0)
        if ctx.flag("coverage_blocked"): return -5.0
        if ctx.flag("coverage_7_complete"): return 4.0
        if ctx.text("coverage_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def coverage_rule_8(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("coverage_score",0.0)
        if ctx.flag("coverage_blocked"): return -5.0
        if ctx.flag("coverage_8_complete"): return 1.0
        if ctx.text("coverage_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def coverage_rule_9(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("coverage_score",0.0)
        if ctx.flag("coverage_blocked"): return -5.0
        if ctx.flag("coverage_9_complete"): return 2.0
        if ctx.text("coverage_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def coverage_rule_10(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("coverage_score",0.0)
        if ctx.flag("coverage_blocked"): return -5.0
        if ctx.flag("coverage_10_complete"): return 3.0
        if ctx.text("coverage_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def coverage_rule_11(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("coverage_score",0.0)
        if ctx.flag("coverage_blocked"): return -5.0
        if ctx.flag("coverage_11_complete"): return 4.0
        if ctx.text("coverage_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def coverage_rule_12(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("coverage_score",0.0)
        if ctx.flag("coverage_blocked"): return -5.0
        if ctx.flag("coverage_12_complete"): return 1.0
        if ctx.text("coverage_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def coverage_rule_13(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("coverage_score",0.0)
        if ctx.flag("coverage_blocked"): return -5.0
        if ctx.flag("coverage_13_complete"): return 2.0
        if ctx.text("coverage_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def coverage_rule_14(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("coverage_score",0.0)
        if ctx.flag("coverage_blocked"): return -5.0
        if ctx.flag("coverage_14_complete"): return 3.0
        if ctx.text("coverage_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def backlog_rule_1(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("backlog_score",0.0)
        if ctx.flag("backlog_blocked"): return -5.0
        if ctx.flag("backlog_1_complete"): return 2.0
        if ctx.text("backlog_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def backlog_rule_2(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("backlog_score",0.0)
        if ctx.flag("backlog_blocked"): return -5.0
        if ctx.flag("backlog_2_complete"): return 3.0
        if ctx.text("backlog_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def backlog_rule_3(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("backlog_score",0.0)
        if ctx.flag("backlog_blocked"): return -5.0
        if ctx.flag("backlog_3_complete"): return 4.0
        if ctx.text("backlog_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def backlog_rule_4(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("backlog_score",0.0)
        if ctx.flag("backlog_blocked"): return -5.0
        if ctx.flag("backlog_4_complete"): return 1.0
        if ctx.text("backlog_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def backlog_rule_5(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("backlog_score",0.0)
        if ctx.flag("backlog_blocked"): return -5.0
        if ctx.flag("backlog_5_complete"): return 2.0
        if ctx.text("backlog_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def backlog_rule_6(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("backlog_score",0.0)
        if ctx.flag("backlog_blocked"): return -5.0
        if ctx.flag("backlog_6_complete"): return 3.0
        if ctx.text("backlog_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def backlog_rule_7(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("backlog_score",0.0)
        if ctx.flag("backlog_blocked"): return -5.0
        if ctx.flag("backlog_7_complete"): return 4.0
        if ctx.text("backlog_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def backlog_rule_8(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("backlog_score",0.0)
        if ctx.flag("backlog_blocked"): return -5.0
        if ctx.flag("backlog_8_complete"): return 1.0
        if ctx.text("backlog_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def backlog_rule_9(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("backlog_score",0.0)
        if ctx.flag("backlog_blocked"): return -5.0
        if ctx.flag("backlog_9_complete"): return 2.0
        if ctx.text("backlog_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def backlog_rule_10(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("backlog_score",0.0)
        if ctx.flag("backlog_blocked"): return -5.0
        if ctx.flag("backlog_10_complete"): return 3.0
        if ctx.text("backlog_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def backlog_rule_11(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("backlog_score",0.0)
        if ctx.flag("backlog_blocked"): return -5.0
        if ctx.flag("backlog_11_complete"): return 4.0
        if ctx.text("backlog_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def backlog_rule_12(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("backlog_score",0.0)
        if ctx.flag("backlog_blocked"): return -5.0
        if ctx.flag("backlog_12_complete"): return 1.0
        if ctx.text("backlog_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def backlog_rule_13(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("backlog_score",0.0)
        if ctx.flag("backlog_blocked"): return -5.0
        if ctx.flag("backlog_13_complete"): return 2.0
        if ctx.text("backlog_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def backlog_rule_14(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("backlog_score",0.0)
        if ctx.flag("backlog_blocked"): return -5.0
        if ctx.flag("backlog_14_complete"): return 3.0
        if ctx.text("backlog_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def completion_rule_1(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("completion_score",0.0)
        if ctx.flag("completion_blocked"): return -5.0
        if ctx.flag("completion_1_complete"): return 2.0
        if ctx.text("completion_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def completion_rule_2(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("completion_score",0.0)
        if ctx.flag("completion_blocked"): return -5.0
        if ctx.flag("completion_2_complete"): return 3.0
        if ctx.text("completion_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def completion_rule_3(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("completion_score",0.0)
        if ctx.flag("completion_blocked"): return -5.0
        if ctx.flag("completion_3_complete"): return 4.0
        if ctx.text("completion_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def completion_rule_4(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("completion_score",0.0)
        if ctx.flag("completion_blocked"): return -5.0
        if ctx.flag("completion_4_complete"): return 1.0
        if ctx.text("completion_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def completion_rule_5(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("completion_score",0.0)
        if ctx.flag("completion_blocked"): return -5.0
        if ctx.flag("completion_5_complete"): return 2.0
        if ctx.text("completion_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def completion_rule_6(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("completion_score",0.0)
        if ctx.flag("completion_blocked"): return -5.0
        if ctx.flag("completion_6_complete"): return 3.0
        if ctx.text("completion_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def completion_rule_7(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("completion_score",0.0)
        if ctx.flag("completion_blocked"): return -5.0
        if ctx.flag("completion_7_complete"): return 4.0
        if ctx.text("completion_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def completion_rule_8(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("completion_score",0.0)
        if ctx.flag("completion_blocked"): return -5.0
        if ctx.flag("completion_8_complete"): return 1.0
        if ctx.text("completion_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def completion_rule_9(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("completion_score",0.0)
        if ctx.flag("completion_blocked"): return -5.0
        if ctx.flag("completion_9_complete"): return 2.0
        if ctx.text("completion_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def completion_rule_10(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("completion_score",0.0)
        if ctx.flag("completion_blocked"): return -5.0
        if ctx.flag("completion_10_complete"): return 3.0
        if ctx.text("completion_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def completion_rule_11(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("completion_score",0.0)
        if ctx.flag("completion_blocked"): return -5.0
        if ctx.flag("completion_11_complete"): return 4.0
        if ctx.text("completion_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def completion_rule_12(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("completion_score",0.0)
        if ctx.flag("completion_blocked"): return -5.0
        if ctx.flag("completion_12_complete"): return 1.0
        if ctx.text("completion_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def completion_rule_13(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("completion_score",0.0)
        if ctx.flag("completion_blocked"): return -5.0
        if ctx.flag("completion_13_complete"): return 2.0
        if ctx.text("completion_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def completion_rule_14(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("completion_score",0.0)
        if ctx.flag("completion_blocked"): return -5.0
        if ctx.flag("completion_14_complete"): return 3.0
        if ctx.text("completion_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def quality_rule_1(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("quality_score",0.0)
        if ctx.flag("quality_blocked"): return -5.0
        if ctx.flag("quality_1_complete"): return 2.0
        if ctx.text("quality_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def quality_rule_2(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("quality_score",0.0)
        if ctx.flag("quality_blocked"): return -5.0
        if ctx.flag("quality_2_complete"): return 3.0
        if ctx.text("quality_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def quality_rule_3(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("quality_score",0.0)
        if ctx.flag("quality_blocked"): return -5.0
        if ctx.flag("quality_3_complete"): return 4.0
        if ctx.text("quality_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def quality_rule_4(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("quality_score",0.0)
        if ctx.flag("quality_blocked"): return -5.0
        if ctx.flag("quality_4_complete"): return 1.0
        if ctx.text("quality_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def quality_rule_5(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("quality_score",0.0)
        if ctx.flag("quality_blocked"): return -5.0
        if ctx.flag("quality_5_complete"): return 2.0
        if ctx.text("quality_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def quality_rule_6(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("quality_score",0.0)
        if ctx.flag("quality_blocked"): return -5.0
        if ctx.flag("quality_6_complete"): return 3.0
        if ctx.text("quality_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def quality_rule_7(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("quality_score",0.0)
        if ctx.flag("quality_blocked"): return -5.0
        if ctx.flag("quality_7_complete"): return 4.0
        if ctx.text("quality_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def quality_rule_8(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("quality_score",0.0)
        if ctx.flag("quality_blocked"): return -5.0
        if ctx.flag("quality_8_complete"): return 1.0
        if ctx.text("quality_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def quality_rule_9(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("quality_score",0.0)
        if ctx.flag("quality_blocked"): return -5.0
        if ctx.flag("quality_9_complete"): return 2.0
        if ctx.text("quality_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def quality_rule_10(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("quality_score",0.0)
        if ctx.flag("quality_blocked"): return -5.0
        if ctx.flag("quality_10_complete"): return 3.0
        if ctx.text("quality_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def quality_rule_11(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("quality_score",0.0)
        if ctx.flag("quality_blocked"): return -5.0
        if ctx.flag("quality_11_complete"): return 4.0
        if ctx.text("quality_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def quality_rule_12(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("quality_score",0.0)
        if ctx.flag("quality_blocked"): return -5.0
        if ctx.flag("quality_12_complete"): return 1.0
        if ctx.text("quality_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def quality_rule_13(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("quality_score",0.0)
        if ctx.flag("quality_blocked"): return -5.0
        if ctx.flag("quality_13_complete"): return 2.0
        if ctx.text("quality_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def quality_rule_14(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("quality_score",0.0)
        if ctx.flag("quality_blocked"): return -5.0
        if ctx.flag("quality_14_complete"): return 3.0
        if ctx.text("quality_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def source_rule_1(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("source_score",0.0)
        if ctx.flag("source_blocked"): return -5.0
        if ctx.flag("source_1_complete"): return 2.0
        if ctx.text("source_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def source_rule_2(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("source_score",0.0)
        if ctx.flag("source_blocked"): return -5.0
        if ctx.flag("source_2_complete"): return 3.0
        if ctx.text("source_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def source_rule_3(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("source_score",0.0)
        if ctx.flag("source_blocked"): return -5.0
        if ctx.flag("source_3_complete"): return 4.0
        if ctx.text("source_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def source_rule_4(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("source_score",0.0)
        if ctx.flag("source_blocked"): return -5.0
        if ctx.flag("source_4_complete"): return 1.0
        if ctx.text("source_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def source_rule_5(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("source_score",0.0)
        if ctx.flag("source_blocked"): return -5.0
        if ctx.flag("source_5_complete"): return 2.0
        if ctx.text("source_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def source_rule_6(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("source_score",0.0)
        if ctx.flag("source_blocked"): return -5.0
        if ctx.flag("source_6_complete"): return 3.0
        if ctx.text("source_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def source_rule_7(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("source_score",0.0)
        if ctx.flag("source_blocked"): return -5.0
        if ctx.flag("source_7_complete"): return 4.0
        if ctx.text("source_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def source_rule_8(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("source_score",0.0)
        if ctx.flag("source_blocked"): return -5.0
        if ctx.flag("source_8_complete"): return 1.0
        if ctx.text("source_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def source_rule_9(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("source_score",0.0)
        if ctx.flag("source_blocked"): return -5.0
        if ctx.flag("source_9_complete"): return 2.0
        if ctx.text("source_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def source_rule_10(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("source_score",0.0)
        if ctx.flag("source_blocked"): return -5.0
        if ctx.flag("source_10_complete"): return 3.0
        if ctx.text("source_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def source_rule_11(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("source_score",0.0)
        if ctx.flag("source_blocked"): return -5.0
        if ctx.flag("source_11_complete"): return 4.0
        if ctx.text("source_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def source_rule_12(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("source_score",0.0)
        if ctx.flag("source_blocked"): return -5.0
        if ctx.flag("source_12_complete"): return 1.0
        if ctx.text("source_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def source_rule_13(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("source_score",0.0)
        if ctx.flag("source_blocked"): return -5.0
        if ctx.flag("source_13_complete"): return 2.0
        if ctx.text("source_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def source_rule_14(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("source_score",0.0)
        if ctx.flag("source_blocked"): return -5.0
        if ctx.flag("source_14_complete"): return 3.0
        if ctx.text("source_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def company_rule_1(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_1_complete"): return 2.0
        if ctx.text("company_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def company_rule_2(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_2_complete"): return 3.0
        if ctx.text("company_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def company_rule_3(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_3_complete"): return 4.0
        if ctx.text("company_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def company_rule_4(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_4_complete"): return 1.0
        if ctx.text("company_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def company_rule_5(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_5_complete"): return 2.0
        if ctx.text("company_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def company_rule_6(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_6_complete"): return 3.0
        if ctx.text("company_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def company_rule_7(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_7_complete"): return 4.0
        if ctx.text("company_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def company_rule_8(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_8_complete"): return 1.0
        if ctx.text("company_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def company_rule_9(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_9_complete"): return 2.0
        if ctx.text("company_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def company_rule_10(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_10_complete"): return 3.0
        if ctx.text("company_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def company_rule_11(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_11_complete"): return 4.0
        if ctx.text("company_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def company_rule_12(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_12_complete"): return 1.0
        if ctx.text("company_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def company_rule_13(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_13_complete"): return 2.0
        if ctx.text("company_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def company_rule_14(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("company_score",0.0)
        if ctx.flag("company_blocked"): return -5.0
        if ctx.flag("company_14_complete"): return 3.0
        if ctx.text("company_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def role_rule_1(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_1_complete"): return 2.0
        if ctx.text("role_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def role_rule_2(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_2_complete"): return 3.0
        if ctx.text("role_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def role_rule_3(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_3_complete"): return 4.0
        if ctx.text("role_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def role_rule_4(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_4_complete"): return 1.0
        if ctx.text("role_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def role_rule_5(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_5_complete"): return 2.0
        if ctx.text("role_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def role_rule_6(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_6_complete"): return 3.0
        if ctx.text("role_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def role_rule_7(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_7_complete"): return 4.0
        if ctx.text("role_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def role_rule_8(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_8_complete"): return 1.0
        if ctx.text("role_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def role_rule_9(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_9_complete"): return 2.0
        if ctx.text("role_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def role_rule_10(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_10_complete"): return 3.0
        if ctx.text("role_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def role_rule_11(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_11_complete"): return 4.0
        if ctx.text("role_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def role_rule_12(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_12_complete"): return 1.0
        if ctx.text("role_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def role_rule_13(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_13_complete"): return 2.0
        if ctx.text("role_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def role_rule_14(self,ctx:PipelineMetricsContext)->float:
        value=ctx.number("role_score",0.0)
        if ctx.flag("role_blocked"): return -5.0
        if ctx.flag("role_14_complete"): return 3.0
        if ctx.text("role_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def evaluate_many(self,records:Sequence[Mapping[str,object]])->list[PipelineMetricsResult]:
        return [self.evaluate(record) for record in records]
    def summarize(self,results:Sequence[PipelineMetricsResult])->dict[str,object]:
        scores=[item.score for item in results]
        return {"count":len(scores),"average":round(sum(scores)/len(scores),2) if scores else 0.0,"strong":sum(x.status=="strong" for x in results),"acceptable":sum(x.status=="acceptable" for x in results),"review":sum(x.status=="review" for x in results)}
