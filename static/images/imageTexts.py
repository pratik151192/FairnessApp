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

image_ids_flickr = {
    "25164146788": 1,
    "38319188074": 2,
    "25164146488": 3,
    "38998495742": 4,
    "38998493212": 5,
    "25164145568": 6,
    "39034982171": 7,
    "38998565232": 8,
    "38149674545": 9,
    "38149674475": 10,
    "27258747489": 11,
    "38149673205": 12,
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