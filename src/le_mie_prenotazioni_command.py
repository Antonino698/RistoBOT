"""
View personal booking
Inseriti i disable per gestire la parte
del modulo logger nei try-catch except
"""
#pylint: disable=W0718
#pylint: disable=E1120
from src.lib.lib import db, datetime, BUTTON_HANDLER
from src.lib.lib import InlineKeyboardButton, InlineKeyboardMarkup
from src.lib.lib import Logger
from src.lib.mysql_class import mysql
from src.start_command import Update, CallbackContext, start_command
async def le_mie_prenotazioni_command(update: Update, context: CallbackContext) -> int:
    """
    View personal booking
    """
    user = update.message.from_user
    user_id=user.id
    # Connessione al database
    try:
        db.connect()
        messaggio = (
        "In questa sezione potrai visualizzare e/o cancellare le tue prenotazioni.\n"
        "Ecco l'elenco delle prenotazioni effettuate:\n"
        )
        await context.bot.send_message(chat_id=update.message.chat_id, text=messaggio)
        pren_query= ("SELECT t1.*,t2.time_slot as tms FROM prenotazioni t1 "
                     "join max_seats_time_slot t2 on t1.time_slot = t2.id "
                     "WHERE t1.id_user= %s")
        res = db.select_query(pren_query, (user_id,))
        keyboard = []
        lista_prenotazioni = []
        for item in res:

            context.user_data["id_prenotazione"]=item['id']
            context.user_data["id_user"]=item['id_user']
            context.user_data["name"]=item['name']
            context.user_data["phone"]=item['phone']
            context.user_data["reserved_seats"]=item['reserved_seats']
            context.user_data["date"]=item['day']
            context.user_data["time_slot"] =  item['tms']
            context.user_data["time_slot_id"] = item['time_slot']
            date_in_iso1 = datetime.strptime(
                str(context.user_data["date"]),'%Y-%m-%d'
            ).strftime('%d-%m-%Y')
            prenotazioni_message = (
                    f'ID_PRENOTAZIONE: {context.user_data["id_prenotazione"]}\n'
                    f'Nome: {context.user_data["name"]}\n'
                    f'Telefono: {context.user_data["phone"]}\n'
                    f'Posti prenotati: {context.user_data["reserved_seats"]}\n'
                    f'Giorno: {date_in_iso1}\n'
                    f'Ora: {context.user_data["time_slot"]}\n\n'
                )
            lista_prenotazioni.append(prenotazioni_message)

        keyboard = [[InlineKeyboardButton(
                f'Elimina prenotazione: {prenotazione["id"]}',
                        callback_data=f'deleteSinglePren@{prenotazione["id"]}'
                )] for prenotazione in res]

        delete_all_b = InlineKeyboardButton("Elimina tutte le prenotazioni",
                        callback_data=f"deleteAllByUser@{user_id}")
        back_b = InlineKeyboardButton("Torna a /start", callback_data="reset@-1")
        keyboard.append([delete_all_b])
        keyboard.append([back_b])
        reply_markup = InlineKeyboardMarkup(keyboard)

        for prenotazioni_message in lista_prenotazioni:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                        text=prenotazioni_message)

        # msg = "Bene, queste sono le tue prenotazioni!\nCosa vuoi fare adesso?"
        await update.message.reply_text(
            "Bene, queste sono le tue prenotazioni!\nCosa vuoi fare adesso?",
            reply_markup=reply_markup
        )
        return BUTTON_HANDLER
    finally:
        # Chiudi la connessione al database
        db.disconnect()


async def edit_booking(update, context):
    """
    edit personal booking
    """
    query= update.callback_query
    id_user = query.message.chat_id
    data = query.data
    # Assume che il campo 'data' abbia la forma 'valore1:valore2'
    #parts = data.split('@')

    if len( data.split('@')) == 2:
        valore1 =  data.split('@')[0]
        valore2 =  data.split('@')[1]
        # gestisce la risposta in base al 'valore1'
        if valore1 == 'deleteSinglePren':
            print('deleteSinglePren')

            try:
                db.connect()
                canc_pren_row = "DELETE FROM prenotazioni WHERE prenotazioni.id = %s"
                id_pren = [int(valore2)]
                db.execute_query(canc_pren_row, id_pren, multi=False)
            except mysql.connector.Error as conn_error:
                Logger.error(f"Errore di connessione al database: {str(conn_error)}")
                await update.callback_query.answer(
                    text="Si è verificato un errore di connessione al database."
                )
            except Exception as e:
                Logger.error(f"Errore generico: {str(e)}")
                await update.callback_query.answer(
                    text="Si è verificato un errore in deleteSinglePren."
                )
            finally:
                # Chiudi la connessione al database
                db.disconnect()
            # Rimuove le prenotazioni e i relativi pulsanti
            await context.bot.delete_message(chat_id=id_user, message_id=query.message.message_id)
            text= (f"La prenotazione numero {valore2} è stata annullata con successo!\n"
            "Ma ti rivedremo presto, vero?!😭\n\n"
            "Noi ti consigliamo di dare un'occhiata ai nostri STREPITOSI /eventi!! 😎\n"
            "Ti sta rivenendo voglia di prenotare, ehh?? 😏")
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


        if valore1 == 'deleteAllByUser':
            print('deleteAllByUser')
            try:
                db.connect()
                # selezione poi la spiego
                canc_all = "DELETE FROM prenotazioni WHERE prenotazioni.id_user = %s"
                id_usr = [str(valore2)]
                db.execute_query(canc_all, id_usr, multi=False)
            except Exception as e:
                Logger.error(str(e))
                await update.callback_query.answer(
                    text="Si è verificato un errore in deleteAllByUser"
                )
            finally:
                # Chiudi la connessione al database
                db.disconnect()
            # Rimuove le prenotazioni e i relativi pulsanti
            await context.bot.delete_message(
                chat_id=id_user, message_id=query.message.message_id
            )
            text=("😱OH NO! NEI NOSTRI SISTEMI SEMBRA TU"
                  "ABBIA CANCELLATO TUTTE LE TUE PRENOTAZIONI🙄..."
                  "MA NOI AVEVAMO GIA' APPARECCHIATO I TAVOLI!!!😧\n\n"
                  "Non preoccuparti, potrai sempre fare"
                  "una nuova prenotazione cliccando qui--> /prenota")
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=text
            )

        if valore1 == 'reset':
            # Puoi aggiungere qui la logica per reimpostare lo stato del tuo bot
            await start_command(update, context)

        await update.callback_query.answer(text="Operazione eseguita")
        #await update.message.reply_text("Operazione eseguita")
        return
    #else:
    await update.callback_query.answer("Formato non valido.")
