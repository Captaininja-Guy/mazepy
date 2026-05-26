class Distances:
    def __init__(self, root):
        self.root = root
        self.cells = {root: 0}
    
    def __getitem__(self, cell):
        if cell in self.cells:
            return self.cells[cell]
        return None
    
    def __setitem__(self, cell, distance):
        self.cells[cell] = distance

    def __contains__(self, cell):
        return cell in self.cells

    def path_to(self, goal):
        current = goal
        breadcrumbs = Distances(self.root) # new distances objects only have the root in them untill a cell calls its method
        breadcrumbs[goal] = self.cells[goal]

        # Starts at the goal and picks the first neighbor with a lower value than it until target (start) is reached
        while current != self.root:
            for linked_neighbor in current.links():
                if self.cells[linked_neighbor] < self.cells[current]:
                    breadcrumbs[linked_neighbor] = self.cells[linked_neighbor]
                    current = linked_neighbor
                    break
            
        return breadcrumbs

    def max(self):
        max_dist = 0
        max_cell = self.root

        for cell, distance in self.cells.items():
            if distance > max_dist:
                max_dist = distance
                max_cell = cell
        
        return max_cell, max_dist
    
    def __str__(self):
        l = []
        for cell, dist in self.cells.items():
            l.append(f'({cell.row}, {cell.column}): {dist}')
        return '\n'.join(l)
        return f'Distances Object with Root: ({self.root.row}, {self.root.column}), Number of Cells: {len(self.cells)}, Max Distance: {self.max()[1]}, Max Cell: ({self.max()[0].row}, {self.max()[0].column})'