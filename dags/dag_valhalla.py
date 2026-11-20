import sys
from pathlib import Path
from datetime import datetime
from airflow.sdk import dag, task

DAGS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(DAGS_DIR))

from pipeline import extract, validate, clean_and_load

@dag(
    dag_id="etl_valhalla_pedidos",
    start_date=datetime(2026, 11, 1),
    schedule="0 2 * * *",
    catchup=False,
)
def valhalla_etl_dag():

    @task
    def tarea_extraer():
        extract()

    @task
    def tarea_validar():
        validate()

    @task
    def tarea_limpiar_y_cargar():
        clean_and_load()

    tarea_extraer() >> tarea_validar() >> tarea_limpiar_y_cargar()

valhalla_etl_dag()