from pathlib import Path
import duckdb

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

if __name__ == "__main__":
    extract()