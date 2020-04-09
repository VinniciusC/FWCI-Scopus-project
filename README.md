# FWCI-Scopus-project

Repository containing the tools used in the article 

Optimized harvesting and usage of FWCI and TPP. Article age- and field-normalized tools to evaluate scientific impact\
Edgar D. Zanotto and Vinicius Carvalho\
Department of Materials Engineering - DEMa\
Federal University of São Carlos - UFSCar


## Requirements
* Python 3
* Selenium 
* Pandas
* Numpy
* Matplotlib
* Scipy
* Full acess at Scopus database


## Collecting the data
Selenium-code.py is the script responsible to collect the data at Scopus.

To get started, it is necessary define some settings filling the variables in the code.

 * scopus_ID\
      Author's ID that can be found in author's page at Scopus\
      Choosing the author number 123456789:
      ```
      scopus_id = '123456789'
      ```
  * ordered_by\
      Specifies the sort that the articles data will be collected\
      Each number represents a sort.\
      1 - All articles\
      2 - Date(Newest)\
      3 - Date(Oldest)\
      4 - Cited by(Highest)\
      5 - Cited by(Lowest)\
      Sorting the articles by the highest citation number:
      ```
      ordered_by = 3
      ```
  * Minimum and maximum years\
      To choose the minimum and maximum year of a publication\
      Fill with 0 to ignore\
      To collect articles published at least in 2000: 
      ```
      min_year = 2000  
      max_year = 0
      ```
   * Size\
      Number of articles to be collected.
      If you choose all articles in sorted_by, fill with 0 and the other options the maximum value is 200.
      To collect 50 articles: 
      ```
      size = 50
      ```
After filling all the variables, it is just necessary run the script:
```
python Selenium-code.py
```
The browser will open and run all the process automatically. \
At the end, the collected data will be written in a CSV file with the following columns and attributes:
| Article_name | FWCI | year | authors_count | Prominence percentile | Topics | Anchors |
|--------------|------|------|---------------|-----------------------|--------|---------|

The file will be saved in author's folder and the name defined by the previously filled variables\
scopus_id_sorted_by_size_min_year_max_year.csv\
After writting, a message of sucess will be shown.\
Observation: sometimes it is necessary to re-execute the code again because of random popups and attributes that were not loaded correctly by the website. We are working in a solution, feel free to contribute.

## Generating graphics and statistics
Using the script graphics-and-statistics.py we can generate graphics and statistics about the previouly collected data.
The graphic represents a count of articles in a specified interval of a chosen attribute. In the following case, the interval is 0.1 and the attribute is Normalized FWCI.
![1](https://user-images.githubusercontent.com/32166287/78833422-3bf95100-79c3-11ea-9730-ab497e3aac2d.png)

Before using the functions, it is necessary specify the csv path with the data. To this, use the variables file and file2, in case of a second dataset.
Example:
```
file = '/home/user/FWCI-Scopus-project/author1/123456_1_0_2000_0.csv'
```
Then, you need to define a interval according with your preferences or data scale. The variable is count_interval, localized in the first lines.\
Defining a 0.5 interval:
```
count_interval = 0.5
```
To use the functions, you need to edit the file calling them with the parameters.

* Graphic with one dataset\
      Function: plot\
      plot(df, title, y,attr)
  * df : The desired dataset. Use df for file and df2 for file2
  * title: The title that will be written on the top of the graphic and the name of the file.
  * y: Name of Y axis
  * attr: Choosen attribute to plot, that could be FWCI, authors_count and Prominence percentile\
  
      Example:
     ```
     plot(df,'Articles count X FWCI', 'Normalized FWCI','FWCI')
     ```
       The png plot will be saved in a folder named by the title inside the dataset csv folder.\
           ![1](https://user-images.githubusercontent.com/32166287/78833422-3bf95100-79c3-11ea-9730-ab497e3aac2d.png)\
 * Graphic with two dataset\
      Function: plot2\
      plot2(df1, df2, title, legend1, legend2, y, attr)
   * df1 : The desired dataset. Use df for file and df2 for file2
   * df2 : The desired dataset. Use df for file and df2 for file2
   * title: The title that will be written on the top of the graphic and the name of the file.
   * legend1: The legend describing the data at dataset 1
   * legend2: The legend describing the data at dataset 2
   * y: Name of Y axis
   * attr: Choosen attribute to plot, that could be FWCI, authors_count and Prominence percentile\
        Example:
        ```
         plot(df,df2,'20 newest and 20 oldest. Article count x FWCI','Oldest','Newest','FWCI value','FWCI')
        ```
        
       The png plot will be saved in a folder named by the title inside the code main folder.\
       ![2](https://user-images.githubusercontent.com/32166287/78835128-06099c00-79c6-11ea-837b-704d9f7675a3.png)
           
  * Dividing an attribute per co-authors number\
      Function: divide_coauthors\
      divide_coauthors(df,attr)
    * df : The desired dataset. Use df for file and df2 for file2
    * attr: Choosen attribute to divide, that could be FWCI and Prominence percentile\
    Example:
    ```
    new_dataset = divide_coauthors(df,'FWCI')
    ```
    This function is not inplace, returns a new dataset without change the original.
      
  * Co-author statistics\
      Function: statistics_coauthors\
      This function prints the mean, mode and median of co-authors number\
      statistics_coauthors(df)
    *  df : The desired dataset. Use df for file and df2 for file2
            
   * Attribute statistics\
      Function: statistics_attribute\
      This function prints the sum, mean, mode, median and standard deviation of co-authors number\
      statistics_attribute(df, attr):
     * df : The desired dataset. Use df for file and df2 for file2
     * attr: Choosen attribute to calculate the statistics, that could be FWCI and Prominence percentile\
            
   * Top 20 Highest of an attribute\
      Function: statistics_attribute\The png plot will be saved in file folder, being named as scatter co-authors X FWCI.png
      This function returns a dataset containing just the top 20 of a choosen attribute.\
      twenty_highest_att(df,attr):
     * df : The desired dataset. Use df for file and df2 for file2
     * attr: Choosen attribute to calculate the top 20, that could be FWCI, authors_count and Prominence percentile\
      Example:
      ```
      top_fwci = twenty_highest_att(df,'FWCI')
      ```
      This function is not inplace, returns a new dataset without change the original.\
      
   * Scatter graphic Co-authors count X FWCI\
       Function: scatter_coauthorsxfwci\
       This function plot a scatter graphic to compare the number of co-authors with the FWCI in each article.\
       scatter_coauthorsxfwci(df):
     * df : The desired dataset. Use df for file and df2 for file2
       
       The png plot will be saved in file folder, being named as scatter co-authors X FWCI.png\
       ![1 (1)](https://user-images.githubusercontent.com/32166287/78920771-4a4e7800-7a6a-11ea-898c-069988fa2a81.png)

       
