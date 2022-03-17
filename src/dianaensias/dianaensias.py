import numpy as np;
import pandas as pd

def avg_dissim_within_group_element(ele, element_list, dissimilarity_matrix):
	max_diameter = -np.inf
	sum_dissm = 0
	for i in element_list:
		sum_dissm += dissimilarity_matrix[ele][i]   
		if( dissimilarity_matrix[ele][i]  > max_diameter):
			max_diameter = dissimilarity_matrix[ele][i]
	if(len(element_list)>1):
		avg = sum_dissm/(len(element_list)-1)
	else: 
		avg = 0
	return avg

def avg_dissim_across_group_element(ele, main_list, splinter_list, dissimilarity_matrix):
	if len(splinter_list) == 0:
		return 0
	sum_dissm = 0
	for j in splinter_list:
		sum_dissm = sum_dissm + dissimilarity_matrix[ele][j]
	avg = sum_dissm/(len(splinter_list))
	return avg
	
	
def splinter(main_list, splinter_group, dissimilarity_matrix):
	most_dissm_object_value = -np.inf
	most_dissm_object_index = None
	for ele in main_list:
		x = avg_dissim_within_group_element(ele, main_list, dissimilarity_matrix)
		y = avg_dissim_across_group_element(ele, main_list, splinter_group, dissimilarity_matrix)
		diff= x -y
		if diff > most_dissm_object_value:
			most_dissm_object_value = diff
			most_dissm_object_index = ele
	if(most_dissm_object_value>0):
		return  (most_dissm_object_index, 1)
	else:
		return (-1, -1)
	
def split(element_list, dissimilarity_matrix):
	main_list = element_list
	splinter_group = []    
	(most_dissm_object_index,flag) = splinter(main_list, splinter_group, dissimilarity_matrix)
	while(flag > 0):
		main_list.remove(most_dissm_object_index)
		splinter_group.append(most_dissm_object_index)
		(most_dissm_object_index,flag) = splinter(element_list, splinter_group, dissimilarity_matrix)
	
	return (main_list, splinter_group)

def max_diameter(cluster_list, dissimilarity_matrix):
	max_diameter_cluster_index = None
	max_diameter_cluster_value = -np.inf
	index = 0
	for element_list in cluster_list:
		for i in element_list:
			for j in element_list:
				if dissimilarity_matrix[i][j]  > max_diameter_cluster_value:
					max_diameter_cluster_value = dissimilarity_matrix[i][j]
					max_diameter_cluster_index = index
		
		index +=1
	
	if(max_diameter_cluster_value <= 0):
		return -1
	
	return max_diameter_cluster_index

def diana(data, indexes):
	mat = np.array(indexes)
	all_elements = data
	dissimilarity_matrix = pd.DataFrame(mat,index=all_elements, columns=all_elements)
	current_clusters = ([all_elements])
	level = 1
	index = 0
	while(index!=-1):
		print(level, current_clusters)
		(a_clstr, b_clstr) = split(current_clusters[index], dissimilarity_matrix)
		del current_clusters[index]
		current_clusters.append(a_clstr)
		current_clusters.append(b_clstr)
		index = max_diameter(current_clusters, dissimilarity_matrix)
		level +=1
	print(level, current_clusters)










