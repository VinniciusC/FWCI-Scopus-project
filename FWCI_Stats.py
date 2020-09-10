import PySimpleGUI as sg
from GUI_Selenium import config_selenium
from GUI_graphics_statistics import graphics_and_statistics_menu
import sys

def main():
    layout = [
        [sg.Button('Collect data')],
        [sg.Button('Generate graphics and statistics')]
    ]
    
    sg.theme('TealMono')
    window = sg.Window('Menu').layout(layout)

    while True:
        event,values = window.Read()
        if event == sg.WIN_CLOSED:
                sys.exit() 
        if event == 'Collect data':
            window.Hide()
            config_selenium()
            window.UnHide()
        if event == 'Generate graphics and statistics':
            window.Hide()
            graphics_and_statistics_menu()
            window.UnHide()

main()
