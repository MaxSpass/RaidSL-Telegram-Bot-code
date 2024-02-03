import os
import pyautogui
from telegram.ext import Updater, CommandHandler, CallbackContext
from helpers.common import image_path
from PIL import Image
from io import BytesIO
from helpers.common import log

class TelegramBOT:
    # Define your token here @TODO should be taken from .env
    TOKEN = '6722044970:AAGZ5EtkQPVFpSzHqhKeAiCf3sXD-PRX6_w'

    def __init__(self, props=None):
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
            {
                'name': 'screen',
                'description': 'Capture and send a screenshot',
                'handler': {'type': 'screenshot', 'callback': lambda *args: self._screen(*args)}
            },
        ]

        # Create the Updater and pass it your bot's token
        self.updater = Updater(token=self.TOKEN)
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

    # @TODO Important refactoring in order to make 'screen' function working in async way
    def _screen(self, update: Updater, context: CallbackContext) -> None:
        screenshot = pyautogui.screenshot(region=[0, 0, 920, 540])

        # Convert the screenshot to bytes
        image_bytes = BytesIO()
        screenshot.save(image_bytes, format='PNG')
        image_bytes.seek(0)

        context.bot.send_photo(chat_id=update.message.chat_id, photo=image_bytes)


    def add(self, obj):
        self.commands.append(obj)
        name = obj['name']
        handler = obj['handler']
        _type = handler['type'] if 'type' in handler else 'none'
        callback = handler['callback']

        if _type == 'message':
            def final_callback(upd, ctx):
                result = callback()
                message = result if result else 'Empty'
                upd.message.reply_text(message)

            self.dp.add_handler(CommandHandler(name, final_callback))
        else:
            def final_callback(upd, ctx):
                callback()
                upd.message.reply_text(f'Done - {name}')

            self.dp.add_handler(CommandHandler(name, final_callback))

    def run(self):
        log('An App is waiting for some command')
        # Start the Bot
        self.updater.start_polling()
        # Run the bot until you send a signal to stop (e.g., Ctrl+C)
        # self.updater.idle()
