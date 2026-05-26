class GridNotSupportedException(Exception):
    def __init__(self, message: str):
        self.message = message
        self.__class__.__module__ = 'Maze'
        super(GridNotSupportedException, self).__init__(message)