# Weighted-EPA by @greerreNFL
By weighting certain play types,  Expected Points Added (EPA) can be made more accurate than Point Margin in predicting out of sample Point Margin. Even without controlling for strength of schedule, homefield, or any pre-season priors, a weighted EPA can even be more accurate than DVOA, which includes all of the aforementioned data points.

Link to original post:
http://www.robbygreer.com/blog/2018/12/26/weighting-epa-to-improve-predictive-power

In this repository are the scripts used in the analysis
Note - The original post used nflscrapR's points scored pbp information to calculate margin. This methods yields slightly different results than using the actual final scores in the nflscrapR's game files. The new scripts use the game files for point margin resulting in higher R2'd

Also included is a new file that allows for easy testing of new play types
