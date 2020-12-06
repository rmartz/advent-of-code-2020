from operator import itemgetter


def topological_sort(dependencies, step_costs, num_pipelines):
    remaining_steps = sorted(step_costs.keys())
    current_time = 0
    pipelines = []
    while remaining_steps:
        for step in remaining_steps:
            if (
                len(pipelines) < num_pipelines
                and not any(step == pipeline_step for _, pipeline_step in pipelines)
                and not any(d in remaining_steps for d in dependencies[step])
            ):
                next_time = current_time + step_costs[step]
                pipelines.append((next_time, step))
                break
        else:
            # Unable to add anything to pipeline, advance time
            print(pipelines)
            next_tuple = min(pipelines, key=itemgetter(0))
            pipelines.remove(next_tuple)
            next_time, next_step = next_tuple
            print("Removing {}".format(next_step))
            remaining_steps.remove(next_step)
            current_time = next_time
    return current_time


with open("data.txt", "r") as fp:
    records = [(row[5], row[36]) for row in fp]

print(records)

all_steps = set()
for a, b in records:
    all_steps.add(a)
    all_steps.add(b)

dependencies = dict((step, set()) for step in all_steps)

for parent, child in records:
    dependencies[child].add(parent)
print(dependencies)

ordered_steps = sorted(all_steps)
step_costs = dict(
    (step, 60 + index) for index, step in enumerate(ordered_steps, start=1)
)

print(topological_sort(dependencies, step_costs, 4))
