# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_name = models.CharField(max_length=20)
    admin_password = models.CharField(max_length=20)

    class Meta:
        db_table = 'admin'


class Friends(models.Model):
    record_id = models.AutoField(primary_key=True)
    friend1 = models.ForeignKey('Player', models.DO_NOTHING)
    friend2 = models.ForeignKey('Player', models.DO_NOTHING, related_name='friends_friend2_set')

    class Meta:
        db_table = 'friends'


class Player(models.Model):
    player_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    play_time = models.FloatField()
    played_round = models.IntegerField()
    max_score = models.FloatField()
    number_of_cooperation = models.IntegerField(db_column='Number_of_cooperation')  # Field name made lowercase.

    class Meta:
        db_table = 'player'


class RankRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    player = models.ForeignKey(Player, models.DO_NOTHING)
    score = models.FloatField()
    upload_time = models.DateTimeField()
    team = models.ForeignKey('Teams', models.DO_NOTHING)

    class Meta:
        db_table = 'rank_record'


class Teams(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=32)
    highest_score = models.CharField(max_length=32)
    player1 = models.ForeignKey(Player, models.DO_NOTHING, blank=True, null=True)
    player2 = models.ForeignKey(Player, models.DO_NOTHING, related_name='teams_player2_set', blank=True, null=True)

    class Meta:
        db_table = 'teams'
