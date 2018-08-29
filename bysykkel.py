# -*- coding: utf-8 -*-
import requests
import sys

def request(endpoint):
    url = API_ROOT+endpoint
    headers = {'Client-Identifier':IDENTIFIER}
    response = requests.get(url, headers = headers).json()
    if(response.get("error") != None):
        raise Exception(response.get("error"))
    return response

def loadStationsIntoMap():
    stations = request("stations").get("stations")
    mapToLoad = {}
    for station in stations:
        mapToLoad[station.get("id")] = station
    return mapToLoad

def filterAvailabilities(availabilityJson, known, unknown, stations):
    for stationAvailability in availabilityJson:
        availability = stationAvailability.get("availability")
        stationId = stationAvailability.get("id")
        station = stations.get(stationId)
        if station != None:
            known[stationId] = availability
        else:
            unknown.append(stationAvailability)

def printStationAvailabilities(stations, availabilities):
    for stationId in stations:
        station = stations.get(stationId)
        availability = availabilities.get(stationId)
        headerOutput = " har følgende tilgjengelighet:".decode("utf-8")
        headerOutput = station.get("title") + headerOutput
        print(headerOutput)
        bikes = availability.get("bikes")
        locks = availability.get("locks")
        output = str(locks) + " tilgjengelige låser og " + str(bikes) + " sykler"
        print(output)
        print("\n")

API_ROOT = "https://oslobysykkel.no/api/v1/"

IDENTIFIER = sys.argv[1]

stationsMap = loadStationsIntoMap()

availability = request("stations/availability").get("stations")

unknownStationAvailabilities = list()
knownStationAvailabilities = {}

filterAvailabilities(availability, knownStationAvailabilities, unknownStationAvailabilities, stationsMap)

printStationAvailabilities(stationsMap, knownStationAvailabilities)

print("I tillegg var det " + str(len(unknownStationAvailabilities)) + " objecter med ukjent id fra stations/availability")


