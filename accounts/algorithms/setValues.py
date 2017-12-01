from accounts.models import UserValues

def setAtLogin(request):
    uservalues = UserValues.objects.get(user=request.user)
    imageId = uservalues.image_id
    request.session['image_id'] = imageId

def setFinalUserVals(request):
    uservalues = UserValues.objects.get(user=request.user)
    uservalues.image_id = request.session['image_id']
    uservalues.save()
