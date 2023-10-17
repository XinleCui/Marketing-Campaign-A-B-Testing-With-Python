import pandas as pd
import statsmodels.api as sm
import statsmodels.stats.api as sms
import scipy.stats as stats
import matplotlib.pyplot as plt

from scipy.stats import ttest_ind


# file path
file = "/Users/rhscue/Desktop/Python A:B Test/Practice Mean/pretest_data.csv"

# data
data_pretest = pd.read_csv(file)
print(data_pretest.head())  # Print the first 5 rows of the dataframe

# VALIDITY CHECK (AA TEST)

# Group by test groups, and calculate the mean of each group (check if there's any difference between two group)
AA_avgsales_per_group = data_pretest.groupby('GROUP')['SALES'].mean().reset_index()
print(AA_avgsales_per_group)

# Assuming data_pretest is your datafreame containing the data (Using statastical model to check if there's any difference between two group)) 
  # create two array
    # one for the control group
    # one for the test group
x = data_pretest.loc[data_pretest['GROUP'] == 0, 'SALES'].astype(float)
y = data_pretest.loc[data_pretest['GROUP'] == 1, 'SALES'].astype(float)
print(x.head())
print(y.head)

# Calculate the Confidence Interval (CI) of the means
cm = sms.CompareMeans(sms.DescrStatsW(x), sms.DescrStatsW(y))
lb, ub = cm.tconfint_diff(usevar='unequal') # lb = lower bound, ub = upper bound

def hypothesis_test_output(lb, ub):
  if 0 > float(lb) and 0 < float(ub):
    return  "The difference between the two groups is not statistically significant"
  else:
    return "The difference between the two groups is statistically significant"
  
result = hypothesis_test_output(lb, ub)
print(result)
# The difference between the two groups is not statistically significant, which means the two groups are the same

# create a plot to check if the data is normally distributed
  
  # histogram
plt.hist(x, alpha=0.5, label='control')
plt.hist(y, alpha=0.5, label='test')  
plt.legend(loc='upper right')
plt.show()
  # The histogram shows that the data is not normally distributed because the observation is not centered around the mean
  
  # QQ plot
sm.qqplot(x, line='s')
plt.show()
sm.qqplot(y, line='s')
plt.show() 
  # The QQ plot shows that the data is not normally distributed because the observation are located on the line

  # average sales per user per day
avg_sales_per_day = data_pretest.groupby(['GROUP','DATE'])['SALES'].mean()
control_avg_sales = avg_sales_per_day.loc[0]
treat_avg_sales = avg_sales_per_day.loc[1]

  # get the day range of experiment
exp_day = range(1, data_pretest['DATE'].nunique()+1)

  # display the avg sales per experiment day
f, ax = plt.subplots(figsize=(10, 6))

  # generate the plot
ax.plot(exp_day, control_avg_sales, label='control', color = 'blue')
ax.plot(exp_day, treat_avg_sales, label='treat', color = 'red')

  # format plot
ax.set_title('AA TEST: Average Sales Per User Per Day')
ax.set_xticks(exp_day)
ax.set_ylabel('Average Sales Per Day')
ax.set_xlabel('Experiment Day')
ax.legend()
plt.show()
  # The plot shows that the average sales per user per day is not normally distributed because the two lines are overlapped


# VALIDITY CHECK (SAMPLE RATION MIS-MATCH)

file2 = "/Users/rhscue/Desktop/Python A:B Test/Practice Mean/abtest_result.csv"
data_abtest_result = pd.read_csv(file2)
print(data_abtest_result.head())

  # set test parameter
SRM_alpha = 0.05

  # get the observed and expected counts in the experiment
observed = data_abtest_result.groupby('GROUP')['USER_ID'].nunique().values  # how many unique user in each group
expected = data_abtest_result['USER_ID'].nunique()*0.5 # half of the total test population

print(observed) # [9240 9366]
print(expected) # 9303.0

  # perform chi-square goodness of fit test
chi_stats, p_value = stats.chisquare(f_obs=observed, f_exp=expected)

  # print the result
print('------- A Chi-square Goodness of Fit Test --------\n')
print('H0: The sample ratio is 1:1.')
print('H1: The sample ratio is not 1:1.\n')
print(f'Significance level: {SRM_alpha}')

print(f'Chi-square ={chi_stats:.3f} | P-value = {p_value:.3f}')

print('\nConclusion:')
if p_value < SRM_alpha:
    print('Reject H0. The sample ratio is not 1:1.')
else:
    print('Fail to reject H0. The sample ratio is 1:1.')
# Fail to reject H0. The sample ratio is 1:1.

# VALIDITY CHECK (Novelty Effect)(IF USER NOT RECONGIZE THE NEW FEATURE. THEN NOVELTY EFFECT IS NOT MEANINGFUL)
  
  # average sales per user per day
avg_sales_per_day = data_abtest_result.groupby(['GROUP','DATE'])['SALES'].mean()
control_avg_sales = avg_sales_per_day.loc[0]
treat_avg_sales = avg_sales_per_day.loc[1]

  # get the day range of experiment
exp_day = range(1, data_abtest_result['DATE'].nunique()+1)

  # display the avg sales per experiment day
f, ax = plt.subplots(figsize=(10, 6))

  # generate the plot
ax.plot(exp_day, control_avg_sales, label='control', color = 'blue')
ax.plot(exp_day, treat_avg_sales, label='treat', color = 'red')

  # format plot
ax.set_title('AB TEST: Average Sales Per User Per Day')
ax.set_xticks(exp_day)
ax.set_ylabel('Average Sales Per Day')
ax.set_xlabel('Experiment Day')
ax.legend()
plt.show()

# IF THERE IS A NOVELTY EFFECT, THEN THE TWO LINES HAS SURGE AT THE BEGINNING OF THE EXPERIMENT, AND GRADUALLY DECREASE TO THE BASELINE

# CONDUCT STATISTICAL INFERENCE

  # set the alpha for ab test
ab_alpha = 0.05

  # get the control and test group
ab_control = data_abtest_result[data_abtest_result.GROUP == 0].groupby('USER_ID')['SALES'].mean()
ab_treat = data_abtest_result[data_abtest_result.GROUP == 1].groupby('USER_ID')['SALES'].mean()

print(ab_control.head())
print(ab_treat.head())  

  # analyze statistics
AB_tstat, AB_pvalue = ttest_ind(ab_control, ab_treat, equal_var=False)

  # print the result
print('Ho: The average sales of the control group is equal to the average sales of the test group.')
print('H1: The average sales of the control group is not equal to the average sales of the test group.\n')
print(f'Significance level: {ab_alpha}')

print(f'T-test statistic = {AB_tstat:.3f} | P-value = {AB_pvalue:.3f}')
  # T-test statistics = -49.200 | P-value = 0.000

print('\nConclusion:')
if AB_pvalue < ab_alpha:
    print('Reject H0. The average sales of the control group is not equal to the average sales of the test group.')
else:
    print('Fail to reject H0. The average sales of the control group is equal to the average sales of the test group.')

# Result: The average sales of the control group is not equal to the average sales of the test group.

  # get stats information
AB_control_sales = ab_control.sum()
AB_treat_sales = ab_treat.sum()

AB_control_avgsales= ab_control.mean()
AB_treat_avgsales = ab_treat.mean()

AB_control_n = ab_control.count()
AB_treat_n = ab_treat.count()

  # create two descriptive statistics object using treat and control data
desc_stats_control = sm.stats.DescrStatsW(ab_control)
desc_stats_treat = sm.stats.DescrStatsW(ab_treat)

  # compare the mean of the two datasets
cm = sm.stats.CompareMeans(desc_stats_treat, desc_stats_control)

  # calculate the confidence interval for the difference between two means(unequal variance)
lb, ub = cm.tconfint_diff(usevar='unequal')
  # uservarstr: 'pooled', 'unequal'
  # if pooled, then the standard deviation of the samples is assumed to be the same
  # if unequal, then the standard deviation of the samples is not assumed to be the same
print(f'Confidence Interval (absolute difference): [{lb}, {ub}]')
  # Confidence Interval (absolute difference): [2.0000119489531527, 2.1659828775954684]


  # calculate lift between treat and control
lower_lift = lb/ AB_control_avgsales
upper_lift = ub/ AB_control_avgsales

print(f'Confidence Interval (lift): [{lower_lift*100:.1f}%, {upper_lift*100:.1f}%]')
  # Confidence Interval (lift): [40.3%, 43.7%]
  # We are 95% confident that the lift is between 40.3% and 43.7%

# CONCLUSION
print('--------- Sample Sizes ---------')
print(f'Control Group: {AB_control_n}')
print(f'Treatment Group: {AB_treat_n}\n')

print('\n--------- Group Statistics ---------')
print(f'Treatment Group: {AB_treat_avgsales:.4f}')
print(f'Control Group: {AB_control_avgsales:.4f}')

print('\n--------- Difference ---------')
print(f'Absolute Difference: {AB_treat_avgsales - AB_control_avgsales:.4f}')
print(f'Relative Difference: {(AB_treat_avgsales - AB_control_avgsales)/AB_control_avgsales*100:.1f}%')

print('\n--------- T-Statistics ---------')
print(f'T-Statistics: {AB_tstat:.3f}')
print(f'P-Value: {AB_pvalue:.5f}')

print('\n--------- Confidence Interval ---------')
print(f'Confidence Interval (absolute difference): [{lb:.3f}, {ub:.3f}]')
print(f'Confidence Interval (lift): [{lower_lift*100:.1f}%, {upper_lift*100:.1f}%]')

# Based on the test results, we noted a substantial 42% increase in performance compared to the control group. 
# These results were statistically significant, as indicated by a 95% confidence interval ranging from 40.3% to 43.7%. 
# It's noteworthy that the lower boundary of this confidence interval exceeds the Minimum Detectable Effect (MDE) of 5%.
# With the combined evidence of both practical and statistical significance, our recommendation is to proceed with the implementation of the new search algorithm.