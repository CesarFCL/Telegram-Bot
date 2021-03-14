import logging
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
    update.message.reply_text('Aun no configurado')

#comando brt_ticket
def BUYRT_TICKET_command(update, context):
    update.message.reply_text('Aun no configurado')

#comando b_ticket
def BUY_TICKET_command(update, context):
    update.message.reply_text('Aun no configurado')

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