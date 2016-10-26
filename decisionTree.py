import numpy as np
from collections import Counter

def cal_entropy(list):
	Count = Counter(list)
	total = len(list)
	entropy = 0
	for i in Count:
		entropy += -1*Count[i]/total*np.log2(Count[i]/total)
	return entropy
class treeNode(object):
	def __init__(self, parent, instances_num):
		self.parent = parent
		self.children = {}
		self.index_num = None #the index_num will be use in this node
		self.target = None
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
#		print(type(index_list))
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
		del index_list[max_infromation_gain_ratio[0]]
		for i in self.children:
			self.children[i].grow(data, index_list, threshold)
	#input instance x, use the tree make decision
	def apply(self, x):
		#where x has a dimension as interpret
		if self.target:
			return self.target
		return self.children[x[self.index_num]].apply(x)
	def printTree(data):
		pass
def check_end_test(tree, data):
	for i in tree.instances_num:
		if not data[i][len(data[i])-1]==data[0][len(data[0])-1]:
			return False
	return True
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
#	print (index)
	decisionTree = treeNode(None, list(range(len(data))))
	decisionTree.grow(data, index, threshold)
	return decisionTree

data=[line.replace("\n","").split(',') for line in open('car.data').readlines()]
for threshold in list(map(lambda i:(i+1)*0.1,range(10))):
	decisionTree = makeDecisionTree(data[:1600], threshold)
	account = 0
	for i in range(1600,len(data)):
		if not decisionTree.apply(data[i])==data[i][len(data[i])-1]:
			account += 1
	print(threshold," ",account/len(data))