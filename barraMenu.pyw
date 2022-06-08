# ARCHIVOS DEL PROGRAMA
from IngCompras import ventanaCompras
from IngVentas import ventanaVentas
from CRUD_IngCompras import valoresCampo
# LIBRERIAS
from tkinter import *
from tkinter import messagebox

# CLASE BARRA MENU
class navBar():
    # ESTADO INICIAL DE LA CLASE
    # LE PASAMOS LA RAIZ DESDE main.pyw | PARA NO TENER QUE VOLVER A CREAR LA VENTANA
    def __init__(self):
        # LA VARIABLE ME GUARDA LAS PROPIEDADES DE LA VENTANA QUE ESTA ACTUALMENTE ABIERTA
        self.objetoVentana = ""
    # PASAMOS LA VARIABLE ventanaLogin desde main.py | PARA MOSTRAR NUEVAMENTE LA VENTANA LOGIN CUANDO SE CIERRE LA VENTANA ACTUAL
    # PASAMOS LA RAIZ DE LA VENTANA QUE ESTA ACTUALMENTE ABIERTA PARA CERRARLA Y ABRIR LOGIN
    def Sesion(self,root,rootLogin): 
        valor = messagebox.askokcancel("Salir","¿Deseas Cerrar la Sesión?")
        if valor == True:
            rootLogin.deiconify()
            # DESTRUIMOS LA VENTANA ACTUAL PARA MOSTRAR EL LOGIN
            root.destroy()
            
    # IMPORTAMOS LA VARIABLE rootLogin desde main.py | PARA MOSTRAR NUEVAMENTE LA VENTANA LOGIN CUANDO SE CIERRE LA VENTANA ACTUAL
    # IMPORTAMOS LA VARIABLE numVentana PARA QUE EL PROGRAMA COMPRENDA CUAL ES LA VENTANA QUE SE QUIERE ABRIR
    # IMPORTAMOS EL OBJETO MenuNavegacion PARA REESCRIBIR SUS CARACTERISTICAS Y QUE ME GUARDE LAS PROPIEDADES DE LA VENTANA ACTUAL EN LA VARIABLE | self.objetoVentana  
    def crearMenu(self,rootLogin,numVentana,tipoUsu,MenuNavegacion):
        # OBTENEMOS LAS CARACTERISTICAS DE LA VENTANA QUE SE DESEA ABRIR A PARTIR DE SU NUMERO
        self.objetoVentana = MenuNavegacion.mostrarVentana(numVentana)
        # OBTENEMOS LA RAIZ DE LA VENTANA ELEGIDA | ESTO SE HACE PARA COMPRENDER CUAL CERRAR AL PASAR A LA SIGUIENTE VENTANA
        root = self.objetoVentana.obRoot()
        # ESTABLECEMOS LA VENTANA A LA CUAL SE LE CREARA EL MENU A PARTIR DE SU RAIZ
        barraMenu = Menu(root)
        root.config(menu=barraMenu) # INSERTAMOS EL MENU EN LA VENTANA
        # EVALUAMOS QUE SE LE INSERTARA AL MENU, PUESTO QUE NO PODEMOS ENLAZAR EN LA BARRA MENU LA MISMA DIRECCIÓN DE LA VENTANA YA ABIERTA
        # VERIFICAMOS QUE LA VENTANA EN LA QUE ESTAMOS NO SEA LA 1, PARA NO AGREGAR SU ENLACE EN LA BARRA DE NAVEGACION
        if numVentana != 1:
            barraMenu.add_command(label="Ingreso de Compras", command= lambda: MenuNavegacion.ocultarVentana(rootLogin,1,tipoUsu,root,MenuNavegacion))
        # VERIFICAMOS QUE LA VENTANA EN LA QUE ESTAMOS NO SEA LA 3, PARA NO AGREGAR SU ENLACE EN LA BARRA DE NAVEGACION
        if numVentana != 2:
            barraMenu.add_command(label="Ingreso de Ventas", command= lambda: MenuNavegacion.ocultarVentana(rootLogin,2,tipoUsu,root,MenuNavegacion))
        # SI EL USUARIO ES DETECTADO COMO ADMINISTRADOR SE LE MOSTRARA LA OPCION EN LA BARRA MENU
        # if tipoUsu == "admin":
        #     barraMenu.add_command(label="Crear nuevo Usuario")
            
        barraMenu.add_command(label="Cerrar Sesión", command= lambda: MenuNavegacion.Sesion(root,rootLogin))  
        
        # INSERTAMOS LOS BOTONES DE LA INTERFAZ (CRUD)
        MenuNavegacion.BotonesInterfaz()

    # IMPORTAMOS LA VARIABLE numVentana PARA EVALUAR LAS CONDICIONES
    def mostrarVentana(self,numVentana):
        # CREAMOS UNA RAIZ PARA ASIGNARLA A LA VENTANA QUE SE DESEA ABRIR
        window = Toplevel()
        # VERIFICAMOS CUAL ES LA VENTANA QUE SE DESEA ABRIR
        if numVentana == 1:
            # VENTANA INGRESAR COMPRAS
            objetoVentana = ventanaCompras(window)
        elif numVentana == 2:
            # VENTANA INGRESAR VENTAS
            objetoVentana = ventanaVentas(window)
        # RETORNAMOS EL OBJETO DE LA VENTANA CREADA
        return objetoVentana

    # OCULTA LA VENTANA ACTUAL EN LA QUE SE ENCUENTRA EL PROGRAMA PARA PASAR A LA SIGUIENTE
    # EL PARAMETRO rotLogin SE RETOMA PARA NO OLVIDAR LA VARIABLE DE main.pyw, CON EL FIN DE QUE SI SE CIERRA SESION EN CUALQUIER MOMENTO AUN SE PUEDA MOSTRAR LA VENTANA LOGIN
    def ocultarVentana(self,rootLogin,numVentana,tipoUsu,root,MenuNavegacion):
        # DESTRUIMOS LA VENTANA ACTUAL EN LA QUE NOS ENCONTRAMOS
        root.destroy()
        # SOBRE ESCRIBIMOS LAS CUALIDADES DEL OBJETO MENU NAVEGACION PARA ABRIR LA VENTANA SIGUIENTE SOBRE EL MISMO
        MenuNavegacion.crearMenu(rootLogin,numVentana,tipoUsu,MenuNavegacion)
    
    def BotonesInterfaz(self):
        # BOTONES (GUARDAR,ELIMINAR,ACTUALIZAR y BUSCAR)
        if self.objetoVentana.obNumVent() == 1:
            Button(self.objetoVentana.contBtnGuardar, text = 'CREAR PRODUCTO',font="Arial 10", bg="#00E3A2",width= 40, command= lambda:valoresCampo.Crear(self.objetoVentana)).pack()
            Button(self.objetoVentana.contBtnGuardarCam, text = 'ACTUALIZAR PRODUCTO',font="Arial 10", bg="#00E3A2",width= 40, command= lambda:valoresCampo.guardarCambios(self.objetoVentana)).pack()
            Button(self.objetoVentana.contTabla,text = 'ELIMINAR',font="Arial 10", bg="#00ACEC", relief=FLAT, command= lambda:valoresCampo.Eliminar(self.objetoVentana)).grid(row = 5, padx=5, column = 0, sticky = W + E)
            Button(self.objetoVentana.contTabla,text = 'ACTUALIZAR',font="Arial 10", bg="#00ACEC", relief=FLAT, command= lambda:valoresCampo.Actualizar(self.objetoVentana)).grid(row = 5, padx=5, column = 1, sticky = W + E)
            Button(self.objetoVentana.contTabla,text = 'BUSCAR',font="Arial 10", bg="#00ACEC", relief=FLAT, command= lambda:valoresCampo.Leer(self.objetoVentana)).grid(row = 5, padx=5, column = 2, sticky = W + E)
            Button(self.objetoVentana.contCancelarBus,text = 'CANCELAR BUSQUEDA',font="Arial 10", bg="#00D7B3", relief=FLAT,width= 40, command= lambda:valoresCampo.borrarBusqueda(self.objetoVentana)).pack()
        elif self.objetoVentana.obNumVent() == 2:
            Button(self.objetoVentana.contBtnGuardar, text = 'INGRESAR VENTA',font="Arial 10", bg="#00E3A2",width= 40, command= lambda:valoresCampo.Crear(self.objetoVentana)).pack()
            Button(self.objetoVentana.contTabla,text = 'BUSCAR',font="Arial 10", bg="#00ACEC", relief=FLAT, command= lambda:valoresCampo.Leer(self.objetoVentana)).grid(row = 5, padx=5, column = 1, sticky = W + E)
            Button(self.objetoVentana.contCancelarBus,text = 'CANCELAR BUSQUEDA',font="Arial 10", bg="#00D7B3", relief=FLAT,width= 40, command= lambda:valoresCampo.borrarBusqueda(self.objetoVentana)).pack()
            
        
        
    

        
        