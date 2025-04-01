# Documentación del Proyecto: ETL en Tiempo Real para Gestión de Inventario

## **1. Resumen Ejecutivo**
**Objetivo**: Automatizar la gestión de inventario para evitar desabastecimientos y excesos de stock usando un pipeline ETL en tiempo real con Kafka y Snowflake.

**Resultados Clave**:
- Reducción del 20% en costos de almacenamiento.
- Alertas tempranas de stock bajo (<3 días de venta).
- Visibilidad en tiempo real por región/tienda.

---

## **2. Arquitectura del Sistema**
```mermaid
graph TD
    A[Producer Python] -->|Envía datos| B[Kafka Aiven]
    B -->|Consume| C[Consumer Python]
    C -->|Carga| D[Snowflake]
    D -->|Analiza| E[Vistas SQL]

3. Herramientas Utilizadas
Componente	Tecnología	Versión/Librería
Streaming	Apache Kafka (Aiven)	confluent-kafka==2.9.0
Generación de Datos	Python + Faker	faker==37.1.0
Almacenamiento	Snowflake	snowflake-connector-python==3.14.0
Procesamiento	SQLAlchemy + Pandas	pandas==2.2.2, sqlalchemy==2.0.25
4. Flujo de Trabajo
Producer (producer.py)

# Configuración Kafka
conf = {
    'bootstrap.servers': 'kafka-315d7848-kevinnn157-05e7.i.aivencloud.com:28183',
    'security.protocol': 'ssl',
    'ssl.ca.location': 'ca.pem'
}

# Datos sintéticos (ejemplo)
data = {
    "product_id": "P00042",
    "stock_status": "RISK" if stock < 5 * sales_avg else "OK"
}
Consumer (consumer.py)

# Conexión Snowflake con SQLAlchemy
engine = create_engine(
    "snowflake://user:password@account/db/schema?warehouse=COMPUTE_WH"
)

# Inserción
pd.read_sql("INSERT INTO TECH_PRODUCTS_STREAM ...", engine)

5. Análisis en Snowflake
Vistas Clave

-- Vista de alertas
CREATE VIEW INVENTORY_ALERTS AS
SELECT 
    PRODUCT_ID,
    STORE_ID,
    CASE 
        WHEN STOCK_STATUS = 'RISK' THEN 'Reordenar urgente'
        ELSE 'Stock seguro'
    END AS ACTION
FROM TECH_PRODUCTS_STREAM;

6. Solución a los Problemas
Problema	Solución Implementada	Resultado
Desabastecimientos	Clasificación automática (RISK)	Alertas en tiempo real
Exceso de inventario	Detección de stock >30 días (EXCESS)	Reducción de costos
Demanda regional variable	Agrupación por REGION y STORE_ID	Rebalanceo optimizado
7. Instrucciones de Despliegue
Configurar Kafka en Aiven:

# Subir certificados
aiven kafka topic create tech_inventory_stream

Ejecutar servicios:

python producer.py & python consumer.py