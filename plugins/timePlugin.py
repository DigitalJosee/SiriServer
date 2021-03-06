#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import urllib2, urllib
import json

from plugin import *

from siriObjects.baseObjects import AceObject, ClientBoundCommand
from siriObjects.uiObjects import AddViews, AssistantUtteranceView
from siriObjects.systemObjects import DomainObject

class ClockSnippet(AceObject):
    def __init__(self, clocks=None):
        super(ClockSnippet, self).__init__("Snippet", "com.apple.ace.clock")
        self.clocks = clocks if clocks != None else []

    def to_plist(self):
        self.add_property('clocks')
        return super(ClockSnippet, self).to_plist()

class ClockObject(DomainObject):
    def __init__(self):
        super(ClockObject, self).__init__("com.apple.ace.clock")
        self.unlocalizedCountryName = None
        self.unlocalizedCityName = None
        self.timezoneId = None
        self.countryName = None
        self.countryCode = None
        self.cityName = None
        self.alCityId = None
    
    def to_plist(self):
        self.add_property('unlocalizedCountryName')
        self.add_property('unlocalizedCityName')
        self.add_property('timezoneId') 
        self.add_property('countryName')
        self.add_property('countryCode')
        self.add_property('cityName')
        self.add_property('alCityId')
        return super(ClockObject, self).to_plist()


####### geonames.org API username ######
geonames_user="test2"

class time(Plugin):
    
    localizations = {"currentTime": 
                        {"search":{"de-DE": "Es wird gesucht ...", "en-US": "Procurando ..."}, 
                         "currentTime": {"de-DE": "Es ist @{fn#currentTime}", "en-US": "Sao @{fn#currentTime}"}}, 
                     "currentTimeIn": 
                        {"search":{"de-DE": "Es wird gesucht ...", "en-US": "Procurando ..."}, 
                         "currentTimeIn": 
                                {
                                "tts": {"de-DE": u"Die Uhrzeit in {0},{1} ist @{{fn#currentTimeIn#{2}}}:", "en-US": "The time in {0}, {1} is @{{fn#currentTimeIn#{2}}}:"},
                                "text": {"de-DE": u"Die Uhrzeit in {0}, {1} ist @{{fn#currentTimeIn#{2}}}:", "en-US": "As horas em {0}, {1} sao @{{fn#currentTimeIn#{2}}}:"}
                                }
                        },
                    "failure": {
                                "de-DE": "Ich kann dir die Uhr gerade nicht anzeigen!", "en-US": "Eu nao posso mostrar o seu relogio agora!"
                                }
                    }

    @register("de-DE", "(Wie ?viel Uhr.*)|(.*Uhrzeit.*)")     
    @register("en-US", "(Que horas sao*)|(.*Horas.*)|(.*Hora.*)")
    def currentTime(self, speech, language):
        #first tell that we look it up
        view = AddViews(self.refId, dialogPhase="Reflection")
        view.views = [AssistantUtteranceView(text=time.localizations['currentTime']['search'][language], speakableText=time.localizations['currentTime']['search'][language], dialogIdentifier="Clock#getTime")]
        self.sendRequestWithoutAnswer(view)
        
        # tell him to show the current time
        view = AddViews(self.refId, dialogPhase="Summary")
        view1 = AssistantUtteranceView(text=time.localizations['currentTime']['currentTime'][language], speakableText=time.localizations['currentTime']['currentTime'][language], dialogIdentifier="Clock#showTimeInCurrentLocation")
        clock = ClockObject()
        clock.timezoneId = self.connection.assistant.timeZoneId
        view2 = ClockSnippet(clocks=[clock])
        view.views = [view1, view2]
        self.sendRequestWithoutAnswer(view)
        self.complete_request()
    
    @register("de-DE", "(Wieviel Uhr.*in ([\w ]+))|(Uhrzeit.*in ([\w ]+))")
    @register("en-US", "(Que horas sao.*em ([\w ]+))|(.*Horas.*em ([\w ]+))")
    def currentTimeIn(self, speech, language):
        view = AddViews(self.refId, dialogPhase="Reflection")
        view.views = [AssistantUtteranceView(text=time.localizations['currentTimeIn']['search'][language], speakableText=time.localizations['currentTimeIn']['search'][language], dialogIdentifier="Clock#getTime")]
        self.sendRequestWithoutAnswer(view)
        
        error = False
        countryOrCity = re.match("(?u).* in ([\w ]+)$", speech, re.IGNORECASE)
        if countryOrCity != None:
            countryOrCity = countryOrCity.group(1).strip()
            # lets see what we got, a country or a city... 
            # lets use google geocoding API for that
            url = "http://maps.googleapis.com/maps/api/geocode/json?address={0}&sensor=false&language={1}".format(urllib.quote_plus(countryOrCity), language)
            # lets wait max 3 seconds
            jsonString = None
            try:
                jsonString = urllib2.urlopen(url, timeout=3).read()
            except:
                pass
            if jsonString != None:
                response = json.loads(jsonString)
                # lets see what we have...
                if response['status'] == 'OK':
                    components = response['results'][0]['address_components']
                    types = components[0]['types'] # <- this should be the city or country
                    if "country" in types:
                        # OK we have a country as input, that sucks, we need the capital, lets try again and ask for capital also
                        components = filter(lambda x: True if "country" in x['types'] else False, components)
                        url = "http://maps.googleapis.com/maps/api/geocode/json?address=capital%20{0}&sensor=false&language={1}".format(urllib.quote_plus(components[0]['long_name']), language)
                            # lets wait max 3 seconds
                        jsonString = None
                        try:
                            jsonString = urllib2.urlopen(url, timeout=3).read()
                        except:
                            pass
                        if jsonString != None:
                            response = json.loads(jsonString)
                            if response['status'] == 'OK':
                                components = response['results'][0]['address_components']
                # response could have changed, lets check again, but it should be a city by now 
                if response['status'] == 'OK':
                    # get latitude and longitude
                    location = response['results'][0]['geometry']['location']
                    url = "http://api.geonames.org/timezoneJSON?lat={0}&lng={1}&username={2}".format(location['lat'], location['lng'], geonames_user)
                    jsonString = None
                    try:
                        jsonString = urllib2.urlopen(url, timeout=3).read()
                    except:
                        pass
                    if jsonString != None:
                        timeZoneResponse = json.loads(jsonString)
                        if "timezoneId" in timeZoneResponse:
                            timeZone = timeZoneResponse['timezoneId']
                            city = filter(lambda x: True if "locality" in x['types'] or "administrative_area_level_1" in x['types'] else False, components)[0]['long_name']
                            country = filter(lambda x: True if "country" in x['types'] else False, components)[0]['long_name']
                            countryCode = filter(lambda x: True if "country" in x['types'] else False, components)[0]['short_name']
                            
                            view = AddViews(self.refId, dialogPhase="Summary")
                            view1 = AssistantUtteranceView(text=time.localizations['currentTimeIn']['currentTimeIn']['text'][language].format(city, country, timeZone), speakableText=time.localizations['currentTimeIn']['currentTimeIn']['tts'][language].format(city, country, timeZone), dialogIdentifier="Clock#showTimeInOtherLocation")
                            clock = ClockObject()
                            clock.timezoneId = timeZone
                            clock.countryCode = countryCode
                            clock.countryName = country
                            clock.cityName = city
                            clock.unlocalizedCityName = city
                            clock.unlocalizedCountryName = country
                            view2 = ClockSnippet(clocks=[clock])
                            view.views = [view1, view2]
                            self.sendRequestWithoutAnswer(view)
                        else:
                            error = True
                    else:
                        error = True
                else:
                    error = True
            else:
                error = True
        else:
            error = True
        if error:
            view = AddViews(self.refId, dialogPhase="Completion")
            view.views = [AssistantUtteranceView(text=time.localizations['failure'][language], speakableText=time.localizations['failure'][language], dialogIdentifier="Clock#cannotShowClocks")]
            self.sendRequestWithoutAnswer(view)
        self.complete_request()


## we should implement such a command if we cannot get the location however some structures are not implemented yet
#{"class"=>"AddViews",
#    "properties"=>
#        {"temporary"=>false,
#            "dialogPhase"=>"Summary",
#            "scrollToTop"=>false,
#            "views"=>
#                [{"class"=>"AssistantUtteranceView",
#                 "properties"=>
#                 {"dialogIdentifier"=>"Common#unresolvedExplicitLocation",
#                 "speakableText"=>
#                 "Ich weiß leider nicht, wo das ist. Wenn du möchtest, kann ich im Internet danach suchen.",
#                 "text"=>
#                 "Ich weiß leider nicht, wo das ist. Wenn du möchtest, kann ich im Internet danach suchen."},
#                 "group"=>"com.apple.ace.assistant"},
#                 {"class"=>"Button",
#                 "properties"=>
#                 {"commands"=>
#                 [{"class"=>"SendCommands",
#                  "properties"=>
#                  {"commands"=>
#                  [{"class"=>"StartRequest",
#                   "properties"=>
#                   {"handsFree"=>false,
#                   "utterance"=>
#                   "^webSearchQuery^=^Amerika^^webSearchConfirmation^=^Ja^"},
#                   "group"=>"com.apple.ace.system"}]},
#                  "group"=>"com.apple.ace.system"}],
#                 "text"=>"Websuche"},
#                 "group"=>"com.apple.ace.assistant"}]},
#    "aceId"=>"fbec8e13-5781-4b27-8c36-e43ec922dda3",
#    "refId"=>"702C0671-DB6F-4914-AACD-30E84F7F7DF3",
#    "group"=>"com.apple.ace.assistant"}