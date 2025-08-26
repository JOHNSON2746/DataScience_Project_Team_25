import pandas as pd
from pgmpy.factors.discrete import TabularCPD

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
        # 自动归一化 PROPORTION 列
        self._normalize_proportions()

    def _normalize_proportions(self):
        if 'IncomeLevel' in self.df.columns:
            multiplyer = self.df.groupby(['Gender', 'AgeGroup']).sum(numeric_only=True).sum()

        # 归一化每组的 PROPORTION，使每个条件组合下的概率和为 1
        self.df['Proportion'] = self.df['Proportion'] / multiplyer['Proportion']
    # def _normalize_proportions(self):
    #     # 按 Gender 分组，计算每个性别的总量
    #     total_by_gender = self.df.groupby('Gender')['Proportion'].sum()

    #     # 对每行进行归一化：除以该行对应性别的总量
    #     self.df['Proportion'] = self.df.apply(
    #         lambda row: row['Proportion'] / total_by_gender[row['Gender']],
    #         axis=1
    #     )
    
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
                ]['Proportion'].sum()  # 合并不同性别的比例
                row.append(prob)
            cpt_matrix.append(row)

        # 每列是一个 AgeGroup，按列归一化
        import numpy as np
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

# 构建BN框架
from pgmpy.models import DiscreteBayesianNetwork

#TODO modify file path later
builder = BayesianCPTBuilder("Age group_gender_transformed.csv")
gender_proportions = builder.df.groupby('Gender')['Proportion'].sum()
cpd_age = builder.build_age_given_gender_cpd()
cpd_income = builder.build_income_given_age_cpd()

# 定义结构：Gender → AgeGroup
model = DiscreteBayesianNetwork([('Gender', 'AgeGroup'), ('AgeGroup', 'IncomeLevel')])
model.add_cpds(cpd_age)
# model.add_cpds(cpd_income)
# model.add_cpds(cpd_age, cpd_income)

# 加入先验gender概率
from pgmpy.factors.discrete import TabularCPD

cpd_gender = TabularCPD(
    variable='Gender',
    variable_card=2,
    values=[[gender_proportions['FEMALES']], [gender_proportions['MALES']]],
    state_names={'Gender': ['FEMALES', 'MALES']}
)
model.add_cpds(cpd_gender)
# 检查模型是否有效（所有节点都有 CPT，结构无环）
assert model.check_model()