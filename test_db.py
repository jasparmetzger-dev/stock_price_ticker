from app.database import engine, Base
print("imported app.database")
from app import models
print("imported app.models")

Base.metadata.create_all(bind=engine)
print("Tables created successfully!")