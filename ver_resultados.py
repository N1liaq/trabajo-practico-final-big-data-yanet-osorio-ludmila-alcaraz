import duckdb

con = duckdb.connect("dags/valhalla.duckdb")

print("=== REGLAS ===")
print(con.sql("SELECT motivo_rechazo, COUNT(*) cant FROM rechazados GROUP BY 1 ORDER BY 2 DESC").df())

consultas = open("dags/sql/consultas.sql", encoding="utf-8").read().split(";")
for i, q in enumerate(consultas, 1):
    if q.strip():
        print(f"\n=== CONSULTA {i} ===")
        print(con.sql(q).df())