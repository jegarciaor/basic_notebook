# Librerías externas.
import customtkinter
import tkinter as tk
from pathlib import Path
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename


class EditorTexto:
    """Al crear la clase EditorTexto, indicamos que es heredada de la clase
    CTk, por lo cual puedo usar sus métodos.

    Lo primero que hago es crear el constructor de mi clase EditorTexto.

    La ventana principal tendrá un ancho de 900px y largo de 500px.

    La fuente está inspirada en Notepad++, donde se usa courier new, que emula
    la fuente de una máquina de escribir.
    """

    def __init__(self):
        self.archivo_actual = None
        self.file_path = None
        self.ventana_principal = tk.Tk()
        self.ventana_principal.title("Editor básico de texto")
        self.ventana_principal.geometry("900x500+400+52")
        self.fuente = customtkinter.CTkFont("Courier New", 16)

        self.formatos = [("Archivos de texto", "*.txt"),
                         ("Todos los archivos", "*")]

        #                           Menú superior
        self.menu_superior = tk.Menu(master=self.ventana_principal)
        self.ventana_principal.config(menu=self.menu_superior)

        # Creación de los distintos submenús.
        self.menu_archivo = tk.Menu(master=self.menu_superior, tearoff=0)
        self.menu_editar = tk.Menu(master=self.menu_superior, tearoff=0)

        # Agregamos opciones principales.
        self.menu_superior.add_cascade(label="Archivo", menu=self.menu_archivo)
        self.menu_superior.add_cascade(label="Editar", menu=self.menu_editar)

        # Agregamos las opciones desplegables en el menú archivo.
        self.menu_archivo.add_command(label="Nuevo", command=self.nuevo_archivo)

        self.menu_archivo.add_command(
            label="Abrir", command=self.abrir_archivo, accelerator="Ctrl+O")

        self.menu_archivo.add_command(
            label="Guadar", command=self.guardar, accelerator="Ctrl+S")

        self.menu_archivo.add_command(
            label="Guadar como", command=self.guardar_como)

        self.menu_archivo.add_separator()
        self.menu_archivo.add_command(
            label="Salir", command=self.cerrar_ventana, accelerator="Ctrl+W")

        # Agregamos las opciones desplegables en el menú editar.
        self.menu_editar.add_command(label="Deshacer")

        self.menu_editar.add_separator()

        self.menu_editar.add_command(
            label="Cortar", command=self.cortar_texto, accelerator="Ctrl+X")
        self.menu_editar.add_command(
            label="Copiar", command=self.copiar_texto, accelerator="Ctrl+C")
        self.menu_editar.add_command(
            label="Pegar", command=self.pegar_texto, accelerator="Ctrl+V")

        # Creación del cuadro de texto para escribir.
        self.cuadro_texto = customtkinter.CTkTextbox(
            master=self.ventana_principal, width=900, height=500,
            corner_radius=0, font=self.fuente, border_spacing=8)

        self.cuadro_texto.grid(row=0, column=0, sticky="nsew")

        # Creamos shorcuts.
        self.ventana_principal.bind(
            "<Control-o>", lambda x: self.abrir_archivo())

        self.ventana_principal.bind(
            "<Control-w>", lambda x: self.ventana_principal.destroy())
        self.ventana_principal.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

    def cerrar_ventana(self) -> None:
        if not self.continuar():
            return
        self.ventana_principal.destroy()

    def set_archivo_actual(self, archivo_actual: Path):
        self.archivo_actual = archivo_actual
        self.ventana_principal.title(
            self.archivo_actual.name + " - EditorTexto")

    def continuar(self):
        if self.cuadro_texto.edit_modified():
            resultado = messagebox.askyesnocancel(
                title="Cambios sin guardar", message="¿Desea guardarlos?")

            cancelar = resultado is None
            guardar_antes = resultado is True

            if cancelar:
                return False
            elif guardar_antes:
                self.guardar()
            return True
        return True

    def nuevo_archivo(self):
        if not self.continuar():
            return
        self.cuadro_texto.delete("1.0", tk.END)
        self.archivo_actual = None
        self.ventana_principal.title("EditorTexto")

    def abrir_archivo(self):

        nombre_archivo = askopenfilename(filetypes=self.formatos)

        if not nombre_archivo or not self.continuar():
            return

        self.cuadro_texto.delete("1.0", tk.END)
        archivo = Path(nombre_archivo)
        self.cuadro_texto.insert("1.0", archivo.read_text("utf8"))

        self.cuadro_texto.edit_modified(False)
        self.set_archivo_actual(archivo)

    def guardar_archivo_actual(self):
        if self.archivo_actual is None:
            return
        self.archivo_actual.write_text(self.cuadro_texto.get(
            "1.0", tk.END), "utf8")

    def guardar(self):
        if self.archivo_actual is None:
            self.guardar_como()
            return
        self.guardar_archivo_actual()

    def guardar_como(self):
        nombre_archivo = asksaveasfilename(
            defaultextension=".txt", filetypes=self.formatos)
        if not nombre_archivo:
            self.set_archivo_actual(Path(nombre_archivo))
            self.guardar_archivo_actual()

    def cortar_texto(self):
        try:
            texto_seleccionado = self.cuadro_texto.get(
                tk.SEL_FIRST, tk.SEL_LAST)
            self.cuadro_texto.delete(tk.SEL_FIRST, tk.SEL_LAST)
            self.ventana_principal.clipboard_clear()
            self.ventana_principal.clipboard_append(texto_seleccionado)
        except:
            texto_seleccionado = ""

    def copiar_texto(self):
        try:
            texto_seleccionado = self.cuadro_texto.get(
                tk.SEL_FIRST, tk.SEL_LAST)
            self.ventana_principal.clipboard_clear()
            self.ventana_principal.clipboard_append(texto_seleccionado)
        except:
            texto_seleccionado = ""

    def pegar_texto(self):
        try:
            texto_a_pegar = self.ventana_principal.clipboard_get()
            self.cuadro_texto.insert(tk.INSERT, texto_a_pegar)
        except:
            texto_a_pegar = ""
