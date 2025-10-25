from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///marketmind.db")

with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM stocks LIMIT 5"))
    for row in result:
        print(row)