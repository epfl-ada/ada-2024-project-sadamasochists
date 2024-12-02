# **Title**: Breweries, Beer, and Breviews: Unraveling the Global Beer Experience

## Prepare the data
To initialize the dataset and prepare it for the analysis you should:
- Download the original BeerAdvocate dataset and unzip it in the `data/` folder.
- Run the `Processing.ipynb` notebook to process the reviews and ratings.
- Run the `Cleaning.ipynb` notebook to process all the data into the final cleaned and partially processed dataset. All the code that is needed to clean and pre-process the data should be placed here (e.g. recompute some metrics, add some metrics used everywhere,...).

The data into the `data/processed` folder are the one that should be used for the analysis.

## Data structure
The data structure is as follows:
- `data/`: Contains all the data needed (both the processed and the raw ones).
- `data/processed/`: Contains the processed data that should be used for the analysis.
- `src/`: Contains all the code needed for the analysis that is not directly needed to display the results in the data story.
- `src/data/`: Contains all the notebooks and code needed to clean and process the data. Here only notebooks should be used.
- `src/utils/`: Contains all the additional general purpose code that is needed for the analysis.

All the results are displayed in the `results.ipynb` notebook placed at the root of the repository. <br><br>
The data story is contained in the branch `website` and is displayed at the [following link](https://epfl-ada.github.io/ada-2024-project-sadamasochists/)


## Project details
### Abstract

Our project aims to explore the intricate relationship between brewery prevalence, beer preferences, and customer and expert reviews through the data of popular beer rating websites (RateBeer and BeerAdvocate). We strive to understand which factors influence consumer preferences across time and geographic regions. This project will utilize trend analysis methods, examining the evolution of global and local beer preferences, thus identifying both gradually emerging patterns and immediate changes triggered by specific circumstances, for instance following major events like the Super Bowl, World Cup or presidential elections. We will examine multiple variables, such as beer style, alcohol content, and reviewer demographics, aiming to combine statistical methods with NLP techniques, such as topic modeling and sentiment analysis, to identify the key characteristics that make specific beers more popular, whether at a global or regional level. Ultimately, we aim to provide an in-depth understanding of global beer trends and consumer reviews.

### Research Questions

1. What patterns in consumer reviews reveal cyclical (e.g. seasonal) trends and event-driven changes, and how do these differ between global and regional contexts?
2. How do intrinsic beer characteristics (such as alcohol content, stylistic classification, and brewery location) correlate with consumer ratings across geographic regions, and what statistically significant outliers emerge in rating patterns when controlling for these factors?
3. How do regional preferences and cultural factors shape consumer beer selection patterns and consumption behavior?
4. To what extent do rating distributions and consumer preferences differ between RateBeer and BeerAdvocate, indicating a platform effect?

### Proposed additional dataset

We opted against utilizing another existing dataset, instead proposing to create a collection of significant sociocultural (e.g. Superbowl, World Cup) and economic occurrences. This dataset will form the basis for analyzing variations in beer consumption and rating patterns. Given the predominantly North American user demographic of our primary datasets, the focus will primarily be on U.S.-centric events, while also incorporating key international occurrences. Specifically, this dataset will include:

1\. Athletic Competitions: International and domestic sporting events.

2\. Cultural Celebrations: Beer-centric festivals and holidays.

3\. Macroeconomic Indicators: Market dynamics and regulatory shifts within the beverage industry.

This dataset will be loosely structured, containing temporal markers, event identifiers, and categorical classifications. These attributes are intended to facilitate temporal joins with our primary beer review datasets, enabling deeper exploration of correlations and patterns.

### Methodology
Throughout the project we will use the following methodology:

1. **Data handling**: The provided files were mostly in CSV and TXT format. Thus, to facilitate quicker (as well as simpler in the instance of TXT files) data loading we converted larger files into parquet files.
2. **Data processing**: Whilst the size of the provided dataset is manageable (some GBs of data) we saw that we weren't always able to handle the data with pandas, the go to library for data manipulation in Python. We choose instead to do as follow:
    - Small files (such as the beers, the breweries or the users) are handled with pandas. This has done because the data is small enough to be handled with pandas and it is easier to manipulate since we are more familiar with it.
    - Larger files (such as reviews and ratings) are handled with polars and the data without the textual reviews are handled with pandas.
3. **Data cleaning**: After inspecting the data, basic cleaning methods were utilized, mainly: outlier removal, duplicate removal, and inconsistency. Post-cleaning, typical statistical values were added (e.g. avg, std, median…). Additionally, for consistency across the datasets, an outline (e.g. renaming columns, enforcing datetime formats, etc.) was enforced.
4. **Data analysis:**
    - **Quantitative and Statistical Analysis:** This phase encompass an examination of the data through descriptive statistical analysis of key variables (e.g. brewery distribution by country, mean beer ratings by country, …). Next, through correlation analysis, we will try to elucidate the relationships within the data, followed by conducting regression analysis to understand which variables affect beer rating.
    - **Natural Language Processing:** This component aims to focus on processing the textual reviews using sentiment analysis and topic modeling techniques (e.g. LDA). This allow us to identify key themes in beer descriptors and reviews while allowing us to extract additional data from the textual data.
    - **Geospatial Analysis & Temporal Analysis:** This stage aims to implement time trend analysis (e.g. Mann-Kendall) alongside spatial and correlation analyses. This approach enables us to examine temporal shifts in popularity patterns and their geographical variations.
    - **Cross-Platform Analysis:** Upon conducting the individual dataset analyses, we strive to seek discrepancies between the two platform user bases. This analysis should assess potential differences and evaluate the extent to which the reviewing platform users influence metrics.

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

- _Alex Procelewski_ and _Konstantinos Chasialis_: Geospatial analysis & Temporal analysis.
- _Alessandro Dalbesio_ and _Rik de Vries_: Finish quantitative and statistical analysis started in milestone 2 and work on the natural language processing part.
- _Oscar de Francesca_: Set up the website & cross-platform analysis.
