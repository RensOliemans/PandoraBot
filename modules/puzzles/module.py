from modules.telegram_module import TelegramModule
from modules.telegram_module import command
from . import util
from .morse import CODE, CODE_REVERSED


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

    @command
    def locations(self, length):
        """
        Geeft een lijst met alle locaties die een specifieke lengte hebben
        """
        results = util.location_by_length(length)
        self.respond('Er zijn %i resultaten met lengte %s' % (len(results), length))
        self.respond(', '.join([x.name for x in results]))

    @command
    def locations_with(self, symbols):
        """
        Geeft een lijst met alle locaties waarvan de naam alle gegeven symbolen bevat
        """
        results = util.locations_containing_symbols(symbols)
        self.respond('Er zijn %i resultaten die de symbolen \'%s\' bevatten' % (len(results), symbols))
        self.respond(', '.join([x.name for x in results]))

    @command
    def buildings(self, length):
        """
        Geeft een lijst met alle gebouwen die een specifieke lengte hebben
        """
        results = util.buildings_by_length(length)
        self.respond('Er zijn %i gebouwen met lengte %s' % (len(results), length))
        self.respond(', '.join([str(x) for x in results]))

    @command
    def buildings_with(self, symbols):
        """
        Geeft een lijst met alle gebouwen waarvan de naam alle gegeven symbolen bevat
        """
        results = util.buildings_containing_symbols(symbols)
        self.respond('Er zijn %i gebouwen die de symbolen \'%s\' bevatten' % (len(results), symbols))
        self.respond(', '.join([str(x) for x in results]))


class Words(TelegramModule):
    @command
    def text_to_morse(self, *words):
        """
        Zet een aantal woorden om naar morse
        """
        self.respond('\n'.join([' '.join(CODE.get(i.upper(), '?') for i in word)
                               for word in words]))

    @command
    def morse_to_text(self, *morse):
        """
        Zet een aantal morse letters (onderbroken door spatie) en woorden (onderbroken door ; )
        om naar letters
        """
        words = self._determine_words(*morse)
        self.respond(' '.join(''.join(CODE_REVERSED.get(i, '?') for i in word) for word in words))

    def _determine_words(self, *morse):
        word_breaks = [i for i, x in enumerate(morse) if x == ';']
        start_index = 0
        words = list()

        for _, end_index in enumerate(word_breaks):
            words.append(morse[start_index:end_index])
            start_index = end_index + 1
        words.append(morse[start_index:])  # Don't forget the last word
        return words
