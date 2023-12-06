import itertools
import time
import sys


def brute_force_tsp(dists):
    n = len(dists)

    min_cost = float('inf')
    best_path = None

    for path in itertools.permutations(range(1, n)):
        current_path = (0,) + path + (0,)
        current_cost = sum(dists[current_path[i]][current_path[i + 1]] for i in range(n))
        if current_cost < min_cost:
            min_cost = current_cost
            best_path = current_path
            writeBestPath("Brute-Force\log_brute_force.txt", best_path, min_cost)


    return min_cost, best_path


def writeBestPath(file_path, best_path, min_cost):
    try:
        with open(file_path, 'w') as file:
            file.write(f"Melhor caminho: {best_path}\n")
            file.write(f"Custo minimo: {min_cost}\n")
    except Exception as e:
        print(f"An error occurred: {e}")


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


def main():
    args = sys.argv[1]
    graph = readAdjacencyMatrix(args)

    min_cost_brute, best_path_brute = brute_force_tsp(graph)

    print("Melhor caminho:", best_path_brute)
    print("Custo minimo:", min_cost_brute)


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print("Tempo total de execucao:", end - start)