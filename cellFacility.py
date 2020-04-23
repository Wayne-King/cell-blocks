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

		all_anchors = { occupant.anchor for occupant in self.occupants }

		for occupant in self.occupants:
			for layout in occupant.layouts.copy():
				# TODO: the occupant class should take care of examining the layout cells
				#       and especially of updating the layouts list

				# get the cells (locations) of this layout, sans the anchor cell
				layout_cells = layout.cells - {occupant.anchor}

				# discard the layout if it overlaps any anchors
				if not layout_cells.isdisjoint(all_anchors):
					occupant.layouts.remove(layout)


	def abandon_redundant_layouts(self, layout):
		"""Abandon any occupants' layouts that intrude upon a specified layout."""

		for test_occupant in self.occupants:
			for test_layout in test_occupant.layouts:
				# TODO: occupant class should take care of this work

				# if any intersecting cells, remove the whole layout
				if test_layout != layout \
						and not layout.cells.isdisjoint(test_layout.cells):
					test_occupant.layouts.remove(test_layout)


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


	def secure_singleton_layouts(self):
		"""Claim the cells of each occupant that has exactly one layout."""
		for occupant in self.occupants:
			if len(occupant.layouts) == 0:
				raise Exception(f"Occupant at {occupant.anchor} has no layouts.")

			elif len(occupant.layouts) == 1:
				self.assign_occupant_layout(occupant, occupant.layouts[0])


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
