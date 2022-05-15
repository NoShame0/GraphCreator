import os
import tkinter.messagebox as mb
import matplotlib.pyplot
import json


def print_error_count():
    message = 'Невозможно создать файл!'
    mb.showerror('Ошибка!', message)


def save_picture():

    count_created_graphs = 0
    with open('seetings.json', 'r') as file:
        base_link = json.load(file)['savelink']

    while True:
        link = base_link + "/graph{}.png".format(count_created_graphs)
        try:
            check_file = open(link, 'rb')
        except FileNotFoundError:
            matplotlib.pyplot.savefig(link, format="PNG")
            break
        else:
            check_file.close()
            count_created_graphs = count_created_graphs + 1

    return link


def save_picture_name(name, old_link=None):

    namec = name
    count_created_graphs = 0
    same_exist = False
    change = True

    with open('seetings.json', 'r') as file:
        base_link = json.load(file)['savelink']

    if not name:
        if old_link is None:
            name = 'graph'
        else:
            mb.showerror('Ошибка!', 'Введите новое название файла!')
            return ''

    while True:
        if count_created_graphs == 0:
            link = base_link + "/" + name + '.png'
            new_name = name + '.png'
        else:
            link = base_link + "/" + name + str(count_created_graphs) + '.png'
            new_name = name + str(count_created_graphs) + '.png'

        if link == old_link and same_exist:
            mb.showinfo('Предупреждение!', 'Не удается переименовать файл!\nФайл с таким '
                                           'названием уже существует!')
            return ''
        elif link == old_link and not same_exist:
            mb.showinfo('Предупреждение!', 'Не удается переименовать файл!\nТекущее название файла совпадает с новым!')
            return ''

        if new_name in os.listdir(link.replace('/' + new_name, '')):
            count_created_graphs += 1
            same_exist = True
        else:
            if old_link is None:
                if namec: # Если исходное имя не пустая строка
                    if same_exist:
                        # Если возникали совпадения при генерации, возникает запрос на сохранение с новым именем
                        change = mb.askyesno('Предупреждение!',
                                             'Файл с таким названием уже существет!\nСохранить с именем ' +
                                              new_name + ' ?')
                if change:
                    matplotlib.pyplot.savefig(link, format="PNG")
                else:
                    return ''
                break
            else:

                if same_exist:
                    change = mb.askyesno('Предупреждение!', 'Файл с таким названием уже существует!\n'
                                                            'Сохранить с именем ' +
                                                            new_name + ' ?')
                if change:

                    os.rename(old_link, link)
                    mb.showinfo("Успешно!", 'Файл успешно переименован!')

                break

    if not old_link is None and not change:
        return old_link

    return link
