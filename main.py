import customtkinter as ctk
from Pipeline import Pipeline
from Essentials import Txt_package

data_path = 'topic_offers.csv'
pipeline = Pipeline(data_path)

summaries = []
sum_options = {}

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
app = ctk.CTk()
app.geometry("850x480")

# Поля ввода

pathEntry = ctk.CTkEntry(master=app, placeholder_text="Path to PDF")
pathEntry.place(relx=0.075, rely=0.2, anchor=ctk.W)

url_use_box = ctk.CTkCheckBox(master=app, text="Use URL", onvalue='True', offvalue='False')
url_use_box.place(relx=0.075, rely=0.3, anchor=ctk.W)

page_numLabel = ctk.CTkLabel(master=app, text="Start from page:")
page_numLabel.place(relx=0.075, rely=0.4, anchor=ctk.W)

page_numEntry = ctk.CTkEntry(master=app, placeholder_text="1", width=30)
page_numEntry.place(relx=0.2, rely=0.4, anchor=ctk.W)

def summarize():
    summaries = pipeline.sum_eval(pathEntry.get(), eval(url_use_box.get()), int(page_numEntry.get()))
    sum_options.clear()

    for i in range(len(summaries)):
        option_name = 'Option ' + str(i+1)
        sum_options[option_name] = summaries[i]

    options = list(sum_options.keys())

    optionmenu_var = ctk.StringVar(value='Option 1')

    sum_optionsMenu = ctk.CTkOptionMenu(master=app, values= options, command=optionmenu_callback, variable=optionmenu_var)
    sum_optionsMenu.place(relx=0.9, rely=0.1, anchor=ctk.E)

    print_summary(summaries[0])

def reinit_summarizer(choice):
    if (choice == 'LSA'):
        pipeline.summarizator.init_summarizer('LSA')
    elif (choice == 'T5'):
        pipeline.summarizator.init_summarizer('T5')


button = ctk.CTkButton(master=app, text="Summarize", command=summarize)
button.place(relx=0.075, rely=0.8, anchor=ctk.W)

methods_Label = ctk.CTkLabel(master=app, text="Summariazation method:")
methods_Label.place(relx=0.075, rely=0.5, anchor=ctk.W)

method_var = ctk.StringVar(value='LSA')
sum_methodsMenu = ctk.CTkOptionMenu(master=app, values=['LSA','T5'], command=reinit_summarizer, variable=method_var)
sum_methodsMenu.place(relx=0.075, rely=0.6, anchor=ctk.W)

# Вывод суммаризации
def switch_sum_display():
    if len(summaries) > 0:
        print('Option changed')
switch_sum = switch_sum_display()

def optionmenu_callback(choice):
    print_summary(sum_options[choice])

options_Label = ctk.CTkLabel(master=app, text="Summariazation option:")
options_Label.place(relx=0.7, rely=0.1, anchor=ctk.E)

optionmenu_var = ctk.StringVar(value="None")
sum_optionsMenu = ctk.CTkOptionMenu(master=app, values=[], command=optionmenu_callback, variable=optionmenu_var)
sum_optionsMenu.place(relx=0.9, rely=0.1, anchor=ctk.E)

sum_displayBox = ctk.CTkTextbox(master=app, width=500, height=320)
sum_displayBox.place(relx=0.9, rely=0.5, anchor=ctk.E)

score_Label = ctk.CTkLabel(master=app, text="Summary score:")
score_Label.place(relx=0.45, rely=0.9, anchor=ctk.E)

score_displayBox = ctk.CTkTextbox(master=app, width=150, height=20)
score_displayBox.place(relx=0.65, rely=0.9, anchor=ctk.E)

def print_summary(pack: Txt_package):
    sum_displayBox.delete('0.0', '200.0')
    sum_displayBox.insert(index='0.0', text=pack.txt)

    score_displayBox.delete('0.0', '200.0')
    score_displayBox.insert(index='0.0', text=str(pack.interest_score))


app.mainloop()