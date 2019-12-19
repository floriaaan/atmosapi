import network

def connect_Tetra():

    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)
    sta_if.active((True))
    ap_if.active((False))
    sta_if.ifconfig(('192.168.43.100', '255.255.255.0', '192.168.0.1', '8.8.8.8'))
    sta_if.connect('Tetra+', '28042000')

    if sta_if.isconnected()==True:
        print('Connexion success on "Tetra+" with IP : 192.168.43.100')
    if sta_if.isconnected()==False:
        print('Connexion on "Tetra+" failed')
        
