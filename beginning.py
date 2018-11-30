import re
##At the beginning of the project
#We need to ask users to provide the assets they would like to invest
print('Welcome to use the Blacklitterman Model project.')
print('Based on the performance, we provided 20 assets that are worthy investing.')
print('The symbols of these 20 assets are as follows:')
print('1 GE; 2 CVX; ...')
print('Please select assets that you want to invest: ')
print('(enter the number of the assets, e.g. if you want to invest GE, type in 1; CVX for 2;...)')
illegal_asset = 100
judgement = 0
print('(please use list to type in, e.g. [1,4,6,7,9])')
while illegal_asset > 0 or judgement < 1:
    number_of_assets = input('hhaha')
    pattern1 = r'[0-9.]+'
    type_in_assets = re.findall(pattern1,number_of_assets)
    illegal_asset = 0
    select_assets = []
    for i in type_in_assets:
        a = int(float(i))
        if a < 0 or a > 20 or a != float(i):
            illegal_asset += 1
            print('Please type in integer numbers between 1-20!')
        exist = 0
        for j in select_assets:
            if j == a:
                exist += 1
        if exist >= 1:
            continue
        else:
            select_assets.append(a)
    if illegal_asset == 0:
        print(f'Your choices are assets: {select_assets}')
        print('Please verify your choice: 1 for Yes, 0 for No.')
        judge = input('judge = ')
        if int(float(judge)) == 1:
            judgement == 1
            break
        else:
            judgement == 0
            print('Please choose again:')
print(f'Your choices are assets: {select_assets}')
