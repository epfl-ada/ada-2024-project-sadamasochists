# Import all the necessary libraries
import polars as pl
import polars as pl
import tqdm
from datetime import datetime
import os

# Define the path to the data folder
DATA_FOLDER = '../../data'
DATA_FOLDER = os.path.abspath(DATA_FOLDER)

# Define the mapping
mapping_pl = {
    "user_id": pl.Utf8,
    "rating": pl.Float64,
    "review": pl.Boolean,
    "abv": pl.Float64,
    "brewery_name": pl.Utf8,
    "user_name": pl.Utf8,
    "beer_id": pl.Int64,
    "appearance": pl.Float64,
    "palate": pl.Float64,
    "text": pl.Utf8,
    "aroma": pl.Float64,
    "overall": pl.Float64,
    "taste": pl.Float64,
    "style": pl.Utf8,
    "beer_name": pl.Utf8,
    "brewery_id": pl.Int64,
    "date": pl.Datetime
}

file_name = "ratings"

# Create an empty list to collect rows
rows = []

# Open the file to read the reviews
with open(f'{DATA_FOLDER}/{file_name}.txt', 'r') as f:
    for line in tqdm.tqdm(f):
        # Remove leading/trailing whitespaces
        line = line.strip()
        
        # Create a dictionary to store the content of the row
        content = {label: None for label in mapping_pl.keys()}

        # Process the line until we get a complete record
        while line:
            # Split the line into label and value
            label, value = line.split(":", 1)
            label = label.strip()
            value = value.strip()

            # Skip 'nan' values (these values are used to indicate missing data)
            if value != 'nan':
                # Cast the value to the correct type based on the mapping
                if mapping_pl[label] == pl.Int64:
                    value = int(value)
                elif mapping_pl[label] == pl.Float64:
                    value = float(value)
                elif mapping_pl[label] == pl.Utf8:
                    value = str(value)
                elif mapping_pl[label] == pl.Datetime:
                    value = datetime.fromtimestamp(int(value))
                elif mapping_pl[label] == pl.Boolean:
                    value = value == "True"

                # Store the value in the content dictionary
                content[label] = value

            # Read the next line (for multiline records, like reviews)
            line = f.readline().strip()

        # Add the processed row to the list
        rows.append(content)

# After processing all lines, create a DataFrame from the accumulated rows
df = pl.DataFrame(rows)

# Save it as parquet
df.write_parquet(f'{DATA_FOLDER}/{file_name}.pq')