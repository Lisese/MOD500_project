import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor, plot_tree
import matplotlib.pyplot as plt

class InvestmentDecisionTree:
    def __init__(self):
        self.model = DecisionTreeRegressor(max_depth=4, random_state=42)
        self.feature_names = [
            'fleet_size',      # Number of campervans
            'price_level',     # 1: Budget, 2: Mid-range, 3: Luxury
            'season',          # 1: Off-season, 2: Shoulder, 3: Peak
            'van_type',        # 1: Compact, 2: Mixed, 3: Luxury
            'services'         # 1: Basic, 2: Medium, 3: Comprehensive
        ]

    def generate_scenarios(self, n_scenarios=1000):
        """Generate random scenarios for training"""
        np.random.seed(42)
        
        scenarios = {
            'fleet_size': np.random.choice([5, 10, 20], n_scenarios),
            'price_level': np.random.choice([1, 2, 3], n_scenarios),
            'season': np.random.choice([1, 2, 3], n_scenarios),
            'van_type': np.random.choice([1, 2, 3], n_scenarios),
            'services': np.random.choice([1, 2, 3], n_scenarios)
        }
        
        # Calculate expected returns based on scenarios
        returns = []
        for i in range(n_scenarios):
            # Base return calculation
            base_return = scenarios['fleet_size'][i] * 1000  # Base monthly return per van
            
            # Adjust for price level
            price_multiplier = {1: 0.8, 2: 1.0, 3: 1.3}[scenarios['price_level'][i]]
            
            # Adjust for season
            season_multiplier = {1: 0.6, 2: 1.0, 3: 1.4}[scenarios['season'][i]]
            
            # Adjust for van type
            van_multiplier = {1: 0.9, 2: 1.0, 3: 1.2}[scenarios['van_type'][i]]
            
            # Adjust for services
            service_multiplier = {1: 0.9, 2: 1.0, 3: 1.15}[scenarios['services'][i]]
            
            # Calculate final return
            final_return = (base_return * price_multiplier * season_multiplier * 
                          van_multiplier * service_multiplier)
            
            # Add some random noise
            final_return *= np.random.normal(1, 0.1)
            
            returns.append(final_return)
        
        scenarios['returns'] = returns
        return pd.DataFrame(scenarios)

    def train_model(self, data):
        """Train the decision tree model"""
        X = data[self.feature_names]
        y = data['returns']
        self.model.fit(X, y)

    def visualize_tree(self):
        """Create and save a visualization of the decision tree"""
        plt.figure(figsize=(20,10))
        plot_tree(self.model, feature_names=self.feature_names, 
                 filled=True, rounded=True, fontsize=10)
        plt.savefig('investment_decision_tree.png')
        plt.close()

    def analyze_feature_importance(self):
        """Analyze and return feature importance"""
        importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        return importance

    def predict_return(self, scenario):
        """Predict return for a given scenario"""
        return self.model.predict(scenario)

def main():
    # Initialize the decision tree
    dt = InvestmentDecisionTree()
    
    # Generate and train on scenarios
    scenarios = dt.generate_scenarios()
    dt.train_model(scenarios)
    
    # Visualize the tree
    dt.visualize_tree()
    
    # Analyze feature importance
    importance = dt.analyze_feature_importance()
    print("\nFeature Importance:")
    print("==================")
    print(importance)
    
    # Example predictions for different scenarios
    print("\nExample Scenario Predictions:")
    print("============================")
    
    # Test different fleet sizes with other parameters held constant
    test_scenarios = pd.DataFrame([
        [5, 2, 3, 2, 2],   # Small fleet
        [10, 2, 3, 2, 2],  # Medium fleet
        [20, 2, 3, 2, 2]   # Large fleet
    ], columns=dt.feature_names)
    
    predictions = dt.predict_return(test_scenarios)
    
    for i, fleet_size in enumerate([5, 10, 20]):
        print(f"\nFleet Size: {fleet_size}")
        print(f"Predicted Monthly Return: ${predictions[i]:,.2f}")

if __name__ == "__main__":
    main()
