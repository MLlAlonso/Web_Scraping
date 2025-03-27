import csv
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

# Cargar las variables de entorno del archivo .env
load_dotenv()

# Leer las credenciales del archivo .env
username = os.getenv("campus_user")  # Usando campus_user
password = os.getenv("campus_pwd")  # Usando campus_pwd

# Verificar que las credenciales se están cargando correctamente
print(f"USERNAME: {username}")
print(f"PASSWORD: {password}")

# Configurar el WebDriver
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

# Lista de URLs de los cursos
urls = [
    "https://campus.elhubdeseguridad.com/wp-admin/?page=stm-lms-dashboard#/course/8841",
    "https://campus.elhubdeseguridad.com/wp-admin/?page=stm-lms-dashboard#/course/10388",
    "https://campus.elhubdeseguridad.com/wp-admin/?page=stm-lms-dashboard#/course/9692",
    "https://campus.elhubdeseguridad.com/wp-admin/?page=stm-lms-dashboard#/course/10481",
    "https://campus.elhubdeseguridad.com/wp-admin/?page=stm-lms-dashboard#/course/11089",
    "https://campus.elhubdeseguridad.com/wp-admin/?page=stm-lms-dashboard#/course/11187",
    "https://campus.elhubdeseguridad.com/wp-admin/?page=stm-lms-dashboard#/course/11357",
    "https://campus.elhubdeseguridad.com/wp-admin/?page=stm-lms-dashboard#/course/11712",
    "https://campus.elhubdeseguridad.com/wp-admin/?page=stm-lms-dashboard#/course/12302",
    "https://campus.elhubdeseguridad.com/wp-admin/?page=stm-lms-dashboard#/course/12822",
    "https://campus.elhubdeseguridad.com/wp-admin/?page=stm-lms-dashboard#/course/12914",
    "https://campus.elhubdeseguridad.com/wp-admin/?page=stm-lms-dashboard#/course/13342"
]

# Ruta relativa donde se guardarán los archivos CSV
folder_path = os.path.join(os.getcwd(), "cursos_csv")

# Crear la carpeta si no existe
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

def obtener_nombre_curso(driver):
    """ Extrae el nombre del curso desde el bloque HTML """
    try:
        titulo_elemento = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.titles h2"))
        )
        return titulo_elemento.text.strip().replace(",", "")  # Remover comas para evitar errores en el CSV
    except:
        return "Curso_Desconocido"

try:
    # Ir a la página de login
    driver.get("https://campus.elhubdeseguridad.com/wp-login.php?redirect_to=https%3A%2F%2Fcampus.elhubdeseguridad.com%2Fwp-admin%2F&reauth=1")
    print("Abriendo la página...")

    # Esperar a que los campos de login sean visibles
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "user_login")))
    print("Página cargada. Buscando campos de inicio de sesión...")

    # Introducir credenciales desde las variables de entorno
    driver.find_element(By.ID, "user_login").send_keys(username)
    driver.find_element(By.ID, "user_pass").send_keys(password)

    # Enviar formulario
    driver.find_element(By.ID, "wp-submit").click()
    print("Enviando formulario de inicio de sesión...")

    # Esperar la redirección después del login
    WebDriverWait(driver, 18).until(EC.url_contains("wp-admin"))
    print("URL actual después del login:", driver.current_url)

    # Abrir nuevas pestañas y recorrer las URLs
    for index, url in enumerate(urls):
        # Abrir una nueva pestaña con la URL
        driver.execute_script(f"window.open('{url}', '_blank');")
        time.sleep(2)  # Esperar un poco para que la nueva pestaña se cargue

        # Cambiar a la nueva pestaña
        driver.switch_to.window(driver.window_handles[-1])

        # Esperar que la tabla cargue correctamente
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "name")))
        print(f"Extrayendo datos del curso: {url}")

        # Obtener el nombre del curso
        nombre_curso = obtener_nombre_curso(driver)

        # Obtener todas las filas de la tabla
        filas = driver.find_elements(By.XPATH, "//table//tr")

        # Guardar los datos del curso en la lista
        curso_datos = []

        for fila in filas:
            try:
                nombre = fila.find_element(By.CLASS_NAME, "author__info").text
            except:
                nombre = "No encontrado"

            try:
                email = fila.find_element(By.CLASS_NAME, "email").text
            except:
                email = "No encontrado"

            try:
                tiempo = fila.find_element(By.CLASS_NAME, "time").text
                tiempo = tiempo.replace("hace", "").strip()  # Eliminar la palabra "hace" y limpiar espacios
            except:
                tiempo = "No encontrado"

            try:
                # Buscar el progreso dentro de la fila basado en la clase específica
                progress_bar = fila.find_element(By.XPATH, ".//div[contains(@class, 'progress-bar')]")
                progreso = progress_bar.get_attribute("style")  # Extraer el atributo "style"

                # Extraer el valor numérico del width
                progreso = progreso.split("width:")[1].strip().replace(";", "") if "width:" in progreso else "No encontrado"
            except:
                progreso = "No encontrado"

            # Guardar los datos en la lista de curso
            curso_datos.append([nombre, email, tiempo, progreso])

        # Guardar los datos en un archivo CSV con el nombre del curso
        file_name = f"Estudiantes_Curso_{nombre_curso}.csv"
        file_path = os.path.join(folder_path, file_name)

        with open(file_path, mode="w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow(["Nombre", "Email", "Comenzó", "Progreso"])  # Encabezados
            writer.writerows(curso_datos)  # Escribir los datos

        print(f"Datos de {nombre_curso} guardados en {file_path} ✅")

        # Cambiar a la primera pestaña para continuar con la siguiente URL
        driver.switch_to.window(driver.window_handles[0])

except Exception as e:
    print("Error:", e)

finally:
    # Cerrar todas las pestañas y el navegador
    driver.quit()
    print("Navegador cerrado.")
