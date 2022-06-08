# ARCHIVOS DEL PROGRAMA
from verificarUsuario import Usuario
from barraMenu import navBar
# LIBRERIAS
from tkinter import *
import sqlite3

# _____________________________CONEXION BASE DE DATOS_________________________________
try:
  Conexion = sqlite3.connect("baseDtos")
  Cursor = Conexion.cursor()
  Cursor.execute("CREATE TABLE USUARIOS(USUARIO VARCHAR(10) UNIQUE, CONTRASENA VARCHAR(8))")
  Cursor.execute("CREATE TABLE ADMINISTRADOR(USUARIO VARCHAR(10) UNIQUE, CONTRASENA VARCHAR(8))")
  Cursor.execute("INSERT INTO ADMINISTRADOR VALUES('admin','1234')")
  Cursor.execute("INSERT INTO USUARIOS VALUES('usu','1234')")
  # REALIZA LAS PETICIONES A LA BASE DE DATOS 
  Conexion.commit()
  # CERRAMOS LA CONEXION CON LA BASE DE DATOS
  Conexion.close()
except:
  pass

# RAIZ Y FRAME
# NOTA: DECLARAMOS LA RAIZ Y LA IMAGEN AFUERA; DEBIDO A QUE LA IMAGEN NO CARGA DENTRO DE LA CLASE(PROBLEMAS DE LECTURA)
root = Tk() # CREAMOS LA VENTANA
frame = Frame(root) # CREAMOS EL CONTENEDOR DEL CONTENIDO DE LA VENTANA
frame.pack(expand="True") # AÑADIMOS EL FRAME A LA RAIZ(VENTANA)
# IMAGEN
Imagen = PhotoImage(file="img/Icon-form.png") # SELECCIONAMOS LA IMAGEN CON SU RUTA
Imagen = Imagen.subsample(3) # TAMAÑO DE LA IMAGEN
Label(frame, image=Imagen).grid(row=0, column=1, ipady=10) # INSERTAMOS LA IMAGEN EN EL FRAME

# CLASE PRINCIPAL
class ventanaLogin():
  # ESTADO INICIAL DE LA CLASE
  def __init__(self,root,frame): #PARAMETROS DE LA CLASE
    # CENTINELAS DE VERIFICACION (ME PERMITEN SABER QUE USUARIO ENTRO, SI LOS DATOS SON CORRECTOS)
    self.tipoUsu = ""
    self.usuCorrecto = False
    # RAIZ Y FRAME
    self.root = root
    self.frame = frame
    # CAMPOS DEL FORMULARIO
    self.usuario = StringVar()
    self.contrasena = StringVar()
    # UBICACION DE LA VENTANA EN LA PANTALLA DEL USUARIO
    ancho_ventana = 400
    alto_ventana = 450
    x_ventana = self.root.winfo_screenwidth() // 2 - ancho_ventana // 2
    y_ventana = self.root.winfo_screenheight() // 2 - alto_ventana // 2
    posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
    
    self.root.title("Login") # NOMBRE DE LA VENTANA
    self.root.geometry(posicion) # POSICION DE LA VENTANA CON RESPECTO AL CENTRO
    self.root.iconbitmap("img/Icon-form.ico") # ICONO DE LA VENTANA
    
  def crearVentana(self):
    # LABEL
    Label(self.frame, text="Usuario", font="Arial 10 bold").grid(row=1, column=1, pady=3)
    Label(self.frame, text="Contraseña", font="Arial 10 bold").grid(row=3, column=1, pady=3)
    # ENTRY
    self.Usu = Entry(self.frame, textvariable=self.usuario, width=32, borderwidth= 4, relief=FLAT, font="Arial 10")
    self.Usu.focus()
    self.Usu.grid(row=2, column=1, pady=5, ipady= 3, ipadx= 3)
    Entry(self.frame, textvariable=self.contrasena, width=32, borderwidth= 4, relief=FLAT, font="Arial 10", show="*").grid(row=4, column=1, pady=5, ipady= 3, ipadx= 3)
    # BOTONES
    Button(self.frame,text="Iniciar Sesión", font="Arial 11", bg="#00ACEC", relief=FLAT, command= lambda: self.limpiarCampos()).grid(row=5, column=1, pady=20, ipady=5, columnspan=2, sticky=W + E)
    # RETORNO DE LA RAIZ PARA SER EJECUTADA
    return self.root
  
  def limpiarCampos(self):
    # VALORES DE LOS CAMPOS
      # NOTA: CAPTURAMOS LOS VALORES ANTES DE LIMPIAR LOS CAMPOS
    usuario = self.usuario.get().strip().lower()
    contrasena = self.contrasena.get().strip().lower()
    # LIMPIAMOS LOS CAMPOS
    self.usuario.set("")
    self.contrasena.set("")
    # VALIDAMOS QUE LOS CAMPOS NO ESTEN VACIOS Y QUE LOS DATOS ESTEN CORRECTOS
    self.tipoUsu,self.usuCorrecto = Usuario.verificar(usuario,contrasena)
    # CONFIRMAMOS SI LA VERIFICACION FUE EXITOSA
    if self.usuCorrecto == True:
      # DESTRUIMOS LA VENTANA LOGIN PARA ABRIR LA PRINCIPAL (INGRESAR COMPRAS)
      self.root.withdraw()
      # EJECUTAMOS LA FUNCION PARA ABRIR LA NUEVA VENTANA
      Login.iniciarPrograma()
  
  def iniciarPrograma(self):
    # NOTA: LA PRIMERA VENTANA QUE SE ABRE ES INGRESAR COMPRAS
    # EL NUMERO DE DE LA VENTANA QUE SE INICIARA SERA LA 2
    # CREAMOS EL MENU DE LA INTERFAZ (NAVBAR)
    MenuNavegacion = navBar()
    # SE ENVIA EL OBJETO COMO PARAMETRO PARA REESCRIBIRLO (ESTO SE HACE CON LA INTENCION DE QUE EL PROGRAMA INTERPRETE EN QUE VENTANA ESTAMOS --> barraMenu.pyw)
    MenuNavegacion.crearMenu(self.root,1,self.tipoUsu,MenuNavegacion)
  
#_________________________________________________________________________________________________________
# CREAMOS EL OBJETO VENTANA (INSTANCIA DE LA CLASE)
Login = ventanaLogin(root,frame)
# CREAMOS LA VENTANA
rootLogin = Login.crearVentana()
# EJECUTAMOS LA VENTANA CREADA
rootLogin.mainloop()