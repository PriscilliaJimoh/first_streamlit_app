import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🥑🍞 Hard-Boiled Free-Range Egg')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
# 🥣 🥗 🐔 🥑🍞

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# fruits_selected2 = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Mango', 'Pear'])
# fruits_to_show2 = my_fruit_list.loc[fruits_selected2]
# streamlit.dataframe(my_fruit_list)
streamlit.dataframe(fruits_to_show)
# streamlit.dataframe(fruits_to_show2)

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    stream.error("Pleased select a fruit to get information.")
else:
# streamlit.write('The user entered ', fruit_choice)
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  streamlit.dataframe(fruityvice_normalized)
 execpt URLError as e:
    streamlit.error()
  

add_my_fruit = streamlit.text_input('What fruit would you like information about?','Jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)
streamlit.stop()
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
# my_cur.execute("insert into fruit_load_list values ('from streamlit')")
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
# my_data_row = my_cur.fetchone()
# streamlit.text("Hello from Snowflake:")
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)
