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
username = os.getenv("campus_user")
password = os.getenv("campus_pwd")

# Configurar el WebDriver
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

# Obtener la ruta de la carpeta Documentos
documents_path = os.path.join(os.path.expanduser("~"), "Documents", "Estudiantes Cursos")

# Crear la carpeta si no existe
if not os.path.exists(documents_path):
    os.makedirs(documents_path)

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

def obtener_nombre_curso():
    """Extrae el nombre del curso desde la página."""
    try:
        titulo_elemento = driver.find_element(By.XPATH, "//div[@class='titles']/h2")
        return titulo_elemento.text.strip().replace(" ", "_").replace(",", "")
    except:
        return "Curso_Desconocido"

try:
    # Ir a la página de login
    driver.get("https://campus.elhubdeseguridad.com/wp-login.php")
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "user_login")))

    # Ingresar credenciales
    driver.find_element(By.ID, "user_login").send_keys(username)
    driver.find_element(By.ID, "user_pass").send_keys(password)
    driver.find_element(By.ID, "wp-submit").click()

    # Esperar redirección
    WebDriverWait(driver, 18).until(EC.url_contains("wp-admin"))

    # Crear el archivo CSV donde se almacenarán todos los datos
    file_path = os.path.join(documents_path, "Estudiantes_Cursos.csv")
    
    # Abrir el archivo en modo de escritura
    with open(file_path, mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["Nombre", "Email", "Comenzó", "Progreso", "Curso"])

        for url in urls:
            # Abrir una nueva pestaña con la URL
            driver.execute_script(f"window.open('{url}', '_blank');")
            time.sleep(2)
            driver.switch_to.window(driver.window_handles[-1])

            # Esperar que cargue la página del curso
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "name")))

            # Obtener nombre del curso
            nombre_curso = obtener_nombre_curso()

            # Extraer datos de estudiantes
            filas = driver.find_elements(By.XPATH, "//table//tr")
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
                    tiempo = fila.find_element(By.CLASS_NAME, "time").text.replace("hace", "").strip()
                except:
                    tiempo = "No encontrado"

                try:
                    progress_bar = fila.find_element(By.XPATH, ".//div[contains(@class, 'progress-bar')]")
                    progreso = progress_bar.get_attribute("style").split("width:")[1].strip().replace(";", "") if "width:" in progress_bar.get_attribute("style") else "No encontrado"
                except:
                    progreso = "No encontrado"

                # Añadir la fila con el nombre del curso
                curso_datos.append([nombre, email, tiempo, progreso, nombre_curso])

            # Escribir los datos de los estudiantes en el archivo CSV
            writer.writerows(curso_datos)
            print(f"Datos de {url} guardados en {file_path} ✅")

            # Cerrar la pestaña y volver a la original
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

except Exception as e:
    print("Error:", e)

finally:
    driver.quit()
    print("Navegador cerrado.")
