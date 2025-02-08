# Veterinaria Patitas Felices
#### Video Demo: [https://youtu.be/nmGf1JDhicE](https://youtu.be/nmGf1JDhicE)
#### Description:
Este proyecto es una plataforma web para una veterinaria que facilita la gestión de citas, servicios y productos en línea.

### Funcionalidades Principales:
- **Gestión de usuarios**: Registro y control de usuarios con diferentes roles (administrador, veterinario y cliente).
- **Agendamiento de citas**: Los usuarios pueden agendar citas para sus mascotas, especificando el servicio deseado y recibiendo confirmación por correo electrónico.
- **Tienda en línea**: Permite la compra de productos veterinarios, incluye carrito de compras, control de stock y categorías.
- **Historial de mascotas**: Los usuarios pueden consultar información y servicios previos de sus mascotas.
- **Administración de servicios y veterinarios**: Edición, activación/inactivación y consulta de servicios y datos de veterinarios.

### Tecnologías Utilizadas:
1. **Back-End**:
   - **Flask**: Framework para crear y gestionar la aplicación web.
   - **SQLite**: Base de datos para almacenar información sobre usuarios, mascotas, servicios, productos y citas.
   - **Flask-Mail**: Para enviar correos electrónicos de confirmación.

2. **Front-End**:
   - **HTML**: Se utilizaron plantillas dinámicas para renderizar páginas de usuario y administrador.
   - **CSS**: Para el diseño visual y estilos personalizados, se incluyeron hojas de estilo propias y librerías como Bootstrap para un diseño responsivo.
   - **JavaScript**: Utilizado para funcionalidades interactivas, validaciones en tiempo real y manejo dinámico del DOM.
   - **Jinja2**: Motor de plantillas de Flask para integrar datos dinámicos en HTML.

3. **Otros**:
   - **Bootstrap**: Framework CSS para diseños modernos y responsivos.
   - **Werkzeug Security**: Gestión segura de contraseñas utilizando hashing.

### Descripción Técnica:
- **Plantillas HTML**: Cada página de la aplicación utiliza plantillas diseñadas con Jinja2, que integran datos dinámicos enviados desde el servidor.
- **JavaScript**: Implementado para mejorar la experiencia del usuario en la tienda en línea, como la validación de formularios, la actualización dinámica de precios en el carrito y el manejo de interacciones asincrónicas con el servidor.
- **CSS**: Se desarrollaron estilos personalizados para la identidad visual de la veterinaria, además de usar Bootstrap para garantizar un diseño amigable y adaptado a dispositivos móviles.

Este proyecto busca optimizar la experiencia tanto para los clientes como para el personal administrativo de la veterinaria, haciendo más eficiente la gestión de citas y servicios.

