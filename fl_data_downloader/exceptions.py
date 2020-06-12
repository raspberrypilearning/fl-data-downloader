class NeedToLoginException(Exception):
    pass

class DatasetNotKnownException(Exception):
    pass

class DatasetNotFoundForCourse(Exception):
    pass

class CourseRunNotFound(Exception):
    pass

class ConnectionErrorMaxRetriesExceeded(Exception):
    pass