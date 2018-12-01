###Ask for relative views
print('''Now, please type in your relative views towards assets.\n
This kind of view should claim relationship between two different assets,\n
both of which should come from your chosen assets.\n
To input your relative views, you should compare the return of two chosen assets\n
using specific patterns as follows(should include > or <):\n
'AMZN > CVX 0.03', which means that you think that the asset 'AMZN' will have a higher return\n
compared with 'CVX', and the difference between them should be 3%(=0.03).\n
So, a valid example could be:\n
'AMZN > CVX 0.03;AAPL < JPM 0.02'\n
(Attention please: the difference here should be positive, for you can input < or >)''')

relat_view_judge = 1
while relat_view_judge:
    relat_view_judge = 0
    relat_view_ori = input()
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
