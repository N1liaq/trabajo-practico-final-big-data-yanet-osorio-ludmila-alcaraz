from pathlib import Path
import duckdb
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "valhalla.duckdb"
CSV_PATH = BASE_DIR / "data" / "pedidos.csv"
SQL_DIR = BASE_DIR / "sql"

def read_sql(filename: str) -> str:
    return (SQL_DIR / filename).read_text(encoding="utf-8")

def extract():
    with duckdb.connect(str(DB_PATH)) as con:
        con.execute(read_sql("01-extract.sql"), [str(CSV_PATH)])
        filas = con.sql("SELECT COUNT(*) FROM raw_pedidos").fetchone()[0]
        print("OK -> raw_pedidos cargada con filas:", filas)

def validate():
    with duckdb.connect(str(DB_PATH)) as con:
        con.execute(read_sql("02-validate.sql"))
        val = con.sql("SELECT COUNT(*) FROM validos").fetchone()[0]
        rech = con.sql("SELECT COUNT(*) FROM rechazados").fetchone()[0]
        print(f"OK -> validos: {val} | rechazados: {rech}")

def clean_and_load():
    with duckdb.connect(str(DB_PATH)) as con:
        df_val = con.execute("SELECT * FROM validos").df()
        df_rech = con.execute("SELECT * EXCLUDE (motivo_rechazo) FROM rechazados").df()

        # Diccionarios desde válidos para recuperar pais (por ciudad) y categoria (por producto)
        mapa_pais = df_val.dropna(subset=["ciudad", "pais"]).drop_duplicates("ciudad").set_index("ciudad")["pais"].to_dict()
        mapa_cat = df_val.dropna(subset=["producto", "categoria"]).drop_duplicates("producto").set_index("producto")["categoria"].to_dict()

        # 1. Deduplicar id_pedido
        df_rech = df_rech.dropna(subset=["id_pedido"]).drop_duplicates(subset=["id_pedido"], keep="first")

        # 2. Recuperar pais y categoria nulos
        df_rech["pais"] = df_rech["pais"].fillna(df_rech["ciudad"].map(mapa_pais))
        df_rech["categoria"] = df_rech["categoria"].fillna(df_rech["producto"].map(mapa_cat))

        # 3. Normalizar estado a minúsculas
        df_rech["estado"] = df_rech["estado"].astype(str).str.strip().str.lower()

        # 4. Estandarizar fechas DD/MM/YYYY a YYYY-MM-DD
        df_rech["fecha_pedido"] = pd.to_datetime(df_rech["fecha_pedido"], format="mixed", dayfirst=True, errors="coerce")
        df_rech = df_rech.dropna(subset=["fecha_pedido"])
        df_rech["fecha_pedido"] = df_rech["fecha_pedido"].dt.strftime("%Y-%m-%d")

        # 5. Corregir cantidades y precios negativos, y recalcular total
        df_rech["cantidad"] = pd.to_numeric(df_rech["cantidad"], errors="coerce").abs()
        df_rech["precio_unitario"] = pd.to_numeric(df_rech["precio_unitario"], errors="coerce").abs()
        df_rech["descuento_pct"] = pd.to_numeric(df_rech["descuento_pct"], errors="coerce").fillna(0).clip(0, 100)
        df_rech = df_rech[(df_rech["cantidad"] > 0) & (df_rech["precio_unitario"] > 0)]
        df_rech["total"] = (df_rech["cantidad"] * df_rech["precio_unitario"] * (1 - df_rech["descuento_pct"] / 100.0)).round(2)

        # Guardar rechazados_limpios y construir tabla_final
        con.register("df_rech_view", df_rech)
        con.execute("CREATE OR REPLACE TABLE rechazados_limpios AS SELECT * FROM df_rech_view")
        con.execute(read_sql("04-final.sql"))

        limpios = con.sql("SELECT COUNT(*) FROM rechazados_limpios").fetchone()[0]
        final = con.sql("SELECT COUNT(*) FROM tabla_final").fetchone()[0]
        print(f"OK -> rechazados_limpios: {limpios} | tabla_final: {final}")

if __name__ == "__main__":
    extract()
    validate()
    clean_and_load()