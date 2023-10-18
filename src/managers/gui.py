import PySimpleGUI as sg


def create_gui():
    layout = [
        [sg.Checkbox('Save', default=True, key='-SAVE-')],
        [sg.Checkbox('Print', default=False, key='-PRINT-')],
        [sg.Checkbox('Email', default=False, key='-EMAIL-')],
        [sg.Button('Submit')]
    ]
    window = sg.Window('Actions', layout)
    return window
