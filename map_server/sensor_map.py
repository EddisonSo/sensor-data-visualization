import base64
import folium
from sensor_plot import SensorPlot
from utils import *
from typing import Union
import plotly.express as px
import json

class SensorMap:
    default_location: list[int]
    zoom_start: int
    tiles: str

    def __init__(self, default_location=[40.7440, -74.0324], zoom_start=15, tiles="openstreetmap"):
        self.default_location = default_location
        self.zoom_start = zoom_start
        self.tiles = tiles

    def generate_map(self):
        m = folium.Map(location=self.default_location, zoom_start=self.zoom_start, tiles=self.tiles)
        folium.TileLayer(tiles="Stamen Terrain").add_to(m)
        folium.TileLayer('cartodbdark_matter').add_to(m)
        with open("nj_polygon.json") as handle:
            hoboken_geo = json.loads(handle.read())

        folium.GeoJson(hoboken_geo,
               name='hoboken').add_to(m)


        # add control to be able to select base map
        m.add_child(folium.LayerControl())


        sensors: list[Sensor] = get_sensors()

        for sensor in sensors:
            html = f"""
            <h1>No Available Data</h1>
            """
            datas = get_datas_since(sensor.get_id(), 48)

            if datas:
                plot = SensorPlot(datas)

                fig_distance_html = plot.plot_distance()
                fig_rain_html = plot.plot_rain()
                image = '<img src="data:image/png;base64, {}" width="150px" align="right">'.format(base64.b64encode(open("static/logo.png", "rb").read()).decode())
                html = f"""
                <p>
                    <b>Location: </b>{sensor.address}
                    {image}
                </p>
                <p>
                    <b>Deployment Date: </b>{str(sensor.get_date())}
                </p>
                <p>
                    <b>Distance Readings:</b>
                </p>
                    {fig_distance_html}
                <p>
                    <b>Rain Readings:</b>
                </p>
                    {fig_rain_html}
                <br style="line-height: 10px"/>
                <center>
                    <button onclick="window.top.location.href='https://web.stevens.edu/ismart/';" style="width:200px;height:30px">
                        Click Here
                    </button>
                </center>
                """

            iframe = folium.IFrame(html)
            iframe.get_root().height = "510px"
            popup = folium.Popup(iframe, min_width=380, max_width=380, frameborder="0", scrolling="no")

            if sensor.get_longitude() and sensor.get_latitude():
                folium.Marker(
                    [sensor.longitude, sensor.latitude],
                    popup=popup,
                    icon=folium.Icon(icon='water', prefix='fa')
                ).add_to(m)

        return m.get_root().render()
