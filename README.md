# Análisis de Datos Meteorológicos con DuckDB y SQL

Proyecto de análisis exploratorio y estadístico sobre datos meteorológicos diarios utilizando **DuckDB** como motor analítico embebido en memoria, consultando directamente archivos en formato **Parquet** sin bases de datos tradicionales ni archivos binarios de base de datos

## Dataset utilizado

* **Fuente:** Meteostat Bulk Data (`https://data.meteostat.net/daily/2026.parquet`), con registros diarios meteorológicos en formato Parquet de acceso público y directo.
* **Volumen inicial:** 4.683.243 filas (con columnas como `station`, `date`, `temp`, `tmin`, `tmax`, `rhum` y `prcp`, entre otras).

## Estructura del proyecto

```text
proyecto-duckdb-clima/
├── data/
│   └── clima.parquet     # Dataset descargado localmente
├── .gitignore            # Exclusión de archivos de datos, temporales y binarios de BD
├── requirements.txt      # Dependencias del proyecto
├── analyze_clima.py      # Script de limpieza y consultas analíticas con DuckDB
└── README.md             # Documentación, tiempos y hallazgos del análisis
```

## Cómo replicar el análisis

1. Clonar el repositorio e ingresar a la carpeta del proyecto:
```
git clone https://github.com/cancelagisela/duckdb-clima-analisis.git
cd duckdb-clima-analisis
```
2. Crear y activar un entorno virtual (opcional, recomendado):
```
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux / macOS:
source venv/bin/activate
```
3. Instalar las dependencias desde requirements.txt
```
pip install -r requirements.txt
```
4. Descargar el archivo Parquet de Meteostat en data/clima.parquet (o ejecutar desde Google Colab clonando el repo y descargando el archivo en la sesión)

5. Ejecutar el script de análisis:
```
python analyze_clima.py
```
## Limpieza de datos y consultas analíticas
*Tratamiento de nulos y coherencia térmica*

En la exploración inicial sobre las 4.683.243 filas se detectaron 34.199 valores nulos en temp, 14.699 en tmin y 14.729 en tmax. Para evitar sesgos en promedios y comparaciones entre extremos diarios, se creó la vista virtual clima_limpio descartando registros donde temp, tmin o tmax son nulos y exigiendo tmax >= tmin.

*Consultas realizadas con DuckDB*

- Promedios mensuales: Agrupación por mes (DATE_TRUNC('month', date)::DATE) calculando cantidad de registros y promedios de temp, tmin y tmax.
- Estaciones con mayor temperatura máxima registrada: Agrupación por station (GROUP BY station) calculando MAX(tmax), AVG(temp) y COUNT(*) para identificar los valores máximos y su contexto promedio.

## Tiempos de ejecución y hallazgos principales
*Tiempos de ejecución (Google Colab con DuckDB en memoria)*
- Exploración inicial (esquema, primeras filas y conteo de nulos sobre 4.683.243 filas): 11 s en la celda.
- Celda de limpieza y análisis: 14 s en total.
- Consulta de promedios mensuales: 929.43 ms.
- Consulta de Top 15 estaciones por temperatura máxima: 1426.29 ms.

## Hallazgos principales
- Estacionalidad mensual (enero a noviembre de 2026): Los promedios mensuales muestran su valor más bajo en enero de 2026 (temp_media de 4.02 y tmin_media de 0.03) y ascienden progresivamente hasta alcanzar su pico promedio en julio de 2026 (temp_media de 21.11 y tmax_media de 26.27), seguido por agosto de 2026 (temp_media de 20.88).
- Temperaturas máximas por estación: Las máximas más altas del listado alcanzan 65.0 en estaciones como 61497, KJQF0 y 65125.
- Contraste entre máxima registrada y media anual: Algunas estaciones con temperaturas máximas elevadas presentan medias anuales mucho más moderadas o bajas (por ejemplo, KJQF0 con máxima de 65.0 y media anual de 18.36, o 12001 con máxima de 63.7 y media anual de 9.75), lo que marca un punto de atención para revisar posibles valores atípicos o extremos puntuales antes de entrenar modelos de Machine Learning. 
