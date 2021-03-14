import logging
from time import sleep
from selenium import webdriver
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Configurar loggin
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

#logger del usuario
logger = logging.getLogger()

#comando start
def start(update, context):
    print(update)
    nombre=update.effective_user['first_name']
    update.message.reply_text(f'Hola {nombre} este es un bot con fines academicos.\n '
                              'A partir de este bot puedes buscar vuelos disponibles ' 
                              'y ver la disponibilidad de reservar vuelos.\n'
                              'Toda información, busqueda y resultados son obtenidos de despegar.com.ec\n'
                              'Ingrese el comando /help para mayor información y ver los comandos disponibles')

#comando help
def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Los comandos disponibles son:\n\n'
                              '1. /start -> Iniciar bot\n\n'
                              '2. /help -> Listado de comandos\n\n'
                              '3. /LIST -> Listado de vuelos disponibles\n\n'
                              '4. /SEARCHD [IATA code] -> Mostrar todos los vuelos disponibles a ese destino\n\n'
                              '5. /SEARCHO [IATA code] -> Mostrar todos los vuelos disponibles desde ese origen\n\n'
                              '6. /BUY_TICKET [Parameters] -> Mostrar todos los tickets/vuelos de solo ida disponibles de compra a partir de sus especificaciones\n'
                              '7. /BUYRT_TICKET [Parameters] -> Mostrar todos los tickets/vuelos ida y vuelta disponibles de compra a partir de sus especificaciones\n')

#comando list
def list_command(update, context):
    CPaises = ['GYE', 'UIO', 'GRU', 'BOG', 'SCL', 'LIM', 'CGH', 'GIG', 'AEP', 'MEX', 'LAX', 'JFK', 'DUB', 'FRA', 'HKG',
               'YYZ', 'MIA', 'MAD', 'BCN', 'SJO', 'PTY', 'BAQ', 'MVD', 'BQN', 'HND', 'AMS', 'ORY', 'SYD']
    CPaises2 = CPaises
    driver = webdriver.Chrome('./chromedriver.exe')
    update.message.reply_text('La busqueda de vuelos esta en proceso.\n'
                              'Este proceso puede tardar unos segundos'
                              ' debido a que las busquedas se realizan en tiempo'
                              ' real.\n'
                              'En cuanto se acabe de realizar el listado'
                              ' se le notificara con un mensaje.\n'
                              'Porfavor sea paciente')
    for j in CPaises:
        for k in CPaises2:
            driver.get(f'https://www.despegar.com.ec/vuelos/{j}/{k}/')

            vuelos = driver.find_elements_by_class_name('reduced-cluster.margin-bottom-reduced-cluster')

            listprecio = list()

            info = driver.find_element_by_class_name('ux-common-results-title').text

            for vuelo in vuelos:
                precio = vuelo.find_element_by_class_name('pricebox-big-text.price').text
                listprecio.append(precio)
                # listprecio.append(precio)

            # print("Precio de los vuelos:")
            # print(listprecio)

            listida = list()

            for vuelo in vuelos:
                ida = vuelo.find_elements_by_class_name('cluster-part-0')
                for i in ida:
                    listida.append(i.text)

            listreg = list()

            for vuelo in vuelos:
                reg = vuelo.find_elements_by_class_name('cluster-part-1')
                for i in reg:
                    listreg.append(i.text)
                # print(reg)

            aux = 0
            for i in listida:
                listida[aux] = i.replace("\n-", " - ").replace("\n", " - ").replace("  ", " ").replace("- -", "-")
                aux = aux + 1

            aux = 0
            for i in listreg:
                listreg[aux] = i.replace("\n-", " - ").replace("\n", " - ").replace("  ", " ").replace("- -", "-")
                aux = aux + 1

            listidavuelta = zip(listida, listreg, listprecio)
            listidavuelta = tuple(listidavuelta)

            print(info)
            numeracion = 1
            for i in range(len(listidavuelta)):
                update.message.reply_text(str(numeracion) + '\n' +
                                          str(info) + '\n' +
                                          str(listidavuelta[i][0]) + '\n' +
                                          str(listidavuelta[i][1]) + '\n' +
                                          'Precio: ' + str(listidavuelta[i][2]) + ' $\n')
                numeracion = numeracion + 1

#comando brt_ticket
def BUYRT_TICKET_command(update, context):
    busqueda = 1
    if not context.args:
        busqueda = 0
        update.message.reply_text('Introduzca los parametros adecuados\n'
                                  'Ejemplo: "/BUYRT_TICKET GYE AMS 2021-05-29 2021-06-16 3"\n'
                                  'Para mas información use /help')
    while busqueda == 1:
        try:
            update.message.reply_text('La busqueda de vuelos esta en proceso.\n'
                                      'Este proceso puede tardar unos segundos'
                                      ' debido a que las busquedas se realizan en tiempo'
                                      ' real.\n'
                                      'En cuanto se acabe de realizar el listado'
                                      ' se le notificara con un mensaje.\n'
                                      'Porfavor sea paciente')
            origen = ''
            destino = ''
            Fsal = ''
            Fret = ''
            Nasientos = ''
            try:
                origen = context.args[0]
                destino = context.args[1]
                Fsal = context.args[2]
                Fret = context.args[3]
                Nasientos = context.args[4]
            except:
                update.message.reply_text('Error en los datos de busqueda')

            # -------------------------------------------------

            driver = webdriver.Chrome('./chromedriver.exe')

            driver.get(
                f'https://www.despegar.com.ec/shop/flights/results/roundtrip/{origen}/{destino}/{Fsal}/{Fret}/{Nasientos}/0/0/NA/NA/NA/NA/NA?from=SB&di={Nasientos}-0')

            sleep(5)

            for i in range(3):
                try:
                    driver.execute_script("window.scrollBy(0,4000);")
                    sleep(4)
                except:
                    break

            for i in range(2):
                try:
                    boton = driver.find_element_by_class_name('eva-3-btn-ghost.-lg')
                    boton.click()
                    sleep(4)
                except:
                    break

            vuelos = driver.find_elements_by_class_name('eva-3-cluster-basic.-eva-3-shadow-line-hover')

            listprecio = list()

            for vuelo in vuelos:
                precio = vuelo.find_element_by_class_name('amount.price-amount').text
                listprecio.append(precio)
                listprecio.append(precio)
                # print(precio)
            print("Precio de los vuelos:")
            print(listprecio)

            listida = list()
            for vuelo in vuelos:
                ida = vuelo.find_elements_by_class_name('city-departure.route-info-item.route-info-item-city-departure')
                for i in ida:
                    listida.append(i.text)

            listreg = list()

            for vuelo in vuelos:
                reg = vuelo.find_elements_by_class_name('city-arrival.route-info-item.route-info-item-city-arrival')
                for i in reg:
                    listreg.append(i.text)
                # print(reg)

            listhoras = list()

            for vuelo in vuelos:
                Firsthora = vuelo.find_elements_by_class_name('itinerary-wrapper.-selected')
                for x in Firsthora:
                    hora = x.find_elements_by_class_name('hour')
                    for i in hora:
                        listhoras.append(i.text)

            x = len(listhoras)

            horaida = listhoras[0::2]
            horareg = listhoras[1::2]
            print("Horas de ida")
            print(horaida)
            print("Horas de regreso")
            print(horareg)

            listidavuelta = zip(listida, horaida, horareg, listreg, listprecio)
            listidavuelta = tuple(listidavuelta)
            print(len(listidavuelta))
            tam = len(listidavuelta)
            tam = tam / 2
            print("Ciudad origen - Hora de salida- Hora de regreso - Ciudad destino")
            print(listidavuelta)

            update.message.reply_text("Boletos disponibles de compra:")
            numeracion = 1
            aux = 0
            for i in range(int(tam)):
                update.message.reply_text('\n' + str(numeracion) + '.\n- Fecha de salida: ' + str(Fsal) +
                                          ' \n- Ciudad de partida: ' + str(listidavuelta[aux][0]) +
                                          ' \n- Hora salida: ' + str(listidavuelta[aux][1]) +
                                          ' \n- Destino: ' + str(listidavuelta[aux][3]) +
                                          ' \n- Hora llegada: ' + str(listidavuelta[aux][2]) +
                                          ' \n---------------------------------------------'
                                          ' \n- Fecha de regreso: ' + str(Fret) +
                                          ' \n- Ciudad de partida: ' + str(listidavuelta[aux + 1][0]) +
                                          ' \n- Hora salida: ' + str(listidavuelta[aux + 1][1]) +
                                          ' \n- Destino: ' + str(listidavuelta[aux + 1][3]) +
                                          ' \n- Hora llegada: ' + str(listidavuelta[aux + 1][2]) +
                                          ' \n---------------------------------------------'
                                          ' \n- Numero de asientos: ' + str(Nasientos) +
                                          ' \n- Precio: ' + str(listidavuelta[aux + 1][4]))
                aux = aux + 2
                numeracion = numeracion + 1
            # -------------------------------------------------
            busqueda = 0
            update.message.reply_text('Busqueda finalizada!')
        except:
            busqueda = 0
            "Error en la busqueda"

#comando b_ticket
def BUY_TICKET_command(update, context):
    busqueda = 1
    if not context.args:
        busqueda = 0
        update.message.reply_text('Introduzca los parametros adecuados\n'
                                  'Ejemplo: "/BUY_TICKET GYE AMS 2021-05-29 3"\n'
                                  'Para mas información use /help')
    while busqueda == 1:
        try:
            update.message.reply_text('La busqueda de vuelos esta en proceso.\n'
                                      'Este proceso puede tardar unos segundos'
                                      ' debido a que las busquedas se realizan en tiempo'
                                      ' real.\n'
                                      'En cuanto se acabe de realizar el listado'
                                      ' se le notificara con un mensaje.\n'
                                      'Porfavor sea paciente')
            origen = ''
            destino = ''
            Fsal = ''
            Nasientos = ''
            try:
                origen = context.args[0]
                destino = context.args[1]
                Fsal = context.args[2]
                Nasientos = context.args[3]
            except:
                update.message.reply_text('Error en los datos de busqueda')

            # -------------------------------------------------

            driver = webdriver.Chrome('./chromedriver.exe')

            driver.get(
                f'https://www.despegar.com.ec/shop/flights/results/oneway/{origen}/{destino}/{Fsal}/{Nasientos}/0/0/NA/NA/NA/NA?from=SB&di={Nasientos}-0')

            sleep(5)

            for i in range(3):
                try:
                    driver.execute_script("window.scrollBy(0,4000);")
                    sleep(4)
                except:
                    break

            for i in range(2):
                try:
                    boton = driver.find_element_by_class_name('eva-3-btn-ghost.-lg')
                    boton.click()
                    sleep(4)
                except:
                    break

            vuelos = driver.find_elements_by_class_name('eva-3-cluster-basic.-eva-3-shadow-line-hover')

            listprecio = list()

            for vuelo in vuelos:
                precio = vuelo.find_element_by_class_name('amount.price-amount').text
                listprecio.append(precio)
                # listprecio.append(precio)

            # print("Precio de los vuelos:")
            # print(listprecio)

            listida = list()

            for vuelo in vuelos:
                ida = vuelo.find_elements_by_class_name('city-departure.route-info-item.route-info-item-city-departure')
                for i in ida:
                    listida.append(i.text)

            listreg = list()

            for vuelo in vuelos:
                reg = vuelo.find_elements_by_class_name('city-arrival.route-info-item.route-info-item-city-arrival')
                for i in reg:
                    listreg.append(i.text)
                # print(reg)

            listhoras = list()

            for vuelo in vuelos:
                Firsthora = vuelo.find_elements_by_class_name('itinerary-wrapper.-selected')
                for x in Firsthora:
                    hora = x.find_elements_by_class_name('hour')
                    for i in hora:
                        listhoras.append(i.text)

            horaida = listhoras[0::2]
            horareg = listhoras[1::2]
            # print("Horas de ida")
            # print(horaida)
            # print("Horas de regreso")
            # print(horareg)

            listhida = list()
            listhreg = list()

            listidavuelta = zip(listida, horaida, horareg, listreg, listprecio)
            listidavuelta = tuple(listidavuelta)
            print("Ciudad origen - Hora de salida- Hora de regreso - Ciudad destino")
            print(len(listidavuelta))
            tam = len(listidavuelta)
            print("Ciudad origen - Hora de salida- Hora de regreso - Ciudad destino")
            print(listidavuelta)

            update.message.reply_text("Boletos disponibles de compra:")
            numeracion = 1
            aux = 0
            for i in range(int(tam)):
                update.message.reply_text('\n' + str(numeracion) + '. Fecha de salida: ' + str(Fsal) +
                                          ' \n- Ciudad de partida: ' + str(listidavuelta[aux][0]) +
                                          ' \n- Hora salida: ' + str(listidavuelta[aux][1]) +
                                          ' \n- Destino: ' + str(listidavuelta[aux][3]) +
                                          ' \n- Hora llegada: ' + str(listidavuelta[aux][2]) +
                                          ' \n- Numero de asientos: ' + str(Nasientos) +
                                          ' \n- Precio: ' + str(listidavuelta[aux][4]))
                aux = aux + 1
                numeracion = numeracion + 1
            # -------------------------------------------------
            busqueda = 0
            update.message.reply_text('Busqueda finalizada!')
        except:
            "Error en la busqueda"
            busqueda = 0

#comando searchD
def SearchD_command(update, context):
    update.message.reply_text('Aun no configurado')

#comando searchO
def SearchO_command(update, context):
    update.message.reply_text('Aun no configurado')

#echo
def echo(update, context):
    update.message.reply_text('No se ha logrado reconocer su mensaje.\n'
                              'Para mas información use /help')

#main
def main():
    """Start the bot."""
    # Enlazar updater con el bot.
    updater = Updater(TOKEN)

    # Cear despachadores
    dispatcher = updater.dispatcher

    # Comandos
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("LIST", list_command))
    dispatcher.add_handler(CommandHandler("SEARCHD", SearchD_command))
    dispatcher.add_handler(CommandHandler("SEARCHO", SearchO_command))
    dispatcher.add_handler(CommandHandler("BUYRT_TICKET", BUYRT_TICKET_command))
    dispatcher.add_handler(CommandHandler("BUY_TICKET", BUY_TICKET_command))

    # Mensaje random
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Iniciat bot
    updater.start_polling()

    # FInalizar bot con Ctrl+C
    updater.idle()

#Donde se ejecuta el main
if __name__ == '__main__':
    main()
