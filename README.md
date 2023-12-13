# G3st0r-de-C0ntras3-as-Python3.9
# Gestor de Contraseñas
dev bryantreze

Este es un gestor de contraseñas simple creado en Python. Permite almacenar y gestionar contraseñas de manera segura utilizando cifrado Fernet y funciones hash.

## Características

- **Añadir Contraseña:** Permite agregar una nueva contraseña para un sitio web junto con el nombre de usuario.
- **Obtener Contraseña:** Recupera y muestra las contraseñas almacenadas para un sitio web específico.
- **Eliminar Contraseña:** Elimina una contraseña asociada a un sitio web.
- **Mostrar Todas las Contraseñas:** Muestra todas las contraseñas almacenadas.
- **Guardar y Salir:** Guarda los cambios realizados y cierra el gestor de contraseñas.

## Requisitos

- Python 3.x
- Instalar los paquetes requeridos:
  ```bash
  pip install cryptography


En caso de error eliminar los archivos .key y .txt que se generan
