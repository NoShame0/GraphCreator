import json
import os

from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
import mainStructures as mS
from PIL import Image, ImageTk
import save
import tkinter.filedialog as fd

with open('seetings.json', 'r') as file:
    settings = json.load(file)

# names_graphs = ["Бинарное дерево", "Гиперкуб", "Сбалансированное дерево", "Циркулянт", "Граф штанги",
#                 "Сетчатый граф", 'Граф "Звезда"', 'Граф "Колесо"', 'Граф "Тюран"', "Лестничный граф",
#                 "Граф Дороговцева-Гольцева-Мендеса"]


available_graphs = {
    "Бинарное дерево": (mS.binomal_tree_create, 'Высота дерева'),
    "Гиперкуб": (mS.hypercube_create, 'Размерность гиперкуба'),
    "Сбалансированное дерево": (mS.balanced_tree_create, 'Количество ветвлений',
                                'Высота сбалансированного деорева'),
    "Циркулянт": (mS.circulant_create, 'Количество вершин результирующего графа',
                  'Элементы порождающего множества, '
                  'состоящего из целых чисел вида x1, x2, x3 ... xm такие, что '
                  '1 <= x1 < x2 < x3 < ... < xm, где m - количество чисел в множестве'),
    "Граф штанги": (mS.barbell_graph_create, 'Размерность m1', 'Размерность m2'),
    "Сетчатый граф": (mS.grid_graph_create, 'Размерность сетчатого графа(2 числа)', ''),
    'Граф "Звезда': (mS.star_graph_create, 'Количество вершин'),
    'Граф "Колесо': (mS.wheel_graph_create, 'Количество вершин'),
    'Граф "Тюран"': (mS.turan_graph_create, 'Количество вершин', 'Количество разделов'),
    "Лестничный граф": (mS.ladder_graph_create, 'Количество вершин'),
    "Граф Дороговцева-Гольцева-Мендеса": (mS.dorogovtsev_graph_create, 'Поколение')
}

names_graphs = available_graphs.keys()


# Класс главного окна
class MainWindow(Tk):
    def __init__(self, *args):

        super().__init__(*args)

        self.title("Graph Creator")

        _monitor_height = self.winfo_screenheight()  # Высота экрана
        _monitor_width = self.winfo_screenwidth()  # Ширина экрана

        self.geometry(f'{_monitor_width // 2}x{_monitor_height // 2}+{_monitor_width // 4}+{_monitor_height // 4}')

        self.mainmenu = Menu(self, tearoff=0)
        self.config(menu=self.mainmenu)

        # Меню файл
        self.mainmenu.add_cascade(label='Файл', menu=self.file_menu_create())

        # Окно настроек
        self.setWin = None
        self.mainmenu.add_cascade(label='Настройки', menu=self.settings_menu_create())

        self.tab_control = ttk.Notebook(self)

        self.menu_tab = Menu(self, tearoff=0)  # Меню вкладки изображения
        self.menu_tab_create = Menu(self, tearoff=0)  # Меню вкладки создания графов

        self._current_tab = None
        self.menu_tab_create.add_command(label='Закрыть вкладку', command=self.tab_close)
        self.menu_tab.add_command(label='Удалить из директории', command=self.delete_tab)
        self.menu_tab.add_command(label='Закрыть вкладку', command=self.tab_close)
        self.menu_tab.add_command(label='Показать папку хранения', command=self.tab_storage)
        self.menu_tab.add_command(label='Переименовать файл', command=self.tab_rename)

        self.tab_control.bind('<Button-3>', self.show_tab_menu)  # Бинд правой кнопки мыши на всплывающее меню
        self.tab_picLinks = []

        self._btn_open, self._btn_create = None, None
        self.tab_create = None
        self.general_menu_create()

    def general_menu_create(self):

        font_size, bg_color, fg_color = '15', '#555', '#ccc'
        self._btn_open = Button(self, text='Открыть файл...', font=font_size, background=bg_color, foreground=fg_color,
                                command=self.filesopen)
        self._btn_create = Button(self, text='Создать файл...', font=font_size, background=bg_color,
                                  foreground=fg_color, command=self.filescreate)

        self._btn_open.pack(expand=True, side=LEFT)
        self._btn_create.pack(expand=True, side=RIGHT)

    def general_menu_destroy(self):

        self._btn_open.destroy()
        self._btn_create.destroy()

    def tab_picture_create(self, link):
        tab_name = link.split('/')[-1]

        self.tab_picLinks.append(link)

        tab = GraphPictureTab(self, link)
        if not self.tab_create is None:
            self.tab_control.insert(self.tab_control.index(self.tab_create), tab, text=tab_name)
        else:
            self.tab_control.add(tab, text=tab_name)

        self.tab_control.select(tab)
        self.tab_control.pack(expand=True, fill=BOTH)

    # Метод создания меню компонента панели инструментов "Файл"
    def file_menu_create(self):

        file_menu = Menu(self.mainmenu, tearoff=0)
        file_menu.add_command(label='Открыть...', command=self.filesopen)
        file_menu.add_command(label='Создать...', command=self.filescreate)

        return file_menu

    # Метод создания меню компонента панели инструментов "Настройки"
    def settings_menu_create(self):

        settings_menu = Menu(self.mainmenu, tearoff=0)
        settings_menu.add_command(label='Папка хранения', command=self.settings_window_create)

        return settings_menu

    def filescreate(self):
        if not self.tab_create:
            self.general_menu_destroy()
            self.tab_create = ttk.Frame(self.tab_control)

            label_create = Label(self.tab_create, text='Выберите топологию', font='20')
            label_create.grid(column=0, row=0, columnspan=3, pady=40)

            max_len = max([len(name) for name in names_graphs])

            btns = [ButtonCreate(name, self, text=name, width=max_len, activebackground='Gray',
                                 activeforeground='white',
                                 highlightcolor='purple',
                                 relief='ridge') for name in names_graphs]

            n_columns = 3

            for i in range(n_columns):
                self.tab_create.grid_columnconfigure(i, weight=1)

            for i in range(len(btns) // n_columns + 10):
                self.tab_create.grid_rowconfigure(i, weight=1)

            for btn in btns:
                btn['command'] = btn.input_window_create

            for i in range(len(btns)):
                btns[i].grid(column=i % 3, row=(i // 3) + 1)

            self.tab_control.insert(END, self.tab_create, text='Создание графа')

        self.tab_control.select(self.tab_create)
        self.tab_control.pack(expand=1, fill='both')

    def filesopen(self):

        ftypes = [('PNG файлы', '*.png'), ('Все файлы', '*')]
        dlg = fd.Open(self, filetypes=ftypes)
        open_link = dlg.show()

        if open_link != '':
            self.general_menu_destroy()
            if open_link not in self.tab_picLinks:
                self.tab_picture_create(open_link)
                print_open_successful()

            self.tab_control.select(self.tab_picLinks.index(open_link))

    def show_tab_menu(self, event):

        self._current_tab = self.tab_control.index('@%d,%d' % (event.x, event.y))

        if not self.tab_create is None and self._current_tab == self.tab_control.index(self.tab_create):
            self.menu_tab_create.post(event.x_root, event.y_root)
            return

        self.menu_tab.post(event.x_root, event.y_root)

    # Переименование файла
    def tab_rename(self):
        new_name = None

        def rename():
            nonlocal new_name
            new_name = entry_for_new_name.get()
            try:
                new_link = save.save_picture_name(new_name, self.tab_picLinks[index])
            except FileNotFoundError:
                print_delete_error()
                new_name_window.destroy()
                self.tab_close()
            else:
                if new_link != self.tab_picLinks[index] and new_link != '':
                    self.tab_control.tab(index, text=new_link.split('/')[-1])
                    self.tab_control.pack()
                    self.tab_picLinks[index] = new_link
                    new_name_window.destroy()

        index = self._current_tab

        new_name_window = Toplevel()
        new_name_window.title('Переименование файла')
        new_name_window.geometry('600x200')
        new_name_window.resizable(False, False)  # Запрет на мастштабирование

        label_name = Label(new_name_window, text='Новое имя:')
        label_name.pack(padx=10, pady=1)

        entry_for_new_name = Entry(new_name_window)
        entry_for_new_name.pack(padx=20, pady=20)

        btn_name_create = Button(new_name_window, text='Переименовать', command=rename)
        btn_name_create.pack(padx=10, pady=30)

    # Закрытие вкладки
    def tab_close(self):
        index = self._current_tab

        if not self.tab_create is None and index == self.tab_control.index(self.tab_create):
            self.tab_create.destroy()
            self.tab_create = None
        else:
            self.tab_control.forget(index)
            self.tab_picLinks.pop(index)
        # Проверка на существование вкладок
        if not self.tab_control.tabs():
            self.tab_control.pack_forget()
            self.general_menu_create()

    # Отображение файла изображения в проводнике
    def tab_storage(self):
        index = self._current_tab
        tab = self.tab_control.tab(index)

        link = self.tab_picLinks[index].replace(tab['text'], '')
        script_link = os.getcwd()
        os.chdir(link)
        os.system('start .')
        os.chdir(script_link)

    # Удаление файла
    def delete_tab(self):
        index = self._current_tab

        try:
            os.remove(self.tab_picLinks[index])
        except FileNotFoundError:
            print_delete_error()

        self.tab_control.forget(index)
        self.tab_picLinks.pop(index)

        if not self.tab_control.tabs():
            self.tab_control.pack_forget()
            self.general_menu_create()

    def settings_window_create(self):
        if self.setWin is None:
            self.setWin = Settings()
            self.setWin.protocol('WM_DELETE_WINDOW', self.settings_window_delete)

    def settings_window_delete(self):
        self.setWin.destroy()
        self.setWin = None


class DataWindow(Toplevel):
    def __init__(self, master, name):
        super().__init__()

        self.resizable(False, False)

        self.master = master
        self.data = []
        self.graph = available_graphs[name]
        self.entrs = []  # Инициализация списка доступных в окне полей

        for _i in range(1, len(self.graph)):
            lbl = Label(self, text=self.graph[_i], padx=10, anchor='w')
            lbl.grid(row=_i, column=0)

            # Создание полей
            entry = Entry(self)
            self.entrs.append(entry)
            entry.grid(row=_i, column=2, pady=10, padx=20)

        self.lbl_name = Label(self, text='Имя файла', padx=10, pady=30, anchor='w')
        self.entry_name = Entry(self)
        self.lbl_name.grid(row=len(self.graph) + 1, column=0)
        self.entry_name.grid(row=len(self.graph) + 1, column=2)

        self.btnin = Button(self, text='Создать граф', command=self.graph_create)
        self.btnin.grid(column=2, pady=30)

    def graph_create(self):

        self.data = []
        for en in self.entrs:
            self.data.append(en.get())

        try:
            self.graph[0](self.data)
        except:
            print_create_error()
        else:
            filename = self.entry_name.get()

            link_save = save.save_picture_name(filename)
            if link_save:
                self.master.tab_create.destroy()  # Уничтожение вкладки создания графов в главном окне
                self.master.tab_create = None

                self.master.tab_picture_create(link_save)
                self.destroy()  # Уничтожение окна ввода данных, требующихся для создания графов в главном окне

                print_create_successful()


# Класс кнопки для создания окна ввода данных о графе
class ButtonCreate(Button):

    def __init__(self, name_graph, master, **kwargs):
        super().__init__(master.tab_create, kwargs)
        self.name = name_graph
        self.master = master  # Окно, в котором отображается кнопка

    def input_window_create(self):
        window_data = DataWindow(self.master, self.name)
        window_data.title('Создание графа')


class GraphPictureTab(ttk.Frame):
    def __init__(self, master, link):
        super().__init__(master.tab_control)

        self.master = master
        self.link = link

        img = Image.open(self.link)
        img = ImageTk.PhotoImage(img)

        self.label_photo = Label(self, image=img)  # Создается Label для вставки изображения
        self.label_photo.image = img

        self.label_photo.pack()


class Settings(Toplevel):
    def __init__(self):
        super().__init__()

        try:
            with open('seetings.json', 'r') as _file:
                self.link_save = json.load(_file)['savelink']
        except KeyError:
            self.link_save = '(Папка не выбрана)'

        self.resizable(False, False)
        self.label_dir = Label(self, text=f'Текущая папка дляв сохранения файлов: {self.link_save}', padx=30, pady=30)
        self.label_dir.grid()
        Button(self, text='Изменить...', command=self.changedir).grid(padx=30, pady=30)

    def changedir(self):
        directory = fd.askdirectory(title="Выбрать папку для сохранения файлов")

        if directory != '':
            with open('seetings.json', 'w') as _file:
                self.label_dir['text'] = f'Текущая папка для сохранения файлов: {directory}'
                settings['savelink'] = directory
                json.dump(settings, _file)


# Всплывающие окна
def print_create_error():
    msg = 'Не удалось построить граф по введенным данным'
    mb.showerror('Ошибка!', msg)


def print_create_successful():
    msg = 'Граф успешно создан!'
    mb.showinfo('Успешно!', msg)


def print_open_successful():
    msg = 'Граф успешно открыт!'
    mb.showinfo('Успешно!', msg)


def print_delete_error():
    msg = 'Файл не найден!'
    mb.showerror('Ошибка!', msg)
