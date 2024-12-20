# Breweries, Beer, and Breviews: Unraveling the Global Beer Preferences
## Introduction
### Data structure
The data structure is as follows:
- `data/`: Contains all the data needed (both the processed and the raw ones).
- `data/processed/`: Contains the processed data that should be used for the analysis.
- `src/`: Contains all the code needed for the analysis.
- `src/data/`: Contains the code to process the data and prepare it for further analysis.
- `src/processing/`: Contains all the code needed inside the `results.ipynb` notebook. Here each file correspond to a specific section.
- `src/utils/`: Contains some utility functions that are used in the analysis.

All the results are displayed in the `results.ipynb` notebook placed at the root of the repository. <br><br>
The data story can be found [following link](https://epfl-ada.github.io/ada-2024-project-sadamasochists/)


### Prepare the data
To initialize the dataset and prepare it for the analysis you should:
- Download the original RateBeer dataset and unzip it in the `data/` folder.
- Run the `src/data/processing.py` file to convert the ratings into a parquet file. This is done to ease the data manipulation.
- Run the `src/data/cleaning.py` file to clean and process all the data into the `data/processed` folder.  

The data into the `data/processed` folder are the one that will be used for the analysis.

## Project details
### Abstract
Our project explores the dynamic relationship between brewery prevalence, beer consumption, and customer reviews to better understand global user preferences and their evolution over time. We aim to uncover what people enjoy drinking and how their preferences change across time and regions. <br>
To achieve this, we will utilize RateBeer, a popular beer ratings platform, combining quantitative methods—such as correlation, regression, and natural language processing (NLP)—with qualitative tools like pie charts, bar plots, and maps. This approach will help us analyze how characteristics like beer styles and alcohol content influence a beer's popularity. <br>
Our analysis extends beyond global trends, focusing on how preferences evolve over time and vary between countries. Ultimately, we seek to identify potential trend, either global or local, in the beer-loving community and explore if the beer culture of a country influences its beer preferences.

### Research Questions
Our study addresses the following key questions:
1. Which specific beer characteristics (e.g., alcohol content, style, and other features) are most favored by users, and how do they influence a beer's overall rating?
2. How do these influential characteristics vary across countries and over time?
3. Are people more inclined to prefer beers from their own country, or do they embrace international options?

### Methodology
Throughout the project we will use the following methodology:

1. **Data handling**: The provided files were mostly in CSV and TXT format. Thus, to facilitate quicker (as well as simpler in the instance of TXT files) data loading we converted all files into parquet format. This format is more efficient in terms of memory usage and speed, which is crucial for handling large datasets.
2. **Data cleaning**: After inspection of the data, basic cleaning methods are used, mainly: outlier removal, duplicate removal, and inconsistency. This is done to ensure that the data is clean and ready for analysis.
3. **Data analysis:**: To be able to propertly answer the research questions we are going to combine different methods:
    - **Quantitative and Statistical Analysis:**: This phase encompass an examination of the data through descriptive statistical analysis of key variables. We are going to use different statistical methods (mean, median, skewness, ...) together with correlation analysis and regression analysis to understand which variables affect beer rating and how they are correlated.
    - **Qualitative analysis:** This phase encompass an examination of the data through the use of pie charts, bar plots and maps. We saw that the use of these qualitative methods are really helpful to understand our data and uncover some hidden patterns.
    - **Natural Language Processing:**: [TO ADD]

### Proposed Timeline

Our proposed timeline for milestone 3 is

- _Week 1: (Nov 18 - Nov 24 | 7 days)_:
  - Start conducting more detailed analysis and additional data processing (if needed).
  - Define the structure of the data story and set up the website.
  - Insert basic analysis conducted for milestone 2 in the data story.
- _Week 2-3: (Nov 25 - Dec 08 | 14 days)_
  - Answer all the research questions by conducting in-depth analysis and by applying different analysis methods.
  - Work on the documentation and improve the data story with preliminary results obtained during these weeks.
- _Week 4: (Dec 09 - Dec 16 | 7 days)_:
  - Finalize analysis.
  - Complete data story.
  - Ensure proper documentation and code structure.
- _Week 5: (Dec 16 - Dec 20)_: final project review and project submission.

We plan to finish one week early to be able to have more time for reviewing and do some last minute modifications if needed.

## Organization Within the Team

We plan to split the work between our team in subgroups:

- _Alex Procelewski_ and _Konstantinos Chasialis_: NLP analysis and world data visualization.
- _Alessandro Dalbesio_ and _Rik de Vries_: Do quantitative and statistical analysis and work on the data story.
- _Oscar de Francesca_: Set up the website and work on the data story.
