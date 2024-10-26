
print("Verifying package installations in myenv environment...")

try:
    import pandas as pd
    print("✓ pandas")
    
    import numpy as np
    print("✓ numpy")
    
    import matplotlib.pyplot as plt
    print("✓ matplotlib")
    
    import seaborn as sns
    print("✓ seaborn")
    
    from sklearn.model_selection import train_test_split
    print("✓ scikit-learn")
    
    import statsmodels.api as sm
    print("✓ statsmodels")
    
    import plotly.express as px
    print("✓ plotly")
    
    print("\nAll required packages successfully installed in myenv!")
    
except Exception as e:
    print(f"\nError importing packages: {str(e)}")
