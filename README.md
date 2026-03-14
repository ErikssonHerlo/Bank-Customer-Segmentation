# Bank Customer Segmentation

## Descripción general

Este proyecto desarrolla un análisis de datos avanzado sobre una base de clientes bancarios con el objetivo de identificar patrones de comportamiento previos a una campaña de marketing telefónico orientada a la suscripción de depósitos a plazo.

El trabajo integra análisis exploratorio de datos, preparación y transformación de variables, reducción de dimensionalidad y segmentación no supervisada mediante técnicas de clustering. A partir de los resultados obtenidos, se construyen perfiles de clientes con distinto nivel de valor comercial, lo que permite traducir hallazgos analíticos en recomendaciones estratégicas para campañas futuras.

El dataset de referencia corresponde al caso de estudio presentado por Moro, Cortez y Rita (2014), ampliamente utilizado en contextos académicos y analíticos para estudiar el éxito de campañas de telemarketing bancario.

---

## Objetivo del proyecto

El objetivo principal es segmentar clientes bancarios en grupos homogéneos a partir de sus características demográficas, financieras, comerciales y económicas, con el fin de comprender mejor su comportamiento y su relación con la variable objetivo `y`, que indica si el cliente suscribió o no un depósito a plazo.

De forma específica, el proyecto busca:

- desarrollar un análisis exploratorio de datos estructurado,
- evaluar la calidad y consistencia del dataset,
- aplicar procesos de ingeniería de datos para preparar la información,
- construir segmentos mediante K-Means,
- contrastar la estructura obtenida con un segundo método de clustering,
- e interpretar los resultados desde una perspectiva de negocio.

---

## Alcance del análisis

El proyecto se organiza en cuatro grandes bloques analíticos:

### 1. Análisis Exploratorio de Datos (EDA)
Se estudia la estructura del dataset mediante análisis univariado, bivariado y multivariado. En esta fase se revisan distribuciones, frecuencias, posibles outliers, correlaciones entre variables numéricas, relaciones entre variables categóricas y la variable objetivo, así como patrones de redundancia estructural.

### 2. Preparación e ingeniería de datos
Se realiza la selección y transformación de variables necesarias para clustering. Esto incluye exclusión justificada de variables con sesgo metodológico, codificación de variables categóricas y escalamiento de variables numéricas.

### 3. Segmentación de clientes
Se implementa **K-Means** como método principal de segmentación y **Clustering Jerárquico con enlace Ward** como método comparativo y de validación estructural.

### 4. Interpretación estratégica
Los clusters obtenidos se perfilan y analizan en términos de tamaño, tasa de conversión, características dominantes y potencial de uso en decisiones comerciales.

---

## Pregunta de negocio

¿Qué tipos de clientes pueden identificarse antes de una campaña telefónica y cuáles de esos grupos presentan mayor probabilidad de conversión hacia la suscripción de depósitos a plazo?

---

## Enfoque metodológico

El proyecto sigue una lógica analítica reproducible y orientada a negocio. Las principales decisiones metodológicas fueron las siguientes:

- **Uso de K-Means como método principal**, debido a su escalabilidad, simplicidad e interpretabilidad.
- **Uso de Clustering Jerárquico con Ward** como técnica complementaria para validar la estructura de grupos.
- **Exclusión de la variable `duration`** del proceso de clustering, ya que esta variable solo se conoce una vez realizada la llamada y su inclusión generaría un sesgo de información futura.
- **Codificación de variables categóricas con One-Hot Encoding**, para representar categorías nominales sin imponer un orden artificial.
- **Escalamiento con StandardScaler**, con el fin de evitar que las diferencias de magnitud entre variables afecten de manera desproporcionada las distancias utilizadas por los algoritmos.

---

## Estructura del proyecto

```text
Bank-Customer-Segmentation/
├── data/
│   └── raw/
│       └── bank-additional-full.csv
├── notebooks/
│   └── 01_bank_customer_segmentation.ipynb
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── data_utils.py
│   ├── eda_utils.py
│   └── clustering_utils.py
├── requirements.txt
└── README.md
````

### Descripción de carpetas y archivos

* **data/raw/**: contiene el dataset original utilizado en el análisis.
* **notebooks/**: contiene el notebook principal del proyecto, donde se presenta el flujo analítico completo con narrativa, tablas y visualizaciones.
* **src/config.py**: centraliza parámetros y constantes del proyecto.
* **src/data_utils.py**: funciones de carga, profiling y preparación básica de datos.
* **src/eda_utils.py**: funciones auxiliares para análisis exploratorio y diagnóstico estadístico.
* **src/clustering_utils.py**: funciones de transformación, evaluación e implementación de clustering.
* **src/run_analysis.py**: script auxiliar para ejecución estructurada del flujo, aunque el entregable principal es el notebook.
* **requirements.txt**: dependencias necesarias para reproducir el entorno.

---

## Entregables del proyecto

Este repositorio contiene dos entregables principales:

### Notebook técnico

Documento analítico completo en formato Jupyter Notebook, con el desarrollo del EDA, preparación de datos, modelado de clustering, análisis comparativo e interpretación de resultados.

### Informe ejecutivo

Documento orientado a síntesis y comunicación de hallazgos, enfocado en:

* hallazgos del EDA,
* justificación técnica del modelo,
* perfil de segmentos,
* recomendaciones estratégicas,
* métricas utilizadas.

---

## Resultados esperados

A partir de la ejecución del proyecto, se espera obtener:

* una caracterización clara de la base de clientes,
* evidencia de patrones relevantes en variables demográficas, comerciales y económicas,
* una segmentación interpretable de clientes,
* comparación entre dos técnicas de clustering,
* y recomendaciones accionables para orientar campañas futuras de marketing.

---

## Tecnologías y librerías utilizadas

* Python
* pandas
* numpy
* matplotlib
* seaborn
* scikit-learn
* scipy
* Jupyter Notebook

---

## Reproducción del proyecto

### 1. Clonar el repositorio

```bash
git clone git@github.com:ErikssonHerlo/Bank-Customer-Segmentation.git
cd bank_customer_segmentation_project
```

### 2. Crear y activar un entorno virtual

```bash
python -m venv .venv
```

En Windows:

```bash
venv\\Scripts\\activate
```

En Linux/macOS:

```bash
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Colocar el dataset

Asegúrate de que el archivo `bank-additional-full.csv` se encuentre en la ruta:

```text
data/raw/bank-additional-full.csv
```

### 5. Ejecutar el notebook

Abrir el archivo:

```text
notebooks/01_bank_customer_segmentation.ipynb
```

y ejecutar sus celdas en orden.

---

## Consideraciones importantes

* El análisis está diseñado para ser **reproducible** y **modular**.
* Aunque existe lógica reutilizable en `src/`, el **entregable principal** es el notebook.
* La variable `duration` fue excluida del clustering por razones metodológicas, pero puede conservarse dentro del análisis descriptivo para enriquecer la interpretación.
* El segundo método de clustering se utiliza como herramienta de contraste analítico, no necesariamente como reemplazo del método principal.

---

## Valor del proyecto

Este proyecto no se limita a describir datos, sino que busca convertir información histórica de clientes en conocimiento útil para negocio. La segmentación obtenida puede utilizarse como base para mejorar la eficiencia de campañas comerciales, priorizar perfiles con mayor potencial de conversión y reducir el costo asociado a contactos de baja probabilidad de respuesta.

En ese sentido, el valor del trabajo radica en conectar técnicas de análisis de datos con decisiones estratégicas concretas.

---

## Referencias

* Moro, S., Cortez, P., & Rita, P. (2014). *A data-driven approach to predict the success of bank telemarketing*. Decision Support Systems.
* Tan, P. N., Steinbach, M., & Kumar, V. (2019). *Introduction to Data Mining* (2nd ed.). Pearson.
* James, G., Witten, D., Hastie, T., & Tibshirani, R. (2021). *An Introduction to Statistical Learning* (2nd ed.). Springer.


