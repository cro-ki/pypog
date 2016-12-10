'''
Created on 5 dec. 2016
    Pencil classes allow you to get an evolving selection of coordinates, according to the type of pencil you use.
    
    Start it, set size (default: 1), update it as many times you want with new positions on the grid, then
    get the list of selected coordinates, or the list of added / removed coorinates by the last update.
    
    Connect those functions to your graphical grid, and let it do the job.
    
    Example of use:
        On mouse left button down on a (x, y) cell: pencil.start(x, y)
        On hover event on cells: pencil.update(), then display the result on your grid
        On mouse left button up: Apply the modification on your grid, then delete your pencil object
        
@author: olinox
'''
from abc import ABCMeta

from prompt_toolkit import selection

from pypog import geometry
from pypog.Grid import HexGrid


class BasePencil(object):
    """Base class of all pencils
    This is an abstract class: override it!"""
    __metaclass__ = ABCMeta
    
    def __init__(self, grid):
        
        # do we really need the grid ref? cell_shape could be enough?
        self._grid = grid
        
        self._origin = None
        self._position = None
        self._positions_history = []
        
        self._size = 1
        self._selection = set()

        self._added = set()
        self._removed = set()

    @property
    def origin(self):
        """returns the coordinates of the cell where the painting began
        This property is read-only: use the 'start' method to set it"""
        return self._origin

    @property
    def size(self):
        """returns the current size of the pencil"""
        return self._size

    @size.setter
    def size(self, size):
        """sets the current size of the pencil
        size has to be a strictly positive integer"""
        if not isinstance(size, int):
            raise TypeError("size has to be an integer (given: {})".format(size))
        if not size > 0:
            raise ValueError("size has to be strictly positive (given: {})".format(size))
        self._size = size

    @property
    def position(self):
        """returns the current (x, y) position of the pencil
        This property is read-only: use the 'update' method to give it a new value"""
        return self._position

    @property
    def selection(self):
        """return the current list of coordinates selected by the pencil (read-only)"""
        return list( self._selection )
        
    @property
    def added(self):
        """return the list of coordinates added to the last selection by the last update (read-only)
        
        This property exists for performances reasons: you probably don't want to update your whole graphic scene if 
        just one or two cells where added or removed from the selection!
        """
        return list( self._added )

    @property
    def removed(self):
        """return the list of coordinates removed from the last selection by the last update (read-only)
                
        This property exists for performances reasons: you probably don't want to update your whole graphic scene if 
        just one or two cells where added or removed from the selection!
        """
        return list( self._removed )

    def _update(self):
        """this method update the selection, added and removed lists, according to the current size, position, origin
        Override it to create your own pencil"""
        # this method should be overrided to update : self._selection, self._added, self._removed
        raise NotImplementedError("_update method has to be overrided")

    def start(self, x0, y0):
        """start a new painting
        (x0, y0) is the origin of the painting, and will not be modified."""
        if len(self._selection) > 0:
            raise Exception("the pencil has already been started")
        self._origin = (x0, y0)
        self.update(x0, y0)

    def update(self, x, y):
        """Updates the current position of the pencil
        If (x, y) is not in the position's history, it updates the current selection, and the added / removed lists."""
        if not all(isinstance(var, int) for var in (x, y)):
            raise TypeError("x, y has to be an integers (given: {})".format((x, y)))
        if self._origin == None:
            raise Exception("Pencil has to be started before any update: use 'start' method")
        self._position = (x, y)
        if not (x, y) in  self._positions_history:
            self._positions_history.append( (x, y) )
            self._update()
        
class LinePencil(BasePencil):
    """Paint a 2d line between origin and position"""
    def __init__(self, *args):
        BasePencil.__init__(self, *args)
        
    def _update(self):
        x0, y0 = self._origin
        x, y = self._position
        
        # use a set because of performance (should we generalize the use of sets for coordinates lists?)
        result = set([])
        
        line = set( geometry.line2d(self._grid.cell_shape, x0, y0, x, y) )
        
        # apply size with geometry.zone
        for x, y in line:
            result |= set( geometry.zone(self._grid.cell_shape, x, y, self.size) )
        
        self._added = result - self._selection
        self._removed = self._selection - result
        self._selection = result


class SimplePencil(BasePencil):
    """Free handed pencil"""
    def __init__(self, *args):
        BasePencil.__init__(self, *args)
        
    def _update(self):
        x, y = self.position
        zone_set = set( geometry.zone(self._grid.cell_shape, x, y, self.size) )

        self._added = zone_set - self._selection
        # there can't be any removed coordinates with this pencil
        self._selection = self._selection + zone_set
        
        
class PaintPotPencil(BasePencil):
    """This particular pencil selects all cells of same nature from nearest to nearest
    
    The 'same nature' is confirmed by passing a comparaison method to the pencil
    This method should take x1, y1, x2, y2 as args, and return a boolean: True for similar cells, False in other case
    
    WARNING: this pencil result is not modified by the update method, because the result is already defined when it starts
    
    WARNING 2: take care of what you put in your comparing method, it could end with a infinite loop if you are not working on a finite grid!
    
    example of use:
        
        # your comparison function
        my_grid = HexGrid(30,30)
        
        def identical_cells_function(x1, y1, x2, y2):
            if my_grid.cell(x1, y1).color == my_grid.cell(x2, y2).color:
                return True
            return False
            
        my_pencil = PaintPotPencil(my_grid)
        my_pencil.start(3, 3, identical_cells_function)
        
        print(my_pencil.selection)
    
    """
    
    def __init__(self, *args):
        BasePencil.__init__(self, *args)
        self._comparing_method = (lambda x: False)

    def start(self, x0, y0, comparing_method_pointer):
        self._comparing_method_pointer = comparing_method_pointer
        BasePencil.start(self, x0, y0)

    def update(self, *args):
        if not len(self._selection) > 0:
            BasePencil.update(self, *args)

    @property
    def added(self):
        return self._selection

    def _update(self):
        x0, y0 = self._origin 
        current_selection = { (x0, y0) }
        buffer = set( geometry.neighbours_of(self._grid._cell_shape, x0, y0) )
        
        while len(buffer) > 0:
            x, y = buffer.pop()
            if self._comparing_method_pointer(x0, y0, x, y):
                current_selection.add( (x, y) )
                buffer |= ( set( geometry.neighbours_of(self._grid._cell_shape, x, y) ) - current_selection)
                
        self._selection = current_selection
        
        



