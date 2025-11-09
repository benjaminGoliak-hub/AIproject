"""Example usage of the KeyActuator in dry-run mode.

This script shows two simple ways to use the actuator:
1) Apply a single action vector that presses then releases a key.
2) Apply a short sequence of action vectors (press 'a' then press 'd').

Run this during development to see textual output of the actions and make
sure the mapping from vectors to keys matches your expectations.
"""

import numpy as np
from actuator import KeyActuator, vector_from_keynames


def main():
    # Keep dry_run=True while testing so we don't send real keystrokes.
    actuator = KeyActuator(dry_run=True, rate_limit=0.0)

    # Example 1: press and then release the 'w' key. The helper builds the
    # 2*N action vector (press bits then release bits) used throughout the project.
    vec1 = vector_from_keynames(['w'], ['w'])
    print("Example 1: press+release 'w'")
    actuator.apply_action_vector(vec1, hold_time=0.01)

    # Example 2: a tiny scripted sequence — press 'a' (hold briefly), then
    # press 'd'. Useful to simulate multi-step inputs.
    vec2 = vector_from_keynames(['a'], [])
    vec3 = vector_from_keynames(['d'], [])
    print("Example 2 (sequence): press 'a' then 'd'")
    actuator.press_sequence([vec2, vec3], hold_time=0.02)


if __name__ == '__main__':
    main()
