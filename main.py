from kb_loader import load_rules
from engine import ForwardChainingEngine

KB_PATH = "kb/laptop_rules.json"

# asks user a question and collects their answer
def ask(question, fact, rules):
    answer = input(question + " (y/n): ").strip().lower()

    # if the user types why, show which rules need this answer
    while True:
        if answer == "why":
            print("I need to know this because of these rules:")
            for rule in rules:
                if fact in rule["antecedents"]:
                    print("  -", rule["name"])
        # If user does not type y, yes, n, or no, prompt them again.
        elif answer in ("y", "yes"):
            return True
        elif answer in ("n", "no"):
            return False
        else:
            answer = input("Please answer with 'y', 'n', or 'why': ").strip().lower()


def collect_initial_facts(rules):
    facts = []
    # Ask more questions to collect facts for reasoning
    if ask("Is portability important?", "portable", rules):
        facts.append("portable")
    if ask("Do you need long battery life?", "long_battery", rules):
        facts.append("long_battery")
    if ask("Is your budget high?", "budget_high", rules):
        facts.append("budget_high")
    elif ask("Is your budget medium?", "budget_medium", rules):
        facts.append("budget_medium")
    else:
        facts.append("budget_low")
    if ask("Will you use it for gaming?", "gaming", rules):
        facts.append("gaming")
    if ask("Will you do creative work?", "creative_work", rules):
        facts.append("creative_work")
    if ask("Is it only for office work?", "office_only", rules):
        facts.append("office_only")
    if ask("Do you need AI acceleration?", "needs_ai_accel", rules):
        facts.append("needs_ai_accel")
    if ask("Do you want a large screen?", "large_screen", rules):
        facts.append("large_screen")
    if ask("Do you travel often?", "travel_often", rules):
        facts.append("travel_often")
    if ask("Do you prefer macOS?", "pref_os_macos", rules):
        facts.append("pref_os_macos")
    elif ask("Do you prefer Linux?", "pref_os_linux", rules):
        facts.append("pref_os_linux")
    else:
        facts.append("pref_os_windows")
    return facts



def main():
    # Load rules, create engine, assert facts, and run inference
    # Loop until the user decides to stop
    while True:
        rules = load_rules(KB_PATH)
        engine = ForwardChainingEngine(rules)
        print("Answer y or n. Type 'why' at any question to see why it's asked.\n")
        engine.assert_facts(collect_initial_facts(rules))
        engine.run()

        print()

        # Print the recommendations and their explanations
        for step in engine.trace:
            if step["consequent"].startswith("recommend:"):
                print(f"=> Recommendation: {step['consequent'].split(':', 1)[1]} (confidence: {step['cf']:.0%})")
                print(f"=> Explanation: derived from rule '{step['rule']}'")
                print()
        if not engine.conclusions()["recommendations"]:
            print("No recommendations matched your answers.")
            print()

        for spec in engine.conclusions()["specs"]:
                print(f"=> Spec: {spec} (confidence: {engine.cf['spec:' + spec]:.0%})")
        if engine.conclusions()["specs"]:
            print()
            
        for model in engine.conclusions()["models"]:
                print(f"=> Example model: {model.replace('_', ' ')} (confidence: {engine.cf['model:' + model]:.0%})")

        print("\nRules fired:")
        if not engine.trace:
            print(" (=> None. - no rule's conditions were fully met)")

        for step in engine.trace:
            print(f" - {step['rule']}")

        # Print the reasoning behind the conclusions if there are any
        if engine.trace:
            print("\n=> How I got these results:\n")
            for step in engine.trace:
                print(f"{step['consequent']} came from rule '{step['rule']}' because:")
                for condition in step["antecedents"]:
                    from_rule = False
                    for other in engine.trace:
                        if other["consequent"] == condition:
                            print(f"   - {condition} (found by rule '{other['rule']}')")
                            from_rule = True
                    if not from_rule:
                        print(f"   - {condition} (from your answers)")

        # Ask the user if they want to try again
        if not input("\nDo you want to try again? (y/n): ").lower().startswith("y"):
            print("Exiting...")
            break
        
if __name__ == "__main__":
    main()
    