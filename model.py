from sklearn.cluster import KMeans
import pandas as pd

def cluster_spending(df, k=3):
    """
    Cluster spending categories into groups using KMeans.

    Parameters:
    - df: DataFrame with transaction data (must include 'Category' and 'Amount')
    - k: Number of clusters (default is 3)

    Returns:
    - DataFrame with each category and its assigned cluster label
    """
    # Group the data by category and sum the amounts
    category_df = df.groupby("Category")["Amount"].sum().reset_index()

    # Apply KMeans clustering
    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    category_df["Cluster"] = model.fit_predict(category_df[["Amount"]])

    return category_df
