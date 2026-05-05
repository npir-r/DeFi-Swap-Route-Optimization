import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os

def main():
    print("🚀 DeFi Smart Routing Optimization Started...\n")

    data_path = 'data/dex_pools.csv'
    if not os.path.exists(data_path):
        data_path = '../data/dex_pools.csv'
        
    try:
        df = pd.read_csv(data_path)
        print(f"✅ Loaded {len(df)} liquidity pools from database.")
    except FileNotFoundError:
        print(f"❌ Error: Could not find dataset. Check folder structure.")
        return

    G = nx.DiGraph()

    for index, row in df.iterrows():
        total_cost = row['commission'] + row['slippage']
        G.add_edge(row['token_in'], row['token_out'], weight=total_cost)
        
    print(f"✅ Network constructed with {G.number_of_nodes()} tokens.\n")

    source_token, target_token = 'USDC', 'ETH'

    try:
        optimal_path = nx.shortest_path(G, source=source_token, target=target_token, weight='weight')
        optimal_cost = nx.shortest_path_length(G, source=source_token, target=target_token, weight='weight')
        
        print("-" * 40)
        print("🎯 OPTIMIZATION RESULTS")
        print("-" * 40)
        print(f"Optimal Route: {' → '.join(optimal_path)}")
        print(f"Total Lowest Cost: {optimal_cost:.4f}%\n")
        
        direct_cost = G[source_token][target_token]['weight']
        print(f"💡 Managerial Insight: Multi-hop route saves {direct_cost - optimal_cost:.4f}% compared to direct swap!")

    except nx.NetworkXNoPath:
        print("❌ No route exists.")
        return

    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42)
    nx.draw_networkx_nodes(G, pos, node_size=2000, node_color='#A0C4FF', edgecolors='#000000')
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    nx.draw_networkx_edges(G, pos, edge_color='#CCCCCC', arrows=True)
    
    optimal_edges = [(optimal_path[i], optimal_path[i+1]) for i in range(len(optimal_path)-1)]
    nx.draw_networkx_edges(G, pos, edgelist=optimal_edges, edge_color='#FF9F1C', width=3, arrows=True)
    
    edge_labels = {(u, v): f"{d['weight']:.2f}%" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    
    plt.title("DeFi Liquidity Network Topology\n(Orange Path = Optimal Cost Route)", fontsize=14, fontweight='bold')
    plt.axis('off')
    
    os.makedirs('results', exist_ok=True)
    plt.savefig("results/network_visualization.png", format="png", dpi=300, bbox_inches='tight')
    print(f"\n📊 Network visualization saved to 'results/network_visualization.png'.")

if __name__ == "__main__":
    main()