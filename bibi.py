from evpn import ExpressVpnApi

with ExpressVpnApi() as api:
    locations = api.locations  # get available locations
    loc = locations
    #write locations to a separate file
    with open('locations.txt', 'w') as file:
        for location in locations:
            file.write(f"{locations}")
