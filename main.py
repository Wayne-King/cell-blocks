from cellFacility import CellFacility
from occupant import Occupant

facility = CellFacility(row_count = 7, column_count = 7)

print(f"Facility row & col count: {facility.grid.row_count}, {facility.grid.column_count}.")

# assign all the occupants
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

