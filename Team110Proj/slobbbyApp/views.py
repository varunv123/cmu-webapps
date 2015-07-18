from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, Http404
from mimetypes import guess_type

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.core import serializers
import json

from slobbbyApp.models import *
from slobbbyApp.forms import *

# Create your views here.
@login_required
def unfollow(request,id):
	u = User.objects.get(id=id)
	follow = Follow.objects.get(follower=request.user,followee=u)
	follow.delete()
	following = False
	blocked = False
	blocks = Block.objects.filter(blocker=request.user,blockee=u)
	if (len(blocks)>0):
		blocked = True
	users = User.objects.filter(id=id)
	events = Event.objects.filter(user=User.objects.get(id=id)).order_by('startTime')
	searchForm = SearchForm()
	return render(request,'UserProfile.html',{'users':users,'events':events,'following':following,'searchForm':searchForm,'blocked':blocked})


@login_required
def follow(request,id):
	user_to_follow = User.objects.get(id=id)
	user_requesting_follow = request.user
	new_follow = Follow(follower=user_requesting_follow,followee=user_to_follow)
	new_follow.save()
	users = User.objects.filter(username=request.user.username)
	searchForm = SearchForm()
	user1 = User.objects.get(username__exact=request.user.username)
	blocks = user1.blockees.all()
	blockedBy = []
	for block in blocks:
		blockedBy.append(block.blocker)
	follows = user1.followers.all()
	usersFollowing = []
	for follow in follows:
		usersFollowing.append(follow.followee)
	events = Event.objects.exclude(user=request.user).filter(user__in = usersFollowing).exclude(user__in = blockedBy).order_by('startTime')
	return render(request,'FollowerStream.html',{'users':users,'events':events,'searchForm':searchForm,'blockedBy':blockedBy})

@login_required
def unblock_user(request,id):
	u = User.objects.get(id=id)
	block = Block.objects.get(blocker=request.user,blockee=u)
	block.delete()
	blocked = False
	following = False
	follow = Follow.objects.filter(follower=request.user,followee=u)
	if (len(follow)>0):
		following = True
	users = User.objects.filter(id=id)
	events = Event.objects.filter(user=User.objects.get(id=id)).order_by('startTime')
	searchForm = SearchForm()
	return render(request,'UserProfile.html',{'users':users,'events':events,'following':following,'searchForm':searchForm,'blocked':blocked})

@login_required
def block_user(request,id):
	user_to_block = User.objects.get(id=id)
	user_blocking = request.user
	new_block = Block(blocker=user_blocking,blockee=user_to_block)
	new_block.save()
	users = User.objects.filter(username=request.user.username)
	#grumbls = Grumbl.objects.exclude(user=request.user).order_by('-date')
	searchForm = SearchForm()
	user1 = User.objects.get(username__exact=request.user.username)
	blocks = user1.blockees.all()
	blockedBy = []
	for block in blocks:
		blockedBy.append(block.blocker)
	follows = user1.followers.all()
	usersFollowing = []
	for follow in follows:
		usersFollowing.append(follow.followee)
	events = Event.objects.exclude(user=request.user).filter(user__in = usersFollowing).exclude(user__in = blockedBy).order_by('startTime')
	return render(request,'FollowerStream.html',{'users':users,'events':events,'searchForm':searchForm,'blockedBy':blockedBy})

@login_required
def delete_event(request,id):
	if request.method == "POST" :
		eventForm = EventForm(request.POST)
	else:
		eventForm = EventForm()
	errors = []
	try:
		event_to_delete = Event.objects.get(id=id,user=request.user)
		event_to_delete.delete()
	except ObjectDoesNotExist:
		errors.append("Event does not exist")
	events = Event.objects.filter(user=request.user).order_by('startTime')
	searchForm = SearchForm()
	users = User.objects.filter(username=request.user.username)
	user1 = User.objects.get(username__exact=request.user.username)
	blocks = user1.blockees.all()
	blockedBy = []
	for block in blocks:
		blockedBy.append(block.blocker)
	follows = user1.followers.all()
	usersFollowing = []
	for follow in follows:
		usersFollowing.append(follow.followee)
	events1 = Event.objects.exclude(user=request.user).filter(user__in = usersFollowing).exclude(user__in = blockedBy).order_by('startTime')
	overlapEvents = []
	for e in events1:
		for e2 in events:
			if (e.location==e2.location):
				if ((e.startTime>=e2.startTime and e.startTime<=e2.endTime)or(e.endTime>=e2.startTime and e.endTime<=e2.endTime)):
					overlapEvents.append(e)
				elif ((e2.startTime>=e.startTime and e2.startTime<=e.endTime) or(e2.endTime>=e.startTime and e2.endTime<=e.endTime)):
					overlapEvents.append(e)
	invitedEvents = user1.invitedUsers.all()
	context = {'invitedEvents':invitedEvents,'followingUsers':usersFollowing,'users':users,'events':events,'errors':errors,'eventForm':eventForm,'searchForm':searchForm,'overlapEvents':overlapEvents}
	return render(request,'ProfilePage.html',context)

@login_required
def add_user_to_group(request,groupid,userid):
	group = Group.objects.get(id=groupid)
	print group.groupName
	user1 = User.objects.get(id=userid)
	group.groupUsers.add(user1)
	group.save()
	print user1
	return redirect("/slobbbyrobbby/groupPage/" + groupid)
	


@login_required
def groupPage(request,id):
	try:
		g = Group.objects.get(id=id)
	except:
		raise Http404

	users = User.objects.filter(username=request.user.username)
	groupEvents = []
	for user in Group.objects.get(id=id).groupUsers.all():
		print user.username
		events = Event.objects.filter(user=user)
		for event in events:
			groupEvents.append(event)
		events = []
	print groupEvents
	searchForm = SearchForm()
	user1 = User.objects.get(username=request.user.username)
	follows = user1.followers.all()
	usersFollowing = []
	for follow in follows:
		usersFollowing.append(follow.followee)
	return render(request,'Groups.html',{'group':g,'followingUsers':usersFollowing,'users':users,'searchForm':searchForm, 'groupName':g.groupName , 'events':groupEvents})

@login_required
def userProfile(request,id):
	following = False
	try:
		u = User.objects.get(id=id)
	except:
		raise Http404
	follow = Follow.objects.filter(follower=request.user,followee=u)
	blocks = Block.objects.filter(blocker=request.user,blockee=u)
	if (len(follow)>0):
		following = True
	blocked = False
	if (len(blocks)>0):
		blocked = True
	users = User.objects.filter(id=id)
	events = Event.objects.filter(user=User.objects.get(id=id)).order_by('startTime')
	searchForm = SearchForm()
	return render(request,'UserProfile.html',{'users':users,'events':events,'following':following,'searchForm':searchForm,'blocked':blocked})

@login_required
def get_stream(request,id):
	response_text1 = ["test"]
	jsonresponse = json.dumps(response_text1)
	return HttpResponse(jsonresponse, content_type="application/json")



@login_required
def home(request):
	searchForm = SearchForm()
	groupForm = GroupForm()
	users = User.objects.filter(username=request.user.username)
	user1 = User.objects.get(username__exact=request.user.username)
	blocks = user1.blockees.all()
	blockedBy = []
	for block in blocks:
		blockedBy.append(block.blocker)
	follows = user1.followers.all()
	usersFollowing = []
	for follow in follows:
		usersFollowing.append(follow.followee)
	groups = Group.objects.filter(owner=request.user)
	events = Event.objects.exclude(user=request.user).filter(user__in = usersFollowing).exclude(user__in = blockedBy).order_by('startTime')
	users = User.objects.filter(username=request.user.username)
	return render(request,'FollowerStream.html',{'searchForm':searchForm, 'groupForm':groupForm, 'events':events,'users':users, 'groups':groups})

@transaction.atomic
def register(request):
	context = {}

	errors = []
	context['errors'] = errors

	if request.method == "POST" :
		form = AuthenticationForm(request,data=request.POST)
		regform = RegistrationForm(request.POST)
	else:
		form = AuthenticationForm(request)
		regform = RegistrationForm()

	context['form'] = form
	context['regform'] = regform

	if not regform.is_valid():
		return render(request,'LoginPage.html',context)

	new_user = User.objects.create_user(username=regform.cleaned_data['username'], \
									email=regform.cleaned_data['email'], \
									password=regform.cleaned_data['password1'])
	new_user.save()
	new_user = authenticate(username=regform.cleaned_data['username'], \
							password=regform.cleaned_data['password1'])
	new_profile = UserProfile(user=new_user)
	new_profile.save()
	new_user.is_active = False
	new_user.save()
	token = default_token_generator.make_token(new_user)
	email_body = """
Welcome to the SlobbbyRobbby.  Please click the link below to
verify your email address and complete the registration of your account:

  http://%s%s
""" % (request.get_host() + "/slobbbyrobbby", 
       reverse('confirm', args=(new_user.username, token)))

	send_mail(subject="Verify your email address",
              message= email_body,
              from_email="charlie+devnull@cs.cmu.edu",
              recipient_list=[new_user.email])

    
	#login(request,new_user)
	context['email'] = regform.cleaned_data['email']
	return render(request, 'needs-confirmation.html', context)
	return redirect('/grumblr/')


@transaction.atomic
def confirm_registration(request, username, token):
    user = get_object_or_404(User, username=username)

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404

    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()
    return render(request, 'confirmed.html', {})

@login_required
def profile(request):
	if request.method == "POST" :
		eventForm = EventForm(request.POST)
	else:
		eventForm = EventForm()
	users = User.objects.filter(username=request.user.username)
	events = Event.objects.filter(user=request.user).order_by('startTime')
	searchForm = SearchForm()

	user1 = User.objects.get(username__exact=request.user.username)
	blocks = user1.blockees.all()
	blockedBy = []
	for block in blocks:
		blockedBy.append(block.blocker)
	follows = user1.followers.all()
	usersFollowing = []
	for follow in follows:
		usersFollowing.append(follow.followee)
	events1 = Event.objects.exclude(user=request.user).filter(user__in = usersFollowing).exclude(user__in = blockedBy).order_by('startTime')
	overlapEvents = []
	for e in events1:
		for e2 in events:
			if (e.location==e2.location):
				if ((e.startTime>=e2.startTime and e.startTime<=e2.endTime)or(e.endTime>=e2.startTime and e.endTime<=e2.endTime)):
					overlapEvents.append(e)
				elif ((e2.startTime>=e.startTime and e2.startTime<=e.endTime) or(e2.endTime>=e.startTime and e2.endTime<=e.endTime)):
					overlapEvents.append(e)
	invitedEvents = user1.invitedUsers.all()
	return render(request,'ProfilePage.html',{'invitedEvents':invitedEvents,'followingUsers':usersFollowing,'users':users,'events':events,'overlapEvents':overlapEvents,'eventForm':eventForm,'searchForm':searchForm})

@login_required
def add_group(request):
	errors = []
	if request.method == "POST" :
		groupForm = GroupForm(request.POST)
		group = Group(owner=request.user, groupName=request.POST['groupName'])
	else:
		groupForm = GroupForm()

	group.save()
	searchForm = SearchForm()
	users = User.objects.filter(username=request.user.username)
	user1 = User.objects.get(username__exact=request.user.username)
	blocks = user1.blockees.all()
	blockedBy = []
	for block in blocks:
		blockedBy.append(block.blocker)
	follows = user1.followers.all()
	usersFollowing = []
	for follow in follows:
		usersFollowing.append(follow.followee)
	events = Event.objects.exclude(user=request.user).filter(user__in = usersFollowing).exclude(user__in = blockedBy).order_by('startTime')
	users = User.objects.filter(username=request.user.username)
	groups = Group.objects.filter(owner = request.user)
	if not groupForm.is_valid():
		context = {'followingUsers':usersFollowing,'users':users,'errors':errors,'groupForm':groupForm, 'events':events, 'searchForm':searchForm, 'groups':groups}
		return render(request,'FollowerStream.html',context)
	context = {'followingUsers':usersFollowing,'users':users,'errors':errors,'groupForm':groupForm, 'events':events, 'searchForm':searchForm, 'groups':groups}
	render(request,'FollowerStream.html',context)
	return redirect('/slobbbyrobbby/')

@login_required
def add_event(request):
	errors = []
	if request.method == "POST" :
		new_event = Event(user=request.user)
		eventForm = EventForm(request.POST,instance=new_event)
	else:
		eventForm = EventForm()
	if not eventForm.is_valid():
		events = Event.objects.filter(user=request.user).order_by('startTime')
		searchForm = SearchForm()
		users = User.objects.filter(username=request.user.username)
		user1 = User.objects.get(username__exact=request.user.username)
		blocks = user1.blockees.all()
		blockedBy = []
		for block in blocks:
			blockedBy.append(block.blocker)
		follows = user1.followers.all()
		usersFollowing = []
		for follow in follows:
			usersFollowing.append(follow.followee)
		events1 = Event.objects.exclude(user=request.user).filter(user__in = usersFollowing).exclude(user__in = blockedBy).order_by('startTime')
		overlapEvents = []
		for e in events1:
			for e2 in events:
				if (e.location==e2.location):
					if ((e.startTime>=e2.startTime and e.startTime<=e2.endTime)or(e.endTime>=e2.startTime and e.endTime<=e2.endTime)):
						overlapEvents.append(e)
					elif ((e2.startTime>=e.startTime and e2.startTime<=e.endTime) or(e2.endTime>=e.startTime and e2.endTime<=e.endTime)):
						overlapEvents.append(e)
		invitedEvents = user1.invitedUsers.all()
		context = {'invitedEvents':invitedEvents,'followingUsers':usersFollowing,'users':users, 'events':events,'errors':errors,'eventForm':eventForm,'searchForm':searchForm,'overlapEvents':overlapEvents}
		return render(request,'ProfilePage.html',context)

	eventForm.save()
	events = Event.objects.filter(user=request.user).order_by('startTime')
	eventForm = EventForm()
	searchForm = SearchForm()
	user1 = User.objects.get(username__exact=request.user.username)
	follows = user1.followers.all()
	usersFollowing = []
	for follow in follows:
		usersFollowing.append(follow.followee)
	users = User.objects.filter(username=request.user.username)
	invitedEvents = user1.invitedUsers.all()
	context = {'invitedEvents':invitedEvents,'followingUsers':usersFollowing,'users':users,'events':events,'errors':errors,'eventForm':eventForm,'searchForm':searchForm}
	print context
	render(request,'ProfilePage.html',context)
	return redirect('/slobbbyrobbby/profilePage')

@login_required
def search(request):
	users = User.objects.filter(username=request.user.username)
	errors = []
	if request.method == "POST":
		searchForm = SearchForm(request.POST)
	else:
		searchForm = SearchForm(request.GET)
	user1 = User.objects.get(username__exact=request.user.username)
	blocks = user1.blockees.all()
	blockedBy = []
	for block in blocks:
	 	blockedBy.append(block.blocker)
	if not searchForm.is_valid():
		return render(request,'SearchResults.html',{'users':users,'searchForm':searchForm,'blockedBy':blockedBy})
	events = Event.objects.filter(location__icontains=searchForm.cleaned_data['searchfield']).exclude(user__in = blockedBy).order_by('startTime')
	searchForm = SearchForm()
	return render(request,'SearchResults.html',{'users':users,'events':events,'errors':errors,'searchForm':searchForm,'blockedBy':blockedBy})

def upload_image(request):
	if request.method == "POST":
		changePictureForm = PictureForm(request.POST,request.FILES)
	else:
		changePictureForm = PictureForm()
	users = User.objects.filter(username=request.user.username)
	changePasswordForm = ChangePasswordForm()
	changeEmailForm = ChangeEmailForm()
	context = {'users':users,'changePasswordForm':changePasswordForm,'changeEmailForm':changeEmailForm,'changePictureForm':changePictureForm}
	if not changePictureForm.is_valid():
		return render(request,'EditProfile.html',context)
	cur_user = User.objects.get(username__exact=request.user.username)
	try:
		new_profile = UserProfile.objects.get(user=cur_user)
	except ObjectDoesNotExist:
		new_profile = UserProfile(user=cur_user,image=changePictureForm.cleaned_data['picture'])
	new_profile.save()
	user_profile = UserProfile.objects.get(user=cur_user)
	cur_user.userprofile = user_profile
	cur_user.userprofile.image = changePictureForm.cleaned_data['picture']
	cur_user.save()
	user_profile.save()
	changePictureForm = PictureForm()
	context['changePictureForm'] = changePictureForm
	return render(request,'EditProfile.html',context)

@login_required
def get_image(request,id,userid):
	cur_user = User.objects.get(id=userid)
	profile = get_object_or_404(UserProfile,user=cur_user,id=id)
	if not profile.image:
		raise Http404
	content_type = guess_type(profile.image.name)
	return HttpResponse(profile.image,content_type=content_type)

@login_required
def invite_user(request,eventid,userid):
	event1 = Event.objects.get(id=eventid)
	user1 = User.objects.get(id=userid)
	print event1
	print event1.user
	print event1.invitedUsers.all()
	print user1.username
	event1.invitedUsers.add(user1)
	event1.save()
	return redirect('/slobbbyrobbby/profilePage')


@login_required
def changeEmail(request):
	users = User.objects.filter(username=request.user.username)
	context = {}
	errors = []
	context['errors'] = errors
	context['users'] = users
	if request.method == "POST" :
		changeEmailForm = ChangeEmailForm(request.POST)
	else:
		changeEmailForm = ChangeEmailForm()
	changePasswordForm = ChangePasswordForm()
	context['changeEmailForm'] = changeEmailForm
	context['changePasswordForm'] = changePasswordForm
	changePictureForm = PictureForm()
	context['changePictureForm'] = changePictureForm
	if not changeEmailForm.is_valid():
		return render(request,'EditProfile.html',context)
	cur_user = User.objects.get(username__exact=request.user.username)
	cur_user.email = changeEmailForm.cleaned_data['email1']
	cur_user.save()
	errors.append("Email changed")
	changeEmailForm = ChangeEmailForm()
	changePictureForm = PictureForm()
	context['changePictureForm'] = changePictureForm
	context['changeEmailForm'] = changeEmailForm
	return render(request,'EditProfile.html',context)

@login_required
def changePassword(request):
	context = {}
	errors = []
	
	users = User.objects.filter(username=request.user.username)
	context['users'] = users
	if request.method == "POST" :
		changePasswordForm = ChangePasswordForm(request.POST)
	else:
		changePasswordForm = ChangePasswordForm()
	changeEmailForm = ChangeEmailForm()
	context['changeEmailForm'] = changeEmailForm
	context['changePasswordForm'] = changePasswordForm
	changePictureForm = PictureForm()
	context['changePictureForm'] = changePictureForm
	if not changePasswordForm.is_valid():
		return render(request,'EditProfile.html',context)
	if (authenticate(username=request.user.username,password=changePasswordForm.cleaned_data['oldpassword'])):
		cur_user = User.objects.get(username__exact=request.user.username)
		cur_user.set_password(changePasswordForm.cleaned_data['password1'])
		cur_user.save()
		errors.append("Password succesfully changed")
		new_user = authenticate(username=request.user.username, \
								password=changePasswordForm.cleaned_data['password1'])
		changePasswordForm = ChangePasswordForm()
		context['changePasswordForm'] = changePasswordForm
		changePictureForm = PictureForm()
		context['changePictureForm'] = changePictureForm
		login(request,new_user)
		return render(request,'EditProfile.html',context)
	else:
		errors.append("Old Password incorrect. Try again.")
		context['errors'] = errors
		return render(request,'EditProfile.html',context)
	

@login_required
def editProfile(request):
	changePasswordForm = ChangePasswordForm()
	changeEmailForm = ChangeEmailForm()
	changePictureForm = PictureForm()
	users = User.objects.filter(username=request.user.username)
	return render(request,'EditProfile.html',{'users':users,'changePasswordForm':changePasswordForm,'changeEmailForm':changeEmailForm,'changePictureForm':changePictureForm})

def forgot_password(request):
	context = {}
	resetform = PasswordResetForm()
	context['resetform'] = resetform
	return render(request,'forgot-password.html',context)

@transaction.atomic
def reset_password(request):
	context = {}
	if request.method == "POST":
		resetform = PasswordResetForm(request.POST)
	else:
		resetform = PasswordResetForm()
	context['resetform'] = resetform
	errors = []
	if not resetform.is_valid():
		return render(request,'forgot-password.html',context)
	user = None
	try:
		user = User.objects.get(email__exact=resetform.cleaned_data['email'])
	except:
		errors.append("User with given email does not exist")
		context['errors'] = errors
		return render(request,'forgot-password.html',context)
	token = default_token_generator.make_token(user)
	email_body = """
Please click the link below to reset your password:
http://%s%s
""" % (request.get_host() + "/slobbbyrobbby", 
   reverse('confirm_reset', args=(user.username, token)))
	send_mail(subject="Verify your email address",
          message= email_body,
          from_email="charlie+devnull@cs.cmu.edu",
          recipient_list=[user.email])
	context['email'] = resetform.cleaned_data['email']
	return render(request, 'needs-reset.html', context)

@transaction.atomic
def confirm_reset(request, username, token):
	context = {}
	user = get_object_or_404(User, username=username)
	if not default_token_generator.check_token(user, token):
		raise Http404
	cur_user = User.objects.get(username__exact=username)
	if cur_user.is_active:
		resetchangeform = ResetChangePasswordForm()
		context['resetchangeform'] = resetchangeform
		context['username'] = username
		return render(request, 'reset-password.html', context)
	else:
		context['email'] = cur_user.email
		return render(request, 'needs-confirmation.html', context)


def reset_change_password(request,username):
	context = {}
	errors = []
	if request.method == "POST":
		resetchangeform = ResetChangePasswordForm(request.POST)
	else:
		resetchangeform = ResetChangePasswordForm()
	context['resetchangeform'] = resetchangeform
	context['username'] = username
	if not resetchangeform.is_valid():
		return render(request,'reset-password.html',context)
	cur_user = User.objects.get(username__exact= username)
	cur_user.set_password(resetchangeform.cleaned_data['password1'])
	cur_user.save()
	errors.append("Password succesfully changed")
	new_user = authenticate(username=request.user.username, \
							password=resetchangeform.cleaned_data['password1'])
	return render(request,'password-changed.html',{})
	

