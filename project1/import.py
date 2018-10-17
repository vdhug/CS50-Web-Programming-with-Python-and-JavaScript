import csv, os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


# Check for environment variable
if not os.getenv("DATABASE_URL"):
  raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    print(type(f))
    reader = csv.reader(f)
    print(type(reader))
    for isbn, title, author, year in reader[1:]:
   	    db.execute("INSERT INTO books(isbn, title, author, year) VALUES (:isbn, :title, :author, :year)", {"isbn": isbn, "title": title, "author": author, "year": year})
   	db.commit()

if __name__ == "__main__":
	main()