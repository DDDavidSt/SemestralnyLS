libraries = sqlite3, hashlib (to hash passwords with MD5), json(turned out to be useless), datetime, random,calendar, curses, tkinter
tcalendar, PIL


You need to run the file 'databaza.py' to create a random database with names and animals. (if already exists needs to be removed first)
User 'admin' with password 'admin' has admin privileges meaning they can add new employees or sack them, add/remove animals
Other users can just view their animals and a two lists of duties (feeding and cleaning)

Improvements- the code can be definitely more efficient but I was doing it in a hurry so thats why, visuals definitely and maybe
adding a scrollable page on which the whole database can be shown without needing to select which animal or employee i want to see
Also the duties lists count on max 3 animals, so that can be improved with the aformentioned solution too.
