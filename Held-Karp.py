# https://github.com/CarlEkerot/held-karp/tree/master
import itertools
import sys


def readAdjacencyMatrix(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

            adjacency_matrix = [list(map(int, line.strip().split())) for line in lines]

            return adjacency_matrix
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def heldKarp(dists):
    n = len(dists)
    C = {}

    for k in range(1, n):
        C[(1 << k, k)] = (dists[0][k], 0)
    
    for subset_size in range(2, n):
        for subset in itertools.combinations(range(1, n), subset_size):
            
            bits = 0
            for bit in subset:
                bits |= 1 << bit

            for k in subset:
                prev = bits & ~(1 << k)

                res = []
                for m in subset:
                    if m == 0 or m == k:
                        continue
                    res.append((C[(prev, m)][0] + dists[m][k], m))
                C[(bits, k)] = min(res)

    
    bits = (2**n - 1) - 1

    res = []
    for k in range(1, n):
        res.append((C[(bits, k)][0] + dists[k][0], k))
    opt, parent = min(res)

    path = []
    for i in range(n - 1):
        path.append(parent)
        new_bits = bits & ~(1 << parent)
        _, parent = C[(bits, parent)]
        bits = new_bits

    path.append(0)

    return opt, list(reversed(path))


def main():
    arg =  sys.argv[1]

    dists = readAdjacencyMatrix(arg)

    print(heldKarp(dists))


if __name__ == '__main__':
    main()