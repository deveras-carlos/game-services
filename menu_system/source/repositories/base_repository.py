from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, text
from config.database import Database

class BaseRepository:
    def __init__(self, model):
        self.model = model

    def get_all(self, order_by = None, descending=False):
        db = Database.get_db()
        if order_by:
            order_clause = order_by.desc() if descending else order_by
            selection = select(self.model).order_by(order_clause)
        else:
            selection = select(self.model)
        
        query = db.session.execute( selection )
        return query.scalars().all()

    def get_by_id(self, id):
        db = Database.get_db()
        query = db.session.execute(
            select(self.model)
            .where(self.model.id == id)
        )
        return query.scalars().first()

    def find_all_by(self, **kwargs):
        db = Database.get_db()
        conditions = [getattr(self.model, k) == v for k, v in kwargs.items()]
        query = db.session.execute(select(self.model).where(*conditions))
        return query.scalars().all()

    def find_first_by(self, **kwargs):
        db = Database.get_db()
        conditions = [getattr(self.model, k) == v for k, v in kwargs.items()]
        query = db.session.execute(select(self.model).where(*conditions))
        return query.scalars().first()

    def save(self, entity):
        db = Database.get_db()
        self.before_save(entity)
        try:
            db.session.add(entity)
            db.session.commit()
            self.after_save(entity)
            return entity
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error saving entity: {e}")
            raise

    def delete(self, entity):
        db = Database.get_db()
        try:
            db.session.delete(entity)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error deleting entity: {e}")
            raise

    def count(self):
        db = Database.get_db()
        return db.session.query(self.model).count()

    def count_by(self, **kwargs):
        db = Database.get_db()
        query = db.session.query(self.model).filter_by(**kwargs)
        return query.count()

    def update(self, entity, **kwargs):
        db = Database.get_db()
        try:
            for attr, value in kwargs.items():
                setattr(entity, attr, value)
            db.session.commit()
            return entity
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error updating entity: {e}")
            raise

    def bulk_save(self, entities, lookup_field: str = None):
        db = Database.get_db()
        try:
            db.session.add_all(entities)
            db.session.commit()
            return entities
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error in bulk save: {e}")
            raise

    def bulk_delete(self, entities):
        db = Database.get_db()
        try:
            for entity in entities:
                db_entity = self.get_by_id(entity.id)
                if db_entity is not None:
                    db.session.delete(entity)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error in bulk delete: {e}")
            raise

    def execute_raw_sql(self, sql, params=None):
        db = Database.get_db()
        try:
            result = db.session.execute(text(sql), params or {})
            db.session.commit()
            return result
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error executing raw SQL: {e}")
            raise

    def before_save(self, entity):
        # Can be overridden by subclasses to perform actions before save
        return entity

    def after_save(self, entity):
        # Can be overridden by subclasses to perform actions after save
        return entity