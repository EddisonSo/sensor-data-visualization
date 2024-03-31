from sqlalchemy import DateTime
from datetime import  date
import plotly.express as px
from models.sensor_data import SensorData


class SensorPlot:
    layout = {
        "l": 0,
        "r": 0,
        "t": 0,
        "b": 0
    }
    width=350
    height=150

    def __init__(self, data: list[SensorData]) -> None:
        self.data = data
        self.distance, self.rain, self.voltage, self.time, self.data_date = zip(*list(map(lambda x: (x.get_distance(), x.get_rain(), x.get_voltage(), x.get_time(), x.get_date()), data)))
 
    def test_line(self):
        fig = px.line(x=(10000), y=range(10000), width=self.width, height=self.height).update_layout(margin=self.layout, yaxis_title=None, xaxis_title="1 Day")
        return fig.to_html(include_plotlyjs="cdn", config = {'displayModeBar': False})

    def plot_distance(self):
        fig = px.line(x=self.time, y=self.distance, width=self.width, height=self.height)
        fig.update_layout(margin=self.layout, yaxis_title=None, xaxis_title="1 Day")
        fig.update_layout(xaxis={'visible': False, 'showticklabels': False})
        fig.update_yaxes(range=[300, 5000])
        fig.update_xaxes(autorange="reversed")
        return fig.to_html(include_plotlyjs="cdn", config = {'displayModeBar': False})


    def plot_rain(self):
        fig = px.line(x=self.time, y=self.rain, width=self.width, height=self.height)
        fig.update_layout(margin=self.layout, yaxis_title=None, xaxis_title="1 Day")
        fig.update_layout(xaxis={'visible': False, 'showticklabels': False})
        fig.update_yaxes(range=[0, 10])
        fig.update_xaxes(autorange="reversed")
        return fig.to_html(include_plotlyjs="cdn", config = {'displayModeBar': False})


