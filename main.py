import logging
import os
from re import U
from typing import Text
import qrcode


from telegram import *
from telegram.ext import Updater, dispatcher
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext import ConversationHandler, CommandHandler
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler


# Configurando el Loggin
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Estados de la Conversacion
INPUT_TEXT = 1

# Funciones para generar codigo QR
def generar_qr(text):
    file_name = text + ".jpg"
    
    img = qrcode.make(text)
    img.save(file_name)
    return file_name

def send_file(filename, chat: Chat):
    # Muestra la accion que se esta ejecutando
    chat.send_action(
        action=ChatAction.UPLOAD_PHOTO,
        timeout=None
    )
    # Envio la foto
    chat.send_photo(
        photo=open(filename, "rb")
    )

    os.unlink(filename)               # Elimino el archivo del servidor

# Funciones para los comandos
def start(update:Update, context: CallbackContext):
    name = update.effective_user.first_name
    logger.info(f"Usuario: {name} ha iniciado el Bot")
    update.message.reply_text("Ha iniciado en este Bot")

def to_qr(update: Update, context: CallbackContext):
    update.message.reply_text("Para generar el codigo QR envie el texto a convertir")
    return INPUT_TEXT

def input_text(update: Update, context: CallbackContext):
    
    text = update.message.text
    chat = update.message.chat
    
    file_name = generar_qr(text)       # Funcion que genera el codigo
    send_file(file_name, chat)         # Funcion que envia el codigo
    
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext):
    name = update.effective_user.first_name
    logger.info(f"Usuario: {name} ha cancelado la generacion del QR")
    update.message.reply_text('Ha cancelado la generacion de QR')
    return ConversationHandler.END

def main():
    # Obtengo el token
    TOKEN = os.getenv("TOKEN")
    print(TOKEN)
    
    # Creamos el UPDATER
    updater = Updater(TOKEN)
    
    # Creamos el DISPATCHER
    dispatcher = updater.dispatcher
    # Creamos Conversacion
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("to_qr", to_qr)],
        states={
            INPUT_TEXT:[MessageHandler(Filters.text & ~Filters.command, input_text)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    
    #Creamos los comandos
    dispatcher.add_handler(CommandHandler("start", start))
    # Agregamos la conversacion
    dispatcher.add_handler(conv_handler)
    
    # Ponemos el BOT a escuchar
    updater.start_polling()
    
    # Para poder cerrar la ejecucion con Ctrl+C
    updater.idle()


if __name__=="__main__":
    main()