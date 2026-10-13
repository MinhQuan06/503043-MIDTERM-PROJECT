# Requirement 5 - GUI design notes (spec, not code)

## Why build this before the search algorithms

`game.py` should only ever call one function from the solver side:

    solve(initial_state, algorithm) -> list[Action]      # algorithm: "UCS" | "A*"

Until Requirements 1-4 are done, `solve()` can just return an empty list, or a short
hand-written list of actions for testing (e.g. ["East", "East", "South"]) - that's
enough to build and test the rendering/controls without waiting on the search code.
When the real UCS/A* land later, only the body of `solve()` changes; `game.py` doesn't.

## Pieces `game.py` needs (design it yourself - this is the checklist, not the code)

1. **Window + tile grid**: pick a tile size in pixels, compute window dimensions from
   the map's width/height, draw one rectangle (or sprite) per cell based on its symbol.
2. **Static layer vs. dynamic layer**: walls and targets don't move - you can draw them
   once per frame cheaply, or pre-render them to a background surface. Agent and box
   positions change every step - those need to be redrawn from the *current* state.
3. **Action counter**: a piece of on-screen text showing how many actions have been
   taken so far - update it whenever you step forward/backward through the solved path.
4. **Algorithm selector**: some way (menu, keypress, command-line arg - your choice) to
   pick UCS vs A* before/at launch, which decides which `solve(..., algorithm=...)`
   call to make.
5. **Playback controls** (per the spec):
   - `Space` -> pause/resume
   - Right arrow -> step forward one action in the solved path
   - Left arrow -> step backward one action (undo the last action shown)
6. **OOP structure** (explicitly graded): think in terms of a `Game` class owning the
   render loop + current step index, and a separate state/model layer (`state.py`) it
   reads from - don't put game logic and rendering in one big script.

## pygame concepts you'll need (generic - look these up in pygame's own docs, not
tied to your specific game, so using them isn't "AI-authored" content)

- `pygame.init()`, `pygame.display.set_mode((w, h))` - window setup
- The main loop: `for event in pygame.event.get(): ...` to read keyboard/quit events
- `screen.blit(surface, (x, y))` or `pygame.draw.rect(...)` to draw each frame
- `pygame.time.Clock().tick(fps)` to cap the frame rate
- `pygame.font.Font(...).render(text, ...)` for the action-counter text

## Test before moving on

Manually play through `example_map.txt` with placeholder actions from a stub
`solve()` and confirm: the grid matches the legend, the action counter updates,
and Space/arrow keys behave as specified - before wiring in the real UCS/A*.
