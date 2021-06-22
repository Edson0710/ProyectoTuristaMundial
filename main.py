import random

"""
Notas importantes:
- Hay casillas que no tienen función ya que no se especifican en los requerimientos (visa, embajada, consulado)
- Es muy probable que el jugador siempre gane si se inicializa con las propiedades que indica el requerimiento
- Si se quitan las propiedades al inicio, la probabilidad cae a 50-50, por lo que se alarga mucho el juego
- Cada que gana el jugador, el juego se reinicia
- Cuando pierde el jugador, el programa se termina
- Para demostrar que el jugador tambien pierde, se puede bajar su cantidad de BTC
- El juego se puede hacer turno por turno al descomentar el ultimo input()
- Por predeterminado el juego se detiene hasta que alguno de los dos pierde
- Por predeterminado el juego decide de manera aleatoria si se compran las propiedades o no
"""

#   Variables
#   0 -> Nombre, 1 -> Posicion, 2 -> BTC, 3 -> propiedades
jugadores = [["",0,10000,[]], ["CPU",0,10000,[]]]
turnos = 0

nombre = input("Nombre: ")
color = input("Color: ")

#   Propiedades al iniciar el juego
def inicializarPropiedades():
    jugadores[0][3] = [["EUA",200], ["BRASIL",200], ["ITALIA",300], ["ALEMANIA",300], ["EGIPTO", 400], ["ARGELIA", 400], ["MADAGASCAR",500], ["RUSIA",300], ["TURQUIA",400], ["CHINA",500]]

#   Inicializar juego
def inicializar():
    global turnos
    turnos = 0
    global jugadores
    #   Aqui se modifican los valores iniciales
    jugadores = [[nombre,0,10000,[]], ["CPU",0,10000,[]]]
    #   Comentar la linea de abajo para no iniciar con propiedades
    inicializarPropiedades()

#   Tableros
tableroA = [["salida",0], ["MEXICO",100], ["EUA",200], ["visa",0], ["COSTA RICA",200], ["L.A. Americana",300], ["PERU",200], ["ARGENTINA",200], ["correo",0], ["BRASIL",200], ["deportado",0]]
tableroB = [["ESPAÑA",300], ["ITALIA",300], ["embajada",0], ["FRANCIA",300], ["L.A. Europea",300], ["INGLATERRA",300], ["sms",0], ["ALEMANIA",300], ["HOLANDA",300], ["OCEANIA",0]]
tableroC = [["EGIPTO", 400], ["MARRUECOS",400], ["correo",0], ["ARGELIA", 400], ["L.A. Africana",300], ["SUDAFRICA",400], ["CONGO",400], ["aduana",0], ["MADAGASCAR",500], ["GROELANDIA",0]]
tableroD = [["RUSIA",300], ["consulado",0], ["INDIA",400], ["TURQUIA",400], ["L.A. Asiatica",300], ["CHINA",500], ["sms",0], ["JAPON",500], ["TAILANDIA",600]]

#   Union de tableros
tableroA.extend(tableroB)
tableroA.extend(tableroC)
tableroA.extend(tableroD)

#   Tirar dados
def dados() -> int:
    dado1 = random.randint(1,6)
    dado2 = random.randint(1,6)
    return dado1 + dado2

#   Numero aleatorio entre dos opciones
def random1or2() -> int:
    return random.randint(1,2)

#   BTC aleatorio
def randombtc() -> int:
    return random.randint(100,800)

#   Casillas especiales
def casillas(casilla:str, jugador:int):
    if casilla == "sms" or casilla == "correo":
        btc = randombtc()
        op = random1or2()
        if op == 1:
            print("Pagas {} BTC al banco".format(btc))
            jugadores[jugador][2] -= btc
        if op == 2:
            print("Cobras {} BTC al banco".format(btc))
            jugadores[jugador][2] += btc
    elif casillas == "deportado":
        #   Vas a Groelandia
        print("Te vas a Groelandia")
        jugadores[jugador][1] = 30 
    else: 
        print("Solo estás de paso")

#   Marcador
def marcador():
    print("{}: {} {} BTC\t\tCPU: {} {} BTC".format(jugadores[0][0], tableroA[jugadores[0][1]][0], jugadores[0][2], tableroA[jugadores[1][1]][0], jugadores[1][2]))

#  Turnos
def turno(jugador:int, otro:int):
    tiro = dados()
    jugadores[jugador][1] += tiro
    print("\n" + jugadores[jugador][0])
    print("Avanza: " + str(tiro) + " casillas")
    #   Si la posicion es mayor o igual a 40 quiere decir que se completó uan vuelta
    if jugadores[jugador][1] >= len(tableroA):
        #   Se hace un ajuste para volver a iniciar una vuelta
        jugadores[jugador][1] = jugadores[jugador][1] - len(tableroA)
        #   Cobrar salida
        print("Pasaste por la salida, cobras 100 BTC")
        jugadores[jugador][2] += 100
    print("Nueva posicion: " + tableroA[jugadores[jugador][1]][0])
    #   Comprobar si la propiedad pertenece al otro jugador
    if tableroA[jugadores[jugador][1]] in jugadores[otro][3]:
        print("Vas a pagar {} al otro jugador por caer en su propiedad".format(tableroA[jugadores[jugador][1]][1]))
        jugadores[jugador][2] -= tableroA[jugadores[jugador][1]][1]
        jugadores[otro][2] += tableroA[jugadores[jugador][1]][1]
    #   Comprobar si la propiedad no te pertenece y si se puede comprar
    elif tableroA[jugadores[jugador][1]] not in jugadores[jugador][3] and tableroA[jugadores[jugador][1]][1] > 0:
        print("¿Quieres comprar {} por {} BTC?".format(tableroA[jugadores[jugador][1]][0], tableroA[jugadores[jugador][1]][1]))
        #   Comentar la linea de abajo para hacerlo automatico
        # op = input("1. Si or 2. No : ")
        #   Compentar las dos lines de abajo para hacerlo manual
        print("1. Si or 2. No : ")
        op = str(random1or2())
        if op == '1':
            jugadores[jugador][2] -= tableroA[jugadores[jugador][1]][1]
            if jugadores[jugador][2] >= 0:
                jugadores[jugador][3].append(tableroA[jugadores[jugador][1]])
                print("Compra exitosa")
            else:
                print("No tienes BTC suficientes")
                jugadores[jugador][2] += tableroA[jugadores[jugador][1]][1]
        elif op == '2':
            print("La propiedad no ha sido comprada")
        else:
            print("Opcion no valida, por ende no será comprada esta propiedad")
    #   Comprobar si la propiedad te pertenece
    elif tableroA[jugadores[jugador][1]] in jugadores[jugador][3]:
        print("{} es de tu propiedad".format(tableroA[jugadores[jugador][1]][0]))
    #   Caiste en una casilla especial
    else:
        print("Caiste en una casilla de {}".format(tableroA[jugadores[jugador][1]][0]))
        casillas(tableroA[jugadores[jugador][1]][0], jugador)
            

inicializar()
while True:
    turnos += 1
    print("----------------------------------------------------------------------")
    print("\tTurno " + str(turnos))
    marcador()
    turno(0,1)
    #   Comprobar si jugador pierde o no
    if jugadores[0][2] < 0:
        print("{} ha perdido. Fin del juego".format(jugadores[0][0]))
        input()
        break
    turno(1,0)
    #   Comprobar si CPU perdio, si fue así, el juego se vuelve a iniciar
    if jugadores[1][2] < 0:
        print("{} ha perdido. Presiona enter para seguir jugando".format(jugadores[1][0]))
        inicializar()
        input()
    # input()


