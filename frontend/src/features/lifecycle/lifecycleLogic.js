export const LIFECYCLE_STATUSES=['saved','applied','screening','interview','offer','rejected','withdrawn'];
export const LIFECYCLE_LABELS={saved:'Saved',applied:'Applied',screening:'Screening',interview:'Interview',offer:'Offer',rejected:'Rejected',withdrawn:'Withdrawn'};
export const TERMINAL_STATUSES=['rejected','withdrawn'];
export function isTerminal(status){return TERMINAL_STATUSES.includes(status);}
export function statusIndex(status){return LIFECYCLE_STATUSES.indexOf(status);}
export function transitionDirection(from,to){return statusIndex(to)>statusIndex(from)?'forward':'backward';}
export function transitionOptions(status){return LIFECYCLE_STATUSES.filter(value=>value!==status).map(value=>({status:value,label:LIFECYCLE_LABELS[value],direction:transitionDirection(status,value),terminal:isTerminal(value)}));}
export function nextFollowUp(status,fromDate=new Date()){const days={applied:7,screening:4,interview:2,offer:2}[status];if(!days)return null;const date=new Date(fromDate);date.setDate(date.getDate()+days);return date.toISOString().slice(0,10);}
export function summarizeLifecycle(application){return {status:LIFECYCLE_LABELS[application?.status]||'Unknown',terminal:isTerminal(application?.status),followUp:application?.next_action_date||null,action:application?.next_action||'No next action'};}
