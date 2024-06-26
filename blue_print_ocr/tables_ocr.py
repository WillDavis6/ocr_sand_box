import sys
from sqlalchemy import create_engine, Column, Integer, String, Table, desc, MetaData, inspect, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from colorama import Fore, init
from sqlalchemy.exc import IntegrityError

# Add custom path to sys.path
sys.path.append("C:\\Users\\William.davis\\Desktop\\python_data_set")

# Initialize colorama
init(autoreset=True)

# Database URI
DATABASE_URI = 'postgresql+psycopg2://postgres:Msi_123@localhost:5432/portal_data_base?client_encoding=utf8'

blueprint_list = [
    "C:\\Users\\William.davis\\Desktop\\python_data_set\\static\\blueprints\\35-8227_01.png",
    "C:\\Users\\William.davis\\Desktop\\python_data_set\\static\\blueprints\\35-8227_02.png",
    "C:\\Users\\William.davis\\Desktop\\python_data_set\\static\\blueprints\\35-8227_03.png",
    "C:\\Users\\William.davis\\Desktop\\python_data_set\\static\\blueprints\\35-8227_04.png",
    "C:\\Users\\William.davis\\Desktop\\python_data_set\\static\\blueprints\\35-8227_5.png",
    "C:\\Users\\William.davis\\Desktop\\python_data_set\\static\\blueprints\\35-8227_6.png",
    "C:\\Users\\William.davis\\Desktop\\python_data_set\\static\\blueprints\\35-8227_7.png",
    "C:\\Users\\William.davis\\Desktop\\python_data_set\\static\\blueprints\\35-8227_8.png",
    "C:\\Users\\William.davis\\Desktop\\python_data_set\\static\\blueprints\\35-8227_9.png"
]

export_url = "C:\\Users\\William.davis\\OneDrive - msiGCCH\\Pictures\\Screenshots\\test_updated_image_cv2.png"

tables_list = ['comp_table', 'dynamic_table_0', 'dynamic_table_1', 'dynamic_table_2', 'dynamic_table_3', 'dynamic_table_4', 'dynamic_table_5', 'dynamic_table_6', 'dynamic_table_7', 'dynamic_table_8']


# Create an engine and metadata instance
engine = create_engine(DATABASE_URI)
metadata = MetaData()
Base = declarative_base()



# Define CompTable model
class CompTable(Base):
    __tablename__ = 'comp_table'

    id = Column(Integer, primary_key=True, autoincrement=True)
    part_id = Column(String(100))
    material = Column(String(100))

# Create a session factory
Session = sessionmaker(bind=engine)
session = Session()



# Define DynamicTable class with a class method to create tables dynamically
class DynamicTable(Base):
    __tablename__ = 'dynamic_table'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)

    @classmethod
    def create_table(cls, num_columns, i, metadata, engine):
        table_name = f"dynamic_table_{i}"
        columns = {'id': Column(Integer, primary_key=True)}

        for j in range(num_columns):
            column_name = f"column_{j+1}"
            columns[column_name] = Column(String(255))

        table_class = type(table_name, (Base,), {
            '__tablename__': table_name,
            '__table_args__': {'extend_existing': True},
            **columns
        })

        setattr(sys.modules[__name__], table_name, table_class)

        #table_class.__table__.metadata = metadata
        table_class.__table__.create(bind=engine)
        metadata.reflect(bind=engine)

        print(Fore.GREEN + f'INITIATE --> CREATED TABLE: {table_name}')
        return table_class

# Function to add a row to a table
def add_row(row_values, table, session):
    try:
        new_row = table()
        for i, value in enumerate(row_values):
            setattr(new_row, f"column_{i}", value)
        session.add(new_row)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f'Error adding row: {e}')


        
def find_columns(last_row, table):
    part_num_data = None
    material_data = None

    for column in table:

        #Convert cell value into workable string
        string = str(getattr(last_row, column.name))

        #If Part column is found
        if 'PART' in string:
            target_column = column.name

            #print(Fore.BLUE + f'FOUND PART NUMBER COLUMN: {string}. PART NUMBER: {column.name}')

            part_num_data = session.query(getattr(table, target_column)).all()

        # else:
        #     part_num_data = None

        if 'MAT' in string:
            target_column = column.name
            #print(Fore.BLUE + f'FOUND MATERIAL COLUMN: {string}. COLUMN NAME: {target_column}')

            material_data = session.query(getattr(table, target_column)).all()

        # else: material_data = None

    return part_num_data, material_data







# Example usage of DynamicTable
if __name__ == "__main__":
    from ocr_optimization_testing import ocr_magic, drop_tables

    # Drop and recreate all tables defined by Base
    drop_tables(tables_list, metadata, engine, Fore, inspect, text)

    # Auto create the compiled table during each run
    CompTable.__table__.create(bind=engine)
    print(Fore.GREEN + 'comptable created')


    # Iterate over list of blueprint screen shots
    for i, blueprint_url in enumerate(blueprint_list):


        #Run ocr_magic funciton including all background functions to preprocess and pull data from screenshots, return sql table name created
        table_name = ocr_magic(blueprint_url, export_url, 20, 500, 4, i, metadata, engine, Session)

        #If said created table is in metadata contiune
        try:

            if table_name in metadata.tables:

                #pull table data from metadata
                table = metadata.tables[table_name]

                #query in session the data from table in descending order
                query = session.query(table).order_by(desc(table.c.id)).limit(1)
                
                #query the first row which is really the last row (We are searching for the column names)
                last_row = query.one()
            
                #Iterate over the columns (We will be searching for the Material and Part Number columns)
                part_num_data, material_data = find_columns(last_row, table.c)

                #Iterate over both lists in tandem
                if part_num_data and material_data:
                    for part_num, material in zip(part_num_data, material_data):

                        mat = material[0]
                        part_id = None

                        #Extract applicable data from values
                        if not part_num[0]:

                            part_id = None
                        elif len(part_num[0]) <= 4: 
                            part_id = f'35-8227-{part_num[0]}'
                            
                        else:
                            part_id = part_num[0]

                        #Fill new row with captured data (Primary key will be a sequncial integer)
                        new_row = CompTable(part_id=part_id, material=mat)
                        session.add(new_row)

                else:
                    print(Fore.RED + f'Something Wrong With part_num_data or material_data')

           
                session.commit()
                print(Fore.GREEN + 'Session Changes Committed')

                TABLE_NAME = tables_list[0]
                OUTPUT_FILE = "C:\\Users\\William.davis\\Desktop\\python_data_set\\blue_print_ocr\\g_vision_test.py"            

                table = Table(TABLE_NAME, metadata, autoload=True, autoload_with=engine)

                with engine.connect() as connection:
                    result = connection.execute(table.select())

                    with open(OUTPUT_FILE, "w", encoding='utf-8') as file:

                        file.write('\t'.join(table.columns.keys()) + '\n')

                        for row in result:
                            row_values = [str(value) for value in row]
                            file.write("\t".join(row_values) + '\n')

            else:
                print(Fore.RED + f'Error: Table {table_name} not found in metadata.tables')

        except IntegrityError as e:
                session.rollback()
                print(Fore.RED + f'Error committing changes: {e}')

   
    session.close()





            
          







