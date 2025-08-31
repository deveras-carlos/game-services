from models import MenuTextModel
from .base_repository import BaseRepository

class MenuTextRepository( BaseRepository ):
    def __init__( self ):
        super(  ).__init__( MenuTextModel )