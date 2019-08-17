from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class DemoPartyUser(AbstractUser):
    BANNED = -1
    NORMAL = 0
    API_USER = 1
    MODERATOR = 2
    ADMIN = 3
    SUPERADMIN = 4

    TYPES = [
        (BANNED, "Banned"),
        (NORMAL, "Normal"),
        (API_USER, 'API User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin'),
        (SUPERADMIN, 'Jumal Lavis'),
    ]

    scene_id = models.PositiveIntegerField(blank=True, null=True)

    user_class = models.PositiveIntegerField(choices=TYPES, default=NORMAL)
    ban_reason = models.CharField(max_length=255, null=True, blank=True)
    ban_ends = models.DateTimeField(blank=True, null=True)

    def get_user_class_tuple(self):
        return next(filter(lambda x: x[0] == self.user_class, self.TYPES))

    def get_user_class_str(self):
        return next(filter(lambda x: x[0] == self.user_class, self.TYPES))[1]

    def lift_ban(self):
        self.user_class = self.NORMAL
        self.ban_reason = None
        self.ban_ends = None
        self.save()

    def set_infinite_ban(self, reason):
        self.user_class = self.BANNED
        self.ban_reason = reason
        self.ban_ends = timezone.now().replace(year=9999, month=12, day=31, hour=23, minute=59, second=59,
                                               microsecond=999999)
        self.save()

    def __str__(self):
        return self.username
