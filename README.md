# livestock_vessels

This repository contains code used for our story on livestock vessels in the European Union. The data is available on request because some of it is proprietary. 

The repository contains several [notebooks](notebooks/) and [code](src/) for querying Global Fishing Watch.

## About the methodology

We started this research by compiling a list of all livestock vessels, using the following sources:

- [MarineTraffic](https://marinetraffic.com)
- [VesselFinder](https://vesselfinder.com)
- [Global Fishing Watch](https://globalfishingwatch.org)
- And several EU documents

With the MMSI (semi-persistant 'phone number' of ships) and IMO number (persistant identification number) we gathered additional information on ownership, classification and inspections in the public ship registry [Equasis](https://equasis.org), [GISIS](https://gisis.imo.org) and Global Fishing Watch.

Through Global Fishing Watch we collected the travel history (AIS data), port visits and loitering events of the 33 most active vessels between 2012 and present. For each journey between two ports we sampled the position of the vessel for every day at 2 PM and 2 AM. These positions were used to query the Marine Weather API with historical weather data. We analysed temperature and windspeed for every sample. For the Sarah M and Ganado Express we took hourly sample intervals between November 1st 2023 and December 20th 2023. 
