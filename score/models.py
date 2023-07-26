from enum import Enum
from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class User(AbstractUser):
    username = models.CharField(verbose_name="username", max_length=255, unique=True)
    email = models.CharField(verbose_name="email", max_length=255, unique=True)
    password = models.CharField(verbose_name="password", max_length=255)
    groups = models.ManyToManyField(Group)
    # username = None

    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class FamilyStatus(Enum):
    divorsed = 'divorsed'
    single = 'single'
    married = 'married'
    widowed = 'widowed'
    separated = 'separated'


class Branch(Enum):
    n_shouna = 'n_shouna'
    dayr_alla = 'dayr_alla'
    koura_branch = 'koura_branch'
    zarqa = 'zarqa'
    hussein = 'hussein'
    rsaifeh_branch = 'rsaifeh_branch'
    beni_kenana_branch = 'beni_kenana_branch'
    irbid = 'irbid'
    salt_branch = 'salt_branch'
    sahab = 'sahab'
    hitteen = 'hitteen'
    marka_branch = 'marka_branch'
    jerash = 'jerash'
    madaba = 'madaba'
    biader_office = 'biader_office'
    al_karak_branch = 'al_karak_branch'


class ScoreModel(models.Model):
    FAMILY_STATUS_CHOICES = [(tag.value, tag.name.capitalize()) for tag in FamilyStatus]
    BRANCH_CHOICES = [(tag.value, tag.name.capitalize()) for tag in Branch]

    family_status = models.CharField(max_length=10, choices=FAMILY_STATUS_CHOICES)
    branch = models.CharField(max_length=30, choices=BRANCH_CHOICES)
    prior_loans = models.PositiveIntegerField(
        verbose_name="Prior Loans",
        validators=[MinValueValidator(1), MaxValueValidator(15)]
    )
    loan_duration = models.PositiveIntegerField(
        verbose_name="Loan Duration",
        validators=[MinValueValidator(6), MaxValueValidator(128)]
    )
    total_income = models.FloatField(
        verbose_name="Total Income",
        validators=[MinValueValidator(-3730.0), MaxValueValidator(50000.0)]
    )
    interest_rate_monthly = models.FloatField(
        verbose_name="Interest Rate Monthly",
        validators=[MinValueValidator(0.22), MaxValueValidator(0.42)]
    )
    gender = models.PositiveIntegerField(
        verbose_name="Gender",
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )
    age = models.PositiveIntegerField(
        verbose_name="Age",
        validators=[MinValueValidator(18), MaxValueValidator(70)]
    )
    loan_amount = models.FloatField(
        verbose_name="Loan Amount",
        validators=[MinValueValidator(300.0), MaxValueValidator(8000.0)]
    )
    co_borrower = models.FloatField(
        verbose_name="Co-borrower",
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )
    inflation_rate = models.FloatField(
        verbose_name="Inflation Rate",
        validators=[MinValueValidator(-0.567), MaxValueValidator(5.393)]
    )
