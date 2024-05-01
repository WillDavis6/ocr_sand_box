from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import psycopg2

# Create an engine and connect to a PostgreSQL database
engine = create_engine('postgresql+psycopg2://postgres:Msi_123@localhost:5432/portal_data_base')
Base = declarative_base()

Base.metadata.bind = engine

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

        # Create the table
        Base.metadata.create_all(engine)
        print(f'CREATED TABLE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

        return table


def build_dynamic_table(width, height):
    print(f'STARTING TABLE BUILD!!!!!!!!!!!!!!!!!!!!!!  WIDTH IS: {width}  HEIGHT IS: {height}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

    if __name__ == "__main__":
        # Connect to the database
        connection = engine.connect()
        print(f'START YOU ENGINES !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

        # Create a table with 3 rows and 4 columns
        DynamicTable.create_table(width, height)

        # Test querying the created table
        rows = connection.execute(DynamicTable.__table__.select()).fetchall()
        print(rows)

        # Close the connection
        connection.close()

   
