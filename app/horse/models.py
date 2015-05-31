import sqlobject


class Base(sqlobject.SQLObject):
    created = sqlobject.DateTimeCol(default=sqlobject.DateTimeCol.now())


class User(Base):
    string_id = sqlobject.StringCol()
    username = sqlobject.StringCol()
    real_name = sqlobject.StringCol()
    image = sqlobject.StringCol()

    def __str__(self):
        return self.string_id


class Channel(Base):
    string_id = sqlobject.StringCol()
    name = sqlobject.StringCol()

    def __str__(self):
        return self.string_id
