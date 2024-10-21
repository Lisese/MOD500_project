import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_npv(cash_flows, discount_rate):
    """Calculate Net Present Value"""
    return np.sum(cash_flows / (1 + discount_rate)**np.arange(len(cash_flows)))

def calculate_irr(cash_flows):
    """Calculate Internal Rate of Return"""
    return np.irr(cash_flows)

def simulate_financials(initial_investment, annual_revenue, annual_costs, years, discount_rate):
    """Simulate financial projections"""
    cash_flows = [-initial_investment] + [annual_revenue - annual_costs] * years
    npv = calculate_npv(cash_flows, discount_rate)
    try:
        irr = calculate_irr(cash_flows)
    except:
        irr = None
    
    return {
        'cash_flows': cash_flows,
        'npv': npv,
        'irr': irr
    }

def plot_cash_flows(cash_flows):
    """Plot cumulative cash flows"""
    cumulative_cash_flows = np.cumsum(cash_flows)
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(cash_flows)), cumulative_cash_flows, marker='o')
    plt.title('Cumulative Cash Flows')
    plt.xlabel('Year')
    plt.ylabel('Cumulative Cash Flow')
    plt.axhline(y=0, color='r', linestyle='--')
    plt.savefig('cumulative_cash_flows.png')
    plt.close()

# Main execution
if __name__ == "__main__":
    # Sample financial projections (you should replace these with more accurate estimates)
    initial_investment = 500000  # Initial investment for campervans, equipment, etc.
    annual_revenue = 300000  # Estimated annual revenue
    annual_costs = 200000  # Estimated annual costs (maintenance, staff, etc.)
    years = 5  # Projection period
    discount_rate = 0.1  # 10% discount rate

    results = simulate_financials(initial_investment, annual_revenue, annual_costs, years, discount_rate)

    print(f"Net Present Value (NPV): ${results['npv']:.2f}")
    if results['irr'] is not None:
        print(f"Internal Rate of Return (IRR): {results['irr']:.2%}")
    else:
        print("Internal Rate of Return (IRR): Could not be calculated")

    plot_cash_flows(results['cash_flows'])

    print("\nFinancial projection plot saved as 'cumulative_cash_flows.png'")
    print("\nHow to use this data:")
    print("1. Use NPV to assess the overall profitability of the venture")
    print("2. Compare IRR with the company's required rate of return to make the Business Launch Decision")
    print("3. Analyze the cumulative cash flow plot to understand the payback period")
    print("4. Adjust inputs (initial investment, revenue, costs) to compare different scenarios for Fleet Size and Pricing Strategy")

    # Sensitivity analysis
    print("\nPerforming sensitivity analysis...")
    sensitivity_results = []
    for revenue_change in np.arange(-0.2, 0.21, 0.1):  # -20% to +20% in 10% steps
        adjusted_revenue = annual_revenue * (1 + revenue_change)
        sens_result = simulate_financials(initial_investment, adjusted_revenue, annual_costs, years, discount_rate)
        sensitivity_results.append({
            'revenue_change': revenue_change,
            'npv': sens_result['npv']
        })

    sensitivity_df = pd.DataFrame(sensitivity_results)
    plt.figure(figsize=(10, 6))
    plt.plot(sensitivity_df['revenue_change'], sensitivity_df['npv'], marker='o')
    plt.title('NPV Sensitivity to Revenue Changes')
    plt.xlabel('Revenue Change (%)')
    plt.ylabel('NPV')
    plt.axhline(y=0, color='r', linestyle='--')
    plt.savefig('npv_sensitivity.png')
    plt.close()

    print("Sensitivity analysis plot saved as 'npv_sensitivity.png'")
    print("Use the sensitivity analysis to understand how changes in revenue affect the project's NPV")
