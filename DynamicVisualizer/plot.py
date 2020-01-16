import json
import numpy as np
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
from pprint import pprint
import traceback

dataset = []
with open('eval_result-10-1-2020.json', 'r') as input:
    dataset = json.load(input)

result = []


for data in dataset:
    #print(data[0]['Accuracy'])
    result.append([data[0]['Accuracy'], data])

x = sorted(dataset, key = lambda x: (x[0]['Accuracy']))



s = sorted(result, key = lambda x: (x[0]))

#print(s[len(s)-11:len(s)-1])

bestresult = x[len(x)-5:len(x)-1]

topresult = x[-1]
#conf = topresult[1][0]['ConfusionMatrix']
#print(conf)

#pprint(topresult[1][0])
#pprint(s[0][1])


topresultsconfig = bestresult[-1]
worstresultsconfig = x[0:6]

#x = [i[1][1]for i in topresultsconfig]
bestworstconfigs = []
for i in bestresult:
    bestworstconfigs.append(i[1])

for i in worstresultsconfig:
    bestworstconfigs.append(i[1])

#pprint(bestworstconfigs)
#pprint(x)
#pprint([worstresultsconfig])

with open('bestandworstconfigs.json','w') as output:
    json.dump(bestworstconfigs, output, indent= 4)