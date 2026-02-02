def sort_func(s: str) -> tuple[str, int]:
    return (s, len(s))


set1 = []
set2 = []

set1_length = int(input())

for i in range(set1_length):
    set1.append(input())

set2_length = int(input())

for i in range(set2_length):
    set2.append(input())


set_union = set1.copy()

for item in set2:
    if not (item in set1):
        set_union.append(item)

set_union.sort(key = sort_func)

set_intersection = []

for item1 in set1:
    for item2 in set2:
        if item1 == item2:
            set_intersection.append(item1)

set_intersection.sort(key = sort_func)

set_cartesian_product = []
for thing1 in set1:
    for thing2 in set2:
        set_cartesian_product.append(thing1 + " " + thing2)

set_cartesian_product.sort(key=sort_func)

for item in set_union:
    print(item)

print()

for item in set_intersection:
    print(item)

print()

for item in set_cartesian_product:
    print(item)