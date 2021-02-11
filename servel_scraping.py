#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 08:02:13 2021

@author: anonimo
"""

import pandas as pd
import numpy as np
import time

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
url = 'https://pv.servelelecciones.cl/'
driver.get(url)

### Definir tiempo de esepra
espera = WebDriverWait(driver, 10)

### Seleccionar "Participación" y "Chile"
participacion = espera.until(EC.presence_of_element_located((By.XPATH, '//*[@id="menu"]/ul/li[3]/a')))
participacion.click()

seleccionar_chile = espera.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[2]/div/ul/li[3]/a')))
seleccionar_chile.click()

    
### Objeto que identifica la lista de regiones
selecionador_regiones = espera.until(EC.presence_of_element_located((By.XPATH, '//*[@id="selRegion"]')))
dropdown = Select(selecionador_regiones)


### Lista de regiones
regiones = [dropdown.options[i].text for i in range(1,len(dropdown.options))]


### Seleccionar Region
dropdown.select_by_visible_text(regiones[0])


### Encontrar la tabla y cabecera de tabla
headers = driver.find_elements_by_xpath('//*[@id="basic-table"]/table/thead/tr/th')
cabeceras = [headers[i].text for i in range(0, len(headers))]
  

### Pasar los datos a una lista
datos = []

for i in range(0, len(regiones)):
    dropdown.select_by_visible_text(regiones[i])
    time.sleep(1)
    td = driver.find_elements_by_tag_name('td')
    datos += [td[i].text for i in range(0,len(td))]

driver.quit()

datos = np.array(datos)    
df = pd.DataFrame(np.reshape(datos, (int(datos.shape[0]/5),5)), columns=cabeceras)
df.drop(df[df['Comuna'] == ""].index, inplace=True)
df.reset_index(drop=True, inplace=True)

### Guardar DataFrame en disco

path = '/home/anonimo/Documentos/servel/'
file_name = 'servel'
df.to_csv(path+file_name+'.csv', index=False)
