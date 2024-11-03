1.list_datasets.py
This script connects to the Open Canada Data API to retrieve a list of datasets. It sends a request to the package_search endpoint, specifying the number of results per request with the rows parameter (default set to 100). If the request is successful, the script outputs the titles and descriptions of the retrieved datasets.

2.get_dataset_id.py
This script searches for a specific dataset by title using the Open Canada Data API. It sends a request to the package_search endpoint with a search query for the target dataset (in this case, "Crime Statistics - Incidents and rates for selected offences"). If the request succeeds, the script checks each result for a title match and outputs the dataset's title and unique ID.

3.download_dataset.py
This script downloads specific datasets from the Open Canada Data API by their unique IDs. For each dataset in the datasets_to_download list, the script retrieves detailed information from the package_show endpoint. It then searches for resources in CSV format and, if found, downloads and saves the file locally with a filename based on the dataset title.

4.data_cleaning.py
This script performs essential data cleaning and integration tasks as an initial step for dataset preparation. It loads two primary datasets: "completed access to information requests" and "contracts with dates corrected." The script then standardizes the date format in the contracts dataset, extracting the year and month for further analysis. Next, it performs an outer join on owner_org to combine both datasets, identifying matches (both) and non-matches (left_only, right_only). This initial step provides two consolidated CSV files—combined_data_all_corrected.csv and combined_data_both_corrected.csv—that serve as a basis for further analysis or exploration.
data_cleaning.ipynb
Following the initial cleaning, the Jupyter Notebook dives deeper into exploratory analysis and validation of the merged data. It enables iterative data inspection, where specific queries and additional observations on data relationships and quality are documented. This notebook format is particularly useful for testing hypotheses, identifying potential anomalies, and generating insights that might not have been evident in the basic cleaning phase of data_cleaning.py. The .ipynb thus builds on the foundation set by the initial script, allowing for more flexible, in-depth exploration and preparation for the subsequent eda_analysis phase.

eda_analysis.ipynb
This Jupyter Notebook explores the primary hypothesis: “Access to Information requests related to national security, environmental issues, and government contracts have seen a significant increase in the past five years, indicating a growing public interest in government transparency on critical policy matters.”

The notebook is structured to progressively analyze datasets that may support or refute this hypothesis, allowing an in-depth exploration of request trends, categorization, temporal changes, and key correlations. The following steps outline the notebook’s methodology and rationale for processing different CSV files sequentially:

Step 1: Preliminary Analysis of Access Requests
The analysis begins with the completed_access_to_information_requests.csv file. This dataset provides a general view of information requests, with attributes like request category, date, and resolution (e.g., granted, denied). Key actions taken include:

Category Identification: Requests are filtered by relevant categories (e.g., national security, environment, government contracts).
Trend Analysis: Temporal trends are calculated for each category to detect any significant increases in recent years.
Data Aggregation: Request counts are aggregated by year and category, establishing a baseline to identify patterns over time.
Step 2: Integrating Contract Data for Cross-Reference
After identifying the main categories of interest, the contracts_with_dates_corrected.csv file is used to explore potential correlations between government contracts and information requests:

Date Extraction and Temporal Mapping: The dataset is filtered by year and month, allowing for comparisons with request patterns.
Cross-Referencing Contracts and Requests: Contracts are linked to requests based on owner_org (organization) or related topics to observe if request peaks align with contracting activities, especially in high-interest areas like national security and environmental contracts.
Hypothesis Evaluation: The notebook assesses whether an increase in contracts for specific categories coincides with a rise in information requests, thus exploring the public’s response to contracting decisions in sensitive policy areas.
Step 3: Detailed Analysis by Specific Topic Categories
Next, other datasets were explored or referenced to provide a finer resolution of the hypothesis:

Proactive Disclosure - Contracts: This dataset provides additional details on contract disclosures, enhancing the analysis of public interest in transparency for government spending and procurement.
Standing Committee on Public Safety and National Security (SECU): By examining records associated with national security, the notebook attempts to cross-check whether requests on this topic reflect heightened public interest due to recent policy or national events.
Environmental Incident Statistics: Monthly marine and pipeline incident data are examined to correlate environmental events with surges in access requests. This supports the hypothesis that public interest in environmental transparency spikes in response to specific incidents.
Each additional dataset provides critical contextual details that allow the analysis to move beyond a surface-level evaluation of trends, offering insights into the reasons behind request surges.

Conclusions and Hypothesis Evaluation
After examining the datasets, the notebook documents key findings and evaluates the hypothesis:

Hypothesis Outcome: It was ultimately concluded that the hypothesis was not supported by the data, as the requests did not show a consistent increase in the target categories, nor did they correlate strongly with specific contracting events, environmental incidents, or policy changes.
Challenges and Limitations: A lack of detailed category information and missing data points were noted as primary limitations, making it difficult to establish definitive connections between access requests and specific public interests.
This structured analysis provides a foundation for future research, with recommendations to integrate more granular datasets for enhanced tracking of public interests in government transparency across high-stakes areas like security, environment, and contracts.









