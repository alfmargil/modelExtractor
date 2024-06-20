import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import random
import re

def extraer_datos_por_marca(url_inicial, clase_objetivo):
    """
    Extrae datos de una URL inicial, seleccionando diferentes opciones de marca y guarda los datos en un archivo .txt.
    El nombre del archivo es el contenido del h1 de la web scrapeada.

    Args:
      url_inicial (str): La URL de la página web inicial.
      clase_objetivo (str): La clase CSS que se quiere buscar después de la selección de marca.
    """
    try:
        # Configuración del servicio de Chromedriver
        service = Service('./chromedriver')  # Ruta al Chromedriver local
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')  # Opcional, si es necesario deshabilitar el sandbox

        # Inicializar el driver usando el servicio configurado
        driver = webdriver.Chrome(service=service, options=chrome_options)

        driver.get(url_inicial)

        # Espera explícita para cargar la página completamente (ajusta el tiempo según sea necesario)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "h1")))

        # Extraer el contenido del h1
        h1_element = driver.find_element(By.TAG_NAME, "h1")
        h1_text = h1_element.text.strip()

        # Limpiar el texto del h1 para que sea un nombre de archivo válido
        nombre_archivo = re.sub(r'[^A-Za-z0-9 ]+', '', h1_text) + '.txt'

        # Seleccionar el desplegable de marcas
        select_element = Select(driver.find_element(By.CLASS_NAME, "product-fits__brand"))
        
        # Obtener todas las opciones del desplegable
        options = select_element.options

        # Iterar sobre cada opción del desplegable
        for option in options:
            # Obtener el valor y texto de la opción
            option_value = option.get_attribute("value")
            option_text = option.text

            # Seleccionar la opción en el desplegable
            select_element.select_by_value(option_value)

            campo_busqueda = driver.find_element(By.CSS_SELECTOR, ".product-fits__search")
            ActionChains(driver).move_to_element(campo_busqueda).click().perform()

            # Seleccionar la opción en el desplegable
            #select_element.select_by_value(option_value)

            # Esperar un tiempo suficiente para que se cargue el contenido dinámico
            time.sleep(random.uniform(4, 6))  # Ajusta según sea necesario

            # Extraer HTML después de la selección
            contenido_html = driver.page_source

            # Analizar el código HTML con BeautifulSoup
            sopa = BeautifulSoup(contenido_html, 'html.parser')

            # Encuentra todos los elementos con la clase objetivo
            elementos = sopa.find_all('div', class_=clase_objetivo)

            # Lista para almacenar todos los valores de data-checkid con la marca
            data_checkids_con_marca = []

            for elemento in elementos:
                if elemento.has_attr('data-checkid'):
                    data_checkid_valor = elemento['data-checkid']
                    # Agregar el nombre de la marca antes del valor de data-checkid
                    data_checkids_con_marca.append(f"{option_text.strip()} {data_checkid_valor}")

            # Abre el archivo .txt en modo escritura
            with open(nombre_archivo, 'a', encoding='utf-8') as archivo:  # 'a' para añadir al archivo
                # Escribe cada valor de data-checkid con la marca en el archivo
                for valor in data_checkids_con_marca:
                    archivo.write(valor + '\n')

        # Cierra el navegador al finalizar
        driver.quit()
        messagebox.showinfo("Completado", f"Extracción de datos finalizada. Datos guardados en {nombre_archivo}")

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

def generar_datos():
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Error", "Por favor ingresa una URL válida.")
        return

    url_inicial = url
    clase_objetivo = 'product-fits__item'

    extraer_datos_por_marca(url_inicial, clase_objetivo)

# Crear ventana Tkinter
root = tk.Tk()
root.title("Extracción de Datos")

# Crear etiqueta y campo de entrada para la URL
url_label = tk.Label(root, text="URL:")
url_label.pack(pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.pack()

# Crear botón para generar datos
generar_button = tk.Button(root, text="Generar", command=generar_datos)
generar_button.pack(pady=20)

# Ejecutar el bucle principal de la ventana Tkinter
root.mainloop()
