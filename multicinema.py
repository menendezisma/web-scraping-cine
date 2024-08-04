from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import locale
import pandas as pd
from datetime import datetime

def conversion_fecha(fecha):
    locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')
    date_text=fecha.text[22:]
    date_text=date_text.split()
    if(date_text[0]=="Miercoles"):
        date_text[0]="Miércoles"
    elif date_text[0]=="Sabado":
        date_text[0]="Sábado"
    date_text=" ".join(date_text)
    fecha_datetime=datetime.strptime(date_text, "%A %d %B %Y")
    fecha_formato=fecha_datetime.strftime("%m-%d-%Y")
    return fecha_formato

def parse_cinema_data(data, date, country):
    # Inicializar variables para almacenar datos
    complejo = ""
    titulo = ""
    clasificacion = ""
    promocion = ""
    duracion = ""
    idioma = ""
    formato = ""
    horarios = []

    # Lista para almacenar filas de datos
    data_rows = []

    # Procesar los datos
    for line in data.split("\n"):
        if line.startswith("Complejo:"):
            if horarios:
                for hora in horarios:
                    data_rows.append({
                        "Fecha": date,
                        "Pais": country,
                        "Cine": "Multicinema",
                        "Nombre_cine": complejo.replace(" ", "_"),
                        "Titulo": titulo.replace(" ", "_"),
                        "Hora": hora,
                        "Idioma": idioma,
                        "Formato": formato
                    })
            complejo = line.split("Complejo:")[1].strip()
            horarios = []
        elif line.startswith("Título:"):
            titulo = line.split("Título:")[1].strip()
        elif line.startswith("Clasificación:"):
            clasificacion = line.split("Clasificación:")[1].strip()
        elif line.startswith("Promoción:"):
            promocion = line.split("Promoción:")[1].strip()
        elif line.startswith("Duración:"):
            duracion = line.split("Duración:")[1].strip()
        elif line.startswith("Español"):
            if horarios:
                for hora in horarios:
                    data_rows.append({
                        "Fecha": date,
                        "Pais": country,
                        "Cine": "Multicinema",
                        "Nombre_cine": complejo.replace(" ", "_"),
                        "Titulo": titulo.replace(" ", "_"),
                        "Hora": hora,
                        "Idioma": idioma,
                        "Formato": formato
                    })
            idioma_formato = line.strip().split()
            idioma = idioma_formato[0]
            formato = "".join(idioma_formato[1:]) if len(idioma_formato) > 1 else ""
            horarios = []
        elif line.strip():
            horarios.extend(line.strip().split())

    # Añadir la última tanda de horarios
    if horarios:
        for hora in horarios:
            data_rows.append({
                "Fecha": date,
                "Pais": country,
                "Cine": "Multicinema",
                "Nombre_cine": complejo.replace(" ", "_"),
                "Titulo": titulo.replace(" ", "_"),
                "Hora": hora,
                "Idioma": idioma,
                "Formato": formato
            })

    return data_rows

def combine_time_parts(data_rows):
    combined_data = []
    skip_next = False

    for i in range(len(data_rows)):
        if skip_next:
            skip_next = False
            continue

        current_row = data_rows[i]
        if i + 1 < len(data_rows) and data_rows[i+1]["Hora"] in ["AM", "PM"]:
            current_row["Hora"] += " " + data_rows[i+1]["Hora"]
            skip_next = True

        combined_data.append(current_row)
    
    return combined_data


#Crear instancia de Options
options = Options()
#Abrir la ventana del navegador en tamaño grande.
options.add_argument('--start-maximized')
#options.add_argument()

driver_path = 'C:\\Users\\Usuario\\Desktop\\EdgeDriver\\msedgedriver.exe'
service=Service(driver_path)
driver = webdriver.Edge(service=service, options=options)
driver.get('https://multicinema.com.sv/') 
time.sleep(2)
cartelera_button = driver.find_element(By.LINK_TEXT, "Cartelera")
cartelera_button.click()

#en la nueva página, en el selector elegimos "sabado 27 Julio 2024"
# Encontrar el elemento select con el nombre "Dias"
#select_element = driver.find_element(By.NAME, "Dias")

# Crear un objeto Select para interactuar con el elemento
#select_object = Select(select_element)

# Seleccionar la opción por su texto visible
#select_object.select_by_visible_text("Sabado 27  Julio  2024 ")

#selector1 = driver.find_element(By.XPATH, '//*[@id="frmCartelera"]/div/center/select[1]/option[2]')
#selector1.click()
#selector2 = driver.find_element(By.XPATH, '//*[@id="frmCartelera"]/div/center/select[2]/option[2]')
#selector2.click()
#tambien seleccionamos Multicinema Plaza mundo soyapango
#select_element2 = driver.find_element(By.NAME, "Complejo")
#select_object2 = Select(select_element2)
#select_object2.select_by_visible_text("Multicinema Plaza Mundo Soyapango")

#Dar click al boton de consulta
# Encontrar el botón "Consulta"
#consulta_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Consulta']")
# Hacer clic en el botón
#consulta_button.click()
time.sleep(2)
#name_cinema=driver.find_element(By.XPATH, '//h3[@class="panel-title"]')
#print(name_cinema.text[9:])
# Cierra el navegador
date_cinema=driver.find_element(By.XPATH, '/html/body/div[1]/div/div/h3/center')

#variables para almacenar información
data=[]
pais="El Salvador"
#print(fecha_formato)
data_info=[]
info_cinema=driver.find_elements(By.XPATH, '//div[@class="tab-content"]')
for infos in info_cinema:
    data_info.append(infos.text)
    #data_info.append(infos.text)
    #print(infos.text)
data_info = "\n".join(data_info)
#print(data_info)    
#pasar los datos
fecha_formato=conversion_fecha(date_cinema)
data_rows = parse_cinema_data(data_info, fecha_formato, pais)
data_rows = combine_time_parts(data_rows)
df=pd.DataFrame(data_rows)
#df=df.to_string(index=False)
print(df)
df.to_excel('Multicinema2.xlsx', index=False)
driver.quit()





            