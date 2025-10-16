# views.py
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from utils.viewtools import *
from .models import HauntedStory
from .forms import StorySubmissionForm
import json


def index(request):
	"""About page"""
	# Get some statistics
	total_stories = HauntedStory.objects.filter(approved=True).count()
	recent_stories = HauntedStory.objects.filter(approved=True).order_by('-submitted_at')[:3]
	
	context = {
		'total_stories': total_stories,
		'recent_stories': recent_stories,
	}
	
	return render(request, 'mapping/index.html', context)

def map(request):
	# Get cases from Haunting Lawrence Book
	location_dict = locationgather()
	mapdic, center_long, center_lat = locationdata(location_dict)
	
	# Get approved haunted stories and convert to GeoJSON
	approved_stories = HauntedStory.objects.filter(approved=True)
	story_geojson = {
		"type": "FeatureCollection",
		"features": [story.get_geojson_feature() for story in approved_stories]
	}
		
	template = loader.get_template('mapping/map.html')
	context = {
		'locationdata': mapdic,
		'locationdata_user': story_geojson,
		'story_count': approved_stories.count(),
	}
	
	return HttpResponse(template.render(context, request))


def submitstory(request):
	"""Story submission page with interactive map"""
	if request.method == 'POST':
		form = StorySubmissionForm(request.POST)
		if form.is_valid():
			print (form)
			story = form.save()
			
			# Send notification email to admin (optional)
			try:
				send_notification_email(story)
			except Exception as e:
				# Log error but don't fail the submission
				print(f"Failed to send notification email: {e}")
			
			# Success message
			messages.success(
				request, 
				f'🎭 Your haunting tale "{story.title}" has been submitted! '
				'It will be reviewed and added to the map soon.'
			)
			
			# Redirect to prevent resubmission
			return redirect('/story')
		else:

			# Form has errors - they will be displayed in the template
			messages.error(
				request,
				'👻 There were some issues with your submission. '
				'Please check the errors below and try again.'
			)
	else:
		form = StorySubmissionForm()
	
	# Get existing approved stories for map display
	existing_stories = HauntedStory.objects.filter(approved=True)
	existing_locations = []
	
	for story in existing_stories:
		existing_locations.append({
			'lat': float(story.latitude),
			'lng': float(story.longitude),
			'title': story.title,
			'author': story.display_author
		})
	
	context = {
		'form': form,
		'existing_locations': json.dumps(existing_locations),
	}
	
	return render(request, 'mapping/submitstory.html', context)


def send_notification_email(story):
	"""Send email notification when new story is submitted"""
	if hasattr(settings, 'ADMINS') and settings.ADMINS:
		admin_emails = [admin[1] for admin in settings.ADMINS]
		
		subject = f'New Haunted Story Submitted: {story.title}'
		message = f"""
A new haunted story has been submitted to Haunted Lawrence:

Title: {story.title}
Author: {story.display_author}
Location: {story.coordinate_string}
Submitted: {story.submitted_at.strftime('%B %d, %Y at %I:%M %p')}

Story Preview:
{story.story[:500]}{'...' if len(story.story) > 500 else ''}

Please review and approve this story in the admin panel.
		"""
		
		send_mail(
			subject,
			message,
			settings.DEFAULT_FROM_EMAIL,
			admin_emails,
			fail_silently=False,
		)


def get_haunting_json(request):
	"""API endpoint to get approved stories as JSON"""
	approved_stories = HauntedStory.objects.filter(approved=True)
	
	geojson = {
		"type": "FeatureCollection",
		"features": [story.get_geojson_feature() for story in approved_stories]
	}
	
	return JsonResponse(geojson)


def haunting_detail(request, story_id):
	"""View individual story details"""
	try:
		story = Haunting.objects.get(id_haunting=story_id)
	except Haunting.DoesNotExist:
		messages.error(request, "Story not found.")
		return redirect('index')
	
	# # Get nearby stories (within ~1km)
	# lat_range = 0.01  # Approximately 1km
	# lng_range = 0.01
	
	# nearby_stories = HauntedStory.objects.filter(
	# 	latitude__range=(float(story.latitude) - lat_range, float(story.latitude) + lat_range),
	# 	longitude__range=(float(story.longitude) - lng_range, float(story.longitude) + lng_range)
	# ).exclude(id=story.id)[:5]
	
	context = {
		'haunting': story,
		# 'nearby_stories': nearby_stories,
	}
	
	return render(request, 'mapping/haunting.html', context)


def haunting_search(request):
	# Get all hauntings described in Haunting Lawrence
	story_dict = haunting_searchset()
			
	context = {
		'haunting_set': story_dict,
		# 'total_stories': stories.count(),
	}
	
	return render(request, 'mapping/haunting_search.html', context)


def about(request):
	"""About page"""
	# Get some statistics
	total_stories = HauntedStory.objects.filter(approved=True).count()
	recent_stories = HauntedStory.objects.filter(approved=True).order_by('-submitted_at')[:3]
	
	context = {
		'total_stories': total_stories,
		'recent_stories': recent_stories,
	}
	
	return render(request, 'mapping/about.html', context)


def credit(request):
	"""Credits page"""
	return render(request, 'mapping/credit3.html', {})
