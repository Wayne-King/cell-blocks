from cellFacility import CellFacility, OccupantLayout
from occupant import Occupant

row_count = 7
column_count = 7
print_template_cell = ' {} |'
print_template_wall = '---+'

facility = CellFacility(row_count = row_count, column_count = column_count)


def primary_action_sequence():
	print(f"Facility row & col count: {facility.grid.row_count}, {facility.grid.column_count}.")
	print_facility()

	assign_all_occupants()
	print('occupants assigned:')
	print_facility()

	facility.abandon_nonisolating_layouts()

	facility.secure_singleton_layouts()
	print('secured singleton layouts:')
	print_facility()

	while facility.secure_singleton_cells(): pass
	print('secured singleton cells:')
	print_facility()

	secure_open_cells()
	print('secured open cells:')
	print_facility()

	print('Done.')


def assign_all_occupants():
	"""Assign each occupant to its anchor cell."""
	facility.assign_occupant(row_index = 0, column_index = 2, volume = 2)
	facility.assign_occupant(0, 5, 2)
	facility.assign_occupant(1, 0, 4)
	facility.assign_occupant(2, 2, 3)
	facility.assign_occupant(2, 3, 5)
	facility.assign_occupant(3, 0, 2)
	facility.assign_occupant(3, 1, 2)
	facility.assign_occupant(4, 2, 3)
	facility.assign_occupant(4, 5, 8)
	facility.assign_occupant(5, 2, 3)
	facility.assign_occupant(5, 4, 6)
	facility.assign_occupant(5, 6, 2)
	facility.assign_occupant(6, 1, 3)
	facility.assign_occupant(6, 4, 2)
	facility.assign_occupant(6, 6, 2)


def print_facility():
	"""Output a representation of the cell facility (grid) to the console."""

	row_separator = print_template_wall * (column_count + 1)
	def print_row(row_contents):
		print(*[print_template_cell.format(x) for x in row_contents], sep='')
		print(row_separator)

	print_row([' '] + [x for x in range(0, column_count)])

	for row_index in range(0, row_count):
		row_contents = [row_index]

		for column_index in range(0, column_count):
			occupant = facility.grid.occupant_of(row_index, column_index)
			row_contents += [occupant.volume if occupant else ' ']

		print_row(row_contents)


#TODO: move this function, or most of this work, into CellFacility
def secure_open_cells():
	"""Traverse-search remaining open cells for the set of layouts that claims them all."""

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
			for occupant in facility.occupants if not occupant.is_secure
				for layout in occupant.layouts })

	initial_vacant = facility.grid.get_vacant_cells()

	## TODO: maybe don't need this looping -- pick any single, vacant cell and traversing
	##  from it will check all possible paths, right?
	#for root_cell in initial_vacant:
	#
	#	vacant_cells = initial_vacant.copy()
	#	solution_track = set()  # set of OccupantLayout
	#
	#	traversal_stack = [ (vacant_cells, solution_track) ]

	result = None
	traversal_stack = [ (initial_vacant, set()) ]

	while not result and len(traversal_stack):
		result = search_and_traverse(*traversal_stack.pop())

	if result:
		facility.assign_OccupantLayouts(result)
	else:
		print("warning:  did not find a solution. :(")


primary_action_sequence()
