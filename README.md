# DeFi Smart Routing Engine: Minimizing Transaction Costs via Network Optimization

## 1. Real-World Problem Context
In the rapidly expanding decentralized finance (DeFi) ecosystem, cryptocurrency traders frequently exchange assets across fragmented liquidity pools spread over multiple platforms (e.g., Uniswap, SushiSwap, Balancer). 

**The Business Challenge:** When users want to swap Token A for Token B, a direct liquidity pool either might not exist or might suffer from severe price impact (slippage) due to low liquidity. Consequently, traders must execute multi-hop transactions (e.g., USDC → USDT → ETH). Each hop incurs cumulative costs:
1.  **Commission Fees:** Platform-specific percentage fees (0.01% - 0.5%).
2.  **Slippage:** The hidden cost of price impact based on trade size vs. pool liquidity.

**The MIS & FinTech Impact:** For an automated market maker (AMM) or a digital platform's traffic management system, routing efficiency is a massive competitive advantage. A retail user swapping $10,000 might lose $100 to suboptimal routing, while institutional traders face millions in unnecessary friction. This project develops the algorithmic core of a "Smart Router" (Decision Support System) that programmatically finds the minimum-cost execution path.

## 2. Problem Definition
The objective of this network optimization model is to determine the most cost-efficient transaction route from a Source Token to a Target Token across a fragmented DeFi network.

*   **Objective Function:** Minimize the total transaction cost $Z = \sum (Commission_i + Slippage_i)$ for all traversed liquidity pools.
*   **Constraints:**
    *   The path must sequentially connect the source node to the destination node.
    *   Every edge (pool) utilized must have sufficient liquidity (Capacity >= Trade Volume).
    *   Non-negativity: Costs and capacities are strictly positive.

## 3. Network Model
We formulated this MIS problem as a **Shortest Path Problem** using a directed graph architecture.
*   **Nodes ($V$):** Represent individual cryptocurrency tokens.
*   **Edges ($E$):** Represent the specific DeFi liquidity pools connecting two tokens.
*   **Edge Weights ($W$):** Represent the total financial friction (Commission % + Slippage %). 

A directed graph (`DiGraph`) is essential because swap dynamics (liquidity and slippage) can differ significantly depending on the direction of the trade (e.g., swapping ETH to USDC is not always the exact mathematical inverse of USDC to ETH).

## 4. Nodes and Edges Data Structure
The network consists of **6 Nodes (Tokens)** and **16 Edges (Swap Pools)**, heavily interconnected.

**Nodes (Cryptocurrencies):**
USDC, DAI, ETH, USDT, WBTC, LINK

**Data Dictionary & Assumptions (`data/dex_pools.csv`):**
In accordance with data preparation guidelines, our dataset includes the following attributes:
*   `token_in` (Node A): The token being sold.
*   `token_out` (Node B): The token being purchased.
*   `commission` (Weight component 1): Fixed platform fee percentage (Unit: %).
*   `slippage` (Weight component 2): Variable price impact percentage estimated for a standard $10k swap (Unit: %).
*   `liquidity` (Capacity constraint): Total USD value locked in the pool (Unit: $). Assumption: Minimum threshold is $3.2M.

## 5. Selected Algorithm
To solve this optimization problem, we implemented **Dijkstra's Algorithm**.

| Criteria | Dijkstra's Algorithm | Bellman-Ford |
| :--- | :--- | :--- |
| **Graph Type** | Weighted, Directed | Weighted, Directed |
| **Edge Weights** | Non-negative costs (Valid for DeFi fees) | Handles negative weights |
| **Time Complexity** | $O(E \log V)$ | $O(VE)$ |
| **MIS Justification** | **Optimal.** Execution speed is critical for financial routing. Since DeFi swap fees are never negative, Dijkstra provides the fastest, most scalable real-time result. | **Overkill.** Slower execution time makes it unsuitable for high-frequency trading networks where milliseconds matter. |

## 6. Python Implementation
The solution is built using Python, leveraging the `NetworkX` library for graph theory operations and `Pandas` for data management.
```python
1. Loading the DeFi Infrastructure Data
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

df = pd.read_csv('data/dex_pools.csv')

# 2. Constructing the Directed Network
# We use DiGraph because financial swap routes are directional. 
G = nx.DiGraph()

for _, pool in df.iterrows():
    # Total cost is the sum of commission and slippage (Edge Weight)
    total_cost = pool['commission'] + pool['slippage']
    G.add_edge(pool['token_in'], pool['token_out'], 
               weight=total_cost, 
               capacity=pool['liquidity'])

# 3. Executing the Optimization Model
optimal_path = nx.shortest_path(G, source='USDC', target='ETH', weight='weight')
optimal_cost = nx.shortest_path_length(G, source='USDC', target='ETH', weight='weight')
7. Results and FindingsThe algorithm successfully analyzed the network topography to find the optimal route from USDC to ETH.Winner: The Multi-Hop Route (USDC → USDT → ETH)Total Financial Cost: 0.56%Path Length: 2 HopsExecution Time: < 5 msAlternative Route Analysis:USDC → USDT → ETH: 0.56% (Optimal)USDC → ETH (Direct): 0.65% (Suboptimal by +0.09%)USDC → DAI → ETH: 1.00% (Suboptimal by +0.44%)Key Insight: The model proves that taking a longer path through a highly liquid "bridge" currency (USDT) mathematically yields lower total friction than a direct swap across an illiquid pool.8. Managerial InterpretationAs an MIS solution, this network optimization engine delivers quantifiable business value:For Platform Administrators (DEXs): Integrating this routing logic into a consumer-facing application increases the platform's competitive advantage. Users are guaranteed the best rates, directly driving up daily active users (DAU) and trading volume.Financial ROI for Traders: The algorithm saves ~0.09% per transaction compared to naive direct routing. For an institutional fund executing $1,000,000 in volume monthly, this single algorithmic optimization yields $9,000 in direct monthly savings, demonstrating the profound impact of IS infrastructure optimization.System Scalability: The $O(E \log V)$ complexity ensures that as we add hundreds of new tokens (nodes) and pools (edges) in Phase 2, the system will remain highly performant without requiring massive server upgrades.9. How to Run the CodeEnsure your environment matches the expected repository structure.Prerequisites:Bashpython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
Execution:Bashpython src/solution.py
The script will output the optimal routing logs to the terminal and save the network topology to results/network_visualization.png.10. ReferencesAcademic: Dijkstra, E. W. (1959). A note on two problems in connexion with graphs. Numerische Mathematik.Academic: Ahuja, R. K., Magnanti, T. L., & Orlin, J. B. (1993). Network Flows: Theory, Algorithms, and Applications.Library Documentation: NetworkX Developers. (2024). NetworkX Reference Release. https://networkx.org/Industry Context: Uniswap V3 Documentation. https://docs.uniswap.org/Author: Seval KurtuluşSubject: Network Optimization in MISDate: May 2026Institution: Marmara University
