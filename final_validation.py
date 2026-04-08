#!/usr/bin/env python3
"""
Final validation check before resubmission
Verifies:
1. At least 3 tasks with graders defined
2. All scores strictly between 0 and 1
"""

import yaml
from env.environment import SupportEnv
from env.models import Action
from pathlib import Path

def validate_yaml_tasks():
    """Check openenv.yaml has 3 tasks with graders"""
    print("=" * 70)
    print("REQUIREMENT 1: At least 3 tasks with graders")
    print("=" * 70)
    
    yaml_path = Path(__file__).parent / "openenv.yaml"
    with open(yaml_path) as f:
        config = yaml.safe_load(f)
    
    tasks = config.get("tasks", [])
    print(f"\nFound {len(tasks)} tasks in openenv.yaml:\n")
    
    for task in tasks:
        name = task.get("name")
        grader = task.get("grader")
        status = "✓" if grader else "✗"
        print(f"  {status} {name:20s} -> {grader}")
    
    has_3_graders = len([t for t in tasks if t.get("grader")]) >= 3
    print(f"\n✓ PASS: 3+ tasks with graders" if has_3_graders else "\n✗ FAIL: Less than 3 graders")
    return has_3_graders

def validate_score_ranges():
    """Check all graders return scores in (0, 1)"""
    print("\n" + "=" * 70)
    print("REQUIREMENT 2: Scores strictly between 0 and 1")
    print("=" * 70)
    
    test_cases = []
    
    # Test 1: Empty history (minimum score)
    print("\nTest Case 1: Empty history (baseline scores)")
    for task_type in ["easy_ticket", "medium_ticket", "hard_ticket"]:
        env = SupportEnv()
        env.reset()
        score = env.grade(task_type)
        valid = 0 < score < 1
        status = "✓" if valid else "✗"
        print(f"  {status} {task_type:20s} score={score:.4f}")
        test_cases.append((task_type, "empty", score, valid))
    
    # Test 2: Partial history
    print("\nTest Case 2: Partial history (1-2 actions)")
    for task_type in ["easy_ticket", "medium_ticket", "hard_ticket"]:
        env = SupportEnv()
        env.reset()
        env.step(Action(action_type="classify", value="high"))
        score = env.grade(task_type)
        valid = 0 < score < 1
        status = "✓" if valid else "✗"
        print(f"  {status} {task_type:20s} score={score:.4f}")
        test_cases.append((task_type, "partial", score, valid))
    
    # Test 3: Full history (perfect actions)
    print("\nTest Case 3: Full history (perfect actions)")
    for task_type in ["easy_ticket", "medium_ticket", "hard_ticket"]:
        env = SupportEnv()
        env.reset()
        
        # Run optimal actions
        actions = [
            Action(action_type="classify", value="high"),
            Action(action_type="assign", value=env.state_data.get("correct_agent", "support")),
            Action(action_type="respond", value="refund processed" if env.category == "billing" else "resolved")
        ]
        
        for action in actions:
            result = env.step(action)
            if result["done"]:
                break
        
        score = env.grade(task_type)
        valid = 0 < score < 1
        status = "✓" if valid else "✗"
        print(f"  {status} {task_type:20s} score={score:.4f}")
        test_cases.append((task_type, "full", score, valid))
    
    # Verify no scores are exactly 0 or 1
    print("\nValidating score bounds:")
    invalid_scores = [tc for tc in test_cases if not tc[3]]
    exact_zero = [tc for tc in test_cases if tc[2] == 0.0]
    exact_one = [tc for tc in test_cases if tc[2] == 1.0]
    
    print(f"  ✓ No scores equal 0.0: {len(exact_zero) == 0}")
    print(f"  ✓ No scores equal 1.0: {len(exact_one) == 0}")
    print(f"  ✓ All scores in (0, 1): {len(invalid_scores) == 0}")
    
    all_valid = len(invalid_scores) == 0 and len(exact_zero) == 0 and len(exact_one) == 0
    print(f"\n✓ PASS: All scores strictly between 0 and 1" if all_valid else "\n✗ FAIL: Some invalid scores")
    return all_valid

def main():
    print("\n")
    print("█" * 70)
    print("  FINAL VALIDATION - OpenEnv Requirements Check")
    print("█" * 70)
    
    req1_pass = validate_yaml_tasks()
    req2_pass = validate_score_ranges()
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"\n  Requirement 1 (3+ graders):     {'✓ PASS' if req1_pass else '✗ FAIL'}")
    print(f"  Requirement 2 (scores 0<x<1):  {'✓ PASS' if req2_pass else '✗ FAIL'}")
    
    if req1_pass and req2_pass:
        print("\n✓ ALL REQUIREMENTS MET - Ready for resubmission!")
        return 0
    else:
        print("\n✗ SOME REQUIREMENTS FAILED - Please fix before resubmission")
        return 1

if __name__ == "__main__":
    exit(main())
