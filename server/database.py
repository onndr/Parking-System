import sqlalchemy
import urllib


class Database:
    SELECT_ALL_SPACES = '''SELECT * FROM ParkingSpaces'''
    SELECT_SPACE_BY_ID ='''SELECT * FROM ParkingSpaces WHERE ParkingId = {ParkingId} AND ParkingSpaceId = {ParkingSpaceId}'''
    SELECT_ALL_PARKINGS = '''SELECT * FROM Parkings'''
    SELECT_SPACES_BY_PARKING_ID ='''SELECT * FROM ParkingSpaces WHERE ParkingId = {ParkingId}'''

    SELECT_PARKING_BY_ID = '''SELECT * FROM Parkings WHERE ParkingId = {Id}'''

    UPDATE_PARKING_SPACE_IS_TAKEN = '''UPDATE ParkingSpaces SET IsTaken = {IsTaken} WHERE ParkingId = {ParkingId} AND ParkingSpaceId = {ParkingSpaceId}'''

    COUNT_FREE_PARKING_SPACES_BY_PARKING_ID = '''SELECT COUNT(id) FROM ParkingSpaces WHERE ParkingId = {ParkingId} AND IsTaken = 0'''
    COUNT_ALL_FREE_PARKING_SPACES = '''SELECT COUNT(id) FROM ParkingSpaces WHERE IsTaken = 0'''

    params = urllib.parse.quote_plus(r'DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:zerojeden-server.database.windows.net;DATABASE=parkingDB;Uid=xxxx;Pwd=xxxx;')
    CONNECTION_STRING = 'mssql+pyodbc:///?odbc_connect={}'.format(params)

    def __init__(self):
        self._engine = sqlalchemy.create_engine(Database.CONNECTION_STRING)

    def execute(self, command):
        return self._engine.execute(command)

    def get_all_parkings(self):
        cursor = self.execute(Database.SELECT_ALL_PARKINGS)
        return cursor.fetchall()

    def get_parking_by_id(self, parking_id):
        command = Database.SELECT_PARKING_BY_ID.format(Id=parking_id)
        cursor = self.execute(command)
        return cursor.fetchall()

    def get_all_parking_spaces(self):
        cursor = self.execute(Database.SELECT_ALL_SPACES)
        return cursor.fetchall()

    def get_parking_space_by_id(self, parking_id, parking_space_id):
        command = Database.SELECT_SPACE_BY_ID.format(ParkingId=parking_id, ParkingSpaceId=parking_space_id)
        cursor = self.execute(command)
        return cursor.fetchall()

    def update_parking_space_is_taken(self, parking_id, parking_space_id, is_taken):
        command = Database.UPDATE_PARKING_SPACE_IS_TAKEN.format(ParkingId=parking_id, ParkingSpaceId=parking_space_id, IsTaken=is_taken)
        try:
            self.execute(command)
            return True
        except Exception:
            return False

    def get_parking_spaces_by_parking_id(self, parking_id):
        command = Database.SELECT_SPACES_BY_PARKING_ID.format(ParkingId=parking_id)
        cursor = self.execute(command)
        return cursor.fetchall()

    def get_number_of_free_spaces_by_parking_id(self, parking_id):
        command = Database.COUNT_FREE_PARKING_SPACES_BY_PARKING_ID.format(ParkingId=parking_id)
        cursor = self.execute(command)
        return cursor.fetchone()

    def get_number_of_all_free_spaces(self):
        command = Database.COUNT_ALL_FREE_PARKING_SPACES
        cursor = self.execute(command)
        return cursor.fetchone()
