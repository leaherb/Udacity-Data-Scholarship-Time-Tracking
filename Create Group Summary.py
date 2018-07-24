
# coding: utf-8

# In[ ]:


import dateutil
import numpy
import pandas as pd
from tkinter import filedialog
import csv
from pprint import pprint


# In[ ]:


def csv_to_df(csv_filename):
    '''Return a dataframe with contents from CSV file.'''
    
    df = pd.read_csv(csv_filename)

    # Convert Date column from string to datetime 
    df['Date']=pd.to_datetime(df['Date'])

    # Index dataframe on Date field, making it easier to do time-based analysis
    df.set_index(df['Date'], inplace=True)
    
    return df


# In[ ]:


def calc_c_versus_p_hours(list):
    '''Return two numbers: total Class Hours and total Participation (non-Class) Hours.'''
    
    result = []
    total_c_hours = 0
    total_p_hours = 0
    for item in list:
        # note: 'type of participation' is a column heading in the time sheet that is manually 
        # updated prior to loading via this python script. 
        # Make standardizing column headings part of the cleaning function.
        time_type, hours = item['type of participation'], item['Hours']
        if time_type == 'C':
            total_c_hours += hours
        else:
            total_p_hours += hours
            
    return [round(total_c_hours,2), round(total_p_hours,2)]


# In[ ]:


def analyze_df(df):
    '''Return list of calculations based on dataframe columns.'''
    
    # Code is rough for now, but works. 
    # Rework so I don't have to manually update timesheets with Hours. Just use Duration.
    
    # Group by weeks, sum the hours
    hours=df['Hours'].resample('W').sum()
 
    # Count number of unique weeks
    week_count=df['Hours'].resample('W').sum().count()
    
    # Calculate basic stats
    mean_hours=round(numpy.mean(hours),2)
    median_hours=round(numpy.median(hours),2)
    STD_hours=round(numpy.std(hours,ddof=1),2)
    
    # Convert df to list for easier calculating. Recode when I know more python. 
    df_list = df.to_dict('records')
    
    # Get Class vs Participation totals
    subtotals = calc_c_versus_p_hours(df_list)

    result_list = [week_count, mean_hours, median_hours, STD_hours, subtotals[0], subtotals[1], round((subtotals[0]/week_count),2), round((subtotals[1]/week_count),2)]
    
    return result_list


# In[ ]:


def print_report(list):
    
    for i in range(1,len(list)):
        for j in range(len(list[0])):
            print('{}:\t{}'.format(list[0][j], list[i][j]))
        print('\n')


# In[ ]:


# ----------------------------------------------------------------------
# Main
if __name__ == '__main__':
    '''Summarize a set of time sheets, output to a CSV file named "timesheet_summary.csv".'''
    
    # Possible Improvements: 
    # * Use upload survey spreadsheet to grab filenames and incorporate answers from upload survey 
    #   (need a purpose for the survey answers first!), 
    #   -- or --
    #   Instead of prompting for csv files, prompt for a directory then grab all CSV files in it.

    # Initialize 
    consolidated_list = [['Participant','Week Count','Mean Hours','Median Hours','STD Hours',                          'Total C Hours','Total P Hours','Avg C Hours','Avg P Hours']]
    filename = ' '
    list_index = 0

    # Prompt for CSV files until cancel, processing and adding each CSV's data to consolidated list.
    while filename:
        filename = filedialog.askopenfilename(title='Select FitBit CSV', filetypes=[("CSV","*.csv"),("All files","*.*")])
        if filename:
            print('Loading {}\n'.format(filename))
            list_index += 1
            df = csv_to_df(filename)  
            csv_list = [list_index] + analyze_df(df)
            consolidated_list.append(csv_list)
            
    summary_filename = 'timesheet_summary.csv'
    with open(summary_filename, "w") as f:
        writer = csv.writer(f)
        writer.writerows(consolidated_list)
        
    print('...\nSummary data written to: {}\nProcess complete.'.format(summary_filename))


# In[ ]:


print_report(consolidated_list)

