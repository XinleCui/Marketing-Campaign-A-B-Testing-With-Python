# Marketing-Campaign-A-B-Testing-With-Python

Title: Experimentation Frameworks for Search Ranking and Banner Click-through Rate Optimization
Author: Xinle Cui
Data: Kaggle

Introduction

This repository contains two separate experimental frameworks designed to evaluate and optimize different aspects of online user engagement. The first experiment is conducted by Amazon's search team to assess a new sponsored search ranking algorithm's effectiveness, aiming to improve product suggestion precision for customers. The second experiment is by Company A, aiming to improve a display banner's click-through rate (CTR) by introducing a new creative with an attention-grabbing call-out.

Experiment 1: Evaluating Sponsored Search Ranking Algorithm

Objective
The primary objective is to evaluate whether the new sponsored search ranking algorithm enhances the precision of product suggestions for customers, ultimately leading to better user engagement and satisfaction.

Data Collection
Collect data on user interactions, click-through rates, and conversion rates before and after implementing the new algorithm.
Ensure to collect a substantial amount of data to derive statistically significant conclusions.

Analysis
Compare the click-through and conversion rates before and after the algorithm's implementation.
Use statistical tests like t-tests or chi-square tests to evaluate the significance of the observed differences.
Visualize the distribution of user interactions and other relevant metrics.

Conclusion
Summarize the findings and provide recommendations on whether to adopt the new algorithm or iterate further based on the results.

Experiment 2: Enhancing Banner Click-through Rate (CTR)

Objective
The primary objective is to determine whether a new creative featuring an attention-grabbing call-out can enhance the click-through rate of a display banner.

Data Collection
Implement an A/B testing framework where one group of users sees the existing banner (control group) and another group sees the new creative (treatment group).
Collect data on user interactions, click-through rates, and any other relevant metrics.

Analysis
Compare the CTR between the control and treatment groups using statistical tests like t-tests or chi-square tests to evaluate the significance of the observed differences.
Visualize the results to better understand the data distribution and the impact of the new creative.

Conclusion
Summarize the findings and provide recommendations on whether to adopt the new creative or iterate further based on the results.

Files in this Repository
ab testing mean.py: Whole code for experiment 1
abtest_result.csv & pretest.csv: Sample data files used for the experiment 1

ab testing proportion: Whole code for experiment 2
pretest_proportion.csv & test_proportion.csv: Sample data files used for the experiment 2

Usage
Ensure you have a Python environment with the necessary libraries installed (e.g., pandas, statsmodels, scipy, matplotlib).
Run the ab testing proportion.py & ab testing mean.py to perform the experiments and analyze the results.

Contributing
Feel free to fork this repository and submit pull requests or issues if you have suggestions or find bugs.
