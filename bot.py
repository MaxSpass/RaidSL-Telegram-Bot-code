import threading
from telegram.ext import Updater, CommandHandler, CallbackContext
from helpers.common import log

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

        self.dp.add_handler(CommandHandler(command, handler, run_async=True))

    def listen(self):
        log('An App is waiting for some command')
        # Start the Bot
        self.updater.start_polling()
        # Run the bot until you send a signal to stop (e.g., Ctrl+C)
        # self.updater.idle()
