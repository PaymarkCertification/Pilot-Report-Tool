import pandas as pd
import datetime
import glob
import os
import configparser
import io

class Pilot:

    today = datetime.datetime.now()

    def __init__(self):
        # self.week_ago = weekago
        pass

    @staticmethod
    def load_config(self):
        """Directory for RPT files. Set accordingly."""
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Pilot_Report_Config.ini'))
        path = config.get('path', 'rpt_file')
        return path

    def process_f(self):
        mylist = [f for f in glob.glob("*.txt")] # grabs all files in our RPT directory (load_config())
        list=[]
        try:
            for file in mylist:
                new = file[6:-4] # strips the chars to retrieve date from file name
                list.append(new.format(datetime.datetime.strptime(new, '%y%m%d')))
        except ValueError as e:
            print(f'{process_f.__name__}')
            exit()
        print('Presets:\n7 days ago = ', week_ago, '\n')
        dateObjects = []

        for date in list:
            convertedDateObject = datetime.datetime.strptime(date, '%y%m%d') # converts stripped file name into date object
            if convertedDateObject >= week_ago: 
                dateObjects.append(convertedDateObject.strftime('%y%m%d')) # adds the date of the file to list if they are within the last 7 days

        list_of_files = []
        for date in dateObjects:
            for file in mylist:
                if date in file:
                    list_of_files.append(file) # Returns the filename for processing if the dates are in the filename
        print('Processing the following files:\n', list_of_files, '\n')
        return list_of_files

    def concatentate_csvs(self, list_of):
        '''concatenates our CSV file(s) into a single dataframe'''
        li = []
        try:
            for filename in list_of:
                df = pd.read_csv(filename, index_col=None, header=0, sep='|')
                li.append(df)
            dframe = pd.concat(li, axis=0, ignore_index=True)
            return dframe
        except ValueError as e:
            print(f'{concatentate_csvs.__name__}: No objects to concatenate')
            exit()

    def main(self, frame):
        import re
        UniqueID = frame['Terminal'].unique() # Returns all the unique terminal ID(s) found in the dataframe
        print(f'{50 * "*"}\nTerminal ID\'s Found:\n', frame['Terminal'].unique(), f'\n{50 * "*"}\n\n')
        frame['Terminal'] = frame['Terminal'].astype(str) # casts col as str for user input matching.

        # TODO - Exception Handling of Input data 
        terminal_input = input('Enter Terminal ID [If multiple IDs separate by space]: ')

        user_list = terminal_input.split() # returns list from user input
        print('\nProcessing the following ID(s):\n\t', user_list,'\n')

        date_time = today.strftime("%m-%d-%Y %H%M%S")
        try:
            absFilePath = os.path.abspath(__file__)
            os.chdir(os.path.dirname(absFilePath)) #change save folder to root path of CWD
        except FileNotFoundError:
            print('Exception Occured:', FileNotFoundError)

        writer = (pd.ExcelWriter(f'Pilot_Report {date_time}.xlsx', engine='xlsxwriter'))

        for userID in user_list:
            frame.loc[frame['Terminal'] == userID]\
            .to_excel(writer, index=False, sheet_name=userID) # set sheet name and writes sheet data with terminal ID from dataframe
            for column in frame:
                column_width = max(frame[column].astype(str).map(len).max(), len(column))
                col_idx = frame.columns.get_loc(column)
                writer.sheets[str(userID)].set_column(col_idx, col_idx, column_width) # sets the width of the col
        
