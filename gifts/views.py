from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from gifts.models import Gift
from members.models import Member, Club


# Create your views here.
@login_required(login_url='login')
def gifts_view(request):
    """List, create and edit gifts"""
    member = Member.objects.get(user=request.user)

    if request.method == 'POST':
        short_name = request.POST['short_name']
        description = request.POST['description']
        url = request.POST['url']
        Gift.objects.create(user=member, short_name=short_name, description=description, link=url)

    gift_query = Gift.objects.filter(user=member)
    gifts_lists = []

    for present in gift_query:
        gift_dict = {}
        this_gift_groups_list = []

        gift_dict['id'] = present.id
        gift_dict['shortname'] = present.short_name
        gift_dict['description'] = present.description

        this_gift_groups = Club.objects.filter(gift__id=present.id)
        # print(this_gift_groups)
        for group in this_gift_groups:
            this_gift_groups_list.append(group)

        gift_dict['groups'] = this_gift_groups_list
        gifts_lists.append(gift_dict)

    user_groups = Club.objects.filter(member=member)

    return render(request, 'gifts.html',
                  {
                      'gifts': gifts_lists,
                      'user_groups': user_groups,
                  })


@login_required(login_url='login')
def delete_gift(request):
    if request.method == 'POST':
        g_id = request.POST['object_id']
        obj = Gift.objects.get(id=g_id)
        obj.delete()

    return redirect('gifts')


@login_required(login_url='login')
def set_gift_groups(request):
    if request.method == 'POST':
        gift_id = request.POST['gift_id']
        clubs_id_list = request.POST.getlist('user_clubs_list')
        this_gift = Gift.objects.get(id=gift_id)

        for g in clubs_id_list:
            this_gift.clubs.add(g)

    return redirect('gifts')
