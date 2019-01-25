'''the views are kinda modularized and I've tried to avoid unconventional practices.
Being the sole developer of this project, and a timeline of 55 days, this is the best I could
do with respect to applying design patterns. In future, I plan to adhere to SRP and modularize this better'''

'''Note that while rendering HTML, a combination of Jinja 2 and jQuery is used. This can be confusing for the
browsers and bugs can appear if not done properly. I suggest using one WAY for one component 
of your application and not mixing them up'''

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from accounts.algorithms import Game
from accounts.forms import RegistrationForm, DocumentForm
from accounts.models import UserValues, Robots
from accounts.static.images.imageTexts import getImageTexts, getNames, getSettings, getFlickrIds, getExtensions, getRole

'''registration of account; mostly handled by Django'''
def register(request):
    form = RegistrationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('/accounts/profile')
    args = {'form':form}
    return render(request, 'accounts/reg_form.html', args)

'''the survey page; contains logic for user both in the offeror and acceptor case.
the cases appear alternate identified by image id modulo 2.'''
def pages(request):
    if request.user.is_authenticated:
        imageId = request.session['image_id']
        names = getNames()
        imageTexts = getImageTexts()
        settings = getSettings()
        extensions = getExtensions()
        if request.POST:
            user = UserValues.objects.get(user=request.user)

            if 'began' in request.POST:
                user.firstLogin = False
                user.save()

            if 'next' in request.POST:
                request.session['image_id'] += 1
                imageId = request.session['image_id']
                no_images = user.offeror_count + user.acceptor_count
                failure_count = user.user_offeror_failure + user.user_acceptor_failure
                if(imageId > len(getImageTexts())):
                    return render(request, 'accounts/finished.html', {'imageId':imageId, 'no_images':no_images,
                                                                      'failure_count': failure_count},)

            if 'offeror' in request.POST:
                offeror_values = list(map(float, user.offeror_values.split()))
                del offeror_values[-1]
                offeror_values.append(float(request.POST.get('offeror')))
                user.offeror_values = " ".join(map(str, offeror_values))
                user.save()
                offeror_val = list(map(float, user.offeror_values.split()))[-1]
                imagePath = "images/" + str(imageId) + "." + extensions[imageId]
                return render(request, 'accounts/model_form_upload.html', {
                    'image_id': imageId, "imagePath": imagePath, "role": getRole(imageId),
                    'setting': settings[offeror_val], 'name': names[int(request.session['image_id']) - 1]
                })

            '''if image id is odd, user is an acceptor'''
            if imageId % 2 == 1:
                preference=""
                change = ""

                if 'began' in request.POST or 'next' in request.POST or 'continue' in request.POST:
                    uservalues, current_robot = Game.getRobot(request, 1)
                    robot_offeror_value = list(map(float, current_robot.offeror_values.split()))[-1]
                    request.session['robot_offeror_value'] = robot_offeror_value
                    request.session['current_robot'] = current_robot.id

                if 'preference' in request.POST:
                    preference = request.POST.get('preference')
                    current_robot = Robots.objects.get(id=request.session['current_robot'])
                    (user, robot) = Game.imagePreference(request, current_robot, 1)
                    if 'Yes' in preference:
                        user.user_acceptor_success += 1
                    else:
                        user.user_acceptor_failure += 1
                    user_acceptor_values = list(map(float, user.user_acceptor_values.split()))
                    user_offeror_values = list(map(float, user.user_offeror_values.split()))
                    user_acceptor_values.append(user_acceptor_values[-1])
                    user_offeror_values.append(user_offeror_values[-1])
                    user.user_acceptor_values = " ".join(map(str, user_acceptor_values))
                    user.user_offeror_values = " ".join(map(str, user_offeror_values))
                    user.save()
                    robot.save()

                if 'change' in request.POST:
                    change = 'Yes'
                    user_acceptor_values = list(map(float, user.user_acceptor_values.split()))
                    del user_acceptor_values[-1]
                    user_acceptor_values.append(float(request.POST.get('change')))
                    user.user_acceptor_values = " ".join(map(str, user_acceptor_values))
                    user.save()

                imagePath = "images/" + str(imageId) + "." + extensions[imageId]
                args = {'image_id':imageId, 'imagePath': imagePath, 'preference':preference,
                        'change':change, 'text':imageTexts[str(imageId)], 'role': getRole(imageId),
                        'name': names[int(imageId-1)], 'setting': settings[request.session['robot_offeror_value']]}

                return render(request, 'accounts/pages.html', args)
            else:
                '''if image id is even, user is an offeror'''

                form = DocumentForm(request.POST or None)

                if 'began' in request.POST or 'next' in request.POST or 'continue' in request.POST:
                    current_robot, uservalues = Game.getRobot(request, 0)
                    request.session['current_robot'] = current_robot.id
                    form = DocumentForm()
                    offeror_val = list(map(float, uservalues.offeror_values.split()))[-1]
                    uservalues.save()
                    current_robot.save()
                    return render(request, 'accounts/model_form_upload.html', {
                        'form': form,
                    })

              '''  if "link" in request.POST:'''
                    uservalues = UserValues.objects.get(user=request.user)
                    link = request.POST.get("link")
                    segemented_link = link.split("/")
                    image_ids = getFlickrIds()
                
                   try:
                        imageId = int(image_ids[segemented_link[5]])
                    except (KeyError, IndexError):
                        errorMsg = "We're sorry! The link doesn't exist! Are you sure you copied it  from the album AFTER opening the photo? Please retry!"
                        form = DocumentForm()
                        return render(request, 'accounts/model_form_upload.html', {
                            'form': form, 'error': errorMsg
                        }) 
                
                offeror_val = list(map(float, uservalues.offeror_values.split()))[-1]
                    imagePath = "images/" + str(imageId) + "." + extensions[imageId]
                    return render(request, 'accounts/model_form_upload.html', {
                        'image_id': imageId, "imagePath": imagePath, "role": getRole(imageId),
                        'form': form, 'setting': settings[offeror_val], 'name':names[int(request.session['image_id'])-1]
                    })

                if "shared" in request.POST:
                    current_robot = Robots.objects.get(id=request.session['current_robot'])
                    (robot, user) = Game.imagePreference(request, current_robot, 0)
                    user_acceptor_values = list(map(float, user.user_acceptor_values.split()))
                    user_offeror_values = list(map(float, user.user_offeror_values.split()))
                    user_acceptor_values.append(user_acceptor_values[-1])
                    user_offeror_values.append(user_offeror_values[-1])
                    user.user_acceptor_values = " ".join(map(str, user_acceptor_values))
                    user.user_offeror_values = " ".join(map(str, user_offeror_values))
                    result = ""
                    if request.session['success'] == True:
                        user.user_offeror_success += 1
                        result = "pass"
                    elif request.session['failure'] == True:
                        user.user_offeror_failure += 1
                        result = "fail"
                    user.save()
                    robot.save()
                    return render(request, 'accounts/model_form_upload.html', {
                        'result': result, 'name':names[int(request.session['image_id'])-1]
                    })

                if 'change' in request.POST:
                    change = 'Yes'
                    user = UserValues.objects.get(user=request.user)
                    user_offeror_values = list(map(float, user.user_offeror_values.split()))
                    del user_offeror_values[-1]
                    user_offeror_values.append(float(request.POST.get('change')))
                    user.user_offeror_values = " ".join(map(str, user_offeror_values))
                    user.save()
                    return render(request, 'accounts/model_form_upload.html', {
                        'change': change,
                    })
        else:
            '''this part is to control the state of the page in case the user presses the refresh button'''
            settings = getSettings()

            if(imageId > len(getImageTexts())):
                user = UserValues.objects.get(user=request.user)
                no_images = user.offeror_count + user.acceptor_count
                failure_count = user.user_offeror_failure + user.user_acceptor_failure
                return render(request, 'accounts/finished.html', {'imageId':imageId, 'no_images':no_images,
                                                                  'failure_count': failure_count},)
            if imageId % 2 == 1:
                imagePath = "images/" + str(imageId) + ".png"
                args = {'image_id':imageId, 'imagePath':imagePath, 'text':getImageTexts()[str(imageId)], 'role': getRole(imageId),
                        'name': names[int(imageId-1)], 'setting': settings[request.session['robot_offeror_value']]}
                return render(request, 'accounts/pages.html', args)
            else:
                current_robot, uservalues = Game.getRobot(request, 0)
                request.session['current_robot'] = current_robot.id
                form = DocumentForm()
                offeror_val = list(map(float, uservalues.offeror_values.split()))[-1]
                uservalues.save()
                current_robot.save()
                return render(request, 'accounts/model_form_upload.html', {
                    'form': form, 'setting': settings[offeror_val], 'name':names[int(request.session['image_id'])],
                })
    else:
        return render(request, 'accounts/login.html')

@login_required()
def profile(request):
    if request.user.is_authenticated:
        uservalues = UserValues.objects.get(user=request.user)
        if 'image_id' not in request.session:
            request.session['image_id'] = uservalues.image_id
        imageId = request.session['image_id']

        '''there will be total 12 iterations; finish the study when image id exceeds.'''
        if(imageId > len(getImageTexts())):
            no_images = uservalues.offeror_count + uservalues.acceptor_count
            failure_count = uservalues.user_offeror_failure + uservalues.user_acceptor_failure
            return render(request, 'accounts/finished.html', {'imageId':imageId, 'no_images':no_images,
                                                              'failure_count': failure_count},)

        args = {'username': request.user.username, 'user':uservalues,
                'image_id':uservalues.image_id, 'firstLogin':uservalues.firstLogin,
                'offeror':'No', 'acceptor':'No'}

        if imageId % 2 == 0:
            args['toggle'] = 'upload'
        else:
            args['toggle'] = 'pages'

        if 'showQuestions' in request.POST:
            request.session['questions'] = 'Yes'
        if 'questions' in request.session:
            args['questions'] = request.session['questions']

        if 'offeror' in request.POST:
            offeror = request.POST.get('offeror')
            uservalues.comfort = float(offeror)
            uservalues.offeror_values = offeror
            uservalues.user_offeror_values = offeror
            request.session['offeror'] = 'Yes'
            uservalues.save()

        if 'acceptor' in request.POST:
            comfort = request.POST.get('acceptor')
            uservalues.comfort = float(comfort)
            request.session['acceptor']= 'Yes'
            uservalues.acceptor_values = comfort
            uservalues.user_acceptor_values = comfort
            uservalues.save()

        if 'offeror' in request.session:
            args['offeror'] = request.session['offeror']
        if 'acceptor' in request.session:
            args['acceptor'] = request.session['acceptor']

        return render(request, 'accounts/profile.html', args)


@login_required()
def logout(request):
    uservalues = UserValues.objects.get(user=request.user)
    if 'image_id' in request.session:
        uservalues.image_id = request.session['image_id']
    if 'robot_offeror_value' in request.session:
        uservalues.last_robot_value = request.session['robot_offeror_value']
    uservalues.save()
    request.session.flush()
    auth.logout(request)
    return render(request, "accounts/logout.html")
