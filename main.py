import json


def check_settings():
    with open('seetings.json', 'r') as file_check_settings:
        flag = False
        default_settings = {
            'savelink': '',
            'node_color': 'blue',
            'node_size': 300
        }
        try:
            settings = json.load(file_check_settings)
        except json.decoder.JSONDecodeError:
            settings = default_settings
            flag = True
        else:
            for setting in default_settings.keys():
                if setting not in settings:
                    flag = True
                    settings[setting] = default_settings[setting]

    if flag:
        with open('seetings.json', 'w') as file_write:
            json.dump(settings, file_write)


if __name__ == '__main__':

    check_settings()

    from gui import MainWindow

    root = MainWindow()
    root.config(bg='aquamarine')
    root.mainloop()
