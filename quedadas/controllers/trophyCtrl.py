from rest_framework import serializers

from quedadas.controllers import firebaseCtrl


class TrophySerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    km_1 = serializers.SerializerMethodField()
    km_10 = serializers.SerializerMethodField()
    km_100 = serializers.SerializerMethodField()
    km_1000 = serializers.SerializerMethodField()
    h_1 = serializers.SerializerMethodField()
    h_10 = serializers.SerializerMethodField()
    h_100 = serializers.SerializerMethodField()
    h_1000 = serializers.SerializerMethodField()
    meetings_1 = serializers.SerializerMethodField()
    meetings_5 = serializers.SerializerMethodField()
    meetings_10 = serializers.SerializerMethodField()
    meetings_20 = serializers.SerializerMethodField()
    meetings_50 = serializers.SerializerMethodField()
    level_1 = serializers.SerializerMethodField()
    level_5 = serializers.SerializerMethodField()
    level_10 = serializers.SerializerMethodField()
    level_25 = serializers.SerializerMethodField()
    level_40 = serializers.SerializerMethodField()
    level_50 = serializers.SerializerMethodField()
    max_distance_1 = serializers.SerializerMethodField()
    max_distance_5 = serializers.SerializerMethodField()
    max_distance_10 = serializers.SerializerMethodField()
    max_distance_21 = serializers.SerializerMethodField()
    max_distance_42 = serializers.SerializerMethodField()
    steps_10000 = serializers.SerializerMethodField()
    steps_20000 = serializers.SerializerMethodField()
    steps_25000 = serializers.SerializerMethodField()
    steps_50000 = serializers.SerializerMethodField()
    steps_100000 = serializers.SerializerMethodField()
    challenges_1 = serializers.SerializerMethodField()
    challenges_5 = serializers.SerializerMethodField()
    challenges_10 = serializers.SerializerMethodField()
    challenges_20 = serializers.SerializerMethodField()
    friends_1 = serializers.SerializerMethodField()
    friends_5 = serializers.SerializerMethodField()
    friends_10 = serializers.SerializerMethodField()
    friends_20 = serializers.SerializerMethodField()

    @staticmethod
    def get_km_1(obj):
        return obj.distance >= 1 * 1000

    @staticmethod
    def get_km_10(obj):
        return obj.distance >= 10 * 1000

    @staticmethod
    def get_km_100(obj):
        return obj.distance >= 100 * 1000

    @staticmethod
    def get_km_1000(obj):
        return obj.distance >= 1000 * 1000

    @staticmethod
    def get_h_1(obj):
        return obj.totalTimeMillis >= 1 * 1000 * 3600

    @staticmethod
    def get_h_10(obj):
        return obj.totalTimeMillis >= 10 * 1000 * 3600

    @staticmethod
    def get_h_100(obj):
        return obj.totalTimeMillis >= 100 * 1000 * 3600

    @staticmethod
    def get_h_1000(obj):
        return obj.totalTimeMillis >= 1000 * 1000 * 3600

    @staticmethod
    def get_meetings_1(obj):
        return obj.meetingsCompletats >= 1

    @staticmethod
    def get_meetings_5(obj):
        return obj.meetingsCompletats >= 5

    @staticmethod
    def get_meetings_10(obj):
        return obj.meetingsCompletats >= 10

    @staticmethod
    def get_meetings_20(obj):
        return obj.meetingsCompletats >= 20

    @staticmethod
    def get_meetings_50(obj):
        return obj.meetingsCompletats >= 50

    @staticmethod
    def get_level_1(obj):
        return obj.prof.level >= 1

    @staticmethod
    def get_level_5(obj):
        return obj.prof.level >= 5

    @staticmethod
    def get_level_10(obj):
        return obj.prof.level >= 10

    @staticmethod
    def get_level_25(obj):
        return obj.prof.level >= 25

    @staticmethod
    def get_level_40(obj):
        return obj.prof.level >= 40

    @staticmethod
    def get_level_50(obj):
        return obj.prof.level >= 50

    @staticmethod
    def get_max_distance_1(obj):
        return obj.maxDistance >= 1 * 1000

    @staticmethod
    def get_max_distance_5(obj):
        return obj.maxDistance >= 5 * 1000

    @staticmethod
    def get_max_distance_10(obj):
        return obj.maxDistance >= 10 * 1000

    @staticmethod
    def get_max_distance_21(obj):
        return obj.maxDistance >= 21 * 1000

    @staticmethod
    def get_max_distance_42(obj):
        return obj.maxDistance >= 42 * 1000

    @staticmethod
    def get_steps_10000(obj):
        return obj.steps >= 10000

    @staticmethod
    def get_steps_20000(obj):
        return obj.steps >= 20000

    @staticmethod
    def get_steps_25000(obj):
        return obj.steps >= 25000

    @staticmethod
    def get_steps_50000(obj):
        return obj.steps >= 50000

    @staticmethod
    def get_steps_100000(obj):
        return obj.steps >= 100000

    @staticmethod
    def get_challenges_1(obj):
        return obj.challenges >= 1

    @staticmethod
    def get_challenges_5(obj):
        return obj.challenges >= 5

    @staticmethod
    def get_challenges_10(obj):
        return obj.challenges >= 10

    @staticmethod
    def get_challenges_20(obj):
        return obj.challenges >= 20

    @staticmethod
    def get_friends_1(obj):
        return obj.prof.friend_number >= 1

    @staticmethod
    def get_friends_5(obj):
        return obj.prof.friend_number >= 5

    @staticmethod
    def get_friends_10(obj):
        return obj.prof.friend_number >= 10

    @staticmethod
    def get_friends_20(obj):
        return obj.prof.friend_number >= 20


def check_km(stats, old, new):
    check(stats, old, new, "km", [1, 10, 100, 1000])


def check_h(stats, old, new):
    check(stats, old / (3600 * 1000), new / (3600 * 1000), "h", [1, 10, 100, 1000])


def check_meetings(stats, old, new):
    check(stats, old, new, "meetings", [1, 5, 10, 20, 50])


def check_level(stats, old, new):
    check(stats, old, new, "level", [1, 5, 10, 20, 25, 40, 50])


def check_max_distance(stats, old, new):
    check(stats, old, new, "max_distance", [1, 5, 10, 21, 42])


def check_steps(stats, old, new):
    check(stats, old, new, "steps", [10000, 20000, 25000, 50000, 100000])


def check_challenges(stats, old, new):
    check(stats, old, new, "challenges", [1, 5, 10, 20])


def check_friends(user):
    friends = user.prof.friend_number
    check(user.prof.statistics, friends - 1, friends, "friends", [1, 5, 10, 20])


def check(stats, old, new, prefix, values):
    for treshold in values:
        if old < treshold and new >= treshold:
            firebaseCtrl.trophy_obtained(stats, prefix + '_' + str(treshold))
