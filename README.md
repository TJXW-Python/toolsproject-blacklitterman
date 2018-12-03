# toolsproject-blacklitterman

**Group name:** 

TJXW_Python 
**Section 1**

**Members:**

Zihao Wu; Jinghan Xue; Ningyuan Tang; Zhuangzhuang Jia


**For Tools Project- Porfolio Optimization with the Black-Litterman Model**

This project is created to calculate optimal portfolio based on the Black-Litterman Model, which is based on the Markowitz Model. In real life, there are several disadvantages in using the Markowitz Model to find out the optimal portfolio, because the Markowitz Model only pays attention to historical statistics, which may not be able to reflect accurate situation in reality, especially when somebody holds unexposed news. Therefore, the Blacklitterman Model could be an alternative to the Markowitz Model, for it contains subject views hold by investors. 

**INSTALLATION INSTRUCTIONS**

In order to use the tool, the user must put the folder "data" in the same folder as "Project_Blacklitterman_Model.py". Also, the user should install pandas-datareader on the terminal first. For Anaconda users, enter in the terminal

    conda install -c anaconda pandas-datareader
Otherwise, enter in the terminal

    pip install pandas-datareader


**Beginning: data collection & portfolio construction**
- In order to solve the optimal portfolio based on Blacklitterman Model, we need not only some important views towards assets but also the choice of assets that investors would like to invest. In our project, we would provide the user 20 assets with high market capitilization. Users should choose assets that they would like to invest based on their knowledge. At the same time, considering that investors may not be quite familiar with finance market, we would set some important views in advance. Therefore, the portfolio will be optimized automatically with some important views based on Blacklitterman Model. 
- To achieve this end, we use several lines of code at the beginning to interact with users and get the input about what assets users would like to invest. If the user input is consistent with the prompt (in terms of both the format and the stock symbols indicated), then we start to optimize the portfolio. Otherwise, the prompt pops up again to ask for a legal user input.
- We choose 20 stocks with high market capitalization ("caps") according to the following website: https://www.theonlineinvestor.com/large_caps/
- We save the 20 stock sticks and their corresponding market caps in a csv file and access stock data from Yahoo Finance with pandas given the csv file. This gives us two main advantages.
 (1)The SymbolAndCap.csv file is handy since we can load symbols and market caps from the csv file easily for further use and we can also easily update our pool of assets and their market caps as time passes. 
 (2)The 20 csv files store historical stock prices and other stock-specific data from 2015-01-01 to 2018-11-1. They can be easily used when there is no strong demand for up-to-date data. By the way, we can load historical stock prices of S&P companies mentioned in the SymbolAndCap.csv file and return them together with their market capitalizations for further use. The code for updating the stock pool is in the file 'Access Data.ipynb'.

**Interaction: Views Collection:**

To achieve our purpose for customization, we also need to ask for views from users. In our program, we could deal with two kinds of views: Absolute view & Relative view. In order to get views from users, we need to recognize the input provided by users. Therefore, we chose to use Regular Expression method to complete this part. Based on the specific form we provided, users could type their views (both absolute and relative) into our project with proofreading, which is beneficial for not only users but also our project to calculate results. What is more, to better interact with users, we print out the requirement for typing holds, which could help users to type in their views in a right way. (For more details, please run the corresponding code and get more information about the format to input absolute views and relative views)


**Here are main steps to complete the model:**
- To start with, we need to obtain the matrix of return and variance-covariance matrix of specific stocks, which would be used during the calculation. 
- Then, we calculate the optimal portfolio based on Markowitz Model using optimization method. Based on the optimized result, we could find out the valid frontier of portfolio. And we could give out the optimal portfolio according to Markowitz Model. 
- After that, we re-calculate the portfolio using Blacklitterman Model. This time, we will take investor's views into consideration. With different views, the project would adjust the matrix of return of each stock. Using updated matrices, we could re-calculate the optimal portfolio frontier and corresponding optimal solution. 


**Constructing User's view matrix based on investment portfolio(Function:Matrix View and link):**
- Input:
  (1)The selected assets' symbols from privious selection part input by users.
  (2)Users investing views(abosulute and relative)from previous interaction part into the funciton;
- Constrtucting view matrix based on excess return given by their relative and absolute views, for example:[0.02,0.03,0.04]
- Setting empty link matrix to link every view into the investment assets pool, if user select n assets to be a portfolio and has k views, then the link matrix should be a k * n matrix; 
- For absolute views, the weight in link matrix should be 1; for relative views the weights in matrix should be -1 and 1 according to ezch assets position in users view. Finally, the sum of each row in the link matrix should be 0 for relative views.
- Return the view matrix and link matrix for further blacklitterman model.


**Optimizing Assets Allocation Weights based on Markowitz Model(Function:frontier_of_portfolio):**

The main idea of this part is to optimize the portfolio by adjusting its weights for different assets. The objective function is minimizing the variance of the portfolio, given the target expected return. 
- The input of the function should be: 
  (1)Rp: the matrix of return of assets derived by historical data;
  (2)Vp: the variance-covariances matrix between different assets;
  (3)rf: risk-free rate in the market. This is a given value. We set it equal to 0.015.
- The main procedure of the function is as follows:
  (1)Choose different target expected return; 
  (2)Optimize(Minimize) the objective function(the variance of the portfolio) by adjusting the weights of assets
  (3)Return the arrays of given expected returns and optimized variance of portfolio


**Optimizing Assets Allocation Weights(Function:weight_MV):**

Blacklitterman mainly depends on the technique of reverse optimization of conventional approach to get optimal allocation of assets in a given portfolio. Therefore, after aassets information collection, we should build function to sovle the optimal allocation weights of each assets in the portfolio based on Markowitz Model.
- Input the estimated parameters of the portfolio:
  (1)Portfolio expected returns
  (2)variance-covariance matrix of the assets pool.
- Setting the optimization objective function:
  Maximize the sharp ratio of the portfolio, which is the portfolio's express return divided by portfolio's variance.
- Subject to: the sum of weight should equal to 1; 
- Boundary: each assets' weight should be less or equal to 1 and be non-negative
- Using Sequential Least Squares Programming Method to get optimal allocation weights 
- Return the optimal allocation weights as an array.


**Optimizing allocation weights based on implied equilibrium return and investors' views(Function:optimal_portfolio_based_on_equilibrium_returns:**

After constructing the views matrix and link matrix to express the investors' views on some assets of the portfolio, we need to add these views to the implied equilibrium excess return to get new optimal weights, the weight of view is determined by the scaling factor for views. This scalar number indicating the uncertainty of the CAPM distribution (0.025-0.05). If this scalar is too high, it will make a very weak statement for our prior estimate of the mean.The scaling factor here is set to be 0.025, referring to Lee's paper materials. User can also set this scalar equals to 1 divided by observation numbers.
- Input of the function should be:
  (1)view matrix
  (2)link matrix to assets pool, scaling factor
  (3)implied equilibrium excess return vector
  (4)variance-covariance matrix of original portfolio
  (5)risk-free rate
- Calculate the uncertainty of views and uncertainty of implied equilibrium excess return;
- Calculate the adjusted implied equilibrium excess return by adding view matrix into it, the weight is measured by the inverse of uncertainty.
- Optimize: Using the new equilibirum excess return, which including the new infomation of investors' views, the weight is determined by the scaling factor for views to get new allocation weights and efficient frontier.
- Return the blacklitterman allocation weights, new optimal portfolio return and variance, the efficient frontier.


**Making integrated graph of efficient frontier and tangent point:**
- After optimizing the portfolio based on Markowitz, Implied Excess Return and Blacklitterman Model,drawing the efficient frontier of three models' optimal results.


**Output Collection:**
- Output the graph of optimal results based on three models to make a comparison for user;
- Output the optimal allocation weights of three models into dataframe;
- Output the variance covariance matrix of the selected assets in user's portfolio for reference.


**Further Reference for using this project for better adjustment:**

Blacklitterman Model has different scaling factor('scalar') based on academic research and professional industry experience, the scalar and the uncertainty in the views are the most abstract and difficult to specify parameters of the model. Therefore, i recommend users to change scalar in the function based on their confidence of expressed views.

