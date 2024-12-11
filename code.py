
from collections import defaultdict
from itertools import combinations
from typing import List, Tuple
import copy

def solve(job_times: List[int], dependencies: List[Tuple[int, int]], num_machines: int) -> Tuple[int, List[List[int]]]:
    # Initialize in-degree and dependants
    in_degree = defaultdict(int)
    dependants = defaultdict(list)

    for job, dependent in dependencies:
        dependants[job].append(dependent)
        in_degree[dependent] += 1

    # Find jobs with zero in-degree
    zero_in_degree = [job for job in range(len(job_times)) if in_degree[job] == 0]

    machine_times = [0] * num_machines
    job_availabile_times = [0] * len(job_times)

    assignments = [[] for _ in range(num_machines)]

    min_assignments = None
    min_makespan = float('inf')

    # Backtracking function to find the minimum makespan
    def backtrack(zero_in_degree: List[int], machine_times: List[int], current_max_makespan: int, job_availabile_times: List[int], assignments: List[int]) -> int:
        nonlocal min_assignments, min_makespan

        # Base case: If there are no jobs with zero in-degree
        if not zero_in_degree:
            if current_max_makespan < min_makespan:
                min_assignments = copy.deepcopy(assignments)
                min_makespan = current_max_makespan

        # Prune the search if the current makespan is greater than the minimum makespan
        if current_max_makespan >= min_makespan:
            return

        # Find the machines with the minimum time
        min_machine_time = min(machine_times)
        available_machines = [i for i, time in enumerate(machine_times) if time == min_machine_time]

        # Generate job combinations for available machines
        num_jobs_to_assign = min(len(zero_in_degree), len(available_machines))
        job_combinations = combinations(zero_in_degree, num_jobs_to_assign)

        for jobs in job_combinations:
            new_zero_in_degree = [job for job in zero_in_degree if job not in jobs]
            machine_times_backup = machine_times[:]
            current_max_makespan_new = current_max_makespan
            job_availabile_times_backup = job_availabile_times[:]

            for i, job in enumerate(jobs):
                machine_index = available_machines[i]
                if job_availabile_times[job] > machine_times[machine_index]:
                    machine_times[machine_index] = job_availabile_times[job] + job_times[job]
                else:
                    machine_times[machine_index] += job_times[job]

                assignments[machine_index].append(job)

                current_max_makespan_new = max(current_max_makespan_new, machine_times[machine_index])

                for dependent in dependants[job]:
                    in_degree[dependent] -= 1
                    if in_degree[dependent] == 0:
                        new_zero_in_degree.append(dependent)

                    job_availabile_times[dependent] = max(job_availabile_times[dependent], machine_times[machine_index])

            backtrack(new_zero_in_degree, machine_times, current_max_makespan_new, job_availabile_times, assignments)

            for i, job in enumerate(jobs):
                for dependent in dependants[job]:
                    in_degree[dependent] += 1

                machine_index = available_machines[i]
                machine_times[machine_index] = machine_times_backup[machine_index]
                job_availabile_times = job_availabile_times_backup[:]
                assignments[machine_index].pop()

        return min_makespan

    # Calculate the minimum makespan
    backtrack(zero_in_degree, machine_times, 0, job_availabile_times, assignments)

    return min_makespan, min_assignments

# Job times and dependencies
job_times = [3, 8, 7, 6, 2, 5, 1, 4, 8, 1] 
dependencies = [(0, 2), (1, 2), (2, 3), (3, 4), (3, 5), (6, 3), (1, 9)]
num_machines = 2

min_makespan, min_assignments = solve(job_times, dependencies, num_machines)
print("Minimum makespan:", min_makespan)
print("Assignments:", min_assignments)
