import os,shutil

blockNum = 500

fileList = os.listdir()
jpgList = []
for file in fileList:
	if os.path.splitext(file)[1] == ".jpg":
		jpgList.append(file)

sizeJpgList = len(jpgList)
cnt = 0

for i in range(0,sizeJpgList,blockNum):
	os.makedirs("split{}".format(cnt))
	
	for j in range(i,min(i+blockNum,sizeJpgList)):
		shutil.move(jpgList[j],"split{}/{}".format(cnt,jpgList[j]))
	cnt += 1
print("OK!")