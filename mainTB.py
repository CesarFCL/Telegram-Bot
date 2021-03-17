#Instalación de Librerias de Telegram-Bot y Selenium-Scrapping
import logging
from time import sleep
from selenium import webdriver
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import sys

driver = webdriver.Chrome('./chromedriver.exe')

# Configurar loggin
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

#logging del usuario
logger = logging.getLogger()

#Comando start (mensaje al iniciar el bot)
def start(update, context):
    print(update)
    nombre=update.effective_user['first_name']
    update.message.reply_text(f'Hola {nombre} este es un bot con fines academicos.\n '
                              'A partir de este bot puedes buscar vuelos disponibles ' 
                              'y ver la disponibilidad de reservar vuelos.\n'
                              'Toda información, busqueda y resultados son obtenidos de despegar.com.ec\n'
                              'Ingrese el comando /help para mayor información y ver los comandos disponibles')

#Comando help_command (listado de comandos)
def help_command(update, context):
    update.message.reply_text('Los comandos disponibles son:\n\n'
                              '1. /start -> Iniciar bot\n\n'
                              '2. /help -> Listado de comandos\n\n'
                              '3. /LIST -> Listado de vuelos disponibles\n\n'
                              '4. /SEARCHD [IATA code] -> Mostrar todos los vuelos disponibles a ese destino\n\n'
                              '5. /SEARCHO [IATA code] -> Mostrar todos los vuelos disponibles desde ese origen\n\n'
                              '6. /BUY_TICKET [Parameters] -> Mostrar todos los tickets/vuelos de solo ida disponibles de compra a partir de sus especificaciones\n'
                              '*El comando /BUY_TICKET usa el formato presentado en /formatB*\n\n'
                              '7. /BUYRT_TICKET [Parameters] -> Mostrar todos los tickets/vuelos ida y vuelta disponibles de compra a partir de sus especificaciones\n'
                              '*El comando /BUY_TICKET usa el formato presentado en /formatBRT*')

#Comando formatB (formato para ingresar el comando BUY_TICKET)
def formatB(update, context):
    update.message.reply_text('El formato para usar el comando /BUY_TICKET es el siguiente:\n'
                              '1. Ingresar el comando /BUY_TICKET\n'
                              '2. Al lado del comando colocar el código IATA de del aeropuerto de origen y del aeropuerto de destino\n'
                              '3. Al lado del codigo IATA se ingresaran la fecha de salida [Ejemplo fecha: 2000-01-20]\n'
                              '4. Por ultimo poner el numero de asientos\n'
                              'Ejemplo: "/BUY_TICKET GYE AMS 2021-05-29 3"')

#Comando formatBRT (formato para ingresar el comando BUYRT_TICKET)
def formatBRT(update, context):
    update.message.reply_text('El formato para usar el comando /BUYRT_TICKET es el siguiente:\n'
                              '1. Ingresar el comando /BUYRT_TICKET\n'
                              '2. Al lado del comando colocar el código IATA de del aeropuerto de origen y del aeropuerto de destino\n'
                              '3. Al lado del codigo IATA se ingresaran las fechas de salida y de retorno [Ejemplo fecha: 2000-01-20]\n'
                              '4. Por ultimo poner el numero de asientos\n'
                              'Ejemplo: "/BUYRT_TICKET GYE AMS 2021-05-29 2021-06-16 3"')

#Comando list_command (lista de vuelos)
def list_command(update, context):
    #Lista de aeropuertos que se tomaran en cuenta
    CPaises = ['GYE', 'UIO','GRU', 'BOG', 'SCL', 'LIM', 'CGH', 'GIG', 'AEP', 'MEX', 'LAX', 'JFK','DUB', 'FRA', 'HKG',
               'YYZ', 'MIA', 'MAD', 'BCN', 'SJO', 'PTY', 'BAQ', 'MVD', 'BQN','HND', 'AMS','ORY','SYD']
    #Copia de la lista para hacer una busqueda bidimensional
    CPaises2=CPaises
    #Msg previo al inicio de la busqueda
    update.message.reply_text('La busqueda de vuelos esta en proceso.\n'
                              'Este proceso puede tardar unos segundos'
                              ' debido a que las busquedas se realizan en tiempo'
                              ' real.\n'
                              'En cuanto se acabe de realizar el listado'
                              ' se le notificara con un mensaje.\n'
                              'Porfavor sea paciente')
    #Inicio de la busqueda(scrapping) aeropuerto por aeropuerto
    for j in CPaises:
        for k in CPaises2:
            #URL donde se hace el scrapping
            driver.get(f'https://www.despegar.com.ec/vuelos/{j}/{k}/')
            #Scrapping de las clases donde se encuentran los datos de los vuelos
            vuelos = driver.find_elements_by_class_name('reduced-cluster.margin-bottom-reduced-cluster')

            #Scrapping de clase info-vuelo
            info = driver.find_element_by_class_name('ux-common-results-title').text

            #lista donde se guardan los precios
            listprecio = list()
            #Scrapping de los precios de los vuelos
            for vuelo in vuelos:
                precio = vuelo.find_element_by_class_name('pricebox-big-text.price').text
                listprecio.append(precio)

            #lista donde se guardaran los vuelos de ida
            listida = list()
            #Scrapping de los vuelos de ida
            for vuelo in vuelos:
                ida = vuelo.find_elements_by_class_name('cluster-part-0')
                for i in ida:
                    listida.append(i.text)

            #lista donde se guardaran los vuelos de regreso
            listreg = list()
            #Scrapping de los vuelos de regreso
            for vuelo in vuelos:
                reg = vuelo.find_elements_by_class_name('cluster-part-1')
                for i in reg:
                    listreg.append(i.text)
                # print(reg)

            '''
            Eliminar espacios en blanco y guiones en los datos guardados
            en las listas de vuelosa de ida y vuelos de regreso para darle 
            formato al texto que posteriormente se imprimira
            '''
            aux = 0
            for i in listida:
                listida[aux] = i.replace("\n-", " - ").replace("\n", " - ").replace("  ", " ").replace("- -", "-")
                aux = aux + 1

            aux = 0
            for i in listreg:
                listreg[aux] = i.replace("\n-", " - ").replace("\n", " - ").replace("  ", " ").replace("- -", "-")
                aux = aux + 1

            #union de las listas de vuelos de ida y vuelos de regreso
            listidavuelta = zip(listida, listreg, listprecio)
            listidavuelta = tuple(listidavuelta)

            #print info-vuelo para saber por que busuqeda de vuelo se encuentra el usuario
            print(info)

            #Se envian msg al usuario por cada vuelo encontrado con todos los datos del vuelo
            numeracion = 1
            for i in range(len(listidavuelta)):
                update.message.reply_text(str(numeracion) + '\n' +
                                          str(info) + '\n' +
                                          str(listidavuelta[i][0]) + '\n' +
                                          str(listidavuelta[i][1]) + '\n' +
                                          'Precio: ' + str(listidavuelta[i][2]) + ' $\n')
                numeracion = numeracion + 1
    #Se envia msg al usuario notificando de la finalización del proceso de busqueda
    update.message.reply_text('Listado de vuelos finalizado!')

def buttons(update, context):
    logger.info('Update: "%s"\nContext: "%s"', update, context.error)

    query = update.callback_query
    query.answer(text='Reservaste el vuelo '+str(query.data)+'!', show_alert=True)

#comando BUYRT_TICKET (comprar ticket de ida y vuelta)
def BUYRT_TICKET_command(update, context):
    #parametro de busqueda pre-establecido en 1
    busqueda=1
    '''
    si el usuario no ha ingresado el comando con los parametros adecuados busqueda=0
    para que no inicie la busqueda, posteriormente se envia un mensaje para que el usuario
    pueda volver a introducir el comando de manera correcta
    '''
    if not context.args:
        busqueda=0
        update.message.reply_text('Introduzca los parametros adecuados\n'
                                  'Ejemplo: "/BUYRT_TICKET GYE AMS 2021-05-29 2021-06-16 3"\n'
                                  'Para mas información use /help')

    #Si el usuario ha introducido el comando con los parametros adecuados se intenta realizar el scrapping
    while busqueda==1:
        try:
            #Mensaje pre-busqueda
            update.message.reply_text('La busqueda de vuelos esta en proceso.\n'
                                      'Este proceso puede tardar unos segundos'
                                      ' debido a que las busquedas se realizan en tiempo'
                                      ' real.\n'
                                      'En cuanto se acabe de realizar el listado'
                                      ' se le notificara con un mensaje.\n'
                                      'Porfavor sea paciente')
            
            #variables donde se guardaran los vuelos de origen, destino, Fechas de salida y retorno y num-asientos
            origen = ''
            destino = ''
            Fsal = ''
            Fret = ''
            Nasientos = ''
            #Se intenta almacenar los parametros especificados por el usuario
            try:
                origen= context.args[0]
                destino= context.args[1]
                Fsal= context.args[2]
                Fret= context.args[3]
                Nasientos= context.args[4]
            #En caso de que no se puedan almacenar por algun error se presenta un msg de error
            except:
                update.message.reply_text('Error en los datos de busqueda')

            #URL donde se realiza el scrapping
            driver.get(f'https://www.despegar.com.ec/shop/flights/results/roundtrip/{origen}/{destino}/{Fsal}/{Fret}/{Nasientos}/0/0/NA/NA/NA/NA/NA?from=SB&di={Nasientos}-0')
            #Se espera 5seg para que se cargue adecuadamente la pagina
            sleep(5)

            #Se realiza un scroll de la pagina para que cargue en su totalidad
            for i in range(3):
                try:
                    driver.execute_script("window.scrollBy(0,4000);")
                    sleep(4)
                except:
                    break
            '''
            En caso de haber botones que extiendan el contenido se pulsaran
            automaticamente para cargar mas contenido.
            '''
            for i in range(2):
                try:
                    boton = driver.find_element_by_class_name('eva-3-btn-ghost.-lg')
                    boton.click()
                    sleep(4)
                except:
                    break

            #Scrapping de las clases donde se encuentran los datos de los vuelos
            vuelos = driver.find_elements_by_class_name('eva-3-cluster-basic.-eva-3-shadow-line-hover')

            #Lista donde se guardaran los precios de los vuelos
            listprecio = list()
            #Scrapping de los precios de los vuelos
            for vuelo in vuelos:
                precio = vuelo.find_element_by_class_name('amount.price-amount').text
                #Doble append para que el tamaño de la lista coincida con los vuelos de ida-retorno 
                listprecio.append(precio)
                listprecio.append(precio)

            #Lista donde se guardaran los vuelos de ida
            listida = list()
            #Scrapping de los vuelos de ida
            for vuelo in vuelos:
                ida = vuelo.find_elements_by_class_name('city-departure.route-info-item.route-info-item-city-departure')
                for i in ida:
                    listida.append(i.text)

            #Lista donde se guardaran los vuelos de regreso/retorno
            listreg = list()
            #Scrapping de los vuelos de regreso
            for vuelo in vuelos:
                reg = vuelo.find_elements_by_class_name('city-arrival.route-info-item.route-info-item-city-arrival')
                for i in reg:
                    listreg.append(i.text)

            #Lista donde se gusradran las horas de ida-vuelta
            listhoras = list()
            #Scrapping de los horas de ida-vuelta 
            for vuelo in vuelos:
                Firsthora = vuelo.find_elements_by_class_name('itinerary-wrapper.-selected')
                for x in Firsthora:
                    hora = x.find_elements_by_class_name('hour')
                    for i in hora:
                        listhoras.append(i.text)

            #Se divide la lista de horas en hora-ida y hora-retorno
            horaida = listhoras[0::2]
            horareg = listhoras[1::2]

            #Union de las listas de vuelos de ida-regreso, hora-ida-regreso y precio
            listidavuelta = zip(listida, horaida, horareg, listreg, listprecio)
            listidavuelta = tuple(listidavuelta)
            
            '''
            Variable tam donde se guarda el tamaño de la lista con todos los datos de vuelo para
            posteriormente usarla como parametro para hacer un bucle de salida de mensajes.
            Se divide en 2 porque se contara un vuelo de ida-vuelta como un solo mensaje de salida
            '''
            tam= len(listidavuelta)
            tam= tam/2

            #msg posterior a la presentacion de boletos disponibles de compra
            update.message.reply_text("Boletos disponibles de compra:")

            #variable numeracion que numera los mensajes
            numeracion=1
            #variable aux que hace la funcion de puntero en la lista con todos los datos de vuelo
            aux=0
            #Se envian los mensaje presentando los boletos disponibles de compra con todos los datos
            for i in range(int(tam)):
                update.message.reply_text('\n'+str(numeracion)+'.\n- Fecha de salida: '+ str(Fsal)+
                                          ' \n- Ciudad de partida: '+ str(listidavuelta[aux][0])+
                                          ' \n- Hora salida: '+ str(listidavuelta[aux][1])+
                                          ' \n- Destino: '+ str(listidavuelta[aux][3])+
                                          ' \n- Hora llegada: '+ str(listidavuelta[aux][2])+
                                          ' \n---------------------------------------------'
                                          ' \n- Fecha de regreso: '+ str(Fret)+
                                          ' \n- Ciudad de partida: '+ str(listidavuelta[aux+1][0])+
                                          ' \n- Hora salida: '+ str(listidavuelta[aux+1][1])+
                                          ' \n- Destino: '+ str(listidavuelta[aux+1][3])+
                                          ' \n- Hora llegada: '+str(listidavuelta[aux+1][2])+
                                          ' \n---------------------------------------------'
                                          ' \n- Numero de asientos: ' + str(Nasientos) +
                                          ' \n- Precio: $ '+str(listidavuelta[aux+1][4]))
                aux=aux + 2
                numeracion=numeracion+1
            
            #Variable busqueda=0 para que no se vuelva a realizar la busqueda
            busqueda=0
            #Escojer vuelo a reservar
            button_list = []
            button_list2 = []
            button_list3 = []
            button_list4 = []
            reply_markup = ''
            if tam <= 8:
                for each in range(int(tam)):
                    button_list.append(InlineKeyboardButton(str(each + 1), callback_data=str(each + 1)))
                reply_markup = InlineKeyboardMarkup([button_list])
            if tam > 8 and tam <= 16:
                for each in range(8):
                    button_list.append(InlineKeyboardButton(str(each + 1), callback_data=str(each + 1)))
                for each in range(int(tam) - 8):
                    button_list2.append(InlineKeyboardButton(str(each + 9), callback_data=str(each + 9)))
                reply_markup = InlineKeyboardMarkup([
                    button_list,
                    button_list2
                ])
            if tam > 16 and tam <=24:
                for each in range(8):
                    button_list.append(InlineKeyboardButton(str(each + 1), callback_data=str(each + 1)))
                    button_list2.append(InlineKeyboardButton(str(each + 9), callback_data=str(each + 9)))
                for each in range(int(tam) - 16):
                    button_list3.append(InlineKeyboardButton(str(each + 17), callback_data=str(each + 17)))
                reply_markup = InlineKeyboardMarkup([
                    button_list,
                    button_list2,
                    button_list3
                ])
            if tam > 24:
                for each in range(8):
                    button_list.append(InlineKeyboardButton(str(each + 1), callback_data=str(each + 1)))
                    button_list2.append(InlineKeyboardButton(str(each + 9), callback_data=str(each + 9)))
                    button_list3.append(InlineKeyboardButton(str(each + 17), callback_data=str(each + 17)))
                for each in range(int(tam) - 24):
                    button_list4.append(InlineKeyboardButton(str(each + 25), callback_data=str(each + 25)))
                reply_markup = InlineKeyboardMarkup([
                    button_list,
                    button_list2,
                    button_list3,
                    button_list4
                ])
            

            update.message.reply_text(
                text='Escoja el vuelo que desea reservar:',
                reply_markup=reply_markup
            )
        #Si el scrapping ha tenido algun error se emite un mensaje de error
        except:
            busqueda=0
            update.message.reply_text('Error en la busqueda')

#comando BUY_TICKET (comprar ticket de solo ida)
def BUY_TICKET_command(update, context):
    #parametro de busqueda pre-establecido en 1
    busqueda = 1
    '''
    si el usuario no ha ingresado el comando con los parametros adecuados busqueda=0
    para que no inicie la busqueda, posteriormente se envia un mensaje para que el usuario
    pueda volver a introducir el comando de manera correcta
    '''
    if not context.args:
        busqueda = 0
        update.message.reply_text('Introduzca los parametros adecuados\n'
                                  'Ejemplo: "/BUY_TICKET GYE AMS 2021-05-29 3"\n'
                                  'Para mas información use /help')
    
    # Si el usuario ha introducido el comando con los parametros adecuados se intenta realizar el scrapping
    while busqueda ==1:
        try:
            # Mensaje pre-busqueda
            update.message.reply_text('La busqueda de vuelos esta en proceso.\n'
                                      'Este proceso puede tardar unos segundos'
                                      ' debido a que las busquedas se realizan en tiempo'
                                      ' real.\n'
                                      'En cuanto se acabe de realizar el listado'
                                      ' se le notificara con un mensaje.\n'
                                      'Porfavor sea paciente')
            
            # variables donde se guardaran los vuelos de origen, destino, Fechas de salida y retorno y num-asientos
            origen = ''
            destino = ''
            Fsal = ''
            Nasientos = ''
            # Se intenta almacenar los parametros especificados por el usuario
            try:
                origen= context.args[0]
                destino= context.args[1]
                Fsal= context.args[2]
                Nasientos= context.args[3]
            # En caso de que no se puedan almacenar por algun error se presenta un msg de error
            except:
                update.message.reply_text('Error en los datos de busqueda')

            # URL donde se realiza el scrapping
            driver.get(f'https://www.despegar.com.ec/shop/flights/results/oneway/{origen}/{destino}/{Fsal}/{Nasientos}/0/0/NA/NA/NA/NA?from=SB&di={Nasientos}-0')
            # Se espera 5seg para que se cargue adecuadamente la pagina
            sleep(5)
            #Se realiza un scroll de la pagina para que cargue en su totalidad
            for i in range(3):
                try:
                    driver.execute_script("window.scrollBy(0,4000);")
                    sleep(4)
                except:
                    break
            '''
            En caso de haber botones que extiendan el contenido se pulsaran
            automaticamente para cargar mas contenido.
            '''
            for i in range(2):
                try:
                    boton = driver.find_element_by_class_name('eva-3-btn-ghost.-lg')
                    boton.click()
                    sleep(4)
                except:
                    break

            # Scrapping de las clases donde se encuentran los datos de los vuelos
            vuelos = driver.find_elements_by_class_name('eva-3-cluster-basic.-eva-3-shadow-line-hover')

            # Lista donde se guardaran los precios de los vuelos
            listprecio = list()
            # Scrapping de los precios de los vuelos
            for vuelo in vuelos:
                precio = vuelo.find_element_by_class_name('amount.price-amount').text
                listprecio.append(precio)

            # Lista donde se guardaran los vuelos de ida
            listida = list()
            # Scrapping de los vuelos de ida
            for vuelo in vuelos:
                ida = vuelo.find_elements_by_class_name('city-departure.route-info-item.route-info-item-city-departure')
                for i in ida:
                    listida.append(i.text)

            # Lista donde se guardara la ciudad de llegada
            listarriv = list()
            # Scrapping de ciudad de llegada
            for vuelo in vuelos:
                llegada = vuelo.find_elements_by_class_name('city-arrival.route-info-item.route-info-item-city-arrival')
                for i in llegada:
                    listarriv.append(i.text)

            # Lista donde se gusradran las horas de salida-llegada
            listhoras = list()
            # Scrapping de los horas de salida-llegada
            for vuelo in vuelos:
                Firsthora = vuelo.find_elements_by_class_name('itinerary-wrapper.-selected')
                for x in Firsthora:
                    hora = x.find_elements_by_class_name('hour')
                    for i in hora:
                        listhoras.append(i.text)

            # Se divide la lista de horas en hora-ida y hora-llegada
            horaida = listhoras[0::2]
            horaarriv = listhoras[1::2]

            # Union de las listas de vuelos de ida-regreso, hora-ida-regreso y precio
            listidavuelta = zip(listida, horaida, horaarriv, listarriv, listprecio)
            listidavuelta= tuple(listidavuelta)

            '''
            Variable tam donde se guarda el tamaño de la lista con todos los datos de vuelo para
            posteriormente usarla como parametro para hacer un bucle de salida de mensajes.
            '''
            tam= len(listidavuelta)

            # msg posterior a la presentacion de boletos disponibles de compra
            update.message.reply_text("Boletos disponibles de compra:")
            # variable numeracion que numera los mensajes
            numeracion=1
            # variable aux que hace la funcion de puntero en la lista con todos los datos de vuelo
            aux=0
            # Se envian los mensaje presentando los boletos disponibles de compra con todos los datos
            for i in range(int(tam)):
                update.message.reply_text('\n'+str(numeracion)+'. Fecha de salida: '+ str(Fsal)+
                                          ' \n- Ciudad de partida: '+ str(listidavuelta[aux][0])+
                                          ' \n- Hora salida: '+ str(listidavuelta[aux][1])+
                                          ' \n- Destino: '+ str(listidavuelta[aux][3])+
                                          ' \n- Hora llegada: '+ str(listidavuelta[aux][2])+
                                          ' \n- Numero de asientos: ' + str(Nasientos) +
                                          ' \n- Precio: $ '+str(listidavuelta[aux][4]))
                aux=aux + 1
                numeracion=numeracion+1
            
            # Variable busqueda=0 para que no se vuelva a realizar la busqueda
            busqueda=0
            # Escojer vuelo a reservar
            button_list = []
            button_list2 = []
            button_list3 = []
            button_list4 = []
            reply_markup = ''
            if tam <=8:
                for each in range(tam):
                    button_list.append(InlineKeyboardButton(str(each+1), callback_data=str(each+1)))
                reply_markup = InlineKeyboardMarkup([button_list])
            if tam > 8 and tam <= 16:
                for each in range(8):
                    button_list.append(InlineKeyboardButton(str(each+1), callback_data=str(each+1)))
                for each in range(tam-8):
                    button_list2.append(InlineKeyboardButton(str(each + 9), callback_data=str(each + 9)))
                reply_markup = InlineKeyboardMarkup([
                    button_list,
                    button_list2
                ])
            if tam > 16 and tam <=24:
                for each in range(8):
                    button_list.append(InlineKeyboardButton(str(each + 1), callback_data=str(each + 1)))
                    button_list2.append(InlineKeyboardButton(str(each + 9), callback_data=str(each + 9)))
                for each in range(int(tam) - 16):
                    button_list3.append(InlineKeyboardButton(str(each + 17), callback_data=str(each + 17)))
                reply_markup = InlineKeyboardMarkup([
                    button_list,
                    button_list2,
                    button_list3
                ])
            if tam > 24:
                for each in range(8):
                    button_list.append(InlineKeyboardButton(str(each + 1), callback_data=str(each + 1)))
                    button_list2.append(InlineKeyboardButton(str(each + 9), callback_data=str(each + 9)))
                    button_list3.append(InlineKeyboardButton(str(each + 17), callback_data=str(each + 17)))
                for each in range(int(tam) - 24):
                    button_list4.append(InlineKeyboardButton(str(each + 25), callback_data=str(each + 25)))
                reply_markup = InlineKeyboardMarkup([
                    button_list,
                    button_list2,
                    button_list3,
                    button_list4
                ])

            update.message.reply_text(
                     text='Escoja el vuelo que desea reservar:',
                     reply_markup= reply_markup
                 )
            
        # Si el scrapping ha tenido algun error se emite un mensaje de error
        except:
            "Error en la busqueda"
            busqueda=0

#comando SearchD (Buscar vuelos hacia un destino en especifico)
def SearchD_command(update, context):
    #Lista de aeropuertos que se tomaran en cuenta
    CPaises = ['GYE', 'UIO','GRU', 'BOG', 'SCL', 'LIM', 'CGH', 'GIG', 'AEP', 'MEX', 'LAX', 'JFK','DUB', 'FRA', 'HKG',
               'YYZ', 'MIA', 'MAD', 'BCN', 'SJO', 'PTY', 'BAQ', 'MVD', 'BQN','HND', 'AMS','ORY','SYD']
    #parametro de busqueda pre-establecido en 1
    busqueda=1
    '''
    si el usuario no ha ingresado el comando con los parametros adecuados busqueda=0
    para que no inicie la busqueda, posteriormente se envia un mensaje para que el usuario
    pueda volver a introducir el comando de manera correcta
    '''
    if not context.args:
        busqueda = 0
        update.message.reply_text('Introduzca los parametros adecuados\n'
                                  'Ejemplo: "/SEARCHD GYE"\n'
                                  'Para mas información use /help')
    # Si el usuario ha introducido el comando con los parametros adecuados se intenta realizar el scrapping
    while busqueda == 1:
      try:
          # Mensaje pre-busqueda
          update.message.reply_text('La busqueda de vuelos esta en proceso.\n'
                                    'Este proceso puede tardar unos segundos'
                                    ' debido a que las busquedas se realizan en tiempo'
                                    ' real.\n'
                                    'En cuanto se acabe de realizar el listado'
                                    ' se le notificara con un mensaje.\n'
                                    'Porfavor sea paciente')
          
          # variables donde se guardara el detino
          detino = ''
          # Se intenta almacenar los parametros especificados por el usuario
          try:
              destino = str(context.args[0])
          # En caso de que no se puedan almacenar por algun error se presenta un msg de error
          except:
              update.message.reply_text('Error en los datos de busqueda')

          '''
          Si el detino especificado por el usuario se encuentra en la tabla de aeropuertos
          que se tomaran en cuenta para la busqueda se elimina dicho aeropuerto de la lista
          '''
          if any(destino in string for string in CPaises):
              CPaises.remove(destino)

          #Se realiza el scrapping aeropuerto por aeropuerto
          for i in CPaises:
              # URL donde se realiza el scrapping
              driver.get(f'https://www.despegar.com.ec/vuelos/{i}/{destino}/')

              # Scrapping de las clases donde se encuentran los datos de los vuelos
              vuelos = driver.find_elements_by_class_name('reduced-cluster.margin-bottom-reduced-cluster')
              
              # Scrapping de las clase donde se encuentra la informacion del vuelo
              info = driver.find_element_by_class_name('ux-common-results-title').text

              # Lista donde se guardaran los precios de los vuelos
              listprecio = list()
              # Scrapping de los precios de los vuelos
              for vuelo in vuelos:
                  precio = vuelo.find_element_by_class_name('pricebox-big-text.price').text
                  listprecio.append(precio)

              # Lista donde se guardaran los vuelos de dia
              listida = list()
              # Scrapping de los vuelos de ida
              for vuelo in vuelos:
                  ida = vuelo.find_elements_by_class_name('cluster-part-0')
                  for i in ida:
                      listida.append(i.text)

              # Lista donde se guardara el aeropuerto de llegada
              listarriv = list()
              # Scrapping de los aeropuertos de llegada
              for vuelo in vuelos:
                  llegada = vuelo.find_elements_by_class_name('cluster-part-1')
                  for i in llegada:
                      listarriv.append(i.text)

              #variable aux que realiza la función de puntero en la lista
              aux = 0
              #se eliminan giones, puntos y caracteres no deseados para una presentacion limpia
              for i in listida:
                  listida[aux] = i.replace("\n-", " - ").replace("\n", " - ").replace("  ", " ").replace("- -", "-")
                  aux = aux + 1

              aux = 0
              for i in listarriv:
                  listarriv[aux] = i.replace("\n-", " - ").replace("\n", " - ").replace("  ", " ").replace("- -", "-")
                  aux = aux + 1

              # Union de las listas de vuelos de ida-llegada y precio
              listidavuelta = zip(listida, listarriv, listprecio)
              listidavuelta = tuple(listidavuelta)

              #print info para saber que aeropuertos se encuentra escrapeando el usuario
              print(info)
              #variable que lleva una numeracion de los mensajes en funcion de los aeropuertos ida-llegada
              numeracion = 1
              # Se envian los mensaje presentando los vuelos disponibles de ida al destino especificado por el usuario
              for i in range(len(listidavuelta)):
                  update.message.reply_text(str(numeracion) + '\n' +
                                            str(info) + '\n' +
                                            str(listidavuelta[i][0]) + '\n' +
                                            str(listidavuelta[i][1]) + '\n' +
                                            'Precio: ' + str(listidavuelta[i][2]) + ' $\n')
                  numeracion = numeracion + 1

          # Variable busqueda=0 para que no se vuelva a realizar la busqueda
          busqueda=0
          # Msg de finalizacion de busqueda
          update.message.reply_text('Busqueda finalizada!')
      # Si el scrapping ha tenido algun error se emite un mensaje de error
      except:
          busqueda = 0
          update.message.reply_text('Error en la busqueda')

# comando SearchO (Buscar vuelos con un porigen especifico hacia diversos destinos)
def SearchO_command(update, context):
    # Lista de aeropuertos que se tomaran en cuenta
    CPaises = ['GYE', 'UIO','GRU', 'BOG', 'SCL', 'LIM', 'CGH', 'GIG', 'AEP', 'MEX', 'LAX', 'JFK','DUB', 'FRA', 'HKG',
               'YYZ', 'MIA', 'MAD', 'BCN', 'SJO', 'PTY', 'BAQ', 'MVD', 'BQN','HND', 'AMS','ORY','SYD']
    # parametro de busqueda pre-establecido en 1
    busqueda = 1
    '''
    si el usuario no ha ingresado el comando con los parametros adecuados busqueda=0
    para que no inicie la busqueda, posteriormente se envia un mensaje para que el usuario
    pueda volver a introducir el comando de manera correcta
    '''
    if not context.args:
        busqueda = 0
        update.message.reply_text('Introduzca los parametros adecuados\n'
                                  'Ejemplo: "/SEARCHO GYE"\n'
                                  'Para mas información use /help')

    # Si el usuario ha introducido el comando con los parametros adecuados se intenta realizar el scrapping
    while busqueda == 1:
      try:
          # Mensaje pre-busqueda
          update.message.reply_text('La busqueda de vuelos esta en proceso.\n'
                                    'Este proceso puede tardar unos segundos'
                                    ' debido a que las busquedas se realizan en tiempo'
                                    ' real.\n'
                                    'En cuanto se acabe de realizar el listado'
                                    ' se le notificara con un mensaje.\n'
                                    'Porfavor sea paciente')
          # variables donde se guardara el origen
          origen = ''
          # Se intenta almacenar los parametros especificados por el usuario
          try:
              origen=str(context.args[0])
          # En caso de que no se puedan almacenar por algun error se presenta un msg de error
          except:
              update.message.reply_text('Error en los datos de busqueda')

          '''
            Si el origen especificado por el usuario se encuentra en la tabla de aeropuertos
            que se tomaran en cuenta para la busqueda se elimina dicho aeropuerto de la lista
          '''
          if any(origen in string for string in CPaises):
              CPaises.remove(origen)

          # Se realiza el scrapping aeropuerto por aeropuerto
          for i in CPaises:
              # URL donde se realiza el scrapping
              driver.get(f'https://www.despegar.com.ec/vuelos/{origen}/{i}/')

              # Scrapping de las clases donde se encuentran los datos de los vuelos
              vuelos = driver.find_elements_by_class_name('reduced-cluster.margin-bottom-reduced-cluster')

              # Scrapping de las clase donde se encuentra la informacion del vuelo
              info = driver.find_element_by_class_name('ux-common-results-title').text

              # Lista donde se guardaran los precios de los vuelos
              listprecio = list()
              # Scrapping de los precios de los vuelos
              for vuelo in vuelos:
                  precio = vuelo.find_element_by_class_name('pricebox-big-text.price').text
                  listprecio.append(precio)

              # Lista donde se guardaran los vuelos de dia
              listida = list()
              # Scrapping de los vuelos de ida
              for vuelo in vuelos:
                  ida = vuelo.find_elements_by_class_name('cluster-part-0')
                  for i in ida:
                      listida.append(i.text)

              # Lista donde se guardaran los datos de llegada
              listarriv = list()
              # Scrapping de los datos de llegada
              for vuelo in vuelos:
                  llegada = vuelo.find_elements_by_class_name('cluster-part-1')
                  for i in llegada:
                      listarriv.append(i.text)

              # variable aux que realiza la función de puntero en la lista
              aux = 0
              # se eliminan giones, puntos y caracteres no deseados para una presentacion limpia
              for i in listida:
                  listida[aux] = i.replace("\n-", " - ").replace("\n", " - ").replace("  ", " ").replace("- -", "-")
                  aux = aux + 1

              aux = 0
              for i in listarriv:
                  listarriv[aux] = i.replace("\n-", " - ").replace("\n", " - ").replace("  ", " ").replace("- -", "-")
                  aux = aux + 1

              # Union de las listas de vuelos de ida-llegada y precio
              listidavuelta = zip(listida, listarriv, listprecio)
              listidavuelta= tuple(listidavuelta)

              # print info para saber que aeropuertos se encuentra scrapeando el usuario
              print(info)
              # variable que lleva una numeracion de los mensajes en funcion de los aeropuertos ida-llegada
              numeracion = 1
              # Se envian los mensaje presentando los vuelos disponibles con el origen especificado por el usuario
              for i in range(len(listidavuelta)):
                  update.message.reply_text(str(numeracion)+'\n'+
                                            str(info)+'\n'+
                                            str(listidavuelta[i][0])+'\n'+
                                            str(listidavuelta[i][1])+'\n'+
                                            'Precio: '+str(listidavuelta[i][2])+' $\n')
                  numeracion=numeracion+1

          # Variable busqueda=0 para que no se vuelva a realizar la busqueda
          busqueda=0
          # Msg de finalizacion de busqueda
          update.message.reply_text('Busqueda finalizada!')
      # Si el scrapping ha tenido algun error se emite un mensaje de error
      except:
          busqueda=0
          update.message.reply_text('Error en la busqueda')

#Mensaje automatico cuando el mensaje del usuario no es ningun comando establecido
def echo(update, context):
    update.message.reply_text('No se ha logrado reconocer su mensaje.\n'
                              'Para mas información use /help')

def main():
    #Inicializar el Bot
    # Enlazar updater con el bot.
    updater = Updater("TOKEN")

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
    dispatcher.add_handler(CommandHandler("formatB", formatB))
    dispatcher.add_handler(CommandHandler("formatBRT", formatBRT))
    buttons_handler = CallbackQueryHandler(buttons)
    dispatcher.add_handler(buttons_handler)

    # Mensaje random
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start Bot
    updater.start_polling()

    updater.idle()

#Aquí se ejecuta el bot
if __name__ == '__main__':
    main()
