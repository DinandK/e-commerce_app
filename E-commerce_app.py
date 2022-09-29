#import packages
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import seaborn as sns

#Create header
st.markdown("<h1 style='text-align: center; color: grey;'>🛍️E-commerce dataset🛍️</h1>", unsafe_allow_html=True)
st.markdown("[Link naar de gebruikte data set🔗](https://www.kaggle.com/datasets/prachi13/customer-analytics)")

#image
image = Image.open('HVA-logo.jpg')
st.image(image)
st.subheader("Opdracht 2 gemaakt door: Jaskirat, Thijs, Maureen en Dinand")

#import dataset
df = pd.read_csv('data_app.csv')
df_user= df

see_data = st.expander('Orginele data 👇')
with see_data:
        st.dataframe(data=df)

#sidebar
st.sidebar.write("""# Opties menu⚙️""")

#_min= df['ID'].min()
#_max = df['ID'].max()
#df_user['Cost_of_the_Product'].min()
#df_user['Cost_of_the_Product'].max()

#sliders
if st.sidebar.checkbox("Sliders menu🎚️"):
    _id = st.sidebar.slider('Aantal IDs', 1 , 10999, 5500)
    df_user = df[df['ID'] <= _id]
    _price = st.sidebar.slider('Selecter een range voor de kosten per prduct', 96, 310, 200)
    df_user = df_user[df_user['Cost_of_the_Product'] <= _price]
    see_user_data = st.expander('Data na selectie👇')
    with see_user_data:
        st.dataframe(data=df_user)


#code voor histogram
def displayplot():
 st.write("""##### Verdeling verkoopprijs in verhouding tot vervoermethode: """)
 fig = px.histogram(data_frame=df_user,
                   x='Cost_of_the_Product',
                   color='Mode_of_Shipment',
                   animation_frame='Product_importance')
 fig['layout'].pop('updatemenus')
 st.plotly_chart(fig)

#code voor scatterplot
def displayplot1():
    st.write("""#####  Correlatie gewicht met korting""")
    fig = plt.subplots()
    fig = px.scatter(df_user,
                 x='Weight_in_gms',
                 y='Discount_offered',
                 color = 'Arrival_Time',
                 animation_frame='Mode_of_Shipment',
                 labels={
                     "Weight_in_gms": "Weight (in grams)",
                     "Discount_offered": "Discount offered (in %)",
                     "Arrival_Time": "On time? "
                 })
    fig['layout'].pop('updatemenus')
    st.plotly_chart(fig)

#code voor barplot
def displayplot2():
#vis1
    st.write("""#####  Leverbetrouwbaarheid per warehouse""")
    fig = plt.figure(figsize = (17, 6))
    sns.countplot('Warehouse_block', hue = 'Arrival_Time', data = df_user)
    st.write(fig)
#vis2
    st.write("""#####  Invloed shipping method op product importance""")    
    fig = px.histogram(df_user,
                 x='Product_importance',
                 color='Mode_of_Shipment')
    dropdown_buttons = [
    {'label': "All shiping methods", 'method': "update", 'args': [{"visible": [True, True, True]}, {"title": "All shiping methods"}]},
    {'label': "Flight", 'method': "update", 'args': [{"visible": [ True, False, False]}, {"title": "Flight"}]},
    {'label': "Ship", 'method': "update", 'args': [{"visible": [False, True, False]}, {"title": "Ship"}]},
    {'label': "Road", 'method': "update", 'args': [{"visible": [False, False, True]}, {"title": "Road"}]}
    ] 
    fig.update_xaxes(title_text="Product importance")
    fig.update_layout({
        'updatemenus': [
        {'active': 0, 'buttons': dropdown_buttons}
        ]})
    st.plotly_chart(fig)



#code voor boxplot
def displayplot3():  
#vis 1
 st.write("""#####  Cost Distribution with refrence to Mode of Shipment""") 
 flight = df_user[df_user["Mode_of_Shipment"]=="Flight"]
 ship = df_user[df_user["Mode_of_Shipment"]=="Ship"]
 road = df_user[df_user["Mode_of_Shipment"]=="Road"]
 trace = go.Box(y = flight["Cost_of_the_Product"], name= "Flight" )
 trace1 = go.Box(y = ship["Cost_of_the_Product"], name= "Ship" )
 trace2 = go.Box(y = road["Cost_of_the_Product"], name= "Road" )
 layout = go.Layout(yaxis=dict(title="Cost of Product"), 
                xaxis= dict(title="Mode of Shipment"))
 data=[trace, trace1, trace2]
 fig = go.Figure(data = data, layout=layout)
 st.plotly_chart(fig)

#vis 2
 st.write("""#####  Cost Distribution with refrence to Arrival TIme""") 
 ontime = df_user[df_user["Arrival_Time"]==0]
 delay = df_user[df_user["Arrival_Time"]==1]
 trace = go.Box(y = ontime["Cost_of_the_Product"], name= "Ontime" )
 trace1 = go.Box(y = delay["Cost_of_the_Product"], name= "Delayed" )
 layout = go.Layout(yaxis=dict(title="Cost of Product"), 
                   xaxis= dict(title="Arrival Time"))
 data=[trace, trace1]
 fig = go.Figure(data = data, layout=layout)
 st.plotly_chart(fig)

def displayplot4():
#vis 1
    st.write("""#####  Items in Each WareHouse Block""")    
    whb_count = pd.DataFrame(df_user["Warehouse_block"].value_counts()).reset_index()
    whb_count.rename(columns={"index": "Warehouse_block","Warehouse_block":"Count"},inplace=True)
    fig = px.pie(whb_count, values='Count', names='Warehouse_block')
    st.plotly_chart(fig)
#vis 2
    st.write("""#####  Leveringsmethode en product prioriteit per warehouse""")
    feature_selection = st.sidebar.selectbox(label="Select Warehouse", options=("A", "B", "C", "D", "E"))
    df_user1 = df_user[df_user['Warehouse_block']== feature_selection]
    plotly_figure=px.sunburst(df_user1, path=['Warehouse_block', 'Mode_of_Shipment', 'Product_importance'])
    st.write(plotly_figure)



options = st.sidebar.radio('Bladzijdes📂', options=['Histogram verdeling', 'Scatter plot', 'Bar chart', 'Boxplot', 'Piechart'])
if options == 'Histogram verdeling':
    displayplot()
elif options == 'Scatter plot' :
    displayplot1()
elif options == 'Bar chart' :
    displayplot2()
elif options == 'Boxplot':
    displayplot3()
elif options == 'Piechart':
    displayplot4()
