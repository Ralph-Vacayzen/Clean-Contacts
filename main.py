import streamlit as st
import pandas as pd

st.set_page_config(page_title='Clean Contacts', page_icon='📇', layout='centered', initial_sidebar_state='auto', menu_items=None)

st.caption('VACAYZEN')
st.title('Clean Contacts')
st.info('Cleans the constant contacts export, removing: old, partner, and duplicate emails.')

pd.options.mode.chained_assignment = None

date = st.date_input('Date of last contact cleaning:')

file = st.file_uploader('Constant Contact.csv','CSV')

if file is not None:
    df = pd.read_csv(file, index_col=False)

    df.columns = ['contact','email','date']

    df['date'] = pd.to_datetime(df['date']).dt.date

    df = df[df['date'] > date]

    for partner in st.secrets['PARTNERS']:
        df = df[df['email'].str.contains(partner) == False]

    df = df.sort_values('date')
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)
    df.index += 1

    st.download_button(label='DOWNLOAD', data=df.to_csv(), file_name='contacts.csv', mime='csv', use_container_width=True, type='primary')