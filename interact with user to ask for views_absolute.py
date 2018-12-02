###Also, we need to ask investors to obtain their views towards the assets they invest.

##Firstly, absolute views
print('''Now, please type in your views towards the assets you would like to invest.\n
There are two kinds of views you could input:\n
Absolute views & Relative views.\n
To express your views, you could type in views in formats as follows:\n
For Absolute views: you could type in 'AMZN 0.05',\n
which means that the asset 'Amazon' could achieve the rate of return at (5%+rf).\n
5% is the excess rate of return compared with risk-free rate.\n
(Attention please: the excess rate of return should be positive)\n
Please type in your absolute views towards assets:\n
(Please use decimal numbers to reflect the return, e.g. 0.03 stands for 3% in rate of return)\n
(one single example:'AMZN, 0.05; CVX, 0.03')\n
(If you do not hold any absolute views, just press enter.)''')

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
