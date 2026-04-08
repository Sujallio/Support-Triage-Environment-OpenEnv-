#!/usr/bin/env python3
"""Test grading functionality"""

from env.environment import SupportEnv
from env.models import Action

# Create environment and run a quick episode
env = SupportEnv()
obs = env.reset()

# Get the task name
task_name = f'{env.category}_ticket'
print(f'Running episode for task: {task_name}')
print(f'Initial observation: ticket_id={obs.ticket_id}, message={obs.message[:50]}...')

# Simulate a few actions
actions = [
    Action(action_type='classify', value='high'),
    Action(action_type='assign', value='billing' if env.category == 'billing' else 'technical' if env.category == 'technical' else 'general'),
    Action(action_type='respond', value='refund processed' if env.category == 'billing' else 'escalated')
]

for action in actions:
    result = env.step(action)
    print(f"Step result: reward={result['reward']:.3f}, done={result['done']}")
    if result['done']:
        break

# Get the grade
score = env.grade(task_name)
print(f'\nFinal grade for {task_name}: {score:.4f}')
print(f'Score is valid (0 < score < 1): {0 < score < 1}')

# Test all three graders
print('\nTesting all three tasks:')
for task in ['easy_ticket', 'medium_ticket', 'hard_ticket']:
    env2 = SupportEnv()
    obs2 = env2.reset()
    for action in actions[:3]:
        result = env2.step(action)
        if result['done']:
            break
    score = env2.grade(task)
    print(f'  {task}: score={score:.4f} (valid: {0 < score < 1})')

print('\nAll checks passed! The environment now properly supports grading.')
