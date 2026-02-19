import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

def iniciar_db():
    conn = sqlite3.connect("finanzas.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS registros 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       ingresos REAL, 
                       gastos REAL, 
                       fecha TEXT)''')
    conn.commit()
    conn.close()

def guardar_datos():
    try:
        ing = float(entry_ingresos.get())
        gas = float(entry_gastos.get())

        # Obtener fecha y hora actual
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = sqlite3.connect("finanzas.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO registros (ingresos, gastos, fecha) VALUES (?, ?, ?)", 
                       (ing, gas, fecha_actual))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", f"Datos guardados el {fecha_actual}")
        entry_ingresos.delete(0, tk.END)
        entry_gastos.delete(0, tk.END)

        actualizar_resumen()
        mostrar_registros()

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa números válidos")

def actualizar_resumen():
    conn = sqlite3.connect("finanzas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(ingresos), SUM(gastos) FROM registros")
    totales = cursor.fetchone()
    conn.close()

    t_ingresos = totales[0] if totales[0] else 0
    t_gastos = totales[1] if totales[1] else 0
    balance = t_ingresos - t_gastos

    lbl_resumen_ing.config(text=f"Total Ingresos: ${t_ingresos:,.2f}")
    lbl_resumen_gas.config(text=f"Total Gastos: ${t_gastos:,.2f}")
    lbl_balance.config(text=f"Balance Final: ${balance:,.2f}")

    if balance > 0:
        lbl_status.config(text="Estado: Ganancias", foreground="green")
    elif balance < 0:
        lbl_status.config(text="Estado: Pérdidas", foreground="red")
    else:
        lbl_status.config(text="Estado: En cero", foreground="black")

def mostrar_registros():
    for fila in tree.get_children():
        tree.delete(fila)

    conn = sqlite3.connect("finanzas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT fecha, ingresos, gastos FROM registros ORDER BY id DESC")
    datos = cursor.fetchall()
    conn.close()

    for registro in datos:
        tree.insert("", tk.END, values=registro)

# ================= INTERFAZ =================

root = tk.Tk()
root.title("Control de Finanzas Semanales")
root.geometry("500x550")

iniciar_db()

main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill="both", expand=True)

ttk.Label(main_frame, text="REGISTRO DIARIO", font=("Arial", 14, "bold")).pack(pady=10)

ttk.Label(main_frame, text="Ingresos del día:").pack()
entry_ingresos = ttk.Entry(main_frame)
entry_ingresos.pack(pady=5)

ttk.Label(main_frame, text="Gastos del día:").pack()
entry_gastos = ttk.Entry(main_frame)
entry_gastos.pack(pady=5)

ttk.Button(main_frame, text="Guardar Registro", command=guardar_datos).pack(pady=15)

ttk.Separator(main_frame, orient="horizontal").pack(fill="x", pady=10)

ttk.Label(main_frame, text="RESUMEN ACUMULADO", font=("Arial", 12, "bold")).pack()
lbl_resumen_ing = ttk.Label(main_frame, text="Total Ingresos: $0.00")
lbl_resumen_ing.pack()
lbl_resumen_gas = ttk.Label(main_frame, text="Total Gastos: $0.00")
lbl_resumen_gas.pack()
lbl_balance = ttk.Label(main_frame, text="Balance Final: $0.00", font=("Arial", 10, "bold"))
lbl_balance.pack(pady=5)
lbl_status = ttk.Label(main_frame, text="Estado: -")
lbl_status.pack()

ttk.Separator(main_frame, orient="horizontal").pack(fill="x", pady=10)

# Tabla de registros
ttk.Label(main_frame, text="HISTORIAL DE REGISTROS", font=("Arial", 12, "bold")).pack()

columnas = ("Fecha y Hora", "Ingresos", "Gastos")
tree = ttk.Treeview(main_frame, columns=columnas, show="headings")
for col in columnas:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

tree.pack(fill="both", expand=True, pady=10)

actualizar_resumen()
mostrar_registros()

root.mainloop()
