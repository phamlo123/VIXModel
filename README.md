# VIXModel
This project is inspired by a paper published by Peter Carr and his colleagues from NYU engineering department in 2019. Link to the paper is added at the bottom.

Market volatility has always been an area of interest for me. While VIX provides a good metric for quick evaluation for future market volatility by aggregating pricing 
data from the SPX options market, it is subject to huge swings in demand and supply of the options market itself. With the rise in speculative trading in recent years,
option market itself is somewhat influenced and does not always translate to future realized variance. 

The paper proposes a new way to estimate realized variance by combining the advantage the VIX provides and Machine learning model derived from historical option data.
It includes new algorithm for selecting options for each trading day to be included in the calculation of synthetic VIX, as well as features for the ML model. 
Specifically, 30 realized variance is calculated for every trading day from 1996 to 2020 (using SPX spot price) and this will serve as lablels for our model. Each trading
day is an observation in our model. And finally, the selected options for each trading day will be aggregated and standardized to be used as features in our model.

Details on how options are selected for each day is presented in the paper. 

In this project, I only implement Feed-Forward neural network machine learning model using Scikit-learn, as it yields the best OOS R^2. This component is still in progress

Looking ahead, this program will include features to fetch current option data daily from Tradier API. The data will be then used as parameters in the model to provide a better prediction of realized variance than current VIX. This will then be published on a webpage






Database is stored locally on MySql server. 



Link to the paper:
https://engineering.nyu.edu/sites/default/files/2020-05/P0639_ZZ-JOI_0.pdf
