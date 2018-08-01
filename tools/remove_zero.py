import os

sourceDir = "."
fileList = os.listdir(sourceDir)
print(len(fileList))

txtList_zero = []
for file in fileList:
	name,Suffix = file.split(".")
	if Suffix =="txt":
		if os.path.getsize(file) ==0:
			txtList_zero.append(file)

for txt in txtList_zero:
	name,_ = txt.split(".")
	os.remove(name+".jpg")
	os.remove(txt)