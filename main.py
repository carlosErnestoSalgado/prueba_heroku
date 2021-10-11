import logging
import os

from telegram import *
from telegram.ext import Updater, dispatcher
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler

# Configurando el Loggin
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Funciones para los comandos
def start(update:Update, context: CallbackContext) -> None:
    name = update.effective_user.first_name
    logger.info(f"Usuario: {name} ha iniciado el Bot")
    update.message.reply_text("Ha iniciado en este Bot")




def main():
    # Obtengo el token
    TOKEN = os.getenv("TOKEN")
    print(TOKEN)
    
    # Creamos el UPDATER
    updater = Updater(TOKEN)
    
    # Creamos el DISPATCHER
    dispatcher = updater.dispatcher
    
    #Creamos los comandos
    dispatcher.add_handler(CommandHandler("start", start))
    
    # Ponemos el BOT a escuchar
    updater.start_polling()
    
    # Para poder cerrar la ejecucion con Ctrl+C
    updater.idle()


if __name__=="__main__":
    main()