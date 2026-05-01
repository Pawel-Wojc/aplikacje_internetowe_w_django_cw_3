from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import get_user_model
from .models import Channel

User = get_user_model()


@login_required
def chat_home(request):
    mode = request.GET.get('mode', 'groups')

    if mode == 'dm':
        dm_threads = Channel.objects.filter(
            channel_type='private',
            members=request.user
        ).prefetch_related('members')
        channels = []
        available_channels = []
        active_channel = dm_threads.first()

        if active_channel:
            other_user = active_channel.members.exclude(id=request.user.id).first()
            active_title = other_user.username if other_user else 'Wybierz rozmowę'
        else:
            active_title = 'Wybierz rozmowę'

    else:
        channels = Channel.objects.filter(
            channel_type='public',
            members=request.user
        ).prefetch_related('members')

        available_channels = Channel.objects.filter(
            channel_type='public'
        ).exclude(
            members=request.user
        )

        dm_threads = []
        active_channel = channels.first()
        active_title = active_channel.name if active_channel else 'Wybierz kanał'

    messages = active_channel.messages.select_related('author').all().order_by('created_at') if active_channel else []
    members = active_channel.members.all() if active_channel else []

    context = {
        'mode': mode,
        'channels': channels,
        'available_channels': available_channels,
        'dm_threads': dm_threads,
        'active_channel': active_channel,
        'active_title': active_title,
        'messages': messages,
        'members': members,
        'all_users': User.objects.exclude(id=request.user.id),
    }
    return render(request, 'chat/chat.html', context)


@login_required
def start_dm(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    if other_user == request.user:
        return redirect('chat_home')

    ids = sorted([request.user.id, other_user.id])
    room_name = f"dm_{ids[0]}_{ids[1]}"

    channel, created = Channel.objects.get_or_create(
        name=room_name,
        channel_type='private',
        defaults={'created_by': request.user}
    )

    if created:
        channel.members.add(request.user, other_user)
    else:
        if request.user not in channel.members.all():
            channel.members.add(request.user)
        if other_user not in channel.members.all():
            channel.members.add(other_user)

    return redirect('channel_room', channel_id=channel.id)


@login_required
def channel_room(request, channel_id):
    active_channel = get_object_or_404(Channel, id=channel_id, members=request.user)

    if active_channel.channel_type == 'private':
        mode = 'dm'
        other_user = active_channel.members.exclude(id=request.user.id).first()
        active_title = other_user.username if other_user else "DM"

        dm_threads = Channel.objects.filter(
            channel_type='private',
            members=request.user
        ).prefetch_related('members')
        channels = []
    else:
        mode = 'groups'
        active_title = active_channel.name
        channels = Channel.objects.filter(
            channel_type='public',
            members=request.user
        ).prefetch_related('members')
        dm_threads = []

    messages = active_channel.messages.select_related('author').all().order_by('created_at')
    members = active_channel.members.all()

    context = {
        'mode': mode,
        'channels': channels,
        'dm_threads': dm_threads,
        'active_channel': active_channel,
        'active_title': active_title,
        'messages': messages,
        'members': members,
        'all_users': User.objects.exclude(id=request.user.id),
    }
    return render(request, 'chat/chat.html', context)


@login_required
def join_channel(request, channel_id):
    channel = get_object_or_404(Channel, id=channel_id, channel_type='public')

    channel.members.add(request.user)

    return redirect('channel_room', channel_id=channel.id)