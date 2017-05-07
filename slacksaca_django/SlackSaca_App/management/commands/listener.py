from SlackSaca_App.models import Team, User, Question, Knowledge
from slackclient import SlackClient
from django.core.management.base import BaseCommand
from datetime import datetime
import time, re

class Command(BaseCommand):
    help = 'Starts the bot for the first'

    def handle(self, *args, **options):
        # Conectamos con el bot
        team = Team.objects.first()
        client = SlackClient(team.bot_access_token)

        # Definimos todos los regex
        create_question = re.compile(r'^create new question:([^=]*);([^=]*)')
        create_answer = re.compile(r'^answer to:([^=]*);([^=]*)')
        to_add = re.compile(r'^add to saca ([^=]*)')
        to_del = re.compile(r'^delete from saca ([^=]*)')
        my_saca = re.compile(r'^my saca')
        comando_help = re.compile(r'^help')

        if client.rtm_connect():
            while True:
                # Leemos todos los eventos disponibles
                events = client.rtm_read()
                for event in events:
                    if 'type' in event and 'text' in event:
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
                                quest = create_question.match(event['text'])
                                Question.objects.create(
                                    question=quest.group(2),
                                    asked=event['user'],
                                    subject=quest.group(1),
                                    date_ask=str(datetime.now())
                                )
                                for f in Knowledge.objects.filter(sabiduria=quest.group(1)):
                                    x = ''
                                    for e in User.objects.filter(user_name=f.user_name):
                                        x += e.channel

                                    if event['user'] != f.user_name:
                                        client.rtm_send_message(
                                            x,
                                            'Hi! Someone is asking from ' + quest.group(1) + '\n. The question is the following:\n' + quest.group(2) + '\n. If u want to answer please use the next command: answer to:'+ quest.group(2) +';[answer]'
                                        )

                                client.rtm_send_message(
                                    event['channel'],
                                    "Question made succesfully! I'm going to notice you if I'll have an answer"
                                )
                            elif create_answer.match(event['text']):
                                answ = create_answer.match(event['text'])
                                for f in Question.objects.filter(question=answ.group(1)):
                                    x = ''
                                    for e in User.objects.filter(user_name=f.asked):
                                        x += e.channel

                                    client.rtm_send_message(
                                        x,
                                        'Hi! Someone answered your question! \nThe question was:\n' + answ.group(1) + '\n. The answer is:\n' + answ.group(2)
                                    )

                                client.rtm_send_message(
                                    event['channel'],
                                    "Thank you for your collaboration! I'm going to transmit the answer to the person which asked!"
                                )
                            elif to_add.match(event['text']):
                                # aqui va una funcion para añadir
                                x = ''
                                creat = to_add.match(event['text'])
                                for e in User.objects.filter(user_name=event['user']):
                                    x += e.in_team
                                Knowledge.objects.create(
                                    sabiduria=creat.group(1),
                                    user_name=event['user'],
                                    in_team=x
                                )
                                for e in User.objects.filter(user_name=event['user']):
                                    e.channel = event['channel']
                                    e.save()

                                client.rtm_send_message(
                                    event['channel'],
                                    "¡TriSeco! Your hability have been added to your saca"
                                )
                            elif to_del.match(event['text']):
                                # aqui va una funcion para borrar
                                dlt = to_del.match(event['text'])
                                for e in Knowledge.objects.all():
                                    if e.user_name==event['user'] and e.sabiduria==dlt.group(1): e.delete()
                                client.rtm_send_message(
                                    event['channel'],
                                    "¡TriSeco! Your hability have been deleted from your saca"
                                )

                            elif comando_help.match(event['text']):
                                x = "Hi! My name is SlackSaca, and I am tool created to communicate people with questions in Hackathons with people which knows the answers. You can use the following commands:\n"
                                x += "*IMPORTANT:* The first command you have to do is *'add to saca [topic]'* to be able to ask your questions ot other people and also to be able to recibe questions and help.\n"
                                x += "*create new question:[topic];[question] ->* This command allows you to find someone who knows about the topic specified.\n"
                                x += "*answer to:[question recieved];[answer] ->* This command is used to answer a question you recieved.\n"
                                x += "*add to saca [topic] ->* This command is used to add a topic you know about in your saca (an imaginary recipient which contains all the information you are familiaritzated).\n"
                                x += "*delete from saca [topic] ->* This command is used to remove a topic you don't want to have in the saca anymore.\n"
                                x += "*my saca ->* Returns all the topics you have in the saca. \n"

                                client.rtm_send_message(
                                    event['channel'],
                                    x
                                )


                            elif my_saca.match(event['text']):
                                x = '';
                                for e in Knowledge.objects.filter(user_name=event['user']):
                                    x += e.sabiduria + '; '
                                client.rtm_send_message(
                                    event['channel'],
                                    "These are the habilities in your saca: \n" + x
                                )
                                # llamada a la consultora de la saca.
                        elif event['type']=='im_created':
                            # Función que comprueba que existe el usuario en la BD.
                            # Si no existia lo crea y envia este mensaje de bienvenida
                            client.rtm_send_message(
                                event['channel'],
                                "Hi! My name is SlackSaca, and I am tool created to communicate people with questions in Hackathons with people which knows the answers. Please, tip \'add to saca [your skills separated by commas] to start.\n"

                            )

                time.sleep(1)
