import datetime

from modules.telegram_module import TelegramModule, location, command

LOCATIONS = dict()


class Location(TelegramModule):
    @location
    def recv_location(self):
        print(self.update)
        if hasattr(self.update, 'edited_message') and self.update.edited_message:
            msg = self.update.edited_message
        else:
            msg = self.update.message
        loc = msg['location']
        self.context['location'] = {'longitude': loc.longitude, 'latitude': loc.latitude}
        self.context['location']['date'] = msg['edit_date'] or msg['date']
        LOCATIONS[msg['chat']['first_name'].lower()] = self.context['location']

    @command
    def where(self, firstname):
        """
        Geeft de locatie van een teamgenoot terug.(Mits deze live locatie aan heeft staan)
        """
        firstname = firstname.lower()
        if firstname in LOCATIONS:
            loc = LOCATIONS[firstname]
            self.bot.sendLocation(self.update.message.chat_id, latitude=loc['latitude'],
                                  longitude=loc['longitude'])
            self.respond('Deze locatie update is %i minuten oud.' %
                         ((datetime.datetime.now() - loc['date']).seconds//60))
        else:
            self.respond('%s heeft helaas zijn locatie delen niet aanstaan!' % firstname)
