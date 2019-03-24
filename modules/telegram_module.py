import inspect
import logging

from telegram.ext import CommandHandler, MessageHandler, Filters
from config.telegram import dispatcher


def command(func):
    func.is_command = True
    return func


def photo(func):
    func.filter = Filters.photo
    return func


def location(func):
    func.filter = Filters.location
    return func


class TelegramModuleMeta(type):
    def __new__(cls, name, bases, dct):
        x = super().__new__(cls, name, bases, dct)
        for name in list(x.__dict__):
            method = getattr(x, name)
            if hasattr(method, "is_command"):
                def get_wrapper(func):
                    argspec = inspect.getfullargspec(method).args

                    if (argspec[0] != 'self'):
                        raise ValueError('First argument of TelegramCommand should be '
                                         'self')
                    argspec = argspec[1:]

                    def wrapper(bot, update, user_data=None, args=[]):
                        ins = x(context=user_data, update=update, bot=bot)
                        if len(argspec) != len(args):
                            logging.debug('Command called with invalid argument count')
                            bot.send_message(chat_id=update.message.chat_id,
                                             text='Ongeldig aantal argumenten.')
                            bot.send_message(chat_id=update.message.chat_id,
                                             text=cls.get_help_text(func))
                        else:
                            func(ins, *args)
                    wrapper.original = func
                    return wrapper

                setattr(x, name, get_wrapper(method))

                handler = CommandHandler(name, getattr(x, name), pass_user_data=True,
                                         pass_args=True)
                dispatcher.add_handler(handler)
            elif hasattr(method, 'filter'):
                def get_wrapper(func):
                    def wrapper(bot, update, user_data=None):
                        ins = x(context=user_data, update=update, bot=bot)
                        func(ins)
                    wrapper.original = func
                    return wrapper
                setattr(x, name, get_wrapper(method))
                handler = MessageHandler(method.filter, getattr(x, name),
                                         pass_user_data=True, edited_updates=True)
                dispatcher.add_handler(handler)

        return x

    @staticmethod
    def get_help_text(func):
        argspec = inspect.getfullargspec(func).args[1:]
        funcspec = '/%s %s\n' % (func.__name__,
                                 ' '.join(['<%s>' % arg for arg in argspec]))
        helptext = func.__doc__.replace('\n', ' ').replace('\t', ' ')
        helptext = ' '.join([x for x in helptext.split() if x != ''])
        return funcspec + helptext


class TelegramModule(metaclass=TelegramModuleMeta):

    def __init__(self, context=None, bot=None, update=None):
        super(TelegramModule, self).__init__()
        self.context = context
        self.bot = bot
        self.update = update

    def respond(self, msg):
        self.bot.send_message(chat_id=self.update.message.chat_id,
                              text=msg)
        logging.log(logging.INFO, 'Sending message: %s' % msg)

