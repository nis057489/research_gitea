# Example Python analysis script
# This demonstrates a simple computational workflow
# In practice, your actual research code would be here. For example, I have programs in several languages that perform statistical analyses and generate figures for publication.
# As long as your code produces data, you can run an analysis script on the produced data, save the results and produce the figures all within the CI workflow.

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

def main():
    print("Starting computational analysis...")

    # Generate sample data
    n_samples = 10000
    data = np.random.randn(n_samples)

    # Perform analysis
    mean = np.mean(data)
    std = np.std(data)
    median = np.median(data)

    print(f"Mean: {mean:.4f}")
    print(f"Std Dev: {std:.4f}")
    print(f"Median: {median:.4f}")

    # Create visualization
    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=50, alpha=0.7, edgecolor='black')
    plt.axvline(mean, color='red', linestyle='--', label=f'Mean: {mean:.2f}')
    plt.axvline(median, color='green', linestyle='--', label=f'Median: {median:.2f}')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Data Distribution')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('distribution.png', dpi=150, bbox_inches='tight')
    print("Saved distribution.png")

    # Save results to CSV
    results = {
        'mean': [mean],
        'std': [std],
        'median': [median],
        'n_samples': [n_samples]
    }

    import csv
    with open('results.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['metric', 'value'])
        writer.writerow(['mean', mean])
        writer.writerow(['std', std])
        writer.writerow(['median', median])
        writer.writerow(['n_samples', n_samples])
    print("Saved results.csv")

    print("Analysis complete!")

if __name__ == "__main__":
    main()
