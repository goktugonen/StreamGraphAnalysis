#!/usr/bin/env python3
import csv
from datetime import datetime

NODE_CSV = 'node_table_terror_network_dated.csv'
EDGE_CSV = 'edge_table_terror_network_dated.csv'
OUTPUT = 'terror_external.sga'

def parse_date(value: str) -> datetime.date:
    return datetime.strptime(value, '%d.%m.%Y').date()

# Load nodes
def load_nodes():
    nodes = []
    with open(NODE_CSV, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            nodes.append((row['ID'], parse_date(row['First_Date']), parse_date(row['Last_Date'])))
    return nodes

# Load edges
def load_edges():
    edges_set = set()
    with open(EDGE_CSV, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            edges_set.add((row['Source'], row['Target'], parse_date(row['First_Date']), parse_date(row['Last_Date'])))
    return list(edges_set)

nodes = load_nodes()
edges = load_edges()

all_dates = [d for _, d, _ in nodes] + [d for _, _, d in nodes] \
            + [d for _, _, d, _ in edges] + [d for _, _, _, d in edges]
start = min(all_dates)
end = max(all_dates)
lifespan = (end - start).days + 1

# Map node ids to indices
node_index = {nid: i for i, (nid, _, _) in enumerate(nodes)}

# Collect events
events = []
for nid, fd, ld in nodes:
    s = (fd - start).days
    e = (ld - start).days + 1
    idx = node_index[nid]
    events.append((s, '+', 'N', idx))
    events.append((e, '-', 'N', idx))

for src, tgt, fd, ld in edges:
    s = (fd - start).days
    e = (ld - start).days + 1
    events.append((s, '+', 'L', node_index[src], node_index[tgt]))
    events.append((e, '-', 'L', node_index[src], node_index[tgt]))

# Sort events chronologically
events.sort(key=lambda x: (x[0], 0 if x[1] == '-' else 1))

with open(OUTPUT, 'w', encoding='utf-8') as out:
    out.write('SGA External version 1.0.0\n\n')
    out.write('[General]\n')
    out.write(f'Lifespan=(0 {lifespan})\n')
    out.write('TimeScale=1\n\n')
    out.write('[Events]\n')
    for ev in events:
        if ev[2] == 'N':
            t, sign, _, idx = ev
            out.write(f'{t} {sign} N {idx}\n')
        else:
            t, sign, _, i, j = ev
            out.write(f'{t} {sign} L {i} {j}\n')
    out.write('\n[EndOfStream]\n')
