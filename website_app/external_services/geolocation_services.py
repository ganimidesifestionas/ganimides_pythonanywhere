import requests
from ..debug_services.debug_log_services import *
##########################################################################################################
def get_geolocation_info_from_IP(ip=None):
    log_start('get_geolocation_info_from_IP')
    if not ip:
        log_error('get_geolocation_info_from_IP requires input','ip address')
        log_finish('get_geolocation_info_from_IP')
        return None
    if not ip:
        ip = '127.0.0.1'
    if ip == '127.0.0.1':
        ip = '213.149.173.194'
    ################################################################
    ### ipstack access key
    ################################################################
    #IPSTACK_API_ACCESSKEY = '4022cfd2249c3431953ecf599152892e'
    #IPSTACK_URL = 'http://api.ipstack.com/'
    #IPSTACK_URL_CMD = 'http://api.ipstack.com/{0}?access_key={1}'
    path = 'http://api.ipstack.com/{0}?access_key={1}'.format(ip, '4022cfd2249c3431953ecf599152892e')
    log_variable('apistack geolocation path', path)
    response = {}
    try:
        r = requests.post(path)
    except:
        r = None
    #print(r)
    #reply_code=r.status_code
    # if not r.status_code == requests.codes.ok:
    if r:
        response = r.json()
        #log_variable('apistack geolocation result', response)
        for key, value in response.items():
            log_variable('geolocationDictionary '+key+'=', value)
        loc = response['location']
        for key, value in loc.items():
            log_variable('geolocationDictionary location '+key+'=', value)
        log_finish('get_geolocation_info_from_IP')
        return response
    else:
        log_warning('api.ipstack.com is not available...')
        log_finish('get_geolocation_info_from_IP')
        return None
    #res = response.json()
        #print(res)
    #r = requests.post(api_url,headers=headers,data=payload)
    #reply_code=r.status_code
##########################################################################################################
def get_geolocation_info(latitude, longitude):
    log_start('get_geolocation_info')
    geolocationDictionary = {}
    geolocationDictionary.update({'latitude' : latitude})
    geolocationDictionary.update({'longitude' : longitude})
    #log_variable('latitude', latitude)
    #log_variable('longitude', longitude)

    GOOGLE_MAPS_API_KEY = 'AIzaSyCstqUccUQdIhV69NtEGuzASxBQX5zPKXY'
    # api_url = 'https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyCstqUccUQdIhV69NtEGuzASxBQX5zPKXY
    path = 'https://maps.googleapis.com/maps/api/geocode/json?latlng={0},{1}&key={2}'.format(latitude,longitude,GOOGLE_MAPS_API_KEY)
    log_variable('apistack geolocation path', path)
    try:
        r = requests.post(path)
    except:
        log_warning('https://maps.googleapis.com/maps/... is NOT AVAILABLE....')
        r = None
    #print(r)
    #reply_code=r.status_code
    #print(requests.codes.ok)
    #log_variable('reply status', r.status_code)
    if not r.status_code == requests.codes.ok:
        log_finish('get_geolocation_info')
        return None
    if r:
        response = r.json()
        #log_variable('GEOLOCATION', response)
        status = response.get('status')
        #log_variable('status', status)
        plus_code = response.get('plus_code')
        #log_variable('plus_code', plus_code)
        results = response.get('results')
        #log_variable('results',results)
        if status != 'OK':
            log_finish('get_geolocation_info')
            return None
        for res in results:
            types = res.get('types')
            compos = res.get('address_components')
            address = res.get('formatted_address')
            geometry = res.get('geometry')
            place_id = res.get('place_id')
            plus_code = res.get('plus_code')
            #log_variable('types', types)
            for geoname in compos:
                #log_variable('   types', geoname.get('types'))
                #log_variable('   value', geoname.get('long_name'))
                val = geoname.get('long_name')
                if 'country' in geoname.get('types'):
                    geolocationDictionary.update({'country_name' : val})
                    #log_variable('--- --- country', val)
                if 'postal_code' in geoname.get('types'):
                    geolocationDictionary.update({'zip' : val})
                    #log_variable('--- --- postal code', val)
                if 'administrative_area_level_1' in geoname.get('types'):
                    geolocationDictionary.update({'region_name' : val})
                    #log_variable('--- --- region', val)
                if 'locality' in geoname.get('types'):
                    geolocationDictionary.update({'city' : val})
                    #log_variable('--- --- city', val)
                if 'sublocality' in geoname.get('types'):
                    geolocationDictionary.update({'area' : val})
                    #log_variable('--- --- area', val)
                if 'neighborhood'  in geoname.get('types'):
                    geolocationDictionary.update({'area' : val})
                    #log_variable('--- --- area', val)
            if 'street_address' in res.get('types'):
                val = res.get('formatted_address')
                #log_variable('--- --- address', val)
                geolocationDictionary.update({'address' : val})

                val = res.get('geometry')
                nam = 'geometry'
                #log_variable('--- --- geometry', val)
                #geolocationDictionary.update({'address' : val})
        for geoname in geolocationDictionary.items():
            log_variable('geolocationDictionary', geoname)

        log_finish('get_geolocation_info')
        return geolocationDictionary
##########################################################################################################
##########################################################################################################
#print(__name__)
if __name__ == '__main__':
    log_start('geolocation_services')
    get_geolocation_info(35.123647 , 33.367925)
    get_geolocation_info_from_IP('127.0.0.1')
    log_finish('geolocation_services')
    log_info('finish.....')
    #log_variable('test', 'test')
