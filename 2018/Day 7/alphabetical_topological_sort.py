def topological_sort(dependencies, all_steps):
    remaining_steps = sorted(all_steps)
    while remaining_steps:
        for step in remaining_steps:
            if not any(d in remaining_steps for d in dependencies[step]):
                yield step
                remaining_steps.remove(step)
                break


with open('data.txt', 'r') as fp:
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

print(''.join(topological_sort(dependencies, all_steps)))