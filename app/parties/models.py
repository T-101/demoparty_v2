from django.db import models
from django.template.defaultfilters import slugify

from authentication.models import DemoPartyUser


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class DemoPartyLocation(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    address_extra = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    latitude = models.DecimalField(
        max_digits=32, decimal_places=29, blank=True, null=True)
    longitude = models.DecimalField(
        max_digits=32, decimal_places=29, blank=True, null=True)

    def __str__(self):
        return f"{self.name}, {self.city}, {self.country}"


class DemoPartyExternalURL(models.Model):
    url = models.URLField()

    def __str__(self):
        return self.url


class DemoPartySeries(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Demo Party series"

    def __str__(self):
        return self.name


class DemoParty(TimeStampModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True)
    series = models.ForeignKey(DemoPartySeries, on_delete=models.CASCADE, related_name='parties')

    location = models.ForeignKey(
        DemoPartyLocation, on_delete=models.CASCADE, related_name='demo_parties', blank=True, null=True)
    url = models.URLField()
    external_urls = models.ManyToManyField(DemoPartyExternalURL, related_name='demo_parties')

    demo_party_start = models.DateField()
    demo_party_end = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.demo_party_start.year})"

    def save(self, *args, **kwargs):
        # TODO strip year from party name if matches with demo_party_start.year
        if not self.demo_party_end:
            self.demo_party_end = self.demo_party_start
        if not self.slug:
            slug = slugify('%s %s' % (self.name, self.demo_party_start.year))
            self.slug = re.sub(r'-(\d{4})(?=.+\1)', '', slug)

        return super().save(*args, **kwargs)


class DemoPartyVisitor(models.Model):
    NOT_GOING = 0
    PLANNING = 1
    WENT = 2

    CHOICES = [
        (NOT_GOING, "Not going"),
        (PLANNING, "Planning"),
        (WENT, "Went")
    ]

    user = models.OneToOneField(DemoPartyUser, on_delete=models.CASCADE)
    demo_party = models.ForeignKey(DemoParty, on_delete=models.CASCADE, related_name='visitors')
    status = models.IntegerField(choices=CHOICES, default=PLANNING)

    def __str__(self):
        return f"{self.user.username} at {self.demo_party.name}"
