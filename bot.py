import threading
from helpers.common import log, log_save
import traceback
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.error import NetworkError, BadRequest


EMULATE_NETWORK_ERROR = False

class TelegramBOT(threading.Thread):
    def __init__(self, props=None):
        threading.Thread.__init__(self)
        self.token = props['token'] if 'token' in props and bool(props['token']) else None

        if not self.token:
            raise 'No telegram token provided'
        else:
            self.commands = [
                {
                    'command': 'start',
                    'description': 'Start the bot',
                    'handler': {'type': 'message', 'callback': self._start}
                },
                {
                    'command': 'help',
                    'description': 'Show available commands',
                    'handler': {'type': 'message', 'callback': self._help}
                },
            ]

            # Create the Updater and pass it your bot's token
            self.updater = Updater(token=self.token, use_context=True)
            # Get the dispatcher to register handlers
            self.dp = self.updater.dispatcher


            print(self.updater.bot)

            # Register the /start command
            for i in range(len(self.commands)):
                command = self.commands[i]['command']
                handler = self.commands[i]['handler']['callback']
                self.dp.add_handler(CommandHandler(command, handler))
            #
            # # Get a list of all chats your bot is a member of
            # updates = self.updater.bot.get_updates()
            # print('updates', updates)
            # # Iterate over each chat and send the message
            # for update in updates:
            #     chat_id = update.message.chat_id
            #     try:
            #         self.updater.bot.send_message(chat_id=chat_id, text='Done')
            #     except Exception:
            #         error = traceback.format_exc()
            #         log_save(error)

            # # Get a list of all chats your bot is a member of
            # chats = self.updater.bot.get_updates()
            # # Iterate over each chat and send the message
            # for chat_id in chats:
            #     chat_id = update.message.chat_id
            #     try:
            #         self.updater.bot.send_message(chat_id=chat_id, text='Done')
            #     except BadRequest:
            #         error = traceback.format_exc()
            #         log_save(error)

    def _all_commands(self):
        commands = list(map(lambda x: f"/{x['command']} - {x['description']}", self.commands))
        return '\n\n'.join(commands)

    def _start(self, update: Updater, context: CallbackContext) -> None:
        message = 'Hello! I am your bot. Here are some available commands:\n\n' + self._all_commands()
        update.message.reply_text(message)

    def _help(self, update: Updater, context: CallbackContext) -> None:
        message = self._all_commands()
        update.message.reply_text(message)

    def add(self, obj):
        self.commands.append(obj)
        command = obj['command']
        handler = obj['handler']

        def final_callback(*args, retry=True):
            global EMULATE_NETWORK_ERROR
            try:
                if EMULATE_NETWORK_ERROR:
                    EMULATE_NETWORK_ERROR = False
                    raise NetworkError("Emulated network error from Bot")
                log(f"Logging the command: {command}")

            except NetworkError as e:
                error = f"NetworkError: {e}"
                log(error)
                log_save(error)
                if retry:
                    final_callback(*args, retry=False)
                    return

            log(f"Starting the command: {command}")
            handler(*args)

        self.dp.add_handler(CommandHandler(command, final_callback, run_async=True))

        # except Exception as e:
        #     error = traceback.format_exc()
        #     log_save(error)

        # def final_callback_new(*args, retry=True):
        #     global EMULATE_NETWORK_ERROR
        #     try:
        #         if EMULATE_NETWORK_ERROR:
        #             EMULATE_NETWORK_ERROR = False
        #             raise NetworkError("from bot.add")
        #
        #         log(f"Starting the command: {command}")
        #         handler(*args)
        #
        #     except NetworkError as e:
        #         error = f"NetworkError: {e}"
        #         log_save(error)
        #         if retry:
        #             final_callback_new(*args, retry=False)
        #             return
        #
        #     except Exception as e:
        #         error = traceback.format_exc()
        #         log_save(error)
        # self.dp.add_handler(CommandHandler(command, final_callback_new, run_async=True))

    def listen(self):
        # Start the Bot
        self.updater.start_polling()
        log('An App is waiting for some command')
        # Run the bot until you send a signal to stop (e.g., Ctrl+C)
        self.updater.idle()
        log('Idle is started')
