import time
import duckdb


def main():
    t_total = time.perf_counter()
    con = duckdb.connect(database=":memory:")

    con.execute("""
        CREATE OR REPLACE VIEW clima AS
        SELECT *
        FROM read_parquet('https://data.meteostat.net/daily/2026.parquet')
    """)

    con.execute("""
        CREATE OR REPLACE VIEW clima_limpio AS
        SELECT
            station,
            date,
            temp,
            tmin,
            tmax,
            prcp
        FROM clima
        WHERE temp IS NOT NULL
          AND tmin IS NOT NULL
          AND tmax IS NOT NULL
          AND tmax >= tmin
    """)

    t0 = time.perf_counter()
    promedios_mensuales = con.sql("""
        SELECT
            DATE_TRUNC('month', date)::DATE AS mes,
            COUNT(*) AS registros,
            ROUND(AVG(temp), 2) AS temp_media,
            ROUND(AVG(tmin), 2) AS tmin_media,
            ROUND(AVG(tmax), 2) AS tmax_media
        FROM clima_limpio
        GROUP BY 1
        ORDER BY 1
    """)
    t_mensual = (time.perf_counter() - t0) * 1000
    print(f"\n--- Promedios mensuales ({t_mensual:.2f} ms) ---")
    promedios_mensuales.show()

    t0 = time.perf_counter()
    max_por_estacion = con.sql("""
        SELECT
            station,
            ROUND(MAX(tmax), 2) AS temp_max_registrada,
            ROUND(AVG(temp), 2) AS temp_media_anual,
            COUNT(*) AS dias_validos
        FROM clima_limpio
        GROUP BY station
        HAVING COUNT(*) >= 30
        ORDER BY temp_max_registrada DESC
        LIMIT 15
    """)
    t_max = (time.perf_counter() - t0) * 1000
    print(f"\n--- Top 15 estaciones por temperatura máxima ({t_max:.2f} ms) ---")
    max_por_estacion.show()

    total_s = time.perf_counter() - t_total
    print(f"\nTiempo total de ejecución: {total_s:.2f} s")


if __name__ == "__main__":
    main()
