import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def plot_correlation_matrix(df, cmap='coolwarm'):
    corr = df.corr()
    xlabels = list(corr.columns[:-1]) + ['']
    ylabels = [''] + list(corr.columns[1:])
    mask = np.triu(np.ones_like(corr, dtype=bool))
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, mask=mask, annot=True, cmap=cmap, center=0, xticklabels=xlabels, yticklabels=ylabels)
    plt.title('Correlation matrix')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.show()