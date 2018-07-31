
# coding: utf-8

# In[12]:


import pandas as pd
from tkinter import filedialog

# ----------------------------------------------------------------------
# Main
# Caveat:  assumes all CSVs are in 'current' directory.

if __name__ == '__main__':
    '''
    Consolidate  timesheets listed in a CSV file into a single file 'group_timesheet.csv'.
    Add 'Timesheet ID' column to differentiate individual timesheet data sets.
    '''
    
    # Prompt for CSV  containing the list of timesheets,  write its contents to a dataframe.
    index_df = pd.read_csv(filedialog.askopenfilename(title='Select FitBit CSV', filetypes=[("CSV","*.csv"),("All files","*.*")]))
    
    # Add column, FileID = basename of the CSV filename
    index_df['FileID'] = index_df['Csv-filefile'].str.split('.', 1).str[0]
    
    index_df = index_df.set_index('FileID')

    # Loop through each timesheet listed in index_df, adding its data set to a consolidated df.
    # Do not process unless source is 'My Own Data' (e.g., not Sample Data)
    # Better way of doing this: just append directly to the group file, rather than to df first.
    
    group_df = pd.DataFrame()
    
    for index, row in index_df[index_df['Data-source'] == 'My Own Data'].iterrows():
        filename = row['Csv-filefile']

        if filename:
            df = pd.read_csv(filename)
            df['Timesheet ID'] = index
            group_df = pd.concat([group_df, df])
    
    group_df = group_df.set_index('Timesheet ID')
            
    group_df.to_csv('group_timesheet.csv')
        

