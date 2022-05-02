from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from gifts.models import Gift
from .models import Member


# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        print(username)
        password = request.POST['password']
        print(password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'members/login.html', {'login_error': 'Check username or password'})

    return render(request, 'members/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def user_dashboard(request):
    """Lists groups and gifts for the logged-in user"""

    if request.method == 'POST':
        group_name = request.POST['group_name']
        x = Group.objects.create(name=group_name)
        group_to_add = Group.objects.get(name=group_name)
        request.user.groups.add(group_to_add)

    user_groups = request.user.groups.all()
    groups = []

    for g in user_groups:
        members = User.objects.filter(groups=g)
        group_item = {}
        members_list = []

        for m in members:
            members_dict = {}
            owner_list = []

            gifts_list = Gift.objects.filter(user=m, groups=g)
            for gift in gifts_list:
                owner_list.append(gift)

            members_dict['name'] = m.username
            members_dict['list'] = owner_list
            members_list.append(members_dict)

        group_item['name'] = g.name
        group_item['id'] = g.id
        group_item['members'] = members_list
        groups.append(group_item)

    return render(request, 'members/dashboard.html', {'groups': groups})


def signup_view(request):
    """ New users signup """
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        create_user = User.objects.create_user(username=username, email=email, password=password)
        if create_user is not None:
            print("User " + username + " created")
            user = authenticate(request, username=username, password=password)
            login(request, user)
            Member.objects.create(user=request.user)
            return redirect('dashboard')

    return render(request, 'members/signup.html')


@login_required(login_url='login')
def delete_group(request):
    if request.method == 'POST':
        g_id = request.POST['object_id']
        obj = Group.objects.get(id=g_id)
        obj.delete()

    return redirect('dashboard')
