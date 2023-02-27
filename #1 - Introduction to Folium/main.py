import folium

if __name__ == "__main__":
    # create variables
    map_filepath = "folium-map.html"
    center_coord = [51.083180198360026, 9.307220072053097]
    marker_coord = [51.071834113635504, 8.322130552313338]
    marker_radius = 25_000

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

    # store the map to a file
    vmap.save(map_filepath)

