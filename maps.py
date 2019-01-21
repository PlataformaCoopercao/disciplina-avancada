import urllib.request
import json
import random
from settings import API_KEY

endpoint = 'https://maps.googleapis.com/maps/api/distancematrix/json?'


def get_duration(origin, destination):

    nav_request = 'origins={}&destinations={}' \
                  '&mode=walking&key={}'.format(origin, destination, API_KEY)

    r = endpoint + nav_request
    response = urllib.request.urlopen(r).read()
    directions = json.loads(response)
    duration = directions['rows'][0]['elements'][0]['duration']['value']

    return duration


def route_duration(route):

    duration = 0
    for index, place in enumerate(route):
        if index + 1 < len(route):
            duration += get_duration(place, route[index + 1])
    return duration


def random_hillclimbing_final(route, opt_limit, opt=1, best_duration=None):

    if best_duration is None:
        old_duration = route_duration(route)
    else:
        old_duration = best_duration

    if opt <= opt_limit:
        new_route = []
        old_route = route.copy()

        for place in route:
            random_place = random.choice(old_route)
            new_route.append(random_place)
            old_route.remove(random_place)
        if new_route != route:
            new_duration = route_duration(new_route)
            if new_duration < old_duration:
                return random_hillclimbing_final(new_route, opt_limit,
                                                    opt=opt+1,
                                                    best_duration=new_duration)
        else:
            return random_hillclimbing_final(route, opt_limit, opt=opt+1,
                                                best_duration=old_duration)
    return (route, old_duration)


route2 = ['place_id:EkFSLiBTZWJhc3Rpw6NvIEFsdmVzIC0gVGFtYXJpbmVpcmEsIFJl'
          'Y2lmZSAtIFBFLCA1MjE3MS0wMTEsIEJyYXppbCIuKiwKFAoSCT-irK5UGKsHE'
          'T0hwYvgieVWEhQKEglbeb7xUxirBxHO7QZDwtgYgw',
          'place_id:ChIJISx9OooZqwcRLokhmDAdQBc',
          'place_id:ChIJvYBhVKoZqwcR_MfIpzZMLKs']

print(random_hillclimbing_final(route2, 1))
print(random_hillclimbing_final(route2, 3))
print(random_hillclimbing_final(route2, 5))
