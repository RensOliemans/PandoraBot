from modules.telegram_module import TelegramModule
from modules.telegram_module import command
from . import util


class Puzzles(TelegramModule):

    @command
    def building(self, number):
        """
        Geeft de gebouwnaam bij een gebouwnummer.
        """
        building = util.building_by_number(number)

        if not building:
            self.respond('Dat gebouwnummer bestaat niet!')

        self.respond('Gebouwnummer %s komt overeen met gebouw %s.' % (number, building.name))

    def location(self, length):
        """
        Geeft een lijst met alle locaties die een specifieke lengte hebben
        """
        results = util.location_by_length(length)
        self.respond('Er zijn %i resultaten met lengte %s' % (len(results), length))
        self.respond(' '.join([x.name for x in results]))

    #Aliases
    gebouw = building
