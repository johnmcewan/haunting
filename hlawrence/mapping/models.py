from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Contributor(models.Model):
	id_contributor = models.AutoField(primary_key=True)
	contributor_firstname = models.TextField(blank=True, null=True)
	contributor_secondname = models.TextField(blank=True, null=True)
	contributor_notes = models.TextField(blank=True, null=True)
	contributor_active = models.TextField(blank=True, null=True)
	contributor_photograph = models.TextField(blank=True, null=True)

	def __str__(self): 
		return self.contributor_secondname or ''

	class Meta:
		managed = True
		db_table = 'contributor'


class Haunting(models.Model):
	id_haunting = models.AutoField(primary_key=True)
	haunting_name = models.TextField(blank=True, null=True)
	haunting_physicaldetails = models.TextField(blank=True, null=True)
	haunting_deathstory =models.TextField(blank=True, null=True)
	haunting_discoveryofhaunting = models.TextField(blank=True, null=True)
	haunting_behavior = models.TextField(blank=True, null=True)
	haunting_timeline = models.TextField(blank=True, null=True)
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


class Location(models.Model):
	id_location = models.AutoField(primary_key=True)
	location_name = models.TextField(blank=True, null=True)
	location_namecurrent = models.TextField(blank=True, null=True)
	location_nameformer = models.TextField(blank=True, null=True)
	location_street = models.TextField(blank=True, null=True)
	location_housenumber = models.IntegerField(blank=True, null=True)
	location_houseletter = models.TextField(blank=True, null=True)
	longitude = models.FloatField(blank=True, null=True)
	latitude = models.FloatField(blank=True, null=True)
	location_history = models.TextField(blank=True, null=True)
	location_notes = models.TextField(blank=True, null=True)
	location_photo = models.TextField(blank=True, null=True)

	def __str__(self): 
		return self.location_name or ''

	class Meta:
		managed = True
		db_table = 'location'



class HauntedStory(models.Model):
    title = models.CharField(max_length=200, help_text="Title of your haunting story")
    story = models.TextField(help_text="Detailed description of your paranormal experience")
    author = models.CharField(max_length=100, blank=True, null=True, help_text="Your name (optional)")
    
    # Location coordinates
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6,
        validators=[
            MinValueValidator(38.9),  # Southern boundary of Lawrence area
            MaxValueValidator(39.1)   # Northern boundary of Lawrence area
        ],
        help_text="Latitude coordinate of the haunting location"
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6,
        validators=[
            MinValueValidator(-95.4),  # Western boundary of Lawrence area
            MaxValueValidator(-95.1)   # Eastern boundary of Lawrence area
        ],
        help_text="Longitude coordinate of the haunting location"
    )
    
    # Optional date when the experience occurred
    date_occurred = models.DateField(blank=True, null=True, help_text="When did this haunting occur?")
    
    # Submission tracking
    submitted_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False, help_text="Admin approval for public display")
    featured = models.BooleanField(default=False, help_text="Featured story")
    
    # Contact info (not displayed publicly)
    submitter_email = models.EmailField(blank=True, null=True, help_text="Contact email (not displayed publicly)")
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Haunted Story"
        verbose_name_plural = "Haunted Stories"
    
    def __str__(self):
        return f"{self.title} ({self.submitted_at.strftime('%Y-%m-%d')})"
    
    @property
    def display_author(self):
        """Return author name or 'Anonymous' if no author provided"""
        return self.author if self.author else "Anonymous"
    
    @property
    def coordinate_string(self):
        """Return formatted coordinate string"""
        return f"{self.latitude}, {self.longitude}"
    
    def get_geojson_feature(self):
        """Return GeoJSON feature representation"""
        return {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(self.longitude), float(self.latitude)]
            },
            "properties": {
                "title": self.title,
                "author": self.display_author,
                "story": self.story,
                "date_occurred": self.date_occurred.isoformat() if self.date_occurred else None,
                "submitted_at": self.submitted_at.isoformat(),
                "featured": self.featured,
                "popupContent": f"""
                    <div class="story-popup">
                        <h4>{self.title}</h4>
                        <p><strong>By:</strong> {self.display_author}</p>
                        {f'<p><strong>Date:</strong> {self.date_occurred.strftime("%B %d, %Y")}</p>' if self.date_occurred else ''}
                        <p class="story-preview">{self.story[:200]}{'...' if len(self.story) > 200 else ''}</p>
                        <small>Submitted: {self.submitted_at.strftime('%B %d, %Y')}</small>
                    </div>
                """
            }
        }


# # Additional model for categorizing types of hauntings (optional)
# class HauntingCategory(models.Model):
#     name = models.CharField(max_length=100)
#     icon = models.CharField(max_length=10, help_text="Emoji or icon for this category")
#     description = models.TextField(blank=True)
    
#     class Meta:
#         verbose_name_plural = "Haunting Categories"
    
#     def __str__(self):
#         return self.name


# You can add this field to HauntedStory if you want categories
# category = models.ForeignKey(HauntingCategory, on_delete=models.SET_NULL, null=True, blank=True)