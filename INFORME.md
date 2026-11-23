# Informe Trabajo Integrador - Pipeline ETL Valhalla S.A.

## 1. Arquitectura de la Solución

Se implementó un pipeline ETL modular utilizando DuckDB como motor analítico, Python (pandas) para limpieza y transformación de datos, y Apache Airflow para la orquestación diaria programada a las 02:00 AM (`0 2 * * *`).

- Extracción (`01-extract.sql`): Se cargó el archivo original de `pedidos.csv` sin alteraciones en la tabla `raw_pedidos` (2.575 registros).
- Validación (`02-validate.sql`): Se evaluó 8 reglas de calidad (`R1_ID_DUPLICADO`, `R2_PAIS_NULO`, `R3_CATEGORIA_NULA`, `R4_ESTADO_MAYUSCULAS_O_INVALIDO`, `R5_CANTIDAD_INVALIDA`, `R6_PRECIO_UNITARIO_INVALIDO`, `R7_TOTAL_NULO_O_INCONSISTENTE`, `R8_FECHA_FORMATO_INVALIDO`) y se dividieron los datos en `validos` y `rechazados` con sus respectivos `motivo_rechazo`.
- Limpieza y Carga (`pipeline.py` y `04-final.sql`): Se recuperaron los países por ciudad y categorías por producto, se normalizaron los estados y  las fechas (`YYYY-MM-DD`), se corrigieron las de cantidades/precios negativos, y se recalculó el total en `rechazados_limpios` y unificando todo sin duplicados ni errores de tipo en `tabla_final`.

## 2. Problemas Detectados y Reglas Aplicadas

Durante la exploración inicial con `marimo` (`explorar.py`) se detectaron registros duplicados por `id_pedido`, campos nulos en `pais` y `categoria`, estados en mayúsculas, fechas en formato `DD/MM/YYYY`, cantidades y precios negativos, y totales nulos o inconsistentes con el cálculo de descuento.

## 3. Resultados de Negocio (`consultas.sql`)

1. Las 3 categorías con mayor facturación total excluyendo los pedidos cancelados son electronica(919.826.000,00), hogar (145.312.967,61) y Indumentaria (135.919.650,00).

2. La facturación por mes desde ek 1 de enero de 2024 hasta el 1 de diciembre de 2025 excluyendo los pedidos cancelados, los valores de facturación son variados, el mínimo fue 31.756.382,10 el 01 de junio de 2024 y el máximo 72.756.987,94 en julio de 2024, es decir en esos intervalos fueron el mínimo y máximo en solo un mes. También su promedio de la facturación mensual fue de 51.689.680,09.

3. El ticket promedio por país segun el total promedio por pedido es asi: 
- Colombia: 701.647,01
- Chile: 698.695,93
- Argentina: 626.939,10
- Uruguay: 608.607,82
- Perú: 575.442,63
- Paraguay 482.436,19

4. El porcentaje de los pedidos que fueron cancelados es del 15,45.

5. El medio de pago que más fue utilizado fue transferencia y la cantidad de pedidos de 626.


Las consultas de estos datos estan en el archivo `consultas.sql` y fueron ejecutadas en `explorar.py` para ver sus resultados.