from select import select
import tkinter as tk
from tkinter import messagebox

class GrandmaPantryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vecmāmiņas ievārījuma saraksts")

        # Produktu lists
        self.products_list = [
            'Apelsīnu', 'Aprikožu', 'Aveņu', 'Ābolu', 'Brūkleņu', 
            'Bumbieru', 'Dzērveņu', 'Ķiršu', 'Mango', 'Melleņu', 
            'Plūmju', 'Smiltsērkšķu', 'Tomātu', 'Upeņu', 'Zemeņu'
        ]
        
        self.pantry = []
        self.jams = []

        self.create_widgets()

    def create_widgets(self):
        # Produkta izvēle pievienošanai
        self.product_label = tk.Label(self.root, text="Izvēlies produktu")
        self.product_label.grid(row=0, column=0)
        
        self.product_var = tk.StringVar(value=self.products_list[0])
        self.product_menu = tk.OptionMenu(self.root, self.product_var, *self.products_list)
        self.product_menu.grid(row=0, column=1)
        
        self.quantity_label = tk.Label(self.root, text="Daudzums (kg)")
        self.quantity_label.grid(row=1, column=0)
        
        self.quantity_spinbox = tk.Spinbox(self.root, from_=1, to=10, width=5)
        self.quantity_spinbox.grid(row=1, column=1)
        
        self.add_button = tk.Button(self.root, text="Pievienot", command=self.add_product)
        self.add_button.grid(row=1, column=2)

        # Produkta un ievārījuma saraksts
        self.pantry_label = tk.Label(self.root, text="Produkti")
        self.pantry_label.grid(row=2, column=1)
        
        self.pantry_listbox =tk.Listbox(self.root, height=10, width=50)
        self.pantry_listbox.grid(row=3, column=0, columnspan=3)
        self.pantry_listbox.bind("<<ListboxSelect>>", self.check_jam_selection)

        self.jam_label = tk.Label(self.root, text="Ievārījumi")
        self.jam_label.grid(row=2, column=4)

        self.jam_listbox = tk.Listbox(self.root, height=10, width=50)
        self.jam_listbox.grid(row=3, column=3, columnspan=3)
        self.jam_listbox.bind("<<ListboxSelect>>", self.disable_jam_button)
        
        # Dzēšanas poga
        self.delete_button = tk.Button(self.root, text="Noņemt", command=self.nonemt_product)
        self.delete_button.grid(row=4, column=4)
        
        # ievārījuma taisīšana
        self.jam_quantity_label = tk.Label(self.root, text="Ievārījuma daudzums (kg)")
        self.jam_quantity_label.grid(row=4, column=0)
        
        self.jam_quantity_spinbox = tk.Spinbox(self.root, from_=1, to=10, width=5)
        self.jam_quantity_spinbox.grid(row=4, column=1)
        
        self.jam_button = tk.Button(self.root, text="Taisīt ievārījumu", command=self.make_jam)
        self.jam_button.grid(row=4, column=2)

        # Produktu pievienošana
    def add_product(self):
        product = self.product_var.get()
        quantity = self.quantity_spinbox.get()

        if not quantity or not quantity.isdigit():
            messagebox.showwarning("Kļūda", "Lūdzu ievadiet pareizu daudzumu!")
            return


        # Eksistējošu produktu palielināšana
        for item in self.pantry:
            if item["name"] == product:
                item["quantity"] += int(quantity)
                self.update_pantry_listbox()
                return

        self.pantry.append({"name": product, "quantity": int(quantity)})
        self.update_pantry_listbox()

        index = select[0]
        product = self.pantry[index]
        self.product_var.set(product["name"])
        self.quantity_spinbox.delete(0, tk.END)
        self.quantity_spinbox.insert(0, product["quantity"])

    def nonemt_product(self):
        # Produkta noņemšana
        selected = self.pantry_listbox.curselection()
        if not selected:
            messagebox.showwarning("Kļūda", "Lūdzu izvēlieties produktu!")
            return
        
        index = selected[0]
        self.pantry.pop(index)
        self.update_pantry_listbox()


    def make_jam(self):
        # Ievārījuma taisīšana
        selected = self.pantry_listbox.curselection()
        if not selected:
            messagebox.showwarning("Kļūda", "Lūdzu izvēlieties produktu!")
            return
        
        index = selected[0]
        product = self.pantry[index]

        # Ievārījuma daudzums
        jam_quantity = int(self.jam_quantity_spinbox.get())
        required_quantity = jam_quantity * 2

        if product["quantity"] < required_quantity:
            messagebox.showwarning("Kļūda", f"Nepietiek {product['name']} ievārījumam! Nepieciešami vismaz {required_quantity} kg.")
            return

        # Samazina daudzumu lai pievienotu ievārījumu
        self.pantry[index]["quantity"] -= required_quantity
        if self.pantry[index]["quantity"] == 0:
            self.pantry.pop(index)
        
        jam_name = f"{product['name']} Ievārījums"
        
        # Ievārijuma pievienošana blakus listbox
        self.jams.append({"name": jam_name, "quantity": jam_quantity})
        self.update_pantry_listbox()
        self.update_jam_listbox()

        # Atspējo ievārījuma taisīšanu jau gatavam ievārījumam
    def check_jam_selection(self, event):
        selected = self.pantry_listbox.curselection()
        if selected:
            index = selected[0]
            product_name = self.pantry[index]["name"]
            if product_name.startswith("Ievārījums"):
                self.jam_button.config(state=tk.DISABLED)
            else:
                self.jam_button.config(state=tk.NORMAL)

    def disable_jam_button(self, event):
        self.jam_button.config(state=tk.DISABLED)

        # Produkta saraksta atjaunošana
    def update_pantry_listbox(self):
        self.pantry_listbox.delete(0, tk.END)
        for item in self.pantry:
            entry = f"{item['name']} ({item['quantity']} kg)"
            self.pantry_listbox.insert(tk.END, entry)

        # Ievārījuma saraksta atjaunošana
    def update_jam_listbox(self):
        self.jam_listbox.delete(0, tk.END)
        for item in self.jams:
            entry = f"{item['name']} ({item['quantity']} kg)"
            self.jam_listbox.insert(tk.END, entry)

root = tk.Tk()
app = GrandmaPantryApp(root)
root.mainloop()
