from tinydb import TinyDB, where

db = TinyDB("xp.json")
for entry in db.all():
	entry['messages'] = 0
	db.update(entry,where('id') == entry['id'])
	print("+1")