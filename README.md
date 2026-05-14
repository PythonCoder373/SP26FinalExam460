# The Torchbearer

**Student Name:** Philip Revak
**Student ID:** 131950621
**Course:** CS 460 – Algorithms | Spring 2026

> This README is your project documentation. Write it the way a developer would document
> their design decisions , bullet points, brief justifications, and concrete examples where
> required. You are not writing an essay. You are explaining what you built and why you built
> it that way. Delete all blockquotes like this one before submitting.

---

## Part 1: Problem Analysis

> Document why this problem is not just a shortest-path problem. Three bullet points, one
> per question. Each bullet should be 1-2 sentences max.

- **Why a single shortest-path run from S is not enough:**
  A single shortest-path run only finds the shortest path to individual relics. This problem requires finding a optimal route that visites every relic at least once.

- **What decision remains after all inter-location costs are known:**
  After the distances from every node to all others are known, we still must determine the optimal route that visites every relic at least once, and begins at the start and ends at the exit.

- **Why this requires a search over orders (one sentence):**
  A search over orders is required because the order that relics are visited determines the total cost, so we must find the optimal order that minimizes the cost.

---

## Part 2: Precomputation Design

### Part 2a: Source Selection

> List the source node types as a bullet list. For each, one-line reason.

| Source Node Type | Why it is a source |
|---|---|
| Start S | We must compute the cost from the start node to all other nodes |
| Relics {R1, R2, ..., Rk} | We need the cost of traveling from every relic to all other relics since we dont know which paths are optimal  |

### Part 2b: Distance Storage

> Fill in the table. No prose required.

| Property | Your answer |
|---|---|
| Data structure name | dictionary of dictionaries|
| What the keys represent | first key is the source node, the seccond key is the location node |
| What the values represent | the minimum cost of trversing from the source to the location |
| Lookup time complexity | O(1) |
| Why O(1) lookup is possible | dictionaries allow values to be accesd in O(1) time if keys are known |

### Part 2c: Precomputation Complexity

> State the total complexity and show the arithmetic. Two to three lines max.

- **Number of Dijkstra runs:** 1+k (source and each relic)
- **Cost per run:** O((E+V)log(V)) (E=number of edges, V=number of nodes)
- **Total complexity:** O((1+k)(E+V)log(V))
- **Justification (one line):** Dijkstra runs once for each source node, which is 1+k nodes since the start node and the k relic nodes are the sources. Each run is O((E+V)log(V)) since we are using a priority queue.

---

## Part 3: Algorithm Correctness

> Document your understanding of why Dijkstra produces correct distances.
> Bullet points and short sentences throughout. No paragraphs.

### Part 3a: What the Invariant Means

> Two bullets: one for finalized nodes, one for non-finalized nodes.
> Do not copy the invariant text from the spec.

- **For nodes already finalized (in S):**
  The distance discovered by the algorithm is the optimal distance from the source to the node, and no other path can be better.

- **For nodes not yet finalized (not in S):**
  The distance stored is of the current best known route from the source to the node, but better routes may still be discovered.

### Part 3b: Why Each Phase Holds

> One to two bullets per phase. Maintenance must mention nonnegative edge weights.

- **Initialization : why the invariant holds before iteration 1:**
  Initilly we start with only the route from the source node to itself being known as 0. This is optimal since there are no negative edges. The other nodes are at infinite distance since routes to them have not been discovered.

- **Maintenance : why finalizing the min-dist node is always correct:**
  We can safely finalize the min-dist node because any later route we may discover will have to pass through nodes that are at least as far as the current route. Since there are no negative edges, these other routes cannot become shorter.

- **Termination : what the invariant guarantees when the algorithm ends:**
  When the algorithm ends the invariant gaurentees that all of the stored distances are the optimal distance since all nodes are now finalized.

### Part 3c: Why This Matters for the Route Planner

> One sentence connecting correct distances to correct routing decisions.

This matters for the route planner because it needs to compare routes using optimal distances to correctly choose the minimum route that collects all relics.

---

## Part 4: Search Design

### Why Greedy Fails

> State the failure mode. Then give a concrete counter-example using specific node names
> or costs (you may use the illustration example from the spec). Three to five bullets.

- **The failure mode:** 
A greedy algorithm will choose the next closest unvisited relic repeatedly without considering how that will effect the total route cost through future relics.
- **Counter-example setup:** 
S: [(R1, 1), (R2, 2)]
R1: [(R2, 100), (T, 1)]
R2: [(R1, 5), (T, 1)]
T: []
- **What greedy picks:** 
Greedy starts at S and selects R1 since it is closest S->R1 cost=1, then R2 since it is the only remaining and closest unvisited relic R1->R2 cost=100, then exits R2->T cost=1. total cost=102
- **What optimal picks:**
Optimal starts at S and selects R2 S->R2 cost=2, then R1 R2->R1 cost=5, then exits R1->T cost=1. total cost=8
- **Why greedy loses:** 
Because greedy does not concider the future travel costs for the remaining relics, the choices that are locally optimal at each step do not guarantee the global optimal.

### What the Algorithm Must Explore

> One bullet. Must use the word "order."

- The algorithm must explore difrent possible orders of collecting relics because the total cost depends on the order that relics are collected in.

---

## Part 5: State and Search Space

### Part 5a: State Representation

> Document the three components of your search state as a table.
> Variable names here must match exactly what you use in torchbearer.py.

| Component | Variable name in code | Data type | Description |
|---|---|---|---|
| Current location | current_loc | node | The current node that the torchbearer is located at |
| Relics already collected | relics_visited_order | list[node] | This stores the visited relics in a list in the order they were collected |
| Fuel cost so far | cost_so_far | float | The total amount of fuel needed for the currently considerd route |

### Part 5b: Data Structure for Visited Relics

> Fill in the table.

| Property | Your answer |
|---|---|
| Data structure chosen | list[node] |
| Operation: check if relic already collected | Time complexity: O(n) |
| Operation: mark a relic as collected | Time complexity: O(n) |
| Operation: unmark a relic (backtrack) | Time complexity: O(1) |
| Why this structure fits | The list structure fits for relics_visited_order because it functions like a stack for backtracking since relics are removed and readded in the same order. A list is also apropriate for relics_remaining since it is easy to search and modify. |

### Part 5c: Worst-Case Search Space

> Two bullets.

- **Worst-case number of orders considered:** k!
- **Why:** there are k! possible ways to order k relics, and in the worst case the algorithm may not be able to prune any of them.

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

> Three bullets.

- **What is tracked:** The optimal fuel cost for a complete route that starts at start, collects all relics, and ends at the exit.
- **When it is used:** It is used in the pruning stage, and updated when a new and more optimal route is discovered.
- **What it allows the algorithm to skip:** It allows the algorithm to to identify incomplete routes that can be pruned early if their cost is already more than the best solution's.

### Part 6b: Lower Bound Estimation

> Three bullets.

- **What information is available at the current state:** the torchbearer's current location, unvisited relics, the current route's cost.
- **What the lower bound accounts for:** It conciders the lowest possible extra cost that could complete the route.
- **Why it never overestimates:** It cannot overestimate because cost_so_far is the cost of the current partial path, and all edges have non negative weights so the lowest posible cost the current route could have when completed is its current cost.

### Part 6c: Pruning Correctness

> One to two bullets. Explain why pruning is safe.

- For any incomplete route that already has cost_so_far > best[0], since the rest of the route must add a non negative cost, it can never have a final cost less than cost_so_far. 
- Since we have a complete route with a lower cost, the current route is not optimal and can be pruned.

---

## References

> Bullet list. If none beyond lecture notes, write that.

- Lecture notes only.
