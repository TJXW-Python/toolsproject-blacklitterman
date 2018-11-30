# toolsproject-blacklitterman
For tools project- Blacklitterman

This project is created to calculate optimal portfolio based on Blacklitterman Model, which is based on Markowitz Model. In real life, there are several disadvantages in using Markowitz Model to find out the optimal portfolio, because the Markowitz Model only pays attention to historical statistics, which may not be able to reflect accurate situation in reality, especially when somebody holds unexposed news. Therefore, Blacklitterman Model could be an alternative to Markowitz Model, for it contains subject views given by investors. 

In order to solve the optimal portfolio based on Blacklitterman Model, we need not only some important views towards assets but also the choice of assets that investors would like to invest. In our project, we would provide the user 20 assets with high market value. Users should choose assets that they would like to invest based on their knowledge. At the same time, considering that investors may not be quite familiar with finance market, we would set some important views in advance. Therefore, the portfolio will be optimized automatically with some important views based on Blacklitterman Model. 
In this way, we use several lines of code at the beginning to interact with users and get the input about what assets users would like to invest. 

Data Access:
We choose 20 stocks with high market capitalization ("caps") according to the following website: https://www.theonlineinvestor.com/large_caps/
We save the 20 symbols and their corresponding market caps in a csv file and access stock data from Yahoo Finance with pandas given the csv file.

The main steps to complete the model: 
(1) To start with, we need to obtain the matrix of return and covariance of specific stocks, which would be used during the calculation. 
(2) Then, we calculate the optimal portfolio based on Markowitz Model using optimization method. Based on the optimized result, we could find out the valid frontier of portfolio. And we could give out the optimal portfolio according to Markowitz Model. 
(3) After that, we re-calculate the portfolio with Blacklitterman Model. With different views, the project would adjust the matrix of return of each stock. Using updated matrices, we could re-calculate the optimal portfolio frontier and corresponding optimal solution. 


* Optimizing Assets Allocation Weights based on Markowitz Model:
The main idea of this part is to optimize the portfolio by adjusting its weights for different assets. The objective function is minimizing the variance of the portfolio, given the target expected return. 
The input of the function should be: 
(1) Rp: the matrix of return of assets derived by historical statistics;
(2) Vp: the matrix of covariances between different assets;
(3) rf: risk-free rate in the market. 
The main procedure of the function is as follows:
(1) Choose different target expected return; 
(2) Optimize(Minimize) the objective function(the variance of the portfolio) by adjusting the weights of assets
(3) Return the arrays of given expected returns and optimized variance of portfolio



* Optimizing Assets Allocation Weights:

Blacklitterman mainly depends on the technique of reverse optimization of conventional approach to get optimal allocation of assets in a given portfolio. Therefore, after aassets information collection, we should build function to sovle the optimal allocation weights of each assets in the portfolio based on Markowitz Model.

(1) Input the estimated parameters of the portfolio:
    Portfolio expected returns, variance and covariance matrix of the assets pool.
(2) Settting the optimization objective function:
    Maximize the sharp ratio of the portfolio, which is the portfolio's express return divided by portfolio's variance.
(3) Subject to: the sum of weight should equal to 1; 
(4) Boundary: each assets' weight should be less or equal to 1 and be non-negative
(5) Using Sequential Least Squares Programming Method to get optimal allocation weights 
(6) Return the optimal allocation weights as an array.




* Optimizing allocation weights based on implied equilibrium return and investors' views:

After constructing the views matrix and link matrix to express the investors' views on some assets of the portfolio, we need to add these views to the implied equilibrium excess return to get new optimal weights, the weight of view is determined by the scaling factor for views. The scaling factor here is set to be 0.025, referring to Lee's paper materials. User can also set this scalar equals to 1 divided by observation numbers.

(1)Input of the function should be:
   The view matrix, link matrix to assets pool, scaling factor, implied equilibrium excess return vector, covariance matrix of original portfolio and risk-free rate.
(2)Calculate the uncertainty of views and uncertainty of implied equilibrium excess return;
(3)Calculate the adjusted implied equilibrium excess return by adding view matrix into it, the weight is measured by the inverse of uncertainty.
(4)Optimize: Using the new equilibirum excess return, which including the new infomation of investors' views, the weight is determined by the scaling factor for views to get new allocation weights and efficient frontier.
(5)Return the blacklitterman allocation weights, new optimal portfolio return and variance, the efficient frontier.


