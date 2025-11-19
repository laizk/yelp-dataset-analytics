from datetime import datetime
from airflow.sdk import dag, task


@dag(
    dag_id="simple_decorators_dag",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    description="Simple Airflow 3.1 DAG using decorators",
)
def test_dag():

    @task
    def say_hello():
        print("Hello from Airflow 3.1 TaskFlow API!")
        return "Hello!"

    @task
    def follow_up(message: str):
        print(f"Received: {message}")

    # Task dependency using function calls
    msg = say_hello()
    follow_up(msg)


test_dag()
