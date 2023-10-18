# Load libraries
import io
import pandas as pd
import statsmodels.api as sm
import statsmodels.stats.api as sms
import scipy.stats as stats
import matplotlib.pyplot as plt
import numpy as np
import math

from statsmodels.stats.proportion import proportions_chisquare, confint_proportions_2indep
from statsmodels.stats.power import tt_ind_solve_power, ttest_power
from statsmodels.stats.weightstats import ttest_ind

# PART 1 Upload Data, Change Formart, And Check The Data

# load data, turn csv into dataframe, and check the first 5 rows
file = "/Users/rhscue/Desktop/Python A:B Test/Practice Porportion/pretest.csv"
data_pretest = pd.read_csv(file)
print(data_pretest.head())  # Print the first 5 rows of the dataframe

# casting date column to datetime format
data_pretest['date'] = pd.to_datetime(data_pretest['date'])

# check the data type of each column
print(data_pretest.info())  # Print the info of the dataframe, including the data type of each column 309903 observations

# PART 2 Power Analysis to Calculate Sample Size For The Test

# calculate the mean for power analysis
avg_ctr = data_pretest['clicked'].mean()
print('Average CTR:', avg_ctr.round(4))  # 0.101

# calculate the CPM for power analysis
# total cost for the campaign divided by the total number of impressions
avg_cpm = data_pretest['spend'].sum()/data_pretest['impression_id'].count()
print('Average CPM:', avg_cpm.round(4))  # 0.005

# power analysis input parameters
MDE = 0.1 # minimum detectable effect(Emprical threshold)
significance_level = 0.05 # alpha
power = 0.8 # 1-beta
effect_size = sm.stats.proportion_effectsize(avg_ctr, avg_ctr *(1+MDE)) # effect size

# calculate the sample size
sample_size = tt_ind_solve_power(effect_size=effect_size, 
                                 alpha=significance_level, 
                                 power=power, 
                                 ratio=1,
                                 alternative='two-sided',
                                 nobs1=None)

# show sample size need for each group, and total sample size
print('Sample size needed for each group:', math.ceil(sample_size))  # 14585
print('Sample size needed for the test:', math.ceil(sample_size)*2)  # 29170

# PART 3 Calculate The Test Duration

# group by 'date' and calculate the count impression id 
daily_unique_imp = data_pretest.groupby('date')['impression_id'].nunique()

# get the average daily unique impression
avg_daily_unique_imp = daily_unique_imp.mean()

# calculate the test duration based on the sample size
test_duration = sample_size*2/avg_daily_unique_imp
print('Based on the last 30 days, the average daily impression is:', avg_daily_unique_imp.round(0))  # 9997.0
print('Based on the last 30 days, the best test duration is:', test_duration.round(0))  # 3 days

# we ususally run the test for full weeks, in that case, the test duration is 3 weeks(21 days)
adjusted_test_duration = math.ceil(test_duration/7)*7
print('The adjusted test duration is:', adjusted_test_duration)  # 7

# PART 4 Calculate The Budget Needs For The Test
total_budget = avg_cpm*sample_size*2
print('The total budget needs for the test is:', total_budget.round(2))  # 145.85
daily_budget = total_budget/test_duration
print('The daily budget needs for the test is:', daily_budget.round(2))  # 49.98

# PART 5 Validity Check (Normality Check)

# filter on impression in the AA Test
data_pretest = data_pretest[data_pretest['experiment']=='AA_test']

# grab the control and treatment group
AA_control = data_pretest[data_pretest['group']==0]['clicked']
AA_treat = data_pretest[data_pretest['group']==1]['clicked']

# get stats
AA_control_cnt = AA_control.sum() # how many clicked in control group
AA_treat_cnt = AA_treat.sum() # how many clicked in treatment group
AA_control_total = AA_control.count()  # how many impression in control group
AA_treat_total = AA_treat.count() # how many impression in treatment group
AA_control_rate = AA_control.mean() # CTR in control group
AA_treat_rate = AA_treat.mean() # CTR in treatment group

# print the stats
print('---------AA TEST---------')
print(f'Control group CTR: {AA_control_rate:.3f}')
print(f'Treatment group CTR: {AA_treat_rate:.3f}')
# the control group CTR is 0.101, and the treatment group CTR is 0.099

# For A/A test, you can perform a basic hypothesis test to check if the difference between the two groups is statistically significant.
# Common test include t-test(Compare Means), chi-square test(Compare proportions)

# run a chi-square test
# H0: the difference between the two groups is not statistically significant
# H1: the difference between the two groups is statistically significant

# excute the chi-square test
AA_chistats, AA_pvalue, AA_tab = proportions_chisquare([AA_control_cnt, AA_treat_cnt], [AA_control_total, AA_treat_total])

# grabs dates
AA_start_date = data_pretest['date'].min()
AA_end_date = data_pretest['date'].max()

# set the alpha
AA_alpha = 0.05

# print the result
print(f'------- AA TEST ({AA_start_date} - {AA_end_date}) --------\n')
print('H0: The CTR between the two groups is same.')
print('H1: The CTR between the two groups is different.\n')
print(f'Significance level: {AA_alpha}')

print(f'Chi-square ={AA_chistats:.3f} | P-value = {AA_pvalue:.3f}')

print('\nConclusion:')
if AA_pvalue < AA_alpha:
    print('Reject H0. The CTR between the two groups is different.')
else:
    print('Fail to reject H0. The CTR between the two groups is same.')
# Fail to reject H0. The CTR between the two groups is same.

# using line plot to check the normality

# averge ctr per day
AA_ctr_per_day = data_pretest.groupby(['group','date'])['clicked'].mean()
AA_control_ctr = AA_ctr_per_day.loc[0]
AA_treatment_ctr = AA_ctr_per_day.loc[1]

# get the day range of experiment
AA_exp_day = range(1, data_pretest['date'].nunique()+1)

# display the avg sales per experiment day
f, ax = plt.subplots(figsize=(10, 6))

# generate the plot
ax.plot(AA_exp_day, AA_control_ctr, label='control', color = 'blue')
ax.plot(AA_exp_day, AA_treatment_ctr, label='treat', color = 'red')

# format plot
ax.set_title('AA TEST: Average CTR Per Day')
ax.set_xticks(AA_exp_day)
ax.set_ylabel('Average CTR Per Day')
ax.set_xlabel('Experiment Day')
ax.legend()
plt.show()
# the two lines are overlapped, so the CTR between the two groups is samen

# PART 6 Validity Check (Sample Ratio Mismatch)

# load data
files2 = "/Users/rhscue/Desktop/Python A:B Test/Practice Porportion/test.csv"
data_test = pd.read_csv(files2)

# show the first 20 rows
print(data_test.head(20))

# set test parameter
SRM_alpha = 0.05

# get the observed and expected counts in the experiment
creative_test = data_test[data_test.experiment == 'creative_test']
observed = creative_test.groupby('group')['experiment'].count().values
expected = [creative_test.shape[0]*0.5]*2
print(observed) # [7463 7592]
print(expected) # [7527.5, 7527.5]
 

# perform chi-square goodness of fit test
chi_stats, p_value = stats.chisquare(f_obs=observed, f_exp=expected)

print('------- A Chi-square Goodness of Fit Test --------\n')
print('H0: The sample ratio is 1:1.')
print('H1: The sample ratio is not 1:1.\n')
print(f'Significance level: {SRM_alpha}')

print(f'Chi-square ={chi_stats:.3f} | P-value = {p_value:.3f}') 
#Chi-square =1.105 | P-value = 0.293

print('\nConclusion:')
if p_value < SRM_alpha:
    print('Reject H0. The sample ratio is not 1:1.')
else:
    print('Fail to reject H0. The sample ratio is 1:1.')
# Fail to reject H0. The sample ratio is 1:1.


# PART 7 Validity Check (Novelty Effect)

# average ctr per user per day
AB_ctr_per_day = creative_test.groupby(['group','date'])['clicked'].mean()
AB_control_ctr = AB_ctr_per_day.loc[0]
AB_tretment_ctr = AB_ctr_per_day.loc[1]

# get the day range of experiment
AB_exp_day = range(1, data_test['date'].nunique()+1)

# lets plot the average ctr per user per day
f, ax = plt.subplots(figsize=(10, 6))

# generate the plot
ax.plot(AB_exp_day, AB_control_ctr, label='control', color = 'blue')
ax.plot(AB_exp_day, AB_tretment_ctr, label='treat', color = 'red')

# format plot
ax.set_title('AB TEST: Average CTR Per User Per Day')
ax.set_xticks(AB_exp_day)
ax.set_ylabel('Average CTR Per User Per Day')
ax.set_xlabel('Experiment Day')
ax.legend()
plt.show()
# Based on the plot, there seems no novelty effect

# PART 8 Conduct Statistical Inference

# get the subset table for control and treatment group
control_clicks = creative_test[data_test['group']==0]['clicked']
treatment_clicks = creative_test[data_test['group']==1]['clicked']

# get the stats
AB_control_cnt = control_clicks.sum() # how many clicked in control group
AB_treatment_cnt = treatment_clicks.sum() # how many clicked in treatment group
AB_control_total = control_clicks.count()  # control sample szie
AB_treatment_total = treatment_clicks.count() # treatment sample size
AB_control_rate = control_clicks.mean() # CTR in control group
AB_treatment_rate = treatment_clicks.mean() # CTR in treatment group

# print the stats
print('---------AB TEST---------')
print(f'Control group CTR: {AB_control_rate:.3f}') # 0.095
print(f'Treatment group CTR: {AB_treatment_rate:.3f}') # 0.107

# run t-test for proportions 
# H0: the difference between the two groups is not statistically significant
# H1: the difference between the two groups is statistically significant

# set the alpha
AB_alpha = 0.05

# excute the t-test
AB_tstat, AB_pvalue, AB_df = proportions_chisquare([AB_control_cnt, AB_treatment_cnt], [AB_control_total, AB_treatment_total])

# print the result
print(f'------- AB TEST ({AA_start_date} - {AA_end_date}) --------\n')
print('H0: The CTR between the two groups is same.')
print('H1: The CTR between the two groups is different.\n')
print(f'Significance level: {AB_alpha}')

print(f'T-stat ={AB_tstat:.3f} | P-value = {AB_pvalue:.3f}')
# T-stat =5.405 | P-value = 0.020

print('\nConclusion:')
if AB_pvalue < AB_alpha:
    print('Reject H0. The CTR between the two groups is different.')
else:
    print('Fail to reject H0. The CTR between the two groups is same.')
# Reject H0. The CTR between the two groups is different.

# PART 9 Calculate The Confidence Interval

# create two descriptive stats table for control and treatment group
desc_stats_control = sm.stats.DescrStatsW(control_clicks)
desc_stats_treatment = sm.stats.DescrStatsW(treatment_clicks)

# compare the mean of two groups
cm = sm.stats.CompareMeans(desc_stats_treatment, desc_stats_control)

# calculate the confidence interval for the difference between the means(using uneqaul variance)
lb, ub = cm.tconfint_diff(usevar='unequal')

print(f'The confidence interval for the difference between the means is [{lb:.3f}, {ub:.3f}]')
#The confidence interval for the difference between the means is [0.002, 0.021]

# calculate the lift between the two groups
lower_lift = lb / AB_control_rate
upper_lift = ub / AB_control_rate

print(f'Confidence Interval for lift [{lower_lift*100:.3f}%, {upper_lift*100:.3f}%]')
# Confidence Interval for lift [1.887%, 22.090%]

# While this method is primary used for comparing the means of two groups, it can also be used to compare the proportions of two groups.

# compute the confidence interval for the difference between the proportions
ci = confint_proportions_2indep(AB_treatment_cnt, 
                                AB_treatment_total, 
                                AB_control_cnt, 
                                AB_control_total, 
                                compare='diff', 
                                method=None, 
                                alpha=AB_alpha, 
                                correction=True)
lower = ci[0]
upper = ci[1]

lower_lift = lower / AB_control_rate
upper_lift = upper / AB_control_rate

# PART 10 Print The Result
print('--------- Sample Size ---------')
print(f'Control group sample size: {AB_control_total}')
print(f'Treatment group sample size: {AB_treatment_total}\n')

print('\n--------- Sign-Up Counts(Rate) ---------')
print(f'Control group sign-up counts: {AB_control_cnt} ({AB_control_rate*100:.3f}%)')
print(f'Treatment group sign-up counts: {AB_treatment_cnt} ({AB_treatment_rate*100:.3f}%)\n')

print('\n--------- Differences ---------')
print(f'Absolute difference: {AB_treatment_rate - AB_control_rate}')
print(f'Relative difference: {(AB_treatment_rate - AB_control_rate)/AB_control_rate*100:.3f}%\n')

print('\n--------- T-Stats ---------')
print(f'T-stat: {AB_tstat:.3f}')
print(f'P-value: {AB_pvalue:.3f}\n')

print('\n--------- Confidence Interval ---------')
print(f'Confidence Interval: [{lower:.3f}, {upper:.3f}]') 
print(f'Confidence Interval for lift [{lower_lift*100:.3f}%, {upper_lift*100:.3f}%]\n')

# During the test, we noticed a 12% (Absolute difference) increase in CTR between the treatment and control group.
# This outcome is statistically significant with a p-value of 0.020, which is less than the significance level of 0.05.
# With a 95% confidence interval from 1.881% to 22.094%. However, our MDE is 10%, which means the MDE fall in the confidence interval.
# And the MDE higher than the lower bound of the confidence interval.
# Nevertheless, since the lower bound of the confidence interval falls below 10%
# We have chosen to repeat the test with a larger sample size to see if the results hold.