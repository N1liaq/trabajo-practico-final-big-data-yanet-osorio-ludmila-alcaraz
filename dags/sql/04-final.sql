CREATE OR REPLACE TABLE tabla_final AS
WITH union_tablas AS (
    SELECT * FROM validos
    UNION ALL
    SELECT * FROM rechazados_limpios
),
deduplicados AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY id_pedido ORDER BY fecha_pedido) AS rn
    FROM union_tablas
)
SELECT
    TRIM(id_pedido) AS id_pedido,
    CAST(fecha_pedido AS DATE) AS fecha_pedido,
    TRIM(id_cliente) AS id_cliente,
    LOWER(TRIM(email_cliente)) AS email_cliente,
    TRIM(pais) AS pais,
    TRIM(ciudad) AS ciudad,
    TRIM(categoria) AS categoria,
    TRIM(producto) AS producto,
    CAST(cantidad AS INTEGER) AS cantidad,
    CAST(precio_unitario AS DOUBLE) AS precio_unitario,
    CAST(descuento_pct AS DOUBLE) AS descuento_pct,
    ROUND(CAST(total AS DOUBLE), 2) AS total,
    LOWER(TRIM(estado)) AS estado,
    LOWER(TRIM(medio_pago)) AS medio_pago
FROM deduplicados
WHERE rn = 1;