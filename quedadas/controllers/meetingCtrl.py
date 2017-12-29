def update_stats(sender, instance, **kwargs):
    stats = instance.user.prof.statistics
    stats.distance += instance.distance
    stats.steps += instance.steps
    stats.totalTimeMillis += instance.totalTimeMillis
    stats.calories += instance.calories
    stats.meetingsCompletats += 1
    stats.lastTracking = instance
    if stats.maxDistance < instance.distance:
        stats.maxDistance = instance.distance
    if stats.maxAverageSpeed < instance.averagespeed:
        stats.maxAverageSpeed = instance.averagespeed
    if stats.maxDuration < instance.totalTimeMillis:
        stats.maxDuration = instance.totalTimeMillis
    if stats.minDistance > instance.distance or stats.minDistance == 0:
        stats.minDistance = instance.distance
    if stats.minAverageSpeed > instance.averagespeed or stats.averagespeed == 0:
        stats.minAverageSpeed = instance.averagespeed
    if stats.minDuration > instance.totalTimeMillis or stats.totalTimeMillis == 0:
        stats.minDuration = instance.totalTimeMillis
    stats.save()
