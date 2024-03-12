import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def sim_social_hierarchy_adjusted(X, T):
    np.random.seed(42)  # For reproducibility
    for t in range(1, T + 1):
        M_t = max(X)  # Calculate the maximum at time t to determine relative growth rates
        
        # Dynamically adjust growth rates based on the current maximum to simulate differentiation
        growth_rates = [np.random.normal(loc=0.01, scale=0.005) for _ in X]
        
        # Update each x_j(t) with a controlled growth rate
        X = [max(min(x * (1 + rate), 100), 0) for x, rate in zip(X, growth_rates)]  # Ensure values are within [0, 100]
        
        # Apply differentiation logic to simulate a social hierarchy
        if M_t > 1:  # Only apply if there's meaningful variation to work with
            X.sort(reverse=True)  # Sort to work with ranking
            X = [min(x * (0.98 ** idx), 100) for idx, x in enumerate(X)]  # Apply diminishing returns based on rank
        
        # Apply a soft cap to the growth to promote hierarchy
        X = [min(100, x * (1 + 0.02)**(t/60)) for x in X]  # Adjust growth cap as a function of time

    # Creating the DataFrame
    DF = pd.DataFrame({'seq': range(1, len(X) + 1), 'value': X})
    # Sorting the DataFrame in descending order by value
    DF = DF.sort_values(by='value', ascending=False).reset_index(drop=True)
    
    return DF

# Rerun simulation with adjustments for hierarchical distribution
X_social_hierarchy_adjusted = [1] * 1000
T_social_hierarchy_adjusted = 70

DF_social_hierarchy_adjusted = sim_social_hierarchy_adjusted(X_social_hierarchy_adjusted, T_social_hierarchy_adjusted)
DF_social_hierarchy_adjusted.head(100)  # Show top 10 values to observe the hierarchy


DF = DF_social_hierarchy_adjusted.head(200)
DFF = DF.sample(frac=1)
DFF['seq'] = range(1, 201)


DFF['size'] = DFF['value'] * 50  # Adjust this scaling factor as needed

plt.figure(figsize=(8, 5))
# Plotting each point as an empty circle ('o') and making the size of the circle depend on the 'value'
#plt.scatter(DFF['seq'], DFF['value'], s=DFF['size'], facecolors='none', edgecolors='r')

plt.scatter(DFF['seq'], DFF['value'], s=DFF['size'], facecolors='blue', edgecolors='blue')

plt.title('Evolution Simulation Result')
plt.xlabel('Sequence')
plt.ylabel('Value')
plt.show()
