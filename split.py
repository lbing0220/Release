#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os

LIMIT=5
file_count=0
url_list=[]
print("Please input the file_name which you want to split:")
print("The default name is eqpt.log")
orignal_name=input()
if (orignal_name==""):
	orignal_name="eqpt.log"

####Create folder split_file#######	
if not os.path.exists("split_file"):
	
	os.mkdir("split_file")
	
		
#########################################
####clean split_file
for file in os.listdir(r"./split_file"):
	os.remove(r"./split_file/"+file)
#########################################
with open(orignal_name) as f:
	file_name="./split_file/"+orignal_name+"__"+str(file_count)+".txt"
	for line in f:
		url_list.append(line)
		if len(url_list)<LIMIT:
			with open(file_name,'w') as file:
				for url in url_list:
					file.write(url)
			continue
		with open(file_name,'w') as file:
			for url in url_list[:-1]:
				file.write(url)
			file.write(url_list[-1].strip())
			url_list=[]
			file_count+=1
print(orignal_name +" has been splited "+str(file_count+1)+" files successfully")
print("Please check the split_file Directory")

