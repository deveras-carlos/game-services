from .base_repository import BaseRepository
from .menu_text_repository import MenuTextRepository

class ManagerRepository:
    _menu_text_repository : MenuTextRepository = None

    _repositories = dict(  )

    @staticmethod
    def get_repository_from_model( model ):
        key = f"{ model.__name__ }_GenericRepository"
        if key in ManagerRepository._repositories:
            return ManagerRepository._repositories[ key ]
        class GenericRepository( BaseRepository ):
            def __init__( self ):
                super(  ).__init__( model )
                ManagerRepository._repositories[ key ] = self
        return GenericRepository(  )

    @staticmethod
    def get_menu_text_repository(  ) -> MenuTextRepository:
        if ManagerRepository._menu_text_repository is None:
            ManagerRepository._menu_text_repository = MenuTextRepository(  )
        ManagerRepository._repositories[ "MenuTextRepository" ] = ManagerRepository._menu_text_repository
        return ManagerRepository._menu_text_repository