# LIBRERIAS
import sqlite3
from tkinter import messagebox

class Usuario():
    def verificar(usu,contra):
        # CENTINELA GUIA PARA SABER SI EL USUARIO ES CORRECTO
        usuCorrecto = False
        # CENTINELA GUIA PARA RECONOCER EL TIPO DE USUARIO--> ESTO ES PARA MOSTRARLE AL ADMIN UN MENU DIFERENTE DE OPCIONES
        tipoUsu = "No validado"
        
        # _____________________________CONEXION BASE DE DATOS_________________________________
        Conexion = sqlite3.connect("baseDtos")
        Cursor = Conexion.cursor()
        # BUSCA EN LA BASE DE DATOS SI EL USUARIO INSERTADO PERTENECE A UN USUARIO
        Cursor.execute("SELECT * FROM USUARIOS WHERE USUARIO='"+ usu +"'")
        resultados = Cursor.fetchall()
        if resultados != []:
            for resultado in resultados:
                if usu == resultado[0] and contra == resultado[1]:
                    tipoUsu = "usu"
                    usuCorrecto = True
            # SI LOS RESULTADOS NO COINCIDEN: MUESTRA EL MENSAJE 
            if usuCorrecto == False:
                messagebox.showerror("Mensaje", "LOS DATOS NO COINCIDEN")
        else:
            # BUSCA EN LA BASE DE DATOS SI EL USUARIO INSERTADO PERTENECE A UN ADMINISTRADOR
            Cursor.execute("SELECT * FROM ADMINISTRADOR WHERE USUARIO='"+ usu +"'")
            resultados = Cursor.fetchall()
            if resultados != []:
                for resultado in resultados:
                    if usu == resultado[0] and contra == resultado[1]:
                        tipoUsu = "admin"
                        usuCorrecto = True
                # SI LOS RESULTADOS NO COINCIDEN: MUESTRA EL MENSAJE 
                if usuCorrecto == False:
                    messagebox.showerror("Mensaje", "LOS DATOS NO COINCIDEN")
            else:
                # VERIFICACION DE QUE LOS CAMPOS NO ESTEN VACIOS
                if usu == "" or contra == "":
                    messagebox.showinfo("Mensaje", "COMPLETE TODOS LOS CAMPOS")
                else:
                    # CUANDO EL USUARIO NI LA CONTRASEÑA EXISTEN EN LA BASE DE DATOS: MUESTRA EL MENSAJE
                    messagebox.showwarning("Mensaje", "EL USUARIO NO EXISTE") 
        # REALIZA LAS PETICIONES A LA BASE DE DATOS 
        Conexion.commit()
        # CERRAMOS LA CONEXION CON LA BASE DE DATOS
        Conexion.close()
        
        # DEVOLVEMOS LOS VALORES DE VALIDACION
        return tipoUsu,usuCorrecto

