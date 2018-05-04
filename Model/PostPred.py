import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
import datetime
import pickle



def createGraphs(path,companyName):
    df = pd.read_csv(path+companyName +'/PredictedValues.csv')
    dayslength = int(len(df)/2)
    # print(dayslength)
    pred = df[-(dayslength+1) : ]
    real = df[:-dayslength]
    real.index = real['Date']
    # print(real['Close'])
    plt.plot(real['Close'],label='Current')
    # plt.show()
    
    # Index dates correctly
    real[-1:]['Date'].iloc[0]
    startday = datetime.datetime.strptime(real[-1:]['Date'].iloc[0],"%Y-%m-%d")
    arr = []
    for i in range(0,dayslength+1):
        for j in range(0,3):
            if (startday.isoweekday()==6 or startday.isoweekday()==7):
                startday =startday +  datetime.timedelta(days = 1)
            else:
                break
        arr.append([str(startday.date())])
        startday =startday +  datetime.timedelta(days = 1)
    datesFrame = (pd.DataFrame(arr,columns=['Date']))
    pred.index=datesFrame['Date']

    plt.plot(pred['Close'],label = 'Predicted')
    plt.ylabel('Close')
    plt.xlabel('Date')
    plt.title(companyName)
    plt.legend()
    plt.xticks([0,4,8,12,14])
    plt.savefig(path+companyName+'/Future.png')
    plt.close()


def processMeta():
    path = "./Data/"
    
    args = os.listdir(path)
    for i in args:
        df = pd.read_csv(path+i+"/PredictedValues.csv")
        dayslength = int(len(df)/2)

        #For percent change
        startClose = df['Close'][dayslength-1]
        finalClose = df['Close'][dayslength*2-1]
        percentChange = (finalClose-startClose)/startClose * 100
        print(startClose,finalClose,percentChange)
        meta = {}
        if (os.path.isfile(path+i+"/data.meta")):
            with open(path+i+'/data.meta','rb') as metaFile:
                meta = pickle.load(metaFile)
        meta['PerChange'] = percentChange
        if (os.path.isfile(path+i+"/data.meta")):
            with open(path+i+'/data.meta','wb') as metaFile:
                meta = pickle.dump(meta,metaFile)
        
        


def createPiChart():
    path = "./Data/"
    piDetails = {}
    args = os.listdir(path)
    for i in args:
        temp={}
        meta = {}
        if (os.path.isfile(path+i+"/data.meta")):
            with open(path+i+'/data.meta','rb') as metaFile:
                meta = pickle.load(metaFile)
        temp['PerChange'] = meta['PerChange']
        temp['Type'] = meta['Type']
        piDetails[meta['Name']] = temp
    indexcolours = ['red', 'cyan', 'brown', 'green', 'blue']
    
    label = []
    perChange = []
    Type = []
    uniqueTypes =[]
    for i in piDetails:
        if not (piDetails[i]['Type'] in uniqueTypes):
            uniqueTypes.append(piDetails[i]['Type'])
    perChangeType =[np.float(0)]*len(uniqueTypes)
    print(perChangeType)
    for j in uniqueTypes:
        for i in piDetails:
            if(piDetails[i]['Type']==j):
                perChangeType[uniqueTypes.index(j)] = perChangeType[uniqueTypes.index(j)] +  piDetails[i]['PerChange']
    total = np.sum(perChangeType)
    perChange = list(map(lambda x:x/total,perChangeType))
    plt.pie(perChange,labels=uniqueTypes,colors=indexcolours,autopct='%1.1f%%',startangle=90)
    plt.legend(uniqueTypes,loc = 'upper right')
    plt.savefig("./IndustryComparision.png")
    # plt.show()        

def giveColour(uniqueTypes,Type,colours):
    # print()
    return colours[uniqueTypes.index(Type)]




def main():
    for i in os.listdir("./Data/"):
        print(i)
        createGraphs("./Data/",i)

    processMeta()    
    

    createPiChart()    
    

if __name__ == '__main__':
    main()