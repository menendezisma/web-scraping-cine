from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time
import locale
import pandas as pd
from datetime import datetime
import os

#funcion que servira para convertir la fecha al formato de mes-dia-año.
def conversion_de_fecha(date_movies):
  locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')
  date_text=date_movies.text[22:]
  date_text=date_text.split()
  if(date_text[0]=="Miercoles"):
    date_text[0]="Miércoles"
  elif date_text[0]=="Sabado":
    date_text[0]="Sábado"
  date_text=" ".join(date_text)
  fecha_datetime=datetime.strptime(date_text, "%A %d %B %Y")
  fecha_formato=fecha_datetime.strftime("%m-%d-%Y")
  return fecha_formato

def obtener_hora(peli):
  peli_hosrario=[]

  #print(elem)
  for i in range(0,len(peli)):
    if "AM" in peli[i] or "PM" in peli[i]:
      peli_hosrario.append([peli[i]])
      #print(peli[i])

  #print(peli_hosrario)
  hora_peliculas=[]
 
  for separa_hora in range(0, len(peli_hosrario)):
    horarios = peli_hosrario[separa_hora][0]
    horarios = horarios.split()
    hora_separadas=[]
    #print(horarios)
    for sep in range(0, len(horarios), 2):
      hora = horarios[sep]+" "+horarios[sep+1]
      hora_separadas.append(hora)
    hora_peliculas.append(hora_separadas)

  #print(hora_peliculas)
  return hora_peliculas
  
def obtener_idioma(peli):
  peli_idiomas = []
  for i in range(0,len(peli)):
    if "Español" in peli[i] or "Subtitulada" in peli[i] or "Ingles" in peli[i]:
      ext_idioma=peli[i].split()
      idioma_original=ext_idioma[0]
      peli_idiomas.append([idioma_original])
      #print(peli[i])
    
  return peli_idiomas
  
def obtener_formato(peli):
  peli_formatos = []
  for i in range(0,len(peli)):
    if "2D" in peli[i] or "3D" in peli[i]:
      ext_formato=peli[i].split()
      formato_pelicula=ext_formato[1]
      peli_formatos.append([formato_pelicula])
      #print(peli[i])
      
  return peli_formatos

#codigo main que servira para extraer los datos
if __name__=='__main__':
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
  #Dar clic al botón "Cartelera" del navbar
  cartelera_button.click()
  time.sleep(2)

  #obtener la fecha de la cartelera
  fecha_cartelera=driver.find_element(By.XPATH, '/html/body/div[1]/div/div/h3/center')
  fecha=conversion_de_fecha(fecha_cartelera)
  print(fecha)
  #variables para almacenar información
  cine="Multicinema"
  pais="El Salvador"
  #Array en el que se guardara la información a extraer.
  peli=[]
  #seleccionar el div que contiene toda la información de la cartelera
  info_cinema=driver.find_elements(By.XPATH, '//div[@class="tab-content"]')
  for infos in info_cinema:
    pelicula_en_cartelera=infos.text
    peli.append(pelicula_en_cartelera.split("\n"))
    #data_info.append(infos.text)
    #print(infos.text)
    
    #print(cartelera_cine_inicial)
  #peli = ['Complejo: Multicinema Plaza Mundo Soyapango', 'Título: Deadpool & Wolverine', 'Clasificación: Mayores de 15 años', 'Promoción: No', 'Duración: 2h 07m', '', 'Español 2D', '10:30 AM 12:00 PM 01:00 PM 02:30 PM 03:30 PM 05:00 PM 06:00 PM 07:30 PM','Subtitulada 3D','02:30 PM']
  #peli = [['Complejo: Multicinema Plaza Mundo Soyapango', 'Título: Deadpool & Wolverine', 'Clasificación: Mayores de 15 años', 'Promoción: No', 'Duración: 2h 07m', '', 'Español 2D', '10:30 AM 12:00 PM 01:00 PM 02:30 PM 03:30 PM 05:00 PM 06:00 PM 07:30 PM'], ['Complejo: Multicinema Plaza Mundo Soyapango', 'Título: Mi Villano Favorito 4', 'Clasificación: Todo Público', 'Promoción: Si', 'Duración: 1h 35m', '', 'Español 2D', '10:15 AM 11:45 AM 01:45 PM 05:15 PM'], ['Complejo: Multicinema Plaza Mundo Soyapango', 'Título: Intensamente 2', 'Clasificación: Todo Público', 'Promoción: Si', 'Duración: 1h 36m', '', 'Español 2D', '12:00 PM 01:30 PM 03:30 PM 07:15 PM'], ['Complejo: Multicinema Plaza Mundo Soyapango', 'Título: Plan de Retiro', 'Clasificación: Mayores de 15 años', 'Promoción: Si', 'Duración: 1h 43m', '', 'Español 2D', '03:30 PM 07:15 PM'], ['Complejo: Multicinema Plaza Mundo Soyapango', 'Título: La Trampa', 'Clasificación: Mayores de 15 años', 'Promoción: Si', 'Duración: 1h 46m', '', 'Español 2D', '12:15 PM 03:45 PM'], ['Complejo: Multicinema Plaza Mundo Soyapango', 'Título: Romper el Círculo', 'Clasificación: Mayores de 15 años', 'Promoción: Si', 'Duración: 2h 11m', '', 'Español 2D', '12:00 PM 02:30 PM 05:00 PM 07:30 PM'], ['Complejo: Multicinema Plaza Mundo Soyapango', 'Título: Borderlands', 'Clasificación: Mayores de 12 años', 'Promoción: No', 'Duración: 1h 41m', '', 'Español 2D', '10:00 AM 05:30 PM 07:30 PM'], ['Complejo: Multicinema Plaza Mundo Soyapango', 'Título: Beetlejuice', 'Clasificación: Mayores 12 años, menores acompañados de un ad', 'Promoción: Si', 'Duración: 1h 32m', '', 'Subtitulada 2D', '10:00 AM'], ['Complejo: Multicinema Plaza Mundo Soyapango', 'Título: Harold y su Crayón Mágico', 'Clasificación: Todo Público', 'Promoción: Si', 'Duración: 1h 30m', '', 'Español 2D', '10:30 AM'], ['Complejo: Multicinema Plaza Mundo Soyapango', 'Título: De Noche con el Diablo', 'Clasificación: Mayores de 15 años', 'Promoción: No', 'Duración: 1h:33m', '', 'Español 2D', '02:00 PM 05:30 PM'], ['Complejo: Multicinema Plaza Mundo Apopa', 'Título: Plan de Retiro', 'Clasificación: Mayores de 15 años', 'Promoción: Si', 'Duración: 1h 43m', '', 'Español 2D', '11:00 AM 05:30 PM'], ['Complejo: Multicinema Plaza Mundo Apopa', 'Título: Romper el Círculo', 'Clasificación: Mayores de 15 años', 'Promoción: Si', 'Duración: 2h 11m', '', 'Español 2D', '11:00 AM 01:00 PM 03:15 PM 07:30 PM'], ['Complejo: Multicinema Plaza Mundo Apopa', 'Título: Beetlejuice', 'Clasificación: Mayores 12 años, menores acompañados de un ad', 'Promoción: Si', 'Duración: 1h 32m', '', 'Subtitulada 2D', '03:30 PM'], ['Complejo: Multicinema Plaza Mundo Apopa', 'Título: Mi Villano Favorito 4', 'Clasificación: Todo Público', 'Promoción: Si', 'Duración: 1h 35m', '', 'Español 2D', '11:30 AM 01:30 PM 03:30 PM 05:30 PM 07:30 PM'], ['Complejo: Multicinema Plaza Mundo Apopa', 'Título: Intensamente 2', 'Clasificación: Todo Público', 'Promoción: Si', 'Duración: 1h 36m', '', 'Español 2D', '11:00 AM 01:00 PM 03:00 PM 05:00 PM 07:00 PM'], ['Complejo: Multicinema Plaza Mundo Apopa', 'Título: La Trampa', 'Clasificación: Mayores de 15 años', 'Promoción: Si', 'Duración: 1h 46m', '', 'Español 2D', '11:00 AM 04:15 PM 07:45 PM'], ['Complejo: Multicinema Plaza Mundo Apopa', 'Título: De Noche con el Diablo', 'Clasificación: Mayores de 15 años', 'Promoción: No', 'Duración: 1h:33m', '', 'Español 2D', '02:30 PM 06:00 PM'], ['Complejo: Multicinema Plaza Mundo Apopa', 'Título: Deadpool & Wolverine', 'Clasificación: Mayores de 15 años', 'Promoción: No', 'Duración: 2h 07m', '', 'Español 2D', '11:00 AM 12:00 PM 01:30 PM 02:30 PM 04:00 PM 05:00 PM 06:30 PM 07:30 PM'], ['Complejo: Multicinema Plaza Mundo Apopa', 'Título: Borderlands', 'Clasificación: Mayores de 12 años', 'Promoción: No', 'Duración: 1h 41m', '', 'Español 2D', '01:30 PM 05:45 PM 07:30 PM'], ['Complejo: Multicinema Plaza Mundo Apopa', 'Título: Harold y su Crayón Mágico', 'Clasificación: Todo Público', 'Promoción: Si', 'Duración: 1h 30m', '', 'Español 2D', '12:45 PM']]
  #print(len(peli))

  peliculas_filas = []
  for info_pelis in peli:  
    horas=obtener_hora(info_pelis)
    idiomas=obtener_idioma(info_pelis)
    formatos=obtener_formato(info_pelis)


    for i in range(len(horas)):
      for hora in horas[i]:
        for idioma in idiomas[i]:
          for formato in formatos[i]:
            diccionario = {'Fecha':fecha , 'Pais':pais,'Cine':cine,'Nombre cine':info_pelis[0][10:],'Titulo':info_pelis[1][8:],'Hora': hora, 'Idioma': idioma, 'Formato': formato}
            peliculas_filas.append(diccionario)

  #print(peliculas_filas)
  peliculas_cartelera_completa=pd.DataFrame(peliculas_filas)
  print(peliculas_cartelera_completa)
  #Crear la ruta completa al archivo de Excel
  ruta_carpeta = "results"
  hora=datetime.now()
  nombre_archivo="multicinema "+fecha+" "+str(hora.strftime("%H-%M-%S"))+".xlsx"
  ruta_archivo = os.path.join(ruta_carpeta, nombre_archivo)
  
  #Crear la carpeta si no existe
  os.makedirs(ruta_carpeta, exist_ok=True)
  
  peliculas_cartelera_completa.to_excel(ruta_archivo, index=False)
  print("Información de peliculas guardada en carpeta results en el archivo de excel "+nombre_archivo)
  # Cerrar el navegador
  driver.quit()

