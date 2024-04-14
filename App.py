import customtkinter as ctk
from Pipeline import Pipeline
from Essentials import Txt_package

class App(ctk.CTk):
    def __int__(self):
        ctk.CTk()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("SumEval")
        self.geometry("850x480")

        # Поля ввода - слева

        self.pathEntry = ctk.CTkEntry(master=self, placeholder_text="Path to PDF")
        self.pathEntry.place(relx=0.075, rely=0.2, anchor=ctk.W)

        self.url_use_box = ctk.CTkCheckBox(master=self, text="Use URL", onvalue='True', offvalue='False')
        self.url_use_box.place(relx=0.075, rely=0.3, anchor=ctk.W)

        self.page_numLabel = ctk.CTkLabel(master=self, text="Start from page:")
        self.page_numLabel.place(relx=0.075, rely=0.4, anchor=ctk.W)

        self.page_numEntry = ctk.CTkEntry(master=self, placeholder_text="1", width=30)
        self.page_numEntry.place(relx=0.2, rely=0.4, anchor=ctk.W)

        self.sum_button = ctk.CTkButton(master=self, text="Summarize", command=self.summarize)
        self.sum_button.place(relx=0.075, rely=0.8, anchor=ctk.W)

        self.methods_Label = ctk.CTkLabel(master=self, text="Summariazation method:")
        self.methods_Label.place(relx=0.075, rely=0.5, anchor=ctk.W)

        self.method_var = ctk.StringVar(value='LSA')
        self.sum_methodsMenu = ctk.CTkOptionMenu(master=self, values=['LSA', 'T5'], command=self.reinit_summarizer, variable=self.method_var)
        self.sum_methodsMenu.place(relx=0.075, rely=0.6, anchor=ctk.W)

        # Поля вывода - справа

        self.options_Label = ctk.CTkLabel(master=self, text="Summariazation option:")
        self.options_Label.place(relx=0.7, rely=0.1, anchor=ctk.E)

        self.optionmenu_var = ctk.StringVar(value="None")
        self.sum_optionsMenu = ctk.CTkOptionMenu(master=self, values=[], command=self.optionmenu_callback, variable=self.optionmenu_var)
        self.sum_optionsMenu.place(relx=0.9, rely=0.1, anchor=ctk.E)

        self.sum_displayBox = ctk.CTkTextbox(master=self, width=500, height=320)
        self.sum_displayBox.place(relx=0.9, rely=0.5, anchor=ctk.E)

        self.score_Label = ctk.CTkLabel(master=self, text="Summary score:")
        self.score_Label.place(relx=0.45, rely=0.9, anchor=ctk.E)

        self.score_displayBox = ctk.CTkTextbox(master=self, width=150, height=20)
        self.score_displayBox.place(relx=0.65, rely=0.9, anchor=ctk.E)

        self.data_path = 'topic_offers.csv'
        self.pipeline = Pipeline(self.data_path)

        self.summaries = []
        self.sum_options = {}

    def summarize(self):
        self.summaries = self.pipeline.sum_eval(self.pathEntry.get(), eval(self.url_use_box.get()), int(self.page_numEntry.get()))
        self.sum_options.clear()

        for i in range(len(self.summaries)):
            option_name = 'Option ' + str(i + 1)
            self.sum_options[option_name] = self.summaries[i]

        options = list(self.sum_options.keys())

        self.optionmenu_var = ctk.StringVar(value='Option 1')

        self.sum_optionsMenu = ctk.CTkOptionMenu(master=self, values=options, command=self.optionmenu_callback,variable=self.optionmenu_var)
        self.sum_optionsMenu.place(relx=0.9, rely=0.1, anchor=ctk.E)

        self.print_summary(self.summaries[0])

    def reinit_summarizer(self, choice):
        if (choice == 'LSA'):
            self.pipeline.summarizator.init_summarizer('LSA')
        elif (choice == 'T5'):
            self.pipeline.summarizator.init_summarizer('T5')

    # Вывод суммаризации
    def switch_sum_display(self):
        if len(self.summaries) > 0:
            print('Option changed')

    #switch_sum = switch_sum_display()

    def optionmenu_callback(self, choice):
        self.print_summary(self.sum_options[choice])

    def print_summary(self, pack: Txt_package):
        self.sum_displayBox.delete('0.0', '200.0')
        self.sum_displayBox.insert(index='0.0', text=pack.txt)

        self.score_displayBox.delete('0.0', '200.0')
        self.score_displayBox.insert(index='0.0', text=str(pack.interest_score))


if __name__ == '__main__':
    app = App()
    app.mainloop()