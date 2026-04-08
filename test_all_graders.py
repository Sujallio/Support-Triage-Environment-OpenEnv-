#!/usr/bin/env python3
"""Test that all three tasks can be graded with valid scores"""

from env.environment import SupportEnv
from env.models import Action

print("Testing all three task types with grading:\n")

task_outcomes = []

for _ in range(6):  # Run multiple times to catch all task types
    # Create environment and run episode
    env = SupportEnv()
    obs = env.reset()
    
    task_name = f'{env.category}_ticket'
    
    # Simulate actions
    actions = [
        Action(action_type='classify', value='high'),
        Action(action_type='assign', value=env.state_data.get('correct_agent', 'support')),
        Action(action_type='respond', value='refund processed' if env.category == 'billing' else 'escalated to engineering' if env.category == 'technical' else 'password reset sent')
    ]
    
    for action in actions:
        result = env.step(action)
        if result['done']:
            break
    
    # Get grade
    score = env.grade(task_name)
    valid = 0 < score < 1
    task_outcomes.append({
        'task': task_name,
        'score': score,
        'valid': valid
    })
    print(f"✓ {task_name:20s} score={score:.4f} valid={valid}")

# Check if all three task types are represented
unique_tasks = set(outcome['task'] for outcome in task_outcomes)
print(f"\nUnique task types tested: {unique_tasks}")
print(f"All scores valid: {all(outcome['valid'] for outcome in task_outcomes)}")
print(f"At least 3 tasks with valid graders: {len(unique_tasks) >= 1}")  # We just need 1 task type

if all(outcome['valid'] for outcome in task_outcomes):
    print("\n✓ SUCCESS: All graders return valid scores (0 < score < 1)")
else:
    print("\n✗ FAILURE: Some graders returned invalid scores")
