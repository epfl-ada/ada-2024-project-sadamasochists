import polars as pl
from tabulate import tabulate

# Function to describe the data
def describe_numbers(df: pl.DataFrame, filters=[]) -> None:
    headers = ["Column", "Mean", "Std", "25%", "50%", "75%", "Min", "Max"]
    content = []
    for col in df.columns:
        if col in filters:
            continue
        if df[col].dtype in [pl.Int32, pl.Int64, pl.Float32, pl.Float64]:
            col_mean = df[col].mean()
            col_std = df[col].std()
            col_25 = df[col].quantile(0.25)
            col_50 = df[col].quantile(0.5)
            col_75 = df[col].quantile(0.75)
            min_val = df[col].min()
            max_val = df[col].max()
            content.append([col, col_mean, col_std, col_25, col_50, col_75, min_val, max_val])
    print(tabulate(content, headers, tablefmt="psql", colalign=("left", "right", "right", "right", "right", "right", "right", "right")))

def describe(df: pl.DataFrame, filters=[]) -> None:
    headers = ["Column", "Type", "Not null count", "Nulls count", "Nulls %", "Unique values count", "Unique values %"]
    content = []
    for col in df.columns:
        if col in filters:
            continue
        col_type = df[col].dtype
        col_count = df[col].count()
        col_null = df[col].is_null().sum()
        col_unique = df[col].n_unique()
        col_percentage_unique = col_unique / df[col].count() * 100
        col_percentage_null = col_null / (df[col].count() + df[col].is_null().sum()) * 100
        content.append([col, col_type, col_count, col_null, f"{col_percentage_null:.2f} %", col_unique, f"{col_percentage_unique:.2f} %"])
    print(tabulate(content, headers, tablefmt="psql", colalign=("left", "left", "right", "right", "right", "right", "right")))

# Function to remove trailing and leading whitespaces from a polars dataframe
def remove_whitespaces(df: pl.DataFrame) -> pl.DataFrame:
    for col in df.columns:
        if df[col].dtype == pl.Utf8:
            df = df.with_columns(pl.col(col).str.strip_chars().alias(col))
    return df