import numpy as np
import time
import sys

INT_MAX = 9999999

def prim(matrix, nodes, num_edges):
    if num_edges == 0:
        return

    parents = [0] * nodes
    min_key, x, y = 0, 0, 0
    cost = 0
    minimum_spanning_tree = []

    for i in range(nodes):
        parents[i] = 0

    parents[0] = 1

    i = 0
    while i < nodes - 1:
        min_key = INT_MAX

        x, y = 0, 0

        for j in range(nodes):
            if parents[j] == 1:
                for k in range(nodes):
                    if parents[k] == 0 and matrix[j][k]:
                        if min_key > matrix[j][k]:
                            min_key = matrix[j][k]
                            x, y = j, k

        edge = (x, y)
        minimum_spanning_tree.append(edge)
        cost += matrix[x][y]
        parents[y] = 1
        i += 1

    adjacency_matrix = [[0] * nodes for _ in range(nodes)]
    for edge in minimum_spanning_tree:
        x, y = edge
        adjacency_matrix[x][y] = matrix[x][y]
        adjacency_matrix[y][x] = matrix[x][y]
        
    adjacency_matrix = np.array(adjacency_matrix)
    return adjacency_matrix, cost


def main():
    num_edges = 1
    args = sys.argv[1]

    matrix_values = readAdjacencyMatrix(args)
    nodes = len(matrix_values)
    
    matrix = np.array(matrix_values)

    MinSpanTree, cost = prim(matrix, nodes, num_edges)
    minimumPerfectWeightMatching(MinSpanTree, matrix, findOddDegreeNodes(MinSpanTree))

    cycle = fleuryAlgo(MinSpanTree, 0)
    cycle = removeDuplicates(cycle)
    print("Cycle: ", cycle)
    print(calculateCost(cycle, matrix))


def findOddDegreeNodes(minSpanTree):
    oddDegreeNodes = []
    for node in range(len(minSpanTree)):
        degree = 0
        for edge in range(len(minSpanTree)):
            if minSpanTree[node][edge] != 0:
                degree += 1
        if degree % 2 != 0:
            oddDegreeNodes.append(node)
    return oddDegreeNodes

def minimumPerfectWeightMatching(MinSpanTree, G, odd_vert):
    used = []
    all_matches = [(G[u][v], u, v) for u in odd_vert for v in odd_vert if u != v and u < v]
    all_matches.sort()
    for i in range(len(all_matches)):
        if all_matches[i][1] not in used and all_matches[i][2] not in used:
            MinSpanTree[all_matches[i][1]][all_matches[i][2]] = all_matches[i][0]  
            MinSpanTree[all_matches[i][2]][all_matches[i][1]] = all_matches[i][0]
            used.append(all_matches[i][1])
            used.append(all_matches[i][2])
        if len(used) == len(odd_vert):
            break
    
def fleuryAlgo(MinSpanTree, startNode):
    stack = []
    stack.append(startNode)
    circuit = []
    while len(stack) != 0:
        top = stack[-1]
        for i in range(len(MinSpanTree)):
            if MinSpanTree[top][i] != 0:
                stack.append(i)
                MinSpanTree[top][i] = 0
                MinSpanTree[i][top] = 0
                break
        if top == stack[-1]:
            circuit.append(stack.pop())
    return circuit

def removeDuplicates(circuit):
    cycle = [circuit[i] for i in range(len(circuit)) if circuit[i] not in circuit[:i]]
    cycle.append(circuit[0])
    return cycle

def calculateCost(cycle, G):
    cost = 0
    for i in range(len(cycle)-1):
        cost += G[cycle[i]][cycle[i+1]]
    return cost

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

if __name__ == '__main__':
    starTime = time.time()
    main()
    print("Time taken: ", time.time() - starTime)