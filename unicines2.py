from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import locale
import pandas as pd
from datetime import datetime


def extraer_datos():
    pass

if __name__ == '__main__':
    #Crear instancia de Options
    options = Options()
    #Abrir la ventana del navegador en tamaño grande.
    options.add_argument('--start-maximized')
    #options.add_argument()

    driver_path = 'C:\\Users\\Usuario\\Desktop\\EdgeDriver\\msedgedriver.exe'
    service=Service(driver_path)
    driver = webdriver.Edge(service=service, options=options)
    driver.get('https://unicines.com/cartelera.php') 
    time.sleep(2)
    # Localizamos la lista de enlaces
    #cat_nav = driver.find_element(By.ID, "cat_nav")
    #links = cat_nav.find_elements(By.TAG_NAME, "a")
    # Iteramos sobre cada enlace
    # Bucle principal para iterar sobre los enlaces
    # Localizar todos los enlaces dentro de la lista <ul id="cat_nav">
    enlaces = driver.find_elements(By.CSS_SELECTOR, "#cat_nav li a")
    # Recorrer cada enlace
    # Recorrer cada enlace por su índice
    #arreglo para almecenar data inicial
    data_info=[]
    #lista para almacenar datos con nombre de cine
    data_info_cine=[]
    for i in range(len(enlaces)):
        # Volver a encontrar los elementos <a> después de cada iteración para evitar StaleElementReferenceException
        enlaces = driver.find_elements(By.CSS_SELECTOR, "#cat_nav li a")
        
        # Obtener el href del enlace actual
        url = enlaces[i].get_attribute("href")
        
        # Navegar al enlace
        driver.get(url)
        
        # Realizar cualquier acción que necesites en la página destino
        # (ejemplo: extraer información, interactuar con elementos, etc.)
        #obtener el nombre del cine
        nombre_cine_completo=driver.find_elements(By.XPATH, '//h1[@class="nomargin_top"]')
        #obtener la información para cada pelicula
        info_cinema=driver.find_elements(By.XPATH, '//div[@class="strip_all_tour_list wow fadeIn"]')
        
        for info_nombre_cine in nombre_cine_completo:
            nombre_cine=info_nombre_cine.text
            #print(info_nombre_cine.text)
            
        for infos in info_cinema:
            info_cartelera=infos.text+ "\n" + nombre_cine[13:]
            data_info.append(info_cartelera)
            #print(infos.text)
            
        #print(data_info_cine)
        # Pausa para ver el cambio de página (opcional)
        time.sleep(2)
        
        # Volver a la página principal
        driver.get("https://unicines.com/cartelera.php")

    print(data_info)
    print(len(data_info))
    # Cerrar el navegador
    driver.quit()