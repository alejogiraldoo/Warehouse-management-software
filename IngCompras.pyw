# ARCHIVOS DEL PROGRAMA
from CRUD_IngCompras import valoresCampo
# LIBRERIAS
from tkinter.ttk import Treeview
from tkinter import *
import sqlite3

# _____________________________CONEXION BASE DE DATOS_________________________________
Conexion = sqlite3.connect("baseDtos")
Cursor = Conexion.cursor()
try:
  Cursor.execute("CREATE TABLE COMPRAS(REFERENCIA VARCHAR(50), DESCRIPCION VARCHAR(50), CANTIDAD VARCHAR(50), VALOR_UNI VARCHAR(50))")
except:
  pass

class ventanaCompras():
  def __init__(self, window):
    # RAIZ Y FRAME
    self.wind = window
    self.numVentana = 1
    # UBICACION DE LA VENTANA EN LA PANTALLA DEL USUARIO
    ancho_ventana = 810
    alto_ventana = 550
    x_ventana = self.wind.winfo_screenwidth() // 2 - ancho_ventana // 2
    y_ventana = self.wind.winfo_screenheight() // 2 - alto_ventana // 2
    posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
    
    self.wind.title("Aplicación") # NOMBRE DE LA VENTANA
    self.wind.geometry(posicion) # POSICION DE LA VENTANA CON RESPECTO AL CENTRO
    self.wind.iconbitmap("img/Icon-form.ico") # ICONO DE LA VENTANA
    # CAMPOS DE LA VENTANA
    self.ref = StringVar()
    self.desc = StringVar()
    self.cant = StringVar()
    self.valor_U = StringVar()
    
    # FRAME
    self.contenedor = Frame(self.wind)
    self.contenedor.pack(expand=True,anchor=CENTER)
    self.frame = LabelFrame(self.contenedor, text = 'Registrar Productos')
    self.frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)
    self.contBtnGuardar = Frame(self.frame)
    self.contBtnGuardar.grid(row = 5, column = 0, columnspan = 3)
    self.contBtnGuardarCam = Frame(self.frame)
    self.contBtnGuardarCam.grid(row = 5, column = 0, columnspan = 3)
    self.contTabla = Frame(self.contenedor)
    self.contCancelarBus = Frame(self.contTabla)
    self.contCancelarBus.grid(row = 6, column = 0, columnspan = 3)
    
    # LABEL REFERENCIA
    Label(self.frame, text = 'Referencia: ', font="Arial 10 bold").grid(row = 1, column = 0)
    # ENTRY REFERENCIA
    self.Referencia = Entry(self.frame,text=self.ref,width=32)
    self.Referencia.focus()
    self.Referencia.grid(row = 1, column = 1, padx= 10, pady=5)
    # LABEL DESCRIPCION
    Label(self.frame, text = 'Descripcion: ', font="Arial 10 bold").grid(row = 2, column = 0)
    # ENTRY DESCRIPCION
    self.Descripcion = Entry(self.frame,text=self.desc,width=32)
    self.Descripcion.grid(row = 2, column = 1, padx= 10, pady=5)
    # LABEL CANTIDAD
    Label(self.frame, text = 'Cantidad: ', font="Arial 10 bold").grid(row = 3, column = 0)
    # ENTRY CANTIDAD
    self.Cantidad = Entry(self.frame,text=self.cant,width=32)
    self.Cantidad.grid(row = 3, column = 1, padx= 10, pady=5)
    # LABEL VALOR U
    Label(self.frame, text = 'Valor Unid: ', font="Arial 10 bold").grid(row = 4, column = 0)
    # ENTRY VALOR U
    self.Valor_Unid = Entry(self.frame,text=self.valor_U,width=32)
    self.Valor_Unid.grid(row = 4, column = 1, padx= 10, pady=5)
    
    # TITULO DE LA TABLA
    Label(self.contenedor,text = "Productos Creados", font="Arial 12 bold").grid(row = 2, column = 0, columnspan = 3, sticky = W + E)

    # ZONA DATOS
    self.message = Label(self.contenedor,text = '', fg = 'red', font="Arial 12 bold")
    self.message.grid(row = 3, column = 0, columnspan = 3, sticky = W + E)
    
    # GENERAMOS LA TABLA DE LOS REGISTROS
    self.actualizarTabla()

  def actualizarTabla(self):
    # TABLA (REGISTROS ENCONTRADOS)
    self.resultados = valoresCampo.obProductos()
    self.contTabla.grid(row = 5, column = 0, columnspan=3,sticky = W + E)
    self.tree = Treeview(self.contTabla,height = 10, columns = [f"#{n}" for n in range(1, 4)])
    self.tree.grid(row = 4, column = 0, columnspan = 3)
    self.tree.heading('#0', text = 'Referencia', anchor = CENTER)
    self.tree.heading('#1', text = 'Descripción', anchor = CENTER)
    self.tree.heading('#2', text = 'Cantidad', anchor = CENTER)
    self.tree.heading('#3', text = 'Valor Unid', anchor = CENTER)
        
    # LIMPIA LA TABLA
    records = self.tree.get_children()
    for element in records:
      self.tree.delete(element)
        
    # INSERTAMOS LOS REGISTROS DE COMPRAS
    for resultado in self.resultados:
      self.tree.insert('', 0, text=resultado[0], values= [resultado[1],resultado[2],resultado[3]])
      
    if self.resultados == []:
      self.contTabla.grid_forget()
      self.contBtnGuardar.grid(row = 5, column = 0, columnspan = 3)
      self.contBtnGuardarCam.grid_forget()
      self.message['text'] = "No hay PRODUCTOS CREADOS"
    
    self.contBtnGuardarCam.grid_forget()
    self.contCancelarBus.grid_forget()
  
  def limpiarCampos(self):
    # CAPTURAMOS LOS VALORES ANTES DE SER BORRADOS
    valorReferencia = self.ref.get().strip().lower()
    valorCantidad = self.cant.get().strip().lower()
    valorVU = self.valor_U.get().strip().lower()
    textoDescripcion = self.desc.get().strip().lower()
    # LIMPIAMOS LOS CAMPOS
    self.ref.set("")
    self.desc.set("")
    self.cant.set("")
    self.valor_U.set("")
    return valorReferencia,valorCantidad,valorVU,textoDescripcion
  
  def obRoot(self):
    return self.wind
  
  def obNumVent(self):
    return self.numVentana