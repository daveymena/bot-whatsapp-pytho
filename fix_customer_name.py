from database.connection import SessionLocal
from sqlalchemy import text

db = SessionLocal()
db.execute(text('ALTER TABLE orders ALTER COLUMN "customerName" DROP NOT NULL'))
db.commit()
print('✅ customerName ahora permite NULL')
db.close()
