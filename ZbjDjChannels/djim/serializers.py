def usersession_json(obj):
    return {
        'name': obj.name,
        'subIP': obj.subIP,
        'channel_name': obj.channel_name,
        'activeTime': obj.activeTime
    }


def user_list_json(obj):
    return {

        'uid': obj.uid,
        "sid": obj.session
    }