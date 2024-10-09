import tkinter as tk
from tkinter import messagebox

class GrandmaPantryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vecmāmiņas pieliekamais")
        
        # Pieliekamā produktu saraksts
        self.pantry = []
        
        # UI izkārtojums
        self.create_widgets()

    def create_widgets(self):
        # Produkta ievades daļa
        self.product_label = tk.Label(self.root, text="Produkts")
        self.product_label.grid(row=0, column=0)
        
        self.product_entry = tk.Entry(self.root)
        self.product_entry.grid(row=0, column=1)
        
        self.quantity_label = tk.Label(self.root, text="Daudzums (kg)")
        self.quantity_label.grid(row=1, column=0)
        
        self.quantity_entry = tk.Entry(self.root)
        self.quantity_entry.grid(row=1, column=1)
        
        self.type_label = tk.Label(self.root, text="Veids")
        self.type_label.grid(row=2, column=0)
        
        self.type_var = tk.StringVar(value="Auglis")
        self.type_fruit = tk.Radiobutton(self.root, text="Auglis", variable=self.type_var, value="Auglis", command=self.check_apple)
        self.type_fruit.grid(row=2, column=1)
        self.type_vegetable = tk.Radiobutton(self.root, text="Dārzenis", variable=self.type_var, value="Dārzenis", command=self.check_apple)
        self.type_vegetable.grid(row=2, column=2)
        
        # Ābolu šķirnes lauks
        self.variety_label = tk.Label(self.root, text="Ābolu šķirne")
        self.variety_entry = tk.Entry(self.root)
        
        # Poga ražas pievienošanai
        self.add_button = tk.Button(self.root, text="Pievienot ražu", command=self.add_product)
        self.add_button.grid(row=4, column=1)
        
        # Pieliekamā saraksts
        self.pantry_listbox = tk.Listbox(self.root, height=10, width=50)
        self.pantry_listbox.grid(row=5, column=0, columnspan=3)
        
        # Poga produkta rediģēšanai
        self.edit_button = tk.Button(self.root, text="Labot", command=self.edit_product)
        self.edit_button.grid(row=6, column=0)
        
        # Poga produkta dzēšanai
        self.delete_button = tk.Button(self.root, text="Apēst", command=self.eat_product)
        self.delete_button.grid(row=6, column=1)
        
        # Ievārījuma daļa
        self.jam_label = tk.Label(self.root, text="Izveidot ievārījumu")
        self.jam_label.grid(row=7, column=0)
        
        self.jam_button = tk.Button(self.root, text="Taisīt ievārījumu", command=self.make_jam)
        self.jam_button.grid(row=7, column=1)

    def check_apple(self):
        # Pārbauda vai ir izvēlēti āboli
        if self.product_entry.get().lower() == "āboli":
            self.variety_label.grid(row=3, column=0)
            self.variety_entry.grid(row=3, column=1)
        else:
            self.variety_label.grid_forget()
            self.variety_entry.grid_forget()

    def add_product(self):
        # Iegūst datus no ievades laukiem
        product = self.product_entry.get()
        quantity = self.quantity_entry.get()
        product_type = self.type_var.get()
        variety = self.variety_entry.get() if product.lower() == "āboli" else ""

        if not product or not quantity or not quantity.isdigit():
            messagebox.showwarning("Kļūda", "Lūdzu ievadiet pareizu produkta nosaukumu un daudzumu!")
            return

        entry = f"{product} ({quantity} kg)"
        if product.lower() == "āboli":
            entry += f" - {variety}"
        entry += f" [{product_type}]"
        
        self.pantry.append({"name": product, "quantity": int(quantity), "type": product_type, "variety": variety})
        self.update_pantry_listbox()

    def edit_product(self):
        # Rediģē izvēlēto produktu
        selected = self.pantry_listbox.curselection()
        if not selected:
            messagebox.showwarning("Kļūda", "Lūdzu izvēlieties produktu!")
            return
        
        index = selected[0]
        product = self.pantry[index]
        self.product_entry.delete(0, tk.END)
        self.product_entry.insert(0, product["name"])
        self.quantity_entry.delete(0, tk.END)
        self.quantity_entry.insert(0, product["quantity"])
        self.type_var.set(product["type"])
        
        if product["name"].lower() == "āboli":
            self.variety_entry.delete(0, tk.END)
            self.variety_entry.insert(0, product["variety"])
            self.check_apple()

    def eat_product(self):
        # Apēd izvēlēto produktu
        selected = self.pantry_listbox.curselection()
        if not selected:
            messagebox.showwarning("Kļūda", "Lūdzu izvēlieties produktu!")
            return
        
        index = selected[0]
        self.pantry.pop(index)
        self.update_pantry_listbox()

    def make_jam(self):
        # Izveido ievārījumu no produkta
        selected = self.pantry_listbox.curselection()
        if not selected:
            messagebox.showwarning("Kļūda", "Lūdzu izvēlieties produktu!")
            return
        
        index = selected[0]
        product = self.pantry[index]

        if product["quantity"] < 2:
            messagebox.showwarning("Kļūda", "Nepietiek produkta ievārījumam!")
            return

        # Samazina daudzumu un pievieno ievārījumu
        jam_amount = product["quantity"] // 2
        self.pantry[index]["quantity"] -= jam_amount * 2
        if self.pantry[index]["quantity"] == 0:
            self.pantry.pop(index)
        
        jam_name = f"Ievārījums - {product['name']}"
        self.pantry.append({"name": jam_name, "quantity": jam_amount, "type": "Ievārījums", "variety": ""})
        
        self.update_pantry_listbox()

    def update_pantry_listbox(self):
        # Atjauno pieliekamā sarakstu
        self.pantry_listbox.delete(0, tk.END)
        for item in self.pantry:
            entry = f"{item['name']} ({item['quantity']} kg) [{item['type']}]"
            self.pantry_listbox.insert(tk.END, entry)

# Izveido aplikāciju
root = tk.Tk()
app = GrandmaPantryApp(root)
root.mainloop()
