from modules.telegram_module import TelegramModule, command, TelegramModuleMeta
from modules import loaded_modules


class Help(TelegramModule):

    @command
    def help(self):
        """
        Geeft een overzicht van alle functionaliteit
        """
        result = 'Hieronder staan alle commando\'s die ik begrijp:\n'

        for module in loaded_modules + [Help]:
            result += ' - %s module:\n' % module.__name__
            for name in list(module.__dict__):
                func = getattr(module, name)
                if getattr(func, 'original', False):
                    result += TelegramModuleMeta.get_help_text(func.original)
                    result += '\n\n'

        self.respond(result)
