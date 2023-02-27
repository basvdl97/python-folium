import folium

if __name__ == "__main__":
    # create variables
    map_filepath = "folium-map.html"
    center_coord = [51.083180198360026, 9.307220072053097]
    marker_coord = [51.071834113635504, 8.322130552313338]
    marker_radius = 25_000

    location_marker_coord = [51.44842913103017, 6.76384970210659]
    line_coords = [
        marker_coord,
        location_marker_coord
    ]
    polygon_coords = [
        [51.569268826099616, 7.116230682121438],
        [51.301322468567676, 7.5227741435139714],
        [51.58549267882998, 7.7012214588191],
        [51.569268826099616, 7.116230682121438],
    ]
    polygon_lines = [
        [polygon_coords[i], polygon_coords[i+1]] for i in range(len(polygon_coords) - 1)
    ]

    # create folium map
    vmap = folium.Map(center_coord, zoom_start=9)

    # add a marker to the map
    folium.vector_layers.Circle(
        location=marker_coord,
        tooltip=f"The marker has radius {marker_radius}",
        radius=marker_radius,
        color="red",
        fill=True,
        fill_color="red"
    ).add_to(vmap)

    # add location marker
    folium.Marker(
        location=location_marker_coord,
        tooltip="Duisburg"
    ).add_to(vmap)

    # add line to folium map
    folium.PolyLine(
        line_coords,
        color="blue",
        weight="10",
        opacity=0.8
    ).add_to(vmap)

    # # add line to folium map
    # folium.PolyLine(
    #     polygon_coords,
    #     color="blue",
    #     weight="10",
    #     opacity=0.8
    # ).add_to(vmap)
    
    # add polygon lines separatly
    for line in polygon_lines:
        folium.PolyLine(
            line,
            color="blue",
            weight="10",
            opacity=0.8
        ).add_to(vmap)

    # store the map to a file
    vmap.save(map_filepath)

