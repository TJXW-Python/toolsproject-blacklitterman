%matplotlib inline
import scipy.optimize
from numpy import *
from pandas import *
import re

from datetime import datetime
######################### Have to install pandas-datareader on terminal first!!! ######################
# terminal: conda install -c anaconda pandas-datareader 
# or $ pip install pandas-datareader
import pandas_datareader as pdr



##At the beginning of the project######################################################################
#We need to ask users to provide the assets they would like to invest##################################

## Note here we put the 'SymbolsAndCaps.csv' under the folder named 'data', you can find it in
## our github project. To ensure the program can be be excuted successfully, you MUST put the python file 
## and 'data' folder under the same folder.
base = 'data/'
pool_file = base + 'SymbolsAndCaps.csv'    
    
# Function loads stocks symbols and their market capitalizations, as of Nov 29, 2018
def load_symbols_and_caps(file):
    symbols_caps = pandas.read_csv(file, index_col = None) # symbols_caps is a pandas.dataframe
    symbols_caps.dropna(how = "all", inplace = True)
    symbols = list(symbols_caps['symbols'])
    caps = list(symbols_caps['caps'])
    return symbols, caps

# Function takes in user input and returns a list of stock symbols if input is legal and returns [] otherwise
def select_assets(*args):
    pool_symbols, _ = load_symbols_and_caps(pool_file)
    try:
        assets = ''.join(args).upper().split(' ')
    except:
        print('\n\nWarning: Illegal input!\n\n')
        return []
    if set(pool_symbols).union(set(assets)) != set(pool_symbols):
        print('\n\nWarning: Illegal input format or stock not in our pool! Please type again!\n\n')
        return []
    else:
        print('\n\nCongratulations! Legal Input!')
        return assets

assets_list = []
while assets_list == []:
    assets_list = input('''Welcome to use the Blacklitterman Model project. \nBased on the performance, we provide 20 assets that are worthy of investing. \nThe symbols of these 20 assets are as follows: \n\nAAPL MSFT AMZN JNJ GOOG JPM XOM FB GOOGL BRK-B \nWMT BAC UNH PFE WFC V VZ PG CVX T
    \nPlease type in the stock symbols you are interested in and separate them with a white space. Press Enter to complete. For example, AMZN AAPL BRK-B\n\n''')
    assets_list = select_assets(assets_list)    
    
# Function extract market caps corresponding to the stock symbols entered by the user
# and also loads the historical stock prices and returns stock symbols, caps and historical prices
def load_data(assets_list):
    
    pool_symbols, pool_caps = load_symbols_and_caps(pool_file) # first load all symbols and caps in the pool
    
    symbols = list(set(assets_list)) # remove repeated symbols
    caps = [] # extract market caps of the stocks chosen by the user
    for s in symbols:
        caps.append(pool_caps[pool_symbols.index(s)])
    
    price_arrays = [] # array of close prices of each stock chosen by the user
    for s in symbols:
        data = pandas.read_csv('data/%s.csv' % s, index_col=None, parse_dates=True) # data is a pandas.dataframe
        prices = list(data['Close'])
        price_arrays.append(prices) 
    return symbols, caps, price_arrays # price_arrays is an n*T list    

# We get symbols caps, price_arrays from the load_data function for later use.
symbols, caps, price_arrays = load_data(assets_list)

#Functions get market capitilizaions from our chosen data
#and use these data to calculate weights, return and covariance
def compute_some_statistics(price_arrays):
    #Transfer a list of prices into a matrix
    price_up = numpy.mat(price_arrays)
    #Use our data to compute daily return
    price_row = numpy.size(price_up, 0)
    price_col = numpy.size(price_up, 1)
    data_return = numpy.zeros([price_row, price_col - 1])
    for i in range(price_row):
        for j in range(price_col - 1):
            p_start = price_up[i, j]
            p_end = price_up[i, j + 1]
            data_return[i, j] = (p_end - p_start)/ p_start      
    cal_return = numpy.array([])
    for i in range(price_row):
        mean_return = numpy.mean(data_return[i])
        cal_return = numpy.append(cal_return, mean_return)
    #Use our data to compute daily var_cov matrix  
    var_cov_matx = cov(data_return)
    #We assume that there are 250 tarding days in one year, and calculate annulized return
    #and annulized var_cov matrix
    cal_return = (1 + cal_return) ** 250 - 1
    var_cov_matx  = var_cov_matx * 250
    return cal_return, var_cov_matx

#Calculate weight from market caps
#Calculate return and var_cov_matrix
W = np.array(caps) / sum(caps)
Rp, Vp= compute_some_statistics(price_arrays)
#In practice, this 1.5% real risk-free rate is the rate that investors expect to earn after 
#inflation from a risk-free investment with a 10-year duration after inflation.
rf = 0.015

###Also, we need to ask investors to obtain their views towards the assets they invest.

##Firstly, absolute views

print('''--------------------------------------------------------------------------\n
Now, please type in your views towards assets in your selection set.\n
There are two kinds of views you could input: Absolute views & Relative views.\n
In this part, we only ask you to input your absolute views. \n
To express your absolute views, you could type in views in formats as follows: \n
'AMZN 0.05', which means that the asset 'Amazon' could achieve the rate of return at (5%+rf).\n
Here, 5% is the excess rate of return compared with risk-free rate.\n
(Attention please: the excess rate of return should be positive)\n
Please type in your absolute views towards assets:\n
(Please use decimal numbers to reflect the return, e.g. 0.03 stands for 3% in rate of return)\n
(one single example:'AMZN, 0.05; CVX, 0.03')\n
(If you do not hold any absolute views, just press enter.)''')
view = {'absolute':[],'relative':[]}
abso_view_judge = 1
while abso_view_judge:
    abso_view_judge = 0
    abso_view_ori = input()
    if not abso_view_ori:
        abso_view_ori = 0
        view['absolute'] = []
        break
    else:
        abso_pattern = r'[A-Za-z-]+\W*[0-9.-]+'
        user_abso_view_str = re.findall(abso_pattern,abso_view_ori)
        view = dict()
        abso_view_list = []
        for i in user_abso_view_str:
            abso_name = r'^[A-Za-z-]+'
            abso_excess_return = r'[0-9.-]+$'
            temp_name = re.findall(abso_name,i)
            temp_ret = re.findall(abso_excess_return,i)
            name_judge = 0
            for j in symbols:
                if j == temp_name[0]:
                    name_judge += 1
            if name_judge > 0 and float(temp_ret[0]) > 0:
                abso_view_list.append([temp_name[0],'',temp_ret[0]])
            elif name_judge == 0:
                print('Please input view about assets that you want to invest!\nPlease input your view again!')
                abso_view_judge = 1
                continue
            elif float(temp_ret[0]) <= 0:
                print('Attention please: the excess return should be positive!\nPlease input your view again!')
                abso_view_judge = 1
                continue
        view['absolute'] = abso_view_list

#check the view input
view
################################################################################################

###Ask for relative views

print('''----------------------------------------------------------------------------------\n
Now, please type in your relative views towards assets in your selection set.\n
This kind of view should claim relationship between two different assets in your selection set.\n
To input your relative views, you should compare the return of two chosen assets\n
using specific patterns as follows(should include > or <): 'AMZN > CVX 0.03',\n
which means that you think that the asset 'AMZN' will have a higher return\n
compared with 'CVX', and the difference between them should be 3%(=0.03).\n
So, a valid example could be: 'AMZN > CVX 0.03;AAPL < JPM 0.02'\n
(Attention please: the difference here should be positive, for you can input < or >)''')

relat_view_judge = 1
while relat_view_judge:
    relat_view_judge = 0
    relat_view_ori = input()
    if not relat_view_ori:
        relat_view_judge = 0
        view['relative'] = []
        break
    else:
        relat_pattern = r'[A-Za-z-]+\W*[<>]\W*[A-Za-z-]+\W*[0-9.-]+'
        user_relat_view_str = re.findall(relat_pattern,relat_view_ori)
        if not user_relat_view_str:
                print('Please input valid relative views!\nPlease input again:')
                relat_view_judge = 1
                continue
        relat_view_list = []
        for i in user_relat_view_str:
            relat_both_name = r'^[A-Za-z-]+\W*[<>]\W*[A-Za-z-]+'
            relat_excess_return = r'[0-9.-]+$'
            temp_both_name = re.findall(relat_both_name,i)
            temp_ret = re.findall(relat_excess_return,i)
            smaller = 0
            for k in i:
                if k == '<':
                    smaller = 1
            relat_name1 = r'^[A-Za-z-]+'
            relat_name2 = r'[A-Za-z-]+$'
            temp_name1 = re.findall(relat_name1,temp_both_name[0])
            temp_name2 = re.findall(relat_name2,temp_both_name[0])
            name1 = temp_name1[0]
            name2 = temp_name2[0]
            if name1 == name2:
                print('Cannot compare two assets that are the same.')
                relat_view_judge = 1
                continue
            if smaller == 1:
                temp = name1
                name1 = name2
                name2 = temp
            name_judge = 0
            for j in symbols:
                if j == name1 or j == name2:
                    name_judge += 1
            if name_judge == 2 and float(temp_ret[0]) > 0:
                relat_view_list.append([name1,name2,temp_ret[0]])#adjust the sequence to make name1 > name2
            elif name_judge < 2:
                print('Please input view about assets that you want to invest!\nPlease input your view again!')
                relat_view_judge = 1
                continue
            elif float(temp_ret[0]) <= 0:
                print('Attention please: the excess return should be positive!\nPlease input your view again!')
                relat_view_judge = 1
                continue
        view['relative'] = relat_view_list
#check the view input
view
###################################################################################

##This part of function is to created the view matrix and link matrix according to input of users views
def matrix_view_and_link(symbols,view):
    #set view matrix
    view_=[]
    for i in view:
        for j in view[i]:
            view_.append(j)                
    view_matrix = [view_[i][2] for i in range(len(view_))]
    view_matrix =array([float(i) for i in view_matrix])
    
    #set an empty view link matrix 
    p_count = len(symbols)
    view_count = len(view_matrix)
    link_matrix= zeros([view_count,p_count]) 
    
    #refill the link matrix according to the view matrix
    i = 0
    symbols_index = dict()
    for asset in symbols:
        symbols_index[asset] = i
        i +=1
    for i in range(len(view_)):
        symbol_1=view_[i][0]
        symbol_2=view_[i][1]
        link_matrix[i,symbols_index[symbol_1]] = 1
        #recognize the absolute views and relative views
        if symbol_2:
            link_matrix[i,symbols_index[symbol_2]] = -1
          
    return view_matrix, link_matrix

##Compute the view_matix and link_matrix from our user input 
# for later use
view_matrix, link_matrix = matrix_view_and_link(symbols, view)

###############################################################################################

##The function to calculate the valid frontier of portfolio constructed with given assets##
def frontier_of_portfolio(Rp, Vp, rf):
    exp_mean = []
    opt_var = []
    
    num_of_assets = len(Rp)
    
    min_ret = min(Rp)
    max_ret = max(Rp)
    group = 30 #Calculate 30 groups of optimal solution
    interval = (max_ret - min_ret)/(group - 1)
    ret_list = []
    for i in range(group):
        ret_list.append((min_ret + interval * i))
    # For given level of return r, find weights which minimizes portfolio variance.  
    def func_for_optimization(Wp, Rp, Vp, r):
        mean = dot(Wp, Rp)
        var = dot(dot(Wp, Vp), Wp)
        penalty = 100 * abs(mean - r)
        #To guarantee that the mean of return of the portfolio should equal to r
        return var + penalty
    for r in ret_list:#The recursion should follows different target return
        Wp = ones(num_of_assets) / num_of_assets #The initial weight for optimization
        boundary = [] 
        for i in range(num_of_assets):
            boundary.append((0, 1))
            #The boundary of each weight for a specific asset
        constraint_ = ({'type': 'eq', 'fun': lambda Wp: sum(Wp) - 1.0})
        #The constraints in optimizing that the sum of weights should equal to 1
        opt_result = scipy.optimize.minimize(
            func_for_optimization, Wp, (Rp, Vp, r), method = 'SLSQP',
            constraints = constraint_, bounds = boundary)
        
        if opt_result.success:
            exp_mean.append(r)
            opt_var.append(dot(dot(opt_result.x, Vp), opt_result.x))
        else:
            raise BaseException(opt_result.message)
    
    return array(exp_mean), array(opt_var)
###############################################################################################

##This function is used to calculate tangent point based on optimal portfolio and risk-free rate
def weight_MV(Rp, Vp, rf):
    def weight_initial(Rp):                 # initial weight of the optimization procedure
        port_count = len(Rp)
        Wp=[]
        for i in range(port_count):
            Wp.append(1 / port_count)         # set all of these assets with equal weights in the portfolio
        return Wp
    def MV_object_function(Wp, Rp, Vp, rf):    # return the objective function of MV_optimization $$$$$$$$change 
        p_mean = sum(Rp * Wp)                 #calculate the mean return of the portfolio
        p_var = dot(dot(Wp , Vp), Wp)          #calculate the variance of the portfolio
        p_sharp_ratio= (p_mean - rf) / sqrt(p_var)
        object_func =  1 / p_sharp_ratio
        return object_func
    def MV_optimal(Rp, Vp, rf):
        Wp = weight_initial(Rp)              # input the initial weight
        bound = []                           # add each bound of every assets weight in the spread from [0,1]
        for i in range(len(Rp)):
            bound.append((0., 1.))                 
        constraint = ({'type': 'eq',         # give the constraints of optimization problem, the sum of weight equals to 1.0
                          'fun': lambda Wp: sum(Wp) - 1.}) 
        weight_optimal =scipy.optimize.minimize(MV_object_function, 
                                                Wp,(Rp, Vp, rf), method='SLSQP', constraints=constraint, bounds=bound)
                                             #calculate the optimal weight of each assests in the portfolio in MV model
        if weight_optimal.success:
            return weight_optimal.x
        else:
            raise BaseException(weight_optimal.message)
    return MV_optimal(Rp, Vp, rf)
#####################################################################################################################

##This part is used to optimize the portfolio based on equilibrium excess return##
def optimal_portfolio_based_on_equilibrium_returns(Rp,Vp,rf):
    Wp = weight_MV(Rp,Vp,rf)
    opt_mean = dot(Wp,Rp)
    opt_var = dot(dot(Wp,Vp),Wp)
    frontier_mean,frontier_var = frontier_of_portfolio(Rp,Vp,rf)
    result_implied_return = dict()
    result_implied_return['Weights']=Wp
    result_implied_return['Tangent_mean']=opt_mean
    result_implied_return['Tangent_var']=opt_var
    result_implied_return['Frontier_mean']=frontier_mean
    result_implied_return['Frontier_var']=frontier_var
    return result_implied_return

##W is the market capitalization weights
def equilibrium_excess_return(W,Rp,Vp):
    mean = dot(W,Rp)
    var = dot(dot(W,Vp),W)
    lamuda = (mean - rf)/var
    return dot(dot(lamuda,Vp),W)

Pi = equilibrium_excess_return(W,Rp,Vp)##Using market capitalization weight W

result_eq = optimal_portfolio_based_on_equilibrium_returns(Pi+rf,Vp,rf)

###############################################################################################

## This part is used to optimize the portfolio based on equilibrium excess return 
## after adding investers' views and relation matrix into the equilibrium excess return--"Pi"
def optimization_adding_views(Vp,view,view_link,Pi,rf):

    def pi_add_view(Vp,view,view_link,Pi):  
        scalar = 0.025       # scaling factor for blacklitterman model is set according to Lee's paper
        ##weight is measured by uncertainty, this is the uncertainty matrix of equilibrium excess return: pi_vol (n*n matrix)
        pi_vol = dot(scalar,Vp)                    
        view_vol= dot(dot(dot(scalar,view_link),Vp),transpose(view_link))  
        pi_vol_inv = inv(pi_vol)                
        view_vol_inv = dot(dot(transpose(view_link),inv(view_vol)),view_link) 
        pi_view_weighted =dot(pi_vol_inv,Pi)+dot(dot(transpose(view_link),inv(view_vol)),view) 
        pi_new= dot(inv(view_vol_inv +pi_vol_inv), pi_view_weighted)  
        ##the new equilibrium return weighted by the inverse of uncertainty and standardization
    
        return pi_new                          

    # get the optimal allocation weights and efficent frontier based on new equilibrium excess return
    pi_new = pi_add_view(Vp,view,view_link,Pi)   
    Wp_new = weight_MV(pi_new+rf,Vp,rf)
    mean_new = sum(Wp_new * (pi_new+rf))
    var_new = dot(dot(Wp_new,Vp),Wp_new)
    mean_frontier, var_frontier = frontier_of_portfolio(pi_new+rf,Vp,rf)
    
    result_adding_views= dict()
    result_adding_views['Pi']=pi_new
    result_adding_views['Weights']=Wp_new
    result_adding_views['Tangent_mean']=mean_new
    result_adding_views['Tangent_var']=var_new
    result_adding_views['Frontier_mean']=mean_frontier
    result_adding_views['Frontier_var']=var_frontier
    return result_adding_views
  
######################################################################################################

##This function is used to draw efficient frontier of given assets
def graph_efficient_frontier(optimal,label=None, color='black'):
    text(optimal['Tangent_var'] ** .5, optimal['Tangent_mean'], '   tangent', verticalalignment='center', color=color)
    scatter(optimal['Tangent_var'] ** .5, optimal['Tangent_mean'], marker='o', color=color), grid(True)
    plot(optimal['Frontier_var'] ** .5, optimal['Frontier_mean'], label=label, color=color), grid(True) 
    
##This function is used to add nodes pof assets and mark labels to each nodes in the graph
def graph_names(names, Rp, Vp, color='black'):
    scatter([Vp[i, i] ** .5 for i in range(len(Rp))], Rp, marker='x', color=color), grid(True)  
    for i in range(len(Rp)): 
        text(Vp[i, i] ** .5, Rp[i], '  %s' % names[i], verticalalignment='center', color=color) 


##################################################################################################
##Collect the optimal weight of 3 models
optimal_historical_data = optimal_portfolio_based_on_equilibrium_returns(Rp,Vp,rf)
optimal_implied_excess_return =optimal_portfolio_based_on_equilibrium_returns(Pi+rf,Vp,rf)
optimal_adding_views = optimization_adding_views(Vp,view_matrix,link_matrix,Pi,rf)

##output of the whole model reslut into dataframe and graphs:
def OUTPUT_MODEL(optimal_historical_data,optimal_implied_excess_return,optimal_adding_views):
    #Graph based on comparison among three models
    graph_names(symbols,Rp,Vp,color='blue')
    graph_efficient_frontier(optimal_historical_data,label='Historical Data', color='blue')

    graph_names(symbols, Pi+rf, Vp, color='green')
    graph_efficient_frontier(optimal_implied_excess_return,label='Implied Equilibrium Excess Return', color='green')

    graph_names(symbols,optimal_adding_views['Pi']+rf, Vp, color='red')
    graph_efficient_frontier(optimal_adding_views,label='Adding views', color='red')

    xlabel('variance $\sigma$'), ylabel('mean $\mu$'), legend(), show()
    
    ##This part will output a table to tell the users their optimal weights on their selecting assets based on three given models:
    display(pandas.DataFrame({'Return': Rp, 'Weight (original_MV_opt)': weight_MV(Rp,Vp,rf),
                          'Weight (Reverse Optimization)': optimal_portfolio_based_on_equilibrium_returns(Pi+rf,Vp,rf)['Weights'],
                          'Weight (reverse opt)': optimal_adding_views['Weights']}, index=symbols).T)
    display(pandas.DataFrame(Vp, columns=symbols, index=symbols))

 ######################################################################################################

OUTPUT_MODEL(optimal_historical_data,optimal_implied_excess_return,optimal_adding_views)



