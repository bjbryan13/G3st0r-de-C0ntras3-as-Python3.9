from cryptography.fernet import Fernet
import hashlib
import json
import base64

# Funciones de encriptación y desencriptación
def generate_key():
    return Fernet.generate_key()

def encrypt_data(data, key):
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    return encrypted_data

def decrypt_data(encrypted_data, key):
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data).decode()
    return decrypted_data

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_password(key):
    website = input("Ingrese el sitio web: ")
    username = input("Ingrese el nombre de usuario: ")
    password = input("Ingrese la contraseña: ")

    hashed_password = hash_password(password)
    encrypted_password = encrypt_data(hashed_password, key)

    if website in passwords:
        passwords[website].append({"username": username, "password": encrypted_password})
    else:
        passwords[website] = [{"username": username, "password": encrypted_password}]

    print("Contraseña añadida exitosamente.")

def show_all_passwords(key):
    if passwords:
        print("Contraseñas almacenadas:")
        for website, credentials in passwords.items():
            print(f"Sitio web: {website}")
            for credential in credentials:
                decrypted_password = decrypt_data(credential['password'], key)
                print(f"Usuario: {credential['username']}\nContraseña: {decrypted_password}")
            print("-----------")
    else:
        print("No hay contraseñas almacenadas.")

def save_passwords(filename, key):
    with open(filename, 'w') as file:
        serialized_passwords = {}
        for website, credentials in passwords.items():
            serialized_credentials = []
            for credential in credentials:
                decrypted_password = decrypt_data(credential['password'], key)
                serialized_credentials.append({
                    'username': credential['username'],
                    'password': base64.b64encode(decrypted_password.encode()).decode()
                })
            serialized_passwords[website] = serialized_credentials

        json.dump(serialized_passwords, file)

def load_passwords(filename, key):
    try:
        with open(filename, 'r') as file:
            serialized_passwords = json.load(file)
            loaded_passwords = {}
            for website, credentials in serialized_passwords.items():
                loaded_credentials = []
                for credential in credentials:
                    decrypted_password = base64.b64decode(credential['password']).decode()
                    encrypted_password = encrypt_data(decrypted_password, key)
                    loaded_credentials.append({
                        'username': credential['username'],
                        'password': encrypted_password
                    })
                loaded_passwords[website] = loaded_credentials
            return loaded_passwords
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def get_key():
    try:
        with open("key.key", "rb") as file:
            return file.read()
    except FileNotFoundError:
        key = generate_key()
        with open("key.key", "wb") as file:
            file.write(key)
        return key

def get_password(key):
    website = input("Ingrese el sitio web: ")
    if website in passwords:
        print(f"Contraseñas para {website}:")
        credentials = passwords[website]
        for index, credential in enumerate(credentials):
            decrypted_password = decrypt_data(credential['password'], key)
            print(f"#{index + 1} - Usuario: {credential['username']}\nContraseña: {decrypted_password}")
        
        choice = input("Ingrese el número de la contraseña que desea obtener: ")
        try:
            index = int(choice) - 1
            if 0 <= index < len(credentials):
                selected_credential = credentials[index]
                decrypted_password = decrypt_data(selected_credential['password'], key)
                print(f"Sitio web: {website}\nUsuario: {selected_credential['username']}\nContraseña: {decrypted_password}")
            else:
                print("Selección inválida.")
        except ValueError:
            print("Por favor, ingrese un número válido.")
    else:
        print("El sitio web no está en la base de datos.")

def delete_password(key):
    website = input("Ingrese el sitio web para eliminar la contraseña: ")
    if website in passwords:
        credentials = passwords[website]
        if len(credentials) > 1:
            print(f"Contraseñas para {website}:")
            for index, credential in enumerate(credentials):
                decrypted_password = decrypt_data(credential['password'], key)
                print(f"#{index + 1} - Usuario: {credential['username']}\nContraseña: {decrypted_password}")
            
            choice = input("Ingrese el número de la contraseña que desea eliminar: ")
            try:
                index = int(choice) - 1
                if 0 <= index < len(credentials):
                    del credentials[index]
                    print("Contraseña eliminada exitosamente.")
                else:
                    print("Selección inválida.")
            except ValueError:
                print("Por favor, ingrese un número válido.")
        else:
            del passwords[website]
            print("Única contraseña para este sitio eliminada exitosamente.")
    else:
        print("El sitio web no está en la base de datos.")

def main():
    key = get_key()
    global passwords
    passwords = load_passwords("passwords.txt", key)
    
    while True:
        print("\nBienvenido al gestor de contraseñas")
        print("1. Añadir contraseña")
        print("2. Obtener contraseña")
        print("3. Eliminar contraseña")
        print("4. Mostrar todas las contraseñas")
        print("5. Guardar y salir")
        
        choice = input("Ingrese el número de la opción que desea realizar: ")
        
        if choice == '1':
            add_password(key)
        elif choice == '2':
            get_password(key)
        elif choice == '3':
            delete_password(key)
        elif choice == '4':
            show_all_passwords(key)
        elif choice == '5':
            save_passwords("passwords.txt", key)
            print("¡Contraseñas guardadas con éxito! ¡Hasta luego!")
            break
        else:
            print("Opción inválida. Por favor, elija una opción válida.")

if __name__ == "__main__":
    main()
