'''the logic behind the computations in this module is published in our work
Please refer ... for more information'''

from accounts.models import UserValues, Robots
import random
import math

'''utility function to randomly select a robot/bot for the incoming user from his assigned 10 bots'''
def getRobot(request, toggle):
    user = request.user
    uservalues = UserValues.objects.get(user=user)
    robots = Robots.objects.filter(user=user)
    #current_robot = random.choice(robots)
    current_robot=robots
    if toggle == 1:
        offeror = current_robot
        acceptor = uservalues
    elif toggle == 0:
        offeror = uservalues
        acceptor = current_robot
    offeror_values = list(map(float, offeror.offeror_values.split()))
    acceptor_values = list(map(float, acceptor.acceptor_values.split()))
    sensitivity = 0.5
    (acceptor, offeror) = updateValuesAndLosses(offeror, acceptor, offeror_values, acceptor_values, sensitivity)
    acceptor.acceptor_values = " ".join(map(str, acceptor_values))
    offeror.offeror_values = " ".join(map(str, offeror_values))
    offeror.save()
    acceptor.save()
    return (acceptor, offeror)

'''umbrella function which assigns the offeror and acceptor to robot and user (or vice-versa) and 
wraps and unwraps the offeror and accpetor values from and to the model after the model computation
has been performed respectively.'''
def imagePreference(request, current_robot, toggle):
    user = request.user
    uservalues = UserValues.objects.get(user=user)
    robots = Robots.objects.filter(user=user)
    request.session['success'] = False
    request.session['failure'] = False
    sensitivity =  0.5
    if toggle == 1:
        offeror = current_robot
        acceptor = uservalues
    elif toggle == 0:
        offeror = uservalues
        acceptor = current_robot
    acceptor.acceptor_count += 1
    offeror.offeror_count += 1

    offeror_values = list(map(float, offeror.offeror_values.split()))
    acceptor_values = list(map(float, acceptor.acceptor_values.split()))
    offeror_acceptor_values = list(map(float, offeror.acceptor_values.split()))
    acceptor_offeror_values = list(map(float, acceptor.offeror_values.split()))

    checkConditionAndPerformActions(request, offeror, acceptor, offeror_values, acceptor_values,
                                    sensitivity, offeror_acceptor_values, acceptor_offeror_values, robots)
    acceptor.acceptor_values = " ".join(map(str, acceptor_values))
    acceptor.offeror_values = " ".join(map(str, acceptor_offeror_values))
    offeror.offeror_values = " ".join(map(str, offeror_values))
    offeror.acceptor_values = " ".join(map(str, offeror_acceptor_values))
    offeror.save()
    acceptor.save()
    return (acceptor, offeror)

'''this utility function checks the current content sensitivity against the incoming (previous) offeror and acceptor
values of the respective users and rounds off to the nearest 0.25th value in [0,0.25,0.5,0.75,1]'''
def updateValuesAndLosses(offeror, acceptor, offeror_values, acceptor_values, sensitivity):

    cur_offeror_val = offeror_values[-1]
    if cur_offeror_val >= sensitivity:
        cur_offeror_val = math.ceil(cur_offeror_val * 4) / 4
    else:
        cur_offeror_val = math.floor(cur_offeror_val * 4) / 4

    previous_offeror_val = offeror_values[-1]
    del offeror_values[-1]
    offeror_values.append(cur_offeror_val)

    cur_offeror_loss = cur_offeror_val - previous_offeror_val
    if cur_offeror_loss > 0:
        offeror.offeror_positive_loss_count += 1
        offeror.offeror_positive_loss = (((offeror.offeror_positive_loss_count - 1) *
                                                   offeror.offeror_positive_loss) + (
                                                      abs(cur_offeror_loss))) / (
                                                     offeror.offeror_positive_loss_count)
    else:
        offeror.offeror_negative_loss_count += 1
        offeror.offeror_negative_loss = (((offeror.offeror_negative_loss_count - 1) *
                                                   offeror.offeror_negative_loss) + (
                                                      abs(cur_offeror_loss))) / (
                                                     offeror.offeror_negative_loss_count)

    cur_acceptor_val = acceptor_values[-1]
    if cur_acceptor_val >= sensitivity:
        cur_acceptor_val = math.ceil(cur_acceptor_val * 4) / 4
    else:
        cur_acceptor_val = math.floor(cur_acceptor_val * 4) / 4

    previous_acceptor_val = acceptor_values[-1]
    del acceptor_values[-1]
    acceptor_values.append(cur_acceptor_val)

    cur_acceptor_loss = cur_acceptor_val - previous_acceptor_val
    if cur_acceptor_loss > 0:
        acceptor.acceptor_positive_loss_count += 1
        acceptor.acceptor_positive_loss = (((acceptor.acceptor_positive_loss_count - 1) *
                                            acceptor.acceptor_positive_loss) + (
                                             abs(cur_acceptor_loss))) / (
                                            acceptor.acceptor_positive_loss_count)
    else:
        acceptor.acceptor_negative_loss_count += 1
        acceptor.acceptor_negative_loss = (((acceptor.acceptor_negative_loss_count - 1) *
                                            acceptor.acceptor_negative_loss) + (
                                             abs(cur_acceptor_loss))) / (
                                            acceptor.acceptor_negative_loss_count)
    return (acceptor, offeror)

'''an umbrella utility function which checks the difference of the offeror and acceptor value against
sensitivity of the content and the strength between users and performs appropriate actions'''
def checkConditionAndPerformActions(request, offeror, acceptor, offeror_values, acceptor_values, sensitivity,
                                    offeror_acceptor_values, acceptor_offeror_values, robots):
    window = 0.5
    link_strength = 0.5
    cur_offeror_val = offeror_values[-1]
    cur_acceptor_val = acceptor_values[-1]
    '''Underlying model equation'''
    if (abs(cur_offeror_val - cur_acceptor_val)) < (
                    window * link_strength * sensitivity):
        onSuccess(request, acceptor, offeror, offeror_values, acceptor_values, offeror_acceptor_values, acceptor_offeror_values)
    else:
        onFailure(request, acceptor, offeror, offeror_values, acceptor_values, offeror_acceptor_values, acceptor_offeror_values)
    updateOthers(acceptor, offeror, robots)

'''at each iteration, only 2 users play, retaining values for other users'''
def updateOthers(acceptor, offeror, robots):
    for robot in robots:
        if robot != offeror:
            offeror_values = list(map(float, robot.offeror_values.split()))
            acceptor_values = list(map(float, robot.acceptor_values.split()))
            offeror_values.append(offeror_values[-1])
            acceptor_values.append(acceptor_values[-1])
            robot.offeror_values = " ".join(map(str, offeror_values))
            robot.acceptor_values = " ".join(map(str, acceptor_values))
            robot.save()

'''on successful negotiation, there's no compromise and users retain their previous values'''
def onSuccess(request, acceptor, offeror, offeror_values, acceptor_values, offeror_acceptor_values, acceptor_offeror_values):
    offeror.offeror_success += 1
    acceptor.acceptor_success += 1
    offeror_values.append(offeror_values[-1])  # No motion
    acceptor_offeror_values.append(acceptor_offeror_values[-1])  # No motion
    offeror_acceptor_values.append(offeror_acceptor_values[-1])  # No motion
    acceptor_values.append(acceptor_values[-1])  # No motion
    request.session['success'] = True

'''update accordingly on failed negotiation'''
def onFailure(request, acceptor, offeror, offeror_values, acceptor_values, offeror_acceptor_values, acceptor_offeror_values):
    offeror.offeror_failure += 1
    acceptor.acceptor_failure += 1
    offeror_acceptor_values.append(offeror_acceptor_values[-1])
    acceptor_offeror_values.append(acceptor_offeror_values[-1])

    offeror_val = (offeror_values[-1] * offeror.stubbornness) + (
                    (offeror_values[-1] + acceptor_values[-1]) / 2) * (
                    1 - offeror.stubbornness)
    offeror_values.append(offeror_val)

    acceptor_val = ((acceptor_values[-1]) * acceptor.stubbornness) + (
                    (acceptor_values[-1] + offeror_values[-1]) / 2) * (
                    1 - acceptor.stubbornness)

    acceptor_values.append(acceptor_val)
    request.session['failure'] = True