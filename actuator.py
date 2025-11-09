"""Actuator: turn action-vectors into safe, limited keystrokes.

This module provides a tiny, well-scoped interface to emit keyboard
events that match your project's action-vector format. It is intentionally
conservative:
- Only keys listed in `globals.KEYS` may be actuated.
- By default the actuator runs in `dry_run` mode and only prints the
    actions it *would* take. Switch `dry_run=False` to send real OS events.

Data contract (simple):
- Input: a sequence/array of length 2*N where N = len(KEYS).
    - positions [0:N) are "press" flags, [N:2N) are "release" flags.
    - any non-zero value is treated as True.
- Side-effect: presses/releases issued via `pynput` (or printed in dry-run).

Keep it safe: use `dry_run=True` during development and tests. Only flip
to real mode after you've validated behavior with the example script.
"""

from typing import Sequence, Iterable
import time
from pynput import keyboard
import numpy as np
from globals import KEYS


class KeyActuator:
    """Actuator that issues key press/release commands.

    Parameters
    - dry_run: if True, do not send actual key events; only log actions.
    - rate_limit: minimum seconds between issuing events (float).
    """

    def __init__(self, dry_run: bool = True, rate_limit: float = 0.01):
        """Create an actuator.

        Args:
            dry_run: If True, do not emit OS events; print them instead.
            rate_limit: Minimum seconds to wait between individual events to
                        avoid flooding the OS or the target app.
        """
        self.dry_run = dry_run
        self.rate_limit = rate_limit
        # Controller is the object that sends real key events. Only create it
        # when dry_run is False so unit tests and CI remain side-effect free.
        self._controller = keyboard.Controller() if not dry_run else None
        # Keep the allowed keys in a tuple for fast indexing/lookup.
        self.allowed_keys = tuple(KEYS)

    def _send_press(self, key: keyboard.Key | keyboard.KeyCode):
        # Validate the key is one we expect; avoid accidental presses.
        if key not in self.allowed_keys:
            raise ValueError("attempt to press a key not in allowed KEYS")
        if self.dry_run:
            # Dry-run prints are intentionally human-readable.
            print(f"DRY RUN: press {key}")
        else:
            self._controller.press(key)
        # Small pause to be a bit more human-like and to respect rate limits.
        time.sleep(self.rate_limit)

    def _send_release(self, key: keyboard.Key | keyboard.KeyCode):
        # Release the given key (if allowed). Keep the same validation as
        # for presses so the system remains predictable.
        if key not in self.allowed_keys:
            raise ValueError("attempt to release a key not in allowed KEYS")
        if self.dry_run:
            print(f"DRY RUN: release {key}")
        else:
            self._controller.release(key)
        time.sleep(self.rate_limit)

    def apply_action_vector(self, action: Sequence, hold_time: float = 0.05):
        """Interpret and apply the action vector.

        Behaviour details:
        - The vector is split into two halves: presses then releases.
        - Presses are executed first (so a press+release in the same vector
          results in a short press followed by a release).
        - `hold_time` controls how long we hold a pressed key before continuing.

        Args:
            action: sequence or numpy array of length 2*N where N is number of keys.
            hold_time: how long to keep pressed keys held (seconds).
        """
        arr = np.asarray(action)
        n = len(self.allowed_keys)
        if arr.size != 2 * n:
            raise ValueError(f"action vector must have length {2*n}")

        # Convert to boolean masks for clarity
        presses = arr[:n].astype(bool)
        releases = arr[n:].astype(bool)

        # Process press events first. This gives deterministic behaviour when
        # both press and release bits are set for the same key.
        for i, do_press in enumerate(presses):
            if do_press:
                key = self.allowed_keys[i]
                self._send_press(key)
                if hold_time > 0:
                    time.sleep(hold_time)

        # Now process releases.
        for i, do_release in enumerate(releases):
            if do_release:
                key = self.allowed_keys[i]
                self._send_release(key)

        def press_sequence(self, sequence: Iterable[Sequence], hold_time: float = 0.05):
            """Apply multiple action vectors in order.

            This is a convenience around calling `apply_action_vector` repeatedly.
            It can be useful to script short sequences like "press A, then D".
            """
            for action in sequence:
                self.apply_action_vector(action, hold_time=hold_time)


def vector_from_keynames(pressed: Iterable[str], released: Iterable[str]):
    """Build the project's 2*N action vector from key-name lists.

    This helper is handy for tests and examples. It accepts lists of
    characters (e.g. ['w']) for pressed and released keys and returns a
    numpy int8 array with the corresponding bits set.

    Only character keys that appear in `globals.KEYS` (via their `.char`
    attribute) will be accepted.
    """
    n = len(KEYS)
    arr = np.zeros(2 * n, dtype=np.int8)

    # Build a simple mapping from character -> index into KEYS. Some keys
    # in KEYS might be special keys without a `.char` attribute; those are
    # ignored here on purpose.
    char_to_index = {}
    for i, k in enumerate(KEYS):
        try:
            char_to_index[k.char] = i
        except Exception:
            # Non-character keys are skipped for this helper.
            pass

    # Set press bits
    for p in pressed:
        if p in char_to_index:
            arr[char_to_index[p]] = 1
        else:
            raise ValueError(f"pressed key '{p}' not in allowed KEYS")

    # Set release bits
    for r in released:
        if r in char_to_index:
            arr[char_to_index[r] + n] = 1
        else:
            raise ValueError(f"released key '{r}' not in allowed KEYS")

    return arr


if __name__ == "__main__":
    # quick dry-run demo
    actuator = KeyActuator(dry_run=True)
    print("Demo: press 'w' then release 'w'")
    vec = vector_from_keynames(['w'], ['w'])
    actuator.apply_action_vector(vec, hold_time=0.02)
