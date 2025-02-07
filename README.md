# White House Voluntary Commitments (WHVC) Code
Analysis of public conduct of companies that signed the 2023 Biden-Harris White House Voluntary Commitments on AI.


## Preprocessing
Run `preprocessing.ipynb` to create `final.csv` and `aggregate.csv` scores.

## Visualizations
Install all necessary packages in a new environment. 

1. Run `python aggregate_chart.py` to create the aggregate visualization (seen below).
![alt text](agg_chart.png)

2. Run `python company_level_chart.py` to create the individual company scores visualization. View the visualization in 'voluntary_commitments_scores.pdf'.

3. Run `indicator_level_chart.ipynb` to create the indicator level visualization. View the visualization in 'indicator_level_scores.pdf'.

## Data
- `final.csv` contains the final scores for each company with the average score for each company and commitment.
- `aggregate.csv` contains the aggregate scores for each commitment across each companies.
- `raw.csv` is an example of the original, raw data.