# toolsproject-blacklitterman
For tools project- Blacklitterman

This project is created to calculate optimal portfolio based on Blacklitterman Model, which is based on Markowitz Model. In real life, there are several disadvantages in using Markowitz Model to find out the optimal portfolio, because the Markowitz Model only pays attention to historical statistics, which may not be able to reflect accurate situation in reality, especially when somebody holds unexposed news. Therefore, Blacklitterman Model could be an alternative to Markowitz Model, for it contains subject views given by investors. 

The main steps to complete the model: 
(1) To start with, we need to obtain the matrix of return and covariance of specific stocks, which would be used during the calculation. 
(2) Then, we calculate the optimal portfolio based on Markowitz Model using optimization method. Based on the optimized result, we could find out the valid frontier of portfolio. And we could give out the optimal portfolio according to Markowitz Model. 
(3) After that, we re-calculate the portfolio with Blacklitterman Model. With different views, the project would adjust the matrix of return of each stock. Using updated matrices, we could re-calculate the optimal portfolio frontier and corresponding optimal solution. 

