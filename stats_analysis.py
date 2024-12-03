import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
from analyze_visits import load_data, calculate_cost, add_insurance_info

## Load in the data:
processed_file = "ms_data.csv"  
insurance_file = "insurance.lst"

df = load_data(processed_file)
df = add_insurance_info(df,insurance_file)

# 1. Analyze walking speed:
# Multiple regression with education and age while accounting for repeated measures
model = smf.mixedlm("walking_speed ~ age + C(education_level)", df, groups=df["patient_id"])
result = model.fit()

# Test for significant trends
print(result.summary()) 

# 2. Analyze costs:
#    - Simple analysis of insurance type effect
anova_result = smf.ols("visit_cost ~ C(insurance_type)", data=df).fit()
print(anova_result.summary())

#    - Box plots and basic statistics
plt.figure(figsize=(8, 6))
sns.boxplot(x="insurance_type", y="visit_cost", data=df, palette="Set2")
plt.title("Cost Distribution by Insurance Type")
plt.xlabel("Insurance Type")
plt.ylabel("Cost")
plt.tight_layout()
plt.show()

stats_by_insurance = df.groupby("insurance_type")["visit_cost"].agg(["mean", "std"])
print("\nBasic Statistics by Insurance Type:")
print(stats_by_insurance)

#    - Calculate effect sizes
anova_groups = [df.loc[df["insurance_type"] == g, "visit_cost"] for g in df["insurance_type"].unique()]
f_stat, p_value = stats.f_oneway(*anova_groups)
effect_size = f_stat / (f_stat + (len(df) - len(df["insurance_type"].unique())))
print(f"\nEffect Size (Cohen's f^2): {effect_size:.4f}")


# 3. Advanced analysis:
#    - Education age interaction effects on walking speed
model_interaction = smf.ols("walking_speed ~ age * C(education_level)", data=df).fit()
print("Advanced Analysis: Interaction Effects")
print(model_interaction.summary())

#    - Control for relevant confounders
model_confounded = smf.ols("walking_speed ~ age * C(education_level) + visit_cost + C(insurance_type)", data=df).fit()
print("\nAdvanced Analysis with Confounders")
print(model_confounded.summary())

#    - Report key statistics and p-values
formula = "walking_speed ~ age + visit_cost + C(education_level)"
model = smf.ols(formula, data=df).fit()
print(model.summary()) 

