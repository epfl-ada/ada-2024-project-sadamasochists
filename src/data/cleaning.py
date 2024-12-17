# Do all the imports here
import tqdm
from datetime import datetime
import os
import pandas as pd

# Define the data folder
DATA_FOLDER = os.path.join(os.path.dirname(__file__), '../../data')

# Process the data
# Define the mapping betwen column names and polars types
mapping_pd = {
    'rating': pd.Float64Dtype,
    'palate': pd.Float64Dtype,
    'abv': pd.Float64Dtype,
    'beer_id': pd.Int64Dtype,
    'beer_name': pd.StringDtype,
    'user_id': pd.StringDtype,
    'taste': pd.Float64Dtype,
    'date': pd.Timestamp,
    'style': pd.StringDtype,
    'appearance': pd.Float64Dtype,
    'overall': pd.Float64Dtype,
    'brewery_name': pd.StringDtype,
    'text': pd.StringDtype,
    'aroma': pd.Float64Dtype,
    'user_name': pd.StringDtype,
    'brewery_id': pd.Int64Dtype
}

# Create an empty list to collect rows
rows = []

# Open the file to read the reviews
with open(f"{DATA_FOLDER}/ratings.txt") as f:
    for line in tqdm.tqdm(f):
        # Remove leading/trailing whitespaces
        line = line.strip()
            
        # Create a dictionary to store the content of the row
        content = {label: None for label in mapping_pd.keys()}

        # Process the line until we get a complete record
        while line:
            # Split the line into label and value
            label, value = line.split(":", 1)
            label = label.strip()
            value = value.strip()

            # Skip 'nan' values (these values are used to indicate missing data)
            if value != 'nan':
                # Cast the value to the correct type based on the mapping
                if mapping_pd[label] == pd.Int64Dtype:
                    value = int(value)
                elif mapping_pd[label] == pd.Float64Dtype:
                    value = float(value)
                elif mapping_pd[label] == pd.StringDtype:
                    value = str(value)
                elif mapping_pd[label] == pd.Timestamp:
                    value = datetime.fromtimestamp(int(value))
                elif mapping_pd[label] == pd.Boolean:
                    value = value == "True"

                # Store the value in the content dictionary
                content[label] = value

            # Read the next line (for multiline records, like reviews)
            line = f.readline().strip()

        # Add the processed row to the list
        rows.append(content)

# After processing all lines, create a DataFrame from the accumulated rows
df = pd.DataFrame(rows)

# Save it as parquet
df.to_parquet(f'{DATA_FOLDER}/ratings.pq')

# Delete the ratings.txt file
os.remove(f"{DATA_FOLDER}/ratings.txt")
