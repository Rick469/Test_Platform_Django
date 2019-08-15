from b import line_sum

l = [1, 5, 18, 3, 27, 11, 5, 3, 101]
for target in range(1, 175):
    r = line_sum(l, target)
    print(r[0], target)
    if r[0]:
        assert sum(r[0]) == target