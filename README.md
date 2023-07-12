# Docu y Detalles de los Scripts

## File gl_create_alert.py

> Texto generado con Chat GTP

El código es un script en python que es utilizado en el marco de la implementación de un proceso de seguridad en el desarrollo de aplicaciones (DevSecOps) y que utiliza la API de GitLab para conectarse a un proyecto específico y obtener información de las distintas ejecuciones de las tuberías de compilación (pipelines). La idea es que si alguna de las ejecuciones falla, se generen alertas automáticas para el equipo de seguridad, que le permitan detectar rápidamente cualquier problema de seguridad y trabajar en solucionarlo. A continuación, se describen las partes más importantes del script:

1. En las primeras líneas, se definen un conjunto de variables que son obtenidas a partir de variables de entorno, que deben ser definidas previamente. Algunas de estas variables son utilizadas para obtener información del proyecto y las ejecuciones de las tuberías de compilación.

2. Luego, se hace una llamada a la API de GitLab para obtener información sobre la ejecución de la tubería de compilación que corresponde a la herramienta de seguridad que se está ejecutando. Esto se hace a través de la función "get_jobs()", que se encarga de buscar la ejecución correspondiente en la lista de ejecuciones de la tubería.

3. A continuación, se verifica si la ejecución de la herramienta de seguridad falló, en cuyo caso se genera una alerta. Si la ejecución fue exitosa, no se hace nada más.

4. En la siguiente sección del script, se genera una alerta a través de una llamada a un servicio externo, que recibe un conjunto de parámetros. Este servicio genera un registro de la alerta en una herramienta de gestión de incidentes, que permite hacer un seguimiento y una gestión más efectiva de los incidentes de seguridad.

5. Finalmente, se busca una incidencia abierta en el proyecto que corresponda a la alerta generada. Si no existe, se crea una nueva incidencia y se asigna a los responsables de seguridad. También se agrega un conjunto de etiquetas a la incidencia que permiten identificar la naturaleza del incidente, y se genera un mensaje con la información relevante para enviar a través de un servicio de mensajería instantánea. En caso de que ya exista una incidencia abierta, se agrega un comentario a la misma con la información relevante.
