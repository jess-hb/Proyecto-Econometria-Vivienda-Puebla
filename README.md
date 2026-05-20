# Determinantes del Precio de Vivienda en la Zona Metropolitana de Puebla
**Modelo Hedónico de Precios con Datos de Corte Transversal** *Curso: Econometría I — Proyecto Final* *Equipo: Lobometricos*

---

## 📌 Descripción del Proyecto
Este repositorio contiene el desarrollo, los datos y el informe econométrico de la **Fase 2** del proyecto inmobiliario. El objetivo central es identificar y cuantificar el efecto marginal de las características estructurales, amenidades y localización espacial sobre el precio de venta de las viviendas en la Zona Metropolitana de Puebla (ZMP), fundamentado en el **enfoque hedónico de precios (Rosen, 1974)**.

A través de la comparación de seis especificaciones funcionales estimadas mediante Mínimos Cuadrados Ordinarios (MCO), se determinaron las variables clave que guían el valor de mercado y se aplicó un diagnóstico robusto para corregir fallas en los supuestos clásicos de regresión.

---

## 👥 Estructura del Equipo y Roles

El proyecto fue desarrollado de forma colaborativa por el equipo **Lobometricos**, distribuyendo las responsabilidades de la siguiente manera:

* **Huerta Bárcenas, Jessica** *Rol:* Líder de Modelación Econométrica y Diagnóstico. Responsable del diseño de especificaciones alternativas, validación de supuestos clásicos (RESET, Cook, VIF).
* **Moreno Sotero, Alexa Esmeralda** *Rol:*  Analista Económico y Revisión de Literatura. Responsable de la fundamentación teórica del modelo hedónico y de la interpretación económica y elasticidades de los coeficientes obtenidos.
* **Ramos López, Maritza Alondra** *Rol:* Especialista en Variables de Localización y Georreferenciación. Desarrolló el cálculo de distancias continuas mediante la fórmula de Haversine y la asignación de centroides por zonas de plusvalía.
* **Serrano Hernández, Lenin** *Rol:* Ingeniera de Datos y Web Scrapping. Encargada de la extracción automatizada inicial desde *Inmuebles24*, limpieza de la base de datos y tratamiento de valores faltantes/nulos.
* **González Galeana, Sergio Alejandro** *Rol:* Diseñador de Visualización y Documentación Técnica. Encargado de la generación de gráficos distributivos, diagramas de diagnóstico y la integración final del reporte técnico.


## 📊 Metodología y Datos

### Fuente y Tratamiento de los Datos
* **Fuente:** Extracción mediante Web Scraping del portal inmobiliario *Inmuebles24*.
* **Muestra:** $n = 178$ observaciones de corte transversal tras depuración.
* **Tratamiento de Datos:** * *Valores faltantes:* Imputación justificada con $0$ en variables como `estacionamientos` (6.1%) y `antiguedad_anos` (50.6%), asumiendo que la omisión en el portal web representa la ausencia de la característica (propiedades nuevas o sin estacionamiento).
    * *Outliers:* Identificación y eliminación de errores de captura evidentes para evitar sesgos en los estimadores.

### Diccionario de Variables Principales
* `precio_mxn`: Precio de venta en pesos mexicanos (Variable dependiente).
* `m2`: Superficie construida en metros cuadrados.
* `banos_tot`: Baños completos + 0.5 $\times$ medios baños.
* `estacionamientos`: Número de cajones de estacionamiento disponibles.
* `antiguedad_anos`: Antigüedad de la propiedad en años.
* `dist_zocalo_km`: Distancia calculada en kilómetros hacia el Zócalo de Puebla.
* *Dummies de Control:* `roof_garden`, `alberca`, `es_casa` (1 si es casa, 0 si es departamento).
* *Dummies de Zona (Plusvalía):* `zona_angelopolis`, `zona_la_paz`, `zona_las_animas`, `zona_san_andres`.

---

## 📈 Especificaciones y Selección del Modelo

Se evaluaron 6 modelos alternativos desde lineales simples hasta formas logarítmicas complejas con interacciones. El **Modelo 3 (M3 - Log-Log con Interacciones)** fue seleccionado como el modelo óptimo utilizando criterios de información y pruebas de hipótesis:

* **Criterio de Selección:** Mejor balance ajuste-parsimonia ($R^2\text{-adj} = 0.8711$, mínimos AIC y BIC).
* **Test F (M2 vs M3):** $F = 34.54$ ($p = 0.0000$), demostrando que las interacciones añaden valor explicativo significativo.
* **Test F (M3 vs M4):** $F = 1.65$ ($p = 0.1804$), prefiriendo M3 sobre M4 por el principio de parsimonia.

---

## 🛠️ Diagnóstico Econométrico

Para garantizar inferencias confiables, el modelo fue sometido a una rigurosa batería de pruebas diagnósticas:

1.  **Multicolinealidad:** Evaluada mediante el Factor de Inflación de la Varianza (VIF), asegurando la estabilidad individual de los parámetros.
2.  **Heteroscedasticidad:** Confirmada a través de las pruebas de *Breusch-Pagan* (36.57, $p = 0.0015$) y *White*. **Solución:** Se aplicó una **corrección de errores robustos HC3 (MacKinnon y White, 1985)** en todas las estimaciones para corregir la matriz de varianzas-covarianzas sin sesgar los coeficientes.
3.  **Especificación (RESET de Ramsey):** El Modelo 3 arrojó un estadístico $F = 3.69$ ($p = 0.0271$), validando la correcta forma funcional log-log adoptada.
4.  **Análisis de Influencia (Distancia de Cook):** Se detectaron 15 observaciones influyentes utilizando el umbral crítico de $4/n = 0.0225$. La evaluación de robustez demostró alta estabilidad en variables críticas como `ln_m2` y `estacionamientos`.

---

## 🏆 Conclusiones Clave del Modelo M3

Los resultados del modelo econométrico final revelan insights económicos de alto valor sobre el comportamiento inmobiliario en Puebla:

* **Elasticidad Tamaño-Precio:** La variable `ln_m2` presenta un coeficiente de **0.8932** altamente significativo. Esto implica que un incremento del 1% en la superficie construida aumenta el precio de la vivienda en **0.89%**, consolidándose como el principal determinante físico.
* **Primas de Localización Espacial:** El mercado inmobiliario poblano penaliza fuertemente la distancia al centro urbano y premia los micro-mercados exclusivos. Con respecto a la zona base, las zonas conurbadas muestran primas porcentuales de valor muy marcadas:
    * **San Andrés:** $+70.9\%$
    * **Angelópolis:** $+39.9\%$
    * **La Paz:** $+2
