Determinantes del Precio de la Vivienda en Puebla 🏠🐺
Este proyecto aplica un modelo de Regresión Lineal Múltiple (MCO) para analizar y predecir los factores económicos y estructurales que influyen en el valor inmobiliario del estado de Puebla, México.

1. Pregunta e Hipótesis
Problema: ¿Qué factores explican el precio de las viviendas en Puebla y cuál es la magnitud 
del impacto de variables como el tamaño, número de cuartos y ubicación?

Hipótesis: * Superficie total: Relación positiva (+). A mayor construcción, mayor precio.

Distancia al centro: Relación mixta (-/+). Entre más lejos del Zócalo, menor plusvalía.

Cuartos / Pisos: Relación positiva (+). Mayor utilidad marginal interna.

2. Variables del Modelo
Variable Dependiente (Y): Precio de la vivienda en MXN (precio_mxn).

Variables Independientes (X): - Superficie total en m2 (superficie_total).

Cantidad de habitaciones (cuartos).

Distancia lineal al centro en km (distancia_centro_km).

Número de niveles (pisos).

3. Cómo reproducir el proyecto
Para ejecutar este análisis localmente o en Google Colab:

Instalar dependencias:
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import statsmodels.api as sm
import numpy as np


Ejecutar el Notebook: Abre el archivo PROYECTO_ECONOMETRIA_FINAL.ipynb, carga la base de datos en el entorno de google colab y corre las celdas en orden.

Datos: El script procesa la base original de Properati filtrando 795 registros válidos para el estado de Puebla tras una limpieza de outliers (IQR).

4. Estructura del Repositorio
PROYECTO_ECONOMETRIA_FINAL.ipynb: Código fuente con la limpieza y el modelo.

Econometria_Final.pdf: Reporte ejecutivo con interpretaciones actuariales.

README.md: Documentación del proyecto.

5. Roles del Equipo (Lobo Métricos)
Huerta Barcenas Jessica: Validación estadística y pruebas de robustez.

Moreno Sotero Alexa Esmeralda: Redacción final, conclusiones y presentación.

Ramos Lopez Maritza Alondra: Especificación econométrica y estimación del modelo.

Serrano Hernandez Lenin: Análisis descriptivo y operatorio.

Gonzalez Galeana Sergio Alejandro: Gestión y depuración de la base de datos.

Peña Morales Carlos: Coordinador de Proyecto y Metodología.

6. Declaración del Uso de IA
Se emplearon herramientas de IA Generativa para la optimización de código y resolución de errores estructurales. Todas las decisiones metodológicas y la validación de resultados fueron supervisadas y ejecutadas por el equipo de investigación.

Proyecto desarrollado para la materia de Econometría I - BUAP (Primavera 2026).
