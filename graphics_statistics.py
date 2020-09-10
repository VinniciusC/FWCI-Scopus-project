import pandas as pd
import statistics
import numpy
import matplotlib.pyplot as plt
from scipy import stats as s
import os


def interval(df,attr,count_interval):
    fwcis = df[attr].values.copy()
    fwcis.sort()
    count = 0
    dist = {}
    #Counting articles in the specified interval
    for i in numpy.arange(count_interval, max(fwcis)+count_interval,count_interval):
        max_range = round(float(i)-count_interval,1)
        dist[max_range] = 0
        while count < len(fwcis) and fwcis[count] <= i:
            dist[max_range] +=1
            count+=1
    return dist

def plot(title,count_interval,attr,file,normalize,highest):
    df = pd.read_csv(file)
    if normalize:
        df = divide_coauthors(file,attr)
        x = 'Normalized ' + attr
    else:
        x = attr
    if highest != 0:
        df = highest_att(file,highest,attr)
    y = 'Number of articles'
    print(df)
    dist = interval(df,attr,count_interval)
    values = dist.keys()
    articles_count = dist.values()
    #ploting and saving the bar graphic
    plt.bar(values,articles_count,width=count_interval,align='edge')
    plt.title(title)
    plt.ylabel(y)
    plt.xlabel(x)
    plt.show()

#Plot 2 datasets in a single graphic
def plot2(title, label1, label2,count_interval,attr,file1,file2,normalize,highest):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    if normalize:
        df1 = divide_coauthors(file1,attr)
        df2 = divide_coauthors(file2,attr)
        x = 'Normalized ' + attr
    else:
        x = attr
    if highest != 0:
        df1 = highest_att(file1,highest,attr)
        df2 = highest_att(file2,highest,attr)
    y = 'Number of articles'
    dist1 = interval(df1,attr,count_interval)
    dist2 = interval(df2,attr,count_interval)
    val1 = dist1.keys()
    count1 = dist1.values()
    val2 = dist2.keys()
    count2 = dist2.values()
    plt.bar(val1,count1, label = label1,width=count_interval, color = 'gray',align='edge')
    plt.title(title)
    plt.ylabel(y)
    plt.xlabel(x)
    plt.bar(val2,count2,zorder=2, label = label2,width=count_interval, alpha = 0.4, color = 'red',align='edge')
    plt.legend()
    plt.show()

def divide_coauthors(file,attr):
    df = pd.read_csv(file)
    divided_df = df.copy()
    for i in range(0,len(df)):
        divided_df.at[i,attr] = round(float(df.at[i,attr])/float(df.at[i,'authors_count']),2)
    return divided_df
    

def statistics_attribute(file,attr):
    df = pd.read_csv(file)
    print(attr + " sum:"+ str(sum(df[attr])))
    print(attr + " mean: " + str(round(statistics.mean(df[attr]),2)))
    print(attr + " mode: " + str(s.mode(df[attr]).mode))
    print(attr + " standard deviation:" + str(round(statistics.pstdev(df[attr]),2)))
    print(attr + " median:" + str(round(statistics.median(df[attr]),2)))
    pass

def highest_att(file,size,attr):
    df = pd.read_csv(file)
    df.sort_values(attr, inplace = True, ascending=False)
    df.reset_index(drop=True, inplace=True)
    df = df.head(size)
    return df

def scatter_coauthorsxfwci(file):
    df = pd.read_csv(file)
    plt.scatter(df['authors_count'], df['FWCI'],  c= 'green', alpha=0.5)
    plt.ylabel("FWCI")
    plt.xlabel('Number of authors')
    plt.show()
    pass


