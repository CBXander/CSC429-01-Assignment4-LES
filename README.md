# Laptop Advisor Expert System

## What it does
- Asks the user yes/no questions about what they need in a laptop.
- Uses forward chaining to recommend a laptop type, specs, and an example model.
- Explains its reasoning and shows how confident it is in each result.

## How to run
```
python main.py
python tests/test.py
```

## Files
- `engine.py` - the inference engine
- `main.py` - asks questions and prints results
- `kb_loader.py` - loads the rules from JSON
- `kb/laptop_rules.json` - the rules
- `tests/` - test cases

## How it works
1. The user's answers become facts (like `portable` or `budget_high`).
2. The engine looks for rules where all IF conditions are true.
3. It fires the highest priority rule and adds its THEN part as a new fact.
4. It repeats until no more rules can fire.
5. It prints the recommendations, specs, models, and which rules fired.

## Rules
- There are 14 rules. Four of them use results from other rules.

## Bonus: Why and How explanations
- **Why:** type `why` at any question to see which rules use that answer.
- **How:** after the results, each conclusion shows the rule that produced it
  and where each condition came from (your answer, or another rule).

## Bonus: Confidence factors
- Each rule has a confidence factor (cf) between 0.6 and 1.0.
- A conclusion's confidence = weakest condition x the rule's cf.
- Chained conclusions get less certain: MacBook = 0.95 x 0.8 = 76%.

## Testing
- `tests/test.py` checks 11 cases. Result: **11/11 passed**.
- `tests/test_cases.txt` lists 7 cases with input facts and expected results.
- Example: `['budget_high', 'portable', 'long_battery']` → `recommend:premium_ultrabook (95%)`

## Limitations
- A rule only fires if all of its conditions are true.
- Some answers get no recommendation (for example, a low budget gamer).
- Answers are only yes/no, so confidence comes from the rules, not the user.
