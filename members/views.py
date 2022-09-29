from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from gifts.models import Gift
from .models import Member, Club
import random


# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
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
    """Lists clubs and gifts for the logged-in user"""

    member = Member.objects.get(user=request.user)

    if request.method == 'POST':
        club_name = request.POST['club_name']
        x = Club.objects.create(name=club_name, club_admin=member)
        member.clubs.add(x)

    user_clubs = member.clubs.all()

    clubs = []

    for g in user_clubs:
        members = Member.objects.filter(clubs=g)
        club_item = {}
        members_list = []

        for m in members:
            members_dict = {}
            owner_list = []

            gifts_list = Gift.objects.filter(user=m, clubs=g)
            for gift in gifts_list:
                owner_list.append(gift)

            members_dict['name'] = m.user.username
            members_dict['list'] = owner_list
            members_list.append(members_dict)

        club_item['name'] = g.name
        club_item['id'] = g.id
        club_item['members'] = members_list
        club_item['admin'] = g.club_admin.user
        club_item['matches'] = g.match
        clubs.append(club_item)

    clubs_to_join = member.invited_to.all()

    return render(request, 'members/dashboard.html',
                  {
                      'clubs': clubs,
                      'clubs_to_join': clubs_to_join,
                  }
                  )


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
def delete_club(request):
    if request.method == 'POST':
        g_id = request.POST['object_id']
        obj = Club.objects.get(id=g_id)
        obj.delete()

    return redirect('dashboard')


@login_required(login_url='login')
def invite_members(request):
    if request.method == 'GET':
        club = request.GET['club']

        return render(request, 'members/invite-members.html', {'club': club})

    if request.method == 'POST':
        g_id = request.POST['object_id']
        club = Club.objects.get(id=g_id)
        invited_members_emails = request.POST.getlist('invite_email')

        for email in invited_members_emails:
            if not email:
                pass
            else:
                member = Member.objects.get(user__email=email)
                member.invited_to.add(club)

        send_mail(
            request.user.username + ' wants you to join ' + club + ' group', # Subject
            'Hello, you have been invited to a gift exchange with your friends', # Mail body
            'gxch.mailer@digitalnoreste.com', # Sender
            invited_members_emails, # Recipients
            fail_silently = False, #Show the error when it occurs
            )

        return redirect('dashboard')


@login_required(login_url='login')
def accept_invitation(request):
    if request.method == 'POST':
        accepted_club_id = request.POST['accepted_club']
        accepted_club = Club.objects.get(id=accepted_club_id)
        print(accepted_club)
        member = Member.objects.get(user=request.user)
        member.clubs.add(accepted_club)
        member.invited_to.remove(accepted_club)

    return redirect('dashboard')


@login_required(login_url='login')
def sort_exchange(request):
    if request.method == 'GET':
        club = request.GET['club']

        return render(request, 'members/sort-exchange.html', {'club': club})

    if request.method == 'POST':
        club_id = request.POST['object_id']
        club = Club.objects.get(id=club_id)
        members = club.member_set.all()

        members_ids = []

        for member in members:
            members_ids.append(member.pk)

        random.shuffle(members_ids)
        match = {}

        for i in range(len(members_ids)):
            from_member = Member.objects.get(id=members_ids[i])
            if members_ids[i] == members_ids[-1]:
                to_member = Member.objects.get(id=members_ids[0])

            else:
                i += 1
                to_member = Member.objects.get(id=members_ids[i])

            match[from_member.user.username] = to_member.user.username

        club.match = match
        club.save()
        print(club.match)

    return redirect('dashboard')
