from grid import *
from layout import Layout

class Occupant:
	"""The occupant of a block of cells."""

	patterns = {
			1: ( RectangleSize(rows = 1, columns = 1), ),
			2: ( RectangleSize(2, 1), RectangleSize(1, 2) ),
			3: ( RectangleSize(3, 1), RectangleSize(1, 3) ),
			4: ( RectangleSize(4, 1), RectangleSize(1, 4), RectangleSize(2, 2) ),
			5: ( RectangleSize(5, 1), RectangleSize(1, 5) ),
			6: ( RectangleSize(6, 1), RectangleSize(1, 6), RectangleSize(3, 2), RectangleSize(2, 3) ),
			7: ( RectangleSize(7, 1), RectangleSize(1, 7) ),
			8: ( RectangleSize(8, 1), RectangleSize(1, 8), RectangleSize(4, 2), RectangleSize(2, 4) ),
	}


	def __init__(self, volume):
		if volume < 1 or volume > max(Occupant.patterns.keys()):
			raise Exception(f"Occupant volume '{volume}' must be between 1 and {max(Occupant.patterns.keys())}.")

		self.volume = volume
		"""How many cells this occupant consumes."""

		self.grid: Grid = None
		"""The grid where this occupant resides."""

		self.anchor: Location = None
		"""The anchored location of this occupant in the cell grid."""

		self.is_secure: bool = False
		"""Whether this occupant has been assigned and claims a specific layout in the grid."""

		self.layouts = []
		"""All the ways that this occupant may be able to occupy its volume."""


	def assign_to_grid(self, grid: Grid, row_index: int, column_index: int):
		"""Assign this occupant to a location in a grid."""
		if self.grid or self.layouts:
			raise Exception("This occupant has already been assigned to a grid.")

		self.grid = grid

		self.anchor = Location(row_index, column_index)
		self.grid.assign_occupant(self, row_index, column_index)

		self.assign_possible_layouts()
		if not self.layouts:
			raise Exception("Unable to assign occupant to grid because no possible layouts were discovered.")


	def assign_possible_layouts(self):
		"""Determine possible layouts as allowed by the bounds of the grid."""
		if self.layouts:
			raise Exception("Layouts have already been assigned for this occupant.")
		
		for pattern in Occupant.patterns[self.volume]:
			self.assign_layouts_for_pattern(pattern)


	def assign_secure_layout(self, layout):
		"""Claim one of this occupant's layouts, and abandon its other possible layouts."""
		if layout not in self.layouts:
			raise Exception("Specified layout to secure is not already in the set of possible layouts.")

		# skip anchor b/c assert it is already assigned:
		for cell in layout.cells:
			if cell != self.anchor:
				self.grid.assign_occupant(self, cell.row_index, cell.column_index)

		self.layouts[:] = [layout];
		self.is_secure = True


	def assign_layouts_for_pattern(self, pattern: RectangleSize):
		"""Determine possible layouts of a pattern, within the grid."""

		# compute the min & max indexes for the *top-left corner* of the layout
		# min values are bounded by the grid wall adjacent to index 0
		# max values are bounded by the distance that the layout must extend
		#  from the wall into the grid (because if any part of the layout would
		#  fall outside the grid, it's not a viable layout)
		colmin_index = max(
				self.anchor.column_index - pattern.columns + 1,
				0)
		colmax_index = min(
				self.anchor.column_index,
				self.grid.column_count - pattern.columns)

		rowmin_index = max(
				self.anchor.row_index - pattern.rows + 1,
				0)
		rowmax_index = min(
				self.anchor.row_index,
				self.grid.row_count - pattern.rows)

		for topleft_row in range(rowmin_index, rowmax_index + 1):
			for topleft_col in range(colmin_index, colmax_index + 1):
				self.layouts.append(Layout(
						Location(topleft_row, topleft_col),
						RectangleSize(pattern.rows, pattern.columns)))
