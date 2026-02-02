A, B, C = map(int, input().split())

supported_pairs = {(A, B)}

c_limit = (A + C, B + C)

pair = (A, B)
pair_x = A
pair_y = B
while c_limit not in supported_pairs:
    pair_x += 1
    pair_y += 1

    pair = (pair_x, pair_y)

    supported_pairs.add((A, pair_y))
    supported_pairs.add((pair_x, B))
    supported_pairs.add(pair)

    for x in range(A + 1, pair_x):
        supported_pairs.add((x, pair_y))
    for y in range(B + 1, pair_y):
        supported_pairs.add((pair_x, y))

for pair in supported_pairs:
    print(f"{pair[0]} {pair[1]}")