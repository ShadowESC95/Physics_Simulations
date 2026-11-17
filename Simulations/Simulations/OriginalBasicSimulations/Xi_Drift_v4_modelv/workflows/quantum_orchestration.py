# workflows/quantum_orchestration.py
from airflow import DAG
from airflow.providers.pennylane.operators.quantum import QuantumCircuitOperator

with DAG('hybrid_simulation') as dag:
    qc_task = QuantumCircuitOperator(
        device="lightning.qubit",
        circuit="circuits/field_ansatz.qml",
        outputs_to_xcom=True
    )
    classical_ml = PythonOperator(task_id="postprocess", python_callable=analyze_results)
    qc_task >> classical_ml
