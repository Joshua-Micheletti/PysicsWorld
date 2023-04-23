# PysicsWorld
A 2D physics engine that handles AABB rect vs rect collision detection and resolution

## Installation

### pip
Install the module using `pip`:  
`pip install -i https://test.pypi.org/simple/ PysicsWorld`

### manual
Download the repository or clone it using `git`:  
`git clone https://github.com/Joshua-Micheletti/PysicsWorld`  

Copy the content of the downloaded `src` folder into your project `src` directory

## Usage

### import
Import the PhysicsWorld object (used for all the features of the library) by typing:  
`from PysicsWorld.PysicsWorld import PhysicsWorld`

### creating a PhysicsWorld
Create a PhysicsWorld object through its constructor:  
`physics_world = PhysicsWorld()`

### creating physics bodies
Use the method `add_body()` to create a new physics body to add to the world:  
`physics_world.add_body(name, x, y, width, height, moving)`

### advance the simulation
To simulate one step in the simulation use the `update()` function:  
`physics_world.update(steps)`

### retrieve the bodies new position
In order to visualize the effects of the simulation, you need to retrieve the new positions of the bodies, these are stored in the dictionary `physics_bodies`, where the name of the body is the key, and the value is a `PhysicsBody` object that contains the (x, y) coordinates:  
`physics_world.physics_bodies["name"].x`  
`physics_world.physics_bodies["name"].y`  

### applying forces to the bodies
To apply a force to a body (for example from a controller module to move a character), use the `push(x,y)` method from the PhysicsBody class:  
`physics_world.physics_bodies["player"].push(x,y)`

### variables in the PhysicsWorld
The PhysicsWorld object contains a few variables that allow to change the physics properties and extract information:  
To set the gravity in the world, use:  
`physics_world.gravity = 1`  
To set the air friction, use:  
`physics_world.friction = 0.1`  
To retrieve the time passed to calculate the last step in the simulation, use:  
`physics_world.elapsed_time`
