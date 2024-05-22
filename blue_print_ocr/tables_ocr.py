from sqlalchemy import create_engine, Column, Integer, String, Table, select, desc, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from colorama import Fore


# Create an engine and connect to a PostgreSQL database

engine = create_engine('postgresql+psycopg2://postgres:Msi_123@localhost:5432/portal_data_base')

Base = declarative_base()
metadata = MetaData()


class DynamicTable(Base):
    __tablename__ = 'dynamic_table'
    __table_args__ = {'extend_existing' :True}
    id = Column(Integer, primary_key=True)


    @classmethod
    def create_table(cls, num_columns, i, metadata, engine):
        table_name = f"dynamic_table_{i}"
        columns = {'id': Column(Integer, primary_key=True)}
        


        for j in range(num_columns):
            column_name = f"column_{j+1}"
            columns[column_name] = Column(String(255))

        table = type(table_name, (Base,), {
            '__tablename__': table_name,
            '__table_args__': {'extend_existing': True},
            **columns
        })

        table.__table__.metadata = metadata
        metadata.create_all(engine)
        metadata.reflect(engine)
       
        print(Fore.GREEN + f'INITIATE --> CREATED TABLE: {table_name}')

        return table



def add_row(row_values, table):
    

    try:
        new_row = table()

        for i, value in enumerate(row_values):
            setattr(new_row, f"column_{i}", value)

        session.add(new_row)

        session.commit()
        #print(f'Row {i} added successfully!')
    except Exception as e:
        session.rollback()
        print(f'Error adding row: {e}')

    finally:

        pass


Session = sessionmaker(bind=engine)
session = Session()
metadata = MetaData()



export_url = "C:\\Users\\William.davis\\OneDrive - msiGCCH\\Pictures\\Screenshots\\test_updated_image_cv2.png"

blueprint_list = ["C:\\Users\\William.davis\\Desktop\\python_data_set\\static\\blueprints\\35-8227 ALL COMBINED_Page_01.jpg", "C:\\Users\\William.davis\\Desktop\\python_data_set\\static\\blueprints\\35-8227 ALL COMBINED_Page_02.jpg", "C:\\Users\\William.davis\\Desktop\\python_data_set\\static\\blueprints\\35-8227 ALL COMBINED_Page_24.jpg", "C:\\Users\\William.davis\\Desktop\\python_data_set\\static\\blueprints\\35-8227 ALL COMBINED_Page_25.jpg", "C:\\Users\\William.davis\\Desktop\\python_data_set\\static\\blueprints\\35-8227 ALL COMBINED_Page_26.jpg"]


if __name__ == "__main__":
    from ocr_optimization_testing import ocr_magic
    
    for i, blueprint_url in enumerate(blueprint_list):
        table_name = ocr_magic(blueprint_url, export_url, 20, 500, 4, i, metadata, engine)

        print(f'Table name returned: {table_name}')
        print(f'Metadata tables: {metadata.tables.keys()}')

        if table_name in metadata.tables:
            table = metadata.tables[table_name]
            query = session.query(table).order_by(desc(table.c.id)).limit(1)
            last_row = query.one()
            target_column = None

            for column in table.c:
                if 'MAT' in str(getattr(last_row, column.name)):
                    target_column = column.name
                    print ('FOUND MATERIAL COLUMN')
        else:
            print(f'Error: Table{table_name} not found in metadata.tables')

session.close()        
   
