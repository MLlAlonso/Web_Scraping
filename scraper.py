import csv
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
USERNAME = os.getenv("campus_user")
PASSWORD = os.getenv("campus_pwd")

# Configuración de WebDriver
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

DOCUMENTS_PATH = os.path.join(os.path.expanduser("~"), "Documents", "Estudiantes_Cursos")
os.makedirs(DOCUMENTS_PATH, exist_ok=True)

URLS = [
    "https://campus.elhubdeseguridad.com/wp-admin/?page=stm-lms-dashboard#/course/13342",
    "https://campus.elhubdeseguridad.com/wp-admin/?page=stm-lms-dashboard#/course/12914",
    "https://campus.elhubdeseguridad.com/wp-admin/?page=stm-lms-dashboard#/course/12822",
    "https://campus.elhubdeseguridad.com/wp-admin/?page=stm-lms-dashboard#/course/12302",
    "https://campus.elhubdeseguridad.com/wp-admin/?page=stm-lms-dashboard#/course/11712",
    "https://campus.elhubdeseguridad.com/wp-admin/?page=stm-lms-dashboard#/course/11187",
    "https://campus.elhubdeseguridad.com/wp-admin/?page=stm-lms-dashboard#/course/11089",
    "https://campus.elhubdeseguridad.com/wp-admin/?page=stm-lms-dashboard#/course/10481",
    "https://campus.elhubdeseguridad.com/wp-admin/?page=stm-lms-dashboard#/course/9692",
    "https://campus.elhubdeseguridad.com/wp-admin/?page=stm-lms-dashboard#/course/10388",
    "https://campus.elhubdeseguridad.com/wp-admin/?page=stm-lms-dashboard#/course/8841"
]

def iniciar_sesion():
    driver.get("https://campus.elhubdeseguridad.com/wp-login.php")
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "user_login")))
    driver.find_element(By.ID, "user_login").send_keys(USERNAME)
    driver.find_element(By.ID, "user_pass").send_keys(PASSWORD)
    driver.find_element(By.ID, "wp-submit").click()
    WebDriverWait(driver, 18).until(EC.url_contains("wp-admin"))

def obtener_nombre_curso():
    try:
        nombre_curso = driver.find_element(By.XPATH, "//div[@class='titles']/h2").text.strip()
        return nombre_curso.replace("Estudiantes de ", "").replace(" ", "_").replace(",", "")
    except:
        return "Curso_Desconocido"

def extraer_datos_curso():
    datos = []
    filas = driver.find_elements(By.XPATH, "//table//tr")
    for fila in filas:
        nombre = fila.find_element(By.CLASS_NAME, "author__info").text.strip() if fila.find_elements(By.CLASS_NAME, "author__info") else "No encontrado"
        if nombre in ["No encontrado", "Usuario eliminado"]:
            continue
        email = fila.find_element(By.CLASS_NAME, "email").text.strip() if fila.find_elements(By.CLASS_NAME, "email") else "No encontrado"
        tiempo = fila.find_element(By.CLASS_NAME, "time").text.replace("hace", "").strip() if fila.find_elements(By.CLASS_NAME, "time") else "No encontrado"
        progreso = "No encontrado"
        if fila.find_elements(By.XPATH, ".//div[contains(@class, 'progress-bar')]"):
            progress_bar = fila.find_element(By.XPATH, ".//div[contains(@class, 'progress-bar')]")
            progreso = progress_bar.get_attribute("style").split("width:")[1].strip().replace(";", "") if "width:" in progress_bar.get_attribute("style") else "No encontrado"
        datos.append([nombre, email, tiempo, progreso])
    return datos

def guardar_csv(file_path, headers, datos):
    with open(file_path, mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(datos)
    print(f"Datos guardados en {file_path} ✅")

def procesar_cursos(opcion):
    datos_totales = []
    for url in URLS:
        driver.execute_script(f"window.open('{url}', '_blank');")
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[-1])
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "name")))
        nombre_curso = obtener_nombre_curso()
        datos_curso = extraer_datos_curso()
        
        if opcion == "1":
            for fila in datos_curso:
                fila.append(nombre_curso)
            datos_totales.extend(datos_curso)
        else:
            guardar_csv(
                os.path.join(DOCUMENTS_PATH, f"Estudiantes_{nombre_curso}.csv"),
                ["Nombre", "Email", "Inicio", "Progreso"],
                datos_curso
            )
        
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    
    if opcion == "1":
        guardar_csv(
            os.path.join(DOCUMENTS_PATH, "Estudiantes_Cursos.csv"),
            ["Nombre", "Email", "Inicio", "Progreso", "Curso"],
            datos_totales
        )

try:
    iniciar_sesion()
    opcion = input("Seleccione el modo de guardado (1: Un solo CSV, 2: Un CSV por curso): ")
    while opcion not in ["1", "2"]:
        opcion = input("Opción inválida. Seleccione 1 o 2: ")
    procesar_cursos(opcion)
except Exception as e:
    print("Error:", e)
finally:
    driver.quit()
    print("Navegador cerrado.")