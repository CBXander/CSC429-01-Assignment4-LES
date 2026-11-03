import json
from typing import List
from engine import Rule

def load_rules(path: str) -> List[Rule]:
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    rules = []
    for i, r in enumerate(raw, start=1):
        rules.append(Rule(
            antecedents=r.get("if", []),
            consequent=r["then"],
            priority=r.get("priority", 0),
            name=r.get("name", f"Rule #{i}"),

            # Added for uncertainty handling, read the rule's confidence from JSON.
            # Defaults to 1.0 if not specified in the JSON.
            cf=r.get("cf", 1.0),
        ))
    return rules
