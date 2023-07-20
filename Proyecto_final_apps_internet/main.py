from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask import redirect
from flask import flash
from wtforms.csrf.session import SessionCSRF
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask import jsonify
import forms
from wtforms.widgets import html_params
import sqlite3
from sqlite3 import Error


horarios_bd="C:\\Users\\Usuario\\Documents\\Proyecto_final_apps_internet\\static\\db\\horarios.db"


app = Flask(__name__)
app.secret_key = 'mi_clave'
csrf = SessionCSRF()

@app.route("/login", methods=["GET","POST"])
def login():
    titulo = "login"
    login_form = forms.login(request.form)

    if request.method == "POST" and login_form.validate():
        # -----declaracion variables-----------#
        usuario = login_form.usuario.data.lower()
        clave = login_form.clave.data

        # -----conexión con base de datos-------#
        connect = sqlite3.connect(horarios_bd)
        cursor = connect.cursor()
        sentencia = """SELECT username, password FROM usuarios WHERE username = ?"""
        cursor.execute(sentencia, (usuario,))
        fila = cursor.fetchone()
        connect.commit()
        connect.close()
        print(fila)
        if fila:
            username, password = fila
            if password == clave and username == usuario:
                session['user'] = username
                return redirect(url_for('registro'))
            else:
                # Si las credenciales no son válidas, mostrar un mensaje de error
                flash('Usuario o contraseña incorrectos', 'error')
        else:
            # Si el usuario no está registrado, mostrar un mensaje de error
            flash('Usuario o contraseña incorrectos', 'error')

    return render_template("Login.html", titulo=titulo, form=login_form)


@app.route("/ingresar", methods=["GET","POST"])
def ingresar():
    titulo="ingresar"
    ingresar_form=forms.usuarios(request.form)
    if request.method == "POST" and ingresar_form:
        # -----declaracion variables-----------#
        nombre = ingresar_form.nombre.data.lower()
        apellido = ingresar_form.apellido.data
        cargo = ingresar_form.cargo.data
        tipo_empleado= ingresar_form.tipo_empleado.data
        salario= ingresar_form.salario.data
        descripcion=ingresar_form.descripcion.data
        password= ingresar_form.password.data

        

        #-------Conexion base de datos----------#    
        connect=sqlite3.connect(horarios_bd)
        cursor= connect.cursor()
        
      
        username=nombre+"_"+apellido
        sentencia= (""" INSERT INTO usuarios (username, password, nombre, apellido, cargo, tipo_empleado, salario_X_hora, descripcion, hora_entrada_predeterm, hora_salida_predeterm) VALUES (?,?,?,?,?,?,?, ?, ?, ?)""" )
        
        titulo=username
        cursor.execute( sentencia, ( username, password, nombre, apellido, cargo, tipo_empleado, salario, descripcion,    ))
        connect.commit()
        connect.close()

    return render_template("usuarios.html", titulo=titulo, ingresar_form=ingresar_form)
@app.route("/registro", methods=["GET","POST"])
def registro():
    titulo = "registro"
    login_form = forms.login(request.form)
    flash('Inicio de sesión exitoso', 'success')
    return render_template("registro.html", titulo=titulo, form=login_form)

if __name__ == "__main__":
	app.run(debug=True, port=5000, host="0.0.0.0")
        
        