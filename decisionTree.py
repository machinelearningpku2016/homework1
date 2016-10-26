import numpy as np
from collections import Counter

class treeNode(object):
	def __init__(self, parent, index, instances):
		self.parent = parent
		self.children = {}
		self.index_num = index_num #the index_num will be use in this node
		self.target = NULL
		self.instances = instances
		self.dataDimension = len(instances[0])-1
	#add a child tree to self
	def grow(index_value, child):
		self.children[index_value]:child
	def end():
		#collect all instances' class in this node
		classes = map(lambda i:instances[i][self.dataDimension+1],range(len(instances)))
		#find the dominant one and change self.target from NULL to this class
		self.target = Counter(classes).most_common(1)[0][0]
	def entropy(index_num=-1):
		if index==-1:
			classes = map(lambda i:instances[i][self.dataDimension+1],range(len(instances)))
			Count = Counter(classes)
			entropy = 0
			total = len(instances)
			for i in Count:
				entropy += -1*Count[i]/total*np.log2(Count[i]/total)
			return entropy
		elif not index_num in range(instances[0]-1):
			print("index_num overflow") #in case of wrong index_num
		else:
			#这里需要写按照index_num对应的index分类后的熵



	#input instance x, use the tree make decision
	def apply(x):
		#where x has a dimension as interpret
		if self.target:
			return self.target
		return self.children[x[self.index_num]].apply(x)

def makeDecisionTree(instances):
	#initial index interpret
	#key:value -> column_in_inputdata: [choice1, choice2...]
	index={}
	for index_num in range(len(instances[0]-1)):
		index[index_num]=[]
	for i in range(len(instances)):
		for index_num in range(len(instances[0]-1)):
			if not instances[i][index_num] in index[index_num]:
				index[index_num].append(instances[i][index_num])
	#index set finished

