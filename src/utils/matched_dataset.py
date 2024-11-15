import polars as pl

# This function loads and processes the matched_beer fioles so that all of the columns are appended with _ba or _rb depending on which dataset they are from
def load_and_process_files(file_paths):
    processed_dataframes = []
    
    for file_path in file_paths:
        # Load the first row to get the data source identifiers (e.g., "ba", "ba_1", "rb", etc.)
        header_row = pl.read_csv(file_path, n_rows=1, has_header=False)
        column_source = header_row.row(0)
        
        # Clean the source identifiers to only keep "ba" or "rb" without any suffixes
        source_identifiers = [source.split('_')[0] for source in column_source]
        
        # Load the actual data, skipping the first row
        df = pl.read_csv(file_path, skip_rows=1)
        
        # Rename columns based on the cleaned source identifiers
        new_column_names = [
            f"{name}_{source}".replace("_duplicated_0", "") for name, source in zip(df.columns, source_identifiers)
        ]
        df = df.rename({old: new for old, new in zip(df.columns, new_column_names)})
        
        # Append the processed DataFrame to the list
        processed_dataframes.append(df)
    
    return processed_dataframes