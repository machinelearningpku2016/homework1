import csv

data=[line.replace("\n","").split(',') for line in open('data/car/car.data').readlines()]
train_list=[]
check_list=[]
test_list=[]
for i in range(len(data)):
	if i%7==0 :
		check_list.append(i)
	if i%7==1:
		test_list.append(i)
	else:
		train_list.append(i)
train_data=list(map(lambda k:data[k], train_list))
check_data=list(map(lambda k:data[k], check_list))
test_data=list(map(lambda k:data[k], test_list))

#统计类型
n = 6
typestatistics = []
N = len(train_data)
for i in range(0,n + 1):
    typestatistics.append([])
for data in train_data:
    for i in range(0,n + 1):
        atype = data[i]
        if typestatistics[i].count(atype) == 0:
            typestatistics[i].append(atype)
typecount = []
for i in range(0,n + 1):
    typecount.append(len(typestatistics[i]))


condicount = []
condiprob = []
for i in range(0,n):
    condicount.append([])
    condiprob.append([])
    for x in range(0,typecount[i]):
        condicount[i].append([])
        condiprob[i].append([])
        for y in range(0,typecount[n]):
            condicount[i][x].append(0)
            condiprob[i][x].append(0.0)
ycount = []
for typey in range(0,typecount[n]):
    ycount.append(0)

#统计condicountcount
for i in range(0,N):
    y = typestatistics[n].index(train_data[i][n])
    ycount[y] = ycount[y] + 1
    for j in range(0,n):
        x = typestatistics[j].index(train_data[i][j])
        condicount[j][x][y] = condicount[j][x][y] + 1

#估计
for i in range(0,n):
    for x in range(0,typecount[i]):
        for y in range(0,typecount[n]):
            Sj = float(typecount[i])
            lamda = 1.0
            condiprob[i][x][y] = (float(condicount[i][x][y]) + lamda) / (float(ycount[y]) + Sj * lamda)

#测试
correct = 0
wrong = 0
classdata = test_data
Ntest = len(classdata)
for data in classdata:
    pridprob = []
    for y in range(0,typecount[n]):
        pridprob.append(1.0)
        for i in range(0,n):
            x = typestatistics[i].index(data[i])
            pridprob[y] = pridprob[y] * condiprob[i][x][y]
    pridtype = 0
    for y in range(1,typecount[n]):
        if pridprob[y] > pridprob[pridtype]:
            pridtype = y
    #print (pridtype)
    realy = typestatistics[n].index(data[n])
    #print (realy)

    if pridtype == realy:
        correct = correct + 1
    else:
        wrong = wrong + 1

accuracyrate = float(correct) / float(correct + wrong)
print(accuracyrate)