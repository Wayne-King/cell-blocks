from cellFacility import CellFacility
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
	print('secured singledton cells:')
	print_facility()

	secure_open_cells()
	print('secured open cells:')
	print(' -- NYI --')


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


def secure_open_cells():
	"""Traverse-search remaining open cells for the set of layouts that claims them all."""
	pass
