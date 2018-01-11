def ban_request(user):
    user.prof.ban_count += 1
    if user.prof.ban_count >= 3:
        user.prof.ban_count = 0
        # Do ban