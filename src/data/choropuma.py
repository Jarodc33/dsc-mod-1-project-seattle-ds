import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import psycopg2


ipums = "/ShpFiles/ipums_puma_2010"
ipum_df = gpd.read_file(ipums)
ipum_wa = ipum_df.loc[ipum_df['STATEFIP'] == '53']

DBNAME = "opportunity_youth"
conn = psycopg2.connect(dbname=DBNAME)
oypp = pd.read_sql("""SELECT puma AS "PUMA", sum(pwgtp) AS "OYP"  FROM pums_2017 WHERE puma between '11610' and '11615' and agep between '16' and '24' and sch = '1' and (esr = '6' or esr = '3') GROUP BY puma""", conn)

oypum = pd.merge(ipum_wa,oypp,how='left',on='PUMA')
puma_nums = ['11610', '11611', '11612', '11613', '11614', '11615']

skc = oypum.loc[oypum['PUMA'].isin(puma_nums), ['Name', 'geometry','OYP','PUMA']]
plt.rcParams['figure.figsize'] = [8, 6] #height, width

vmin, vmax = 1500, 2500
# create figure and axes for Matplotlib
fig, ax = plt.subplots(1, figsize=(8,6))
# remove the axis
ax.axis('off')
# add a title and annotation
ax.set_title('''\nCount of 'Opportunity Youth' \n in South King County \n \n''', fontdict={'fontsize': '25', 'fontweight' : '3'})
# Create colorbar legend
sm = plt.cm.ScalarMappable(cmap='summer', norm=plt.Normalize(vmin=vmin, vmax=vmax))
# empty array for the data range
sm.set_array([])
cbar = fig.colorbar(sm)
# create map
skc.plot(column=(skc['OYP']), cmap='summer', linewidth=0.8, ax=ax, edgecolor='1')
# Add Labels
skc['coords'] = skc['geometry'].apply(lambda x: x.representative_point().coords[:])
skc['coords'] = [coords[0] for coords in skc['coords']]
# Display names 
for idx, row in skc.iterrows():
    # plt.annotate(s=row['OYP'], xy=row['coords'],horizontalalignment='center',fontsize=5)
    plt.annotate(s=row['PUMA'], xy=row['coords'],horizontalalignment='center',fontsize=10)