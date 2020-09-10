import PySimpleGUI as sg 
import sys
from datetime import date
import subprocess
import platform
import threading
from Selenium_code import run_selenium 
from json import (load as jsonload, dump as jsondump)
from os import path
          
 #COLOCAR VERIFICACAO NO CAMPO DE ARQUIVO DO WEBDRIVER         
def load_path(SETTINGS_FILE):
    try:
        with open(SETTINGS_FILE, 'r') as f:
            settings = jsonload(f)
    except:
        settings = {'path': None}
        with open(SETTINGS_FILE, 'w') as f:
            jsondump(settings, f)
    return settings

def save_path(SETTINGS_FILE,settings,path):
    settings['path'] = path
    with open(SETTINGS_FILE, 'w') as f:
        jsondump(settings, f) 

def config_selenium():
    window_1 = [
        [sg.Text('Scopus ID'), sg.Input(key='id')],
        [sg.Text('Sort by')],
        [sg.Radio('All articles','sort',key=1),sg.Radio('Date(Newest)','sort',key=2),
        sg.Radio('Date(Oldest)','sort',key=3),sg.Radio('Cited by(Highest)','sort',key=4),
        sg.Radio('Cited by(Lowest)','sort',key=5)],
        [sg.Text('Chrome WebDriver'), sg.Input(key='webdriver_path'), sg.FileBrowse()],
        [sg.Checkbox('Save Chrome WebDriver path', default=False)],
        [sg.Submit('Next'), sg.Button('Cancel')]
    ]

    window_2 = [
        [sg.Text('Minimum year (0 to ignore)'), sg.Input(key='min')],
        [sg.Text('Maximum year (0 to ignore)'), sg.Input(key='max')],
        [sg.Text('Number of articles (0 to all)'), sg.Input(key='size')],
        [sg.Submit('Next'), sg.Button('Cancel')]
    ]

    terminal_window = [      
        [sg.Text('Please click in RUN', size=(40, 1))],      
        [sg.Output(size=(88, 20))],      
        [sg.Button('RUN'),sg.Button('EXIT')]      
    ] 

    #Settings File contains chrome webdriver path if defined by the user
    SETTINGS_FILE = path.join(path.dirname(__file__), r'chromepath.cfg')
    settings = load_path(SETTINGS_FILE)
    window = None

    #Search configuration window
    while True:

        #Creating the window and loading the chrome webdriver path
        if window == None:
            window = sg.Window("Data collection settings",window_1,finalize=True)
            window['webdriver_path'].update(value=settings['path'])

        event, values1 = window.Read()

        if event == sg.WIN_CLOSED:
            sys.exit() 
        if event == 'Next':
            if (values1['id'] is '') or not (values1[1] or values1[2] or values1[3] or values1[4] or values1[5]) or not path.exists(values1['webdriver_path']):
                sg.popup('Please fill Scopus ID, sort and a valid chrome web driver path')
            else:
                if(values1[0]):
                    save_path(SETTINGS_FILE,settings,values1['webdriver_path'])
                break
        if event == 'Cancel':
            window.Close()
            return
    window.Close()

    window = sg.Window("Data collection settings").layout(window_2)

    #Window for all sorts except "All articles"
    while not values1[1]:
        event, values2 = window.Read()

        if event == sg.WIN_CLOSED or event == 'Cancel':
            sys.exit()
        if event == 'Next':
            if values2['min'].isdigit() and values2['max'].isdigit():
                if(not ((1950<=int(values2['min'])<=date.today().year or int(values2['min']) == 0)  and
                    (1950<=int(values2['max'])<=date.today().year or int(values2['max']) == 0))):
                    sg.popup('Please fill with a valid year (>1950 and <2020)')
                    continue
            else :
                sg.popup('Please fill with a valid year (>1950 and <2020)')
                continue
            if not values2['size'].isdigit():
                sg.popup('Please fill with a valid size number')
                continue
            
            break
    window.Close()   
            
    #defining the arguments to run the script
    if values1[1]:
        command = values1['id'] +' '+ '1' +' '+ '0' +' '+ '0' +' '+ '0' +' '+ values1['webdriver_path']
        command_split = command.split()
        
    else:
        if values1[2]:
            sorted = 2
        if values1[3]:
            sorted = 3
        if values1[4]:
            sorted = 4
        command = values1['id'] +' '+ str(sorted) +' '+ values2['min'] +' '+ values2['max'] +' '+ values2['size'] +' '+ values1['webdriver_path']
        command_split = command.split()
        

    window = sg.Window('Script launcher', terminal_window)      
    
    #Script Launcher window 
    while True:      
        (event, value) = window.read()      
        if event == 'EXIT'  or event == sg.WIN_CLOSED:   
            window.Close()   
            break # exit button clicked      
        elif event == 'RUN':
            print('Running...')
            window.FindElement('RUN').Update(disabled=True)
            thread_id = threading.Thread(target=run_selenium, args=(command_split), daemon=True)
            thread_id.start()
            window.FindElement('RUN').Update(disabled=False)
            
