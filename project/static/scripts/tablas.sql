CREATE TABLE Rol (id_rol INT AUTOINCREMENT PRIMARY KEY,
    rol text);

CREATE TABLE Usuarios (id_usuario INTEGER AUTOINCREMENT PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    rol_id INTEGER,
    FOREIGN KEY (rol_id) REFERENCES Rol (id_rol));

CREATE TABLE Persona (id_persona INTEGER AUTOINCREMENT PRIMARY KEY,
        nombre1 text NOT NULL,
        nombre2 text NOT NULL,
        apellido1 text NOT NULL,
        apellido2 text NOT NULL,
        cedula text NOT NULL UNIQUE,
        telefono NUMERIC NOT NULL UNIQUE,
        usuario_id INTEGER NOT NULL UNIQUE,
        FOREIGN key (usuario_id) REFERENCES Usuarios (id_usuario)
    );

CREATE TABLE Categoria (id_categoria INTEGER AUTOINCREMENT PRIMARY KEY,
        nombre text NOT NULL,
        descripcion text NOT NULL
    );

CREATE TABLE Productos (id_producto INTEGER AUTOINCREMENT PRIMARY KEY,
        nombre text NOT NULL,
        descripcion text NOT NULL,
        stock INTEGER NOT NULL,
        categoria_id INTEGER NOT NULL,
        preciounitario DECIMAL NOT NULL,
        FOREIGN KEY (categoria_id) REFERENCES Categoria (id_categoria)
    );

CREATE TABLE Carrito (id_carrito INTEGER AUTOINCREMENT PRIMARY KEY,
        usuario_id INTEGER NOT NULL UNIQUE,
        fecha_creacion DATE NOT NULL,
        estado text NOT NULL,
        producto_id INTEGER NOT NULL,
        cantidad INTEGER NOT NULL,
        total decimal NOT NULL,
        FOREIGN key (usuario_id) REFERENCES Usuarios (id_usuario),
        FOREIGN key (producto_id) REFERENCES Productos (id_producto)
    );

--------
CREATE TABLE Servicios (id_servicio INTEGER AUTOINCREMENT PRIMARY KEY,
        descripcion text NOT NULL,
        duracion text NOT NULL,
        costo DECIMAL NOT NULL
    );

CREATE TABLE Disponibilidad (id_disponibilidad INTEGER AUTOINCREMENT PRIMARY KEY,
        estado BOOLEAN NOT NULL
        -- 1 es igual a disponible y 0 es igual a no disponible--
    );

CREATE TABLE Veterinarios (id_veterinario AUTOINCREMENT PRIMARY KEY,
        persona_id INTEGER NOT NULL,
        especialidad text NOT NULL,
        disponibilidad_id INTEGER NOT NULL,
        FOREIGN KEY (persona_id) REFERENCES Persona (id_persona),
        FOREIGN KEY (disponibilidad_id) REFERENCES Disponibilidad (id_disponibilidad)
    );

CREATE TABLE Raza (id_raza INTEGER AUTOINCREMENT,
        razanombre text,
        PRIMARY key (id_raza)
    );

CREATE TABLE Especie (id_especie INTEGER AUTOINCREMENT PRIMARY KEY,
        especie_nombre text NOT NULL,
        raza_id INTEGER NOT NULL,
        FOREIGN KEY (raza_id) REFERENCES Raza (id_raza)
    );

CREATE TABLE Mascotas (id_mascotas INTEGER AUTOINCREMENT PRIMARY KEY,
        nombre text NOT NULL,
        especie_id INTEGER NOT NULL,
        edad DATE NOT NULL,
        persona_id INTEGER NOT NULL,
        color_id INTEGER NOT NULL,
        estado text NOT NULL,
        FOREIGN KEY (especie_id) REFERENCES Especie (id_especie),
        FOREIGN KEY (persona_id) REFERENCES Persona (id_persona),
        FOREIGN KEY (color_id) REFERENCES Color (id_color)
    );

CREATE TABLE Color (id_color INTEGER AUTOINCREMENT PRIMARY KEY,
        color text NOT NULL
    );

CREATE TABLE
    Citas (id_cita INTEGER AUTOINCREMENT PRIMARY KEY,
        mascota_id INTEGER NOT NULL,
        disponibilidad_id INTEGER NOT NULL,
        servicio_id INTEGER NOT NULL,
        estado text NOT NULL,
        total NUMERIC NOT NULL,
        persona_id INTEGER NOT NULL,
        FOREIGN KEY (mascota_id) REFERENCES Mascotas (id_mascota),
        FOREIGN KEY (disponibilidad_id) REFERENCES Disponibilidad (id_disponibilidad),
        FOREIGN KEY (servicio_id) REFERENCES Servicios (id_servicio)
    );

CREATE TABLE
    Solicitudes_adopcion (id_solicitud INTEGER AUTOINCREMENT PRIMARY KEY,
        mascota_id INTEGER NOT NULL,
        usuario_id INTEGER NOT NULL,
        observaciones text NOT NULL,
        estado text NOT NULL,
        FOREIGN KEY (mascota_id) REFERENCES Mascotas (id_mascota),
        FOREIGN KEY (usuario_id) REFERENCES Usuarios (id_usuario)
    );
