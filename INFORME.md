# Informe Trabajo Integrador - Pipeline ETL Valhalla S.A.

## 1. Arquitectura de la Solución

Se implementó un pipeline ETL modular utilizando **DuckDB** como motor analítico, **Python (pandas)** para limpieza y transformación de datos, y **Apache Airflow** para la orquestación diaria programada a las 02:00 AM (`0 2 * * *`).

- **Extracción (`01-extract.sql`):** Carga el origen `pedidos.csv` sin alteraciones en la tabla `raw_pedidos` (2.575 registros).
- **Validación (`02-validate.sql`):** Evalúa 8 reglas de calidad (`R1_ID_DUPLICADO`, `R2_PAIS_NULO`, `R3_CATEGORIA_NULA`, `R4_ESTADO_MAYUSCULAS_O_INVALIDO`, `R5_CANTIDAD_INVALIDA`, `R6_PRECIO_UNITARIO_INVALIDO`, `R7_TOTAL_NULO_O_INCONSISTENTE`, `R8_FECHA_FORMATO_INVALIDO`) y divide los datos en `validos` y `rechazados` con su respectivo `motivo_rechazo`.
- **Limpieza y Carga (`pipeline.py` y `04-final.sql`):** Recupera países por ciudad y categorías por producto, normaliza estados y fechas (`YYYY-MM-DD`), corrige cantidades/precios negativos, recalcula el total en `rechazados_limpios` y unifica todo sin duplicados ni errores de tipo en `tabla_final`.

## 2. Problemas Detectados y Reglas Aplicadas

Durante la exploración inicial con `marimo` (`explorar.py`) se detectaron registros duplicados por `id_pedido`, campos nulos en `pais` y `categoria`, estados en mayúsculas, fechas en formato `DD/MM/YYYY`, cantidades y precios negativos, y totales nulos o inconsistentes con el cálculo de descuento.

## 3. Resultados de Negocio (`consultas.sql`)

- **Medio de pago más usado:** Transferencia (626 pedidos).
- Las consultas SQL completas para el Top 3 de categorías, facturación mensual, ticket promedio por país, porcentaje de cancelados y medio de pago se encuentran en `dags/sql/consultas.sql`.
