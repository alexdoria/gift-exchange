from django.shortcuts import render
from django.contrib.auth.models import User
from gifts.models import Gift


# Create your views here.
def user_dashboard(request):
    """Lists groups and gifts for the logged-in user"""
    user = User.objects.get(username='amanda')
    user_groups = user.groups.all()
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
