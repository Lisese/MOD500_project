import graphviz

def calculate_expected_value(profits, probabilities):
    return sum(p * v for p, v in zip(probabilities, profits))

def create_decision_tree():
    dot = graphviz.Digraph(comment='Campervan Rental Decision Tree')
    dot.attr(rankdir='LR')

    # Initial investment decision node
    dot.node('D1', 'Invest in\nCampervan Rental?', shape='square')

    # Fleet size decision
    dot.node('D2', 'Fleet Size', shape='square')
    dot.edge('D1', 'D2', 'Yes')

    # Price range decision
    dot.node('D3', 'Price Range', shape='square')

    # Fleet size options
    fleet_sizes = [(2, 100000), (5, 250000), (8, 400000)]  # (num_vans, initial_investment)
    
    # Price range options
    prices = [('High', 200), ('Medium', 150), ('Low', 100)]
    demands = [('High', 25, 0.4), ('Medium', 18, 0.4), ('Low', 10, 0.2)]
    weather = [('Favorable', 0.6), ('Unfavorable', 0.4)]
    maintenance = [('Low', 500, 1/3), ('Medium', 1000, 1/3), ('High', 1500, 1/3)]

    fleet_evs = []

    for num_vans, investment in fleet_sizes:
        fleet_node = f'F_{num_vans}'
        dot.node(fleet_node, f'{num_vans} Vans\nInvestment: ${investment:,}', shape='plaintext')
        dot.edge('D2', fleet_node)
        dot.edge(fleet_node, 'D3')

        price_evs = []

        for price_label, day_rate in prices:
            price_node = f'P_{num_vans}_{price_label}'
            dot.node(price_node, f'{price_label}\n${day_rate}/day', shape='plaintext')
            dot.edge('D3', price_node)

            demand_evs = []

            for demand_label, nights, demand_prob in demands:
                demand_node = f'D_{num_vans}_{price_label}_{demand_label}'
                dot.node(demand_node, f'{demand_label} Demand\n{nights} nights', shape='circle')
                dot.edge(price_node, demand_node, f'{demand_label}\n({demand_prob:.2f})')

                weather_evs = []

                for weather_condition, weather_prob in weather:
                    weather_node = f'W_{num_vans}_{price_label}_{demand_label}_{weather_condition}'
                    dot.node(weather_node, f'Weather:\n{weather_condition}', shape='circle')
                    dot.edge(demand_node, weather_node, f'{weather_condition}\n({weather_prob:.2f})')

                    # Calculate profit before maintenance
                    if weather_condition == 'Favorable':
                        profit = day_rate * nights * num_vans
                    else:
                        full_bookings = nights * 0.8  # 80% of bookings are not cancelled
                        cancelled_bookings = nights * 0.2  # 20% of bookings are cancelled
                        profit = ((day_rate * full_bookings) + (day_rate * 0.5 * cancelled_bookings)) * num_vans

                    maintenance_evs = []

                    for maintenance_label, maintenance_cost, maintenance_prob in maintenance:
                        # Scale maintenance cost with fleet size
                        scaled_maintenance = maintenance_cost * num_vans
                        maint_node = f'M_{num_vans}_{price_label}_{demand_label}_{weather_condition}_{maintenance_label}'
                        dot.node(maint_node, f'Maintenance:\n{maintenance_label}\n${scaled_maintenance}', shape='circle')
                        dot.edge(weather_node, maint_node, f'{maintenance_label}\n({maintenance_prob:.2f})')

                        final_profit = profit - scaled_maintenance
                        profit_node = f'Profit_{num_vans}_{price_label}_{demand_label}_{weather_condition}_{maintenance_label}'
                        dot.node(profit_node, f'Monthly Profit:\n${final_profit:,.0f}', shape='plaintext')
                        dot.edge(maint_node, profit_node)

                        maintenance_evs.append(final_profit)

                    maint_ev = calculate_expected_value(maintenance_evs, [prob for _, _, prob in maintenance])
                    weather_evs.append(maint_ev)

                weather_ev = calculate_expected_value(weather_evs, [prob for _, prob in weather])
                demand_evs.append(weather_ev)

            demand_ev = calculate_expected_value(demand_evs, [prob for _, _, prob in demands])
            price_evs.append(demand_ev)

            dot.node(f'EV_{num_vans}_{price_label}', f'Expected Value:\n${demand_ev:,.2f}', shape='diamond')
            dot.edge(price_node, f'EV_{num_vans}_{price_label}')

        # Calculate NPV for this fleet size
        best_monthly_ev = max(price_evs)
        annual_profit = best_monthly_ev * 12
        npv = annual_profit * 5 - investment  # 5-year projection
        fleet_evs.append(npv)

        dot.node(f'NPV_{num_vans}', f'5-Year NPV:\n${npv:,.2f}', shape='diamond')
        dot.edge(fleet_node, f'NPV_{num_vans}')

    best_fleet_ev = max(fleet_evs)
    dot.node('EV_Invest', f'Best Investment NPV:\n${best_fleet_ev:,.2f}', shape='diamond')
    dot.edge('D2', 'EV_Invest')

    # No investment option
    dot.node('No_Invest', 'No Investment\nProfit $0', shape='plaintext')
    dot.edge('D1', 'No_Invest', 'No')

    dot.node('EV_Decision', f'Expected Value\nof Decision:\n${max(best_fleet_ev, 0):,.2f}', shape='diamond')
    dot.edge('D1', 'EV_Decision')

    dot.render('campervan_decision_tree', format='png', cleanup=True)
    print("Decision tree saved as campervan_decision_tree.png")
    print(f"Expected Value of Best Investment: ${best_fleet_ev:,.2f}")
    print(f"Expected Value of Decision: ${max(best_fleet_ev, 0):,.2f}")

def create_influence_diagram():
    # (The influence diagram function remains unchanged)
    pass

if __name__ == "__main__":
    create_decision_tree()
    create_influence_diagram()
