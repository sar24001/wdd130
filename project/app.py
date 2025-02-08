from flask import Flask, render_template, request, redirect, session, flash, url_for
from cs50 import SQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
from datetime import date
from werkzeug.utils import secure_filename
import sqlite3
from flask_mail import Mail, Message
from flask import jsonify

app = Flask(__name__)
app.secret_key = "88888"  # Replace with a secure key
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'beautyshine684@gmail.com'
app.config['MAIL_PASSWORD'] = 'ogdq gexb zjak xmlq'
app.config['MAIL_DEFAULT_SENDER'] = 'beautyshine684@gmail.com'
mail = Mail(app)

app.config['UPLOAD_FOLDER'] = 'uploads/'  # Ruta relativa a tu proyecto
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}


def mandar_correo(id_cita):
    try:
        print("hola")
        print(id_cita)
        print("hola 2")
        print(session)
        persona = db.execute(
            "SELECT CONCAT_WS(' ', nombre1, apellido1) as nombre FROM Persona WHERE usuario_id = ?", session["id_usuario"])
        cita = db.execute("""
                          SELECT
                          S.descripcion AS servicio,
                          CONCAT_WS(' ', P.nombre1, P.apellido1) as veterinario
                          FROM Servicios AS S
                          JOIN Citas AS C
                          ON S.id_servicio = C.servicio_id
                          JOIN Veterinarios AS V
                          ON C.vet_id = V.id_veterinario
                          JOIN Persona AS P ON P.id_persona =  V.persona_id
                          WHERE id_cita = ?
                          """, id_cita)
        print("hola 4")
        print(cita)
        print("hola5")
        msg = Message(
            "Confirmación de cita",
            recipients=[session["email"]],
            html=f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Confirmación de Cita</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f9;
            }}
            .container {{
                max-width: 600px;
                margin: 20px auto;
                background: #fff;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                overflow: hidden;
            }}
            .header {{
                background: #4CAF50;
                color: #fff;
                padding: 20px;
                text-align: center;
            }}
            .content {{
                padding: 20px;
                line-height: 1.6;
                color: #333;
            }}
            .content h2 {{
                margin-top: 0;
            }}
            .footer {{
                background: #f1f1f1;
                text-align: center;
                padding: 10px;
                color: #555;
                font-size: 0.9em;
            }}

        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>¡Cita Confirmada!</h1>
            </div>
            <div class="content">
                <h2>Hola, {persona[0]["nombre"]}.</h2>
                <p>
                    Queremos confirmarte que tu cita ha sido agendada con éxito. Aquí tienes los detalles:
                </p>
                <ul>
                    <li><strong>Servicio:</strong> {cita[0]["servicio"]}</li>
                    <li><strong>Veterinario:</strong> {cita[0]["veterinario"]}</li>
                </ul>
                <p>
                    Por favor, no dudes en contactarnos si necesitas más información o realizar algún cambio.
                </p>
            </div>
            <div class="footer">
                <p>&copy; 2024 Veterinaria Patitas Felices. Todos los derechos reservados.</p>
            </div>
        </div>
    </body>
    </html>
    """
        )
        print(msg)
        mail.send(msg)
        return "Correo enviado"
    except Exception as e:
        print("error")
        print(e)
        return f"Ocurrió un error: ${e}"


@app.errorhandler(404)
def not_found(error):
    return 'Ruta no encontrada'


# Arrancando la aplicacion
if __name__ == '__main__':
    app.run(debug=True, port=5000)
# Configura la carpeta de destino para los archivos subidos
app.config['UPLOAD_FOLDER'] = 'static/img'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * \
    1024  # Tamaño máximo de archivo (ej. 16 MB)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Crea la carpeta de destino si no existe
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Connect to the SQLite database (using file.db)
db = SQL("sqlite:///veterinary.db")

# Register route


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        nombre1 = request.form.get("primer_nombre")
        nombre2 = request.form.get("segundo_nombre")
        apellido1 = request.form.get("primer_apellido")
        apellido2 = request.form.get("segundo_apellido")
        cedula = request.form.get("cedula")
        telefono = request.form.get("telefono")
        rol = request.form.get("rol")

        # Check if username, password, or email is missing
        if not username or not password or not email:
            flash("Username, email, and password are required!")
            return redirect("/register")

        # Hash the password for secure storage
        hashed_password = generate_password_hash(password)

        # Attempt to insert the new user
        try:

            id_usuario = db.execute(
                "INSERT INTO Usuarios (username, password, email, rol_id) VALUES (?, ?, ?, ?)", username, hashed_password, email, int(rol))
            db.execute("INSERT INTO Persona (nombre1, nombre2, apellido1, apellido2, cedula, telefono, usuario_id) VALUES (?,?,?,?,?,?,?)",
                       nombre1, nombre2, apellido1, apellido2, cedula, telefono, id_usuario)
            flash("Registration successful! Please log in.")
            return redirect(url_for("main"))
        except Exception as e:
            print(e)
            flash(f"An error occurred: {e}")
            return redirect(url_for("register"))

    return render_template("login.html")

# Login route


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Query the user from the database
        user = db.execute(
            "SELECT * FROM usuarios WHERE username = ?", username)

        # Check if user exists and password is correct
        if user and check_password_hash(user[0]["password"], password):

            usuario_datos = User(user[0]['id_usuario'], user[0]['username'])
            login_user(usuario_datos)

            # Log the user in by setting session variables
            session["id_usuario"] = user[0]["id_usuario"]
            session["username"] = user[0]["username"]

            rol_usuario = db.execute(
                "SELECT R.id_rol, U.email FROM Rol AS R INNER JOIN Usuarios AS U ON U.rol_id = R.id_rol WHERE U.username = ?", user[0]["username"])
            session["id_rol"] = rol_usuario[0]["id_rol"]
            session["email"] = rol_usuario[0]["email"]

            if session["id_rol"] == 3:  # cliente
                return redirect(url_for("main"))

            elif session["id_rol"] == 2:  # veterinario
                return redirect(url_for("proximas_citas"))

            elif session["id_rol"] == 1:  # administrador
                return redirect(url_for("proximas_citas"))
            flash("Login successful!")

        else:
            flash("Invalid username or password.")
            return render_template("login.html")
    else:
        return render_template("login.html")

# Logout route


@app.route("/logout", methods=['POST'])
def logout():
    # Clear the session
    print("entra a log")
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("login"))

# Home route


@app.route("/")
def index():

    return render_template("index.html")


@app.route("/agendar", methods=["GET", "POST"])
@login_required
def agendar():
    if request.method == "POST":
        try:
            # Recuperar datos del formulario
            nombre = request.form.get("nombre")
            raza = request.form.get("raza")
            especie = request.form.get("especie")
            edad = request.form.get("edad")
            color = request.form.get("color")
            servicio = request.form.get("servicio")
            veterinario = request.form.get("veterinario")
            estado = request.form.get("estado")
            disponibilidad = request.form.get("disponibilidad")
            fecha = request.form.get("fecha")
            hora = request.form.get("hora")
            id_usuario = session["id_usuario"]

            newcolor = db.execute("INSERT INTO Color(color) VALUES(?)", color)

            # Insertar o buscar raza

            raza_id = db.execute(
                "INSERT INTO Raza (razanombre) VALUES (?)", raza)

            # Buscar persona relacionada al usuario
            persona_row = db.execute(
                "SELECT id_persona FROM Persona WHERE usuario_id = ?", id_usuario)
            if not persona_row:
                return "Usuario no tiene una persona asociada.", 400
            persona_id = persona_row[0]["id_persona"]
            print(persona_id)
            # Insertar mascota
            mascota_id = db.execute(
                "INSERT INTO Mascotas (nombre, especie_id, edad, persona_id, color_id, estado, raza_id) "
                "VALUES (?, ?, ?, ?, ?, ?, ?) ",
                nombre, int(especie), int(
                    edad), persona_id, newcolor, estado, raza_id
            )

            # Insertar cita
            cita_id = db.execute(
                "INSERT INTO Citas (mascota_id, disponibilidad_id, servicio_id, vet_id, estado, persona_id, fecha, hora) "
                "VALUES (?, ?, ?, ?, ?, ?,?, ?)",
                mascota_id, int(disponibilidad), int(servicio), int(
                    veterinario), estado, int(persona_id), fecha, hora
            )

            mandar_correo(cita_id)

            return redirect("compras")  # Redirigir a la página de citas
        except Exception as e:
            return f"Error al procesar la solicitud: {e}", 500
    else:
        # Cargar datos para el formulario
        try:
            especies = db.execute(
                "SELECT ID_Especie, especie_nombre FROM Especie")
            servicios = db.execute(
                "SELECT ID_Servicio, descripcion, duracion, costo FROM Servicios")
            veterinarios = db.execute(
                "SELECT Veterinarios.ID_Veterinario, Persona.nombre1, Persona.apellido1, Veterinarios.especialidad "
                "FROM Veterinarios JOIN Persona ON Veterinarios.persona_id = Persona.ID_Persona"
            )
            return render_template("agendar.html", especies=especies, servicios=servicios, veterinarios=veterinarios)
        except Exception as e:
            return f"Error al cargar el formulario: {e}", 500


@app.route("/compras", methods=["GET", "POST"])
@login_required
def compras():
    if request.method == "GET":
        # Mostrar productos y categorías (como lo haces actualmente)
        productos = db.execute(
            "SELECT categoria_id, id_producto, nombre, descripcion, preciounitario, stock, imagen_path FROM Productos")
        categorias = db.execute(
            "SELECT C.id_categoria, C.nombre FROM Productos AS P INNER JOIN Categoria AS C ON P.categoria_id = C.id_categoria")
        return render_template("compras.html", productos=productos, categorias=categorias)
    else:
        # Añadir un producto al carrito desde la vista de "compras"
        producto_id = request.form.get("producto_id")
        cantidad = int(request.form.get("cantidad"))

        producto = db.execute(
            "SELECT * FROM Productos WHERE id_producto = ?", producto_id)
        if not producto or producto[0]["stock"] < cantidad:
            flash("No hay suficiente stock disponible.")
            return redirect(url_for("compras"))

        # Añadir el producto al carrito
        total = producto[0]["preciounitario"] * cantidad
        db.execute("""
            INSERT INTO Carrito (usuario_id, producto_id, cantidad, total, estado)
            VALUES (?, ?, ?, ?, 'activo')
        """, session["id_usuario"], producto_id, cantidad, total)

        flash("Producto añadido al carrito.")
        return redirect(url_for("ver_carrito"))


@app.route("/carrito", methods=["GET"])
@login_required
def ver_carrito():
    # Obtener los productos en el carrito del usuario
    carrito = db.execute("""
                            SELECT c.id_carrito,
                            p.nombre,
                            CP.cantidad,
                            p.preciounitario,
                            (CP.cantidad * p.preciounitario) AS total
                        FROM Carrito c
                        INNER JOIN Carrito_productos CP ON CP.carrito_id = c.id_carrito
                        JOIN Productos p ON CP.producto_id = p.id_producto
                        WHERE c.usuario_id = ? AND c.estado = 'activo'

    """, session["id_usuario"])

    # Calcular el total del carrito
    total_general = sum(item["total"] for item in carrito)

    return render_template("carrito.html", carrito=carrito, total=total_general)


@app.route("/producto_carrito", methods=["GET", "POST"])
def guardar_producto_carrito():
    try:
        if request.method == "POST":
            # Obtener datos del formulario
            data = request.get_json()  # Obtén los datos enviados en JSON
            # Accede al dato `producto_id`
            producto_id = int(data.get("producto_id"))
            cantidad = int(data.get("cantidad"))   # Accede al dato `cantidad`
            fecha = date.today()

            print("ID DEL PRODUCTO: "+str(producto_id))
            print("CANTIDAD: "+str(cantidad))
            producto = db.execute(
                "SELECT * FROM Productos WHERE id_producto = ?", producto_id)
            carrito = db.execute(
                "SELECT id_carrito FROM Carrito WHERE usuario_id = ?", session["id_usuario"])

            # Si ya existe un carrito a nombre del usuario, solamente insertar un nuevo producto
            if (carrito):
                print("Entra al primer if")
                try:
                    if (producto[0]["stock"] > 0):

                        ya_existe = db.execute(
                            "SELECT producto_id, cantidad FROM Carrito_productos WHERE producto_id = ? and carrito_id = ?", producto_id, carrito[0]["id_carrito"])
                        if (ya_existe):
                            cantidad_ant = ya_existe[0]["cantidad"]
                            db.execute("UPDATE Carrito_productos SET cantidad=? WHERE producto_id = ? AND carrito_id= ? ",
                                       cantidad_ant+cantidad, producto_id, carrito[0]["id_carrito"])
                        else:
                            db.execute("INSERT INTO Carrito_productos(carrito_id, producto_id, cantidad) VALUES(?,?,?)",
                                       carrito[0]["id_carrito"], producto_id, cantidad)
                except:
                    return jsonify({"error": "No hay stock de este producto", "message": "No hay stock de este producto"})
            else:
                print("Entra al segundo if (esperado)")
                if (len(producto) > 0):
                    print("Entra al segundo if.1 (esperado)")
                    # Solamente inserto producto_id, cantidad y total porque es obligatorio (por el NOT NULL)
                    # Y porque no puedo solamente borrar esas columna, tengo que botar toda la bd
                    # paso
                    db.execute("INSERT INTO Carrito(usuario_id, fecha_creacion, estado, producto_id, cantidad,total ) VALUES(?,?,?,?,?,?)",
                               session["id_usuario"], fecha, "activo", producto_id, 1, 0)
                    id_carrito = db.execute("SELECT last_insert_rowid() AS id_carrito")[
                        0]["id_carrito"]

                    if (producto[0]["stock"] > 0):
                        db.execute(
                            "INSERT INTO Carrito_productos(carrito_id, producto_id, cantidad) VALUES(?,?,?)", id_carrito, producto_id, cantidad)

            return jsonify({"success": True, "message": "Producto añadido al carrito correctamente."})
    except:
        return jsonify({"error": True, "message": "Error al guardar el producto"})


@app.route("/carrito/eliminar/<int:id_carrito>", methods=["POST"])
@login_required
def eliminar_producto_carrito(id_carrito):
    db.execute("""
        DELETE FROM Carrito
        WHERE id_carrito = ? AND usuario_id = ? AND estado = 'activo'
    """, id_carrito, session["id_usuario"])

    flash("Producto eliminado del carrito.")
    return redirect(url_for("ver_carrito"))


@app.route("/carrito/comprar", methods=["POST"])
@login_required
def comprar_carrito():
    # Obtener el carrito activo del usuario
    carrito = db.execute("""
        SELECT c.producto_id, c.cantidad, p.stock
        FROM Carrito c
        JOIN Productos p ON c.producto_id = p.id_producto
        WHERE c.usuario_id = ? AND c.estado = 'activo'""", session["id_usuario"])

    # Verificar stock y actualizar la base de datos
    for item in carrito:
        if item["cantidad"] > item["stock"]:
            flash("No hay suficiente stock para completar la compra.")
            return redirect(url_for("ver_carrito"))

        # Reducir el stock del producto
        db.execute("""
            UPDATE Productos
            SET stock = stock - ?
            WHERE id_producto = ?
        """, item["cantidad"], item["producto_id"])

    # Marcar los items del carrito como comprados
    db.execute("""
        UPDATE Carrito
        SET estado = 'comprado'
        WHERE usuario_id = ? AND estado = 'activo'
    """, session["id_usuario"])

    flash("Compra realizada con éxito.")
    return redirect(url_for("compras"))


@app.route("/perfil", methods=["GET", "POST"])
@login_required
def perfil():
    # Obtener información del dueño
    info_dueno = db.execute("""
        SELECT id_persona, nombre1, nombre2, apellido1, apellido2, telefono, email
        FROM Persona AS P
        INNER JOIN Usuarios AS U ON P.usuario_id = U.id_usuario
        WHERE U.id_usuario = ?
    """, session["id_usuario"])
    id_dueno = info_dueno[0]["id_persona"]

    # Obtener información de las mascotas
    info_mascota = db.execute("""
        SELECT id_mascotas, nombre, especie_nombre, edad, razanombre
        FROM Mascotas
        INNER JOIN Especie ON id_especie = especie_id
        INNER JOIN Raza ON id_raza = raza_id
        WHERE persona_id = ?
    """, id_dueno)

    # Inicializar historial como vacío
    historial = []
    if info_mascota:
        mascota_id = info_mascota[0]["id_mascotas"]
        historial = db.execute("""
            SELECT id_cita, descripcion
            FROM Citas
            INNER JOIN Servicios ON id_servicio = servicio_id
            WHERE mascota_id = ?
        """, mascota_id)

    return render_template("perfil.html", info_dueno=info_dueno, info_mascota=info_mascota, historial=historial)


# Ruta para eliminar la cuenta
@app.route("/eliminar_cuenta", methods=["POST"])
@login_required
def eliminar_cuenta():
    id_usuario = session["id_usuario"]
    db.execute("DELETE FROM Usuarios WHERE id_usuario = ?", id_usuario)
    session.clear()  # Cerrar la sesión
    flash("Cuenta eliminada correctamente.", "success")
    return redirect(url_for("index"))


@app.route("/tienda",  methods=["GET", "POST"])
@login_required
def tienda():
    if request.method == "GET":
        categorias = db.execute("SELECT id_categoria, nombre FROM Categoria")
        productos = db.execute(
            "SELECT id_producto, nombre, descripcion,preciounitario, stock, imagen_path FROM Productos")

        return render_template("tienda.html", categoria=categorias, productos=productos)

    else:
        nombre = request.form.get("nombre")
        tipo = request.form.get("tipo")
        precio = request.form.get("precio")
        descripcion = request.form.get("descripcion")
        stock = request.form.get("cantidad")

        if "img_producto" not in request.files:
            print("No subió una img")
            return redirect(url_for("tienda"))

        archivo = request.files["img_producto"]

        # Verifica si se ha seleccionado un archivo
        if archivo.filename == "":
            print("La img no tiene nombre")
            return redirect(url_for("tienda"))

        ruta_imagen = subir_imagen(archivo)
        db.execute("INSERT INTO productos (nombre, descripcion, stock, categoria_id, preciounitario, imagen_path) VALUES (?, ?, ?, ?, ?, ?)",
                   nombre, descripcion, stock, tipo, precio, ruta_imagen)

        return redirect(url_for("compras"))


@app.route("/servicios")
def servicios():
    try:
        servicios = db.execute("SELECT * FROM Servicios")
        return render_template("servicios.html", servicios=servicios, session=session)
    except Exception as e:
        flash("Hubo un error al cargar los servicios.", "danger")
        print(f"Error: {e}")
        return render_template("servicios.html", servicios=servicios, session=session)

# Ruta para editar un servicio


@app.route("/editar/<int:id_servicio>", methods=["GET", "POST"])
def editar(id_servicio):
    if request.method == "GET":
        # Obtener los datos actuales del servicio
        servicio = db.execute(
            "SELECT * FROM Servicios WHERE id_servicio = ?", (id_servicio,))
        if not servicio:
            flash("No se encontró el servicio.", "danger")
            return redirect(url_for("servicios"))

        servicio = servicio[0]  # Seleccionar el primer resultado
        return render_template(
            "editar.html",
            id_servicio=servicio["id_servicio"],
            descripcion=servicio["descripcion"],
            costo=servicio["costo"],
            duracion=servicio["duracion"],
        )

    elif request.method == "POST":
        # Obtener datos desde el formulario
        descripcion = request.form.get("descripcion")
        costo = request.form.get("costo")
        duracion = request.form.get("duracion")
        print(id_servicio)

        try:
            # Actualizar el servicio en la base de datos
            print("hola")
            print(descripcion, costo, duracion)
            db.execute(
                '''
                UPDATE Servicios
                SET descripcion = ?, costo = ?, duracion = ?
                WHERE id_servicio = ?
                ''',
                descripcion, float(costo), duracion, id_servicio,
            )
            flash("El servicio ha sido actualizado con éxito.", "success")
        except Exception as e:
            flash("Hubo un error al actualizar el servicio.", "danger")
            print(f"Error al actualizar servicio: {e}")

        return redirect(url_for("servicios"))


@app.route("/Control_usuario")
@login_required
def Control_usuario():
    Usuarios = db.execute(
        "SELECT Usuarios.username, Usuarios.email, Persona.telefono FROM Persona INNER JOIN Usuarios ON Persona.usuario_id = Usuarios.id_usuario")
    return render_template("Usuarios.html", Usuarios=Usuarios)


"""
@app.route("/adopciones_disponibles")
@login_required
def adopciones_disponibles():
    return render_template("adopciones_disponibles.html")
"""


@app.route('/veterinarios', methods=['GET', 'POST'])
def veterinarios():
    try:
        # Ejecutar consulta para obtener datos de los veterinarios
        veterinarios = db.execute('''
            SELECT
                Veterinarios.id_veterinario,
                CONCAT_WS(' ', Persona.nombre1, Persona.nombre2, Persona.apellido1, Persona.apellido2) AS nombre,
                Veterinarios.especialidad,
                Veterinarios.estado,
                Persona.telefono,
                Persona.cedula
            FROM
                Veterinarios
            INNER JOIN
                Persona
            ON
                Veterinarios.persona_id = Persona.id_persona;
        ''')

        # Renderizar la plantilla con los datos obtenidos
        return render_template("veterinarios.html", veterinarios=veterinarios)
    except Exception as e:
        flash("Hubo un error al obtener los datos de los veterinarios.", "danger")
        print(f"Error: {e}")
        return redirect(url_for("veterinarios"))


@app.route("/editar_veterinario/<int:id_veterinario>", methods=["GET", "POST"])
def editar_veterinario(id_veterinario):
    if request.method == "GET":
        print(id_veterinario)
        # Consultar los datos del veterinario
        veterinario = db.execute('''
                SELECT
                    Veterinarios.id_veterinario,
                    Veterinarios.especialidad,
                    Persona.id_persona,
                    Persona.nombre1,
                    Persona.nombre2,
                    Persona.apellido1,
                    Persona.apellido2,
                    Persona.cedula,
                    Persona.telefono
                FROM
                    Veterinarios
                INNER JOIN
                    Persona
                ON
                    Veterinarios.persona_id = Persona.id_persona
                WHERE Veterinarios.id_veterinario = ?;
            ''', (id_veterinario,))

        # Validar que se encontró el veterinario
        if not veterinario:
            print("entra a no vet")

            flash("No se encontró el veterinario especificado.", "danger")
            return redirect(url_for("veterinarios"))

        # Pasar los datos a la plantilla
        return render_template("editar_veterinario.html", veterinario=veterinario, id_veterinario=id_veterinario)

    elif request.method == "POST":

        # Obtener los datos del formulario
        nombre1 = request.form.get("nombre1")
        nombre2 = request.form.get("nombre2")
        apellido1 = request.form.get("apellido1")
        apellido2 = request.form.get("apellido2")
        cedula = request.form.get("cedula")
        telefono = request.form.get("telefono")
        especialidad = request.form.get("especialidad")
        id_persona = db.execute(
            "SELECT persona_id FROM Veterinarios WHERE id_veterinario = ? ", id_veterinario)
        # Actualizar en la tabla `Persona`
        persona_id =  id_persona[0]["persona_id"]
        db.execute('''
                UPDATE Persona
                SET
                    nombre1 = ?,
                    nombre2 = ?,
                    apellido1 = ?,
                    apellido2 = ?,
                    cedula = ?,
                    telefono = ?
                WHERE id_persona = ?

            ''', nombre1, nombre2, apellido1, apellido2, cedula, telefono,persona_id)

        # Actualizar en la tabla `Veterinarios`
        db.execute('''
                UPDATE Veterinarios
                SET especialidad = ?
                WHERE id_veterinario = ?
            ''', especialidad, id_veterinario)

        flash("El veterinario ha sido actualizado con éxito.", "success")
        return redirect(url_for("veterinarios"))


@app.route("/cambiar_estado_servicio/<int:id_servicio>", methods=["POST"])
def cambiar_estado_servicio(id_servicio):
    if request.method == "POST":
        estado = request.form.get("estado")
        if estado == "activo":
            nuevo_estado = "inactivo"
        else:
            nuevo_estado = "activo"
        db.execute("UPDATE Servicios SET estado = ?  WHERE id_servicio = ?",
                   nuevo_estado, id_servicio)
        return redirect(url_for("servicios"))


@app.route("/cambiar_estado_veterinario/<int:id_veterinario>", methods=["POST"])
def cambiar_estado_veterinario(id_veterinario):
    try:
        # Consultar el estado actual del veterinario
        resultado = db.execute(
            "SELECT estado FROM Veterinarios WHERE id_veterinario = ?", id_veterinario)
        if not resultado:
            flash("No se encontró el veterinario especificado.", "danger")
            return redirect(url_for("veterinarios"))

        estado_actual = resultado[0]["estado"]

        # Cambiar el estado al opuesto
        nuevo_estado = "inactivo" if estado_actual == "activo" else "activo"

        # Actualizar el estado en la base de datos
        db.execute("UPDATE Veterinarios SET estado = ? WHERE id_veterinario = ?",nuevo_estado, id_veterinario)
        flash(f"El estado del veterinario ha sido cambiado a {nuevo_estado}.", "success")
    except Exception as e:
        flash("Hubo un error al cambiar el estado del veterinario.", "danger")
        print(f"Error al cambiar estado: {e}")

    return redirect(url_for("veterinarios"))


@app.route("/main")
def main():
    return render_template("main.html")


@app.route("/proximas_citas")
@login_required
def proximas_citas():
    citas = db.execute('''SELECT (P.nombre1 || " " ||  P.nombre2) AS nombres , ( P.apellido1 || " " ||   P.apellido2) AS apellidos , M.nombre, E.especie_nombre, R.razanombre, (p2.nombre1 || " " || p2.nombre2 || " " || p2.apellido1 || " " || p2.apellido2) AS Veterinario FROM Persona P
                    INNER JOIN Mascotas M ON M.persona_id = P.id_persona
                    INNER JOIN Especie E ON E.id_especie = M.especie_id
                    INNER JOIN Raza R ON R.id_raza = M.raza_id
                    INNER JOIN Citas C on C.mascota_id = M.id_mascotas
                    INNER JOIN Veterinarios v ON C.vet_id = v.id_veterinario
                    inner join Persona P2 ON v.persona_id = P2.id_persona''')
    print(citas)
    return render_template("solicitud_citas.html", citas=citas)


@app.route("/historial_mascotas")
def historial_mascotas():
    mascotas = db.execute('''SELECT
    Mascotas.nombre,
    Especie.especie_nombre,
    Raza.razanombre,
    Color.color,
    Mascotas.estado,
    Mascotas.edad
FROM
    Mascotas
INNER JOIN
    Especie
ON
    Especie.id_especie = Mascotas.especie_id
INNER JOIN
    Raza
ON
    Raza.id_raza = Mascotas.raza_id
INNER JOIN
    Color
ON
    color.id_color=Mascotas.color_id''')

    return render_template("historial_mascotas.html",   mascotas=mascotas)


@app.route("/eliminar_producto", methods=["GET", "POST"])
def eliminar_producto():
    if request.method == "POST":
        id_producto = request.form.get("id_producto")
        db.execute("DELETE FROM Productos WHERE id_producto = ?", id_producto)
        return redirect(url_for("tienda"))


def subir_imagen(archivo):

    if archivo and allowed_file(archivo.filename):
        nombre_archivo = archivo.filename
        ruta_archivo = os.path.join(
            app.config['UPLOAD_FOLDER'], nombre_archivo)
        archivo.save(ruta_archivo)
        return ruta_archivo
    else:
        flash('Tipo de archivo no permitido')
        return redirect(url_for("tienda"))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# CLASE USER ADAPTADA A LAS NECESIDADES DE NUESTRO PROYECTO


class User(UserMixin):
    def __init__(self, id_usuario, username):
        self.id = id_usuario
        self.username = username

# USado para el login required


@login_manager.user_loader
def load_user(user_id):
    # Aquí debes cargar el usuario desde tu base de datos
    user = db.execute("SELECT * FROM usuarios WHERE id_usuario = ?", user_id)
    if user:
        return User(user[0]['id_usuario'], user[0]['username'])
    return None


if __name__ == "_main_":
    app.run(debug=True)
