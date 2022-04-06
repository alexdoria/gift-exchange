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
            return render(request, 'login.html', {'error': 'Check username or password'})
    
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def user_dashboard(request):
    """Lists groups and gifts for the logged-in user"""
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

    return render(request, 'dashboard.html',
                  {
                      'user': user,
                      'groups': groups,
                  }
                  )


@login_required(login_url='login')
def gifts_view(request):
    """List, create and edit gifts"""
    gift_query = Gift.objects.filter(user=request.user)
    gifts_lists = []

    for present in gift_query:
        gift_dict = {}
        this_gift_groups_list = []
        
        gift_dict['shortname'] = present.short_name
        gift_dict['description'] = present.description

        this_gift_groups = Group.objects.filter(gift__id=present.id)
        # print(this_gift_groups)
        for group in this_gift_groups:
            this_gift_groups_list.append(group)

        gift_dict['groups'] = this_gift_groups_list
        gifts_lists.append(gift_dict)

    return render(request, 'gifts.html',
                  {
                      'gifts': gifts_lists,
                  }
                  )
        