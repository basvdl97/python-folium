import folium

def find_map_variable_name(html):
    map_start_index = html.find("var map_") + 4
    short_html = html[map_start_index:]
    map_ending_index = short_html.find(" =") + (len(html) - len(short_html))

    map_variable_name = html[map_start_index:map_ending_index]

    return map_variable_name

def find_popup_variable_name(html):
    map_start_index = html.find("var lat_lng_popup") + 4
    short_html = html[map_start_index:]
    map_ending_index = short_html.find(" =") + (len(html) - len(short_html))

    popup_variable_name = html[map_start_index:map_ending_index]

    return popup_variable_name

def find_popup_slice(html):
    # define pattern to look for
    popup_pattern     = "function latLngPop(e)"

    # find pattern start
    popup_start_index = html.find(popup_pattern)

    # find popup function ending
    tmp_html = html[popup_start_index:]

    # loop to find function close
    found = 0
    index = 0
    opening_found = False
    while not opening_found or found > 0:
        if tmp_html[index] == "{":
            found += 1
            opening_found = True
        elif tmp_html[index] == "}":
            found -= 1

        index += 1

    # determine ending index
    popup_ending_index = popup_start_index + index

    # return slice
    return popup_start_index, popup_ending_index

def custom_custom(popup_variable_name, map_variable_name):
    return '''
            // custom code insert
            function latLngPop(e) {
                %s
                    .setLatLng(e.latlng)
                    .setContent("Latitude: " + e.latlng.lat.toFixed(4) +
                                "<br>Longitude: " + e.latlng.lng.toFixed(4))
                    .openOn(%s);

                console.log("Latitude: " + e.latlng.lat.toFixed(4));
                console.log("Longitude: " + e.latlng.lng.toFixed(4));
            }
            // end custom code insert
    ''' % (popup_variable_name, map_variable_name)

if __name__ == "__main__":
    # create variables
    map_filepath = "folium-map.html"
    center_coord = [51.083180198360026, 9.307220072053097]
    zoom         = 9

    # create folium map
    vmap = folium.Map(center_coord, zoom_start=zoom)

    # adding the longlat popup
    folium.LatLngPopup().add_to(vmap)

    # store the map to a file
    vmap.save(map_filepath)

    # get the folium file html
    html = None
    with open(map_filepath, 'r') as mapfile:
        html = mapfile.read()
    
    # extract variable names
    map_variable_name = find_map_variable_name(html)
    popup_variable_name = find_popup_variable_name(html)

    # find slice starting end ending index of popup function in html
    pstart, pend = find_popup_slice(html)

    # replace popup function with custom function
    with open(map_filepath, 'w') as mapfile:
        mapfile.write(
            html[:pstart] + \
            custom_custom(popup_variable_name, map_variable_name) + \
            html[pend:]
        )
