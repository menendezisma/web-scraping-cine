from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd
from datetime import datetime
import os

import re

def obtener_horarios(peliculas):
    #Se crea una lista vacía para almacenar los horarios encontrados
    horarios = []
    #se itera sobre cada elemento (película) en la lista.
    for peli in peliculas:
        # Buscamos patrones de horarios más flexibles
        patron = r'\d{1,2}:\d{1,2}'
        match = re.search(patron, peli)

        #Si se encuentra una coincidencia, se agrega el horario a la lista
        if match:
            horarios.append(match.group())

    print(horarios)
    return horarios
 

"""
def obtener_idioma(peli):
  peli_idiomas = []
  for i in range(0,len(peli)):
    if "Español" in peli[i] or "Subtitulada" in peli[i] or "Ingles" in peli[i]:
      ext_idioma=peli[i]
      peli_idiomas.append(ext_idioma)
      #print(peli[i])   
    
  return peli_idiomas
"""
def obtener_idioma(peli):
  peli_idiomas = []
  for i in range(0,len(peli)):
    if "Español" in peli[i]:
      ext_idioma="Doblada español"
      peli_idiomas.append(ext_idioma)
      #print(peli[i])
    elif "Ingles" in peli[i]:
        ext_idioma="Ingles"
        peli_idiomas.append(ext_idioma)
    
  return peli_idiomas

def obtener_formato(pelicula):
    formato = []
    for peli in pelicula:
        for parte in peli.split():
            if "2D" in parte:
                formato.append("2D")
                continue
            elif "3D" in parte:
                formato.append("3D")
                continue
    if len(formato)>2:
        formato.pop(0)
        formato.pop(0)
    elif len(formato)<=2:
        formato.pop(0)
    return formato

#funcion que sirve para obtener la fecha actual.
def obtener_fecha_sistema():
    fecha_hoy=datetime.now()
    fecha_hoy_formateada=fecha_hoy.strftime("%m-%d-%Y")
    return fecha_hoy_formateada

if __name__=='__main__':
    options = Options()
    options.add_argument('--start-maximized')
    driver_path = 'C:\\Users\\Usuario\\Desktop\\EdgeDriver\\msedgedriver.exe'
    service=Service(driver_path)
    driver = webdriver.Edge(service=service, options=options)
    driver.get('https://www.metrocinemas.hn/main.aspx#') 
    time.sleep(3)

    menu_trigger = driver.find_element(By.XPATH,"//a[@id='cd-menu-trigger']")
    menu_trigger.click()
    time.sleep(3)
    
    menu_cartelera = driver.find_element(By.LINK_TEXT, "CARTELERA")
    menu_cartelera.click()
    time.sleep(2)
    
    info_cartelera=[]
    
    nombre_cine=["America", "Metromall", "Miraflores", "MegaMall", "Novacentro", "Choloma", "Cortes", "Santa Rosa"]
    for pagina_cine in range(len(nombre_cine)):
        cine=driver.find_element(By.LINK_TEXT, nombre_cine[pagina_cine])
        cine.click()
        time.sleep(5)
        menu_trigger = driver.find_element(By.XPATH,"//a[@id='cd-menu-trigger']")
        menu_trigger.click()
        time.sleep(3)
        if pagina_cine<=len(nombre_cine):
            menu_cartelera = driver.find_element(By.LINK_TEXT, "CARTELERA")
            menu_cartelera.click()
            #Encuentra el elemento contenedor
            contenedor_peliculas = driver.find_element(By.CLASS_NAME, "contenedorpeliculascartelera")

            #Encuentra todos los elementos "combopelicartelera" dentro del contenedor
            combo_peliculas = contenedor_peliculas.find_elements(By.CLASS_NAME, "combopelicartelera")
            for pelicula in combo_peliculas:
                infor_pelicula=pelicula.text+ "\n" + nombre_cine[pagina_cine]
                info_cartelera.append(infor_pelicula.split("\n"))
            time.sleep(2)
        else:
            driver.quit()
    print()      
    peliculas_filas = []        
    pais="Honduras"
    cine="Metrocinemas"
    fecha=obtener_fecha_sistema()
    
    for peli_individual in info_cartelera:
        print(peli_individual[0])
        idiomas=obtener_idioma(peli_individual)
        horarios=obtener_horarios(peli_individual)
        formatos=obtener_formato(peli_individual) 
        
        if horarios == []:
            #print(type(horarios))
            cantidad=len(formatos)
            #print(cantidad)
            horarios.append("No horario")
        

        if "2D VIP DOB" in peli_individual[0] or "3D VIP DOB" in peli_individual[0]:
            nombre_pelicula=peli_individual[0][11:]
        elif "2D DOB" in peli_individual[0] or "2D VIP" in peli_individual[0] or "3D DOB" in peli_individual[0]:
            nombre_pelicula=peli_individual[0][7:]
        elif "2D SVIP DOB" in peli_individual[0]:
            nombre_pelicula=peli_individual[0][12:]
        elif "2D" in peli_individual[0]:
            nombre_pelicula=peli_individual[0][3:]
        else:
            nombre_pelicula=peli_individual[0][:]
            
        for horario, formato in zip(horarios, formatos):
            peliculas_filas.append({
                "Fecha": fecha,
                "Pais":pais,
                "Cine":cine,
                "Nombre cine":peli_individual[-1],
                "Titulo":nombre_pelicula,
                "Hora":horario,
                "Idioma":idiomas[0],
                "Formato":formato
            })
    
    print(peliculas_filas)
    df=pd.DataFrame(peliculas_filas)
    print(df)
    #Crear la ruta completa al archivo de Excel
    ruta_carpeta = "results"
    hora=datetime.now()
    nombre_archivo="metrocinemas "+fecha+" "+str(hora.strftime("%H-%M-%S"))+".xlsx"
    ruta_archivo = os.path.join(ruta_carpeta, nombre_archivo)
  
    #Crear la carpeta si no existe
    os.makedirs(ruta_carpeta, exist_ok=True)
    df.to_excel(ruta_archivo, index=False)
    
    print("Información de peliculas guardada en carpeta results en el archivo de excel "+nombre_archivo)
    # Cerrar el navegador
    driver.quit() 
    #print(len(info_cartelera))    
    #print(info_cartelera)

    