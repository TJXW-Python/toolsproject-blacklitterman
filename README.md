# toolsproject-blacklitterman
For tools project- Blacklitterman


* Assets Poll Allocation Weights:

Blacklitterman mainly depends on the technique of reverse optimization of conventional approach to get optimal allocation of assets in a given portfolio. Therefore, after aassets information collection, we should build function to sovle the optimal allocation weights of each assets in the portfolio based on Markowitz Model:
(1) Input the estimated parameters of the portfolio:
    Portfolio expected returns, variance and covariance matrix of the assets pool.
(2) Settting the optimization objective function:
    Maximize the sharp ratio of the portfolio, which is the portfolio's express return divided by portfolio's variance.
(3) Subject to: the sum of weight should equal to 1; 
(4) Boundary: each assets' weight should be less or equal to 1 and be non-negative
(5) Using Sequential Least Squares Programming Method to get optimal allocation weights 
(6) Return the optyimal allocation weights as an array.

This project is created to calculate optimal portfolio based on Blacklitterman Model, which is based on Markowitz Model. In real life, there are several disadvantages in using Markowitz Model to find out the optimal portfolio, because the Markowitz Model only pays attention to historical statistics, which may not be able to reflect accurate situation in reality, especially when somebody holds unexposed news. Therefore, Blacklitterman Model could be an alternative to Markowitz Model, for it contains subject views given by investors. 

The main steps to complete the model: 
(1) To start with, we need to obtain the matrix of return and covariance of specific stocks, which would be used during the calculation. 
(2) Then, we calculate the optimal portfolio based on Markowitz Model using optimization method. Based on the optimized result, we could find out the valid frontier of portfolio. And we could give out the optimal portfolio according to Markowitz Model. 
(3) After that, we re-calculate the portfolio with Blacklitterman Model. With different views, the project would adjust the matrix of return of each stock. Using updated matrices, we could re-calculate the optimal portfolio frontier and corresponding optimal solution. 


