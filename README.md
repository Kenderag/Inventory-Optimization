📦 Configuración Requerida para el Cluster en Databricks Community Edition
Librerías a instalar (para ETL en streaming con Kafka + Snowflake):

Tipo	Librería/Paquete	Método de Instalación	Notas
Maven	net.snowflake:spark-snowflake_2.12:2.11.0	Pestaña "Libraries" > Install > Maven	Ajustar versión (2.12) según tu Runtime
Maven	net.snowflake:snowflake-jdbc:3.14.0	Pestaña "Libraries" > Install > Maven	Requerido para el conector Spark-Snowflake
PyPI	snowflake-connector-python==3.2.0	Notebook: %pip install snowflake-connector-python==3.2.0	Para operaciones con Python
PyPI	spark-sql-kafka-0-10_2.12==3.5.0	Notebook: %pip install spark-sql-kafka-0-10_2.12==3.5.0	Conector para Kafka
PyPI	pyarrow==10.0.1	Notebook: %pip install pyarrow==10.0.1	Manejo eficiente de datos
📌 Pasos para Instalación:
Crear un cluster:

Runtime recomendado: Databricks Runtime 11.3 LTS (compatible con las librerías mencionadas).

Tipo: Single Node (Community Edition solo permite esto).

Instalar librerías Maven:

Ir a la pestaña "Libraries" en la configuración del cluster.

Hacer clic en "Install New" > Seleccionar "Maven".

Pegar las coordenadas de Maven (ver tabla arriba).

Instalar librerías PyPI:

Abrir un nuevo notebook conectado al cluster.

Ejecutar los comandos %pip install indicados en la tabla.

Reiniciar el cluster después de instalar.

Verificar instalación:

python
Copy
spark.sparkContext.listPackages()  # Mostrará las librerías instaladas
⚠️ Notas importantes:
En Community Edition, las librerías se pierden al terminar el cluster. Debes reinstalarlas en cada nueva sesión.

Espacio limitado: Evita instalar librerías innecesarias (solo las de la tabla).

Si falla la instalación por Maven, usa el método alternativo con código en un notebook (te comparto el ejemplo si lo necesitas).

📂 Documentación de referencia:
Conector Snowflake para Spark

Conector Kafka para Spark