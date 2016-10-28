import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
from collections import Counter

def cal_entropy(list):
	Count = Counter(list)
	total = len(list)
	entropy = 0
	for i in Count:
		entropy += -1*Count[i]/total*np.log2(Count[i]/total)
	return entropy
def test_all_same(list, example):
	for i in list:
		if not i==example:
			return False
	return True
class treeNode(object):
	def __init__(self, parent, instances_num):
		self.parent = parent
		self.children = {}
		self.index_num = None #the index_num will be use in this node
		self.target = None
		self.likely_target = None  #if the tree isn't grow completely, use likely target 
		self.instances_num = instances_num
		
	#generate the child dict
	def end(self, data):
		#collect all instances' class in this node
		classes = list(map(lambda i:data[i][len(data[i])-1], self.instances_num))
		#find the dominant one and change self.target from None to this class
		self.target = Counter(classes).most_common(1)[0][0]
	#check if all instances in this node are in same class
	#if not, return False
	#if true, return true, the node should be ended
	def check_end(self, data):
		for i in self.instances_num:
			if not data[i][len(data[i])-1]==data[0][len(data[0])-1]:
				return False
		return True
	def entropy(self, data, index_num=-1):
		if index_num==-1:
			classes = list(map(lambda i:data[i][len(data[i])-1], self.instances_num))
			return cal_entropy(classes)
		elif not index_num in range(len(data[0])-1):
			print("index_num overflow") #in case of wrong index_num
		else:
			#collect all instances' indexes
			indexes = list(map(lambda i:data[i][index_num], self.instances_num))
			#count the kind of indexes
			indexes_value = Counter(indexes)
			#use dict to storage instances with different index_value
			#initial this dict
			instances_class = {}
			for i in indexes_value:
				instances_class[i]=[]
			for i in self.instances_num:
				instances_class[data[i][index_num]].append(data[i][len(data[i])-1])
			entropy = 0
			for i in instances_class:
				entropy += len(instances_class[i])/len(self.instances_num)*cal_entropy(instances_class[i])
			return entropy
	def generateChild(self, data, index):
		child_instances={}
		for i in self.instances_num:
			if data[i][index] in child_instances:
				child_instances[data[i][index]].append(i)
			else:
				child_instances[data[i][index]]=[i]
		for i in child_instances:
			self.children[i]=treeNode(self, child_instances[i])
	def grow(self, data, index_list, threshold):
		self.likely_target = Counter(list(map(lambda i:data[i][len(data[i])-1], self.instances_num))).most_common(1)[0][0]
		if self.check_end(data) or len(index_list)==0:
			self.end(data)
			return 0
		node_entropy = self.entropy(data)
		#the var below storage the entropy change brought by each index
		information_gain_ratio = {}
		for i in index_list:
			information_gain_ratio[i]=(node_entropy-self.entropy(data, i))/cal_entropy(list(map(lambda k:data[k][i], self.instances_num)))
		max_infromation_gain_ratio = sorted(information_gain_ratio.items(), key = lambda k:k[1], reverse=True)[0]
		if max_infromation_gain_ratio[1]<threshold:
			self.end(data)
			return 0
		#generate child tree by index max_infromation_gain_ratio[0]
		self.generateChild(data, max_infromation_gain_ratio[0])
		self.index_num=max_infromation_gain_ratio[0]
		new_index_list=index_list.copy()
		del new_index_list[max_infromation_gain_ratio[0]]
		for i in self.children:
			self.children[i].grow(data, new_index_list, threshold)
	def purning(self, data, alpha):
		before_purning = 0
		for i in self.children:
			before_purning += len(self.children[i].instances_num)*self.children[i].entropy(data)
		before_purning += alpha*len(self.children)
		after_purning = self.entropy(data)*len(self.instances_num)
		if after_purning < before_purning:
			self.children = {}
			self.end(data)
		for i in self.children:
			self.children[i].purning(data,alpha)
	#Check the tree's children and itself
	#the instances in children should be classified correctly
	#its target should be the maximum element in its instances
	def self_check(self, data):
		for i in self.children:
			if not test_all_same(list(map(lambda k:data[k][self.index_num], self.children[i].instances_num)),i):
				print('wrong instances')
				print(i,' in ', self.index_num)
				self.children[i].self_check(data)
		if self.target:
			a=list(map(lambda k:data[k][len(data[k])-1], self.instances_num))
			if not Counter(a).most_common(1)[0][0]==self.target:
				print('wrong target')
				print(self.target, 'should be', Counter(a).most_common(1)[0][0])
		print ('check passed')
	#input instance x, use the tree make decision
	def apply(self, x):
		#where x has a dimension as interpret
		if self.target:
			return self.target
		if not x[self.index_num] in self.children:
			return self.likely_target
#		print(self.index_num," ",x[self.index_num])
		return self.children[x[self.index_num]].apply(x)
	def printTree(data):
		pass

def makeDecisionTree(data, threshold):
	#initial index interpret
	#key:value -> column_in_inputdata: [choice1, choice2...]
	index={}
	#initial index_entropy
	for index_num in range(len(data[0])-1):
		index[index_num]=[]
	for i in range(len(data)):
		for index_num in range(len(data[0])-1):
			if not data[i][index_num] in index[index_num]:
				index[index_num].append(data[i][index_num])
	#index set finished
	decisionTree = treeNode(None, list(range(len(data))))
	decisionTree.grow(data, index, threshold)
	return decisionTree

data=[line.replace("\n","").split(',') for line in open('car.data').readlines()]
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

parameter_study=[]
for alpha in list(map(lambda i:(i+1)*0.1,range(20))):
	list_threshold=[]
	for threshold in list(map(lambda i:(i+1)*0.01,range(20))):
		decisionTree = makeDecisionTree(train_data, threshold)
		decisionTree.purning(data, alpha)
		account = 0
		for i in range(len(check_data)):
			if not decisionTree.apply(check_data[i])==check_data[i][len(check_data[i])-1]:
				account += 1
		list_threshold.append(1-account/len(check_data))
	parameter_study.append(list_threshold)
	
fig = plt.figure()
ax = fig.gca(projection='3d')
alpha = np.arange(0.1, 2.1, 0.1)
threshold = np.arange(0.01, 0.21, 0.01)
alpha, threshold = np.meshgrid(alpha, threshold)
surf = ax.plot_surface(alpha, threshold, np.array(parameter_study),rstride=1, cstride=1, cmap=cm.coolwarm,linewidth=0, antialiased=False)
plt.show()
#for threshold in list(map(lambda i:(i+1)*0.02,range(10))):
#	decisionTree = makeDecisionTree(train_data, threshold)
#	account = 0
#	for i in range(len(check_data)):
#		if not decisionTree.apply(check_data[i])==check_data[i][len(check_data[i])-1]:
#			account += 1
#	print(threshold," ",account/(len(check_data)))