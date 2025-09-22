# from django.contrib import admin

# from .models import Location, Haunting, Hauntingtype

# admin.site.register(Location)
# admin.site.register(Haunting)
# admin.site.register(Hauntingtype)


# admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import *


admin.site.register(Location)
admin.site.register(Haunting)
admin.site.register(Hauntingtype)
admin.site.register(Contributor)

@admin.register(HauntedStory)
class HauntedStoryAdmin(admin.ModelAdmin):
	list_display = [
		'title', 
		'display_author', 
		'submitted_at', 
		'approved', 
		'featured',
		'coordinate_link',
		'story_preview'
	]
	
	list_filter = [
		'approved', 
		'featured', 
		'submitted_at',
		('date_occurred', admin.DateFieldListFilter),
	]
	
	search_fields = [
		'title', 
		'author', 
		'story',
		'submitter_email'
	]
	
	readonly_fields = [
		'submitted_at', 
		'coordinate_string',
		'map_preview'
	]
	
	fieldsets = (
		('Story Information', {
			'fields': ('title', 'story', 'author', 'date_occurred')
		}),
		('Location', {
			'fields': ('latitude', 'longitude', 'coordinate_string', 'map_preview'),
			'description': 'Location where the haunting occurred'
		}),
		('Submission Details', {
			'fields': ('submitter_email', 'submitted_at'),
			'classes': ('collapse',)
		}),
		('Status', {
			'fields': ('approved', 'featured'),
			'description': 'Approved stories appear on the public map. Featured stories appear prominently.'
		}),
	)
	
	actions = ['approve_stories', 'unapprove_stories', 'feature_stories', 'unfeature_stories']
	
	def display_author(self, obj):
		return obj.display_author
	display_author.short_description = 'Author'
	
	def story_preview(self, obj):
		preview = obj.story[:100] + '...' if len(obj.story) > 100 else obj.story
		return preview
	story_preview.short_description = 'Story Preview'
	
	# def coordinate_link(self, obj):
	# 	"""Display coordinates with link to Google Maps"""
	# 	if obj.latitude and obj.longitude:
	# 		google_maps_url = f"https://www.google.com/maps?q={obj.latitude},{obj.longitude}"
	# 		return format_html(
	# 			'<a href="{}" target="_blank">{:.4f}, {:.4f}</a>',
	# 			google_maps_url,
	# 			obj.latitude,
	# 			obj.longitude
	# 		)
	# 	return "No coordinates"

	def coordinate_link(self, obj):
		"""Display coordinates with link to Google Maps"""
		if obj.latitude and obj.longitude:
			# CORRECT: Construct the URL using a regular f-string first.
			google_maps_url = "https://www.google.com/maps/search/?api=1&query={obj.latitude},{obj.longitude}"
			
			return (google_maps_url)

			# return format_html(
			# 	'<a href="{}" target="_blank">{:.4f}, {:.4f}</a>',
			# 	google_maps_url,
			# 	obj.latitude,
			# 	obj.longitude
			# )
		return "No coordinates"

	coordinate_link.short_description = 'Location'
	coordinate_link.admin_order_field = 'latitude'
	
	def map_preview(self, obj):
		"""Display a small map preview in admin"""
		if obj.latitude and obj.longitude:
			# Using OpenStreetMap static map alternative or simple link
			osm_url = f"https://www.openstreetmap.org/?mlat={obj.latitude}&mlon={obj.longitude}#map=16/{obj.latitude}/{obj.longitude}"
			return format_html(
				'''
				<div style="margin: 10px 0;">
					<a href="{}" target="_blank" style="text-decoration: none;">
						<div style="width: 200px; height: 150px; border: 2px solid #ccc; 
								   display: flex; align-items: center; justify-content: center; 
								   background: #f5f5f5; border-radius: 5px;">
							<div style="text-align: center;">
								<div style="font-size: 24px;">📍</div>
								<div style="font-size: 12px; color: #666;">
									{:.4f}, {:.4f}<br>
									Click to view on map
								</div>
							</div>
						</div>
					</a>
				</div>
				''',
				osm_url,
				obj.latitude,
				obj.longitude
			)
		return "No location selected"
	map_preview.short_description = 'Map Preview'
	
	def approve_stories(self, request, queryset):
		updated = queryset.update(approved=True)
		self.message_user(
			request, 
			f'{updated} story(s) were approved and will now appear on the public map.'
		)
	approve_stories.short_description = "Approve selected stories"
	
	def unapprove_stories(self, request, queryset):
		updated = queryset.update(approved=False)
		self.message_user(
			request, 
			f'{updated} story(s) were unapproved and removed from the public map.'
		)
	unapprove_stories.short_description = "Unapprove selected stories"
	
	def feature_stories(self, request, queryset):
		updated = queryset.update(featured=True, approved=True)
		self.message_user(
			request, 
			f'{updated} story(s) were featured (and approved if not already).'
		)
	feature_stories.short_description = "Feature selected stories"
	
	def unfeature_stories(self, request, queryset):
		updated = queryset.update(featured=False)
		self.message_user(
			request, 
			f'{updated} story(s) were unfeatured.'
		)
	unfeature_stories.short_description = "Unfeature selected stories"
	
	def get_queryset(self, request):
		# Show newest submissions first by default
		return super().get_queryset(request).order_by('-submitted_at')
	
	# Custom admin view styling
	class Media:
		css = {
			'all': ('admin/css/haunted_admin.css',)
		}
		js = ('admin/js/haunted_admin.js',)


# @admin.register(HauntingCategory)
# class HauntingCategoryAdmin(admin.ModelAdmin):
#     list_display = ['name', 'icon', 'description']
#     search_fields = ['name', 'description']


# Customize admin site header and title
admin.site.site_header = "👻 Haunted Lawrence Admin"
admin.site.site_title = "Haunted Lawrence"
admin.site.index_title = "Manage Haunted Stories"