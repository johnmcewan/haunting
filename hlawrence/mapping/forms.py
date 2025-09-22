# forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import HauntedStory
import re

class StorySubmissionForm(forms.ModelForm):
    class Meta:
        model = HauntedStory
        fields = ['title', 'story', 'author', 'latitude', 'longitude', 'date_occurred', 'submitter_email']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'e.g., "The Phantom of Fraser Hall"',
                'maxlength': 200
            }),
            'story': forms.Textarea(attrs={
                'rows': 8,
                'placeholder': 'Describe what happened... Was it a ghostly apparition? Strange sounds? Unexplained phenomena? Be as detailed as possible.',
            }),
            'author': forms.TextInput(attrs={
                'placeholder': 'Leave blank to submit anonymously',
                'maxlength': 100
            }),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'date_occurred': forms.DateInput(attrs={
                'type': 'date'
            }),
            'submitter_email': forms.EmailInput(attrs={
                'placeholder': 'Optional: for follow-up questions only',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make certain fields required
        self.fields['title'].required = True
        self.fields['story'].required = True
        self.fields['latitude'].required = True
        self.fields['longitude'].required = True
        
        # Optional fields
        self.fields['author'].required = False
        self.fields['date_occurred'].required = False
        self.fields['submitter_email'].required = False
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title:
            # Remove excessive whitespace
            title = re.sub(r'\s+', ' ', title.strip())
            
            # Check for minimum length
            if len(title) < 5:
                raise ValidationError("Title must be at least 5 characters long.")
            
            # Check for profanity or inappropriate content (basic check)
            inappropriate_words = ['damn', 'hell']  # Add more as needed
            if any(word.lower() in title.lower() for word in inappropriate_words):
                # In a real app, you might want more sophisticated filtering
                pass
                
        return title
    
    def clean_story(self):
        story = self.cleaned_data.get('story')
        if story:
            # Remove excessive whitespace
            story = re.sub(r'\s+', ' ', story.strip())
            
            # Check for minimum length
            if len(story) < 50:
                raise ValidationError("Please provide a more detailed story (at least 50 characters).")
            
            # Check for maximum length
            if len(story) > 5000:
                raise ValidationError("Story is too long. Please keep it under 5000 characters.")
                
        return story
    
    def clean_author(self):
        author = self.cleaned_data.get('author')
        if author:
            # Remove excessive whitespace
            author = re.sub(r'\s+', ' ', author.strip())
            
            # Check for reasonable length
            if len(author) > 100:
                raise ValidationError("Name is too long.")
                
        return author if author else None
    
    def clean(self):
        cleaned_data = super().clean()
        latitude = cleaned_data.get('latitude')
        longitude = cleaned_data.get('longitude')
        
        if latitude is not None and longitude is not None:
            # Validate coordinates are within Lawrence, KS area
            lat_float = float(latitude)
            lng_float = float(longitude)
            
            # Lawrence, KS approximate boundaries
            if not (38.9 <= lat_float <= 39.1):
                raise ValidationError("Latitude must be within Lawrence, Kansas area.")
            
            if not (-95.4 <= lng_float <= -95.1):
                raise ValidationError("Longitude must be within Lawrence, Kansas area.")
            
            # Check if location is too close to an existing story (optional)
            existing_stories = HauntedStory.objects.filter(approved=True)
            for story in existing_stories:
                # Calculate rough distance (not precise, but good enough for this check)
                lat_diff = abs(float(story.latitude) - lat_float)
                lng_diff = abs(float(story.longitude) - lng_float)
                
                # If within approximately 50 meters (very rough calculation)
                if lat_diff < 0.0005 and lng_diff < 0.0005:
                    raise ValidationError(
                        "This location is very close to an existing story. "
                        "Please select a slightly different location or check if your story "
                        "relates to the same location."
                    )
        
        elif latitude is None or longitude is None:
            raise ValidationError("Please select a location on the map.")
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Set default values
        instance.approved = False  # All submissions need approval
        
        if commit:
            instance.save()
        
        return instance


# Alternative simpler form for quick submissions
class QuickStoryForm(forms.Form):
    title = forms.CharField(max_length=200)
    story = forms.CharField(widget=forms.Textarea)
    latitude = forms.DecimalField(max_digits=9, decimal_places=6, widget=forms.HiddenInput)
    longitude = forms.DecimalField(max_digits=9, decimal_places=6, widget=forms.HiddenInput)
    
    def save(self):
        """Create and save a HauntedStory instance"""
        return HauntedStory.objects.create(
            title=self.cleaned_data['title'],
            story=self.cleaned_data['story'],
            latitude=self.cleaned_data['latitude'],
            longitude=self.cleaned_data['longitude'],
            approved=False
        )