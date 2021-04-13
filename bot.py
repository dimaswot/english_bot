import telegram
from telegram.ext import Updater, ConversationHandler, CommandHandler, CallbackQueryHandler
import states
import menu.test
import menu.settings
import menu.statisctics
import menu.start


class TelBot:
    def __init__(self, token):
        self.updater = Updater(token)
        self.init_command()

    def update(self, request_j):
        update = telegram.Update.de_json(request_j, self.updater.bot)
        self.updater.dispatcher.process_update(update)


    def init_command(self):
        conv_hand = ConversationHandler(
            entry_points=[CommandHandler('start', menu.start.start),
                          CommandHandler('begin', menu.start.start)],
            states={
                states.BEGIN: [
                    CallbackQueryHandler(menu.start.menu, pattern=f'^{str(states.EXIT)}$'),
                    CallbackQueryHandler(menu.test.test_first, pattern=f'^{str(states.TEST)}$'),
                    CallbackQueryHandler(menu.settings.settings, pattern=f'^{str(states.SETTINGS)}$'),
                    CallbackQueryHandler(menu.statisctics.statistics, pattern=f'^{str(states.STATISTICS)}$'),
                ],
                states.TEST: [
                    CallbackQueryHandler(menu.start.menu, pattern=f'^{str(states.EXIT)}$'),
                    CallbackQueryHandler(menu.test.test, pattern=f'@_\w+')
                ],
                states.STATISTICS: [
                    CallbackQueryHandler(menu.start.menu, pattern=f'^{str(states.STATISTICS)}$')

                ],
                states.SETTINGS: [
                    CallbackQueryHandler(menu.start.menu, pattern=f'^{str(states.EXIT)}$'),
                    CallbackQueryHandler(menu.settings.theme, pattern=f'^{str(states.THEME)}$'),
                    CallbackQueryHandler(menu.settings.redact_kol_vo, pattern=f'^{str(states.REDACT_KOL_VO)}$'),
                    CallbackQueryHandler(menu.settings.test_count, pattern=f'^{str(states.STOP_SCHEDULLER)}$')
                ],
                states.THEME: [
                    CallbackQueryHandler(menu.settings.set_theme, pattern=f'\w+'),
                ],
                states.REDACT_KOL_VO: [
                    CallbackQueryHandler(menu.settings.set_kol_vo, pattern=f'\w+')
                ],
                states.STOP_SCHEDULLER:[
                    CallbackQueryHandler(menu.settings.set_test_count, pattern=f'\w+'),
                ]
            },
            fallbacks=[],
        )
        self.updater.dispatcher.add_handler(conv_hand)
