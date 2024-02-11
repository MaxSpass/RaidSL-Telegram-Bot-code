import os
import pyautogui
from telegram.ext import Updater, CommandHandler, CallbackContext
from helpers.common import image_path
from PIL import Image
from io import BytesIO
from helpers.common import log


class TelegramBOT:
    def __init__(self, props=None):
        self.token = props['token'] if 'token' in props and bool(props['token']) else None

        if not self.token:
            raise 'No telegram token provided'
        else:
            self.commands = [
                {
                    'name': 'start',
                    'description': 'Start the bot',
                    'handler': {'type': 'message', 'callback': self._start}
                },
                {
                    'name': 'help',
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
                name = self.commands[i]['name']
                handler = self.commands[i]['handler']['callback']
                self.dp.add_handler(CommandHandler(name, handler))

    def _all_commands(self):
        commands = list(map(lambda x: f"/{x['name']} - {x['description']}", self.commands))
        return '\n\n'.join(commands)

    def _start(self, update: Updater, context: CallbackContext) -> None:
        message = 'Hello! I am your bot. Here are some available commands:\n\n' + self._all_commands()
        update.message.reply_text(message)

    def _help(self, update: Updater, context: CallbackContext) -> None:
        message = self._all_commands()
        update.message.reply_text(message)

    def add(self, obj):
        self.commands.append(obj)
        name = obj['name']
        handler = obj['handler']
        callback = handler['callback']

        def final_callback(upd, ctx):
            res = callback(upd, ctx)
            status = "Done" if bool(res) or res is None else "Error"
            message = f'{status} - {name}'

            if res and type(res) is str:
                message += f'\n{res}'

            upd.message.reply_text(message)

        self.dp.add_handler(CommandHandler(name, final_callback))

    def run(self):
        log('An App is waiting for some command')
        # Start the Bot
        self.updater.start_polling()
        # Run the bot until you send a signal to stop (e.g., Ctrl+C)
        # self.updater.idle()
