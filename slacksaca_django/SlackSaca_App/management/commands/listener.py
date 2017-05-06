from SlackSaca_App.models import Team
from slackclient import SlackClient
from django.core.management.base import BaseCommand
import time



class Command(BaseCommand):
    help = 'Starts the bot for the first'

    def handle(self, *args, **options):
        team = Team.objects.first()
        client = SlackClient(team.bot_access_token)
        if client.rtm_connect():
            while True:
                events = client.rtm_read()
                for event in events:
                    if event['type']=='message' and event['text']=='hi':
                        client.rtm_send_message(
                            event['channel'],
                            "¡TriSeco!"
                        )
                time.sleep(1)