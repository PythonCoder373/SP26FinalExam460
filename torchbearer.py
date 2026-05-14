"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: Philip Revak
Student ID:   131950621

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
"""

import heapq


# =============================================================================
# PART 1
# =============================================================================

def explain_problem():
    """
    Returns
    -------
    str
        Your Part 1 README answers, written as a string.
        Must match what you wrote in README Part 1.

    TODO
    """
    readme_answers= (
        "- **Why a single shortest-path run from S is not enough:**\n"
        "A single shortest-path run only finds the shortest path to individual relics. This problem requires finding a optimal route that visites every relic at least once.\n"
        "- **What decision remains after all inter-location costs are known:**\n"
        "After the distances from every node to all others are known, we still must determine the optimal route that visites every relic at least once, and begins at the start and ends at the exit.\n"
        "- **Why this requires a search over orders (one sentence):**\n"
        "A search over orders is required because the order that relics are visited determines the total cost, so we must find the optimal order that minimizes the cost."
    )
    return readme_answers


# =============================================================================
# PART 2
# =============================================================================

def select_sources(spawn, relics, exit_node):
    """
    Parameters
    ----------
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    list[node]
        No duplicates. Order does not matter.

    TODO
    """
    sources=[spawn]
    for i in relics:
        if i not in sources:
            sources.append(i)
    return sources


def run_dijkstra(graph, source):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
        graph[u] = [(v, cost), ...]. All costs are nonnegative integers.
    source : node

    Returns
    -------
    dict[node, float]
        Minimum cost from source to every node in graph.
        Unreachable nodes map to float('inf').

    TODO
    """
    distances={}
    for node in graph:
        distances[node] = float('inf')

    distances[source] = 0
    pqueue=[(0,source)]

    while len(pqueue) > 0:
        distance, node = heapq.heappop(pqueue)

        if distance > distances[node]: # better path is already known
            continue

        for neighbor, cost in graph[node]:
            dist= cost + distance

            if dist < distances[neighbor]:
                distances[neighbor] = dist
                heapq.heappush(pqueue,(dist,neighbor))

    return distances


def precompute_distances(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    dict[node, dict[node, float]]
        Nested structure supporting dist_table[u][v] lookups
        for every source u your design requires.

    TODO
    """
    sorces=select_sources(spawn, relics, exit_node)
    distanceTable={}
    for source in sorces:
        distanceTable[source] = run_dijkstra(graph, source)

    return distanceTable


# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():
    """
    Returns
    -------
    str
        Your Part 3 README answers, written as a string.
        Must match what you wrote in README Part 3.

    TODO
    """
    readme_answers= (
        "### Part 3a: What the Invariant Means\n"
        "- **For nodes already finalized (in S):**\n"
        "The distance discovered by the algorithm is the optimal distance from the source to the node, and no other path can be better.\n\n"

        "- **For nodes not yet finalized (not in S):**\n"
        "The distance stored is of the current best known route from the source to the node, but better routes may still be discovered.\n\n"


        "### Part 3b: Why Each Phase Holds\n"
        "- **Initialization : why the invariant holds before iteration 1:**\n"
        "Initilly we start with only the route from the source node to itself being known as 0. This is optimal since there are no negative edges. The other nodes are at infinite distance since routes to them have not been discovered.\n\n"

        "- **Maintenance : why finalizing the min-dist node is always correct:**\n"
        "We can safely finalize the min-dist node because any later route we may discover will have to pass through nodes that are at least as far as the current route. Since there are no negative edges, these other routes cannot become shorter.\n\n"

        "- **Termination : what the invariant guarantees when the algorithm ends:**\n"
        "When the algorithm ends the invariant gaurentees that all of the stored distances are the optimal distance since all nodes are now finalized.\n\n"

        "### Part 3c: Why This Matters for the Route Planner\n"
        "This matters for the route planner because it needs to compare routes using optimal distances to correctly choose the minimum route that collects all relics."
    )
    return readme_answers


# =============================================================================
# PART 4
# =============================================================================

def explain_search():
    """
    Returns
    -------
    str
        Your Part 4 README answers, written as a string.
        Must match what you wrote in README Part 4.

    TODO
    """
    readme_answers= (
        "### Why Greedy Fails\n"
        "- **The failure mode:**\n"
        "A greedy algorithm will choose the next closest unvisited relic repeatedly without considering how that will effect the total route cost through future relics.\n"
        "- **Counter-example setup:**\n"
        "S: [(R1, 1), (R2, 2)]\n"
        "R1: [(R2, 100), (T, 1)]\n"
        "R2: [(R1, 5), (T, 1)]\n"
        "T: []\n"
        "- **What greedy picks:**\n"
        "Greedy starts at S and selects R1 since it is closest S->R1 cost=1, then R2 since it is the only remaining and closest unvisited relic R1->R2 cost=100, then exits R2->T cost=1. total cost=102\n"
        "- **What optimal picks:**\n"
        "Optimal starts at S and selects R2 S->R2 cost=2, then R1 R2->R1 cost=5, then exits R1->T cost=1. total cost=8\n"
        "- **Why greedy loses:**\n"
        "Because greedy does not concider the future travel costs for the remaining relics, the choices that are locally optimal at each step do not guarantee the global optimal.\n\n"

        "### What the Algorithm Must Explore\n"
        "- The algorithm must explore difrent possible orders of collecting relics because the total cost depends on the order that relics are collected in."
    )
    return readme_answers


# =============================================================================
# PARTS 5 + 6
# =============================================================================

def find_optimal_route(dist_table, spawn, relics, exit_node):
    """
    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
        Output of precompute_distances.
    spawn : node
    relics : list[node]
        Every node in this list must be visited at least once.
    exit_node : node
        The route must end here.

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    TODO
    """
    best = [float('inf'), []]
    _explore(dist_table, spawn, relics, [], 0, exit_node, best)

    return (best[0],best[1])


def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
    """
    Recursive helper for find_optimal_route.

    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
    current_loc : node
    relics_remaining : collection
        Your chosen data structure from README Part 5b.
    relics_visited_order : list[node]
    cost_so_far : float
    exit_node : node
    best : list
        Mutable container for the best solution found so far.

    Returns
    -------
    None
        Updates best in place.

    TODO
    Implement: base case, pruning, recursive case, backtracking.

    REQUIRED: Add a 1-2 sentence comment near your pruning condition
    explaining why it is safe (cannot skip the optimal solution).
    This comment is graded.
    """

    if len(relics_remaining)==0: # base case
        if dist_table[current_loc][exit_node]==float('inf'):
            return
        else:
            cost = cost_so_far + dist_table[current_loc][exit_node]
            if cost<best[0]:
                best[0]=cost
                best[1]=relics_visited_order[:]
            return
    
    # pruning
    # if the current route's cost is already at least as much as the best soloutions total cost then it cannot be better since all distances are non negative
    if cost_so_far>best[0]:
        return
    
    # recursive case
    for relic in relics_remaining[:]:
        distance=dist_table[current_loc][relic]

        relics_remaining.remove(relic)
        relics_visited_order.append(relic)

        _explore(dist_table, relic, relics_remaining, relics_visited_order, cost_so_far + distance, exit_node, best)

        # backtracking
        relics_visited_order.pop()
        relics_remaining.append(relic)
    
    return


# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    TODO
    """
    pass


# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

def _run_tests():
    print("Running provided tests...")

    # Test 1: Spec illustration. Optimal cost = 4.
    graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
    cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
    print(f"  Test 1 passed  cost={cost}  order={order}")

    # Test 2: Single relic. Optimal cost = 5.
    graph_2 = {
        'S': [('R', 3)],
        'R': [('T', 2)],
        'T': []
    }
    cost, order = solve(graph_2, 'S', ['R'], 'T')
    assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
    print(f"  Test 2 passed  cost={cost}  order={order}")

    # Test 3: No valid path to exit. Must return (inf, []).
    graph_3 = {
        'S': [('R', 1)],
        'R': [],
        'T': []
    }
    cost, order = solve(graph_3, 'S', ['R'], 'T')
    assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
    print(f"  Test 3 passed  cost={cost}")

    # Test 4: Relics reachable only through intermediate rooms.
    # Optimal cost = 6.
    graph_4 = {
        'S': [('X', 1)],
        'X': [('R1', 2), ('R2', 5)],
        'R1': [('Y', 1)],
        'Y': [('R2', 1)],
        'R2': [('T', 1)],
        'T': []
    }
    cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
    assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
    print(f"  Test 4 passed  cost={cost}  order={order}")

    # Test 5: Explanation functions must return non-placeholder strings.
    for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
        result = fn()
        assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
            f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
    print("  Test 5 passed  explanation functions are non-empty")

    print("\nAll provided tests passed.")


if __name__ == "__main__":
    _run_tests()
