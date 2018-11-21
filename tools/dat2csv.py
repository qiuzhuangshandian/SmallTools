#.dat文件中数据内容重新排，存入.csv文件中
import csv
numBatch = 10
for i in range(1,numBatch+1):
    with open("batch"+str(i)+".dat","r") as fr:
        fw = open("batch"+str(i)+".csv","w",newline="")
        csvWriter = csv.writer(fw,dialect="excel")

        for line in fr:
            lineContent = []
            groups = line.strip().split(" ")
            lineContent.append(groups[0]) #label
            for feature in groups[1:]:
                index,v = feature.split(":")
                lineContent.append(v)   #feature
            csvWriter.writerow(lineContent)
        fw.close()
print("convert ok!")