import matplotlib.pyplot as plt

# Graph data: (name, vertices, edges)
graphs = [
    ("G67", 10000, 20000),
    ("TSOPF_RS_b9_c6", 7224, 54082),
    ("nemeth14", 9506, 252825),
    ("nemeth11", 9506, 208885),
    ("nemeth07", 9506, 202159),
    ("nemeth20", 9506, 490688),
    ("nemeth08", 9506, 202161),
    ("nemeth24", 9506, 758028),
    ("nemeth19", 9506, 413904),
    ("Chevron1", 37365, 330633),
    ("nemeth02", 9506, 202157),
    ("bcsstk18", 11948, 80519),
    ("nemeth25", 9506, 760632),
    ("1138_bus", 1138, 2596),
    ("nemeth26", 9506, 760633),
    ("nemeth10", 9506, 205477),
    ("nemeth23", 9506, 758158),
    ("nemeth18", 9506, 352370),
    ("nemeth04", 9506, 202157),
    ("exdata_1", 6001, 1137751),
    ("nemeth13", 9506, 241989),
    ("nemeth17", 9506, 319563),
    ("TSOPF_RS_b39_c7", 14098, 252446),
    ("nemeth06", 9506, 202157),
    ("TSOPF_RS_b162_c3", 15374, 610299),
    ("human_gene2", 14340, 9041364),
    ("TSOPF_RS_b39_c19", 38098, 684206),
    ("jan99jac120sc", 41374, 260202),
    ("nemeth12", 9506, 228162),
    ("TSOPF_RS_b162_c4", 20374, 812749),
    ("nemeth05", 9506, 202157),
    ("nemeth21", 9506, 591626),
    ("nemeth22", 9506, 684169),
    ("TSOPF_FS_b300", 29214, 2203949),
    ("t2em", 921632, 4590832),
    ("shyy161", 76480, 329762),
    ("StocF-1465", 1465137, 11235263),
    ("nemeth16", 9506, 298259),
    ("nemeth03", 9506, 202157),
    ("TSOPF_RS_b162_c1", 5374, 205399),
    ("human_gene1", 22283, 12345963),
    ("nemeth09", 9506, 202506),
    ("nemeth01", 9506, 367280),
    ("TSOPF_RS_b678_c1", 18696, 4396289),
    ("mouse_gene", 45101, 14506196),
    ("TSOPF_RS_b39_c30", 60098, 1079986),
    ("TSOPF_RS_b2383", 38120, 16171169),
    ("TSOPF_RS_b2383_c1", 38120, 16171169),
    ("TSOPF_RS_b2052_c1", 25626, 6761100),
    ("TSOPF_FS_b300_c2", 56814, 4391071),
    ("TSOPF_RS_b678_c2", 35696, 8781949),
    ("TSOPF_FS_b300_c3", 84414, 6578753)
]

# Calculate densities
densities = []
num_vertices = []

for name, V, E in graphs:
    if V > 1:
        density = E/V
        densities.append(density)
        num_vertices.append(V)

# Plotting
plt.figure(figsize=(10, 6))
plt.scatter(num_vertices, densities, color='blue', edgecolors='k')
plt.xscale('log')
plt.yscale('log')
plt.xlabel("Number of Vertices (log scale)")
plt.ylabel("Graph Density = E / V (log scale)")
plt.title("Scatter Plot of Graph Density vs Number of Vertices")
plt.grid(True, which="both", ls="--", linewidth=0.5)
plt.show()
