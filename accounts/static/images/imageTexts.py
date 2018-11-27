'''all static informtion related to rendered images and privacy settings
reside here and are returned through respective utility functions...this Python
file shouldn't ideally exist here; but it contextually makes more sense'''

texts = {
    "1": "A doctor is inspecting a pregnant lady!",
    "2": "Funeral of a friend!",
    "3": "Dinner with clients from Europe!",
    "4": "Bunch of people you're buying stuff from at an Asian store!",
    "5": "Haha! Nurses sleeping in the hospital!",
    "6": "Celebrating Christmas with friends and family!",
    "7": "Commencement day, amazing journey at college comes to an end!",
    "8": "Police arresting a lady for some crime!",
    "9": "The college reunion is always crazy!",
    "10": "A fun picnic with friends and family!",
    "11": "Haha! People doing crazy stuff with their bikes!",
    "12": "The baby doesn't like Santa Claus :(",
}
extensions = {
    1: "png",
    2: "png",
    3: "png",
    4: "jpg",
    5: "jpg",
    6: "png",
    7: "png",
    8: "jpg",
    9: "png",
    10: "png",
    11: "jpg",
    12: "jpg"
}
image_ids_flickr = {
    "42796963350": 1,
    "44557297732": 2,
    "44557302262": 3,
    "43697667145": 4,
    "44557302662": 5,
    "44557302622": 6,
    "43697667285": 7,
    "44607583261": 8,
    "43697667735": 9,
    "44557297492": 10,
    "44607583011": 11,
    "42796962380": 12,
}

names = ['Monica', 'Chandler', 'Joey', 'Phoebe', 'Rachel', 'Ross', 'Eric', 'Sloan', 'Vince', 'Ari', 'Shauna', 'Amanda']

settings = {
    0: 'Private/Only Me',
    0.25: 'Friends',
    0.5: 'Friends of Friends',
    0.75: 'Friends of Friends of Friends',
    1: 'Public'
}
def getImageTexts():
    return texts

def getNames():
    return names

def getSettings():
    return settings

def getFlickrIds():
    return image_ids_flickr

def getExtensions():
    return extensions

def getRole(imageId):
    if imageId % 3 == 1: return "Friends"
    elif imageId %3 == 2: return "Best Friends"
    else: return "Family members"