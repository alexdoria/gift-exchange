from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from gifts.models import Gift


# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'members/login.html', {'error': 'Check username or password'})

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

    user = request.user.username
    user_groups = request.user.groups.all()
    groups = []

    for g in user_groups:
        members = User.objects.filter(groups=g)
        group_item = {}
        members_list = []

        for m in members:
            members_dict = {}
            owner_list = []

            gifts_list = Gift.objects.filter(user=m, group=g)
            for gift in gifts_list:
                owner_list.append(gift)

            members_dict['name'] = m.first_name
            members_dict['list'] = owner_list
            members_list.append(members_dict)

        group_item['name'] = g
        group_item['members'] = members_list
        groups.append(group_item)

    return render(request, 'members/dashboard.html',
                  {
                      'user': user,
                      'groups': groups,
                  }
                  )


@login_required(login_url='login')
def new_group(request):
    """
    This view lets the user create a new group, add members to the group (send invitations)
    and accept invitations.
    """
