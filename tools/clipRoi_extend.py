import os,gc
import cv2 as cv
import numpy as np
#import time

#################
cutRatioControl = 0
sourceDir = "."
targetDir = os.path.join(os.getcwd(),"cliped")
##############

if not os.path.exists(targetDir):
	os.makedirs(targetDir)
print(targetDir)
fileList = os.listdir(sourceDir)
txtList = []
for file in fileList:
	# print(file)
	filename,extension = os.path. splitext(file)
	if extension == ".txt":
		txtList.append(file)
del fileList
gc.collect()
# print(txtList)
cnt = 0
for file in txtList:
	fr = open(os.path.join(sourceDir,file))
	img = cv.imread(os.path.splitext(file)[0]+".jpg")
	# cv.imshow('who',img)
	# cv.waitKey(200)
	# cv.destroyAllWindows()
	img_h,img_w,img_ch = img.shape
	img_np = np.array(img)
	for i,line in enumerate(fr):
		group = line.split(" ")
		c = group[0]
		#print(group[1],type(group[1]))
		w,h = int(float(group[3])*img_w),int(float(group[4])*img_h)
		x = int(float(group[1])*img_w - w/2)
		y = int(float(group[2])*img_h - h/2)
		#x,y,w,h = int(float(group[1])*img_w),int(float(group[2])*img_h),\
		if w*h < img_h*img_w*cutRatioControl:
			print("pass one part!")
			continue
		
		y_start,y_end = max(0,int(y-(h/4))),min(img_h,int(y+h+(h/4)))
		x_start,x_end = max(0,int(x-(w/5))),min(img_w,int(x+w+(w/5)))
		clip_img = img_np[y_start:y_end,x_start:x_end,:]

		# target_path = os.path.join(targetDir,os.path.split(file)[-1].split(".")[0]+"_"+str(i)+".jpg")
		target_path = targetDir+'/'+os.path.split(file)[-1].split(".")[0]+"_"+str(i)+".jpg"
		cnt+=1
		print(cnt,file)
		print(target_path)
		cv.imwrite(target_path,clip_img)
	fr.close()
print("ok!")