import os,sys,shutil

#########config part#######
#def getAllJpg(dir):
#	filelist = os.listdir(dir)
#	jpgList = []
#	for file in filelist:
#		if  file.split(".")[-1] == "jpg":
#			jpgList.append(file)
#	return(jpgList)


print(sys.argv)

argsList = sys.argv
#argsList = ["haha","ans1.txt","Results.txt"]
assert len(argsList) == 3 or len(argsList) == 4 or len(argsList) == 1
if len(argsList) == 3:
	jpgDir = "."
elif len(argsList)== 4:
	jpgDir = argsList[3]
else:
	back = "usage:\n"+"example: "+"getRec.exe cnn_ans.txt bp_ans.txt jpgdir"
	print(back)
	exit(1)

targetFileNames = ["same.txt","none.txt","different.txt",
				argsList[1].split(".")[0]+"y.txt",
				argsList[2].split(".")[0]+"y.txt"]
dirsDiff = [dir.split(".")[0]+"Y" for dir in argsList[1:3]]
fileDirDict = {"same":targetFileNames[0],
			   "none":targetFileNames[1],
			   "different":targetFileNames[2],
				dirsDiff[0]:targetFileNames[3],
				dirsDiff[1]:targetFileNames[4]
}
fr1 = open(argsList[1],"r")
fr2 = open(argsList[2],"r")

content1 = fr1.readlines()
content2 = fr2.readlines()
count_fr1 = len(content1)
count_fr2 = len(content2)
print("length:",count_fr1)

if count_fr1 != count_fr2:
	print("Items in two files are different!! Please check!!")
	exit(1)
	
#############create dirs###############
fw = {}
for dir,file in fileDirDict.items():
	if not os.path.exists(dir):
		os.makedirs(dir)
	fw[dir] = open(dir+"/"+file,"w")

#################split files############	
for item1,item2 in zip(content1,content2):
	group1 = item1.split()
	group2 = item2.split()
	
	assert group1[0] == group2[0]
	sumLength = len(group1)+len(group2)
	if sumLength == 2:
		contetTosave = group1[0]+"\n"
		fw["none"].write(contetTosave)
		shutil.copyfile(jpgDir+"/"+group1[0],"none/"+group1[0])
	if sumLength == 3:
		if len(group1) == 1: # ans2 has results
			contetTosave = group1[0]+" "+group2[1]+"\n"
			fw[dirsDiff[1]].write(contetTosave)
			shutil.copyfile(jpgDir+"/"+group1[0],dirsDiff[1]+"/"+group1[0])
		else:        # ans1 has results
			contetTosave = group1[0]+" "+group1[1]+"\n"
			fw[dirsDiff[0]].write(contetTosave)
			shutil.copyfile(jpgDir+"/"+group1[0],dirsDiff[0]+"/"+group1[0])
	if sumLength == 4:
		if group1[1] == group2[1]:
			contetTosave = group1[0]+" "+group1[1]+"\n"
			fw["same"].write(contetTosave)
			shutil.copyfile(jpgDir+"/"+group1[0],"same/"+group1[0])
		else:
			contetTosave = group1[0]+" "+group1[1]+" "+group2[1]+"\n"
			fw["different"].write(contetTosave)
			shutil.copyfile(jpgDir+"/"+group1[0],"different/"+group1[0])
fr1.close()
fr2.close()
for dir in fileDirDict:
	fw[dir].close()
	

		