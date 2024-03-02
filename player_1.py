from typing import List, Tuple

def make_move(N, edges):
    is_horizontal = random.choice([True, False])
    if is_horizontal:
        x = random.randint(0, N - 2)
        y = random.randint(0, N - 1)
        x1, y1 = x, y
        x2, y2 = x + 1, y
    else:
        x = random.randint(0, N - 1)
        y = random.randint(0, N - 2)
        x1, y1 = x, y
        x2, y2 = x, y + 1

    return x1, y1, x2, y2
