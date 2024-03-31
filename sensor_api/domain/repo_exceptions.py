#General DB Exceptions
class PrimaryKeyConstraint(Exception):
    pass

class DBUnkownException(Exception):
    pass

#Sensor Related Exceptions
class SensorDoesNotExist(Exception):
    pass

class SensorIDMismatch(Exception):
    pass

#Sensor Data Related Exceptions
class DataDoesNotExist(Exception):
    pass

class DataIDMismatch(Exception):
    pass

class DateWrongFormat(Exception):
    pass

#User Related Exceptions
class UserDoesNotExist(Exception):
    pass

