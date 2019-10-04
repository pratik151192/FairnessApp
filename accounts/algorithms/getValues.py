from random import random

def getDefaultUserValues():
    dict = {}
    user_comfort = round(random(), 5)
    #user_discretized_comfort = round(user_comfort*4)/4
    user_discretized_comfort = 0.5

    general_loss = user_comfort - user_discretized_comfort
    offeror_positive_loss_count = offeror_negative_loss_count = acceptor_positive_loss_count = acceptor_negative_loss_count = 0
    offeror_positive_loss = acceptor_positive_loss = offeror_negative_loss = acceptor_negative_loss = 0

    if general_loss > 0:
        offeror_positive_loss_count = acceptor_positive_loss_count = 1
        offeror_positive_loss = acceptor_positive_loss = abs(general_loss)
    else:
        offeror_negative_loss_count = acceptor_negative_loss_count = 1
        offeror_negative_loss = acceptor_negative_loss = abs(general_loss)

    #user_stubbornness = round(random(), 5)
    user_stubbornness = 0.5

    dict['comfort'] = user_discretized_comfort
    dict['stubbornness'] = user_stubbornness
    dict['oplc'] = offeror_positive_loss_count
    dict['aplc'] = acceptor_positive_loss_count
    dict['onlc'] = offeror_negative_loss_count
    dict['anlc'] = acceptor_negative_loss_count
    dict['opl'] = offeror_positive_loss
    dict['apl'] = acceptor_positive_loss
    dict['onl'] = offeror_negative_loss
    dict['anl'] = acceptor_negative_loss
    return dict

