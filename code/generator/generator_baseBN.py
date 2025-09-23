import pandas as pd
import numpy as np
from pgmpy.factors.discrete import TabularCPD
from pgmpy.models import DiscreteBayesianNetwork

"""
BayesianCPTBuilder: Utility class for constructing basic Bayesian Network (BN) Conditional Probability Tables (CPTs). Deprecated.
This class reads data from a CSV file, renames relevant columns, and generates CPTs for Gender, AgeGroup, and IncomeLevel for Bayesian Network modeling. Main features include:
- Data reading and preprocessing (renaming, proportion normalization)
- Building "AgeGroup|Gender" CPT
- Building "IncomeLevel|AgeGroup" CPT
Note: This basic BN generation scheme has been deprecated.
"""

class BayesianCPTBuilder:
    def __init__(self, filepath):
        self.df = pd.read_csv(filepath)
        self.df = self.df.rename(columns={
            'gender': 'Gender',
            'feature': 'AgeGroup',
            'median_income': 'IncomeLevel',
            'PROPORTION': 'Proportion'
        })
        self.genders = sorted(self.df['Gender'].unique())
        self.age_groups = sorted(self.df['AgeGroup'].unique())
        self.income_levels = sorted(self.df['IncomeLevel'].unique())
        self._normalize_proportions()

    def _normalize_proportions(self):
        if 'IncomeLevel' in self.df.columns:
            multiplyer = self.df.groupby(['Gender', 'AgeGroup']).sum(numeric_only=True).sum()
        self.df['Proportion'] = self.df['Proportion'] / multiplyer['Proportion']
    
    def build_age_given_gender_cpd(self):
        cpt_matrix = []
        for age in self.age_groups:
            row = []
            for gender in self.genders:
                prob = self.df[
                    (self.df['Gender'] == gender) & (self.df['AgeGroup'] == age)
                ]['Proportion'].values
                row.append(prob[0] if len(prob) > 0 else 0.0)
            cpt_matrix.append(row)

        return TabularCPD(
            variable='AgeGroup',
            variable_card=len(self.age_groups),
            values=cpt_matrix,
            evidence=['Gender'],
            evidence_card=[len(self.genders)],
            state_names={
                'AgeGroup': self.age_groups,
                'Gender': self.genders
            }
        )

    def build_income_given_age_cpd(self):
        cpt_matrix = []
        for income in self.income_levels:
            row = []
            for age in self.age_groups:
                prob = self.df[
                    (self.df['AgeGroup'] == age) &
                    (self.df['IncomeLevel'] == income)
                ]['Proportion'].sum() 
                row.append(prob)
            cpt_matrix.append(row)

        cpt_array = np.array(cpt_matrix)
        col_sums = cpt_array.sum(axis=0)
        normalized_matrix = (cpt_array / col_sums).tolist()
        return TabularCPD(
            variable='IncomeLevel',
            variable_card=len(self.income_levels),
            values=normalized_matrix,
            evidence=['AgeGroup'],
            evidence_card=[len(self.age_groups)],
            state_names={
                'IncomeLevel': self.income_levels,
                'AgeGroup': self.age_groups
            }
        )

builder = BayesianCPTBuilder("Age group_gender_transformed.csv")
gender_proportions = builder.df.groupby('Gender')['Proportion'].sum()
cpd_age = builder.build_age_given_gender_cpd()
cpd_income = builder.build_income_given_age_cpd()
model = DiscreteBayesianNetwork([('Gender', 'AgeGroup'), ('AgeGroup', 'IncomeLevel')])
model.add_cpds(cpd_age)

cpd_gender = TabularCPD(
    variable='Gender',
    variable_card=2,
    values=[[gender_proportions['FEMALES']], [gender_proportions['MALES']]],
    state_names={'Gender': ['FEMALES', 'MALES']}
)
model.add_cpds(cpd_gender)
assert model.check_model()