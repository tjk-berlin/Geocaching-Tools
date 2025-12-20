import heapq
from math import inf

def dijkstra(graph, start):
    dist = {node: inf for node in graph}
    dist[start] = 0
    pq = [(0, start)]
    prev = {start: None}

    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        for v, w in graph[u].items():
            nd = d + w
            if nd < dist.get(v, inf):
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    return dist, prev

def reconstruct_path(prev, target):
    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        cur = prev.get(cur)
    return list(reversed(path))

# ----------------------------
# Muster-Deutschland-Graph
# ----------------------------
# Startknoten zentral gewählt: Kassel (KAS)
graph = {
    "KAS": {"HNO": 2, "FRA": 4, "ERF": 3, "KOL": 5, "LEI": 7},

    # Nord-Korridor
    "HNO": {"KAS": 2, "HAM": 3, "BRE": 4, "MAG": 4},
    "HAM": {"HNO": 3, "KIE": 2, "BRE": 3},
    "KIE": {"HAM": 1, "FLN": 2},
    "FLN": {"KIE": 1},

    # West / Rhein / Ruhr
    "KOL": {"KAS": 5, "DUS": 2, "BON": 1, "AACH": 3},
    "BON": {"KOL": 1, "TRI": 6, "FRA": 3},
    "DUS": {"KOL": 2, "AACH": 4, "BRE": 5},
    "AACH": {"KOL": 3, "DUS": 4},
    "TRI": {"BON": 6, "SAA": 4},
    "SAA": {"TRI": 4, "FRA": 4},

    # Süd / Bayern
    "FRA": {"KAS": 4, "BON": 3, "STR": 4, "NUR": 6, "STU": 5},
    "STR": {"FRA": 4, "FRE": 3},
    "FRE": {"STR": 3, "STU": 3},
    "STU": {"FRA": 5, "ULM": 2, "FRE": 3},
    "ULM": {"STU": 2, "MUC": 6, "REG": 5},
    "NUR": {"FRA": 6, "REG": 3, "MUC": 5},
    "REG": {"NUR": 3, "ULM": 5, "MUC": 4},
    "MUC": {"NUR": 5, "ULM": 6, "REG": 4},

    # Ost-Korridor
    "ERF": {"KAS": 3, "LEI": 4},
    "LEI": {"KAS": 7, "ERF": 4, "DRE": 8, "MAG": 5},
    "MAG": {"HNO": 4, "LEI": 5, "BER": 6},
    "BER": {"MAG": 6, "ROS": 6, "DRE": 10},
    "ROS": {"BER": 6},

    "DRE": {"LEI": 8, "BER": 10, "BAU": 7},
    "BAU": {"DRE": 7, "GOL": 9},
    "GOL": {"BAU": 9},

    # Nordwest
    "BRE": {"HNO": 4, "HAM": 3, "DUS": 5},
}

# ----------------------------
# 20 Endpunkte
# ----------------------------
endpoints = [
    "FLN", "GOL", "AACH", "TRI", "SAA",
    "FRA", "STR", "FRE", "STU", "ULM",
    "NUR", "REG", "MUC", "KOL", "DUS",
    "BON", "HAM", "BRE", "BER", "ROS"
]

# Koordinaten-Strings pro Endpoint
coords = {
    # Nord-Kandidaten
    "FRA": "N 52° 19.240",
    "FLN": "N 54° 46.812",
    "AACH": "N 50° 45.903",
    "TRI":  "N 49° 44.781",
    "SAA":  "N 49° 13.902",
    "STR":  "N 48° 33.418",
    "FRE":  "N 47° 58.731",
    "STU":  "N 48° 45.692",
    "ULM":  "N 48° 22.514",
    "NUR":  "N 49° 26.836",

    # Ost-Kandidaten
    "GOL": "E 13° 10.125",
    "BER": "E 13° 23.947",
    "REG": "E 12° 05.884",
    "ROS": "E 12° 07.391",
    "MUC": "E 11° 33.208",
    "HAM": "E 09° 59.774",
    "BRE": "E 08° 47.193",
    "KOL": "E 06° 56.604",
    "DUS": "E 06° 44.918",
    "BON": "E 07° 04.081",
}

# ----------------------------
# Auswertung
# ----------------------------
start = "KAS"
dist, prev = dijkstra(graph, start)

# nur die 20 Endpunkte betrachten
endpoint_dist = {ep: dist[ep] for ep in endpoints}

north_ep = min(endpoint_dist, key=endpoint_dist.get)  # kürzester -> Nord
east_ep  = max(endpoint_dist, key=endpoint_dist.get)  # längster -> Ost

print("Start:", start)
print("\nDistanzen zu Endpunkten:")
for ep, d in sorted(endpoint_dist.items(), key=lambda x: x[1]):
    print(f"  {ep:4s}  dist={d:>3}  path={reconstruct_path(prev, ep)}")

print("\n== Auswahl ==")
print("Nord (kürzester):", north_ep, "->", coords[north_ep])
print("Ost  (längster) :", east_ep,  "->", coords[east_ep])