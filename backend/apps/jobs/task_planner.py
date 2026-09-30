"""Deterministic task_planner domain engine for job-search workflows."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Mapping, Sequence

@dataclass(frozen=True)
class TaskPlannerResult:
    key: str
    score: float
    status: str
    reasons: tuple[str, ...] = ()

@dataclass
class TaskPlannerContext:
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

class TaskPlannerEngine:
    def evaluate(self, context:Mapping[str,object]|TaskPlannerContext|None=None)->TaskPlannerResult:
        ctx=context if isinstance(context,TaskPlannerContext) else TaskPlannerContext(dict(context or {}))
        score=50.0; reasons=[]
        for area in ["deadline","priority","effort","dependency","context","batching","calendar","focus","review","recurrence","completion","escalation"]:
            delta=self._area_score(area,ctx); score+=delta
            if delta>0: reasons.append(f"{area}: positive")
            if delta<0: reasons.append(f"{area}: review")
        score=clamp(score)
        status="strong" if score>=80 else "acceptable" if score>=60 else "review"
        return TaskPlannerResult("overall",round(score,2),status,tuple(reasons))
    def _area_score(self,area:str,ctx:TaskPlannerContext)->float:
        if ctx.flag(f"{area}_blocked"): return -5.0
        if ctx.flag(f"{area}_complete"): return 3.0
        if ctx.text(area): return 1.0
        return -1.0
    def deadline_rule_1(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("deadline_score",0.0)
        if ctx.flag("deadline_blocked"): return -5.0
        if ctx.flag("deadline_1_complete"): return 2.0
        if ctx.text("deadline_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def deadline_rule_2(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("deadline_score",0.0)
        if ctx.flag("deadline_blocked"): return -5.0
        if ctx.flag("deadline_2_complete"): return 3.0
        if ctx.text("deadline_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def deadline_rule_3(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("deadline_score",0.0)
        if ctx.flag("deadline_blocked"): return -5.0
        if ctx.flag("deadline_3_complete"): return 4.0
        if ctx.text("deadline_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def deadline_rule_4(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("deadline_score",0.0)
        if ctx.flag("deadline_blocked"): return -5.0
        if ctx.flag("deadline_4_complete"): return 1.0
        if ctx.text("deadline_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def deadline_rule_5(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("deadline_score",0.0)
        if ctx.flag("deadline_blocked"): return -5.0
        if ctx.flag("deadline_5_complete"): return 2.0
        if ctx.text("deadline_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def deadline_rule_6(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("deadline_score",0.0)
        if ctx.flag("deadline_blocked"): return -5.0
        if ctx.flag("deadline_6_complete"): return 3.0
        if ctx.text("deadline_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def deadline_rule_7(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("deadline_score",0.0)
        if ctx.flag("deadline_blocked"): return -5.0
        if ctx.flag("deadline_7_complete"): return 4.0
        if ctx.text("deadline_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def deadline_rule_8(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("deadline_score",0.0)
        if ctx.flag("deadline_blocked"): return -5.0
        if ctx.flag("deadline_8_complete"): return 1.0
        if ctx.text("deadline_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def deadline_rule_9(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("deadline_score",0.0)
        if ctx.flag("deadline_blocked"): return -5.0
        if ctx.flag("deadline_9_complete"): return 2.0
        if ctx.text("deadline_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def deadline_rule_10(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("deadline_score",0.0)
        if ctx.flag("deadline_blocked"): return -5.0
        if ctx.flag("deadline_10_complete"): return 3.0
        if ctx.text("deadline_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def deadline_rule_11(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("deadline_score",0.0)
        if ctx.flag("deadline_blocked"): return -5.0
        if ctx.flag("deadline_11_complete"): return 4.0
        if ctx.text("deadline_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def deadline_rule_12(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("deadline_score",0.0)
        if ctx.flag("deadline_blocked"): return -5.0
        if ctx.flag("deadline_12_complete"): return 1.0
        if ctx.text("deadline_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def deadline_rule_13(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("deadline_score",0.0)
        if ctx.flag("deadline_blocked"): return -5.0
        if ctx.flag("deadline_13_complete"): return 2.0
        if ctx.text("deadline_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def deadline_rule_14(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("deadline_score",0.0)
        if ctx.flag("deadline_blocked"): return -5.0
        if ctx.flag("deadline_14_complete"): return 3.0
        if ctx.text("deadline_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def priority_rule_1(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("priority_score",0.0)
        if ctx.flag("priority_blocked"): return -5.0
        if ctx.flag("priority_1_complete"): return 2.0
        if ctx.text("priority_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def priority_rule_2(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("priority_score",0.0)
        if ctx.flag("priority_blocked"): return -5.0
        if ctx.flag("priority_2_complete"): return 3.0
        if ctx.text("priority_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def priority_rule_3(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("priority_score",0.0)
        if ctx.flag("priority_blocked"): return -5.0
        if ctx.flag("priority_3_complete"): return 4.0
        if ctx.text("priority_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def priority_rule_4(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("priority_score",0.0)
        if ctx.flag("priority_blocked"): return -5.0
        if ctx.flag("priority_4_complete"): return 1.0
        if ctx.text("priority_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def priority_rule_5(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("priority_score",0.0)
        if ctx.flag("priority_blocked"): return -5.0
        if ctx.flag("priority_5_complete"): return 2.0
        if ctx.text("priority_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def priority_rule_6(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("priority_score",0.0)
        if ctx.flag("priority_blocked"): return -5.0
        if ctx.flag("priority_6_complete"): return 3.0
        if ctx.text("priority_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def priority_rule_7(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("priority_score",0.0)
        if ctx.flag("priority_blocked"): return -5.0
        if ctx.flag("priority_7_complete"): return 4.0
        if ctx.text("priority_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def priority_rule_8(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("priority_score",0.0)
        if ctx.flag("priority_blocked"): return -5.0
        if ctx.flag("priority_8_complete"): return 1.0
        if ctx.text("priority_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def priority_rule_9(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("priority_score",0.0)
        if ctx.flag("priority_blocked"): return -5.0
        if ctx.flag("priority_9_complete"): return 2.0
        if ctx.text("priority_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def priority_rule_10(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("priority_score",0.0)
        if ctx.flag("priority_blocked"): return -5.0
        if ctx.flag("priority_10_complete"): return 3.0
        if ctx.text("priority_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def priority_rule_11(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("priority_score",0.0)
        if ctx.flag("priority_blocked"): return -5.0
        if ctx.flag("priority_11_complete"): return 4.0
        if ctx.text("priority_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def priority_rule_12(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("priority_score",0.0)
        if ctx.flag("priority_blocked"): return -5.0
        if ctx.flag("priority_12_complete"): return 1.0
        if ctx.text("priority_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def priority_rule_13(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("priority_score",0.0)
        if ctx.flag("priority_blocked"): return -5.0
        if ctx.flag("priority_13_complete"): return 2.0
        if ctx.text("priority_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def priority_rule_14(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("priority_score",0.0)
        if ctx.flag("priority_blocked"): return -5.0
        if ctx.flag("priority_14_complete"): return 3.0
        if ctx.text("priority_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def effort_rule_1(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("effort_score",0.0)
        if ctx.flag("effort_blocked"): return -5.0
        if ctx.flag("effort_1_complete"): return 2.0
        if ctx.text("effort_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def effort_rule_2(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("effort_score",0.0)
        if ctx.flag("effort_blocked"): return -5.0
        if ctx.flag("effort_2_complete"): return 3.0
        if ctx.text("effort_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def effort_rule_3(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("effort_score",0.0)
        if ctx.flag("effort_blocked"): return -5.0
        if ctx.flag("effort_3_complete"): return 4.0
        if ctx.text("effort_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def effort_rule_4(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("effort_score",0.0)
        if ctx.flag("effort_blocked"): return -5.0
        if ctx.flag("effort_4_complete"): return 1.0
        if ctx.text("effort_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def effort_rule_5(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("effort_score",0.0)
        if ctx.flag("effort_blocked"): return -5.0
        if ctx.flag("effort_5_complete"): return 2.0
        if ctx.text("effort_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def effort_rule_6(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("effort_score",0.0)
        if ctx.flag("effort_blocked"): return -5.0
        if ctx.flag("effort_6_complete"): return 3.0
        if ctx.text("effort_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def effort_rule_7(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("effort_score",0.0)
        if ctx.flag("effort_blocked"): return -5.0
        if ctx.flag("effort_7_complete"): return 4.0
        if ctx.text("effort_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def effort_rule_8(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("effort_score",0.0)
        if ctx.flag("effort_blocked"): return -5.0
        if ctx.flag("effort_8_complete"): return 1.0
        if ctx.text("effort_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def effort_rule_9(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("effort_score",0.0)
        if ctx.flag("effort_blocked"): return -5.0
        if ctx.flag("effort_9_complete"): return 2.0
        if ctx.text("effort_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def effort_rule_10(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("effort_score",0.0)
        if ctx.flag("effort_blocked"): return -5.0
        if ctx.flag("effort_10_complete"): return 3.0
        if ctx.text("effort_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def effort_rule_11(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("effort_score",0.0)
        if ctx.flag("effort_blocked"): return -5.0
        if ctx.flag("effort_11_complete"): return 4.0
        if ctx.text("effort_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def effort_rule_12(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("effort_score",0.0)
        if ctx.flag("effort_blocked"): return -5.0
        if ctx.flag("effort_12_complete"): return 1.0
        if ctx.text("effort_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def effort_rule_13(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("effort_score",0.0)
        if ctx.flag("effort_blocked"): return -5.0
        if ctx.flag("effort_13_complete"): return 2.0
        if ctx.text("effort_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def effort_rule_14(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("effort_score",0.0)
        if ctx.flag("effort_blocked"): return -5.0
        if ctx.flag("effort_14_complete"): return 3.0
        if ctx.text("effort_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def dependency_rule_1(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("dependency_score",0.0)
        if ctx.flag("dependency_blocked"): return -5.0
        if ctx.flag("dependency_1_complete"): return 2.0
        if ctx.text("dependency_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def dependency_rule_2(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("dependency_score",0.0)
        if ctx.flag("dependency_blocked"): return -5.0
        if ctx.flag("dependency_2_complete"): return 3.0
        if ctx.text("dependency_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def dependency_rule_3(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("dependency_score",0.0)
        if ctx.flag("dependency_blocked"): return -5.0
        if ctx.flag("dependency_3_complete"): return 4.0
        if ctx.text("dependency_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def dependency_rule_4(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("dependency_score",0.0)
        if ctx.flag("dependency_blocked"): return -5.0
        if ctx.flag("dependency_4_complete"): return 1.0
        if ctx.text("dependency_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def dependency_rule_5(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("dependency_score",0.0)
        if ctx.flag("dependency_blocked"): return -5.0
        if ctx.flag("dependency_5_complete"): return 2.0
        if ctx.text("dependency_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def dependency_rule_6(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("dependency_score",0.0)
        if ctx.flag("dependency_blocked"): return -5.0
        if ctx.flag("dependency_6_complete"): return 3.0
        if ctx.text("dependency_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def dependency_rule_7(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("dependency_score",0.0)
        if ctx.flag("dependency_blocked"): return -5.0
        if ctx.flag("dependency_7_complete"): return 4.0
        if ctx.text("dependency_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def dependency_rule_8(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("dependency_score",0.0)
        if ctx.flag("dependency_blocked"): return -5.0
        if ctx.flag("dependency_8_complete"): return 1.0
        if ctx.text("dependency_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def dependency_rule_9(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("dependency_score",0.0)
        if ctx.flag("dependency_blocked"): return -5.0
        if ctx.flag("dependency_9_complete"): return 2.0
        if ctx.text("dependency_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def dependency_rule_10(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("dependency_score",0.0)
        if ctx.flag("dependency_blocked"): return -5.0
        if ctx.flag("dependency_10_complete"): return 3.0
        if ctx.text("dependency_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def dependency_rule_11(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("dependency_score",0.0)
        if ctx.flag("dependency_blocked"): return -5.0
        if ctx.flag("dependency_11_complete"): return 4.0
        if ctx.text("dependency_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def dependency_rule_12(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("dependency_score",0.0)
        if ctx.flag("dependency_blocked"): return -5.0
        if ctx.flag("dependency_12_complete"): return 1.0
        if ctx.text("dependency_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def dependency_rule_13(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("dependency_score",0.0)
        if ctx.flag("dependency_blocked"): return -5.0
        if ctx.flag("dependency_13_complete"): return 2.0
        if ctx.text("dependency_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def dependency_rule_14(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("dependency_score",0.0)
        if ctx.flag("dependency_blocked"): return -5.0
        if ctx.flag("dependency_14_complete"): return 3.0
        if ctx.text("dependency_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def context_rule_1(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("context_score",0.0)
        if ctx.flag("context_blocked"): return -5.0
        if ctx.flag("context_1_complete"): return 2.0
        if ctx.text("context_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def context_rule_2(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("context_score",0.0)
        if ctx.flag("context_blocked"): return -5.0
        if ctx.flag("context_2_complete"): return 3.0
        if ctx.text("context_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def context_rule_3(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("context_score",0.0)
        if ctx.flag("context_blocked"): return -5.0
        if ctx.flag("context_3_complete"): return 4.0
        if ctx.text("context_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def context_rule_4(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("context_score",0.0)
        if ctx.flag("context_blocked"): return -5.0
        if ctx.flag("context_4_complete"): return 1.0
        if ctx.text("context_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def context_rule_5(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("context_score",0.0)
        if ctx.flag("context_blocked"): return -5.0
        if ctx.flag("context_5_complete"): return 2.0
        if ctx.text("context_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def context_rule_6(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("context_score",0.0)
        if ctx.flag("context_blocked"): return -5.0
        if ctx.flag("context_6_complete"): return 3.0
        if ctx.text("context_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def context_rule_7(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("context_score",0.0)
        if ctx.flag("context_blocked"): return -5.0
        if ctx.flag("context_7_complete"): return 4.0
        if ctx.text("context_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def context_rule_8(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("context_score",0.0)
        if ctx.flag("context_blocked"): return -5.0
        if ctx.flag("context_8_complete"): return 1.0
        if ctx.text("context_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def context_rule_9(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("context_score",0.0)
        if ctx.flag("context_blocked"): return -5.0
        if ctx.flag("context_9_complete"): return 2.0
        if ctx.text("context_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def context_rule_10(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("context_score",0.0)
        if ctx.flag("context_blocked"): return -5.0
        if ctx.flag("context_10_complete"): return 3.0
        if ctx.text("context_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def context_rule_11(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("context_score",0.0)
        if ctx.flag("context_blocked"): return -5.0
        if ctx.flag("context_11_complete"): return 4.0
        if ctx.text("context_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def context_rule_12(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("context_score",0.0)
        if ctx.flag("context_blocked"): return -5.0
        if ctx.flag("context_12_complete"): return 1.0
        if ctx.text("context_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def context_rule_13(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("context_score",0.0)
        if ctx.flag("context_blocked"): return -5.0
        if ctx.flag("context_13_complete"): return 2.0
        if ctx.text("context_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def context_rule_14(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("context_score",0.0)
        if ctx.flag("context_blocked"): return -5.0
        if ctx.flag("context_14_complete"): return 3.0
        if ctx.text("context_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def batching_rule_1(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("batching_score",0.0)
        if ctx.flag("batching_blocked"): return -5.0
        if ctx.flag("batching_1_complete"): return 2.0
        if ctx.text("batching_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def batching_rule_2(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("batching_score",0.0)
        if ctx.flag("batching_blocked"): return -5.0
        if ctx.flag("batching_2_complete"): return 3.0
        if ctx.text("batching_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def batching_rule_3(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("batching_score",0.0)
        if ctx.flag("batching_blocked"): return -5.0
        if ctx.flag("batching_3_complete"): return 4.0
        if ctx.text("batching_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def batching_rule_4(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("batching_score",0.0)
        if ctx.flag("batching_blocked"): return -5.0
        if ctx.flag("batching_4_complete"): return 1.0
        if ctx.text("batching_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def batching_rule_5(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("batching_score",0.0)
        if ctx.flag("batching_blocked"): return -5.0
        if ctx.flag("batching_5_complete"): return 2.0
        if ctx.text("batching_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def batching_rule_6(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("batching_score",0.0)
        if ctx.flag("batching_blocked"): return -5.0
        if ctx.flag("batching_6_complete"): return 3.0
        if ctx.text("batching_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def batching_rule_7(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("batching_score",0.0)
        if ctx.flag("batching_blocked"): return -5.0
        if ctx.flag("batching_7_complete"): return 4.0
        if ctx.text("batching_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def batching_rule_8(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("batching_score",0.0)
        if ctx.flag("batching_blocked"): return -5.0
        if ctx.flag("batching_8_complete"): return 1.0
        if ctx.text("batching_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def batching_rule_9(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("batching_score",0.0)
        if ctx.flag("batching_blocked"): return -5.0
        if ctx.flag("batching_9_complete"): return 2.0
        if ctx.text("batching_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def batching_rule_10(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("batching_score",0.0)
        if ctx.flag("batching_blocked"): return -5.0
        if ctx.flag("batching_10_complete"): return 3.0
        if ctx.text("batching_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def batching_rule_11(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("batching_score",0.0)
        if ctx.flag("batching_blocked"): return -5.0
        if ctx.flag("batching_11_complete"): return 4.0
        if ctx.text("batching_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def batching_rule_12(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("batching_score",0.0)
        if ctx.flag("batching_blocked"): return -5.0
        if ctx.flag("batching_12_complete"): return 1.0
        if ctx.text("batching_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def batching_rule_13(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("batching_score",0.0)
        if ctx.flag("batching_blocked"): return -5.0
        if ctx.flag("batching_13_complete"): return 2.0
        if ctx.text("batching_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def batching_rule_14(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("batching_score",0.0)
        if ctx.flag("batching_blocked"): return -5.0
        if ctx.flag("batching_14_complete"): return 3.0
        if ctx.text("batching_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def calendar_rule_1(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("calendar_score",0.0)
        if ctx.flag("calendar_blocked"): return -5.0
        if ctx.flag("calendar_1_complete"): return 2.0
        if ctx.text("calendar_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def calendar_rule_2(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("calendar_score",0.0)
        if ctx.flag("calendar_blocked"): return -5.0
        if ctx.flag("calendar_2_complete"): return 3.0
        if ctx.text("calendar_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def calendar_rule_3(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("calendar_score",0.0)
        if ctx.flag("calendar_blocked"): return -5.0
        if ctx.flag("calendar_3_complete"): return 4.0
        if ctx.text("calendar_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def calendar_rule_4(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("calendar_score",0.0)
        if ctx.flag("calendar_blocked"): return -5.0
        if ctx.flag("calendar_4_complete"): return 1.0
        if ctx.text("calendar_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def calendar_rule_5(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("calendar_score",0.0)
        if ctx.flag("calendar_blocked"): return -5.0
        if ctx.flag("calendar_5_complete"): return 2.0
        if ctx.text("calendar_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def calendar_rule_6(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("calendar_score",0.0)
        if ctx.flag("calendar_blocked"): return -5.0
        if ctx.flag("calendar_6_complete"): return 3.0
        if ctx.text("calendar_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def calendar_rule_7(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("calendar_score",0.0)
        if ctx.flag("calendar_blocked"): return -5.0
        if ctx.flag("calendar_7_complete"): return 4.0
        if ctx.text("calendar_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def calendar_rule_8(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("calendar_score",0.0)
        if ctx.flag("calendar_blocked"): return -5.0
        if ctx.flag("calendar_8_complete"): return 1.0
        if ctx.text("calendar_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def calendar_rule_9(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("calendar_score",0.0)
        if ctx.flag("calendar_blocked"): return -5.0
        if ctx.flag("calendar_9_complete"): return 2.0
        if ctx.text("calendar_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def calendar_rule_10(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("calendar_score",0.0)
        if ctx.flag("calendar_blocked"): return -5.0
        if ctx.flag("calendar_10_complete"): return 3.0
        if ctx.text("calendar_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def calendar_rule_11(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("calendar_score",0.0)
        if ctx.flag("calendar_blocked"): return -5.0
        if ctx.flag("calendar_11_complete"): return 4.0
        if ctx.text("calendar_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def calendar_rule_12(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("calendar_score",0.0)
        if ctx.flag("calendar_blocked"): return -5.0
        if ctx.flag("calendar_12_complete"): return 1.0
        if ctx.text("calendar_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def calendar_rule_13(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("calendar_score",0.0)
        if ctx.flag("calendar_blocked"): return -5.0
        if ctx.flag("calendar_13_complete"): return 2.0
        if ctx.text("calendar_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def calendar_rule_14(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("calendar_score",0.0)
        if ctx.flag("calendar_blocked"): return -5.0
        if ctx.flag("calendar_14_complete"): return 3.0
        if ctx.text("calendar_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def focus_rule_1(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("focus_score",0.0)
        if ctx.flag("focus_blocked"): return -5.0
        if ctx.flag("focus_1_complete"): return 2.0
        if ctx.text("focus_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def focus_rule_2(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("focus_score",0.0)
        if ctx.flag("focus_blocked"): return -5.0
        if ctx.flag("focus_2_complete"): return 3.0
        if ctx.text("focus_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def focus_rule_3(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("focus_score",0.0)
        if ctx.flag("focus_blocked"): return -5.0
        if ctx.flag("focus_3_complete"): return 4.0
        if ctx.text("focus_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def focus_rule_4(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("focus_score",0.0)
        if ctx.flag("focus_blocked"): return -5.0
        if ctx.flag("focus_4_complete"): return 1.0
        if ctx.text("focus_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def focus_rule_5(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("focus_score",0.0)
        if ctx.flag("focus_blocked"): return -5.0
        if ctx.flag("focus_5_complete"): return 2.0
        if ctx.text("focus_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def focus_rule_6(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("focus_score",0.0)
        if ctx.flag("focus_blocked"): return -5.0
        if ctx.flag("focus_6_complete"): return 3.0
        if ctx.text("focus_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def focus_rule_7(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("focus_score",0.0)
        if ctx.flag("focus_blocked"): return -5.0
        if ctx.flag("focus_7_complete"): return 4.0
        if ctx.text("focus_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def focus_rule_8(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("focus_score",0.0)
        if ctx.flag("focus_blocked"): return -5.0
        if ctx.flag("focus_8_complete"): return 1.0
        if ctx.text("focus_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def focus_rule_9(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("focus_score",0.0)
        if ctx.flag("focus_blocked"): return -5.0
        if ctx.flag("focus_9_complete"): return 2.0
        if ctx.text("focus_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def focus_rule_10(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("focus_score",0.0)
        if ctx.flag("focus_blocked"): return -5.0
        if ctx.flag("focus_10_complete"): return 3.0
        if ctx.text("focus_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def focus_rule_11(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("focus_score",0.0)
        if ctx.flag("focus_blocked"): return -5.0
        if ctx.flag("focus_11_complete"): return 4.0
        if ctx.text("focus_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def focus_rule_12(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("focus_score",0.0)
        if ctx.flag("focus_blocked"): return -5.0
        if ctx.flag("focus_12_complete"): return 1.0
        if ctx.text("focus_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def focus_rule_13(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("focus_score",0.0)
        if ctx.flag("focus_blocked"): return -5.0
        if ctx.flag("focus_13_complete"): return 2.0
        if ctx.text("focus_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def focus_rule_14(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("focus_score",0.0)
        if ctx.flag("focus_blocked"): return -5.0
        if ctx.flag("focus_14_complete"): return 3.0
        if ctx.text("focus_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def review_rule_1(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("review_score",0.0)
        if ctx.flag("review_blocked"): return -5.0
        if ctx.flag("review_1_complete"): return 2.0
        if ctx.text("review_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def review_rule_2(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("review_score",0.0)
        if ctx.flag("review_blocked"): return -5.0
        if ctx.flag("review_2_complete"): return 3.0
        if ctx.text("review_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def review_rule_3(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("review_score",0.0)
        if ctx.flag("review_blocked"): return -5.0
        if ctx.flag("review_3_complete"): return 4.0
        if ctx.text("review_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def review_rule_4(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("review_score",0.0)
        if ctx.flag("review_blocked"): return -5.0
        if ctx.flag("review_4_complete"): return 1.0
        if ctx.text("review_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def review_rule_5(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("review_score",0.0)
        if ctx.flag("review_blocked"): return -5.0
        if ctx.flag("review_5_complete"): return 2.0
        if ctx.text("review_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def review_rule_6(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("review_score",0.0)
        if ctx.flag("review_blocked"): return -5.0
        if ctx.flag("review_6_complete"): return 3.0
        if ctx.text("review_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def review_rule_7(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("review_score",0.0)
        if ctx.flag("review_blocked"): return -5.0
        if ctx.flag("review_7_complete"): return 4.0
        if ctx.text("review_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def review_rule_8(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("review_score",0.0)
        if ctx.flag("review_blocked"): return -5.0
        if ctx.flag("review_8_complete"): return 1.0
        if ctx.text("review_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def review_rule_9(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("review_score",0.0)
        if ctx.flag("review_blocked"): return -5.0
        if ctx.flag("review_9_complete"): return 2.0
        if ctx.text("review_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def review_rule_10(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("review_score",0.0)
        if ctx.flag("review_blocked"): return -5.0
        if ctx.flag("review_10_complete"): return 3.0
        if ctx.text("review_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def review_rule_11(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("review_score",0.0)
        if ctx.flag("review_blocked"): return -5.0
        if ctx.flag("review_11_complete"): return 4.0
        if ctx.text("review_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def review_rule_12(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("review_score",0.0)
        if ctx.flag("review_blocked"): return -5.0
        if ctx.flag("review_12_complete"): return 1.0
        if ctx.text("review_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def review_rule_13(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("review_score",0.0)
        if ctx.flag("review_blocked"): return -5.0
        if ctx.flag("review_13_complete"): return 2.0
        if ctx.text("review_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def review_rule_14(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("review_score",0.0)
        if ctx.flag("review_blocked"): return -5.0
        if ctx.flag("review_14_complete"): return 3.0
        if ctx.text("review_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def recurrence_rule_1(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("recurrence_score",0.0)
        if ctx.flag("recurrence_blocked"): return -5.0
        if ctx.flag("recurrence_1_complete"): return 2.0
        if ctx.text("recurrence_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def recurrence_rule_2(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("recurrence_score",0.0)
        if ctx.flag("recurrence_blocked"): return -5.0
        if ctx.flag("recurrence_2_complete"): return 3.0
        if ctx.text("recurrence_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def recurrence_rule_3(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("recurrence_score",0.0)
        if ctx.flag("recurrence_blocked"): return -5.0
        if ctx.flag("recurrence_3_complete"): return 4.0
        if ctx.text("recurrence_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def recurrence_rule_4(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("recurrence_score",0.0)
        if ctx.flag("recurrence_blocked"): return -5.0
        if ctx.flag("recurrence_4_complete"): return 1.0
        if ctx.text("recurrence_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def recurrence_rule_5(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("recurrence_score",0.0)
        if ctx.flag("recurrence_blocked"): return -5.0
        if ctx.flag("recurrence_5_complete"): return 2.0
        if ctx.text("recurrence_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def recurrence_rule_6(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("recurrence_score",0.0)
        if ctx.flag("recurrence_blocked"): return -5.0
        if ctx.flag("recurrence_6_complete"): return 3.0
        if ctx.text("recurrence_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def recurrence_rule_7(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("recurrence_score",0.0)
        if ctx.flag("recurrence_blocked"): return -5.0
        if ctx.flag("recurrence_7_complete"): return 4.0
        if ctx.text("recurrence_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def recurrence_rule_8(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("recurrence_score",0.0)
        if ctx.flag("recurrence_blocked"): return -5.0
        if ctx.flag("recurrence_8_complete"): return 1.0
        if ctx.text("recurrence_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def recurrence_rule_9(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("recurrence_score",0.0)
        if ctx.flag("recurrence_blocked"): return -5.0
        if ctx.flag("recurrence_9_complete"): return 2.0
        if ctx.text("recurrence_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def recurrence_rule_10(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("recurrence_score",0.0)
        if ctx.flag("recurrence_blocked"): return -5.0
        if ctx.flag("recurrence_10_complete"): return 3.0
        if ctx.text("recurrence_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def recurrence_rule_11(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("recurrence_score",0.0)
        if ctx.flag("recurrence_blocked"): return -5.0
        if ctx.flag("recurrence_11_complete"): return 4.0
        if ctx.text("recurrence_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def recurrence_rule_12(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("recurrence_score",0.0)
        if ctx.flag("recurrence_blocked"): return -5.0
        if ctx.flag("recurrence_12_complete"): return 1.0
        if ctx.text("recurrence_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def recurrence_rule_13(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("recurrence_score",0.0)
        if ctx.flag("recurrence_blocked"): return -5.0
        if ctx.flag("recurrence_13_complete"): return 2.0
        if ctx.text("recurrence_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def recurrence_rule_14(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("recurrence_score",0.0)
        if ctx.flag("recurrence_blocked"): return -5.0
        if ctx.flag("recurrence_14_complete"): return 3.0
        if ctx.text("recurrence_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def completion_rule_1(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("completion_score",0.0)
        if ctx.flag("completion_blocked"): return -5.0
        if ctx.flag("completion_1_complete"): return 2.0
        if ctx.text("completion_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def completion_rule_2(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("completion_score",0.0)
        if ctx.flag("completion_blocked"): return -5.0
        if ctx.flag("completion_2_complete"): return 3.0
        if ctx.text("completion_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def completion_rule_3(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("completion_score",0.0)
        if ctx.flag("completion_blocked"): return -5.0
        if ctx.flag("completion_3_complete"): return 4.0
        if ctx.text("completion_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def completion_rule_4(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("completion_score",0.0)
        if ctx.flag("completion_blocked"): return -5.0
        if ctx.flag("completion_4_complete"): return 1.0
        if ctx.text("completion_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def completion_rule_5(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("completion_score",0.0)
        if ctx.flag("completion_blocked"): return -5.0
        if ctx.flag("completion_5_complete"): return 2.0
        if ctx.text("completion_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def completion_rule_6(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("completion_score",0.0)
        if ctx.flag("completion_blocked"): return -5.0
        if ctx.flag("completion_6_complete"): return 3.0
        if ctx.text("completion_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def completion_rule_7(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("completion_score",0.0)
        if ctx.flag("completion_blocked"): return -5.0
        if ctx.flag("completion_7_complete"): return 4.0
        if ctx.text("completion_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def completion_rule_8(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("completion_score",0.0)
        if ctx.flag("completion_blocked"): return -5.0
        if ctx.flag("completion_8_complete"): return 1.0
        if ctx.text("completion_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def completion_rule_9(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("completion_score",0.0)
        if ctx.flag("completion_blocked"): return -5.0
        if ctx.flag("completion_9_complete"): return 2.0
        if ctx.text("completion_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def completion_rule_10(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("completion_score",0.0)
        if ctx.flag("completion_blocked"): return -5.0
        if ctx.flag("completion_10_complete"): return 3.0
        if ctx.text("completion_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def completion_rule_11(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("completion_score",0.0)
        if ctx.flag("completion_blocked"): return -5.0
        if ctx.flag("completion_11_complete"): return 4.0
        if ctx.text("completion_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def completion_rule_12(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("completion_score",0.0)
        if ctx.flag("completion_blocked"): return -5.0
        if ctx.flag("completion_12_complete"): return 1.0
        if ctx.text("completion_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def completion_rule_13(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("completion_score",0.0)
        if ctx.flag("completion_blocked"): return -5.0
        if ctx.flag("completion_13_complete"): return 2.0
        if ctx.text("completion_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def completion_rule_14(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("completion_score",0.0)
        if ctx.flag("completion_blocked"): return -5.0
        if ctx.flag("completion_14_complete"): return 3.0
        if ctx.text("completion_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def escalation_rule_1(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("escalation_score",0.0)
        if ctx.flag("escalation_blocked"): return -5.0
        if ctx.flag("escalation_1_complete"): return 2.0
        if ctx.text("escalation_1"): return clamp(value+2,-10.0,10.0)
        return -2.0

    def escalation_rule_2(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("escalation_score",0.0)
        if ctx.flag("escalation_blocked"): return -5.0
        if ctx.flag("escalation_2_complete"): return 3.0
        if ctx.text("escalation_2"): return clamp(value+3,-10.0,10.0)
        return -3.0

    def escalation_rule_3(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("escalation_score",0.0)
        if ctx.flag("escalation_blocked"): return -5.0
        if ctx.flag("escalation_3_complete"): return 4.0
        if ctx.text("escalation_3"): return clamp(value+4,-10.0,10.0)
        return -1.0

    def escalation_rule_4(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("escalation_score",0.0)
        if ctx.flag("escalation_blocked"): return -5.0
        if ctx.flag("escalation_4_complete"): return 1.0
        if ctx.text("escalation_4"): return clamp(value+5,-10.0,10.0)
        return -2.0

    def escalation_rule_5(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("escalation_score",0.0)
        if ctx.flag("escalation_blocked"): return -5.0
        if ctx.flag("escalation_5_complete"): return 2.0
        if ctx.text("escalation_5"): return clamp(value+1,-10.0,10.0)
        return -3.0

    def escalation_rule_6(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("escalation_score",0.0)
        if ctx.flag("escalation_blocked"): return -5.0
        if ctx.flag("escalation_6_complete"): return 3.0
        if ctx.text("escalation_6"): return clamp(value+2,-10.0,10.0)
        return -1.0

    def escalation_rule_7(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("escalation_score",0.0)
        if ctx.flag("escalation_blocked"): return -5.0
        if ctx.flag("escalation_7_complete"): return 4.0
        if ctx.text("escalation_7"): return clamp(value+3,-10.0,10.0)
        return -2.0

    def escalation_rule_8(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("escalation_score",0.0)
        if ctx.flag("escalation_blocked"): return -5.0
        if ctx.flag("escalation_8_complete"): return 1.0
        if ctx.text("escalation_8"): return clamp(value+4,-10.0,10.0)
        return -3.0

    def escalation_rule_9(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("escalation_score",0.0)
        if ctx.flag("escalation_blocked"): return -5.0
        if ctx.flag("escalation_9_complete"): return 2.0
        if ctx.text("escalation_9"): return clamp(value+5,-10.0,10.0)
        return -1.0

    def escalation_rule_10(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("escalation_score",0.0)
        if ctx.flag("escalation_blocked"): return -5.0
        if ctx.flag("escalation_10_complete"): return 3.0
        if ctx.text("escalation_10"): return clamp(value+1,-10.0,10.0)
        return -2.0

    def escalation_rule_11(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("escalation_score",0.0)
        if ctx.flag("escalation_blocked"): return -5.0
        if ctx.flag("escalation_11_complete"): return 4.0
        if ctx.text("escalation_11"): return clamp(value+2,-10.0,10.0)
        return -3.0

    def escalation_rule_12(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("escalation_score",0.0)
        if ctx.flag("escalation_blocked"): return -5.0
        if ctx.flag("escalation_12_complete"): return 1.0
        if ctx.text("escalation_12"): return clamp(value+3,-10.0,10.0)
        return -1.0

    def escalation_rule_13(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("escalation_score",0.0)
        if ctx.flag("escalation_blocked"): return -5.0
        if ctx.flag("escalation_13_complete"): return 2.0
        if ctx.text("escalation_13"): return clamp(value+4,-10.0,10.0)
        return -2.0

    def escalation_rule_14(self,ctx:TaskPlannerContext)->float:
        value=ctx.number("escalation_score",0.0)
        if ctx.flag("escalation_blocked"): return -5.0
        if ctx.flag("escalation_14_complete"): return 3.0
        if ctx.text("escalation_14"): return clamp(value+5,-10.0,10.0)
        return -3.0

    def evaluate_many(self,records:Sequence[Mapping[str,object]])->list[TaskPlannerResult]:
        return [self.evaluate(record) for record in records]
    def summarize(self,results:Sequence[TaskPlannerResult])->dict[str,object]:
        scores=[item.score for item in results]
        return {"count":len(scores),"average":round(sum(scores)/len(scores),2) if scores else 0.0,"strong":sum(x.status=="strong" for x in results),"acceptable":sum(x.status=="acceptable" for x in results),"review":sum(x.status=="review" for x in results)}
