import tkinter as tk
from tkinter import messagebox, filedialog

# ================== PRODUCT DATABASE ==================
items = {
    "rice": {"price": 500, "unit": "cup"},
    "beans": {"price": 700, "unit": "cup"},
    "bread": {"price": 350, "unit": "loaf"},
    "milk": {"price": 1000, "unit": "carton"},
    "eggs": {"price": 150, "unit": "egg"},
    "oil": {"price": 1200, "unit": "bottle"},
    "sugar": {"price": 400, "unit": "kg"},
    "salt": {"price": 200, "unit": "pack"},
    "indomie": {"price": 150, "unit": "pack"},
    "tomato": {"price": 100, "unit": "piece"}
}

cart = []

# ================== FUNCTIONS ==================
def show_available_items():
    text = "🛒 AVAILABLE ITEMS\n\n"
    for item, info in items.items():
        text += f"✔ {item.title()} — ₦{info['price']} per {info['unit']}\n"
    available_label.config(text=text)

def show_unit_prices(event=None):
    def check():
        raw = item_entry.get().strip().lower()
        if not raw:
            unit_price_label.config(text="")
            return

        names = [n.strip() for n in raw.split(",") if n.strip()]
        lines = []

        for name in names:
            if name in items:
                info = items[name]
                lines.append(f"{name.title()}: ₦{info['price']} per {info['unit']}")
            else:
                lines.append(f"{name.title()}: ❌ Item not found")

        unit_price_label.config(text="\n".join(lines))

    root.after_cancel(getattr(root, "_timer", None))
    root._timer = root.after(500, check)

def add_items():
    names = [n.strip().lower() for n in item_entry.get().split(",") if n.strip()]
    qtys = [q.strip() for q in quantity_entry.get().split(",") if q.strip()]

    if len(names) != len(qtys):
        messagebox.showerror("Error", "Items and quantities must match.")
        return

    for name, qty in zip(names, qtys):
        if name not in items:
            messagebox.showwarning("Not Found", f"{name} is not available.")
            continue
        try:
            qty = int(qty)
            if qty <= 0:
                raise ValueError
            cart.append((name, qty))
        except ValueError:
            messagebox.showerror("Error", f"Invalid quantity for {name}")
            return

    update_receipt()
    item_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    unit_price_label.config(text="")

def update_receipt():
    receipt_text.delete("1.0", tk.END)
    receipt_text.insert(tk.END, "🧾 SUPERMARKET RECEIPT\n")
    receipt_text.insert(tk.END, "-" * 45 + "\n")

    for name, qty in cart:
        price = items[name]["price"]
        unit = items[name]["unit"]
        cost = price * qty
        receipt_text.insert(
            tk.END,
            f"{name.title()} ({qty} {unit}(s) @ ₦{price}) = ₦{cost}\n"
        )

def checkout():
    if not cart:
        messagebox.showinfo("Empty", "No items added.")
        return

    total = sum(items[n]["price"] * q for n, q in cart)
    receipt_text.insert(tk.END, "-" * 45 + "\n")
    receipt_text.insert(tk.END, f"💰 TOTAL AMOUNT: ₦{total}\n")

    # Show print button only AFTER checkout
    print_btn.place(relx=1.0, rely=1.0, anchor="se", x=-15, y=-15)

def clear_all():
    cart.clear()
    receipt_text.delete("1.0", tk.END)
    unit_price_label.config(text="")
    item_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    print_btn.place_forget()

def print_receipt():
    content = receipt_text.get("1.0", tk.END).strip()
    if not content:
        messagebox.showwarning("No Receipt", "Nothing to print.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")],
        title="Save Receipt"
    )
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("Success", "Receipt saved successfully!")

# ================== GUI ==================
root = tk.Tk()
root.title("Supermarket Billing System")
root.geometry("760x900")
root.config(bg="#eef2ff")

tk.Label(
    root,
    text="🛒 Supermarket Billing Application",
    font=("Segoe UI", 22, "bold"),
    bg="#eef2ff",
    fg="#1e3a8a"
).pack(pady=10)

available_label = tk.Label(
    root,
    font=("Segoe UI", 11, "bold"),
    bg="#dbeafe",
    fg="#1e40af",
    justify="left",
    relief="ridge",
    bd=3,
    padx=15,
    pady=15
)
available_label.pack(pady=10, fill="x", padx=25)

tk.Label(root, text="Enter item names (comma-separated):",
         bg="#eef2ff", font=("Segoe UI", 11)).pack()
item_entry = tk.Entry(root, width=60, font=("Segoe UI", 12))
item_entry.pack(pady=4)
item_entry.bind("<KeyRelease>", show_unit_prices)

unit_price_label = tk.Label(
    root, bg="#eef2ff", fg="#0f766e",
    font=("Segoe UI", 11, "italic"),
    justify="left"
)
unit_price_label.pack()

tk.Label(root, text="Enter quantities (comma-separated):",
         bg="#eef2ff", font=("Segoe UI", 11)).pack()
quantity_entry = tk.Entry(root, width=60, font=("Segoe UI", 12))
quantity_entry.pack(pady=4)

tk.Button(root, text="➕ Add Items", command=add_items,
          bg="#2563eb", fg="white", width=24,
          font=("Segoe UI", 11, "bold")).pack(pady=8)

tk.Button(root, text="✅ Checkout", command=checkout,
          bg="#16a34a", fg="white", width=24,
          font=("Segoe UI", 11, "bold")).pack()

tk.Button(root, text="🗑 Clear All", command=clear_all,
          bg="#dc2626", fg="white", width=24,
          font=("Segoe UI", 11, "bold")).pack(pady=6)

# ================== RECEIPT BOX ==================
receipt_frame = tk.Frame(root, bg="white", bd=2, relief="solid")
receipt_frame.pack(padx=25, pady=15, fill="both", expand=True)

receipt_text = tk.Text(
    receipt_frame,
    font=("Courier New", 11),
    wrap="word"
)
receipt_text.pack(fill="both", expand=True, padx=10, pady=10)

print_btn = tk.Button(
    receipt_frame,
    text="🖨 Print Receipt",
    command=print_receipt,
    bg="#9333ea",
    fg="white",
    font=("Segoe UI", 10, "bold")
)
print_btn.place_forget()  # hidden until checkout

show_available_items()
root.mainloop()