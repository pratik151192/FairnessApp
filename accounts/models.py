from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.algorithms import getValues

# Create your models here.
#try to update
'''basic profile model for a user'''
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, default='')
    firstName = models.CharField(max_length=20, default='')
    lastName = models.CharField(max_length=20, default='')

'''the parameters and final values we need for each user '''
class UserValues(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstLogin = models.BooleanField(default=True)
    STUB_NEUR=0.5
    COMFORT_NEU=0.5
    COMFORT_CHOICES=[(COMFORT_NEU,'Neur')]
    STUB_CHOICES=[(STUB_NEUR,'Neu')]
    comfort = models.FloatField(choices=COMFORT_CHOICES)
    stubbornness = models.FloatField(choices=STUB_CHOICES)
    neighbors = models.TextField(default='')
    offeror_values = models.TextField(default='')
    user_offeror_values = models.TextField(default='')
    user_acceptor_values = models.TextField(default=' ')
    acceptor_values = models.TextField(default='')
    offeror_count = models.IntegerField(default=0)
    acceptor_count = models.IntegerField(default=0)
    offeror_success = models.IntegerField(default=0)
    acceptor_success = models.IntegerField(default=0)
    offeror_failure = models.IntegerField(default=0)
    acceptor_failure = models.IntegerField(default=0)
    user_offeror_success = models.IntegerField(default=0)
    user_acceptor_success = models.IntegerField(default=0)
    user_offeror_failure = models.IntegerField(default=0)
    user_acceptor_failure = models.IntegerField(default=0)
    offeror_positive_loss = models.FloatField(default=0)
    offeror_negative_loss = models.FloatField(default=0)
    acceptor_positive_loss = models.FloatField(default=0)
    acceptor_negative_loss = models.FloatField(default=0)
    acceptor_positive_loss_count = models.IntegerField(default=0)
    acceptor_negative_loss_count = models.IntegerField(default=0)
    offeror_positive_loss_count = models.IntegerField(default=0)
    offeror_negative_loss_count = models.IntegerField(default=0)
    image_id = models.IntegerField(default=1)
    last_robot_value = models.FloatField(default=0)

'''the robots/bots who will play with the users'''

class Robots(models.Model):
    COMFORT_NEU=0.5
    #COMFORT_MAX=1.0
    #OMFORT_CHOICES=((0.5,'Neur'))
    STUB_NEUR=0.5
    #STUB_MIN=0.0
    #STUB_CHOICES=((0.5,'Neur'))
    COMFORT_CHOICES=[(COMFORT_NEU,'Neur')]
    STUB_CHOICES=[(STUB_NEUR,'Neu')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #comfort = models.FloatField(default=0.0)
    comfort = models.FloatField(choices=COMFORT_CHOICES, default='Neur')
    
    #stubbornness = models.FloatField(default=0.0)
    stubbornness = models.FloatField(choices=STUB_CHOICES, default='Neu')
    
    neighbors = models.TextField(default='')
    offeror_values = models.TextField(default='')
    acceptor_values = models.TextField(default='')
    offeror_count = models.IntegerField(default=0)
    acceptor_count = models.IntegerField(default=0)
    offeror_success = models.IntegerField(default=0)
    acceptor_success = models.IntegerField(default=0)
    offeror_failure = models.IntegerField(default=0)
    acceptor_failure = models.IntegerField(default=0)
    offeror_positive_loss = models.FloatField(default=0)
    offeror_negative_loss = models.FloatField(default=0)
    acceptor_positive_loss = models.FloatField(default=0)
    acceptor_negative_loss = models.FloatField(default=0)
    acceptor_positive_loss_count = models.IntegerField(default=0)
    acceptor_negative_loss_count = models.IntegerField(default=0)
    offeror_positive_loss_count = models.IntegerField(default=0)
    offeror_negative_loss_count = models.IntegerField(default=0)
    image_id = models.IntegerField(default=1)

'''offeror upload image model'''
class Document(models.Model):
    link = models.CharField(max_length=150, default='')

'''as soon as a new user registers, a profile model, values model, and model for user's bots
are immediately created'''
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile.objects.create(user = instance,
                                                  username = instance.username,
                                                  firstName = instance.first_name,
                                                  lastName = instance.last_name)
        dict = getValues.getDefaultUserValues()
        values_profile = UserValues.objects.create(user = instance, comfort = dict['comfort'],
                                                   stubbornness = dict['stubbornness'], 
                                                   offeror_values=str(dict['comfort']),
                                                   acceptor_values = str(dict['comfort']), 
                                                   user_offeror_values=str(dict['comfort']),
                                                   user_acceptor_values = str(dict['comfort']), 
                                                   offeror_positive_loss_count = dict['oplc'],
                                                   offeror_negative_loss_count = dict['onlc'], acceptor_positive_loss_count = dict['aplc'],
                                                   acceptor_negative_loss_count = dict['anlc'], offeror_positive_loss = dict['opl'],
                                                   offeror_negative_loss = dict['onl'], acceptor_positive_loss = dict['apl'],
                                                   acceptor_negative_loss = dict['anl'])

        for i in range (0,10):
            dict = getValues.getDefaultUserValues()
            robot = Robots.objects.create(user = instance, comfort = 0.5, #dict['comfort'],
                                              stubbornness = 0.5, #dict['stubbornness'], 
                                              offeror_values=str(0.5),  #str(dict['comfort']),
                                              acceptor_values = str(0.5),#str(dict['comfort']),
                                              offeror_positive_loss_count = dict['oplc'],
                                              offeror_negative_loss_count = dict['onlc'], acceptor_positive_loss_count = dict['aplc'],
                                              acceptor_negative_loss_count = dict['anlc'], offeror_positive_loss = dict['opl'],
                                              offeror_negative_loss = dict['onl'], acceptor_positive_loss = dict['apl'],
                                              acceptor_negative_loss = dict['anl'])
            values_profile.neighbors += " " + str(robot.id)
            values_profile.save()

post_save.connect(create_profile, sender=User)

