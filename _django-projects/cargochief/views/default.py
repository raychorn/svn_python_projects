from django import http
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseRedirect
from django.conf import settings

import os, sys

from vyperlogix.django import django_utils

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.hash import lists

import mimetypes
from mimetypes import guess_type

__mimetype = mimetypes.guess_type('.html')[0]
__jsonMimetype = 'application/json'
__xmlMimetype = mimetypes.guess_type('.xml')[0]
__textMimetype = 'text/plain'

_root_ = os.path.dirname(__file__)

from users.g import dict_to_json

import models

__error_symbol = 'ERROR'

def rest_handle_get_zipcode(request,parms,browserAnalysis,__air_id__,__apiMap__):
    d = {}
    postalCode = django_utils.get_from_post_or_get(request,'postalCode')
    if (postalCode):
        try:
            city = models.Cities.objects.get(postalCode=postalCode)
            d = dict([(k,v) for k,v in city.__dict__.iteritems() if (not str(k).startswith('_'))])
            #regions = models.Cities.objects.exclude(region__isnull=True).filter(country=city.country).distinct('region').order_by('region').values_list('region')
            #d['regions'] = [str(list(r)[0]) for r in regions]
        except Exception, ex:
            pass
        pass
    json = dict_to_json(d)
    return HttpResponse(content=json,mimetype=__jsonMimetype)

def rest_handle_get_regions(request,parms,browserAnalysis,__air_id__,__apiMap__):
    d = {}
    regions = models.Cities.objects.exclude(region__isnull=True).filter(country='US')
    json = dict_to_json(d)
    return HttpResponse(content=json,mimetype=__jsonMimetype)

def handle_best_quote2(request,parms,browserAnalysis,__air_id__,__apiMap__):
    d = {}
    for k,v in request.POST.iteritems():
        django_utils.put_into_session(request,k,v)
    json = dict_to_json(d)
    return HttpResponse(content=json,mimetype=__jsonMimetype)

_additional_stops_in_transit_key = 'additional_stops_in_transit_'
s_additional_stops_in_transit_count = '%scount' % (_additional_stops_in_transit_key)

_origin_from_location_driver_assist_load_key = 'origin_from_location_driver_assist_load_'
_destination_to_location_driver_assist_unload_key = 'destination_to_location_driver_assist_unload_'

__tokens = ['city','state','zipcode','yes','no']
__locale_tokens = __tokens[0:3]

def handle_best_quote2_add_stop(request,parms,browserAnalysis,__air_id__,__apiMap__):
    d = {}
    try:
        _d_ = get_best_quote2_stops(request)
        count = len(_d_)
        composite_select = []
        composite_value = []
        composite_key = []
        for t in __tokens:
            for k,v in request.POST.iteritems():
                if (str(k).endswith(t)):
                    composite_select.append(v)
                    composite_value.append(k)
                    composite_key.append(str(k).replace(t,'').split('_'))
                    break
        criteria = lambda r,k:any([(k.find(_additional_stops_in_transit_key) == -1) and (k.find(_origin_from_location_driver_assist_load_key) == -1) and (k.find(_destination_to_location_driver_assist_unload_key) == -1) and (k.find('_%s'%(t)) > -1) for t in __tokens])
        session_keys = django_utils.collect_from_session_using(request,criteria)
        criteria_origin = lambda r,k:any([(k.find(_origin_from_location_driver_assist_load_key) > -1) and (k.find('_%s'%(t)) > -1) for t in __tokens])
        session_keys_origin = django_utils.collect_from_session_using(request,criteria_origin)
        criteria_destination = lambda r,k:any([(k.find(_destination_to_location_driver_assist_unload_key) > -1) and (k.find('_%s'%(t)) > -1) for t in __tokens])
        session_keys_destination = django_utils.collect_from_session_using(request,criteria_destination)
        num = 0
        cnt_key0 = '0'
        cnt_keyO = 'O'
        cnt_keyD = 'D'
        cnt_keyS = 'S'
        cnt = {cnt_key0:0,cnt_keyO:0,cnt_keyD:0,cnt_keyS:0}
        for t in __locale_tokens:
            tKey = '_%s' % (t)
            try:
                aKey = [k for k in session_keys if (k.find(tKey) > -1)][0]
            except:
                aKey = None
            try:
                aKeyO = [k for k in session_keys_origin if (k.find(tKey) > -1)][0]
            except:
                aKeyO = None
            try:
                aKeyD = [k for k in session_keys_destination if (k.find(tKey) > -1)][0]
            except:
                aKeyD = None
            if (aKey is not None) or (aKeyO is not None) or (aKeyD is not None):
                value = django_utils.get_from_session(request,aKey,None)
                valueO = django_utils.get_from_session(request,aKeyO,None)
                valueD = django_utils.get_from_session(request,aKeyD,None)
                val = composite_select[num]
                if (value == val):
                    cnt[cnt_key0] += 1
                elif (valueO == val):
                    cnt[cnt_keyO] += 1
                elif (valueD == val):
                    cnt[cnt_keyD] += 1
                else:
                    for k,v in _d_.iteritems():
                        tokens = v.split(',')
                        try:
                            value = tokens[num]
                        except:
                            value = None
                        if (value == val):
                            cnt[cnt_keyS] += 1
            num += 1
        shortest = 2**16
        final_composite_key = []
        for a_composite_key in composite_key:
            shortest = min(len(a_composite_key),shortest)
        for a_composite_key in composite_key:
            if (len(a_composite_key) == shortest):
                final_composite_key = a_composite_key
                break
        # check to see if the values that may go into the session are not already in the session...
        _final_composite_key = 'select_%s'%('_'.join(final_composite_key))
        s_final_composite_select = ','.join(composite_select)
        num = 1
        is_found_using0 = (cnt[cnt_key0] == len(__locale_tokens))
        is_found_usingO = (cnt[cnt_keyO] == len(__locale_tokens))
        is_found_usingD = (cnt[cnt_keyD] == len(__locale_tokens))
        is_found_usingS = (cnt[cnt_keyS] == len(__locale_tokens))
        is_found = (is_found_using0) or (is_found_usingO) or (is_found_usingD) or (is_found_usingS)
        if (not is_found):
            while (1):
                key = '%s%d'%(_final_composite_key,num)
                value = django_utils.get_from_session(request,key,None)
                if (value is None) or (value == s_final_composite_select):
                    if (value == s_final_composite_select):
                        is_found = True
                    break
                num += 1
            if (not is_found):
                count = num
                s_final_composite_key = '%s%d'%(_final_composite_key,count)
                django_utils.put_into_session(request,s_final_composite_key,s_final_composite_select)
                django_utils.put_into_session(request,s_additional_stops_in_transit_count,count)
        elif (is_found_using0) or (is_found_usingS):
            d[__error_symbol] = 'WARNING: Cannot specify an existing destination because it has already been specified as an additional stop.'
        elif (is_found_usingO):
            d[__error_symbol] = 'WARNING: Cannot specify an existing destination because it has already been specified as the origin.'
        elif (is_found_usingD):
            d[__error_symbol] = 'WARNING: Cannot specify an existing destination because it has already been specified as the destination.'
        else:
            d[__error_symbol] = 'WARNING: Cannot process your request at this time due to some kind of system problem.'
        dd = get_best_quote2_stops(request)
        for k,v in dd.iteritems():
            d[k] = v
    except:
        d[__error_symbol] = 'WARNING: Cannot specify an existing destination due to some kind of processing fault.'
    json = dict_to_json(d)
    return HttpResponse(content=json,mimetype=__jsonMimetype)

def get_best_quote2_stops(request,is_removing=False):
    d = {}
    dd = {}
    try:
        num = 1
        count = int(django_utils.get_from_session(request,s_additional_stops_in_transit_count,0))
        while (num <= count):
            key = '%s_%d'%('select_additional_stops_in_transit',num)
            if (is_removing):
                del request.session[key]
            else:
                value = django_utils.get_from_session(request,key,None)
                if (value):
                    toks = value.split(',')
                    toks_len = len(toks) - 2
                    aKey1 = ','.join(toks[0:toks_len])
                    aKey2 = ','.join(toks[0:toks_len-1])
                    if (not dd.has_key(aKey1)) and (not dd.has_key(aKey2)):
                        dd[aKey1] = value
                        dd[aKey2] = value
                        d[key] = value
            num += 1
    except Exception, e:
        d[__error_symbol] = 'WARNING: Cannot retrieve the stops at this time. ('+_utils.formattedException(e)+')'
    cnt = len([k for k in d.keys() if (k != __error_symbol)])
    django_utils.put_into_session(request,s_additional_stops_in_transit_count,cnt)
    return d

def handle_best_quote2_drop_stop(request,parms,browserAnalysis,__air_id__,__apiMap__):
    d = {}
    try:
        count = int(django_utils.get_from_session(request,s_additional_stops_in_transit_count,0))
        for k,v in request.POST.iteritems():
            value = django_utils.get_from_session(request,v,None)
            if (value is not None):
                del request.session[v]
                count -= 1
                django_utils.put_into_session(request,s_additional_stops_in_transit_count,count)
                break
        d = get_best_quote2_stops(request)
    except:
        d[__error_symbol] = 'WARNING: Cannot perform the delete stop function at this time.'
    json = dict_to_json(d)
    return HttpResponse(content=json,mimetype=__jsonMimetype)

def handle_best_quote2_get_stops(request,parms,browserAnalysis,__air_id__,__apiMap__):
    d = get_best_quote2_stops(request)
    json = dict_to_json(d)
    return HttpResponse(content=json,mimetype=__jsonMimetype)

def handle_best_quote2_drop_stops(request,parms,browserAnalysis,__air_id__,__apiMap__):
    d = get_best_quote2_stops(request,is_removing=True)
    json = dict_to_json(d)
    return HttpResponse(content=json,mimetype=__jsonMimetype)
