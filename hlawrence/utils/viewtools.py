from mapping.models import * 
import statistics

def locationgather():

	locationobject = Haunting.objects.all().select_related(
	'fk_location__location_name').select_related(
	'fk_location__location_street').select_related(
	'fk_location__location_housenumber').select_related(
	'fk_location__location_houseletter').select_related(
	'fk_location__longitude').select_related(
	'fk_location__latitude').select_related(
	'fk_location__location_photo').values(
	'id_haunting',
	'haunting_storyshort',
	'fk_hauntingtype',
	'fk_location',
	'fk_location__location_name',
	'fk_location__location_street',
	'fk_location__location_housenumber',
	'fk_location__location_houseletter',
	'fk_location__longitude',
	'fk_location__latitude',
	'fk_location__location_photo',
	)

	location_dict = {}

	for e in locationobject:
		location_case = {}

		if e['fk_location__latitude'] is None:
			pass
		else:
			location_case['id_haunting'] = e['id_haunting']
			location_case['haunting_storyshort'] = e['haunting_storyshort']
			location_case['fk_hauntingtype'] = e['fk_hauntingtype']
			location_case['fk_location'] = e['fk_location']
			location_case['location_name'] = e['fk_location__location_name']
			location_case['location_street'] = e['fk_location__location_street']
			location_case['location_housenumber'] = e['fk_location__location_housenumber']
			location_case['location_houseletter'] = e['fk_location__location_houseletter']
			location_case['longitude'] = e['fk_location__longitude']
			location_case['latitude'] = e['fk_location__latitude']
			location_case['location_photo'] = e['fk_location__location_photo']

			location_dict[e['id_haunting']] = location_case

	return(location_dict)

#based on mapgenerator2
def locationdata(location_object):

	center_lat = []
	center_long = []

	mapdic = {"type": "FeatureCollection"}
	properties = {}
	geometry = {}
	location = {}
	placelist = []
	lat_values = []
	long_values = []

	for loc in location_object.values():
		value1 = loc['id_haunting']
		value2 = loc['location_name']
		# value3 = loc.count
		value4 = loc['longitude']
		value5 = loc['latitude']

		if type(loc['longitude']) == int or type(loc['longitude']) == float:
			long_values.append(loc['longitude'])
		if type(loc['latitude']) == int or type(loc['latitude']) == float:
			lat_values.append(loc['latitude'])

		popupcontent = '<a href="entity/' + str(value1) + '">' + str(value2) + '</a>'

		# if value3 > 0:
		# 	popupcontent = popupcontent + ' ' + str(value3)

		properties = {"id_location": value1, "location": value2, "popupContent": popupcontent}
		geometry = {"type": "Point", "coordinates": [value4, value5]}
		location = {"type": "Feature", "properties": properties, "geometry": geometry}
		placelist.append(location)

	mapdic["features"] = placelist

	center_long = statistics.median(long_values)
	center_lat = statistics.median(lat_values)

	return(mapdic, center_long, center_lat)