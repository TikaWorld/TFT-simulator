import copy
from app.champion.state import State


def find_proximate(cur, include_friendly=False):
    proximate = {"distance": None, "target": []}
    visited = {}
    search_results = _bfs_champion_search(cur, visited)

    for r in search_results:
        target = r[0]
        path = r[1]
        if not include_friendly and target.champion.team == cur.champion.team:
            continue
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


def get_distance(cur, champion):
    visited = {}
    search_results = _bfs_champion_search(cur, visited, conflict=False)
    for r in search_results:
        target = r[0]
        path = r[1]
        distance = len(path)
        if target.champion == champion:
            return distance

    return None


def get_path(cur, champion):
    visited = {}
    search_results = _bfs_champion_search(cur, visited)
    for r in search_results:
        target = r[0]
        path = r[1]
        if target.champion == champion:
            return path

    return None


def _bfs_champion_search(node, visited, conflict=True):
    result = []
    if node.id in visited.keys():
        return result
    visited[node.id] = True

    nodes = [[n, []] for n in node.connect]
    while nodes:
        n = nodes.pop(0)
        if n[0].id in visited.keys() and visited[n[0].id]:
            continue
        visited[n[0].id] = True
        n[1].append(n[0])
        if n[0].champion:
            if State.BANISHES in n[0].champion.state:
                continue
            result.append([n[0], n[1]])
            if conflict:
                continue
        nodes.extend([[c, copy.copy(n[1])] for c in n[0].connect])
    return result
