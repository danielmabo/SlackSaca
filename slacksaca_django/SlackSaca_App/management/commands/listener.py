from SlackSaca_App.models import Team
import SlackSaca_App.views
from slackclient import SlackClient
from django.core.management.base import BaseCommand
import time, re
import sys


class Command(BaseCommand):
    help = 'Starts the bot for the first'

    def handle(self, *args, **options):
        # Conectamos con el bot
        team = Team.objects.first()
        client = SlackClient(team.bot_access_token)

        # Definimos todos los regex
        create_question = re.compile(r'^create new question:(.*?);(.*?)')
        create_answer = re.compile(r'answer to(.*?);(.*?)')
        to_add = re.compile(r'add to saca(.*?)')
        to_del = re.compile(r'delete from saca(.*?)')
        my_saca = re.compile(r'my saca')

        if client.rtm_connect():
            while True:
                # Leemos todos los eventos disponibles
                events = client.rtm_read()
                for event in events:
                    if 'type' in event:
                        if event['type']=='message':
                            if event['text']=='hi':
                                client.rtm_send_message(
                                    event['channel'],
                                    "Hello! You're really cool!"
                                )
                            elif event['text'] == 'create new question':
                                client.rtm_send_message(
                                    event['channel'],
                                    "Please, introduce your question using this format: create new question:[topic];[question]"
                                )
                            elif create_question.match(event['text']):
                                # Creamos query a la BD, hacemos la pregunta a quien toque
                                client.rtm_send_message(
                                    event['channel'],
                                    "Question made succesfully! I'm going to notice you if I'll have an answer"
                                )
                            elif create_answer.match(event['text']):
                                #Creamos respuesta en la BD, mandamos la query al que ha preguntado y fin
                                client.rtm_send_message(
                                    event['channel'],
                                    "Thank you for your collaboration! I'm going to transmit the answer to the person which asked!"
                                )
                            elif to_add.match(event['text']):
                                # aqui va una funcion para añadir

                                client.rtm_send_message(
                                    event['channel'],
                                    "¡TriSeco! Your hability(ies) have been added to your saca"
                                )
                            elif to_del.match(event['text']):
                                # aqui va una funcion para borrar

                                client.rtm_send_message(
                                    event['channel'],
                                    "¡TriSeco! Your hability(ies) have been deleted from your saca"
                                )

                            elif my_saca.match(event['text']):
                                client.rtm_send_message(
                                    event['channel'],
                                    "These are the habilities in your saca: \n"
                                )
                                # llamada a la consultora de la saca.
                        elif event['type']=='im_created':
                            # Función que comprueba que existe el usuario en la BD.
                            # Si no existia lo crea y envia este mensaje de bienvenida
                            informacio_de_retorn = AfegirPersones(event)
                            client.rtm_send_message(
                                event['channel'],
                                "Hi! My name is SlackSaca, and I am tool created to communicate people with questions in Hackathons with people which knows the answers. Please, tip \'add to saca [your skills separated by commas] to start." + informacio_de_retorn
                            )
                            #En caso contrario saludamos al usuario
                time.sleep(1)