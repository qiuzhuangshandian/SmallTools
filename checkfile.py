file = "total_word_feature_extractor_zh.dat"
f = open(file,'rb')
cnt = 0
for line in f:
    if cnt > 15:
        break
    print(line.decode('gbk'))
    cnt +=1