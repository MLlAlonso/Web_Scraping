import csv
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

# Cargar las variables de entorno
env_path = os.path.join(os.getcwd(), ".env")
load_dotenv(env_path)

# Leer credenciales
username = os.getenv("campus_user")
password = os.getenv("campus_pwd")

# Configurar WebDriver
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

documents_path = os.path.join(os.path.expanduser("~"), "Documents", "Estudiantes Cursos")
if not os.path.exists(documents_path):
    os.makedirs(documents_path)

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
    try:
        titulo_elemento = driver.find_element(By.XPATH, "//div[@class='titles']/h2")
        return titulo_elemento.text.strip().replace(" ", "_").replace(",", "")
    except:
        return "Curso_Desconocido"

try:
    driver.get("https://campus.elhubdeseguridad.com/wp-login.php")
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "user_login")))
    driver.find_element(By.ID, "user_login").send_keys(username)
    driver.find_element(By.ID, "user_pass").send_keys(password)
    driver.find_element(By.ID, "wp-submit").click()
    WebDriverWait(driver, 18).until(EC.url_contains("wp-admin"))

    for url in urls:
        driver.execute_script(f"window.open('{url}', '_blank');")
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[-1])
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "name")))
        
        nombre_curso = obtener_nombre_curso()
        file_path = os.path.join(documents_path, f"Estudiantes_{nombre_curso}.csv")
        
        filas = driver.find_elements(By.XPATH, "//table//tr")
        curso_datos = []
        
        for fila in filas:
            try:
                nombre = fila.find_element(By.CLASS_NAME, "author__info").text.strip()
            except:
                nombre = "No encontrado"
            
            if nombre in ["No encontrado", "Usuario eliminado"]:
                continue
            
            try:
                email = fila.find_element(By.CLASS_NAME, "email").text.strip()
            except:
                email = "No encontrado"
            
            try:
                tiempo = fila.find_element(By.CLASS_NAME, "time").text.replace("hace", "").strip()
            except:
                tiempo = "No encontrado"
            
            try:
                progress_bar = fila.find_element(By.XPATH, ".//div[contains(@class, 'progress-bar')]")
                progreso = progress_bar.get_attribute("style").split("width:")[1].strip().replace(";", "") if "width:" in progress_bar.get_attribute("style") else "No encontrado"
                progreso = progreso.replace("%", "")  # Quitar el %
            except:
                progreso = "No encontrado"
            
            curso_datos.append([nombre, email, tiempo, progreso])
        
        with open(file_path, mode="w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow(["Nombre", "Email", "Inicio", "Progreso (porcentaje)"])
            writer.writerows(curso_datos)
        
        print(f"Datos de {url} guardados en {file_path} ✅")
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

except Exception as e:
    print("Error:", e)

finally:
    driver.quit()
    print("Navegador cerrado.")
