# Diseño de Servicios Telemáticos

Este repositorio contiene un proyecto completo sobre diseño e implementación de servicios telemáticos, cubriendo protocolos de comunicación fundamentales como TCP/UDP, MQTT y SMTP, así como técnicas de autenticación mediante códigos OTP (One-Time Password).

## 📋 Descripción del Proyecto

Este proyecto está estructurado en tres prácticas que abordan diferentes aspectos de los servicios telemáticos:

- **Práctica 1**: Comunicaciones TCP/UDP y autenticación OTP
- **Práctica 2**: Protocolo MQTT para comunicación pub/sub
- **Práctica 3**: Protocolo SMTP y envío de correos electrónicos

## 📁 Estructura del Proyecto

```
design_telematic_services/
├── P1/                              # Práctica 1: TCP/UDP y OTP
│   ├── main.py                      # Cliente principal con autenticación OTP
│   ├── tcp_server.py               # Servidor TCP básico
│   ├── tcp_client.py               # Cliente TCP básico
│   ├── udp_server.py                # Servidor UDP con mensajes bidireccionales
│   ├── udp_client.py                # Cliente UDP interactivo
│   ├── pyotp_uri.py                 # Generación y validación de códigos OTP
│   └── Práctica 1 Tema 1.pdf        # Enunciado de la práctica
│
├── P2/                              # Práctica 2: Protocolo MQTT
│   ├── main.py                      # Cliente MQTT con suscripción y publicación
│   ├── pub.py                       # Publicador MQTT simple
│   ├── sub.py                       # Suscriptor MQTT con wildcards
│   ├── other.py                     # Ejemplo de conexión con callbacks
│   └── Practica 2 MQTT 2024.pdf     # Enunciado de la práctica
│
├── P3/                              # Práctica 3: Protocolo SMTP
│   ├── main.py                      # Envío de correo con adjuntos (PDF)
│   ├── 822.py                       # Envío de correo según RFC 822
│   ├── valida.py                    # Validación de direcciones de email
│   ├── main_carlos.py               # Versión alternativa del cliente SMTP
│   ├── docu.pdf                     # Documentación adjunta
│   └── prac3.pdf                    # Enunciado de la práctica
│
├── requirements.txt                 # Dependencias del proyecto
└── README.md                        # Este archivo
```

## 🛠️ Funcionalidades por Práctica

### Práctica 1: Comunicaciones TCP/UDP y Autenticación OTP

**Objetivo**: Implementación de servidores y clientes TCP/UDP, y sistema de autenticación mediante códigos OTP (One-Time Password).

#### Componentes:

**1. Servidores y Clientes TCP/UDP**

- `tcp_server.py`: Servidor TCP que acepta conexiones y envía mensajes de bienvenida
- `tcp_client.py`: Cliente TCP que se conecta al servidor y recibe mensajes
- `udp_server.py`: Servidor UDP que recibe mensajes y permite respuesta interactiva
- `udp_client.py`: Cliente UDP interactivo para envío de mensajes

**2. Autenticación OTP**

- `pyotp_uri.py`: Generación de códigos OTP usando TOTP (Time-based OTP)
- Generación de URIs para códigos QR de autenticación
- Validación de códigos OTP ingresados por el usuario

**3. Cliente Principal**

- `main.py`: Cliente que combina TCP con autenticación OTP
  - Genera código OTP basado en DNI
  - Se conecta a servidor remoto
  - Envía nombre, DNI y código OTP
  - Recibe respuesta del servidor

**Ejemplo de uso**:

```python
# Generar código OTP
python P1/pyotp_uri.py

# Ejecutar servidor TCP
python P1/tcp_server.py

# Ejecutar cliente TCP
python P1/tcp_client.py

# Ejecutar servidor UDP
python P1/udp_server.py

# Ejecutar cliente UDP
python P1/udp_client.py

# Cliente principal con OTP
python P1/main.py
```

**Características**:

- Comunicación TCP orientada a conexión
- Comunicación UDP sin conexión
- Autenticación mediante TOTP (Time-based One-Time Password)
- Generación de secretos basados en DNI
- Soporte para códigos QR mediante URIs de provisioning

### Práctica 2: Protocolo MQTT

**Objetivo**: Implementación de clientes MQTT para publicación y suscripción a topics, implementando el patrón pub/sub.

#### Componentes:

**1. Publicador Simple**

- `pub.py`: Publica mensajes ON/OFF en un topic específico
- Conexión a broker MQTT
- Publicación de mensajes en topic `salon/luz`

**2. Suscriptor con Wildcards**

- `sub.py`: Se suscribe a topics usando wildcards (`#`)
- Recibe y procesa mensajes mediante callbacks
- Suscripción a topic `salon/#` (todos los subtopics)

**3. Cliente Completo**

- `main.py`: Implementa un sistema completo de petición/respuesta
  - Publica DNI en topic `DST/PETICION`
  - Se suscribe a topic `DST/CODIGO`
  - Procesa código recibido y publica solución en `DST/SOLUCION`
  - Autenticación con usuario y contraseña

**4. Ejemplo de Conexión**

- `other.py`: Demuestra manejo de callbacks de conexión
- Implementa timeout y manejo de errores

**Ejemplo de uso**:

```python
# Publicar mensaje
python P2/pub.py

# Suscribirse a topic
python P2/sub.py

# Cliente completo (petición/respuesta)
python P2/main.py
```

**Características**:

- Protocolo MQTT v5 (CallbackAPIVersion.VERSION2)
- Soporte para wildcards en topics (`#`, `+`)
- Callbacks para eventos (on_message, on_connect)
- Autenticación con usuario/contraseña
- Manejo de loops asíncronos (loop_start, loop_forever)
- Desconexión y limpieza de recursos

**Topics utilizados**:

- `DST/PETICION`: Para enviar peticiones (DNI)
- `DST/CODIGO`: Para recibir códigos del servidor
- `DST/SOLUCION`: Para enviar soluciones
- `salon/luz`: Ejemplo de control domótico
- `salon/#`: Wildcard para todos los subtopics de salon

### Práctica 3: Protocolo SMTP y Correo Electrónico

**Objetivo**: Implementación de clientes SMTP para envío de correos electrónicos, incluyendo validación de direcciones y envío de adjuntos.

#### Componentes:

**1. Validación de Email**

- `valida.py`: Valida formato de direcciones de correo electrónico
- Usa librería `validate_email` para verificar formato
- Incluye ejemplos de direcciones válidas e inválidas
- Bucle interactivo hasta recibir dirección válida

**2. Envío según RFC 822**

- `822.py`: Implementa envío de correo según RFC 822
- Uso de `EmailMessage` para construcción del mensaje
- Validación de destinatario antes de enviar
- Ajuste automático de líneas a 78 caracteres
- Entrada interactiva del cuerpo del mensaje

**3. Envío con Adjuntos**

- `main.py`: Envía correo electrónico con adjunto PDF
- Usa `MIMEMultipart` para mensajes multipart
- Adjunta archivos PDF mediante `MIMEApplication`
- Validación de email antes de enviar
- Manejo de errores y excepciones SMTP

**Ejemplo de uso**:

```python
# Validar dirección de email
python P3/valida.py

# Enviar correo según RFC 822
python P3/822.py

# Enviar correo con adjunto PDF
python P3/main.py
```

**Características**:

- Protocolo SMTP en puerto 25
- Soporte para STARTTLS (seguridad)
- Validación de formato de email
- Envío de mensajes de texto plano
- Envío de adjuntos (PDFs)
- Codificación UTF-8 para caracteres especiales
- Manejo de errores SMTP
- Uso de servidor SMTP de UPV (`smtp.upv.es`)

**Configuración**:

- Servidor SMTP: `smtp.upv.es`
- Puerto: 25
- Autenticación: Opcional (comentada en código)
- STARTTLS: Habilitado

## 📦 Dependencias

Las principales librerías utilizadas en el proyecto son:

```python
pyotp              # Generación y validación de códigos OTP
paho-mqtt          # Cliente MQTT para Python
validate-email     # Validación de direcciones de correo
```

### Instalación

Para instalar las dependencias principales:

```bash
pip install pyotp paho-mqtt validate-email
```

O instalar todas las dependencias del archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

**Nota**: El archivo `requirements.txt` incluye también dependencias de Jupyter y otras herramientas de desarrollo.

## 🚀 Uso General

### Práctica 1: TCP/UDP y OTP

1. **Ejecutar servidor TCP**:

   ```bash
   cd P1
   python tcp_server.py
   ```

2. **Ejecutar cliente TCP** (en otra terminal):

   ```bash
   python tcp_client.py
   ```

3. **Generar código OTP**:

   ```bash
   python pyotp_uri.py
   ```

4. **Cliente con autenticación OTP**:
   ```bash
   python main.py
   ```

### Práctica 2: MQTT

1. **Asegúrate de tener acceso al broker MQTT** (por defecto: `158.42.32.220:1883`)

2. **Publicar mensaje**:

   ```bash
   cd P2
   python pub.py
   ```

3. **Suscribirse a topic**:

   ```bash
   python sub.py
   ```

4. **Cliente completo**:
   ```bash
   python main.py
   ```

### Práctica 3: SMTP

1. **Validar email**:

   ```bash
   cd P3
   python valida.py
   ```

2. **Enviar correo simple**:

   ```bash
   python 822.py
   ```

3. **Enviar correo con adjunto**:
   ```bash
   # Asegúrate de ajustar la ruta del PDF en main.py
   python main.py
   ```

## 🔧 Configuración

### Práctica 1

Ajusta las siguientes variables en `main.py`:

```python
DNI = os.getenv("DNI")                     # Tu DNI
NAME = os.getenv("NAME")          # Tu nombre
IP_ADDRESS = "158.42.32.220"        # IP del servidor
PORT = 21000                        # Puerto del servidor
```

### Práctica 2

Ajusta las siguientes variables según tu configuración:

```python
MQTT_BROKER = "158.42.32.220"      # IP del broker MQTT
MQTT_PORT = 1883                    # Puerto del broker
USERNAME = "dst"                    # Usuario MQTT
PASSWORD = "dst"                    # Contraseña MQTT
DNI = os.getenv("DNI")                     # Tu DNI
EMAIL = os.getenv("EMAIL_FROM")         # Tu email
```

### Práctica 3

Ajusta las siguientes variables:

```python
SMTP_SERVER = "smtp.upv.es"         # Servidor SMTP
SMTP_PORT = 25                      # Puerto SMTP
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")
PDF_PATH = "ruta/al/archivo.pdf"    # Ruta del PDF a adjuntar
```

## 📝 Conceptos Clave

### TCP vs UDP

- **TCP**: Protocolo orientado a conexión, confiable, con control de flujo
- **UDP**: Protocolo sin conexión, más rápido, sin garantías de entrega

### OTP (One-Time Password)

- **TOTP**: Time-based OTP, código que cambia cada cierto tiempo
- **Secreto**: Generado a partir del DNI usando codificación base32
- **URI de provisioning**: Formato estándar para generar códigos QR

### MQTT (Message Queuing Telemetry Transport)

- **Pub/Sub**: Patrón de publicación/suscripción
- **Topics**: Jerarquía de temas para organizar mensajes
- **Wildcards**: `#` (multi-nivel) y `+` (single-level)
- **QoS**: Niveles de calidad de servicio (0, 1, 2)

### SMTP (Simple Mail Transfer Protocol)

- **RFC 822**: Estándar para formato de mensajes de correo
- **MIME**: Extensión para adjuntos y contenido multimedia
- **STARTTLS**: Seguridad mediante cifrado TLS
- **Puerto 25**: Puerto estándar para SMTP

## 🎯 Objetivos de Aprendizaje

Este proyecto cubre:

1. **Comunicaciones de red**: TCP y UDP sockets en Python
2. **Autenticación**: Sistemas OTP y generación de códigos temporales
3. **Protocolos de mensajería**: MQTT y patrón pub/sub
4. **Correo electrónico**: Protocolo SMTP y formato de mensajes
5. **Validación**: Verificación de formatos y datos de entrada
6. **Manejo de errores**: Gestión de excepciones en comunicaciones de red

## 🔒 Seguridad

**Notas importantes**:

- Los códigos OTP proporcionan autenticación de dos factores
- MQTT puede usar TLS/SSL para conexiones seguras
- SMTP con STARTTLS cifra la comunicación
- Las credenciales deben manejarse de forma segura (variables de entorno)

## 📄 Licencia

Este es un proyecto académico para fines educativos.

## 👤 Autor

Proyecto desarrollado como parte del curso de Diseño de Servicios Telemáticos.

**Autor**: Oscar Jimenez Bou

---

**Nota**: Asegúrate de tener acceso a los servidores remotos (broker MQTT, servidor TCP) antes de ejecutar las prácticas. Algunos scripts pueden requerir ajustes de configuración según tu entorno.
