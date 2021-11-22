import streamlit as st
import pandas as pd
import numpy as np
import base64

st.text('Scherva')
df = pd.read_csv('df_scherva_with_tp.csv', header=0, delimiter=";")
df['Schadensdatum'] = df['Schadensdatum'].astype('datetime64')
df['Schadensdatum_Jahr'] = df['Schadensdatum'].dt.year
df['Anlage'] = df['Anlage'].fillna('0')




#year_list = list(df['Schadensdatum_Jahr'].dropna().unique())
#year_list2=[]
#year_list2=year_list[:]
#year_list2.append('Select all')
#year_options = np.array(year_list2)
#make_choice_jahr = st.selectbox('Select JAHR', year_options, 1)

#if make_choice_jahr == 'Select all':
#    make_choice_jahr = year_list
#else:
 #   make_choice_jahr = [float(make_choice_jahr)]




bm_list = list(df['MANAGEMENT_NAME'].dropna().unique())
bm_list2=[]
bm_list2=bm_list[:]
bm_list2.append('Select all')
bm_options = np.array(bm_list2)
make_choice_bm = st.selectbox('Select BM', bm_options, 1)

if make_choice_bm == 'Select all':
    make_choice_bm = bm_list
else:
    make_choice_bm = [str(make_choice_bm)]



schaden_list = list(df[df['Anlage'].str.contains("etter")]['Schadenkategorie'].dropna().unique())
schaden_list2=[]
schaden_list2=schaden_list[:]
schaden_list2.append('Select all')
schaden_options = np.array(schaden_list2)
make_choice_schaden = st.selectbox('Select Schadenkategorie', schaden_options, 1)

if make_choice_schaden == 'Select all':
    make_choice_schaden = schaden_list
else:
    make_choice_schaden = [make_choice_schaden]



#st.multiselect('Multiselect', [1,2,3])

make_choice_schaden_mem = ['Graffiti VST', 'Graffiti EG'] + ['Van. Glasbruch', 'Unbeabsichtigte Glas', 'Vandalismus allgem.', 'Einbruch/Diebstahl']









df['Anlage'] = df['Anlage'].fillna('0')
report = pd.pivot_table(df[df['Anlage'].str.contains("etter")], values='Auftragsnummer', index=['MANAGEMENT_NAME', 'Anlage', 'Schadenkategorie'], columns=['Schadensdatum_Jahr'], fill_value=0, aggfunc='count')
report.reset_index(inplace=True)
#report = report[report['Schadensdatum_Jahr'].isin(make_choice_jahr)&report['MANAGEMENT_NAME'].isin(make_choice_bm)]
report = report[report['MANAGEMENT_NAME'].isin(make_choice_bm)&report['Schadenkategorie'].isin(make_choice_schaden)]
#report = report[report['MANAGEMENT_NAME'].isin(make_choice_bm)]
report =pd.concat([report, report.drop(['MANAGEMENT_NAME', 'Anlage', 'Schadenkategorie'], axis=1).sum(axis=1)], axis=1).rename(columns={0:'Total'})
try:
    report = report.sort_values('Total', axis=0, ascending=False, inplace=False, kind='quicksort', na_position='last')
except KeyError:
    pass
st.table(report)

download_1=st.button('Download csv File')
if download_1:
    'Download Started!'

    csv = report.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings
    linko= f'<a href="data:file/csv;base64,{b64}" download="sherva_report.csv">Download</a>'
    st.markdown(linko, unsafe_allow_html=True)


st.text('MEM')

df_mem = pd.read_csv('MEM_data.csv', header=0, delimiter=";")
df_mem = df_mem[df_mem['MDATUM']!='0']
df_mem =df_mem[df_mem['MDATUM']!='1']
df_mem['DATUM'] =pd.to_datetime(df_mem['MDATUM'], format="%d.%m.%Y %H:%M:%S")
df_mem['Schadensdatum_Jahr'] = df_mem['DATUM'].dt.year
df_mem['EQUTXT'] =df_mem['EQUTXT'].fillna('0')

df_wetter = df_mem[df_mem['EQUTXT'].str.contains("etter")]
mem_schaden_list = list(df_wetter['MSCHADEN'].unique())
mem_schaden_list2=[]
mem_schaden_list2=mem_schaden_list[:]
mem_schaden_list2.append('Select all')
mem_schaden_options = np.array(mem_schaden_list2)
make_choice_schaden_mem = st.selectbox('Select Schadenkategorie MEM', mem_schaden_options, 1)


if make_choice_schaden_mem == 'Select all':
    make_choice_schaden_mem = mem_schaden_list
else:
    make_choice_schaden_mem = [make_choice_schaden_mem]

df_station_bm = df[['STATION_ID', 'MANAGEMENT_NAME']].dropna().drop_duplicates()
df_mem = pd.merge(df_mem, df_station_bm, left_on='BAHNH', right_on='STATION_ID', how='left')
mem_report = pd.pivot_table(df_mem[df_mem['EQUTXT'].str.contains("etter")], values='MEMNR', index=['MANAGEMENT_NAME',  'MSCHADEN'], columns=['Schadensdatum_Jahr'], fill_value=0, dropna=True, aggfunc='count')
mem_report.reset_index(inplace=True)
mem_report = mem_report[mem_report['MANAGEMENT_NAME'].isin(make_choice_bm)&mem_report['MSCHADEN'].isin(make_choice_schaden_mem)]
mem_report =pd.concat([mem_report, mem_report.drop(['MANAGEMENT_NAME', 'MSCHADEN'], axis=1).sum(axis=1)], axis=1).rename(columns={0:'Total'})
mem_report = mem_report.sort_values('Total', axis=0, ascending=False, inplace=False, kind='quicksort', na_position='last')
#mem_report = mem_report[mem_report['MANAGEMENT_NAME'].isin(make_choice_bm)]
#mem_report.loc['Total']= mem_report.drop(['MANAGEMENT_NAME', 'EQUTXT', 'Schadensdatum_Jahr'], axis=1).sum(axis=0)


st.table(mem_report)


download_2=st.button('Download csv')
if download_2:
    'Download Started!'

    csv = report.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings
    links= f'<a href="data:file/csv;base64,{b64}" download="mem_report.csv">Download</a>'
    st.markdown(links, unsafe_allow_html=True)
