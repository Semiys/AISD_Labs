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
        self.root.title("Credit Contract Manager")
        self.contracts = []
        self.create_widgets()  # Создаем виджеты при инициализации
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)

    def create_widgets(self):
        # Создаем меню
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        exit_button = tk.Button(self.root, text="Exit", command=self.exit_app)
        exit_button.pack(side='bottom', fill='x', padx=5, pady=5)

        # Создаем метку
        self.label = tk.Label(self.root, text="Credit Contract Manager", font=("Helvetica", 16))
        self.label.pack(pady=10)

        # Создаем кнопку для загрузки данных
        self.load_button = tk.Button(self.root, text="Load Contracts", command=self.load_data)
        self.load_button.pack(pady=5)

        # Создаем кнопку для сегментации по сумме
        self.segment_amount_button = tk.Button(self.root, text="Segment by Amount", command=self.segment_and_visualize_by_amount)
        self.segment_amount_button.pack(pady=5)

        # Создаем кнопку для сегментации по менеджеру
        self.segment_manager_button = tk.Button(self.root, text="Segment by Manager", command=self.segment_and_visualize_by_manager)
        self.segment_manager_button.pack(pady=5)

        # Статусная строка
        self.status = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def load_data(self):
        filename = filedialog.askopenfilename(title="Select a file", filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")])
        if filename:
            self.load_contracts(filename)

    def update_status(self, message):
        self.status.config(text=message)

    def load_contracts(self, filename):
        self.contracts.clear()  # Очистка предыдущих данных
        try:
            with open(filename, 'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) == 3:
                        contract = CreditContract(parts[0], float(parts[1]), parts[2])
                        self.contracts.append(contract)
                    else:
                        messagebox.showerror("Error", "Incorrect file format")
                        return
            messagebox.showinfo("Success", "Contracts loaded successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def segment_and_visualize_by_amount(self):
        # Сегментация по суммам
        segments = {'Small': 0, 'Medium': 0, 'Large': 0}
        for contract in self.contracts:
            if contract.amount < 10000:
                segments['Small'] += 1
            elif contract.amount < 50000:
                segments['Medium'] += 1
            else:
                segments['Large'] += 1

        # Визуализация результатов
        self.visualize_segmentation(segments, "Segmentation by Amount")

    def segment_and_visualize_by_manager(self):
        # Сегментация по менеджерам
        segments = {}
        for contract in self.contracts:
            if contract.manager not in segments:
                segments[contract.manager] = 1
            else:
                segments[contract.manager] += 1

        # Визуализация результатов
        self.visualize_segmentation(segments, "Segmentation by Manager")

    def visualize_segmentation(self, data, title):
        # Визуализация сегментации
        if self.figure_canvas:
            self.figure_canvas.get_tk_widget().destroy()

        figure, ax = plt.subplots()
        ax.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.title(title)

        # Встраиваем Matplotlib в Tkinter
        self.figure_canvas = FigureCanvasTkAgg(figure, master=self.root)
        self.figure_canvas.draw()
        self.figure_canvas.get_tk_widget().pack()

    def exit_app(self):
        print("Exiting the application")
        self.root.quit()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = ContractApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()