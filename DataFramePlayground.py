import PySimpleGUI as sg
import pilotgui as pg
import os
import configparser
import logging
import datetime
import glob
import subprocess
import sys
import pandas as pd
import numpy as np

__version__ = '0.0.1'
# ----- Logging Method ----- #
class Handler(logging.StreamHandler):

    def __init__(self):
        logging.StreamHandler.__init__(self)

    def emit(self, record):
        global buffer
        record = f'{record.name}, [{record.levelname}], {record.message}'
        buffer = f'{buffer}\n{record}'.strip()
        window['-output-'].update(value=buffer)

    @staticmethod
    def load_logging(loggingLevel: int = logging.INFO) -> logging:
        return logging.basicConfig(
            level=loggingLevel, 
            format='%(asctime)s %(levelname)s:%(message)s', 
            handlers=[
                logging.StreamHandler()
            ]
        )

# ----- exception handling func ----- #
# TODO
# def error_handle(errors=(Exception,), default_value=''):
#     """
#     @param func: callable function wrapper
#     Helper function for exception handling of generic errors.
#     """
#     def decor(func):

#         def wrapper(*args, **kwargs):
#             try:
#                 return func(*args, **kwargs)
#             except:
#                 print(f'unexpected error: {func.__name__} suffered an exception: {sys.exc_info()[0]}') 
#                 logging.info(f'{func.__name__, sys.exc_info()[0]}')
#             return default_value
#         return wrapper
#     return decor
            

# ----- GUI Methods ---- #
def load_config():
        """Directory for RPT files. Set accordingly."""
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Pilot_Report_Config.ini'))
        path = config.get('path', 'rpt_file')
        return path

def lastweek(string: int = 1):
    """
    @param string: Toggles return data
    Returns last 7 days from today either as string or date"""
    today = datetime.datetime.now()
    week_ago = today - datetime.timedelta(days=7)
    if string:
        return week_ago.strftime('%d/%m/%Y') # returns string type
    else:
        return week_ago # returns date object


def last_days():
    """returns date object from widget"""
    try:
        date = values['datePick']
        logging.info(f'date returned from widget: {date}')
        selected_date = datetime.datetime.strptime(date,'%d/%m/%Y')
        week = selected_date - datetime.timedelta(days=7)    
    except ValueError as ve:
        print(f'unexpected error: {ve, sys.exc_info()[0]}')
        logging.info(f'Func {last_days.__name__} suffered exception\n {ve, sys.exc_info()[0]}')
    return week

def process_rpt_files():

    def concatentate_csvs(list_of):
        li = []
        logging.info(' Attempting to concatenate')
        try:
            for filename in list_of:
                df = pd.read_csv(filename, index_col=None, header=0, sep='|')
                li.append(df)
            dframe = pd.concat(li, axis=0, ignore_index=True)
            dframe1 = dframe.replace(np.nan, '', regex=True)
            print(dframe1[dframe1['Card Number']].str.match(pat = '^\w+'))
                # print(dframe.groupby(['Terminal','Card Number'], as_index=False).last())
        # except ValueError as e:
        #     print(f'{concatentate_csvs.__name__}: No objects to concatenate')
        except:
            logging.info(f' {sys.exc_info()[0], sys.exc_info()[1]}')

    try:
        os.chdir(load_config())
        print(f"RPT path set to {load_config()}")
            
    except FileNotFoundError:
        print(f'The system cannot find the file specified in {load_config.__name__}. '
        f'\nPlease check Pilot_Report_Config.ini is configured correctly.'
        f'\nCurrent Working Dir: {load_config()}')
        logging.info(' Could not load file')

    print(f'Harvesting data from {values["datePick"]}')
    mylist = [f for f in glob.glob("*.txt")]
    list=[]
    try:
        for file in mylist:
            new = file[6:-4] # strips the chars to retrieve date from file name
            list.append(new.format(datetime.datetime.strptime(new, '%y%m%d')))
        
    except ValueError as e:
        print(f'{process_rpt_files.__name__}: Value Error. Empty list.')


    dateObjects = []
    for date in list:
        convertedDateObject = datetime.datetime.strptime(date, '%y%m%d') # converts stripped file name into date object
        logging.info(f' Convert str "{date}" to date object "{convertedDateObject}"')
        
        if convertedDateObject >= last_days(): #lastweek(string=0) 
            dateObjects.append(convertedDateObject.strftime('%y%m%d')) # adds the date of the file to list if they are within the last 7 days
            logging.info(f' {convertedDateObject} appended to list')

    list_of_files = []
    for date in dateObjects:
        for fileItem in mylist:
            if date in fileItem:
                list_of_files.append(fileItem) # Returns the filename for processing if the dates are in the filename
    if list_of_files != '':
        print('Processing the following files:\n', list_of_files, '\n')
        concatentate_csvs(list_of_files)   
    else:
        print("No files found for selected date range. Select another date.")
        


# ----- Column Definition ----- #
colx = [
    [sg.Text("Date:"), sg.Input(lastweek(), key='datePick', size=(20, 1)),sg.CalendarButton("Select Date", key='date', disabled=False, format='%d/%m/%Y')],
    # [sg.CalendarButton("Select Start Date", key='date', disabled=False, format='%d/%m/%Y')],
    [sg.Radio('Translate Data', group_id='RADIO1', default=True), sg.Radio('Raw Data', group_id='RADIO1', default=False)],
    [sg.Button('Harvest'), sg.Button('Collect'), sg.Button('Clear Log'), sg.Button('path')]
]

coly = [
    [sg.Table(key='-Table-', headings=['Terminal ID', 'Software Version'],
     values=[['TID placeholder', 'TSV placeholder']], col_widths=500,
     num_rows=7)]
]

colz = [sg.Output(size=(81, 9), key='-output-')]

# ----- Set Theme ----- #
sg.theme('Purple')

# ----- Layout Management ----- #
layout = [
    [sg.Column(colx), sg.Column(coly)],
    [sg.Output(size=(81, 9), key='-output-')]
]
window = sg.Window('Pilot Report', layout)


if __name__=='__main__':
    Handler.load_logging()
    
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == 'Harvest':
            process_rpt_files()
            logging.info('Harvest (Event) Selected')
        elif event == 'Clear Log':
            window.FindElement('-output-').Update('')
        elif event == 'path':
            print(load_config())
        elif event == 'Collect':
            pass