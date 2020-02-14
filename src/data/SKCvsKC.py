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
oypp = pd.read_sql("""SELECT DISTINCT(puma5ce) "PUMA", statefp, countyfp  FROM ct_puma_xwalk WHERE statefp = '53' and countyfp = '033' """, conn)

oypum = pd.merge(ipum_wa,oypp,how='right',on='PUMA')

oypum = oypum.dropna()
oypum.head()

puma_nums = ['11610', '11611', '11612', '11613', '11614', '11615']
oypum['skc'] = np.where(oypum['PUMA'].isin(puma_nums),'SOUTH KING COUNTY','THE REST OF\nKING COUNTY')

oypum['Name'] = oypum['Name'].map(lambda x: x.lstrip('King County  (Northwest)-- al)-- ').rstrip('PUMA (Northeast)'))
oypum['Name'][0] = 'Shoreline,\nKenmore,\nBothell'
oypum['Name'][1] = '\nBellevue'
oypum['Name'][2] = 'Renton,\nSkyway'
oypum['Name'][3] = 'Redmond,\nKirkland,\nInglewood'
oypum['Name'][4] = ''
oypum['Name'][5] = 'Capitol\nHill'
oypum['Name'][6] = 'Issaquah,\nMercer Island'
oypum['Name'][7] = 'Kent'
oypum['Name'][8] = 'Auburn'
oypum['Name'][9] = 'Maple Valley,\nCovington & Enumclaw'
oypum['Name'][10] = 'Seattle'
oypum['Name'][11] = 'Queen Anne'
oypum['Name'][12] = ''
oypum['Name'][13] = 'Burien,\nSeaTac,\nTukwila'
oypum['Name'][14] = 'Federal Way,\nDes Moines'
oypum['Name'][15] = 'Snoqualmie City,\nCottage Lake,\n Union Hill'


plt.rcParams['figure.figsize'] = [8, 6] #height, width
vmin, vmax = 0, 1
# create figure and axes for Matplotlib
fig, ax = plt.subplots(1, figsize=(16,12))
# remove the axis
ax.axis('off')
# add a title and annotation
ax.set_title('\n SKC Vs KC', fontdict={'fontsize': '25', 'fontweight' : '3'})
# ax.legend(oypum['skc'],('SKC','KC'))
# Create colorbar legend
sm = plt.cm.ScalarMappable(cmap='Blues', norm=plt.Normalize(vmin=vmin, vmax=vmax))
# empty array for the data range
sm.set_array([])
# cbar = fig.colorbar(sm)
# create map
oypum.plot(column=(oypum['skc']), cmap='Accent', linewidth=0.8, ax=ax, edgecolor='1', legend=True)
# Add Labels
oypum['coords'] = oypum['geometry'].apply(lambda x: x.representative_point().coords[:])
oypum['coords'] = [coords[0] for coords in oypum['coords']]
# Display names 
for idx, row in oypum.iterrows():
    plt.annotate(s=row['Name'], xy=row['coords'],horizontalalignment='center',size='9')