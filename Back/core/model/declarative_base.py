from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    repr_column_num: int = 3
    repr_column: tuple = ()

    def __repr__(self):
        cols = []
        for id_, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_column or id_ < self.repr_column_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"\n* {self.__class__.__name__} {', '.join(cols)} *\n"
