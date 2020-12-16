from bs4 import BeautifulSoup
import sqlite3 

file = 'C:/Users/wabar/OneDrive/Desktop/dotabuff_data.html'
data = open(file,  encoding="UTF-8")

soup = BeautifulSoup(data, "html.parser")


##### SQL #####

# connecting to the database  
connection = sqlite3.connect("Dotabuffer22.db") 
 
# cursor  
crsr = connection.cursor() 
  
# SQL command to create a table in the database 
sql_create_games_table = """
CREATE TABLE IF NOT EXISTS Games (
col_id INTEGER PRIMARY KEY,
hero VARCHAR(30),
result VARCHAR(30),
date VARCHAR(30),
time VARCHAR(30),
duration VARCHAR(30),
kda VARCHAR(30),
game_type VARCHAR(30)
);
"""

sql_create_items_table = """
CREATE TABLE IF NOT EXISTS Items (
col_id INTEGER,
col1 VARCHAR(30),
col2 VARCHAR(30),
col3 VARCHAR(30),
col4 VARCHAR(30),
col5 VARCHAR(30),
col6 VARCHAR(30),
PRIMARY KEY (col_id),
FOREIGN KEY (col_id) REFERENCES Games (col_id)
);
"""
  
# execute the statement 
crsr.execute(sql_create_games_table)
crsr.execute(sql_create_items_table)

#################


table_data = soup.findAll('tbody')[1]
account_name = (soup.findAll('a')[12]).text
print('Account Name: ', account_name)

# Sets initial tag values to scrape
i = 79 
x = 79
t = 0
q = 4 
d = 5
z = 6
xd = 2

itemlist = [] 
item1 = str()
item2 = str()
item3 = str()
item4 = str()
item5 = str()
item6 = str()

# Extracts data for individual match 
for i in range(i, i+20):
    
    game_id = table_data.findAll('a')[xd]
    #print(game_id)
    game_id = (game_id.attrs['href']).split('/')[2]


    while True:
        try:
            game_id = int(game_id)
            break
        except ValueError:
            xd = xd+1
            game_id = table_data.findAll('a')[xd]
            game_id = (game_id.attrs['href']).split('/')[2]
            
    #game_id = (game_id.attrs['href']).split('/')[2]
    print('\nGame ID: ', game_id)
    
    
    hero = (soup.findAll('a')[x]).text
    print('Hero: ', hero)
    
    match_result = (soup.findAll('a')[x+1]).text
    print('Result: ' , match_result)
    
    datetime = table_data.findAll('time')[t]
    date = (datetime.attrs['datetime']).split('T')[0]
    print('Date: ', date)
    time = ((datetime.attrs['datetime']).split('T')[1]).split('+')[0]
    print('Time: ', time)

    duration = table_data.findAll('td')[d]
    duration = duration.text
    print('Duration: ', duration)
    
    kda = table_data.findAll('td')[z]
    kda = kda.text
    print('KDA: ', kda)
    
    game_type = table_data.findAll('td')[q]
    game_type = game_type.text
    print('Game Type: ', (game_type))
    
    # SQL command to insert the data in the table 
    entry_games = (game_id, hero, match_result, date, time, duration, kda, game_type)
    crsr.execute("INSERT INTO Games VALUES(?, ?, ?, ?, ?, ?, ?, ?)", entry_games)
                   
                
    #INSERT INTO Games(col_id, hero, result, date, time, duration, kda, game_type) 
    #VALUES(game_id, '?','?','?','?','?','?', '?');"""==
    #crsr.execute(sql_insert_games_table) 
    
    #INSERT INTO Items (col_id)
    #VALUES ()
    #;
    #crsr.execute(sql_insert_items_game_id) 
    
    z = z+9
    t = t+1
    d = d+9
    q = q+9
    xd = xd+8

    for x in range(x+2, x+8): 
        item = (soup.findAll('a')[x])
        if item.attrs['href'].startswith('/heroes'):
            x = x-1
            break
        else:          
            item_formatting = ((item.attrs['href']).split("/"))
            item_formatting = (item_formatting[2].replace("-", " ")).title() 
            #print("Item ",[x-(d+66)], ":" , item_formatting)
            itemlist.append(item_formatting)
    
                 
# Prints list of items from 1-6.
       
    x = x+2
    try:
        item1 = itemlist[0]
    except IndexError:
         item1 = 'ERROR'
    try:
        print("Item 1: ", item1)
    except:
        continue
    try:
         item2 = itemlist[1]
    except IndexError:
         item1 = 'ERROR'         
    try:
        print("Item 2: ", item2)
    except:
        continue
    try:
         item3 = itemlist[2]
    except IndexError:
         item1 = 'ERROR'
    try:
        print("Item 3: ", item3)#
    except:
        continue
    try:
         item4 = itemlist[3]
    except IndexError:
         item1 = 'ERROR'         
    try:
        print("Item 4:", item4) 
    except NameError:
        continue
    try:
         item5 = itemlist[4]
    except IndexError:
         item1 = 'ERROR'   
    try:
        print("Item 5:", item5)
    except NameError:
        continue
    try:
         item6 = itemlist[5]
    except IndexError:
         item1 = 'ERROR'
    try:
        print("Item 6:", item6) 
    except NameError:
        continue        
    
    # another SQL command to insert the data in the table 
    insert_items_game_id = (game_id, item1, item2, item3, item4, item5, item6)
    crsr.execute("""INSERT INTO Items VALUES(?,?,?,?,?,?,?)""", insert_items_game_id)
    
# Clears values in list and for loop
    itemlist.clear()
    try:
        del item1
    except NameError:
        continue
    try:
        del item2
    except NameError:
        continue
    try:
        del item3
    except NameError:
        continue
    try:
        del item4
    except NameError:
        continue
    try:
        del item5
    except NameError:
        continue
    try:
        del item6
    except NameError:
        continue
 
# To save the changes in the files. Never skip this.  
# If we skip this, nothing will be saved in the database. 
connection.commit() 
  
# close the connection 
connection.close() 


#create table for each match over all 50 pages