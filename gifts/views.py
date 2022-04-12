from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from gifts.models import Gift


# Create your views here.
@login_required(login_url='login')
def gifts_view(request):
    """List, create and edit gifts"""
    if request.method == 'POST':
        short_name = request.POST['short_name']
        description = request.POST['description']
        url = request.POST['url']
        Gift.objects.create(user=request.user, short_name=short_name, description=description, link=url)

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

    return render(request, 'gifts.html', {'gifts': gifts_lists})
        