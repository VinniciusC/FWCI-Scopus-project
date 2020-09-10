import PySimpleGUI as sg
from GUI_Selenium import config_selenium
import sys
import graphics_statistics as gs
import os

def plot1():
    config = [
        [sg.Text('CSV Dataset'), sg.In(key='file'), sg.FileBrowse()],
        [sg.Text('Count interval'), sg.Input(key='count')],
        [sg.Text('Title'), sg.Input(key='title')],
        [sg.Text('Attribute'),sg.Combo(['FWCI', 'authors_count', 'Prominence percentile'])],
        [sg.Checkbox('Divide the attribute by number of authors', default=False)],
        [sg.Text('Top highest attribute (0 to all)'), sg.Input(key='highest')],
        [sg.Submit('Next'), sg.Button('Cancel')]
    ]

    window = sg.Window('Plot one dataset').Layout(config)

    while True:
        event,values = window.Read()
        
        if event == sg.WIN_CLOSED:
            sys.exit() 
        if event == 'Cancel':
            window.close()
            return
        if event == 'Next': 
            if not os.path.exists(values['file']):
                sg.popup('Please fill a valid file')
                continue
            values['count'] = values['count'].replace(',','.',1)
            if not values['count'].replace('.','',1).isdigit():
                sg.popup('Please fill a valid count interval')
                continue
            if values['title'] is '':
                sg.popup('Please fill the title')
                continue
            if values[0] is '':
                sg.popup('Please choose an attribute')
                continue
            if not values['highest'].isdigit():
                sg.popup('Please fill Highest articles by attribute (0 to all)')
                continue
            gs.plot(values['title'],float(values['count']),values[0],values['Browse'],values[1],int(values['highest']))
            
def plot2():
    config = [
        [sg.Text('CSV Dataset 1'),sg.In(key='file1'), sg.FileBrowse()],
        [sg.Text('CSV Dataset 2'),sg.In(key='file2'), sg.FileBrowse()],
        [sg.Text('Count interval'), sg.Input(key='count')],
        [sg.Text('Title'), sg.Input(key='title')],
        [sg.Text('Label dataset 1'), sg.Input(key='label1')],
        [sg.Text('Label dataset 2'), sg.Input(key='label2')],
        [sg.Text('Attribute'),sg.Combo(['FWCI', 'authors_count', 'Prominence percentile'])],
        [sg.Checkbox('Divide the attribute by number of authors', default=False)],
        [sg.Text('Top highest attribute (0 to all)'), sg.Input(key='highest')],
        [sg.Submit('Next'), sg.Button('Cancel')]
    ]

    window = sg.Window('Plot two datasets').Layout(config)

    while True:
        event,values = window.Read()
        if event == sg.WIN_CLOSED:
            sys.exit() 
        if event == 'Cancel':
            window.close()
            return
        if event == 'Next': 
            if not (os.path.exists(values['file1']) and os.path.exists(values['file2'])):
                sg.popup('Please fill a valid file')
                continue
            values['count'] = values['count'].replace(',','.',1)
            if not values['count'].replace('.','',1).isdigit():
                sg.popup('Please fill a valid count interval')
                continue
            if values['title'] is '':
                sg.popup('Please fill the title')
                continue
            if values[0] is '':
                sg.popup('Please choose an attribute')
                continue
            if not values['highest'].isdigit():
                sg.popup('Please fill Top highest attribute (0 to all)')
                continue
            gs.plot2(values['title'], values['label1'], values['label2'],float(values['count']),
            values[0],values['file1'],values['file2'],values[1],int(values['highest']))

def astats():
    config = [
        [sg.Text('CSV Dataset'), sg.In(key='file'), sg.FileBrowse()],
        [sg.Text('Attribute'),sg.Combo(['FWCI', 'authors_count', 'Prominence percentile'])],
        [sg.Output(size=(88, 20))],
        [sg.Submit('Next'), sg.Button('Cancel')],
    ]

    window = sg.Window('Attribute statistics').Layout(config)

    while True:
        event,values = window.Read()
        if event == sg.WIN_CLOSED:
            sys.exit() 
        if event == 'Cancel':
            window.close()
            return
        if event == 'Next': 
            if not (os.path.exists(values['file'])):
                sg.popup('Please fill a valid file')
                continue
            if values[0] is '':
                sg.popup('Please choose an attribute')
                continue
            gs.statistics_attribute(values['file'],values[0])
            
def scatter():
    config = [
        [sg.Text('CSV Dataset'), sg.In(key='file'), sg.FileBrowse()],
        [sg.Submit('Next'), sg.Button('Cancel')],
    ]

    window = sg.Window('Scatter plot').Layout(config)

    while True:
        event,values = window.Read()
        if event == sg.WIN_CLOSED:
            sys.exit() 
        if event == 'Cancel':
            window.close()
            return
        if event == 'Next': 
            if not (os.path.exists(values['file'])):
                sg.popup('Please fill a valid file')
                continue
            gs.scatter_coauthorsxfwci(values['file'])

def graphics_and_statistics_menu():
    layout = [
        [sg.Button('Plot one dataset')],
        [sg.Button('Plot two datasets')],
        [sg.Button('Attribute statistics')],
        [sg.Button('Scatter Authors X FWCI')],
        [sg.Button('Cancel')]
    ]

    window = sg.Window('Menu').layout(layout)

    while True:
        event,values = window.Read()
        if event == sg.WIN_CLOSED:
                sys.exit() 
        if event == 'Cancel':
            window.Close()
            return
        if event == 'Plot one dataset':
            window.Hide()
            plot1()
            window.UnHide()
        if event == 'Plot two datasets':
            window.Hide()
            plot2()
            window.UnHide()
        if event == 'Attribute statistics':
            window.Hide()
            astats()
            window.UnHide()
        if event == 'Scatter Authors X FWCI':
            window.Hide()
            scatter()
            window.UnHide()