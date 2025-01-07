import sqlite3


connection = sqlite3.connect('instance/volumes/user_management.db')

cursor = connection.cursor()

query = 'SELECT _name,_interests FROM users;'
cursor.execute(query)

results = cursor.fetchall()

connection.close()

print(results)
print(type(results[1]))
