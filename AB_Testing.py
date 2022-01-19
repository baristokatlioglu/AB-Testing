import pandas as pd
import numpy as np
from scipy.stats import shapiro, levene, ttest_ind
from statsmodels.stats.proportion import proportions_ztest
import statsmodels.stats.api as sms

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.float_format', lambda x: '%.5f' % x)


df_control = pd.read_excel("datasets/ab_testing.xlsx", sheet_name="Control Group")
df_test = pd.read_excel("datasets/ab_testing.xlsx", sheet_name="Test Group")

# Descriptive Statistics
df_control.describe().T
df_control.isnull().sum()

df_test.describe().T
df_test.isnull().sum()

(df_control["Purchase"] / df_control["Click"]).mean()   # Ad views / purchases by Max bidding group

(df_test["Purchase"] / df_test["Click"]).mean() # Average bidding group ad views / purchases


# The difference in the average conversion rate of average bidding and max bidding introduced by our customer has been observed,
# but I will test if this difference is by chance. I will use the Two Sample Ratio Test for this.

sum_click = np.array([df_control["Click"].sum(), df_test["Click"].sum()]) # Total ad views for the two groups.
# The nobs argument will be entered in the ratio test.
sum_purchase = np.array([df_control["Purchase"].sum(), df_test["Purchase"].sum()]) # The total number of product purchases by the two groups.
# It will be entered into the count argument in the rate test.

######
# Two-Sample Ratio Test Hypotheses
######
# H0 : Mc = Mt (Statistically between the Purchase / Click rate of the Control Group and the purchase / click rate of the Test group
# # there is no significant difference.)
# H1 : Mc != Mt  (There is a difference between the rates of the two Groups.)

# Assumptions:
# N1 > 30
# N2 > 30
len(df_control)
len(df_test)
# There are 40 observations in both datasets, assumptions are provided.

# Ratio test:
test_stat, pvalue = proportions_ztest(count=sum_purchase,
                                      nobs=sum_click)
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Since the p value is less than 0.05, the H0 hypothesis is rejected. There is a statistically significant difference between
# the conversion rates of the two groups. Average bidding conversion rate is statistically higher than max bidding with 95% accuracy

# Let's test if there is a difference between the Average earnings of the two groups.

df_control["Earning"].mean()
df_test["Earning"].mean()
# There is a noticeable difference when we look at average earnings, but let's test if this difference is statistically significant.
# For this I will use the Two-Sample T-Test.

#####
# Two-Sample T-Test Hypotheses
#####
# H0 : Mc = Mt (There is no statistically significant difference between the average earnings of the two offer types)
# H1 : Mc != Mt (There is a statistically significant difference between the average earnings of the two bid types.)

# Assumptions
# Assumption of normality
# H0: The assumption of normal distribution is provided.
# H1:..is not provided.
test_stat, pvalue = shapiro(df_control["Earning"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p-value = 0.5306, H0 cannot be rejected because p value is not < 0.05. The data conforms to a normal distribution.
test_stat, pvalue = shapiro(df_test["Earning"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p-value = 0.6163, H0 cannot be rejected because p value is not < 0.05. The data conforms to a normal distribution.

# Assumption of Variance Homogeneity
# H0: Variances are Homogeneous
# H1: Variances Are Not Homogeneous.

test_stat, pvalue = levene(df_control["Earning"], df_test["Earning"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p-value = 0.5540 , H0 cannot be rejected because p value is not < 0.05. Variances are Homogeneous.

# Hypothesis Testing

test_stat, pvalue = ttest_ind(df_control["Earning"], df_test["Earning"], equal_var=True) # The equal_var argument was entered
# as True because the variance homogeneity assumption was satisfied.
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p-value = 0.0000, Since p value < 0.05, the H0 hypothesis is rejected. There is a statistically significant difference
# between the mean earnings of the two groups.

####
# Average Bidding's Average Earning Confidence Interval
####
sms.DescrStatsW(df_test["Earning"]).tconfint_mean()
# If the Average bidding bid type is used, it will bring us an average of 2424.469 to 2605.312 with 95% certainty.

sms.DescrStatsW(df_control["Earning"]).tconfint_mean()
# If the Maximum bidding bid type continues to be used, it will yield an Average of 1811,690 to 2005,446 with 95% certainty.

# Considering the difference in conversion rates and Average earnings, it is recommended to use the Average bidding bid type,
# and if used, average earnings are presented in confidence intervals.



