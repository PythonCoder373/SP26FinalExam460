# Development Log – The Torchbearer

**Student Name:** Philip Revak
**Student ID:** 131950621

> Instructions: Write at least four dated entries. Required entry types are marked below.
> Two to five sentences per entry is sufficient. Write entries as you go, not all in one
> sitting. Graders check that entries reflect genuine work across multiple sessions.
> Delete all blockquotes before submitting.

---

## Entry 1 – 5/7/2026: Initial Plan

> Required. Write this before writing any code. Describe your plan: what you will
> implement first, what parts you expect to be difficult, and how you plan to test.

I plan on implementing dijkstra's algorithm first because it is needed to find the shortest paths to the relics. Then I will work on the algorithm to determing the optimal route that visits all relics, which I expect to be more cahlengeing since we have already writen dijkstra before. I plan to test each function individualy on several test cases I will create, and test the edge cases.

---

## Entry 2 – [5/8/2026]: Dijkstra Implementation and Misconceptions

> Required. At least one entry must describe a bug, wrong assumption, or design change
> you encountered. Describe what went wrong and how you resolved it.

While I was implementing the run_dijkstra function, I realized that the distances needed to be stored as a dictionary. I previously assumed that I could store them as a 2d array, and have now updated the descriptions in readme part 2b to match this.

I also only realized that the dungeon contained non relic rooms when I was anlyizing the time complexity of Dijkstra in readme part 2c.

---

## Entry 3 – 5/14/2026: find_optimal_route Implementation

I implemented the find_optimal_route and the _explore functions. These search for the optimal relic collection order and use pruning to reduce the search space when possible. The _explore function recursivly explores possible routes in a DFS order using backtracking.

---

## Entry 4 – 5/14/2026: Post-Implementation Reflection

> Required. Written after your implementation is complete. Describe what you would
> change or improve given more time.

I think that one thing I could improve would be changing relics_remaining to some other data type that would be faster than O(n). I also think that the pruning's lower bound could be improved by changing the extra cost required to complete the route to the already calulated optimal distance from the current node to the exit.

---

## Final Entry – 5/14/2026: Time Estimate

> Required. Estimate minutes spent per part. Honesty is expected; accuracy is not graded.

| Part | Estimated Hours |
|---|---|
| Part 1: Problem Analysis | 60 |
| Part 2: Precomputation Design | 60 |
| Part 3: Algorithm Correctness | 60 |
| Part 4: Search Design | 60 |
| Part 5: State and Search Space | 90 |
| Part 6: Pruning | 90|
| Part 7: Implementation | 180 |
| README and DEVLOG writing | 180 |
| **Total** | 450 |

These are very rough estimates since I did not accuratly track how long I spent on each part. I worked on the coresponding sections of readme and torchbearer simultaniously, and took breaks often between questions so the times do not represent long focused sessions.