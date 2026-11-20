CREATE OR REPLACE TABLE pedidos_evaluados AS
WITH conteo_ids AS (
    SELECT id_pedido, COUNT(*) AS cant_id FROM raw_pedidos GROUP BY id_pedido
)
SELECT 
    r.*,
    TRIM(BOTH ' | ' FROM CONCAT_WS(' | ',
        CASE WHEN c.cant_id > 1 THEN 'R1_ID_DUPLICADO' END,
        CASE WHEN r.pais IS NULL OR TRIM(r.pais) = '' THEN 'R2_PAIS_NULO' END,
        CASE WHEN r.categoria IS NULL OR TRIM(r.categoria) = '' THEN 'R3_CATEGORIA_NULA' END,
        CASE WHEN r.estado <> LOWER(TRIM(r.estado)) OR LOWER(TRIM(r.estado)) NOT IN ('entregado', 'enviado', 'pendiente', 'cancelado') THEN 'R4_ESTADO_MAYUSCULAS_O_INVALIDO' END,
        CASE WHEN TRY_CAST(r.cantidad AS INTEGER) IS NULL OR TRY_CAST(r.cantidad AS INTEGER) <= 0 THEN 'R5_CANTIDAD_INVALIDA' END,
        CASE WHEN TRY_CAST(r.precio_unitario AS DOUBLE) IS NULL OR TRY_CAST(r.precio_unitario AS DOUBLE) <= 0 THEN 'R6_PRECIO_UNITARIO_INVALIDO' END,
        CASE WHEN TRY_CAST(r.total AS DOUBLE) IS NULL OR ABS(TRY_CAST(r.total AS DOUBLE) - (TRY_CAST(r.cantidad AS DOUBLE) * TRY_CAST(r.precio_unitario AS DOUBLE) * (1 - TRY_CAST(r.descuento_pct AS DOUBLE)/100.0))) > 0.05 THEN 'R7_TOTAL_NULO_O_INCONSISTENTE' END,
        CASE WHEN TRY_STRPTIME(r.fecha_pedido, '%Y-%m-%d') IS NULL THEN 'R8_FECHA_FORMATO_INVALIDO' END
    )) AS motivo_rechazo
FROM raw_pedidos r
LEFT JOIN conteo_ids c ON r.id_pedido = c.id_pedido;

CREATE OR REPLACE TABLE validos AS
SELECT * EXCLUDE (motivo_rechazo) FROM pedidos_evaluados WHERE motivo_rechazo = '';

CREATE OR REPLACE TABLE rechazados AS
SELECT * FROM pedidos_evaluados WHERE motivo_rechazo <> '';