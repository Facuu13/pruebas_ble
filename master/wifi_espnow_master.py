import network
import espnow
import time

SSID = "quepasapatejode"   # Nombre de la red WiFi 
PASSWORD = "losvilla08"    # Contraseña de la red WiFi

# Diccionario para mapear direcciones MAC a nombres
MAC_A_NOMBRE = {
    b'\x08\xb6\x1f\x81\x19 ': "sensor-DHT11",
    b'00\xf9\xed\xd0\xe4' : "Placa-1",
    # Agrega aquí otras direcciones MAC y sus nombres
}

def wifi_reset():
    sta = network.WLAN(network.STA_IF); sta.active(False)
    ap = network.WLAN(network.AP_IF); ap.active(False)
    sta.active(True)    # Activar el modo estación
    while not sta.active():   
        time.sleep(0.1)
    sta.disconnect()   
    while sta.isconnected():   # Esperar hasta que se desconecte de cualquier red WiFi anterior
        time.sleep(0.1)
    return sta, ap   # Devolver los objetos de estación y punto de acceso

# Función de callback para recibir datos
def recv_cb(e):
    while True:    # Leer todos los mensajes que esperan en el búfer
        mac, msg = e.irecv(0)   # No esperar si no hay mensajes
        if mac is None:   # Si no hay dirección MAC, salir del bucle
            return
        nombre = MAC_A_NOMBRE.get(mac, "desconocido")
        print("Mensaje recibido de:", nombre)
        print("MAC:", mac)
        print("Mensaje:", msg)
        procesar_mensaje(msg)  # Procesar el mensaje recibido

def procesar_mensaje(msg):
    # Decodificar el mensaje de bytearray a string
    mensaje_decodificado = msg.decode('utf-8')
    print("Mensaje decodificado:", mensaje_decodificado)

def conectar_wifi(ssid,password):
    sta = network.WLAN(network.STA_IF)
    sta.connect(ssid, password)
    
    while not sta.isconnected():
        time.sleep(0.1)
    
    print("Conectado a:", ssid)
    print("Dirección IP:", sta.ifconfig()[0])
    
    sta.config(pm=sta.PM_NONE)   # Deshabilitar el ahorro de energía después de la conexión
    print("Proxy corriendo en el canal:", sta.config("channel")) # Imprimir el canal en el que se está ejecutando
    
    return sta

def activar_espNow():
    e = espnow.ESPNow()
    e.active(True)
    return e


sta, ap = wifi_reset()

sta = conectar_wifi(SSID,PASSWORD)  

e = activar_espNow()

# Asignar la función de callback a ESP-NOW
e.irq(recv_cb)   # Establecer la función recv_cb como la función de callback para manejar los datos recibidos