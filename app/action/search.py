from .. import field
import copy

def find_proximate(v):
    cur = field.FIELD[v[0]][v[1]]
    visited = [False for _ in range(field.WIDTH*field.HEIGHT)]
    r = _bfs_champion_search(cur, visited)
    print(r)

def _bfs_champion_search(node, visited):
    count = 0
    result = []
    if visited[node.id]:
        return result
    visited[node.id] = True

    nodes = [[n, []] for n in node.connect]
    find = []
    while nodes:
        n = nodes.pop(0)
        if visited[n[0].id]:
            continue
        visited[n[0].id] = True
        n[1].append(n[0])
        if n[0].champion:
            result.append([n[0], n[1]])
            continue
        nodes.extend([[c, copy.deepcopy(n[1])] for c in copy.deepcopy(n[0].connect)])
    return result

