from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import datetime
import bcrypt

# Create your views here.
def index(request):

    return render(request, "index.html")



#################### Login Register ####################



def registerUser(request, method="POST"):

    errors = User.objects.user_validator(request.POST)

    if len(errors) > 0:
        request.session['err'] = "register"
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")        
    
    password = request.POST['password']
    hashedPass = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    newUser = User.objects.create(fname=request.POST['fname'], lname=request.POST['lname'], dojokey=request.POST['dojokey'], username=request.POST['username'], password=hashedPass.decode())
    if newUser.dojokey == "NickIsTheGreatest":
        newUser.is_admin = True
        newUser.save()

    newFarm = Farm.objects.create(size=3, user=newUser)
    print(newUser.fname)
    print(newUser.lname)
    print(newUser.username)
    print(newUser.dojokey)
    print(newUser.password)

    request.session['userId'] = newUser.id    

    return redirect("/home")

def loginUser(request, metho="POST"):
    errors = User.objects.login_validator(request.POST)

    if len(errors) > 0:
        request.session['err'] = "login"
        for key, value in errors.items():
            messages.error(request,value)
        print('login not successful')
        return redirect("/")

    user = User.objects.filter(username=request.POST['username'])
    loggedInUser = user[0]    
    request.session['userId'] = loggedInUser.id
    
    print("login successful")

    return redirect("/home")



#################### Home Page ####################



def home(request):
    loggedInUser = User.objects.get(id=request.session['userId'] )

    context = {
        "loggedInUser": loggedInUser,
        "allPosts": Post.objects.all().order_by("-created_at"),
        "allEvents": Event.objects.all()
    }

    return render(request, "home.html", context)

def postMessage(request, method="POST"):

    errors = Post.objects.post_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect("/home")

    loggedInUser = User.objects.get(id=request.session['userId'])
    newPost = Post.objects.create(content=request.POST['content'], user=loggedInUser)

    return redirect("/home")

def postComment(request, method="POST"):

    errors = Comment.objects.comment_validator(request.POST)

    if len(errors) > 0:
        for key, value in error.items():
            messages.error(request,value)
            return redirect("/home")
    
    loggedInUser = User.objects.get(id=request.session['userId'])   
    currentPost = Post.objects.get(id=request.POST['currentPost']) 
    newComment = Comment.objects.create(content=request.POST['content'],user=loggedInUser, post=currentPost)
    return redirect("/home")

def removeMessage(request, messageId):
    currentPost = Post.objects.get(id=messageId)
    currentPost.delete()
    return redirect("/home")

def removeComment(request, commentId):
    currentComment = Comment.objects.get(id=commentId)
    currentComment.delete()
    return redirect("/home")

def createEvent(request, method="POST"):
    loggedInUser = User.objects.get(id=request.session['userId'])   
    newEvent = Event.objects.create(name=request.POST['name'], content=request.POST['desc'], uploader=loggedInUser, startdate=request.POST['startdate'], starttime=request.POST['starttime'], enddate=request.POST['enddate'], endtime=request.POST['endtime'])


    return redirect("/home")




#################### Profile Page ####################




def profile(request):
    
    loggedInUser = User.objects.get(id=request.session['userId'])
    context = { 
        "loggedInUser": loggedInUser,
        "allPosts": Post.objects.all().order_by("-created_at")
    }

    return render(request, "profile.html", context)




#######################################################################################################################




def farm(request):
	loggedInUser = User.objects.get(id = request.session['userId'])
	context = {
		'loggedInUser' : loggedInUser,
		'current_farm' : loggedInUser.farm,
		'range': range(loggedInUser.farm.size),
		'size': User.objects.get(id = request.session['userId']).farm.size,
		'myCorn': CornSeed.objects.filter(user = loggedInUser),
		'myWheat':WheatSeed.objects.filter(user = loggedInUser),
		'myCarrot': CarrotSeed.objects.filter(user = loggedInUser),
		'myLeek': LeekSeed.objects.filter(user = loggedInUser),
		'myBlackTomato': BlackTomatoSeed.objects.filter(user = loggedInUser),
		'myCornAmount': len(loggedInUser.corn.all().values()),
		'myPlantedSeeds': len(loggedInUser.cornSeed.filter(isPlanted = True)) + len(loggedInUser.wheatSeed.filter(isPlanted = True)) + len(loggedInUser.carrotSeed.filter(isPlanted = True)) + len(loggedInUser.leekSeed.filter(isPlanted = True)) + len(loggedInUser.blackTomatoSeed.filter(isPlanted = True)),
		'myUnplantedSeeds': len(loggedInUser.cornSeed.filter(isPlanted = False)) + len(loggedInUser.wheatSeed.filter(isPlanted = False)) + len(loggedInUser.carrotSeed.filter(isPlanted = False)) + len(loggedInUser.leekSeed.filter(isPlanted = False)) + len(loggedInUser.blackTomatoSeed.filter(isPlanted = False)),
		# 'myWorld': loggedInUser.world,
		'myFarmSize': loggedInUser.farm.size*10,
		'myPlantedCornSize':len(loggedInUser.cornSeed.filter(isPlanted = True)),
		'myPlantedWheatSize': len(loggedInUser.wheatSeed.filter(isPlanted = True)),
		'myPlantedCarrotSize': len(loggedInUser.carrotSeed.filter(isPlanted = True)),
		'myPlantedLeekSize': len(loggedInUser.leekSeed.filter(isPlanted = True)),
		'myPlantedBlackTomatoSize': len(loggedInUser.blackTomatoSeed.filter(isPlanted = True)),
		'myUnplantedCornSize':len(loggedInUser.cornSeed.filter(isPlanted = False)),
		'myUnplantedWheatSize': len(loggedInUser.wheatSeed.filter(isPlanted = False)),
		'myUnplantedCarrotSize': len(loggedInUser.carrotSeed.filter(isPlanted = False)),
		'myUnplantedLeekSize': len(loggedInUser.leekSeed.filter(isPlanted = False)),
		'myUnplantedBlackTomatoSize': len(loggedInUser.blackTomatoSeed.filter(isPlanted = False))

	}
	return render(request, 'farm.html', context)

def plantCorn(request):
	loggedInUser = User.objects.get(id = request.session['userId'])
	if len(loggedInUser.cornSeed.filter(isPlanted = False)) == 0:
		return redirect('/farm')
	if len(loggedInUser.cornSeed.filter(isPlanted = True)) + len(loggedInUser.wheatSeed.filter(isPlanted = True)) + len(loggedInUser.carrotSeed.filter(isPlanted = True)) + len(loggedInUser.leekSeed.filter(isPlanted = True)) + len(loggedInUser.blackTomatoSeed.filter(isPlanted = True)) >= loggedInUser.farm.size*10:
	 	return redirect('/farm')
	for cornSeed in loggedInUser.cornSeed.filter(isPlanted = False):
			cornSeed.isPlanted = True
			cornSeed.save()
			print(cornSeed.id)
			return redirect('/farm')
def plantWheat(request):
	loggedInUser = User.objects.get(id = request.session['userId'])
	if len(loggedInUser.wheatSeed.filter(isPlanted = False)) == 0:
		return redirect('/farm')
	if len(loggedInUser.cornSeed.filter(isPlanted = True)) + len(loggedInUser.wheatSeed.filter(isPlanted = True)) + len(loggedInUser.carrotSeed.filter(isPlanted = True)) + len(loggedInUser.leekSeed.filter(isPlanted = True)) + len(loggedInUser.blackTomatoSeed.filter(isPlanted = True)) >= loggedInUser.farm.size*10:
	 	return redirect('/farm')	
	for wheatSeed in loggedInUser.wheatSeed.filter(isPlanted = False):
			wheatSeed.isPlanted = True
			wheatSeed.save()
			print(wheatSeed.id)
			return redirect('/farm')

def plantCarrot(request):
	loggedInUser = User.objects.get(id = request.session['userId'])
	if len(loggedInUser.carrotSeed.filter(isPlanted = False)) == 0:
		return redirect('/farm')
	if len(loggedInUser.cornSeed.filter(isPlanted = True)) + len(loggedInUser.wheatSeed.filter(isPlanted = True)) + len(loggedInUser.carrotSeed.filter(isPlanted = True)) + len(loggedInUser.leekSeed.filter(isPlanted = True)) + len(loggedInUser.blackTomatoSeed.filter(isPlanted = True)) >= loggedInUser.farm.size*10:
	 	return redirect('/farm')	
	for carrotSeed in loggedInUser.carrotSeed.filter(isPlanted = False):
			carrotSeed.isPlanted = True
			carrotSeed.save()
			print(carrotSeed.id)
			return redirect('/farm')

def plantLeek(request):
	loggedInUser = User.objects.get(id = request.session['userId'])
	if len(loggedInUser.leekSeed.filter(isPlanted = False)) == 0:
		return redirect('/farm')
	if len(loggedInUser.cornSeed.filter(isPlanted = True)) + len(loggedInUser.wheatSeed.filter(isPlanted = True)) + len(loggedInUser.carrotSeed.filter(isPlanted = True)) + len(loggedInUser.leekSeed.filter(isPlanted = True)) + len(loggedInUser.blackTomatoSeed.filter(isPlanted = True)) >= loggedInUser.farm.size*10:
	 	return redirect('/farm')
	for leekSeed in loggedInUser.leekSeed.filter(isPlanted = False):
			leekSeed.isPlanted = True
			leekSeed.save()
			print(leekSeed.id)
			return redirect('/farm')

def plantBlackTomato(request):
	loggedInUser = User.objects.get(id = request.session['userId'])
	if len(loggedInUser.blackTomatoSeed.filter(isPlanted = False)) == 0:
		return redirect('/farm')
	if len(loggedInUser.cornSeed.filter(isPlanted = True)) + len(loggedInUser.wheatSeed.filter(isPlanted = True)) + len(loggedInUser.carrotSeed.filter(isPlanted = True)) + len(loggedInUser.leekSeed.filter(isPlanted = True)) + len(loggedInUser.blackTomatoSeed.filter(isPlanted = True)) >= loggedInUser.farm.size*10:
	 	return redirect('/farm')
	for blackTomatoSeed in loggedInUser.blackTomatoSeed.filter(isPlanted = False):
			blackTomatoSeed.isPlanted = True
			blackTomatoSeed.save()
			print(blackTomatoSeed.id)
			return redirect('/farm')

def grow(request):
	loggedInUser = User.objects.get(id = request.session['userId'])
	for cornSeed in loggedInUser.cornSeed.all():
		if cornSeed.isPlanted == True:
			cornSeed.isReady += CornSeed.gRate
			cornSeed.save()
		if cornSeed.isReady > 100:
			cornSeed.isReady = 100
			cornSeed.save()
			print('CORN', cornSeed.isReady)
	for wheatSeed in loggedInUser.wheatSeed.all():
		if wheatSeed.isPlanted == True:
			wheatSeed.isReady += wheatSeed.gRate
			wheatSeed.save()
		if wheatSeed.isReady > 100:
			wheatSeed.isReady = 100
			wheatSeed.save()
			print('WHEAT', wheatSeed.isReady)
	for carrotSeed in loggedInUser.carrotSeed.all():
		if carrotSeed.isPlanted == True:
			carrotSeed.isReady += CarrotSeed.gRate
			carrotSeed.save()
		if carrotSeed.isReady > 100:
			carrotSeed.isReady = 100
			carrotSeed.save()
	for leekSeed in loggedInUser.leekSeed.all():
		if leekSeed.isPlanted == True:
			leekSeed.isReady += LeekSeed.gRate
			leekSeed.save()
		if leekSeed.isReady > 100:
			leekSeed.isReady = 100
			leekSeed.save()
	for blackTomatoSeed in loggedInUser.blackTomatoSeed.all():
		if blackTomatoSeed.isPlanted == True:
			blackTomatoSeed.isReady += BlackTomatoSeed.gRate
			blackTomatoSeed.save()
		if blackTomatoSeed.isReady > 100:
			blackTomatoSeed.isReady = 100
			blackTomatoSeed.save()
	return redirect('/farm')

def pick(request):
	loggedInUser = User.objects.get(id = request.session['userId'])
	counter = 0
	for cSeed in loggedInUser.cornSeed.all():
		if cSeed.isReady == 100:
			loggedInUser.balance += Corn.sPrice
			loggedInUser.save()
			# for i in range(cSeed.output):
			# 	newSeed = CornSeed.objects.create(user = loggedInUser, farm = loggedInUser.farm)
			# 	# print(cornSeed.output, 'added a corn seed')
			cSeed.delete()
			print(f'picked corn')
			print(f'Your balance is {loggedInUser.balance}')
	for wSeed in loggedInUser.wheatSeed.all():
		if wSeed.isReady == 100:
			loggedInUser.balance += Wheat.sPrice
			loggedInUser.save()
			# for i in range(wSeed.output):
			# 	newWheat = WheatSeed.objects.create(user = loggedInUser, farm = loggedInUser.farm)
			# 	# print(wheatSeed.output, 'added a wheat seed')
			wSeed.delete()
			print('picked wheat')
			print(f'Your balance is {loggedInUser.balance}')
	for cSeed in loggedInUser.carrotSeed.all():
		if cSeed.isReady == 100:
			loggedInUser.balance += Carrot.sPrice
			loggedInUser.save()
			# for i in range(cSeed.output):
			# 	newCarrot = CarrotSeed.objects.create(user = loggedInUser, farm = loggedInUser.farm)
			# 	# print(carrotSeed.output, 'added a carrot seed')
			cSeed.delete()
	for lSeed in loggedInUser.leekSeed.all():
		if lSeed.isReady == 100:
			loggedInUser.balance += Leek.sPrice
			loggedInUser.save()
			# for i in range(lSeed.output):
			# 	newLeek = LeekSeed.objects.create(user = loggedInUser, farm = loggedInUser.farm)
			lSeed.delete()
	for bTomatoSeed in loggedInUser.blackTomatoSeed.all():
		if bTomatoSeed.isReady == 100:
			loggedInUser.balance += BlackTomato.sPrice
			loggedInUser.save()
			# for i in range(bTomatoSeed.output):
			# 	newBlackTomato = BlackTomatoSeed.objects.create(user = loggedInUser, farm = loggedInUser.farm)
			bTomatoSeed.delete()
	return redirect('/farm')

def buyLand(request):
	loggedInUser = User.objects.get(id = request.session['userId'])
	loggedInUser.farm.size += 1
	loggedInUser.farm.save()
	return redirect('/farm')


def buyCorn(request):
	loggedInUser = User.objects.get(id = request.session['userId'])
	if loggedInUser.balance - CornSeed.bPrice <0:
		loggedInUser.save()
		return redirect('/farm')
	newCorn = CornSeed.objects.create(user = loggedInUser, farm = loggedInUser.farm)
	loggedInUser.balance -= CornSeed.bPrice
	loggedInUser.save()
	print(newCorn)
	print(newCorn.user.fname)
	print(newCorn.user.balance)
	return redirect('/farm')

def buyWheat(request):
	loggedInUser = User.objects.get(id = request.session['userId'])
	if loggedInUser.balance - WheatSeed.bPrice <0:
		loggedInUser.save()
		return redirect('/farm')
	newWheat = WheatSeed.objects.create(user = loggedInUser, farm = loggedInUser.farm)
	loggedInUser.balance -= WheatSeed.bPrice
	loggedInUser.save()
	print(newWheat)
	print(newWheat.user.fname)
	print(newWheat.user.balance)
	return redirect('/farm')

def buyCarrot(request):
	loggedInUser = User.objects.get(id = request.session['userId'])
	if loggedInUser.balance - CarrotSeed.bPrice <0:
		print('you dont have enough money')
		return redirect('/farm')
	newCarrot = CarrotSeed.objects.create(user = loggedInUser, farm = loggedInUser.farm)
	loggedInUser.balance -= CarrotSeed.bPrice
	loggedInUser.save()
	return redirect('/farm')

def buyLeek(request):
	loggedInUser = User.objects.get(id = request.session['userId'])
	if loggedInUser.balance - LeekSeed.bPrice <0:
		loggedInUser.save()
		return redirect('/farm')
	newLeek = LeekSeed.objects.create(user = loggedInUser, farm = loggedInUser.farm)
	loggedInUser.balance -= LeekSeed.bPrice
	loggedInUser.save()
	return redirect('/farm')

def buyBlackTomato(request):
	loggedInUser = User.objects.get(id = request.session['userId'])
	if loggedInUser.balance - BlackTomatoSeed.bPrice <0:
		loggedInUser.save()
		return redirect('/farm')
	newBlackTomato = BlackTomatoSeed.objects.create(user = loggedInUser, farm = loggedInUser.farm)
	loggedInUser.balance -= BlackTomatoSeed.bPrice
	loggedInUser.save()
	return redirect('/farm')


def buyBadge(request):
	loggedInUser = User.objects.get(id = request.session['userId'])
	badge = Badge.objects.get(id = 1)
	loggedInUser.badges.add(badge)
	badge.user.add(loggedInUser)

# def call_backend(request):
# 	print((request.POST))
# 	for key, value in request.POST.items():
# 		if value == 'corn':
# 			loggedInUser = User.objects.get(username = request.session['loggedInUser'])
# 			newCorn = CornSeed.objects.create(user = loggedInUser, farm = loggedInUser.farm)
# 			loggedInUser.balance -= CornSeed.bPrice
# 			loggedInUser.save()
# 			print(newCorn)
# 			print(newCorn.user.fname)
# 			print(newCorn.user.balance)
# 		return JsonResponse({'newCorn.id':newCorn.id})
# 		if value == 'wheat':
# 			loggedInUser = User.objects.get(username = request.session['loggedInUser'])
# 			newWheat = WheatSeed.objects.create(user = loggedInUser, farm = loggedInUser.farm)
# 			loggedInUser.balance -= WheatSeed.bPrice
# 			loggedInUser.save()
# 			print(newWheat)
# 			print(newWheat.user.fname)
# 			print(newWheat.user.balance)
# 		return JsonResponse({'newWheat.id':newWheat.id})

# def getworld(request):
# 	print('blah')
# 	loggedInUser = User.objects.get(username = request.session['loggedInUser'])
# 	return JsonResponse({'world': 'blah'})









def logout(request):
    request.session.clear()
    return redirect("/")


