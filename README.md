# Data Science Project Team 25(MAST90106_2025_SM1)
# Intersectional Data Analysis of Organisational Employee Data to Promote Equity and Inclusion 
# Project Team
Students: Zige Liang, Chao Tang, Hengjin Hou, Xueying Yuan, Yifu Shen  

Supervisors: Ian Gallagher, Joseph Odewole  

Industry Partner: Dr. Arti Agrawal, CEO & Founder, Vividhata Pty Ltd  

# File Structure

- **abs_raw_data**: Raw data tables from the Australia Bureau of Statistics

- **code**:  
  - `reader`: Reads in data from ABS  
  - `generator`: Generates synthetic data (using Bayesian Network and independent marginal sampling)  
  - `evaluator`: Compares generated data to company-level statistics  
  - `processor`: Data preprocessing, independent marginal sampling, and synthetic data generation

- **scripts**: Run the code for reader1 only

- **data**:  
  - `pre_transform`: Preprocessed ABS data for modeling  
  - `synthetic`: Output synthetic datasets
  - `marginal_tables_transformed` and `randomized marginal tables`: Discarded folders for Bayesian Approach


# Data Sources
Australian National Accounts: Input-Output Tables:
https://www.abs.gov.au/statistics/economy/national-accounts/australian-national-accounts-input-output-tables/latest-release


## Project Overview
  This project aims to develop and validate a **methodology for intersectional data analysis** to uncover inequities within organizational employee data. By examining the intersections of gender, age, ethnicity, and education, the project supports evidence-based policy-making to foster workplace **equity and inclusion**.
  
## Objectives
 1.Identify which individual or intersecting characteristics contribute to inequity in the workplace.  
 
 2.Analyze organizational impact on:Salary、Career progression (recruitment, retention, advancement)、Working hours and conditions
   Training opportunities、Workplace culture (psychological and physical safety)  
   
 3.Develop synthetic datasets that resemble real-world company data.  
 
 4.Apply and validate the analysis methodology on: Public datasets (e.g. WGEA)、Synthetic datasets  

## Methodology  
**1.Synthetic Data Generation**  
Synthetic data is generated using independent marginal sampling. The process involves reading raw ABS data, preprocessing it to extract relevant features, and then sampling each employee attribute (e.g., gender, age, ethnicity, education) independently based on their observed marginal distributions. This approach ensures that the generated synthetic datasets reflect the overall statistical properties of the original data while simplifying the modeling process.

**2.Synthetic Data Validation**
！！！TODO！！！

**3.Data Analysis**  
Perform intersectional analysis using employee attributes such as:  
•	Gender  
•	Age  
•	Visa type
•	Work duration in a year
•	Employment business size


## Workflow
First, use the `reader` component to read and convert raw ABS data into a format suitable for further processing. Next, the `processor` performs data preprocessing, including feature extraction and independent marginal sampling. Finally, the `evaluator` assesses the generated data by comparing the synthetic datasets with the original data, validating the reasonableness of the synthetic data and establishing a framework for future company-level statistical comparisons. The entire workflow can be automated to achieve a closed loop of data reading, processing, and evaluation.


