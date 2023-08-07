import geocoder

def get_user_location():
    user_lat_lng = geocoder.ip('me').latlng
    user_lat_lng_string = '{},{}'.format(user_lat_lng[0], user_lat_lng[1])
    return user_lat_lng_string