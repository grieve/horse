import sqlobject


class Base(sqlobject.SQLObject):
    created = sqlobject.DateTimeCol(default=sqlobject.DateTimeCol.now())
