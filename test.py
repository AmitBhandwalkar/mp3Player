import sqlite3  
  
conn = sqlite3.connect('play_list.db') 

print("Opened database successfully")

# try:  
#  conn.execute('''CREATE TABLE Songlist 
#        (  playlist_name text,
#           song_path text  
#        );''')  
#  print("Table created successfully")  
# except sqlite3.OperationalError:
#        print("Table are present")

# conn.execute(""" INSERT INTO Songlist (playlist_name,song_path)  
# VALUES ('fav-1','c/dsgd/dddhd')
# """)
# print("data insert")

data = conn.execute("select * from Songlist");  
for row in data:
       print(row[0],row[1])
      

#Commit Changes
conn.commit()

#Close Connection
conn.close()
