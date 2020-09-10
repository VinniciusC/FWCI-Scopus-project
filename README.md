# FWCI-Scopus-project

Repository containing the tools used in the article 

**Automated harvesting and statistics of FWCI and TPP. Article age- and field-normalized tools to evaluate scientific impact and momentum**\
Edgar D. Zanotto and Vinicius Carvalho\
Department of Materials Engineering – DEMa\
Center for Research, Technology and Education in Vitreous Materials\
Federal University of São Carlos – UFSCar\
Sao Carlos, SP, Brazil\
(dedz@ufscar.br)

## Executable for windows
* Windows:
<https://www.dropbox.com/s/7427jjxits5spe1/FWCI_Stats_Win.rar?dl=0>

## Requirements Windows
* Windows 7 32bits or higher
* Full access to the Scopus database
* Chrome WebDriver

## Requirements Linux
* selenium==3.141.0
* matplotlib==3.3.0
* numpy==1.19.1
* pandas==1.1.0
* PySimpleGUI==4.26.0
* scipy==1.5.2
* Full access to the Scopus database
* Chrome WebDriver

## Chrome WebDriver download
Before, check your Chrome Version acessing <chrome://settings/help> \
Then download the WebDriver according with your chrome version accessing <https://chromedriver.chromium.org/downloads>

## Executing the software
* Windows version\
      Run FWCI_Stats.exe
* Linux version\
      Run python Selenium-code.py 

## Collecting the data
Click *Collect data* in first menu and fill all the fields 

 * Scopus ID\
      Author's ID that can be found in author's page at Scopus
      
  * Sort by\
      Specifies the sort that the articles data will be collected
      
  * Chrome WebDriver \
      Click in browse and select the Chrome WebDriver previously downloaded.\
      It is possible to save the path selecting the item below. 
      
  Click Next.\
  If you choose a sort different from All articles, it will be necessary to fill the following items:
  
  * Minimum and maximum years\
      To choose the minimum and maximum year of a publication\
      Fill with 0 to ignore

   * Size\
      Number of articles to be collected.\
      Fill with 0 to collect all
 
 Click Next.\
 Click Run.
 

The browser will open and run all the process automatically. \
Do not close until *CSV written with sucess* message appear.\
Each article collected will be shown.\
In the end, the collected data will be written in a CSV file with the following columns and attributes:
| Article_name | FWCI | Year |Journal info | authors_count | Prominence percentile | Topics | Anchors |
|--------------|------|------|-------------|---------------|-----------------------|--------|---------|

The file will be saved in the author folder and the name defined by the previously filled variables\
sorted_by_size_min_year_max_year.csv\
Observation: sometimes it is necessary to re-execute the code again because of random popups and attributes that have not been loaded correctly by the website. We are working in a solution, feel free to contribute.

## Generating graphics and statistics
Selecting *Generate graphics and statistics* we can generate graphics and statistics about the previously collected data.
The graphic represents the number of articles in an interval which is defined by the user. In the following case, the interval is 0.1 and the attribute is Normalized FWCI.
![1](https://user-images.githubusercontent.com/32166287/78833422-3bf95100-79c3-11ea-9730-ab497e3aac2d.png)

* Plot one dataset
  * CSV Dataset : The desired dataset. You can choose clicking in browser.
  * Count interval: Define an interval according with your preferences or data scale.
  * Title: The title that will be written on the top of the graphic and the name of the file.
  * Attribute: Choosen attribute to plot, that could be FWCI, authors_count and Prominence percentile
  * Divide the attribute by number of authors: Select to divide the choosen atribute of each article by its number of authors.
  * Top highest attribute: If you are looking for the highests fill this field, if not, fill with 0. 
 
       To save in your device, click in the save button and choose a folder.\
       Result example: \
           ![1](https://user-images.githubusercontent.com/32166287/78833422-3bf95100-79c3-11ea-9730-ab497e3aac2d.png)\
           
 * Plot two datasets
   * CSV Dataset 1 and 2: The first and second desired dataset. You can choose clicking in browser.
   * Count interval: Define an interval according with your preferences or data scale.
   * Title: The title that will be written on the top of the graphic and the name of the file.
   * Label dataset 1 or 2: text to the graphic legend of each dataset
   * Attribute: Choosen attribute to plot, that could be FWCI, authors_count and Prominence percentile
   * Divide the attribute by number of authors: Select to divide the choosen atribute of each article by its number of authors.
   * Top highest attribute: If you are looking for the highests fill this field, if not, fill with 0. 
 
       To save in your device, click in the save button and choose a folder.\
       Result example: \
       ![2](https://user-images.githubusercontent.com/32166287/78835128-06099c00-79c6-11ea-837b-704d9f7675a3.png)
      
  * Attribute statistics\
      This function prints the sum, mean, mode,standard deviation and median of a choosen attribute\
     * CSV Dataset : The desired dataset.
     * Attribute: Choosen attribute to calculate the statistics, that could be FWCI, Prominence percentile or authors count\
            
      
   * Scatter Authors X FWCI\
       This function plot a scatter graphic to compare the number of authors with the FWCI in each article.\
     * CSV Dataset : The desired dataset.
       
       To save in your device, click in the save button and choose a folder.\
       Result example: \
       ![1 (1)](https://user-images.githubusercontent.com/32166287/78920771-4a4e7800-7a6a-11ea-898c-069988fa2a81.png)

       
