"""Transparent offer comparison helpers; no financial or career outcome is guaranteed."""
from decimal import Decimal, InvalidOperation
from typing import Iterable, Mapping

CRITERIA = {"compensation", "benefits", "growth", "role_fit", "flexibility", "stability", "values"}
DEFAULT_WEIGHTS = {"compensation": 25, "benefits": 10, "growth": 20, "role_fit": 20,
                   "flexibility": 10, "stability": 10, "values": 5}

def _decimal(value, field):
    if value in (None, ""):
        return None
    try:
        result = Decimal(str(value).replace(",", ""))
    except InvalidOperation:
        raise ValueError(f"{field} must be numeric")
    if not result.is_finite():
        raise ValueError(f"{field} must be finite")
    return result

def validate_offer(offer: Mapping) -> dict:
    name = str(offer.get("name") or "").strip()
    if not name:
        raise ValueError("Offer name is required")
    salary = _decimal(offer.get("annual_base_salary"), "annual_base_salary")
    bonus = _decimal(offer.get("annual_bonus"), "annual_bonus")
    equity = _decimal(offer.get("annual_equity_estimate"), "annual_equity_estimate")
    if any(value is not None and value < 0 for value in (salary, bonus, equity)):
        raise ValueError("Compensation values cannot be negative")
    currency = str(offer.get("currency") or "unspecified").upper()[:8]
    ratings = {}
    for criterion in CRITERIA:
        value = offer.get(criterion)
        if value in (None, ""):
            ratings[criterion] = None
        else:
            try:
                value = int(value)
            except (ValueError, TypeError):
                raise ValueError(f"{criterion} rating must be an integer")
            if not 1 <= value <= 5:
                raise ValueError(f"{criterion} rating must be between 1 and 5")
            ratings[criterion] = value
    return {"id": offer.get("id"), "name": name[:160], "currency": currency,
            "annual_base_salary": str(salary) if salary is not None else None,
            "annual_bonus": str(bonus) if bonus is not None else None,
            "annual_equity_estimate": str(equity) if equity is not None else None,
            "benefits_notes": str(offer.get("benefits_notes") or "")[:2000],
            "remote_policy": str(offer.get("remote_policy") or "unspecified")[:100],
            "location": str(offer.get("location") or "")[:200],
            "deadline": str(offer.get("deadline") or "")[:40], "ratings": ratings}

def weighted_offer_score(offer: Mapping, weights: Mapping | None = None) -> dict:
    row = validate_offer(offer)
    weights = dict(DEFAULT_WEIGHTS if weights is None else weights)
    unknown = set(weights) - CRITERIA
    if unknown:
        raise ValueError("Unknown criteria: " + ", ".join(sorted(unknown)))
    if any(not isinstance(value, (int, float)) or value < 0 for value in weights.values()):
        raise ValueError("Weights must be non-negative numbers")
    total_weight = sum(weights.values())
    if total_weight <= 0:
        raise ValueError("At least one positive weight is required")
    numerator = denominator = 0.0
    missing = []
    for criterion in CRITERIA:
        weight = float(weights.get(criterion, 0))
        rating = row["ratings"][criterion]
        if rating is None:
            if weight:
                missing.append(criterion)
            continue
        numerator += rating * weight
        denominator += weight
    return {"offer_id": row["id"], "offer_name": row["name"],
            "score_out_of_5": round(numerator / denominator, 2) if denominator else None,
            "score_percent": round(100 * numerator / (5 * denominator), 2) if denominator else None,
            "rated_weight_percent": round(100 * denominator / total_weight, 2),
            "missing_weighted_criteria": sorted(missing),
            "coverage_warning": "Score reflects only criteria you rated; missing ratings can change the result."}

def compare_offers(offers: Iterable[Mapping], weights: Mapping | None = None) -> dict:
    rows = [validate_offer(offer) for offer in offers]
    if len(rows) < 2:
        raise ValueError("At least two offers are required for comparison")
    currencies = {row["currency"] for row in rows}
    compensation_comparable = len(currencies) == 1 and "UNSPECIFIED" not in currencies
    scores = [weighted_offer_score(row, weights) for row in rows]
    combined = []
    for row, score in zip(rows, scores):
        compensation = None
        if compensation_comparable:
            parts = [_decimal(row[key], key) or Decimal("0") for key in
                     ("annual_base_salary", "annual_bonus", "annual_equity_estimate")]
            compensation = str(sum(parts))
        combined.append({"offer": row, "score": score, "estimated_annual_cash_and_equity": compensation})
    combined.sort(key=lambda item: (item["score"]["score_percent"] is not None,
                                    item["score"]["score_percent"] or -1,
                                    item["score"]["rated_weight_percent"]), reverse=True)
    return {"offers": combined, "currency_comparable": compensation_comparable,
            "compensation_warning": None if compensation_comparable else
                "Compensation totals are not compared because currencies are missing or differ.",
            "decision_prompt": "Review your own priorities, contract terms, location, benefits, and personal circumstances.",
            "disclaimer": "This is a decision aid, not financial, legal, immigration, or career advice."}

def negotiation_preparation(offer: Mapping, priorities: Iterable[str], constraints: Iterable[str] = ()) -> dict:
    row = validate_offer(offer)
    priorities = [str(value).strip()[:250] for value in priorities if str(value).strip()]
    constraints = [str(value).strip()[:250] for value in constraints if str(value).strip()]
    if not priorities:
        raise ValueError("Add at least one negotiation priority")
    prompts = [
        "Identify the single most important change you are requesting.",
        "Prepare a truthful explanation of the value and experience you bring.",
        "Check whether the request is negotiable and who can approve it.",
        "Ask respectfully, leave room for discussion, and confirm any agreement in writing.",
    ]
    return {"offer": row["name"], "priorities": priorities[:10], "constraints": constraints[:10],
            "preparation_steps": prompts,
            "example_structure": ["Express appreciation", "State the request clearly",
                                  "Give a concise factual rationale", "Ask whether there is flexibility"],
            "warning": "Do not misrepresent competing offers, qualifications, or personal circumstances."}

def offer_missing_information(offer: Mapping) -> list[dict]:
    row = validate_offer(offer)
    missing = []
    for field, label in (
        ("annual_base_salary", "Base salary"), ("annual_bonus", "Bonus terms"),
        ("annual_equity_estimate", "Equity terms"), ("benefits_notes", "Benefits"),
        ("remote_policy", "Remote or onsite expectations"), ("deadline", "Decision deadline"),
    ):
        value = row.get(field)
        if value in (None, "", "unspecified"):
            missing.append({"field": field, "label": label,
                            "question": f"Ask for written clarification of {label.lower()}."})
    if row["currency"] == "UNSPECIFIED":
        missing.append({"field": "currency", "label": "Currency",
                        "question": "Confirm the currency and pay period."})
    return missing

def compare_compensation(offers: Iterable[Mapping]) -> dict:
    rows = [validate_offer(offer) for offer in offers]
    if not rows:
        return {"comparable": False, "offers": [], "reason": "No offers supplied"}
    currencies = {row["currency"] for row in rows}
    if len(currencies) != 1 or "UNSPECIFIED" in currencies:
        return {"comparable": False, "offers": [{"name": row["name"], "currency": row["currency"]}
                                                 for row in rows],
                "reason": "Currencies must match before comparing amounts."}
    values = []
    for row in rows:
        amounts = [_decimal(row[field], field) for field in
                   ("annual_base_salary", "annual_bonus", "annual_equity_estimate")]
        total = sum((value or Decimal("0")) for value in amounts)
        values.append({"name": row["name"], "currency": row["currency"],
                       "base": amounts[0], "bonus": amounts[1], "equity_estimate": amounts[2],
                       "estimated_total": total})
    values.sort(key=lambda item: item["estimated_total"], reverse=True)
    return {"comparable": True, "currency": next(iter(currencies)),
            "offers": [{key: str(value) if isinstance(value, Decimal) else value for key, value in row.items()}
                       for row in values],
            "warning": "Equity is uncertain and bonus is not guaranteed; compare written terms and benefits."}
