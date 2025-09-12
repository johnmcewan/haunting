from django.db import models

class Location(models.Model):
	id_location = models.AutoField(primary_key=True)
	location_name = models.TextField(blank=True, null=True)
	location_street = models.TextField(blank=True, null=True)
	location_housenumber = models.IntegerField(blank=True, null=True)
	location_houseletter = models.TextField(blank=True, null=True)
	longitude = models.FloatField(blank=True, null=True)
	latitude = models.FloatField(blank=True, null=True)
	location_notes = models.TextField(blank=True, null=True)
	location_photo = models.TextField(blank=True, null=True)

	def __str__(self): 
		return self.location_name or ''

	class Meta:
		managed = True
		db_table = 'location'

class Haunting(models.Model):
	id_haunting = models.AutoField(primary_key=True)
	haunting_name = models.TextField(blank=True, null=True)
	haunting_booktext = models.TextField(blank=True, null=True)
	haunting_pagestart = models.IntegerField(blank=True, null=True)
	haunting_pageend = models.IntegerField(blank=True, null=True)
	haunting_storyabstract = models.TextField(blank=True, null=True)
	haunting_storyshort = models.TextField(blank=True, null=True)
	fk_location = models.ForeignKey('Location', models.DO_NOTHING, related_name="fk_location", db_column='fk_location', blank=True, null=True)
	fk_hauntingtype = models.ForeignKey('Hauntingtype', models.DO_NOTHING, related_name="fk_hauntingtype", db_column='fk_hauntingtype', blank=True, null=True)

	def __str__(self): 
		return self.haunting_name or ''

	class Meta:
		managed = True
		db_table = 'haunting'


class Hauntingtype(models.Model):
	id_hauntingtype = models.AutoField(primary_key=True)
	hauntingtype = models.TextField(blank=True, null=True) 

	def __str__(self): 
		return self.hauntingtype or ''

	class Meta:
		managed = True
		db_table = 'hauntingtype'
