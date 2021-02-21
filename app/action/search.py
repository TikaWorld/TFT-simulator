import copy

def find_proximate(v, field):
    proximate = {"distance": None, "target": []}
    cur = field[v[0]][v[1]]
    visited = [False for _ in range(len(field[0])*len(field))]
    search_results = _bfs_champion_search(cur, visited)
    
    for r in search_results:
        target = r[0]
        path = r[1]
        distance = len(path)
        if proximate["distance"] is None:
            proximate["distance"] = distance
            proximate["target"].append(target)
        elif proximate["distance"] == distance:
            proximate["target"].append(target)
        elif proximate["distance"] > distance:
            proximate["target"] = [target]
            proximate["distance"] = distance
    
    return proximate["distance"], proximate["target"]


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
        nodes.extend([[c, copy.copy(n[1])] for c in n[0].connect])
    return result

