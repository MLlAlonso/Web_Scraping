# Web Scraping con Python y Selenium

Este proyecto implementa **web scraping** utilizando **Python y Selenium** para automatizar la extracción de datos de páginas web. El script se encarga de:

- Iniciar sesión en una plataforma web.
- Navegar por diferentes URLs.
- Extraer información específica de cada página.
- Guardar los datos en archivos CSV.

## Características
- Inicio de sesión automático con credenciales almacenadas en un archivo `.env`.
- Extracción de datos de múltiples pestañas desde una lista de URLs.
- Manejo de excepciones para evitar fallos si un dato no está disponible.
- Guardado de la información en archivos CSV dentro de una carpeta predefinida.
- Cambio automático entre pestañas para navegar.

## Tecnologías utilizadas

- **Python**
- **Selenium** (Automatización del navegador)
- **Chrome WebDriver**
- **dotenv** (Manejo de credenciales de forma segura)
- **CSV** (Almacenamiento de los datos extraídos)

## Instalación y configuración

### 1. Clona o descarga el repositorio** en tu máquina.
```bash
git clone https://github.com/tuusuario/web-scraping.git
cd web-scraping
```
### 2. Instalar dependencias

### 3. Configurar variables de entorno
Crear un archivo **.env** en la raíz del proyecto con las credenciales necesarias:
```ini
USERNAME=tu_usuario\PASSWORD=tu_contraseña
```

## Ejecución

Ejecuta el script con:
```bash
python scraper.py
```
El proceso abrirá el navegador, iniciará sesión y comenzará a extraer los datos, almacenándolos en archivos CSV.

## Personalización
El código puede adaptarse a cualquier otra página web ajustando los **selectores** de los elementos que se desean extraer.

## Consideraciones legales
Antes de realizar web scraping en cualquier sitio, revisa sus **Términos y Condiciones** para asegurarte de cumplir con las normas de uso.

## Licencia
Este proyecto está bajo la licencia MIT. Puedes usarlo y modificarlo libremente.