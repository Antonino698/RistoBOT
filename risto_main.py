"""
Main dell'applicazione
"""
from typing import Final
from warnings import filterwarnings
from telegram.warnings import PTBUserWarning
from src.lib.config import BOT_CONFIG
from src.lib.lib import CommandHandler, MessageHandler
from src.lib.lib import filters, CallbackQueryHandler, ConversationHandler
from src.lib.lib import Application

# #import command_functions
from src.start_command import start_command
from src.menu_command import menu_command
from src.eventi_command import eventi_command
from src.info_command import info_command
from src.prenota_command import prenota_start
from src.prenota_command import prenota_name
from src.prenota_command import prenota_phone
from src.prenota_command import prenota_reserved_seats
from src.prenota_command import prenota_day
from src.prenota_command import prenota_time_slot
from src.prenota_command import confirmation
from src.prenota_command import button_click
from src.le_mie_prenotazioni_command import le_mie_prenotazioni_command, edit_booking
from src.lib.lib import NAME, PHONE, RESERVED_SEATS
from src.lib.lib import DAY, TIME_SLOT, CONFIRMATION, BUTTON_HANDLER
filterwarnings(action="ignore", message=r".*CallbackQueryHandler",
               category=PTBUserWarning)

TOKEN: Final = BOT_CONFIG['__TOKEN']

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('prenota', prenota_start)],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, prenota_name)],
        PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, prenota_phone)],
        RESERVED_SEATS: [MessageHandler(filters.TEXT & ~filters.COMMAND, prenota_reserved_seats)],
        DAY: [MessageHandler(filters.TEXT & ~filters.COMMAND, prenota_day)],
        TIME_SLOT: [MessageHandler(filters.TEXT & ~filters.COMMAND, prenota_time_slot)],
        CONFIRMATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirmation)],
        BUTTON_HANDLER: [CallbackQueryHandler(button_click)],
    },
    fallbacks=[]
)


# Configurazione del bot con il ConversationHandler
# Inizializzazione dell'applicazione
app = Application.builder().token(TOKEN).build()
#updater = Updater(TOKEN, use_context=True)
print('🤙 EUREKA 🤙')
# Aggiunta del ConversationHandler



app.add_handler(CommandHandler("start", start_command))
app.add_handler(CommandHandler("le_mie_prenotazioni", le_mie_prenotazioni_command))
app.add_handler(CommandHandler("menu", menu_command))
app.add_handler(CommandHandler("eventi", eventi_command))
app.add_handler(CommandHandler("info", info_command))
app.add_handler(conv_handler)
app.add_handler(CallbackQueryHandler(edit_booking))


# Avvio dell'applicazione
app.run_polling()
