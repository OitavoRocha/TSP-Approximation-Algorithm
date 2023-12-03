import numpy as np

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

    matrix_values = readAdjacencyMatrix("tsp1_253.txt")
    nodes = len(matrix_values)
    
    matrix = np.array(matrix_values)

    MinSpanTree, cost = prim(matrix, nodes, num_edges)
    minimumPerfectWeightMatching(MinSpanTree, matrix, findOddDegreeNodes(MinSpanTree))
    print("MST")
    print(MinSpanTree)

    cycle = fleuryAlgo(MinSpanTree, 0)
    print(cycle)
    cycle = removeDuplicates(cycle)
    print(cycle)
    print(calculateCost(cycle, matrix))



"""
        0  1  2  3  4  5  6  7  8  9 10 
   0  [ 0  0  0  0  0  0  0 12  4  0  0]
   1  [ 0  0  0  0  0  0 72  0  0  0 12]
   2  [ 0  0  0  0  0  0  0  9  0  0 13]
   3  [ 0  0  0  0  4 12  0  0  0  0  0]
   4  [ 0  0  0  4  0  0  0  9  0  0  0]
   5  [ 0  0  0 12  0  0  0  0  0  3  0]
   6  [ 0 72  0  0  0  0  0  0  0 99  0]
   7  [12  0  9  0  9  0  0  0 15  0  0]
   8  [ 4  0  0  0  0  0  0 15  0  0  0]
   9  [ 0  0  0  0  0  3 99  0  0  0  0]
   10 [ 0 12 13  0  0  0  0  0  0  0  0]

   0, 8, 7, 2, 10, 1, 6, 9, 5, 3, 4, 7, 0
"""

"""
     0      1   2   3   4   5   6    7   8  9   10
  0  [0,   29, 20, 21, 16, 31, 100, 12, 4,  31, 18]
  1  [29,  0,  15, 29, 28, 40, 72,  21, 29, 41, 12]
  2  [20,  15, 0,  15, 14, 25, 81,  9,  23, 27, 13]
  3  [21,  29, 15, 0,  4,  12, 92,  12, 25, 13, 25]
  4  [16,  28, 14, 4,  0,  16, 94,  9,  20, 16, 22]
  5  [31,  40, 25, 12, 16, 0,  95,  24, 36, 3, 37 ]
  6  [100, 72, 81, 92, 94, 95, 0,   90, 101,99, 84]
  7  [12,  21, 9,  12, 9,  24, 90,  0,  15, 25, 13]
  8  [4,   29, 23, 25, 20, 36, 101, 15, 0,  35, 18]
  9  [31,  41, 27, 13, 16, 3,  99,  25, 35, 0,  38]
 10  [18,  12, 13, 25, 22, 37, 84,  13, 18, 38, 0 ]
"""

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
    main()

"""""
1.Create a minimum spanning tree T of G.
2.Let O be the set of vertices with odd degree in T. By the handshaking lemma, O has an even number of vertices.
3.Find a minimum-weight perfect matching M in the induced subgraph given by the vertices from O.
4.Combine the edges of M and T to form a connected multigraph H in which each vertex has even degree.
5.Form an Eulerian circuit in H.
6.Make the circuit found in previous step into a Hamiltonian circuit by skipping repeated vertices (shortcutting).


"""""
