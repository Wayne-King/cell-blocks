from dataclasses import *
from grid import *

# this type is logically and effectively immutable, and would prefer to
#  specify the frozen=True parameter; however, that fails -- even
#  __post_init__ is not allowed to update fields !?  Then must use
#  unsafe_hash to get a hash method, and immutability is on honor system.
@dataclass(unsafe_hash=True)
class Layout:
	"""Indicates a set of cells in a grid that an occupant may occupy."""

	top_left: InitVar[Location]
	size: InitVar[RectangleSize]

	cells: frozenset = field(init=False)


	def __post_init__(self, top_left, size):
		self.cells = frozenset(
				[Location(row_index, column_index)
				for row_index in range(
						top_left.row_index,
						top_left.row_index + size.rows)
					for column_index in range(
							top_left.column_index,
							top_left.column_index + size.columns)] )
