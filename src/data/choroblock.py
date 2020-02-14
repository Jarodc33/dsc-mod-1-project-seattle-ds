import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import psycopg2

cb = "/ShpFiles/cb_2017_53_bg_500k"
dbcb = gpd.read_file(cb)

DBNAME = "opportunity_youth"
conn = psycopg2.connect(dbname=DBNAME)
pumrg = pd.read_sql(f"""SELECT geo.bgrp  "GEOID",SUM(c000)  "SALL", SUM(ca01) "SU29", puma.puma5ce "PUMA", name.puma_name
                FROM wa_jobs_2017 jobs
                JOIN wa_geo_xwalk geo
                ON jobs.w_geocode = geo.tabblk2010
                JOIN ct_puma_xwalk puma
                ON geo.trct = CONCAT(puma.statefp, puma.countyfp, puma.tractce)
                JOIN puma_names_2010 name
                ON puma.puma5ce = name.puma
                WHERE puma5ce between '11610' and '11615'
                GROUP BY geo.bgrp, "PUMA",name.puma_name """, conn)

block_df = pd.merge(dbcb,pumrg,how='left',on='GEOID')
block_df['Percent'] = (block_df['SU29']/block_df['SALL']).round(2)
block_df['id'] = block_df['TRACTCE'].astype('str')+block_df['BLKGRPCE']
puma_nums = ['11610', '11611', '11612', '11613', '11614', '11615']
skc = block_df.loc[block_df['PUMA'].isin(puma_nums), ['puma_name', 'geometry','Percent','id']]

plt.rcParams['figure.figsize'] = [9, 6] 

vmin, vmax = .1, .67
# create figure and axes for Matplotlib
fig, ax = plt.subplots(1, figsize=(14,6))
# remove the axis
ax.axis('off')
# add a title and annotation
ax.set_title('Percentage of Workers \n Under Age 29 in Workforce \n Per Census Block\n', fontdict={'fontsize': '25', 'fontweight' : '3'})
# Create colorbar legend
sm = plt.cm.ScalarMappable(cmap='Blues', norm=plt.Normalize(vmin=vmin, vmax=vmax))
# empty array for the data range
sm.set_array([])
cbar = fig.colorbar(sm)
cbar.set_ticks([.2,.3, .4, .5, .6])
cbar.set_ticklabels(['20%', '30%', '40%', '50%','60%'])
# create map
skc.plot(column=(skc['Percent']), cmap='Blues', linewidth=0.8, ax=ax, edgecolor='1')