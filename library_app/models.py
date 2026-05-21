# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Author(models.Model):
    id_author = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=200)
    biography = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'author'


class Book(models.Model):
    id_book = models.AutoField(primary_key=True)
    title = models.CharField(max_length=300)
    isbn = models.CharField(unique=True, max_length=20, blank=True, null=True)
    id_publisher = models.ForeignKey('Publisher', models.RESTRICT, db_column='id_publisher')
    id_author = models.ForeignKey(Author, models.RESTRICT, db_column='id_author')
    id_genre = models.ForeignKey('Genre', models.RESTRICT, db_column='id_genre')

    class Meta:
        managed = False
        db_table = 'book'


class Copy(models.Model):
    STATUS_CHOICES = (
        ('available', 'Доступна'),
        ('issued', 'Выдана'),
        ('lost' , 'Потеряна'),
        ('repair' , 'Ремонт'),
    )
    id_copy = models.AutoField(primary_key=True)
    id_book = models.ForeignKey(Book, models.CASCADE, db_column='id_book')
    status = models.CharField(max_length=20, default='available', choices=STATUS_CHOICES)

    class Meta:
        managed = False
        db_table = 'copy'


class Genre(models.Model):
    id_genre = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'genre'


class Loan(models.Model):
    id_loan = models.AutoField(primary_key=True)
    id_reader = models.ForeignKey('Reader', models.CASCADE, db_column='id_reader')
    id_copy = models.ForeignKey(Copy, models.CASCADE, db_column='id_copy')
    issue_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)
    fine = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'loan'


class Publisher(models.Model):
    id_publisher = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'publisher'


class Reader(models.Model):
    id_reader = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(unique=True, max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reader'
