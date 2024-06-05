import sys
from sqlalchemy import create_engine, Column, Integer, String, Table, desc, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from colorama import Fore, init
from sqlalchemy.exc import IntegrityError

# Add custom path to sys.path
sys.path.append("C:\\Users\\William.davis\\Desktop\\python_data_set")

# Initialize colorama
init(autoreset=True)

# Database URI
DATABASE_URI = 'postgresql+psycopg2://postgres:Msi_123@localhost:5432/portal_data_base'

# Create an engine and metadata instance
engine = create_engine(DATABASE_URI)
metadata = MetaData()
Base = declarative_base()

# Drop and recreate all tables defined by Base
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

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
    for column in table:

                

        #Convert cell value into workable string
        string = str(getattr(last_row, column.name))

        #If Part column is found
        if 'PART' in string:
            target_column = column.name

            print(Fore.BLUE + f'FOUND PART NUMBER COLUMN: {string}. PART NUMBER: {column.name}')

            part_num_data = session.query(getattr(table, target_column)).all()

        else:
            part_num_data = None

        if 'MAT' in string:
            target_column = column.name
            print(Fore.BLUE + f'FOUND MATERIAL COLUMN: {string}. COLUMN NAME: {target_column}')

            material_data = session.query(getattr(table, target_column)).all()

        else: material_data = None

    return part_num_data, material_data







# Example usage of DynamicTable
if __name__ == "__main__":
    from ocr_optimization_testing import ocr_magic

    blueprint_list = [
        "C:\\Users\\William.davis\\Desktop\\python_data_set\\static\\blueprints\\35-8227 ALL COMBINED_Page_01.jpg",
        "C:\\Users\\William.davis\\Desktop\\python_data_set\\static\\blueprints\\35-8227 ALL COMBINED_Page_02.jpg",
        "C:\\Users\\William.davis\\Desktop\\python_data_set\\static\\blueprints\\35-8227 ALL COMBINED_Page_24.jpg",
        "C:\\Users\\William.davis\\Desktop\\python_data_set\\static\\blueprints\\35-8227 ALL COMBINED_Page_25.jpg",
        "C:\\Users\\William.davis\\Desktop\\python_data_set\\static\\blueprints\\35-8227 ALL COMBINED_Page_26.jpg"
    ]

    export_url = "C:\\Users\\William.davis\\OneDrive - msiGCCH\\Pictures\\Screenshots\\test_updated_image_cv2.png"



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

                print(f'This is part_num_data{part_num_data}. This is material_data{material_data}')

                #Iterate over both lists in tandem
                if part_num_data and material_data:
                    for part_num, material in zip(part_num_data, material_data):

                        #Extract applicable data from values
                        part_id = f'35-8227-{part_num[0]}'
                        mat = material[0]

                        #Fill new row with captured data (Primary key will be a sequncial integer)
                        new_row = CompTable(part_id=part_id, material=mat)

                        session.add(new_row)

                else:
                    print(Fore.RED + f'Something Wrong With part_num_data or material_data')

           
                session.commit()
                print(Fore.GREEN + 'Session Changes Committed')

            else:
                print(Fore.RED + f'Error: Table {table_name} not found in metadata.tables')

        except IntegrityError as e:
                session.rollback()
                print(Fore.RED + f'Error committing changes: {e}')

            

    session.close()

            
          









    #         for column in table.c:
    #             string = str(getattr(last_row, column.name))

    #             if 'PART' in string:
    #                 target_column = column.name
    #                 print(Fore.BLUE + f'FOUND PART NUMBER COLUMN: {string}. PART NUMBER: {target_column}')

    #                 part_num_column_data = session.query(getattr(table.c, target_column)).all()

    #                 for data in part_num_column_data:
    #                     part_id = f'35-8227-{data[0]}'

                     
    #                     if not session.query(CompTable).filter_by(part_id=part_id).first():
                            
    #                         print(Fore.CYAN + f'Adding Data {part_id}')
                            
    #                         new_row = CompTable(part_id=part_id)
    #                         session.add(new_row)
    #                     else:
    #                         print(Fore.YELLOW + f'Duplicate entry found: {part_id}, skipping insertion.')

    #             session.commit()
    #             print(Fore.GREEN + f'Part Number Information Committed')

    #             if 'MAT' in string:
    #                 target_column = column.name
    #                 print(Fore.BLUE + f'FOUND MATERIAL COLUMN: {string}. COLUMN NAME: {target_column}')

    #                 mat_column_data = session.query(getattr(table.c, target_column)).all()

    #                 print(Fore.CYAN + 'Session data added?')

    #                 for data in mat_column_data:
                        
    #                     print(Fore.CYAN + f'Adding Data {data[0]}')
                        
    #                     new_row = session.query(CompTable).filter_by(part_id=f'35-8227-{data[0]}').first()
    #                     if new_row:
    #                         new_row.material = data[0]
    #                     else:
    #                         new_row = CompTable(material=data[0])
    #                         session.add(new_row)

    #         try:
    #             session.commit()
    #             print(Fore.GREEN + 'Session Changes Committed')
    #         except IntegrityError as e:
    #             session.rollback()
    #             print(Fore.RED + f'Error committing changes: {e}')
    #     else:
    #         print(Fore.RED + f'Error: Table {table_name} not found in metadata.tables')

    # session.close()






#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# import sys
# sys.path.append("C:\\Users\\William.davis\\Desktop\\python_data_set")

# from sqlalchemy import create_engine, Column, Integer, String, Table, select, desc, MetaData
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base


# from colorama import Fore, init

# init(autoreset=True)


# # Create an engine and connect to a PostgreSQL database

# engine = create_engine('postgresql+psycopg2://postgres:Msi_123@localhost:5432/portal_data_base')

# Base = declarative_base()
# metadata = MetaData()

# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)

# class DynamicTable(Base):
#     __tablename__ = 'dynamic_table'
#     __table_args__ = {'extend_existing' :True}
#     id = Column(Integer, primary_key=True)


#     @classmethod
#     def create_table(cls, num_columns, i, metadata, engine):
#         table_name = f"dynamic_table_{i}"
#         columns = {'id': Column(Integer, primary_key=True)}
        


#         for j in range(num_columns):
#             column_name = f"column_{j+1}"
#             columns[column_name] = Column(String(255))

#         table_class = type(table_name, (Base,), {
#             '__tablename__': table_name,
#             '__table_args__': {'extend_existing': True},
#             **columns
#         })

#         table_class.__table__.metadata = metadata
#         Base.metadata.create_all(engine)
#         metadata.reflect(engine)
       
#         print(Fore.GREEN + f'INITIATE --> CREATED TABLE: {table_name}')

#         return table_class
    




# def add_row(row_values, table, session):

#     try:
#         new_row = table()

     

#         for i, value in enumerate(row_values):
#             setattr(new_row, f"column_{i}", value)

#         session.add(new_row)

#         session.commit()
#         #print(f'Row {i} added successfully!')
#     except Exception as e:
#         session.rollback()
#         print(f'Error adding row: {e}')

   
# class CompTable(Base):
#     __tablename__ = 'comp_table'

#     part_id = Column(String(100), primary_key=True)
#     material = Column(Integer)


# Session = sessionmaker(bind=engine)
# session = Session()
# metadata = MetaData()



# export_url = "C:\\Users\\William.davis\\OneDrive - msiGCCH\\Pictures\\Screenshots\\test_updated_image_cv2.png"

# blueprint_list = ["C:\\Users\\William.davis\\Desktop\\python_data_set\\static\\blueprints\\35-8227 ALL COMBINED_Page_01.jpg", "C:\\Users\\William.davis\\Desktop\\python_data_set\\static\\blueprints\\35-8227 ALL COMBINED_Page_02.jpg", "C:\\Users\\William.davis\\Desktop\\python_data_set\\static\\blueprints\\35-8227 ALL COMBINED_Page_24.jpg", "C:\\Users\\William.davis\\Desktop\\python_data_set\\static\\blueprints\\35-8227 ALL COMBINED_Page_25.jpg", "C:\\Users\\William.davis\\Desktop\\python_data_set\\static\\blueprints\\35-8227 ALL COMBINED_Page_26.jpg"]


# if __name__ == "__main__":
#     from ocr_optimization_testing import ocr_magic
    
#     for i, blueprint_url in enumerate(blueprint_list):
#         table_name = ocr_magic(blueprint_url, export_url, 20, 500, 4, i, metadata, engine, Session)

        

#         if table_name in metadata.tables:
#             table = metadata.tables[table_name]
#             query = session.query(table).order_by(desc(table.c.id)).limit(1)
#             last_row = query.one()
#             target_column = None

#             for column in table.c:
#                 string = str(getattr(last_row, column.name))

#                 if 'PART' in string:
#                     target_column = column.name
#                     print (Fore.BLUE + f'FOUND PART NUMBER COLUMN: {string}. PART NUMBER: {target_column}')

#                     part_num_column_data = session.query(getattr(table.c, target_column)).all()

                    

#                     for data in part_num_column_data:
#                         print(Fore.CYAN + f'Adding Data 35-8227-{data[0]}')
#                         new_row = CompTable(part_id=f'35-8227-{data[0]}')
#                         session.add(new_row)


#                 if 'MAT' in string:
#                     target_column = column.name
#                     print (Fore.BLUE + f'FOUND MATERIAL COLUMN: {string}. COLUMN NAME: {target_column}')

#                     mat_column_data = session.query(getattr(table.c, target_column)).all()

#                     print(Fore.CYAN + 'Session data added?')

#                     for data in part_num_column_data:
#                         print(Fore.CYAN + f'Adding Data {data}')
#                         new_row = CompTable(material=data[0])
#                         session.add(new_row)

#             session.commit()
#             print(Fore.GREEN + 'Session Changes Commited')
                    

              
                
#         else:
#             print(Fore.RED + f'Error: Table{table_name} not found in metadata.tables')

# session.close()        
   
