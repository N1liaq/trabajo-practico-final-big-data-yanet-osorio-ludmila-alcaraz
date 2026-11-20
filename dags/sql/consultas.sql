-- 1. Top 3 categorías con mayor facturación total (excluyendo cancelados)
SELECT categoria, ROUND(SUM(total), 2) AS facturacion_total
FROM tabla_final
WHERE estado <> 'cancelado'
GROUP BY categoria
ORDER BY facturacion_total DESC
LIMIT 3;

-- 2. Facturación por mes (excluyendo cancelados)
SELECT DATE_TRUNC('month', fecha_pedido) AS mes, ROUND(SUM(total), 2) AS facturacion_mensual
FROM tabla_final
WHERE estado <> 'cancelado'
GROUP BY mes
ORDER BY mes;

-- 3. Ticket promedio por país (excluyendo cancelados)
SELECT pais, ROUND(AVG(total), 2) AS ticket_promedio
FROM tabla_final
WHERE estado <> 'cancelado'
GROUP BY pais
ORDER BY ticket_promedio DESC;

-- 4. Porcentaje de pedidos cancelados
SELECT ROUND(100.0 * SUM(CASE WHEN estado = 'cancelado' THEN 1 ELSE 0 END) / COUNT(*), 2) AS porcentaje_cancelados
FROM tabla_final;

-- 5. Medio de pago más usado y cantidad de pedidos
SELECT medio_pago, COUNT(*) AS cantidad_pedidos
FROM tabla_final
GROUP BY medio_pago
ORDER BY cantidad_pedidos DESC
LIMIT 1;