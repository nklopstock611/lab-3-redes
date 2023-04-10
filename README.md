# Laboratorio 3: Implementación de Servidor y Cliente TCP y UDP

[Contexto](#contexto)

[Protocolo TCP](#tcp)

[Protocolo UDP](#udp)

[Ejecución](#ejecucion)

## <a name="contexto"></a> Contexto

- Durante el laboratorio se puede utilizar las máquinas propias de los integrantes del grupo o hacer
uso de la infraestructura del laboratorio. En caso de elegir utilizar la infraestructura del laboratorio
esta decisión debe ser informada lo antes posible al profesor de laboratorio para que se habilite el
acceso a la máquina virtual correspondiente.
- Durante el desarrollo de este laboratorio usted desarrollará un servidor de transferencia de archivos
y un aplicativo cliente usando el protocolo TCP; de tal forma que se logre una comunicación entre
estos desarrollos utilizando una arquitectura del tipo cliente-servidor.

![Diagrama de comunicación por socket TCP](https://www.solvetic.com/uploads/monthly_12_2013/tutorials-2308-0-27579200-1385956835.jpg "Diagrama de comunicación por socket TCP")

- Durante el desarrollo de este laboratorio usted desarrollará un servidor de transferencia de archivos
y de un aplicativo cliente usando el protocolo UDP; de tal forma que se logre una comunicación
entre estos desarrollos utilizando una arquitectura del tipo cliente-servidor.
- Se recomienda leer la guía completamente antes de iniciar a resolver las actividades propuestas,
con el objetivo de tener presente las actividades y los entregables a desarrollar.

## <a name="tcp"></a> Procedimiento Protocolo TCP

Finalmente, se espera que se implementen pruebas de carga y desempeño sobre la arquitectura desarrollada, con el fin de evaluar el funcionamiento del servicio mediante métricas de desempeño como: total de bytes transmitidos por el servidor, tiempo de transferencia promedio medido en servidor, tasa de transferencia promedio medido en servidor, total de bytes recibidos por el cliente, tiempo de transferencia promedio medido en cliente, tasa de transferencia promedio medido en cliente. Esto permitirá realizar un análisis de rendimiento de las transferencias con el protocolo TCP en diferentes escenarios. Por último, usted deberá subir sus aplicativos de cliente y servidor en Github. Asegúrese de incluir un archivo readme en donde se pueda encontrar instrucciones sobre la instalación y ejecución de cada uno de los programas.

### <a name="tcp"></a> Video
https://www.youtube.com/watch?v=TiOtoiMAwJY 

## <a name="udp"></a> Procedimiento Protocolo UDP

Tal como se enuncio en el anterior apartado, en este laboratorio se debe realizar un desarrollo de un servicio de transferencia de archivo utilizando el protocolo de datagramas de usuario (UDP por sus siglas
en inglés) emulando una arquitectura cliente – servidor. Finalmente, se espera que se implementen pruebas de carga y desempeño sobre la arquitectura desarrollada, con el fin de evaluar el funcionamiento del servicio mediante métricas de desempeño, como: total de bytes transmitidos por el servidor, tiempo de transferencia promedio medido en servidor, tasa de transferencia promedio medido en servidor, total de bytes recibidos por el cliente, tiempo de transferencia promedio medido en cliente, tasa de transferencia promedio medido en cliente. Esto permitirá realizar un análisis de rendimiento de las transferencias con el protocolo UDP y posteriormente, hacer una comparación con los resultados obtenidos del servicio funcionando con el protocolo TCP. Por último, usted deberá subir sus aplicativos de cliente y servidor en Github. Asegúrese de incluir un
archivo readme en donde se pueda encontrar instrucciones sobre la instalación y ejecución de cada uno de los programas.

### <a name="udp"></a> Video
https://www.youtube.com/watch?v=S-TI389QuXk

## <a name="ejecucion"></a> Ejecución

- Cambiar IP y el puerto en archivos de cliente y servidor de ambos protocolos
```bash
server_address = ("IP", "PORT")
```

- Si se quiere, se puede modificar el tiempo del temporizador en el archivo del cliente de UDP
```bash
sock.settimeout("TIEMPO (segundos)")
```
