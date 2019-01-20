# Weighted-EPA by @greerreNFL
By weighting certain play types,  Expected Points Added (EPA) can be made more accurate than Point Margin in predicting out of sample Point Margin. Even without controlling for strength of schedule, homefield, or any pre-season priors, a weighted EPA can even be more accurate than DVOA, which includes all of the aforementioned data points.

Link to original post:
http://www.robbygreer.com/blog/2018/12/26/weighting-epa-to-improve-predictive-power

Note - The original post used nflscrapR's points scored pbp information to calculate margin. This methods yields slightly different results than using the actual final scores in the nflscrapR's game files. The new scripts use the game files for point margin resulting in higher RSQs.


To recreate the original baseline look at RSQ, use:
https://github.com/greerre/Weighted-EPA/blob/master/baseline_epa_analysis.py

To calculate the RSQ of DVOA, use:
https://github.com/greerre/Weighted-EPA/blob/master/dvoaPull.py
and
https://github.com/greerre/Weighted-EPA/blob/master/dvoa_rsq.py

To calculate the RSQ's of the individual features used in th post, use:
https://github.com/greerre/Weighted-EPA/blob/master/maximizing_weightings.py

To calculate the RSQ of the individual features weighted together, use:
https://github.com/greerre/Weighted-EPA/blob/master/weighted_epa.py

To easily explore new weights w/ only two lines of code, use:
https://github.com/greerre/Weighted-EPA/blob/master/new_feature_test.py


Please reach out to @greerreNFL on twitter if you have any questions!

