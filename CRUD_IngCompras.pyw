# LIBRERIAS
import sqlite3
from tkinter import messagebox

from numpy import pad

# _____________________________CONEXION BASE DE DATOS_________________________________
Conexion = sqlite3.connect("baseDtos")
Cursor = Conexion.cursor()

class valoresCampo():
    def obProductos():
        Cursor.execute("SELECT * FROM COMPRAS")
        Conexion.commit()
        resultados = Cursor.fetchall()
        return resultados
    
    def Crear(objetoVentana):
        ref,cant,valU,desc = objetoVentana.limpiarCampos()
        camposVacios = valoresCampo.validarCampos(ref,cant,valU,desc)
        if camposVacios == 0:
            Cursor.execute("INSERT INTO COMPRAS VALUES('"+ ref +"','"+ desc +"','"+ cant +"','"+ valU +"')")
            Conexion.commit()
            objetoVentana.message['text'] = "El Producto con la REFERENCIA | {} | ha sido AGREGADO...".format(ref)
            objetoVentana.actualizarTabla()
        else:
            messagebox.showwarning("Mensaje", "COMPLETE TODOS LOS CAMPOS PAPRA CREAR EL PRODUCTO")
    
    def Leer(objetoVentana):
        objetoVentana.message['text'] = ""
        objetoVentana.actualizarTabla()
        
        objetoVentana.message['text'] = ""
        objetoVentana.contBtnGuardarCam.grid_forget()
        objetoVentana.contBtnGuardar.grid(row = 5, column = 0, columnspan = 3)
        ref = objetoVentana.ref.get().strip().lower()
        desc = objetoVentana.desc.get().strip().lower()
        cant = objetoVentana.cant.get().strip().lower()
        valor_U = objetoVentana.valor_U.get().strip().lower()
        camposVacios = valoresCampo.validarCampos(ref,cant,valor_U,desc)
        if camposVacios < 4:
            # UBICACION DE LA VENTANA EN LA PANTALLA DEL USUARIO
            ancho_ventana = 810 
            alto_ventana = 600
            x_ventana = objetoVentana.wind.winfo_screenwidth() // 2 - ancho_ventana // 2
            y_ventana = objetoVentana.wind.winfo_screenheight() // 2 - alto_ventana // 2
            posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
            objetoVentana.wind.geometry(posicion) # POSICION DE LA VENTANA CON RESPECTO AL CENTRO
            objetoVentana.contCancelarBus.grid(row = 6, column = 0, columnspan = 3, pady=10)
            consulta = valoresCampo.FiltroConsulta(ref,cant,valor_U,desc)
            Cursor.execute("SELECT * FROM COMPRAS WHERE" + " " + consulta)
            Conexion.commit()
            resultados = Cursor.fetchall()
            # LIMPIA LA TABLA
            records = objetoVentana.tree.get_children()
            for element in records:
                objetoVentana.tree.delete(element)
            # INSERTAMOS LOS REGISTROS DE COMPRAS
            for resultado in resultados:
                objetoVentana.tree.insert('', 0, text=resultado[0], values= [resultado[1],resultado[2],resultado[3]])
            if resultados == []:
                objetoVentana.message['text'] = "No hay PRODUCTOS QUE CUMPLAN LAS CONDICIONES DE LA BUSQUEDA..."
            else:
                objetoVentana.message['text'] = "Resultados ENCONTRADOS de la BUSQUEDA..."
        else:
            messagebox.showwarning("Mensaje", "No hay requerimientos en la CONSULTA... Por favor digíte lo que quiere CONSULTAR en la TABLA DE | Registrar Productos |,\nUNA VEZ HECHO PRESIONE EL BOTON BUSCAR")
        objetoVentana.ref.set("")
        objetoVentana.desc.set("")
        objetoVentana.cant.set("")
        objetoVentana.valor_U.set("")
    
    def Actualizar(objetoVentana):
        objetoVentana.message['text'] = ""
        if objetoVentana.tree.item(objetoVentana.tree.selection())['text'] != "":
            ref = str(objetoVentana.tree.item(objetoVentana.tree.selection())['text'])
            desc = str(objetoVentana.tree.item(objetoVentana.tree.selection())['values'][0])
            cant = str(objetoVentana.tree.item(objetoVentana.tree.selection())['values'][1])
            valor_U = str(objetoVentana.tree.item(objetoVentana.tree.selection())['values'][2])
            objetoVentana.ref.set(ref)
            objetoVentana.desc.set(desc)
            objetoVentana.cant.set(cant)
            objetoVentana.valor_U.set(valor_U)
            objetoVentana.contBtnGuardar.grid_forget()
            objetoVentana.contBtnGuardarCam.grid(row = 5, column = 0, columnspan = 3)
            messagebox.showinfo("Mensaje", "LAS CARACTERISTICAS DEL PRODUCTO SERAN MOSTRADAS EN LA TABLA DE | Registrar Productos |.\nUna vez cambiadas presione ACTUALIZAR PRODUCTO para Guardar lo CAMBIOS")
        else:
            messagebox.showwarning("Mensaje", "PARA ACTUALIZAR SELECCIONE UN PRODUCTO DE LA TABLA: | Registros del Inventario |") 
    
    def guardarCambios(objetoVentana):
        objetoVentana.message['text'] = ""
        objetoVentana.contBtnGuardar.grid(row = 5, column = 0, columnspan = 3)
        if objetoVentana.tree.item(objetoVentana.tree.selection())['text'] != "":
            selecRef = str(objetoVentana.tree.item(objetoVentana.tree.selection())['text'])
            selecDesc = str(objetoVentana.tree.item(objetoVentana.tree.selection())['values'][0])
            selecCant = str(objetoVentana.tree.item(objetoVentana.tree.selection())['values'][1])
            selecValor_U = str(objetoVentana.tree.item(objetoVentana.tree.selection())['values'][2])
            ref = objetoVentana.ref.get().strip().lower()
            desc = objetoVentana.desc.get().strip().lower()
            cant = objetoVentana.cant.get().strip().lower()
            valor_U = objetoVentana.valor_U.get().strip().lower()
            valor = messagebox.askokcancel("¡ALERTA!",f"¿DESEA REALIZAR LOS CAMBIOS EN EL PRODUCTO? \nREFERENCIA: {selecRef}, DESCRIPCIÓN: {selecDesc}, CANTIDAD: {selecCant}, VALOR U: {selecValor_U}")
            if valor == True:
                Cursor.execute("UPDATE COMPRAS SET REFERENCIA = '"+ref+"',DESCRIPCION = '"+desc+"',CANTIDAD = '"+cant+"',VALOR_UNI = '"+valor_U+"' WHERE REFERENCIA = '"+selecRef+"' AND DESCRIPCION = '"+selecDesc+"' AND CANTIDAD = '"+selecCant+"' AND VALOR_UNI = '"+selecValor_U+"'")
                Conexion.commit()
                objetoVentana.message['text'] = "El Producto con la REFERENCIA {} ha sido MODIFICADO...".format(selecRef)
            objetoVentana.contBtnGuardarCam.grid_forget()
            objetoVentana.ref.set("")
            objetoVentana.desc.set("")
            objetoVentana.cant.set("")
            objetoVentana.valor_U.set("")  
            objetoVentana.actualizarTabla()
    
    def Eliminar(objetoVentana):
        objetoVentana.message['text'] = ""
        objetoVentana.contBtnGuardar.grid(row = 5, column = 0, columnspan = 3)
        if objetoVentana.tree.item(objetoVentana.tree.selection())['text'] != "":
            ref = str(objetoVentana.tree.item(objetoVentana.tree.selection())['text'])
            desc = str(objetoVentana.tree.item(objetoVentana.tree.selection())['values'][0])
            cant = str(objetoVentana.tree.item(objetoVentana.tree.selection())['values'][1])
            valor_U = str(objetoVentana.tree.item(objetoVentana.tree.selection())['values'][2]) 
            Cursor.execute("DELETE FROM COMPRAS WHERE REFERENCIA = '"+ ref +"' AND DESCRIPCION = '"+ desc +"' AND CANTIDAD = '"+ cant +"' AND VALOR_UNI = '"+ valor_U +"'")
            Conexion.commit()
            objetoVentana.message['text'] = "El Producto con la REFERENCIA {} ha sido ELIMINADO...".format(ref) 
            objetoVentana.actualizarTabla()
        else:
            messagebox.showwarning("Mensaje", "PARA ELIMINAR SELECCIONE UN PRODUCTO DE LA TABLA: | Registros del Inventario |") 
        objetoVentana.ref.set("")
        objetoVentana.desc.set("")
        objetoVentana.cant.set("")
        objetoVentana.valor_U.set("")
    
    def borrarBusqueda(objetoVentana):
        # UBICACION DE LA VENTANA EN LA PANTALLA DEL USUARIO
        ancho_ventana = 810 
        alto_ventana = 520
        x_ventana = objetoVentana.wind.winfo_screenwidth() // 2 - ancho_ventana // 2
        y_ventana = objetoVentana.wind.winfo_screenheight() // 2 - alto_ventana // 2
        posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
        objetoVentana.wind.geometry(posicion) # POSICION DE LA VENTANA CON RESPECTO AL CENTRO
        objetoVentana.message['text'] = ""
        objetoVentana.contCancelarBus.grid_forget()
        objetoVentana.actualizarTabla()
        
    def validarCampos(ref,cant,valU,desc):
        camposVacios = 0
        camposForm = [ref,cant,valU,desc]
        for campos in camposForm:
            if len(campos) <= 0:
                camposVacios += 1
        return camposVacios
    
    def FiltroConsulta(ref,cant,valU,desc):
        consulta = ""
        contador = 0
        if ref != "":
            consulta+= "REFERENCIA = '"+ ref +"'"
            contador += 1
        if len(desc) > 1:
            if contador > 0:
                consulta+=" AND "
            consulta+= "DESCRIPCION = '"+ desc +"'"
            contador += 1
        if cant != "":
            if contador > 0:
                consulta+=" AND "
            consulta+= "CANTIDAD = '"+ cant +"'"
            contador += 1
        if valU != "":
            if contador > 0:
                consulta+=" AND "
            consulta+= "VALOR_UNI = '"+ valU +"'"
            contador += 1
        return consulta