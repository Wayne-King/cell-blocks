import itertools
from collections import namedtuple
from typing import NamedTuple


RectangleSize = namedtuple('RectangleSize', 'rows columns')

Location = namedtuple('Location', 'row_index column_index')


class Grid:
	"""A rectangular (or square) matrix of cells."""

	def __init__(self, row_count: int, column_count: int):
		self.row_count: int = row_count
		self.column_count: int = column_count
		self.grid = [
			[None for cell in range(self.column_count)]
				for row in range(self.row_count)]

	def occupant_of(self, row_index, column_index):
		"""Gets the occupant of a specified location."""
		return self.grid[row_index][column_index]

	def assign_occupant(self, occupant, row_index, column_index):
		"""Assigns an occupant to a specified location."""
		self.grid[row_index][column_index] = occupant

	def get_vacant_cells(self) -> set:
		"""Returns the set of grid locations that are not assigned to an occupant."""
		return { Location(row_index, column_index)
				for column_index in range(self.column_count)
					for row_index in range(self.row_count)
						if not self.grid[row_index][column_index] }
