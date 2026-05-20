# Conclusiones del Modelo Econométrico e Implicaciones Estadísticas

Este documento sintetiza los resultados, transformaciones metodológicas y diagnósticos finales aplicados a la base de datos inmobiliaria de Puebla[cite: 1, 3].

## 📊 Metodología e Ingeniería de Variables

### 1. Limpieza y Depuración de Datos
[cite_start]Durante el Análisis Exploratorio de Datos (EDA) se detectaron anomalías severas producto de errores de captura en el portal de origen (por ejemplo, propiedades con `m2 = 0` o un departamento con un área irreal de `9,134 m²`). Se aplicó un filtro estricto reduciendo la base final a **178 observaciones limpias**.

[cite_start]Los valores faltantes (`NaN`) en variables de amenidades como estacionamientos y antigüedad se trataron bajo el supuesto de que su omisión en la plataforma significa la inexistencia del atributo, imputándoseles el valor de `0`.

### 2. Estrategia Híbrida de Localización Espacial
Para capturar la geografía y plusvalía de Puebla de forma robusta, se implementó un enfoque doble:
**Componente Continuo:** Cálculo de la distancia euclidiana/haversine desde cada propiedad hacia el **Zócalo de Puebla**, modelada de forma cuadrática (`dist_zocalo_km2`) bajo la premisa económica de que los primeros kilómetros de distancia impactan de forma más agresiva en el valor de la tierra.
**Componente Categórico (Variables Dummy):** Clasificación de las observaciones según la zona de plusvalía más cercana (Angelópolis, La Paz, Las Ánimas, San Andrés), omitiendo intencionalmente la zona de **San Manuel** como la *categoría base* de comparación para evitar la trampa de la colinealidad perfecta.

---

## 📈 Especificación de Modelos Estadísticos
Se contrastaron múltiples formas funcionales para evaluar el comportamiento del mercado:

1.**Modelo 1 (Lineal-Lineal):** Evaluó los precios directamente en niveles de pesos, asumiendo efectos marginales constantes corrientes[cite: 33, 41]. [cite_start]Presentó problemas de colinealidad y rigidez teórica].
2. **Modelo 2 (Log-Log / Semilog):** Transformó la variable dependiente a su logaritmo natural (`ln_precio`), adaptándose a la teoría económica inmobiliaria que demuestra que la relación entre el precio y el espacio físico no es lineal. 

---

## 🔍 Principales Hallazgos y Conclusiones Económicas

* **Anelasticidad del Espacio Metrado:** De acuerdo con la estimación del modelo Log-Log, el coeficiente asociado a los metros cuadrados (`ln_m2`) se sitúa en un valor cercano a `0.5131`.Esto indica que, manteniendo todo lo demás constante, **un incremento del 1% en la superficie total de la propiedad genera un aumento aproximado de solo el 0.51% en su precio final**[cite: 44, 45]. Existe un efecto decreciente en el valor marginal del espacio.
* **Robustez ante Heterocedasticidad:** Debido a la naturaleza de corte transversal de la base de datos (donde la varianza del error tiende a incrementarse conforme aumentan los precios de las propiedades de lujo), todas las inferencias y desviaciones estándar se estimaron utilizando **errores estándar robustos (tipo HC3)**, garantizando que las pruebas de significancia no estén sesgadas.
* **El Efecto de la Plusvalía Geográfica:** Los modelos demuestran una alta sensibilidad respecto a las variables dummy de zona[cite: 1, 3]. [cite_start]Las propiedades ubicadas en zonas como Angelópolis y San Andrés Cholula exhiben primas de precio marcadamente positivas y estadísticamente significativas al contrastarse contra la zona base de San Manuel, validando las hipótesis de segregación y concentración del valor comercial en los polos de desarrollo recientes de la ciudad.
