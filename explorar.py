import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import pandas as pd

    return (pd,)


@app.cell
def _(pd):
    df = pd.read_csv("dags/data/pedidos.csv", dtype=str)
    return (df,)


app._unparsable_cell(
    r"""
    df[df.duplicated(subset=['id_pedido'], keep=False)]S
    """,
    name="_"
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Los datos duplicados se mueran en las 148 filas que muestra la consulta, las cuales corresponden a 73 identificadores en id_pedidos repetidos, al hacer la restra entre ambas (148 - 73 = 75) nos da 75, lo cual seria la cantidad exacta de las de los registros rebundantes. index0 es el número de la fila original que tenía cada registro en el archivo CSV.
    """)
    return


@app.cell
def _(df):
    df.isna().sum()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    En esta consulta se ven las celdas las cuales estan vacías (nulos) de las columnas que hay en la DB . Países tiene 126, categoria 101 y total 129.
    """)
    return


@app.cell
def _(df):
    df["estado"].value_counts()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    En la columna estado, estan repetido varias veces entregado, cancelado, enviado y pendiente pero en mayusculas.
    """)
    return


@app.cell
def _(df):
    df["medio_pago"].value_counts()
    return


@app.cell
def _(df):
    df["medio_pago"].isna().sum()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    En la columna medio_pago esta todo en orden, no tiene duplicadas ni nulos.
    """)
    return


@app.cell
def _(df):
    df["pais"].value_counts()
    return


@app.cell
def _(df):
    df["pais"].isna().sum()
    return


@app.cell
def _(df):
    df["categoria"].value_counts()
    return


@app.cell
def _(df):
    df["categoria"].isna().sum()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    las columnas categoria y pais no tienen filas repetidas pero tienen filas nulas las cuales se necesita arreglar, categoria 101 y pais 126.
    """)
    return


@app.cell
def _(df, pd):
    cant = pd.to_numeric(df["cantidad"], errors="coerce")
    df[cant.isna() | (cant <= 0)]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    En la columna cantidad se muestra vacia o con valores menores a cero.
    """)
    return


@app.cell
def _(df, pd):
    precio = pd.to_numeric(df["precio_unitario"], errors="coerce")
    df[precio.isna() | (precio <= 0)]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    la tabla precio unitario se detectaron 130 registros con un precio unitario incorrecto.
    """)
    return


@app.cell
def _(df, pd):
    cant_t = pd.to_numeric(df["cantidad"], errors="coerce")
    precio_t = pd.to_numeric(df["precio_unitario"], errors="coerce")
    desc_t = pd.to_numeric(df["descuento_pct"], errors="coerce")
    tot_t = pd.to_numeric(df["total"], errors="coerce")

    calculado_t = cant_t * precio_t * (1 - desc_t / 100)

    df[tot_t.isna() | ((tot_t - calculado_t).abs() > 0.05)]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    En esta consulta se pueden ver el mal calculo y las partes nulas del total. El porqué esta mal calculado es porque las cantidades de esos productos son negativos, algo que no debería ser posible por lo que su total es incoherente como sus cantidades y los que presentan cantidades coherentes sus totales son nulos.
    """)
    return


@app.cell
def _(df, pd):
    df[pd.to_datetime(df["fecha_pedido"], format="%Y-%m-%d", errors="coerce").isna()]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    El formato de la fecha de la fecha del pedido se detectaron 257 registros con el formato DD/MM/YYYY en lugar del estandár el cuál es YYYY-MM-DD.
    """)
    return


@app.cell
def _(df):
    df[~df["email_cliente"].str.contains("@", na=False) | (df["email_cliente"] != df["email_cliente"].str.strip().str.lower())]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    La tabla email_cliente, los emails son válidos, no hay ninguno que esté invalido.
    """)
    return


@app.cell
def _(df, pd):
    desc_check = pd.to_numeric(df["descuento_pct"], errors="coerce")
    df[desc_check.isna() | (desc_check < 0) | (desc_check > 100)]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    No hay descuentos fuera del rango < 0, > 100 o nulos.
    """)
    return


@app.cell
def _():
    import duckdb

    with duckdb.connect("dags/valhalla.duckdb", read_only=True) as con_respuestas:
        queries = [q.strip() for q in open("dags/sql/consultas.sql", encoding="utf-8").read().split(";") if q.strip()]
        resultados_consultas = [con_respuestas.sql(q).df() for q in queries]

    resultados_consultas
    return (resultados_consultas,)


@app.cell
def _(resultados_consultas):
    promedio_mensual = round(resultados_consultas[1]["facturacion_mensual"].mean(), 2)
    promedio_mensual
    return


if __name__ == "__main__":
    app.run()
