import os
import pyautogui
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.error import NetworkError
from helpers.common import image_path
from PIL import Image
from io import BytesIO
from helpers.common import log, sleep
from datetime import datetime

MAX_RETRIES = 3
DELAY = 5
EMULATE_NETWORK_ERROR = False

class TelegramBOT:
    def __init__(self, props=None):
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
            # Register the /start command
            for i in range(len(self.commands)):
                command = self.commands[i]['command']
                handler = self.commands[i]['handler']['callback']
                self.dp.add_handler(CommandHandler(command, handler))

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
        callback = handler['callback']

        def final_callback(upd, ctx):
            global EMULATE_NETWORK_ERROR

            retries = 0
            while retries < MAX_RETRIES:
                try:

                    if EMULATE_NETWORK_ERROR:
                        EMULATE_NETWORK_ERROR = False
                        raise NetworkError("Emulated network error")

                    start_time = datetime.now()
                    res = callback(upd, ctx)
                    status = "Done" if bool(res) or res is None else "Error"
                    duration_str = f"Duration: {str(datetime.now() - start_time).split('.')[0]}"
                    message = f'{status}: {command} | {duration_str}'

                    if res and type(res) is str:
                        message += f'\n{res}'

                    upd.message.reply_text(message)

                    log("Message sent successfully!")
                    return  # Exit the function if message is sent successfully
                except NetworkError as e:
                    log(f"Network error occurred: {e}")
                    retries += 1
                    log(f"Retrying ({retries}/{MAX_RETRIES})...")
                    sleep(DELAY)  # Wait for a few seconds before retrying

            log("Max retries reached. Failed to send message.")


        self.dp.add_handler(CommandHandler(command, final_callback))

    def run(self):
        log('An App is waiting for some command')
        # Start the Bot
        self.updater.start_polling()
        # Run the bot until you send a signal to stop (e.g., Ctrl+C)
        # self.updater.idle()
