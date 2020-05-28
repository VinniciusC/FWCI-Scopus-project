import pandas as pd
import statistics
import numpy
import matplotlib.pyplot as plt
from scipy import stats as s
import os

plt.rcParams['figure.figsize'] = (11,7)
plt.rcParams['xtick.labelsize'] = 16
plt.rcParams['ytick.labelsize'] = 16
plt.rcParams['axes.labelsize'] = 18
plt.rcParams['axes.titlesize'] = 16

count_interval =

def interval(df,attr):
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

def plot(df, title, x, y,attr):
    dist = interval(df,attr)
    values = dist.keys()
    articles_count = dist.values()
    #ploting and saving the bar graphic
    plt.bar(values,articles_count,width=count_interval,align='edge')
    plt.title(title)
    plt.ylabel(y)
    plt.xlabel(x)
    if not os.path.exists(file):
                os.makedirs(file)
    plt.savefig(file + "/" + title + ".png", format='png')
    plt.show()

#Plot 2 datasets in a single graphic
def plot2(df1, df2, title, legend1, legend2, x, y, attr):
    dist1 = interval(df1,attr)
    dist2 = interval(df2,attr)
    val1 = dist1.keys()
    count1 = dist1.values()
    val2 = dist2.keys()
    count2 = dist2.values()
    plt.bar(val1,count1, label = legend1,width=count_interval, color = 'gray',align='edge')
    plt.title(title)
    plt.ylabel(y)
    plt.xlabel(x)
    plt.bar(val2,count2,zorder=2, label = legend2,width=count_interval, alpha = 0.6, color = 'red',align='edge')
    plt.legend()
    if not os.path.exists(title):
                os.makedirs(title)
    plt.savefig(title + "/" + title + ".png", format='png')
    plt.show()

def divide_coauthors(df,attr):
    divided_df = df.copy()
    for i in range(0,len(df)):
        divided_df.at[i,attr] = round(float(df.at[i,attr])/float(df.at[i,'authors_count']),2)
    return divided_df

def statistics_coauthors(df):
    print("Co-author mean per article: " + str(round(statistics.mean(df['authors_count']),2)))
    print("Co-author mode per article: " + str(s.mode(df['authors_count'])))
    print("Co-author median per article: " + str(statistics.median(df['authors_count'])))

def statistics_attribute(df, attr):
    print(attr + " sum:"+ str(sum(df[attr])))
    print(attr + " mean: " + str(round(statistics.mean(df[attr]),2)))
    print(attr + " mode: " + str(s.mode(df[attr])))
    print(attr + " standard deviation:" + str(round(statistics.pstdev(df[attr]),2)))
    print(attr + " median:" + str(round(statistics.median(df[attr]),2)))

def twenty_highest_att(df,attr):
    df.sort_values(attr, inplace = True, ascending=False)
    df.reset_index(drop=True, inplace=True)
    df = df.head(20)
    return df

def scatter_coauthorsxfwci(df):
    plt.scatter(df['authors_count'], df['FWCI'],  c= 'green', alpha=0.5)
    plt.ylabel("FWCI")
    plt.xlabel('Number of authors')
    if not os.path.exists(file):
        os.makedirs(file)
    plt.savefig(file+'/scatter co-authors X FWCI.png', format='png')
    plt.show()

file = ''
file2 = ''
df = pd.read_csv(file+'.csv')
if file2 != '':
    df2 = pd.read_csv(file2+'.csv')
