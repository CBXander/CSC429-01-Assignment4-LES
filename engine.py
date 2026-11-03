from dataclasses import dataclass
from typing import List, Set, Dict, Any

@dataclass
class Rule:
    antecedents: List[str]
    consequent: str
    priority: int = 0
    name: str = ""

    cf: float = 1.0 # Uncertainty handling
    
class ForwardChainingEngine:
    def __init__(self, rules: List[Rule]):
        self.rules = rules
        self.facts: Set[str] = set()
        self.cf: Dict[str, float] = {} # confidence for each fact
        self.trace: List[Dict[str, Any]] = []

    def assert_facts(self, initial: List[str]) -> None:
        """Store initial facts into the working memory."""
        # accepts a list of all 100% sure facts or a dictionary of facts with their confidence levels
        if isinstance(initial, dict):
            for fact in initial:
                self.facts.add(fact)
                self.cf[fact] = initial[fact]
        else:
            for fact in initial:
                self.facts.add(fact)
                self.cf[fact] = 1.0

    def can_fire(self, rule: Rule) -> bool:
        return all(a in self.facts for a in rule.antecedents) and rule.consequent not in self.facts
        

    def run(self) -> None:
        while True:
            # make list of all rules that can fire
            candidates = [r for r in self.rules if self.can_fire(r)]
            if not candidates:
                return

            
            # If several rules can fire, pick the one with the highest priority.
            # max() compares the rules using key=lambda r: r.priority. (aka. each rule's priority number)
            # If to rules tie, max() keeps the one that comes first in the JSON file.
            rule = max(candidates, key=lambda r: r.priority)
                                   # ^ function: call each rule r, check and give its priority number.
            # Look up the confidence of each condition and take the lowest one.
            weakest = min(self.cf[a] for a in rule.antecedents)
            confidence = round(weakest * rule.cf, 2)
            self.cf[rule.consequent] = confidence

            self.facts.add(rule.consequent)
            self.trace.append({
                "rule": rule.name,
                "antecedents": rule.antecedents,
                "consequent": rule.consequent,
                "cf": confidence
            })


    def conclusions(self) -> Dict[str, List[str]]:
        recs = sorted(f.split(":", 1)[1] for f in self.facts if f.startswith("recommend:"))
        specs = sorted(f.split(":", 1)[1] for f in self.facts if f.startswith("spec:"))
        models = sorted(f.split(":", 1)[1] for f in self.facts if f.startswith("model:"))
        other = sorted(f for f in self.facts if ":" not in f)
        return {"recommendations": recs, "specs": specs, "models": models, "other": other}