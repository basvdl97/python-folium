import folium


def find_popup_slice(html):
    '''
    Find the starting and edning index of popup function
    '''

    pattern = "function latLngPop(e)"

    # startinf index
    starting_index = html.find(pattern)

    #
    tmp_html = html[starting_index:]

    #
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

    # determine the edning index of popup function
    ending_index = starting_index + index

    return starting_index, ending_index

def find_map_variable_name(html):
    pattern = "var map_"

    starting_index = html.find(pattern) + 4
    tmp_html = html[starting_index:]
    ending_index = tmp_html.find(" =") + starting_index

    return html[starting_index:ending_index]


def find_popup_variable_name(html):
    pattern = "var lat_lng"

    starting_index = html.find(pattern) + 4
    tmp_html = html[starting_index:]
    ending_index = tmp_html.find(" =") + starting_index

    return html[starting_index:ending_index]

def custom_code(popup_variable_name, map_variable_name):
    return '''
            // custom code
            function latLngPop(e) {
                %s
                    .setLatLng(e.latlng)
                    .setContent("Latitude: " + e.latlng.lat.toFixed(4) +
                                "<br>Longitude: " + e.latlng.lng.toFixed(4))
                    .openOn(%s);

                console.log("Latitude: " + e.latlng.lat.toFixed(4));
                console.log("Longitude: " + e.latlng.lng.toFixed(4));
            }
            // end custom code
    ''' % (popup_variable_name, map_variable_name)

if __name__ == "__main__":
    # create variables
    map_filepath = "folium-map.html"
    center_coord = [51.083180198360026, 9.307220072053097]

    # create folium map
    vmap = folium.Map(center_coord, zoom_start=9)

    # add popup
    folium.LatLngPopup().add_to(vmap)

    # store the map to a file
    vmap.save(map_filepath)

    # read ing the folium file
    html = None
    with open(map_filepath, 'r') as mapfile:
        html = mapfile.read()

    # find variable names
    map_variable_name = find_map_variable_name(html)
    popup_variable_name = find_popup_variable_name(html)

    # determine popup function indicies
    pstart, pend = find_popup_slice(html)

    # inject code
    with open(map_filepath, 'w') as mapfile:
        mapfile.write(
            html[:pstart] + \
            custom_code(popup_variable_name, map_variable_name) + \
            html[pend:]
        )

    