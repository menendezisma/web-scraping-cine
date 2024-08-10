from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import locale
import pandas as pd
import re
from datetime import datetime

def formatear_fecha(fecha, año):
    # Dividimos la fecha original en día y mes
    dia, mes_str = fecha.split('/')
    print(dia)
    print(mes_str)  
    # Creamos un objeto datetime con el día, mes y año proporcionados
    fecha_datetime = datetime.strptime(f"{dia}/{mes_str}/{año}", "%d/%B/%Y")
    mes_numero = fecha_datetime.month

    # Formateamos la fecha en el formato deseado (mes-día-año con mes en número)
    fecha_formateada = f"{mes_numero:02d}-{dia}-{año}"

    return fecha_formateada


def extraer_idioma(lista_pelicula):
    idiomas = []
    for elemento in lista_pelicula:
        for parte in elemento.split("\n"):
            if "Dob" in parte:
                idiomas.append("Doblaje")
                break
            elif "Sub" in parte:
                idiomas.append("Subtitulada")
                break
            elif "Inglés" in parte:
                idiomas.append("Inglés")
                break
    return idiomas

def extraer_horarios_completos(lista_pelicula):
  horarios = []
  for elemento in lista_pelicula:
    # Buscamos patrones de horarios más flexibles
    patron = r'\d{1,2}:\d{2}\s*[ap]m'  # Busca dígitos, dos puntos, dígitos y opcionalmente "am" o "pm"
    match = re.search(patron, elemento)
    if match:
      horarios.append(match.group())
  return horarios

def extraer_formato_pelicula(lista_pelicula):
    formato = []
    for elemento in lista_pelicula:
        for parte in elemento.split():
            if "2D" in parte:
                formato.append("2D")
                break
            elif "3D" in parte:
                formato.append("3D")
                break
                
    return formato


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
        #obtener la fecha
        fecha_cartelera=driver.find_elements(By.XPATH, '//a[@class="accordion-toggle"]')
        for info_nombre_cine in nombre_cine_completo:
            nombre_cine=info_nombre_cine.text
            #print(info_nombre_cine.text)
            
        for infos in info_cinema:
            info_cartelera=infos.text+ "\n" + nombre_cine[13:]
            data_info.append(info_cartelera)
            
        for info_fecha in fecha_cartelera:
            fecha_sin_formato=info_fecha.text
        
        # Pausa para ver el cambio de página (opcional)
        time.sleep(2)
        
        # Volver a la página principal
        driver.get("https://unicines.com/cartelera.php")

    #print(data_info)
    #print(len(data_info))
    #crear lista donde se almacenaran los elementos divididos por el salto de linea
    new_data_info=[]
    data_rows=[] #lista que servira para almacenar los datos estructurados
    for i in data_info:
        data_string=i.split("\n")
        #data_string=data_string.split("\n")
        if(data_string[0]=="ESTRENO"):
            data_string.pop(0)
        new_data_info.append(data_string)
    
    #llamamos a la función que da formato a la fecha, pasamos la fecha obtenida del sitio web, ya que este no tiene año
    #le pasamos el valor de 2024 para el año.
    fecha_formateada=formatear_fecha(fecha_sin_formato, 2024)
    
    for j in new_data_info:
        horarios_completos=extraer_horarios_completos(j)
        formatos = extraer_formato_pelicula(j)
        idiomas = extraer_idioma(j)
        #print(len(idiomas))
        #print(idiomas)
        for hora, formato, idioma in zip(horarios_completos, formatos, idiomas):
            data_rows.append({
                "Fecha": fecha_formateada,
                "Pais": "Honduras",
                "Cine":"Unicines",
                "Nombre cine":j[-1],
                "Titulo":j[0],
                "Hora":hora,
                "Idioma": idioma,
                "Formato": formato 
            })
    #print(fecha_sin_formato)
    print(data_rows)
    print(len(data_rows))
    #creamos el dataframe
    df=pd.DataFrame(data_rows)
    print(df)
    df.to_excel('unicines.xlsx', index=False)
    # Cerrar el navegador
    driver.quit()
    