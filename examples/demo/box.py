# 虚假数据
import random
from pyecharts.charts import HeatMap, Kline, Line, Bar, Scatter, Grid, Boxplot


x_data = ['Apple', 'Huawei', 'Xiaomi', 'Oppo', 'Vivo', 'Meizu']
y_data = [[random.randint(100, 200) for i in range(10)] for item in x_data]

Box = Boxplot()
Box.add_xaxis(x_data)
Box.add_yaxis("", Box.prepare_data(y_data))
Box.render_notebook()