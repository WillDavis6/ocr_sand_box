from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import psycopg2
from ocr_optimization_testing import ocr_magic

# Create an engine and connect to a PostgreSQL database

engine = create_engine('postgresql+psycopg2://postgres:Msi_123@localhost:5432/portal_data_base')

Base = declarative_base()


class DynamicTable(Base):
    __tablename__ = 'dynamic_table'
    id = Column(Integer, primary_key=True)


    @classmethod
    def create_table(cls, num_rows, num_columns):
        table_name = f"dynamic_table_{num_rows}x{num_columns}"
        columns = {'id': Column(Integer, primary_key=True)}
        


        for j in range(num_columns):
            column_name = f"column_{j+1}"
            columns[column_name] = Column(String(255))

        table = type(table_name, (Base,), {
            '__tablename__': table_name,
            **columns
        })

        table.metadata.create_all(engine)
       
        print(f'$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$  CREATED TABLE: {table_name}  $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

        return table

Session = sessionmaker(bind=engine)

def add_row(column_list):
    session = Session()

    try:
        new_row = DynamicTable()

        for i, value in enumerate(column_list, start=1):
            setattr(new_row, f"column_{i}", value)

        session.add(new_row)

        session.commit()
        print(f'Row {i} added successfully!')
    except Exception as e:
        session.rollback()
        print(f'Error adding row: {e}')

    finally:

        session.close()




blueprint_url =  "C:\\Users\\William.davis\\Desktop\\python_data_set\\static\\images\\table_test.png"
#blueprint_url =  "C:\\Users\\William.davis\\Desktop\\python_data_set\\static\\images\\Screenshot 2024-04-24 081630.png"

export_url = "C:\\Users\\William.davis\\OneDrive - msiGCCH\\Pictures\\Screenshots\\test_updated_image_cv2.png"




if __name__ == "__main__":
    DynamicTable.create_table(39, 14)
    ocr_magic(blueprint_url, export_url, 20, 500, 4)
   
