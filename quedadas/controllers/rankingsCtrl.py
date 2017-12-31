def update_zone_ranking(sender, instance, **kwargs):
    zone = instance.user.prof.postal_code
    zone.distance += instance.distance
    if zone.members == 0:
       zone.average = 0
    else:
       zone.average = zone.distance/zone.members.count()
    zone.save()
