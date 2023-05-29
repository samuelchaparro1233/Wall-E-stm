import gui_wall_e
class Robot:
    def __init__(self):
        self.state = 'INITIAL'
        self.position = (0, 0)
        self.current_object = None
        self.matrix = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        self.container_position = (4, 0)
    
    def start(self):
        while self.state != 'FINAL':
            if self.state == 'INITIAL':
                self.move_right()
            elif self.state == 'MOVING_RIGHT':
                self.check_object()
            elif self.state == 'OBJECT_FOUND':
                self.handle_object_found()
            elif self.state == 'OBJECT_PICKED':
                self.move_to_container()
            elif self.state == 'MOVING_TO_CONTAINER':
                self.place_object_in_container()
            elif self.state == 'FINISH':
                self.state = 'FINAL'
                print("Recogida de objetos y colocación en el contenedor finalizada.")
    
    def move_right(self):
        if self.position[1] < 4:
            self.position = (self.position[0], self.position[1] + 1)
            self.state = 'MOVING_RIGHT'
            self.matrix[self.position[0]][self.position[1]] = 1
            self.update_matrix()
            print(f"Moviendo hacia la derecha. Posición actual: {self.position}")
        else:
            self.state = 'FINISH'
    
    def move_down(self):
        if self.position[0] < 4:
            self.position = (self.position[0] + 1, self.position[1])
            self.state = 'MOVING_DOWN'
            self.matrix[self.position[0]][self.position[1]] = 1
            self.update_matrix()
            print(f"Moviendo hacia abajo. Posición actual: {self.position}")
        else:
            self.state = 'FINISH'
    
    def check_object(self):
        object_type = self.matrix[self.position[0]][self.position[1]]
        if object_type != 0 and self.current_object is None:
            self.state = 'OBJECT_FOUND'
            print(f"Objeto {object_type} encontrado en la posición {self.position}")
        else:
            self.state = 'MOVING_RIGHT'
    
    def handle_object_found(self):
        object_type = self.matrix[self.position[0]][self.position[1]]
        if self.current_object is None:
            self.current_object = object_type
            self.matrix[self.position[0]][self.position[1]] = 0  # Actualizar posición del robot
            self.state = 'OBJECT_PICKED'
            self.update_matrix()
            print(f"Objeto {object_type} recogido en la posición {self.position}")
        elif self.current_object == object_type:
            self.state = 'MOVING_RIGHT'
        else:
            self.relocate_object()
    
    def relocate_object(self):
        for row in range(5):
            for col in range(5):
                if self.matrix[row][col] == 0:
                    self.update_matrix()
                    self.matrix[row][col] = self.matrix[self.position[0]][self.position[1]]
                    self.matrix[self.position[0]][self.position[1]] = 0
                    self.position = (row, col)
                    self.state = 'MOVING_RIGHT'
                    print(f"Objeto reubicado en la posición {self.position}")
                    return
    
    def move_to_container(self):
        if self.position[0] != self.container_position[0] or self.position[1] != self.container_position[1]:
            if self.position[0] < self.container_position[0]:
                self.move_down()
            elif self.position[0] > self.container_position[0]:
                self.move_up()
            elif self.position[1] < self.container_position[1]:
                self.move_right()
            elif self.position[1] > self.container_position[1]:
                self.move_left()
        else:
            self.state = 'MOVING_TO_CONTAINER'
    
    def move_up(self):
        self.position = (self.position[0] - 1, self.position[1])
        self.state = 'MOVING_TO_CONTAINER'
        self.matrix[self.position[0]][self.position[1]] = 1
        self.update_matrix()
        print(f"Moviendo hacia arriba. Posición actual: {self.position}")
    
    def move_left(self):
        self.position = (self.position[0], self.position[1] - 1)
        self.state = 'MOVING_TO_CONTAINER'
        self.matrix[self.position[0]][self.position[1]] = 1
        self.update_matrix()
        print(f"Moviendo hacia la izquierda. Posición actual: {self.position}")
    
    def place_object_in_container(self):
        self.current_object = None
        self.state = 'OBJECT_PLACED'
        self.matrix[self.container_position[0]][self.container_position[1]] = 0  # Actualizar posición del robot
        self.matrix[self.position[0]][self.position[1]] = 0
        self.update_matrix()
        print(f"Objeto depositado en el contenedor en la posición {self.container_position}")
    
    def update_matrix(self):
        for row in range(5):
            for col in range(5):
                if self.matrix[row][col] == 1:
                    self.matrix[row][col] = 0
        self.matrix[self.position[0]][self.position[1]] = 1
        print("Estado actual de la matriz:")
        for row in self.matrix:
            print(row)
        print()
        gui_wall_e.tablero(self.matrix)


# Ejemplo de uso
robot = Robot()

# Definir la matriz con los objetos
robot.matrix = [
    [0, 6, 0, 0, 0],
    [0, 0, 0, 5, 0],
    [0, 7, 6, 0, 0],
    [5, 0, 0, 7, 0],
    [4, 0, 0, 0, 0]
]

robot.position=(0,0)
robot.current_object = None
robot.start()
