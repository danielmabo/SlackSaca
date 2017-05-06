from django.db import models
from django.utils import timezone #puede no ser necesario
class Team(models.Model):
    name = models.CharField(max_length=200)
    team_id = models.CharField(max_length=20)
    bot_user_id = models.CharField(max_length=20)
    bot_access_token = models.CharField(max_length=100)

class User(models.Model):
    user_name = models.CharField(max_length=100)
    knows = models.Charfield(max_length=200)
    in_team = models.ForeignKey('Team') #Referencia a qué equipo pertenece (?)

class Question(models.Model):
    question = models.CharField(max_length=400) #La pregunta
    subject = models.CharField(max_length=15) #Sobre qué tema (lenguaje)
    asked = models.ForeignKey('User') #Quién ha preguntado
