from django.db import models
from django.utils import timezone #puede no ser necesario

class Team(models.Model):
    name = models.CharField(max_length=200)
    team_id = models.CharField(max_length=20, primary_key=True)
    bot_user_id = models.CharField(max_length=20)
    bot_access_token = models.CharField(max_length=100)

class User(models.Model):
    user_name = models.CharField(max_length=100, primary_key=True)
    in_team = models.CharField(max_length=200) #Referencia a que equipo pertenece (?)
    channel = models.CharField(max_length=300)

class Question(models.Model):
    question = models.CharField(max_length=400, primary_key=True) #La pregunta
    subject = models.CharField(max_length=15) #Sobre que tema (lenguaje)
    asked = models.CharField(max_length=100) #Quien ha preguntado
    date_ask = models.CharField(max_length=400)    #Data de consulta

class Knowledge (models.Model):
    sabiduria = models.CharField(max_length=15) #llenguatge
    user_name = models.CharField(max_length=100)
    in_team = models.CharField(max_length=200)
