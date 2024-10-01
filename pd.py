import tkinter as tk
from tkinter import ttk

#root window
root = tk.Tk()
root.geometry('500x400')
root.resizable(False, False)
root.title('Listbox')

def nomainit_sarakstu():
   listbox.delete(0,END)
   for cilveks in visi_cilveki:
      listbox.insert("end","{},{},{}".format(cilveks.name,cilveks.sex,cilveks.age))


# create a list box
langs = ('Apelsīnu', 'Aprikožu', 'Aveņu', 'Ābolu', 'Brūkleņu', 'Bumbieru', 'Dzērveņu', 'Ķiršu', 'Mango', 'Melleņu', 
         'Plūmju', 'Smiltsērkšķu', 'Tomātu', 'Upeņu', 'Zemeņu')

var = tk.Variable(value=langs)

listbox = tk.Listbox(
    root,
    listvariable=var,
    height=6,
    selectmode=tk.EXTENDED)

listbox.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)


def items_selected(event):
    # get selected indices
    selected_indices = listbox.curselection()
    # get selected items
    selected_langs = ",".join([listbox.get(i) for i in selected_indices])
    msg = f'You selected: {selected_langs}'

    showinfo(title='Information', message=msg)


listbox.bind('<<ListboxSelect>>', items_selected)

root.mainloop()