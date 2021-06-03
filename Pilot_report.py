import pandas as pd
import datetime
import glob
import os
import configparser
import io

print("""  _____ _ _       _     _____                       _     _______          _ 
 |  __ (_) |     | |   |  __ \                     | |   |__   __|        | |
 | |__) || | ___ | |_  | |__) |___ _ __   ___  _ __| |_     | | ___   ___ | |
 |  ___/ | |/ _ \| __| |  _  // _ \ '_ \ / _ \| '__| __|    | |/ _ \ / _ \| |
 | |   | | | (_) | |_  | | \ \  __/ |_) | (_) | |  | |_     | | (_) | (_) | |
 |_|   |_|_|\___/ \__| |_|  \_\___| .__/ \___/|_|   \__|    |_|\___/ \___/|_|
                                  | |                                        
                                  |_|                                        \n""")
def load_config():
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Pilot_Report_Config.ini'))
    path = config.get('path', 'rpt_file')
    return path



def exporter():
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()
    data = [['xlsx']]


# pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
try:
    os.chdir(load_config())
except FileNotFoundError:
    print(f'The system cannot find the file specified in {load_config.__name__}. '
          f'Please check Pilot_Report_Config.ini is configured correctly.'
          f'\nCurrent Working Dir: {load_config()}')
    os.system('pause')
    exit()


mylist = [f for f in glob.glob("*.txt")]
list=[]
for file in mylist:
    new = file[6:-4]
    list.append(new.format(datetime.datetime.strptime(new, '%y%m%d')))

today = datetime.datetime.now()
week_ago = today - datetime.timedelta(days=7)
print('Presets:\n7 days ago = ', week_ago, '\n')
dateObjects = []
for date in list:
    convertedDateObject = datetime.datetime.strptime(date, '%y%m%d')
    if convertedDateObject >= week_ago:
        dateObjects.append(convertedDateObject.strftime('%y%m%d'))

list_of_files = []
for date in dateObjects:
    for file in mylist:
        if date in file:
            list_of_files.append(file)
print('Processing the following files:\n', list_of_files, '\n')


def contentate_csvs(list_of):
    li = []
    for filename in list_of:
        df = pd.read_csv(filename, index_col=None, header=0, sep='|')
        li.append(df)
    dframe = pd.concat(li, axis=0, ignore_index=True)
    return dframe


def main(frame):
    import re
    UniqueID = frame['Terminal'].unique()
    print(f'{50 * "*"}\nTerminal ID\'s Found:\n', frame['Terminal'].unique(), f'\n{50 * "*"}\n\n')
    # pattern = r'^[a-zA-Z]+'
    frame['Terminal'] = frame['Terminal'].astype(str)
    # soft = frame['Card Number'].apply(lambda x: re.findall(pattern, x))
    # df = frame.drop_duplicates(subset=['Terminal'])
    # print(frame['Terminal'].dtypes)
    terminal_input = input('Enter Terminal ID [If multiple IDs separate by space]: ')

    user_list = terminal_input.split()
    print('\nProcessing the following ID(s):\n\t', user_list,'\n')
    # for i in range(len(user_list)):
    #     # convert each item to int type
    #     user_list[i] = int(user_list[i])
    # terminal = df.merge(df, soft, on='Terminal', how='right')

    # print(df[['Terminal'] & df['Card Number'].apply(lambda x: re.findall(pattern, x))])
    date_time = today.strftime("%m-%d-%Y %H%M%S")
    try:
        absFilePath = os.path.abspath(__file__)
        os.chdir(os.path.dirname(absFilePath))
    except FileNotFoundError:
        print('Exception Occured:', FileNotFoundError)

    writer = (pd.ExcelWriter(f'Pilot_Report {date_time}.xlsx', engine='xlsxwriter'))

    for userID in user_list:

        frame.loc[frame['Terminal'] == userID]\
           .to_excel(writer, index=False, sheet_name=userID)
        for column in frame:
            column_width = max(frame[column].astype(str).map(len).max(), len(column))
            col_idx = frame.columns.get_loc(column)
            writer.sheets[str(userID)].set_column(col_idx, col_idx, column_width)
    saver = input("Save file? (Y/N)")
    if saver.lower() == 'y':
        writer.save()
        print('excel saved')
    else:
        print('Fine. Not Saving')
        os.system('pause')


if __name__ == '__main__':
    main(contentate_csvs(list_of_files))
