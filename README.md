# Breweries, Beer, and Breviews: Unraveling the Global Beer Experience
## Abstract
Our project aims to explore, using data from the two popular beer ratings websites RateBeer and BeerAdvocate, the intricate relationship between brewery prevalence, beer quality, and customer reviews to understand which factors influence the popularity of beers. <br>
By analyzing our data with trend analysis methods we’ll examine the evolution of beer preferences over time, identifying style preference shifts and potential significant event influences, such as elections or big sports events. We’ll also see how these trends change in different countries in the world. <br>
In our analysis we’ll consider factors like beer styles, ABV preferences, and the reviewer’s country of origin by combining statistical methods with NLP techniques, such as topic modeling and sentiment analysis, we aim to understand what makes a beer popular. <br>
Through this study, we will provide valuable insights for beer enthusiasts and breweries, offering a deep understanding of global beer trends and consumer behavior.

## Research Questions
The research questions that we aim to answer through this project are:
- What temporal patterns (e.g., seasonal trends, specific major events, …) can be observed in our reviews? Are the patterns global or local?
- How do beer characteristics (e.g. ABV, style, location of the brewery, …) affect beer popularity and grading across different regions? Are there some beers that are particularly poorly rated given their characteristics or vice-versa?
- Do regional preferences influence the choice of beers to drink?
- Is popularity affected by the platform used for reviewing?

## Proposed Additional Dataset
To enhance our analysis, we will manually curate a list of key major events from several relevant categories. This curated dataset will provide contextual information to help us understand shifts in beer preferences and trends over time. The categories we plan to include are:
- <b>Sporting Events</b>: Major international competitions such as the FIFA World Cup, the Olympics, and significant national sporting events.
- <b>Cultural Festivals</b>: Events that celebrate beer culture, such as Oktoberfest, St. Patrick's Day, and other local beer festivals.
- <b>Economic Events</b>: Significant economic occurrences, such as recessions, market booms, and major policy changes affecting the alcohol industry.

We will compile this information into a parquet file that includes the date, event name, and category. This approach allows us to focus specifically on the events most relevant to our study, ensuring we have a manageable dataset that can be easily integrated with our beer review data.

## Methods
To answer our research questions we are will use the following methodology:
- <b>Data handling</b>: some of the original datasets were provided as txt files. To simplify the process of analysis and handling we have chosen to convert these files into parquet files to speed up the loading, reduce the memory usage and make it possible to use them easily with Python libraries.
- <b>Data processing</b>: even if the dataset is not huge (< 10 GB) we verified significant performance issues with pandas. That has prompted us to explore alternative libraries such as Polars, which, thanks to the use of multithreading, allows us to speed up the operation needed. Given that we have chosen to work on DeepNote, a really powerful tool that helps us with its real time collaborative features, version control and standardized cloud environment but with some memory constraints (5 GB), we have also tested, with success, the use of DuckDB. This powerful tool enables out-of-memory computing and lazy loading for larger datasets letting us work with these memory constraints.
- <b>Data cleaning</b>: after analyzing the data we have done a detailed cleaning of the data. We’ve removed outliers, inconsistent results, duplicates, and data that was not used, in order to reduce the memory usage of our dataset.
- <b>Data enrichment</b>: after cleaning the data we needed to recompute and add some of the values (such as avg, std or median of the beers) useful for our purposes. We additionally modified the data to make them consistent across different datasets. In the next milestone we aim to compute additional values from the reviews dataset to see how other factors, such as smell or taste ratings, affect the popularity of a beer. 
- <b>Data analysis</b>:
    - <b>Quantitative and Statistical analysis</b>: in this process we aim to conduct a general overview of the data by computing descriptive statistics for key variables (e.g. brewery numbers for each country, average rating for beers in a country, …), some correlation analysis to understand how the relationship between the data and finally to conduct some regression analysis to understand which variables affect the beer rating. 
    - <b>Natural language processing</b>: here we aim to process the textual reviews with sentiment analysis and topic modeling (e.g. LDA) to identify key themes in beer descriptions and reviews and to extract additional data from the textual reviews.
    - <b>Geospatial analysis & Temporal analysis</b>: here, by conducting time trend analysis (e.g. Mann-Kendall test for time series), spatial and correlation analysis we aim to conduct in detail on our data to understand how popularity has shifted over time and if how this shift changes in different countries.
    - <b>Cross-platform analysis</b>: after conducting our analysis on both datasets individually we aim to see if there are differences between the two populations and how different the populations of the two websites are to understand if the reviewing platform has an impact on the popularity.

## Proposed Timeline
Our proposed timeline for milestone 3 is
- <b>Week 1</b>: (Nov 18 - Nov 24 | 7 days):
    - Start conducting more detailed analysis and additional data processing (if needed).
    - Define the structure of the data story and set up the website.
    - Insert basic analysis conducted for milestone 2 in the data story.
- <b>Week 2-3</b>: (Nov 25 - Dec 08 | 14 days)
    - Answer all the research questions by conducting in-depth analysis and by applying different analysis methods.
    - Work on the documentation and improve the data story with preliminary results obtained during these weeks.
- <b>Week 4</b>: (Dec 09 - Dec 16 | 7 days): 
    - Finalize analysis. 
    - Complete data story. 
    - Ensure proper documentation and code structure.
- <b>Week 5</b>: (Dec 16 - Dec 20): final project review and project submission.

We plan to finish one week early to be able to have more time for reviewing and do some last minute modifications if needed.

## Organization Within the Team
We plan to split the work between our team in subgroups:
- <b>Alex Procelewski</b> and <b>Konstantinos Chasialis</b>: Geospatial analysis & Temporal analysis.
- <b>Alessandro Dalbesio</b> and <b>Rik de Vries</b>: Finish quantitative and statistical analysis started in milestone 2 and work on the natural language processing part.
- <b>Oscar de Francesca</b>: Set up the website & cross-platform analysis.