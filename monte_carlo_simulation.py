import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

class MonteCarloSimulation:
    def __init__(self, n_simulations=10000):
        self.n_simulations = n_simulations
        self.results = None
        
        # Define parameters matching decision tree
        self.params = {
            'fleet_size': {
                'small': 2,    # Small fleet
                'medium': 5,   # Medium fleet
                'large': 8     # Large fleet
            },
            'initial_investment': {
                2: 100000,     # Cost for 2 vans
                5: 250000,     # Cost for 5 vans
                8: 400000      # Cost for 8 vans
            },
            'price_levels': {
                'low': 100,     # Low pricing
                'medium': 150,  # Medium pricing
                'high': 200     # High pricing
            },
            'demand_levels': {
                'low': {'nights': 10, 'prob': 0.2},      # Low demand
                'medium': {'nights': 18, 'prob': 0.4},   # Medium demand
                'high': {'nights': 25, 'prob': 0.4}      # High demand
            },
            'weather_conditions': {
                'favorable': {'factor': 1.0, 'prob': 0.6},
                'unfavorable': {'factor': 0.8, 'prob': 0.4}  # 20% cancellation rate
            },
            'maintenance_costs': {
                'low': {'cost': 500, 'prob': 1/3},
                'medium': {'cost': 1000, 'prob': 1/3},
                'high': {'cost': 1500, 'prob': 1/3}
            }
        }

    def generate_random_factors(self):
        """Generate random factors for a single simulation"""
        # Price level selection
        price = np.random.choice(list(self.params['price_levels'].values()))
        
        # Demand level selection
        demand_probs = [level['prob'] for level in self.params['demand_levels'].values()]
        demand_nights = [level['nights'] for level in self.params['demand_levels'].values()]
        nights = np.random.choice(demand_nights, p=demand_probs)
        
        # Weather condition
        weather_probs = [cond['prob'] for cond in self.params['weather_conditions'].values()]
        weather_factors = [cond['factor'] for cond in self.params['weather_conditions'].values()]
        weather = np.random.choice(weather_factors, p=weather_probs)
        
        # Maintenance cost
        maint_probs = [cost['prob'] for cost in self.params['maintenance_costs'].values()]
        maint_costs = [cost['cost'] for cost in self.params['maintenance_costs'].values()]
        maintenance = np.random.choice(maint_costs, p=maint_probs)
        
        return {
            'price': price,
            'nights': nights,
            'weather': weather,
            'maintenance': maintenance
        }

    def calculate_monthly_cashflow(self, fleet_size, factors):
        """Calculate monthly cash flow based on all factors"""
        # Calculate revenue
        base_revenue = factors['price'] * factors['nights'] * fleet_size
        revenue = base_revenue * factors['weather']  # Apply weather impact
        
        # Calculate costs
        maintenance_costs = factors['maintenance'] * fleet_size
        
        return revenue - maintenance_costs

    def run_simulation(self, fleet_size):
        """Run Monte Carlo simulation for a given fleet size"""
        results = []
        initial_investment = -self.params['initial_investment'][fleet_size]
        
        for _ in range(self.n_simulations):
            npv = initial_investment
            
            for year in range(5):  # 5-year projection as in decision tree
                annual_cashflow = 0
                
                # Calculate monthly cash flows for the year
                for _ in range(12):
                    factors = self.generate_random_factors()
                    monthly_cashflow = self.calculate_monthly_cashflow(fleet_size, factors)
                    annual_cashflow += monthly_cashflow
                
                # Discount the annual cash flow
                discount_rate = 0.10  # 10% discount rate
                discount_factor = (1 + discount_rate) ** year
                npv += annual_cashflow / discount_factor
            
            results.append(npv)
        
        return np.array(results)

    def analyze_results(self, results):
        """Analyze simulation results"""
        analysis = {
            'mean_npv': np.mean(results),
            'median_npv': np.median(results),
            'std_npv': np.std(results),
            'var_95': np.percentile(results, 5),
            'probability_positive': np.mean(results > 0),
            'max_loss': np.min(results),
            'max_gain': np.max(results)
        }
        return analysis

    def plot_results(self, results, fleet_size):
        """Create visualization of simulation results"""
        plt.figure(figsize=(12, 6))
        
        # Plot histogram
        plt.hist(results, bins=50, density=True, alpha=0.7, color='blue',
                label=f'Fleet Size: {fleet_size}')
        
        # Plot KDE
        kde = stats.gaussian_kde(results)
        x_range = np.linspace(min(results), max(results), 200)
        plt.plot(x_range, kde(x_range), 'r-', lw=2)
        
        plt.title(f'NPV Distribution - Fleet Size: {fleet_size} Vans')
        plt.xlabel('Net Present Value ($)')
        plt.ylabel('Density')
        
        # Add vertical lines for key metrics
        plt.axvline(np.mean(results), color='green', linestyle='--', 
                   label=f'Mean: ${np.mean(results):,.0f}')
        plt.axvline(np.percentile(results, 5), color='red', linestyle='--', 
                   label=f'95% VaR: ${np.percentile(results, 5):,.0f}')
        
        plt.legend()
        plt.savefig(f'monte_carlo_results_{fleet_size}.png')
        plt.close()

def main():
    # Initialize simulation
    mc = MonteCarloSimulation()
    
    print("\nMonte Carlo Simulation Results")
    print("==============================")
    
    # Run simulations for different fleet sizes
    for size_name, fleet_size in mc.params['fleet_size'].items():
        print(f"\nFleet Size: {fleet_size} vans ({size_name} fleet)")
        print("--------------------")
        
        # Run simulation
        results = mc.run_simulation(fleet_size)
        
        # Analyze results
        analysis = mc.analyze_results(results)
        
        # Print results
        print(f"Mean NPV: ${analysis['mean_npv']:,.2f}")
        print(f"Median NPV: ${analysis['median_npv']:,.2f}")
        print(f"Standard Deviation: ${analysis['std_npv']:,.2f}")
        print(f"95% Value at Risk: ${analysis['var_95']:,.2f}")
        print(f"Probability of Positive NPV: {analysis['probability_positive']:.1%}")
        print(f"Maximum Loss: ${analysis['max_loss']:,.2f}")
        print(f"Maximum Gain: ${analysis['max_gain']:,.2f}")
        
        # Create visualization
        mc.plot_results(results, fleet_size)
        print(f"\nVisualization saved as 'monte_carlo_results_{fleet_size}.png'")

if __name__ == "__main__":
    main()
