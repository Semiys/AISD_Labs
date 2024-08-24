"""
Лабораторная работа №8:
Требуется написать объектно-ориентированную программу с графическим интерфейсом в соответствии со своим вариантом.
В программе должны быть реализованы минимум один класс, три атрибута, четыре метода (функции).
Ввод данных из файла с контролем правильности ввода.
Базы данных использовать нельзя. При необходимости сохранять информацию в виде файлов, разделяя значения запятыми или пробелами.
Для GUI использовать библиотеку tkinter.

Вариант 25. Объекты – кредитные договоры
Функции:	сегментация полного списка договоров по суммам (мелкие, средние,крупные)
визуализация предыдущей функции в форме круговой диаграммы
сегментация полного списка договоров по менеджерам
визуализация предыдущей функции в форме круговой диаграммы

"""
import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CreditContract:
    def __init__(self, contract_id, amount, manager):
        self.contract_id = contract_id
        self.amount = amount
        self.manager = manager

    def __repr__(self):
        return f"Contract ID: {self.contract_id}, Amount: {self.amount}, Manager: {self.manager}"

class ContractApp:
    def __init__(self, root):
        self.figure_canvas = None
        self.root = root
        self.root.title("Кредитный контрактный менеджер")
        self.contracts = []
        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)

    def create_widgets(self):
        """ Создание виджетов приложения """
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        exit_button = tk.Button(self.root, text="Выход", command=self.exit_app)
        exit_button.pack(side='bottom', fill='x', padx=5, pady=5)

        """ Создание окна с графиком """
        self.label = tk.Label(self.root, text="Кредитный контрактный менеджер", font=("Helvetica", 16))
        self.label.pack(pady=10)

        """ Создание кнопки для загрузки данных """
        self.load_button = tk.Button(self.root, text="Загрузка контрактов", command=self.load_data)
        self.load_button.pack(pady=5)

        """ Создание кнопки для сегментации по сумме """
        self.segment_amount_button = tk.Button(self.root, text="Сегментировать по сумме", command=self.segment_and_visualize_by_amount)
        self.segment_amount_button.pack(pady=5)

        """ Создание кнопки для сегментации по менеджеру"""
        self.segment_manager_button = tk.Button(self.root, text="Сегментировать по менеджеру", command=self.segment_and_visualize_by_manager)
        self.segment_manager_button.pack(pady=5)

        """ Создание статус-бара """
        self.status = tk.Label(self.root, text="Готов", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def load_data(self):
        filename = filedialog.askopenfilename(title="Выберите файл", filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")])
        if filename:
            self.load_contracts(filename)

    def update_status(self, message):
        self.status.config(text=message)

    def load_contracts(self, filename):
        self.contracts.clear()
        try:
            with open(filename, 'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) == 3:
                        contract = CreditContract(parts[0], float(parts[1]), parts[2])
                        self.contracts.append(contract)
                    else:
                        messagebox.showerror("Error", "Неверный формат файла")
                        return
            messagebox.showinfo("Успех", "Контракты успешно загружены")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def segment_and_visualize_by_amount(self):
        """ Сегментация по сумме"""
        segments = {'Малые': 0, 'Средние': 0, 'Крупные': 0}
        for contract in self.contracts:
            if contract.amount < 10000:
                segments['Малые'] += 1
            elif contract.amount < 50000:
                segments['Средние'] += 1
            else:
                segments['Крупные'] += 1

        """ Визуализация результатов"""
        self.visualize_segmentation(segments, "Сегментация по суммам")

    def segment_and_visualize_by_manager(self):
        """ Сегментация по менеджеру"""
        segments = {}
        for contract in self.contracts:
            if contract.manager not in segments:
                segments[contract.manager] = 1
            else:
                segments[contract.manager] += 1

        """ Визуализация результатов """
        self.visualize_segmentation(segments, "Сегментация по менеджерам")

    def visualize_segmentation(self, data, title):
        """ Визуализация сегментации с помощью Matplotlib  """
        if self.figure_canvas:
            self.figure_canvas.get_tk_widget().destroy()

        figure, ax = plt.subplots()
        ax.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', startangle=90)
        ax.axis('equal')

        plt.title(title)


        self.figure_canvas = FigureCanvasTkAgg(figure, master=self.root)
        self.figure_canvas.draw()
        self.figure_canvas.get_tk_widget().pack()

    def exit_app(self):
        print("Выход из приложения")
        self.root.quit()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = ContractApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
