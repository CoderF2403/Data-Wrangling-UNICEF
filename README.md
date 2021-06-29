# Data Wrangling UNICEF


## OVERVIEW 
   This script is used to intake the male survey data from UNICEF and save it to a simple csv file
  (or a MySQL Database if wished) after it has been checked for duplicates and missing data and after the headers 
  have been properly matched with the data.
  
  It expects there to be a 'mn.csv' file with the data and the 'mn_headers_updated.csv' file in a sub-folder called 
  'unicef' within a data folder in this directory. It also expects there to be a MySql database called datawrangling.
  Finally, it expects to utilize the dataset library (http://dataset.readthedocs.org/en/latest/).
  
  If the script runs without finding any errors, it will save the cleaned data to the 'unicef_survey' folder in the MySQL 
  or if wished can be saved into 'Data Files'.

## Pre-Requesits

- Installed Python Version > 2.0
- Installed Python Library (dataset, csv).

## TODOs

In `script.py` you have to add all these.

`data_path = 'NAME OF DIRECTORY WHERE THE mn.csv IS SAVED'`

`header_path = 'NAME OF DIRECTORY WHERE mn_headers_updated.csv IS SAVED'`

`url = 'CHECK THE DATASET LIBRARY FOR MySQL URL FOR THIS SCRIPT'`

`file_path = 'PATH FOR ALL THE RESPONSES TO BE SAVED IN DIRECTORY'`

Then you can execute this script by running `python scripty.py`
