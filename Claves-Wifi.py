import subprocess

def get_wifi_passwords():
    try:
        profiles_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'], text=True, encoding='utf-8')
        profiles = [
            line.split(":")[1].strip()
            for line in profiles_data.split('\n')
            if "Perfil de usuario actual" in line or "Perfil de todos los usuarios" in line
        ]

        wifi_list = []

        for wifi_name in profiles:
            try:
                profile_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', wifi_name, 'key=clear'], text=True, encoding='utf-8')
                if "Contenido de la clave" in profile_data:
                    password = [
                        line.split(":")[1].strip()
                        for line in profile_data.split('\n')
                        if "Contenido de la clave" in line
                    ][0]
                else:
                    password = "Sin contraseña"
                wifi_list.append((wifi_name, password))
            except subprocess.CalledProcessError:
                wifi_list.append((wifi_name, "Error al obtener contraseña"))

        return wifi_list

    except Exception as e:
        print(f"Error al obtener perfiles de Wi-Fi: {e}")
        return []

# Mostrar las redes Wi-Fi y sus contraseñas (Output limpio)
wifi_passwords = get_wifi_passwords()

if wifi_passwords:
    print("\nRedes Wi-Fi guardadas:\n")
    for wifi in wifi_passwords:
        print(f"- {wifi[0]}: {wifi[1]}")
else:
    print("No se encontraron redes Wi-Fi guardadas.")
