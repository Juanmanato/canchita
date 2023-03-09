
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
import sqlite3
import re
import random


# base datos inicio

def conexion():
   conexion = sqlite3.connect("canchita.db")
   return conexion

def crear_tabla_datos():
    conectar = conexion()
    cursor = conectar.cursor()
    tabla = """CREATE TABLE turnos(id INTEGER PRIMARY KEY AUTOINCREMENT, \
                     nombre varchar(64) NOT NULL, \
                     apellido varchar(64) NOT NULL, \
                     tipo_reserva varchar(64) NOT NULL, \
                     estado varchar(64) NOT NULL, \
                     fecha varchar(64) NOT NULL, \
                     horario varchar(64) NOT NULL)
                     """
    cursor.execute(tabla)
    conectar.commit()

try:
    conexion()
    crear_tabla_datos()
except:
    print("Hay un error")

#funciones para manejar los datos de la base de datos

def limpiar_campos_entradas():
    var_nombre.set(""), var_apellido.set(""), var_tipo_reserva.set("") ,var_estado.set("") ,\
            var_fecha.set("") , var_horario.set("")

   
def traer_datos_entradas():
    valores = mostrar_turnos.selection()
    item = mostrar_turnos.item(valores)
    data = item['values']

    print(data)
    var_nombre.set(data[0]), var_apellido.set(data[1]), var_tipo_reserva.set(data[2]) ,var_estado.set(data[3]) ,\
            var_fecha.set(data[4]) , var_horario.set(data[5])
    showinfo("Modificar", "Ahora puede modificar los campos y presionar el botón Guardar cambios")



def nuevo_turno():
    nombre, apellido, tipo_reserva, estado, fecha, horario = var_nombre.get(),\
          var_apellido.get(), var_tipo_reserva.get() ,var_estado.get() ,\
            var_fecha.get() , var_horario.get()
    
    patron_re="^[A-Za-záéíóú]"
    if (re.match(patron_re, nombre) or re.match(patron_re, apellido)):
        
        conectar = conexion()
        cursor = conectar.cursor()
        datos=(nombre, apellido, tipo_reserva, estado, fecha, horario)
        sql = "INSERT INTO turnos(nombre, apellido, tipo_reserva, estado, fecha, horario) VALUES (?, ?, ?, ?, ?, ?)"
        cursor.execute(sql, datos)
        conectar.commit()
        print("datos: ", datos)
        actualizar_treeview()
        limpiar_campos_entradas()
        showinfo("Mensaje", "El turno se ha guardado exitosamente")
    else:
        showinfo("Error", "Solo usar letras en los campos de Nombre y Apellido")
        print("error")


def modificar_turno():
    
    nombre, apellido, tipo_reserva, estado, fecha, horario = var_nombre.get(),\
          var_apellido.get(), var_tipo_reserva.get() ,var_estado.get() ,\
            var_fecha.get() , var_horario.get()
    print(nombre, apellido, tipo_reserva, estado, fecha, horario)
    
    valor_id = mostrar_turnos.selection()
    item_id = mostrar_turnos.item(valor_id)
    data_id = item_id['text']

    conectar = conexion()
    cursor = conectar.cursor()
    id_turno = data_id
    datos=(nombre, apellido, tipo_reserva, estado, fecha, horario, id_turno)
    sql = "UPDATE turnos SET nombre = ? , apellido = ?, tipo_reserva = ?, estado = ?, fecha = ?, horario = ? WHERE id = ?"
    cursor.execute(sql, datos)
    conectar.commit()
    print("datos: ", datos)
    limpiar_campos_entradas()
    actualizar_treeview()

    
def eliminar_turnos ():
    if askyesno("Eliminar", "Desea eliminar?"):
        valor_id = mostrar_turnos.selection()
        item = mostrar_turnos.item(valor_id)
        mi_id = item['text']
        print("secelcion: ", valor_id, "#", "item: ", item, "#", "id: ", mi_id)

        conectar = conexion()
        cursor = conectar.cursor()
        data = (mi_id,)
        sql = "DELETE FROM turnos WHERE id = ?"
        cursor.execute(sql, data)
        conectar.commit()
        mostrar_turnos.delete(valor_id)
        showerror('Si', "Se ha eliminado correctamente")

    

#inicio de treeview
app=Tk()
app.title("canchita futbol 5")
app.geometry("1000x500")
icono = PhotoImage(file="pelota.png")
app.iconphoto(True, icono)

titulo = Label(app, text="Canchita 5", bg="LightBlue", height=1, width=1)
titulo.grid(row=0, column=0, columnspan=4, sticky=W+E)

#nombres de entrys
nombre = Label(app, text="Nombre",)
nombre.grid(row = 1, column = 2 ,sticky=W)
apellido = Label(app, text="Apellido")
apellido.grid(row= 1, column = 4 ,sticky=W)
tipo_reserva = Label(app, text="Tipo de Reserva")
tipo_reserva.grid(row = 2, column = 2 ,sticky=W)
estado = Label(app, text="Estado")
estado.grid(row=2, column = 4 ,sticky=W)
# monto = Label(app, text="Monto")
# monto.grid(row=2, column = 6 ,sticky=W)
fecha = Label(app, text="Día")
fecha.grid(row=3, column = 2 ,sticky=W)
horario = Label(app, text= "Horario")
horario.grid(row=3, column=4 ,sticky=W)

#variables de tk

var_nombre = StringVar()
var_apellido = StringVar()
var_tipo_reserva = StringVar()
var_estado = StringVar()
# var_monto = IntVar()
var_fecha = StringVar()
var_horario =  StringVar()


#entrys entrada de datos

entry_nombre = Entry(app, textvariable= var_nombre, width=40)
entry_nombre.grid(row = 1, column = 3)
entry_apellido = Entry(app, textvariable= var_apellido, width=40)
entry_apellido.grid(row=1, column = 5)
entry_reserva = ttk.Combobox(
    textvariable= var_tipo_reserva,
    state="readonly",
    values=["canchita 1", "canchita 2", "canchita 2","canchita 4","canchita 5"])
entry_reserva.grid(row=2, column=3)
entry_estado =ttk.Combobox(
    textvariable= var_estado,
    state="readonly",
    values=["impago", "señado"])
entry_estado.grid(row=2, column=5)
entry_fecha = ttk.Combobox(
    textvariable = var_fecha,
    state="readonly",
    values=["Lunes","Martes", "Miercoles", "Jueves","Viernes","Sabado","domingo"])
entry_fecha.grid(row=3, column=3)
entry_horario = ttk.Combobox(
    textvariable = var_horario,
    state="readonly",
    values=[ "10:00 hs", "11:00 hs", "12:00 hs", "13:00 hs", "14:00 hs", "15:00 hs", "16:00 hs", "17:00 hs", "18:00 hs",\
            "19:00 hs", "20:00 hs", "21:00 hs", "22:00 hs",])
entry_horario.grid(row=3, column = 5)



#tkk tabla de muestra de datos y su funcion

mostrar_turnos = ttk.Treeview(app)
mostrar_turnos["columns"] = ("c1", "c2", "c3", "c4", "c5","c6")
mostrar_turnos.column("#0", width=50)
mostrar_turnos.heading("#0",text="")
mostrar_turnos.column("c1", width=150)
mostrar_turnos.heading("c1", text="Nombre")
mostrar_turnos.column("c2", width=150)
mostrar_turnos.heading("c2", text="Apellido")
mostrar_turnos.column("c3", width=120,)
mostrar_turnos.heading("c3", text="Tipo de Reserva")
mostrar_turnos.column("c4", width=120)
mostrar_turnos.heading("c4",text="Estado")
mostrar_turnos.column("c5", width=120)
mostrar_turnos.heading("c5", text="Fecha")
mostrar_turnos.column("c6", width=120)
mostrar_turnos.heading("c6", text="horario")
mostrar_turnos.grid(row = 5, columnspan= 120)

def actualizar_treeview():
    for dato in mostrar_turnos.get_children():
        mostrar_turnos.delete(dato)

    sql = "SELECT * FROM turnos ORDER BY id ASC"
    conectar = conexion()
    cursor = conectar.cursor()
    turnos = cursor.execute(sql)

    for row in turnos.fetchall():
        mostrar_turnos.insert("", "end", text= row[0], values=(row[1], row[2], row[3], row[4], row[5],row[6]))

actualizar_treeview()

#menu y funcion de menu

def color ():
   colores = ["snow", "cadet blue", "misty rose", "dark slate blue", "deep sky blue", "salmon3","DarkOrange1"]
   color = random.choice(colores)
   app.config(bg=color)
    
menu_bar = Menu(app)
menu_1 = Menu(menu_bar, tearoff=True)
menu_1.add_checkbutton(label="Color", command=color)
menu_1.add_command(label="Salir", command= app.quit)
menu_bar.add_cascade(label="Menú", menu=menu_1)
app.config(menu=menu_bar)

# botones

boton_guardar = Button(app, text="Cargar", command= nuevo_turno)
boton_guardar.grid(row=3, column = 9)
boton_Seleccionar = Button(app, text="Modificar", command= traer_datos_entradas)
boton_Seleccionar.grid(row=2, column = 9)
boton_Modificar = Button(app, text="Guardar cambios", command= modificar_turno)
boton_Modificar.grid(row=2, column = 10)
boton_Eliminar = Button(app, text="Eliminar", command= eliminar_turnos)
boton_Eliminar.grid(row=3, column = 10)

app.mainloop()

 
