from pymongo import MongoClient
import pandas as pd
from pyecharts.charts import Bar
import pyecharts.options as opts

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

newhigh=MongoClient()['wencai']['newhigh250']
newlow=MongoClient()['wencai']['newlow250']

newhigh_data=newhigh.find()
newhigh_df=pd.DataFrame(newhigh_data)
newlow_data=newlow.find()
newlow_df=pd.DataFrame(newlow_data)
x=newhigh_df['trade_date'].tolist()
high_num=newhigh_df['新高数量'].tolist()
low_=newlow_df['新高数量'].tolist()
low_num=[-i for i in low_]


bar = (Bar(init_opts=opts.InitOpts(page_title="新高新低趋势对比"))
        .add_xaxis(x)
        .add_yaxis('新高：昨日,{} | 今日,{}'.format(high_num[-2],high_num[-1]), high_num)
        .add_yaxis('新低：昨日,{} | 今日,{}'.format(low_[-2],low_[-1]), low_num)
        .set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),
                         toolbox_opts=opts.ToolboxOpts(),
                         datazoom_opts=opts.DataZoomOpts(),
                         title_opts=opts.TitleOpts(title='新高新低趋势对比', subtitle='大盘趋势'))
       .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        )
bar.render_notebook()