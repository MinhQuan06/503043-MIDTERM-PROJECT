# Rubric checklist

Track progress against `RUBRIC_GK.docx` here. Update as requirements are finished — don't check something off until it's been reviewed against the actual rubric wording, not just "code runs".

## Formulation (2.0)

- [ ] Req 1 — State-space formulation (states, actions, start, goal, transition/cost model)
- [ ] Req 6 — Reformulated as competitive 2-agent problem

## Uninformed Search (3.0)

- [ ] Req 2 (UCS half) — UCS implemented and runs correctly on `example_map.txt`
- [ ] Req 3 (UCS half) — Time/space complexity measured for UCS
- [ ] Req 5/8 (visualize) — GUI shows UCS solving the map, action count correct

## Informed Search (3.0)

- [ ] Req 2 (A* half) — A* implemented, custom heuristic (not Euclidean/Manhattan)
- [ ] Req 3 (A* half) — Time/space complexity measured for A*, compared to UCS
- [ ] Req 4 — Heuristic admissibility proven + verified experimentally
- [ ] Req 4 — Heuristic consistency proven + verified experimentally
- [ ] Req 7 — Competitive-agent control algorithm, <=1000ms/decision
- [ ] Req 5/8 (visualize) — GUI shows A* solving the map, competitive mode working

## Presentation - well-prepared (1.0)

- [ ] Student list with tasks + completion % per member
- [ ] Approach explained with pseudocode/diagrams (no raw source code in slides)
- [ ] Pros/cons of the approaches discussed
- [ ] Completion % table included
- [ ] 4:3 aspect ratio, no dark background, readable in grayscale, <=5 min

## Presentation - Q&A (1.0)

- [ ] (assessed live - no prep checklist item, just know the material)

## Platform requirement (not separately scored, but a submission blocker)

- [ ] Verified running on macOS 13.7.8 (Ventura), Intel Core i5 - do this well before the deadline, not the night of
