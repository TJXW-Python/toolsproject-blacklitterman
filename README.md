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
