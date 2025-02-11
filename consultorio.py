import tkinter as tk
from tkinter import ttk, Scrollbar, messagebox, filedialog
import sqlite3
import os
import shutil

historia_clinica_fields = {}

def setup_database():
    db_path = os.path.join(os.path.dirname(__file__), "consultorio.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS consultorio (
            dni TEXT PRIMARY KEY,
            nombre_apellido TEXT NOT NULL,
            telefono TEXT NOT NULL,
            obra_social TEXT NOT NULL,
            juzgado_civil TEXT,
            expediente_numero TEXT,
            autos TEXT,
            abogado_demanda TEXT,
            abogado_demandada TEXT,
            consultor_tecnico TEXT,
            fecha_examen_pericial TEXT,
            hora_examen_pericial TEXT,
            fecha_hecho TEXT,
            hora_hecho TEXT,
            estado_civil TEXT,
            fecha_nacimiento TEXT,
            edad INTEGER,
            domicilio TEXT,
            trabajo_anterior_hecho TEXT,
            dias_reposo INTEGER,
            trabajo_posterior_hecho TEXT,
            estudios TEXT,
            lado_dominante TEXT,
            deportes_antes TEXT,
            deportes_despues TEXT,
            peso REAL,
            talla REAL,
            art TEXT,
            accidentes_previos TEXT,
            medicacion_actual TEXT,
            cobertura_medica TEXT,
            atencion_medica_luego_accidente TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("Base de datos configurada correctamente.")

def load_data(turnos_tree):
    for item in turnos_tree.get_children():
        turnos_tree.delete(item)

    db_path = os.path.join(os.path.dirname(__file__), "consultorio.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT dni, nombre_apellido, telefono, obra_social, expediente_numero FROM consultorio")
    rows = cursor.fetchall()

    for row in rows:
        turnos_tree.insert("", "end", values=row)

    conn.close()

def add_turno(turnos_tree):
    def save_turno():
        datos = {
            "dni": dni_entry.get(),
            "nombre": nombre_entry.get(),
            "telefono": telefono_entry.get(),
            "obra_social": obra_social_entry.get(),
        }

        if not all(datos.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        db_path = os.path.join(os.path.dirname(__file__), "consultorio.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO consultorio (dni, nombre_apellido, telefono, obra_social)
                VALUES (:dni, :nombre, :telefono, :obra_social)
            ''', datos)

            conn.commit()
            messagebox.showinfo("Éxito", "Turno añadido correctamente.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al guardar los datos: {e}")
        finally:
            conn.close()
            load_data(turnos_tree)
            add_window.destroy()

    add_window = tk.Toplevel()
    add_window.title("Agregar historial clinico")
    add_window.geometry("400x300")

    tk.Label(add_window, text="DNI:").pack(pady=5)
    dni_entry = tk.Entry(add_window)
    dni_entry.pack(pady=5)

    tk.Label(add_window, text="Nombre y Apellido:").pack(pady=5)
    nombre_entry = tk.Entry(add_window)
    nombre_entry.pack(pady=5)

    tk.Label(add_window, text="Teléfono:").pack(pady=5)
    telefono_entry = tk.Entry(add_window)
    telefono_entry.pack(pady=5)

    tk.Label(add_window, text="Obra Social:").pack(pady=5)
    obra_social_entry = tk.Entry(add_window)
    obra_social_entry.pack(pady=5)

    tk.Button(add_window, text="Guardar", command=save_turno).pack(pady=10)
    tk.Button(add_window, text="Cancelar", command=add_window.destroy).pack(pady=5)

def actualizar_datos(turnos_tree):
    load_data(turnos_tree)
    
def delete_turno(turnos_tree):
    selected_item = turnos_tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Por favor, seleccione un turno para eliminar.")
        return

    dni = turnos_tree.item(selected_item)['values'][0]

    confirm = messagebox.askyesno("Confirmar", f"¿Está seguro de que desea eliminar el turno con DNI: {dni}?")
    if confirm:
        db_path = os.path.join(os.path.dirname(__file__), "consultorio.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM consultorio WHERE dni = ?", (dni,))
        conn.commit()
        conn.close()
        load_data(turnos_tree)

def edit_turno(turnos_tree):
    selected_item = turnos_tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Por favor, seleccione un turno para editar.")
        return

    dni, nombre, telefono, obra_social = turnos_tree.item(selected_item)['values']

    def save_changes():
        new_dni = dni_entry.get()
        new_nombre = nombre_entry.get()
        new_telefono = telefono_entry.get()
        new_obra_social = obra_social_entry.get()

        if not all([new_dni, new_nombre, new_telefono, new_obra_social]):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        db_path = os.path.join(os.path.dirname(__file__), "consultorio.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE consultorio SET dni = ?, nombre_apellido = ?, telefono = ?, obra_social = ? WHERE dni = ?",
                       (new_dni, new_nombre, new_telefono, new_obra_social, dni))
        conn.commit()
        conn.close()
        load_data(turnos_tree)
        edit_window.destroy()

    edit_window = tk.Toplevel()
    edit_window.title("Editar historal clínico")
    edit_window.geometry("400x400")

    tk.Label(edit_window, text="DNI:").pack(pady=5)
    dni_entry = tk.Entry(edit_window)
    dni_entry.insert(0, dni)
    dni_entry.pack(pady=5)

    tk.Label(edit_window, text="Nombre y Apellido:").pack(pady=5)
    nombre_entry = tk.Entry(edit_window)
    nombre_entry.insert(0, nombre)
    nombre_entry.pack(pady=5)

    tk.Label(edit_window, text="Teléfono:").pack(pady=5)
    telefono_entry = tk.Entry(edit_window)
    telefono_entry.insert(0, telefono)
    telefono_entry.pack(pady=5)

    tk.Label(edit_window, text="Obra Social:").pack(pady=5)
    obra_social_entry = tk.Entry(edit_window)
    obra_social_entry.insert(0, obra_social)
    obra_social_entry.pack(pady=5)

    tk.Button(edit_window, text="Guardar Cambios", command=save_changes).pack(pady=10)
    tk.Button(edit_window, text="Cancelar", command=edit_window.destroy).pack(pady=5)

def open_datos(turnos_tree):
    
    selected_item = turnos_tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Por favor, seleccione un turno para ver los datos.")
        return

    dni = turnos_tree.item(selected_item)['values'][0]

    def load_formulario_data(dni):
        db_path = os.path.join(os.path.dirname(__file__), "consultorio.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM consultorio WHERE dni = ?", (dni,))
            data = cursor.fetchone()
            
            if data:
                for (field, value) in zip(historia_clinica_fields.keys(), data):
                    historia_clinica_fields[field].config(state="normal")
                    historia_clinica_fields[field].delete(0, tk.END)
                    historia_clinica_fields[field].insert(0, str(value) if value is not None else "")
                    historia_clinica_fields[field].config(state="readonly")
            else:
                messagebox.showinfo("Información", "No se encontró información para este turno.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos: {e}")
        finally:
            conn.close()

    form_window = tk.Toplevel()
    form_window.title(f"Formulario - DNI: {dni}")
    form_window.geometry("600x400")

    form_frame = tk.Frame(form_window)
    form_frame.pack(fill=tk.BOTH, expand=True)

    global historia_clinica_fields
    historia_clinica_fields = {}
    labels = []
    for idx, label_text in enumerate(labels):
        label = tk.Label(form_frame, text=label_text)
        label.grid(row=idx, column=0, padx=10, pady=5)
        entry = tk.Entry(form_frame, state="readonly")
        entry.grid(row=idx, column=1, padx=10, pady=5)
        historia_clinica_fields[label_text] = entry

    load_formulario_data(dni)
    
def buscar_historia(turnos_tree):
    def aplicar_busqueda():
        criterio = entry_busqueda.get().strip()

        if not criterio:
            messagebox.showerror("Error", "Por favor, ingrese un criterio de búsqueda.")
            return

        filtros = """
            juzgado_civil LIKE ? OR 
            nombre_apellido LIKE ? OR 
            dni LIKE ? OR 
            abogado_demanda LIKE ? OR 
            abogado_demandada LIKE ? OR 
            expediente_numero LIKE ?
        """
        valores = [f"%{criterio}%"] * 6

        db_path = os.path.join(os.path.dirname(__file__), "consultorio.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        try:
            query = f"SELECT dni, nombre_apellido, telefono, obra_social FROM consultorio WHERE {filtros}"
            cursor.execute(query, valores)
            rows = cursor.fetchall()

            for item in turnos_tree.get_children():
                turnos_tree.delete(item)
            for row in rows:
                turnos_tree.insert("", "end", values=row)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudieron aplicar los filtros: {e}")
        finally:
            conn.close()
            buscar_window.destroy()

    buscar_window = tk.Toplevel()
    buscar_window.title("Buscar Historias Clínicas")
    buscar_window.geometry("400x200")

    tk.Label(buscar_window, text="Ingrese criterio de búsqueda:").pack(pady=10)
    entry_busqueda = tk.Entry(buscar_window, width=50)
    entry_busqueda.pack(pady=5)

    tk.Button(buscar_window, text="Buscar", command=aplicar_busqueda).pack(pady=10)
    tk.Button(buscar_window, text="Cerrar", command=buscar_window.destroy).pack(pady=5)

def cargar_archivos_existentes(nombre_apellido, listbox):

    listbox.delete(0, tk.END)

    carpeta_principal = os.path.join(os.path.dirname(__file__), "archivos")
    subcarpeta = os.path.join(carpeta_principal, nombre_apellido)

    if os.path.exists(subcarpeta):
        for archivo in os.listdir(subcarpeta):
            listbox.insert(tk.END, archivo)

def manage_historia_clinica(turnos_tree, event=None):
    
    def load_data(dni):
        db_path = os.path.join(os.path.dirname(__file__), "consultorio.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM consultorio WHERE dni = ?", (dni,))
            data = cursor.fetchone()

            if data:
                column_names = [description[0] for description in cursor.description]

                for label, field, _, _ in labels_fields:
                    if field in column_names:
                        value = data[column_names.index(field)]
                        if field in historia_clinica_fields:
                            historia_clinica_fields[field].config(state="normal")
                            historia_clinica_fields[field].delete(0, tk.END)
                            historia_clinica_fields[field].insert(0, str(value) if value is not None else "")
                            historia_clinica_fields[field].config(state="readonly")
            else:
                messagebox.showinfo("Información", "No se encontró información para este DNI.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos: {e}")
        finally:
            conn.close()
            
    def save_historia():
        
        global historia_clinica_fields

        data = {field: historia_clinica_fields[field].get() for field in historia_clinica_fields}

        non_empty_fields = {key: value for key, value in data.items() if value.strip()}

        if 'dni' not in non_empty_fields:
            messagebox.showerror("Error", "El campo DNI es obligatorio.")
            return

        db_path = os.path.join(os.path.dirname(__file__), "consultorio.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT 1 FROM consultorio WHERE dni = ?", (non_empty_fields['dni'],))
            exists = cursor.fetchone() is not None

            if exists:
                update_fields = ", ".join([f"{key} = :{key}" for key in non_empty_fields if key != 'dni'])
                query = f"UPDATE consultorio SET {update_fields} WHERE dni = :dni"
                cursor.execute(query, non_empty_fields)
            else:
                placeholders = ", ".join([f":{key}" for key in non_empty_fields])
                columns = ", ".join(non_empty_fields.keys())
                query = f"INSERT INTO consultorio ({columns}) VALUES ({placeholders})"
                cursor.execute(query, non_empty_fields)

            conn.commit()
            historia_window.destroy()
            messagebox.showinfo("Éxito", "Historia clínica guardada correctamente.")
        except sqlite3.Error as e:
            historia_window.destroy()
            messagebox.showerror("Error", f"Error al guardar los datos: {e}")
        finally:
            conn.close()

    def enable_editing():
        for field in historia_clinica_fields.values():
            field.config(state="normal")
        save_button.config(state="normal")
        edit_button.config(state="disabled")

    def disable_editing():
        for field in historia_clinica_fields.values():
            field.config(state="readonly")
        save_button.config(state="disabled")
        edit_button.config(state="normal")

    historia_window = tk.Toplevel()
    historia_window.title("Historia Clínica")
    historia_window.geometry("900x1200")
    historia_window.resizable(False, False)

    main_frame = tk.Frame(historia_window)
    main_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(main_frame)
    scrollbar = Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    labels_fields = [
        ("Juzgado Civil:", "juzgado_civil", 0, 0),
        ("Expediente N°:", "expediente_numero", 0, 2),
        ("Autos:", "autos", 1, 0),
        ("Abogado demanda:", "abogado_demanda", 2, 0),
        ("Abogado demandada:", "abogado_demandada", 3, 0),
        ("Consultor Técnico:", "consultor_tecnico", 4, 0),
        ("Fecha de examen pericial:", "fecha_examen_pericial", 5, 0),
        ("Hora:", "hora_examen_pericial", 5, 2),
        ("Fecha del hecho:", "fecha_hecho", 6, 0),
        ("Hora:", "hora_hecho", 6, 2),
        ("Nombre y apellido:", "nombre_apellido", 7, 0),
        ("Estado civil:", "estado_civil", 7, 2),
        ("N° DNI:", "dni", 8, 0),
        ("T.E:", "telefono", 8, 2),
        ("Fecha de nacimiento:", "fecha_nacimiento", 9, 0),
        ("Edad:", "edad", 9, 2),
        ("Domicilio:", "domicilio", 10, 0),
        ("Trabajo anterior al hecho:", "trabajo_anterior_hecho", 11, 0),
        ("Días de reposo:", "dias_reposo", 12, 0),
        ("Trabajo posterior al hecho:", "trabajo_posterior_hecho", 13, 0),
        ("Estudios:", "estudios", 14, 0),
        ("Lado dominante:", "lado_dominante", 15, 0),
        ("Deportes Antes:", "deportes_antes", 16, 0),
        ("Deportes Después:", "deportes_despues", 16, 2),
        ("Peso:", "peso", 17, 0),
        ("Talla:", "talla", 17, 2),
        ("ART:", "art", 18, 0),
        ("Accidentes previos:", "accidentes_previos", 19, 0),
        ("Medicación actual:", "medicacion_actual", 20, 0),
        ("Cobertura Médica:", "cobertura_medica", 21, 0),
        ("Atención médica luego del accidente:", "atencion_medica_luego_accidente", 22, 0),
    ]
    
    global historia_clinica_fields
    historia_clinica_fields = {}
    for label_text, field_name, row, col in labels_fields:
        label = tk.Label(scrollable_frame, text=label_text, anchor="w")
        label.grid(row=row, column=col, padx=10, pady=5, sticky="w")
        entry = tk.Entry(scrollable_frame, state="readonly", width=30)
        entry.grid(row=row, column=col + 1, padx=10, pady=5, sticky="w")
        historia_clinica_fields[field_name] = entry
        
    selected_item = turnos_tree.selection()
    if selected_item:
        dni = turnos_tree.item(selected_item)['values'][0]
        load_data(dni)
        
    button_frame = tk.Frame(historia_window)
    button_frame.place(relx=1.0, rely=0.0, anchor="ne")

    edit_button = tk.Button(button_frame, text="EDITAR", command=enable_editing)
    edit_button.pack(side="right", padx=10, pady=10)

    save_button = tk.Button(button_frame, text="GUARDAR", command=save_historia, state="disabled")
    save_button.pack(side="right", padx=10, pady=10)
    
    cargar_archivos_button = ttk.Button(scrollable_frame, text="Cargar Archivos", command=lambda: cargar_archivos(archivos_listbox))
    cargar_archivos_button.grid(row=18, column=2, pady=(10, 0), sticky="w", columnspan=2)

    ttk.Label(scrollable_frame, text="Archivos:").grid(row=19, column=2, pady=(10, 0), sticky="w", columnspan=2)

    archivos_listbox = tk.Listbox(scrollable_frame, height=10, width=50)
    archivos_listbox.grid(row=20, column=2, columnspan=2, rowspan=20, pady=(0, 10), padx=10, sticky="w")

    archivos = []

    def cargar_archivos(listbox):
        selected_item = turnos_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, seleccione un turno para cargar archivos.")
            return

        nombre_apellido = turnos_tree.item(selected_item)['values'][1]
        carpeta_principal = os.path.join(os.path.dirname(__file__), "archivos")
        subcarpeta = os.path.join(carpeta_principal, nombre_apellido)

        if not os.path.exists(subcarpeta):
            os.makedirs(subcarpeta)

        archivos = filedialog.askopenfilenames(title="Seleccionar Archivos", 
                                                filetypes=[("Archivos PDF", "*.pdf"), 
                                                           ("Documentos Word", "*.docx"), 
                                                           ("Imágenes JPG", "*.jpg;*.jpeg"),
                                                           ("Imágenes PNG", "*.png"),
                                                            ("Archivos de Texto", "*.txt"),
                                                            ("Archivos ZIP", "*.zip"),
                                                            ("Archivos de Excel", "*.xlsx"),
                                                            ("Archivos de PowerPoint", "*.pptx")
                                                           ])

        for archivo in archivos:
            shutil.copy(archivo, subcarpeta)
        cargar_archivos_existentes(nombre_apellido, listbox)
    def abrir_archivo(listbox):
        seleccion = listbox.curselection()
        if seleccion:
            archivo_seleccionado = listbox.get(seleccion[0])
            nombre_apellido = turnos_tree.item(turnos_tree.selection()[0])['values'][1]
            carpeta_principal = os.path.join(os.path.dirname(__file__), "archivos")
            subcarpeta = os.path.join(carpeta_principal, nombre_apellido)
            ruta_archivo = os.path.join(subcarpeta, archivo_seleccionado)

            try:
                os.startfile(ruta_archivo)
            except Exception as e:
                messagebox.showerror("Error", f"No se puede abrir el archivo: {e}")

    archivos_listbox.bind("<Double-1>", lambda event: abrir_archivo(archivos_listbox))
    
    selected_item = turnos_tree.selection()
    if selected_item:
        dni = turnos_tree.item(selected_item)['values'][0]
        load_data(dni)

    cargar_archivos_existentes(turnos_tree.item(selected_item)['values'][1], archivos_listbox)
    
    disable_editing()

def create_gui():
    root = tk.Tk()
    root.title("SIGEP")
    root.geometry("900x500")

    nav_frame = tk.Frame(root, relief=tk.RAISED, bd=2)
    nav_frame.pack(fill=tk.X, side=tk.TOP)

    buttons = [("Agregar", lambda: add_turno(turnos_tree)),
               ("Eliminar", lambda: delete_turno(turnos_tree)),
               ("Editar", lambda: edit_turno(turnos_tree)),
               ("Buscar", lambda: buscar_historia(turnos_tree)),
               ("Datos", lambda: manage_historia_clinica(turnos_tree)),
               ("Actualizar", lambda: actualizar_datos(turnos_tree))]

    for text, command in buttons:
        btn = tk.Button(nav_frame, text=text, padx=10, pady=5, command=command)
        btn.pack(side=tk.LEFT, padx=5, pady=5)

    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    upcoming_frame = tk.LabelFrame(main_frame, text="HISTORIA CLINICA", width=400, height=400)
    upcoming_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Próximos turnos (lista)
    turnos_tree = ttk.Treeview(upcoming_frame, columns=("DNI", "Nombre y Apellido", "Teléfono", "Obra Social", "N° de expediente"), show="headings")
    turnos_tree.heading("DNI", text="DNI")
    turnos_tree.heading("Nombre y Apellido", text="Nombre y Apellido")
    turnos_tree.heading("Teléfono", text="Teléfono")
    turnos_tree.heading("Obra Social", text="Obra Social")
    turnos_tree.heading("N° de expediente", text="N° de expediente")
    turnos_tree.pack(fill=tk.BOTH, expand=True)
    
    turnos_tree.column("DNI", anchor='center')
    turnos_tree.column("Nombre y Apellido", anchor='center')
    turnos_tree.column("Teléfono", anchor='center')
    turnos_tree.column("Obra Social", anchor='center')
    turnos_tree.column("N° de expediente", anchor='center')

    load_data(turnos_tree)

    root.mainloop()

if __name__ == "__main__":
    setup_database()
    create_gui()
