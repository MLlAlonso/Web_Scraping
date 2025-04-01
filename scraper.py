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

# Ruta de la carpeta Documentos
documents_path = os.path.join(os.path.expanduser("~"), "Documents", "Estudiantes Cursos")
os.makedirs(documents_path, exist_ok=True)

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

def obtener_nombre_curso(driver):
    """Extrae el nombre del curso desde la página."""
    try:
        titulo_elemento = driver.find_element(By.XPATH, "//div[@class='titles']/h2")
        return titulo_elemento.text.strip().replace(" ", "_").replace(",", "").replace("Estudiantes_de", "").strip()
    except:
        return "Curso_Desconocido"

def extraer_datos_estudiantes(driver):
    """Extrae los datos de los estudiantes desde la tabla."""
    estudiantes = []
    filas = driver.find_elements(By.XPATH, "//table//tr")
    for fila in filas:
        try:
            nombre = fila.find_element(By.CLASS_NAME, "author__info").text
            if nombre == "Usuario eliminado":
                continue
        except:
            continue

        email = fila.find_element(By.CLASS_NAME, "email").text if fila.find_elements(By.CLASS_NAME, "email") else "No encontrado"
        tiempo = fila.find_element(By.CLASS_NAME, "time").text.replace("hace", "").strip() if fila.find_elements(By.CLASS_NAME, "time") else "No encontrado"
        progreso = "No encontrado"
        try:
            progress_bar = fila.find_element(By.XPATH, ".//div[contains(@class, 'progress-bar')]")
            if "width:" in progress_bar.get_attribute("style"):
                progreso = progress_bar.get_attribute("style").split("width:")[1].strip().replace(";", "")
        except:
            pass

        estudiantes.append([nombre, email, tiempo, progreso])
    return estudiantes

def iniciar_sesion(driver, username, password):
    """Inicia sesión en la plataforma."""
    driver.get("https://campus.elhubdeseguridad.com/wp-login.php")
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "user_login")))
    driver.find_element(By.ID, "user_login").send_keys(username)
    driver.find_element(By.ID, "user_pass").send_keys(password)
    driver.find_element(By.ID, "wp-submit").click()
    WebDriverWait(driver, 18).until(EC.url_contains("wp-admin"))

def procesar_cursos(driver, urls, file_path):
    """Procesa cada curso y guarda los datos en un archivo CSV."""
    with open(file_path, mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["Nombre", "Email", "Inicio", "Progreso", "Curso"])

        for url in urls:
            driver.execute_script(f"window.open('{url}', '_blank');")
            time.sleep(2)
            driver.switch_to.window(driver.window_handles[-1])

            try:
                WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "name")))
                nombre_curso = obtener_nombre_curso(driver)
                estudiantes = extraer_datos_estudiantes(driver)
                for estudiante in estudiantes:
                    writer.writerow(estudiante + [nombre_curso])
                print(f"Datos de {url} guardados en {file_path} ✅")
            except Exception as e:
                print(f"Error procesando {url}: {e}")
            finally:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

try:
    iniciar_sesion(driver, username, password)
    file_path = os.path.join(documents_path, "Estudiantes_Cursos.csv")
    procesar_cursos(driver, urls, file_path)
except Exception as e:
    print("Error:", e)
finally:
    driver.quit()
    print("Navegador cerrado.")
