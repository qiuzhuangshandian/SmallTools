import shutil,os,time

##########add dirs that contain same.txt##############
txtDirs = [
"20180412mongolia",
"ANPR_temp",
"D:\haien\projects\yoloMongolia\mongolia_images\Dahua\\20151027_P1",	
"D:\haien\projects\yoloMongolia\mongolia_images\Dahua\\20151107_P4\\temp",
# "D:\haien\projects\yoloMongolia\mongolia_images\\temp",
"D:\haien\projects\yoloMongolia\mongolia_images\\temp2",
"D:\haien\projects\yoloMongolia\mongolia_images\\test",
]
mergeDir = "merge"
if not os.path.exists(mergeDir):
	os.makedirs(mergeDir)

sourceFile = "same.txt"
#targetFile = mergeDir+"/ansMerge.txt"
nowTime = lambda: int(round(time.time()*10000))
#fw = open(targetFile,"w")
content = []
for dir in txtDirs:
	fr = open(dir+"\\"+"same\\"+sourceFile)
	tmpContent = fr.readlines()
	for item in tmpContent:	
		t = nowTime()	
		sourcejpg = dir+"\\"+"same\\"+item.split()[0]
		targetjpg = mergeDir+"\\"+str(t)+".jpg"
		shutil.copyfile(sourcejpg,targetjpg)
		time.sleep(0.001)
	fr.close() 

print("OK!")


	