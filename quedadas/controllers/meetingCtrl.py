from quedadas.controllers import trophyCtrl


def update_stats(instance):
    stats = instance.user.prof.statistics

    trophyCtrl.check_km(stats, stats.distance, stats.distance + instance.distance)
    stats.distance += instance.distance

    trophyCtrl.check_steps(stats, stats.steps, stats.steps + instance.steps)
    stats.steps += instance.steps

    trophyCtrl.check_h(stats, stats.totalTimeMillis, stats.totalTimeMillis + instance.totalTimeMillis)
    stats.totalTimeMillis += instance.totalTimeMillis

    stats.calories += instance.calories

    trophyCtrl.check_meetings(stats, stats.meetingsCompletats, stats.meetingsCompletats + 1)
    stats.meetingsCompletats += 1

    stats.lastTracking = instance
    if stats.maxDistance < instance.distance:
        trophyCtrl.check_max_distance(stats, stats.maxDistance, instance.distance)
        stats.maxDistance = instance.distance
    if stats.maxAverageSpeed < instance.averagespeed:
        stats.maxAverageSpeed = instance.averagespeed
    if stats.maxDuration < instance.totalTimeMillis:
        stats.maxDuration = instance.totalTimeMillis
    if stats.minDistance > instance.distance or stats.minDistance == 0:
        stats.minDistance = instance.distance
    if stats.minAverageSpeed > instance.averagespeed or stats.minAverageSpeed == 0:
        stats.minAverageSpeed = instance.averagespeed
    if stats.minDuration > instance.totalTimeMillis or stats.minDuration == 0:
        stats.minDuration = instance.totalTimeMillis
    stats.save()
