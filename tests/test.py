import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))  # so it can find engine.py

from engine import ForwardChainingEngine
from kb_loader import load_rules

KB = os.path.join(os.path.dirname(__file__), "..", "kb", "laptop_rules.json")


#
#
# Each test: (input facts, expected conclusion)
TESTS = [
    (["budget_high", "portable", "long_battery"],    "recommend:premium_ultrabook"),
    (["budget_low", "office_only", "portable"],      "recommend:budget_ultrabook"),
    (["gaming", "budget_medium"],                    "recommend:midrange_gaming_laptop"),
    (["gaming", "budget_high"],                      "recommend:high_end_gaming_laptop"),
    (["creative_work", "portable"],                  "spec:ram_16_plus"),
    (["creative_work", "large_screen"],              "spec:display_15_plus_color_accurate"),
    (["travel_often", "long_battery"],               "spec:battery_60wh_plus"),
    (["pref_os_macos"],                              "spec:macos_required"),
    (["needs_ai_accel"],                             "spec:gpu_with_tensor_cores"),
    (["pref_os_linux", "office_only"],               "spec:linux_friendly_hw"),
    (["budget_high", "portable", "long_battery", "pref_os_macos"], "model:Apple_MacBook_Air_15"),
]

passed = 0
for facts, expected in TESTS:
    engine = ForwardChainingEngine(load_rules(KB))
    engine.assert_facts(facts)
    engine.run()
    if expected in engine.facts:
        passed += 1
        print(f"PASS  {facts} -> {expected}")
    else:
        print(f"FAIL  {facts} -> expected {expected}")

print(f"\n{passed}/{len(TESTS)} tests passed")