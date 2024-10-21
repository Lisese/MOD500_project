import graphviz

def create_decision_tree():
    dot = graphviz.Digraph(comment='Campervan Rental Decision Tree')
    dot.attr(rankdir='LR')

    # Decision node
    dot.node('D1', 'Invest in\nCampervan Rental?', shape='square')

    # Yes branch
    dot.node('C1', 'Market\nDemand', shape='circle')
    dot.edge('D1', 'C1', 'Yes')

    # Market Demand outcomes
    demands = ['High', 'Medium', 'Low']
    probabilities = [0.4, 0.4, 0.2]
    for i, (demand, prob) in enumerate(zip(demands, probabilities)):
        dot.node(f'C2_{i}', 'Weather\nConditions', shape='circle')
        dot.edge('C1', f'C2_{i}', f'{demand}\n({prob})')

        # Weather outcomes
        weathers = ['Favorable', 'Unfavorable']
        w_probs = [0.6, 0.4]
        profits = {'High': [200000, 100000], 'Medium': [100000, 50000], 'Low': [20000, -30000]}
        for j, (weather, w_prob) in enumerate(zip(weathers, w_probs)):
            dot.node(f'O_{i}_{j}', f'Profit\n${profits[demand][j]:,}', shape='plaintext')
            dot.edge(f'C2_{i}', f'O_{i}_{j}', f'{weather}\n({w_prob})')

    # No branch
    dot.node('O_no', 'Profit $0', shape='plaintext')
    dot.edge('D1', 'O_no', 'No')

    dot.render('campervan_decision_tree', format='png', cleanup=True)
    print("Decision tree saved as campervan_decision_tree.png")

def create_influence_diagram():
    dot = graphviz.Digraph(comment='Campervan Rental Influence Diagram')

    # Nodes
    dot.node('D1', 'Invest in\nCampervan Rental', shape='square')
    dot.node('C1', 'Market\nDemand', shape='circle')
    dot.node('C2', 'Weather\nConditions', shape='circle')
    dot.node('C3', 'Operational\nCosts', shape='circle')
    dot.node('C4', 'Competition', shape='circle')
    dot.node('V1', 'Profitability', shape='diamond')

    # Relationships
    dot.edge('D1', 'V1')
    dot.edge('C1', 'V1')
    dot.edge('C2', 'V1')
    dot.edge('C3', 'V1')
    dot.edge('C4', 'V1')
    dot.edge('C1', 'C3')
    dot.edge('C2', 'C3')
    dot.edge('C4', 'C1')

    dot.render('campervan_influence_diagram', format='png', cleanup=True)
    print("Influence diagram saved as campervan_influence_diagram.png")

if __name__ == "__main__":
    create_decision_tree()
    create_influence_diagram()
    print("Visual diagrams generated successfully.")
