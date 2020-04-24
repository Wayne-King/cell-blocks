from grid import *
from occupant import Occupant


OccupantLayout = namedtuple('OccupantLayout', 'occupant layout')


class CellFacility:
	"""A place containing a grid of cells, cell blocks, occupants, and related."""

	def __init__(self, row_count: int, column_count: int):
		self.grid = Grid(row_count = 7, column_count = 7)
		self.occupants = []


	def assign_occupant(self, row_index, column_index, volume):
		"""Create an occupant and assign it to a location in the grid."""

		if self.grid.occupant_of(row_index, column_index) is not None:
			raise Exception(f"An occupant is already assigned to row & column index ({row_index}, {column_index}).")

		occupant = Occupant(volume)
		occupant.assign_to_grid(self.grid, row_index, column_index)

		self.occupants.append(occupant)


	def abandon_nonisolating_layouts(self):
		"""Abandon occupants' layouts that intrude upon another occupant's anchor cell."""
		all_anchors = frozenset({ occupant.anchor for occupant in self.occupants })

		for occupant in self.occupants:
			occupant.abandon_obstructed_layouts(all_anchors)


	def abandon_redundant_layouts(self, layout):
		"""Abandon any occupants' layouts that intrude upon a specified layout."""

		for occupant in self.occupants:
			occupant.abandon_redundant_layouts(layout)


	def assign_occupant_layout(self, occupant, layout):
		"""Assign an occupant to all the cells of a layout in the grid."""
		if layout not in occupant.layouts:
			raise Exception("The layout must already belong to the occupant.")

		occupant.assign_secure_layout(layout)
		self.abandon_redundant_layouts(layout)


	def assign_OccupantLayouts(self, occupant_layouts):
		"""Assign a set of occupants to all the cells of each of their layouts."""
		for occ_lay in occupant_layouts:
			self.assign_occupant_layout(occ_lay.occupant, occ_lay.layout)


	def secure_singleton_layouts(self) -> int:
		"""Claim the cells of each occupant that has exactly one layout.
		
		Returns the number of additional occupants that were secured."""
		secured_count = 0

		for occupant in self.occupants:
			if len(occupant.layouts) == 0:
				# CONSIDER: is this check really needed
				raise Exception(f"Occupant at {occupant.anchor} has no layouts.")

			if not occupant.is_secure and len(occupant.layouts) == 1:
				self.assign_occupant_layout(occupant, occupant.layouts[0])
				secured_count += 1

		return secured_count


	def secure_singleton_cells(self) -> int:
		"""Claim the cells that exactly one occupant's layout overlays.
		
		Returns the number of additional occupants that were secured."""

		# a flat set of all unsecure layouts
		layouts_unsecure = { OccupantLayout(occupant, layout)
				for occupant in self.occupants if not occupant.is_secure
					for layout in occupant.layouts }

		vacant_cells = self.grid.get_vacant_cells()
		secured_count = 0

		while len(vacant_cells) > 0:
			cell = vacant_cells.pop()

			# get the layouts that overlay this cell
			overlays = [occ_lay
					for occ_lay in layouts_unsecure
						if cell in occ_lay.layout.cells]  #TODO: ok for layout.cells to omit anchor

			# if exactly one, then assign it
			if len(overlays) == 1:
				self.assign_occupant_layout(overlays[0].occupant, overlays[0].layout)
				secured_count += 1

				layouts_unsecure.remove(overlays[0])
				vacant_cells -= overlays[0].layout.cells

		return secured_count


	def secure_open_cells(self) -> int:
		"""Traverse-search open cells for the set of layouts that claims them all.
		
		Returns the number of additional occupants that were secured."""

		def search_and_traverse(vacant_cells: set, solution_track: set):
			"""The main search & traverse algorithm."""

			if not len(vacant_cells):
				# all cells secured: solved!
				return solution_track

			cell = vacant_cells.pop()

			# find remaining layouts that can secure this cell
			solution_track_cells = {cell
					for occ_lay in solution_track for cell in occ_lay.layout.cells}
			layouts_over_solution_track = {occ_lay
					for occ_lay in initial_unsecure_layouts
					if not occ_lay.layout.cells.isdisjoint(solution_track_cells)}

			assert(solution_track <= layouts_over_solution_track)
			remaining_layouts = initial_unsecure_layouts - layouts_over_solution_track

			layouts_over_cell = [occ_lay
					for occ_lay in remaining_layouts
					if cell in occ_lay.layout.cells]
			
			if not len(layouts_over_cell):
				# dead end: no solution for this cell and traversal
				return None

			# traverse each possible layout
			for occ_lay in layouts_over_cell:
				vacant_cells_prime = vacant_cells - occ_lay.layout.cells
				solution_track_prime = solution_track | {occ_lay}

				traversal_stack.append( (vacant_cells_prime, solution_track_prime) )

			return None

		initial_unsecure_layouts = frozenset({ OccupantLayout(occupant, layout)
				for occupant in self.occupants if not occupant.is_secure
					for layout in occupant.layouts })

		initial_vacant = self.grid.get_vacant_cells()

		result = None
		traversal_stack = [ (initial_vacant, set()) ]

		while not result and len(traversal_stack):
			result = search_and_traverse(*traversal_stack.pop())

		if result:
			self.assign_OccupantLayouts(result)
			return len(result)
		elif result is None:
			return None
		else:
			return 0
