import time

class PhysicsBody:
    """Class that represents bodies that move and interact through physics\n
    PhysicsBody(x = 0, y = 0, width = 1, height = 1, mass = 1, moving = True)
    """
    # constructor function
    def __init__(self, x = 0, y = 0, width = 1, height = 1, mass = 1, moving = True):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.mass = mass
        self.movable = moving
        self.force = (0, 0)
        self.speed = (0, 0)
        self.center = (self.x + (self.width / 2), self.y + (self.height / 2))

        self.touching = dict()
        self.touching["up"] = False
        self.touching["down"] = False
        self.touching["left"] = False
        self.touching["right"] = False

    # function to move the body by a (x, y) amount
    def move(self, x, y):
        self.x = self.x + x
        self.y = self.y + y

        self.center = (self.x + (self.width / 2), self.y + (self.height / 2))

    # function to apply a force to the body by a (x, y) amount
    def push(self, x, y):
        self.force = (self.force[0] + x, self.force[1] + y)


class PhysicsWorld:
    """Class to calculate the physics simulation of the physics bodies\n
    PhysicsWorld(gravity = 1, friction = 0.1)"""
    # constructor method
    def __init__(self, gravity = 200, friction = 50):
        self.collision_solve_speed = 0.01
        self.gravity = gravity
        self.friction = friction
        self.physics_bodies = dict()
        self.elapsed_time = 0
        self.last_update = time.time()
        self.zero_division_threshold_x = 0.000001
        self.zero_division_threshold_y = 0.000001

    # function to add a physics body to the world to interact with (wrapper for the physics body constructor)
    def add_body(self, name = "", x = 0, y = 0, width = 1, height = 1, mass = 1, moving = True):
        # if no name is provided to the function
        if len(name) == 0:
            # name the body "physics_body_#" where # is the first available increasing number
            i = 0
            while True:
                key = "physics_body_" + str(i)

                if not key in self.physics_bodies:
                    self.physics_bodies[key] = PhysicsBody(x, y, width, height, mass, moving)
                    return(True)

                i += 1
        # otherwise create a new physics body with the name provided
        else:
            self.physics_bodies[name] = PhysicsBody(x, y, width, height, mass, moving)

    # function to let the physics simulation advance
    def update(self, dt = 0, sub_steps = 1):
        if dt == 0:
            dt = time.time() - self.last_update

        self.last_update = time.time()

        # for every body loaded in the physics world
        for body in self.physics_bodies.values():
            # reset the touching values
            body.touching["left"] = False
            body.touching["right"] = False
            body.touching["up"] = False
            body.touching["down"] = False

            # if the body is movable
            if body.movable:
                # calculate the forces applied on the X and Y components, according to air friction, velocity, mass and gravity
                totalForceX = (body.force[0] + (self.friction * (-body.speed[0]))) * dt
                totalForceY = (body.force[1] + (self.friction * (-body.speed[1])) - (body.mass * self.gravity)) * dt

                # calculate the acceleration by the formula: "a = F / m"
                acceleration_x = (totalForceX / body.mass)
                acceleration_y = (totalForceY / body.mass)
                # update the velocity according to the acceleration
                body.speed = ((body.speed[0] + acceleration_x), (body.speed[1] + acceleration_y))
                # body.speed = ((body.speed[0] + body.force[0] - self.gravity) * dt * dt, (body.speed[1] + body.force[1]) * dt)

                # create a dictionary to store the bodies that the current body collides with
                collisions = dict()

                # for every other body in the world
                for body_2 in self.physics_bodies.values():
                    if body_2 != body:
                        # check the collision
                        collision_result = self.collision_dynamicRect_rect(body.x, body.y, body.width, body.height, body.speed,
                                                                           body_2.x, body_2.y, body_2.width, body_2.height)

                        # if there was a collision
                        if not collision_result is None and not collision_result == False:
                            # find the name of the body that the original body collided with and store its distance in the collisions dictionary
                            collisions[list(self.physics_bodies.keys())[list(self.physics_bodies.values()).index(body_2)]] = collision_result[4]

                # if any collision happened
                if len(collisions) > 0:
                    # sort the collisions by distance from the original body
                    sorted_collisions = sorted(collisions.items(), key = lambda x:x[1])
                    # iterate through all the collisions in the sorted list of collisions
                    for collision in sorted_collisions:
                        # extract the current body for the current collision
                        current_body = self.physics_bodies[collision[0]]

                        # check the collision with the current colliding body (redundant)
                        collision_result = self.collision_dynamicRect_rect(body.x, body.y, body.width, body.height, body.speed,
                                                                           current_body.x, current_body.y, current_body.width, current_body.height)

                        # if there is a collision
                        if not collision_result is None and not collision_result == False:
                            # depending on the normal of the collision, determine where the body is touching
                            if collision_result[2] > 0:
                                body.touching["left"] = True
                            if collision_result[2] < 0:
                                body.touching["right"] = True
                            if collision_result[3] > 0:
                                body.touching["down"] = True
                            if collision_result[3] < 0:
                                body.touching["up"] = True

                            # adjust the current body speed accordingly
                            body.speed = ((body.speed[0] + (collision_result[2] * abs(body.speed[0]) * (1 - collision_result[4]))), (body.speed[1] + collision_result[3] * abs(body.speed[1]) * (1 - collision_result[4])))


                if body.speed[1] != 0:
                    body.touching["down"] = False

                # update the position according to the velocity
                body.x += body.speed[0]
                body.y += body.speed[1]

                # reset the current force on the body
                body.force = (0, 0)



        finish_time = time.time()
        self.elapsed_time = finish_time - self.last_update

    # DEPRECATED
    def solve_collision(self, body_1, body_2):

        # if self.collision_rect_rect(body_1.x, body_1.y, body_1.width, body_1.height,
        #                             body_2.x, body_2.y, body_2.width, body_2.height):
        #     if body_1.movable:
        #         distance = Vec2(body_1.center[0], body_1.center[1]) - Vec2(body_2.center[0], body_2.center[1])
        #         body_1.move(distance.x * self.collision_solve_speed, distance.y * self.collision_solve_speed)

        collision_result = self.collision_dynamicRect_rect(body_1.x, body_1.y, body_1.width, body_1.height, body_1.speed,
                                                           body_2.x, body_2.y, body_2.width, body_2.height)

        # if not collision_result is None and not collision_result == False:
            # body_1.speed = (0, 0)



            # body_1.speed = (body_1.speed[0] + (collision_result[2] * abs(body_1.speed[0]) * (1 - collision_result[4])), body_1.speed[1] + collision_result[3] * abs(body_1.speed[1]) * (1 - collision_result[4]))
            # print(body_1.speed)

            # body_1.force = (0, 0)

    # basic rectangle vs rectangle collision detection (DEPRECATED)
    def collision_rect_rect(self, r1x, r1y, r1w, r1h, r2x, r2y, r2w, r2h):
        # are the sides of one rectangle touching the other?
        return (r1x + r1w >= r2x and # r1 right edge past r2 left
                r1x <= r2x + r2w and # r1 left edge past r2 right
                r1y + r1h >= r2y and # r1 top edge past r2 bottom
                r1y <= r2y + r2h)     # r1 bottom edge past r2 top

    # function to test if a ray intersects a rectangle
    def collision_ray_rect(self, ray_origin_x, ray_origin_y, ray_end_x, ray_end_y, rect_x, rect_y, rect_w, rect_h):
        debug = False

        division_threshold_x = self.zero_division_threshold_x
        division_threshold_y = self.zero_division_threshold_y

        if ray_origin_x <= rect_x + rect_w / 2:
            division_threshold_x = -self.zero_division_threshold_x
        elif ray_origin_x > rect_x + rect_w / 2:
            division_threshold_x = self.zero_division_threshold_x

        if ray_origin_y <= rect_y + rect_h / 2:
            division_threshold_y = -self.zero_division_threshold_y
        elif ray_origin_y > rect_y + rect_h / 2:
            division_threshold_y = self.zero_division_threshold_y

        if debug:
            print("ray vs rect collision")

            print(f"rect_pos:  ({rect_x}, {rect_y})")
            print(f"rect_size: ({rect_w}, {rect_h})")

            print(f"ray_origin: ({ray_origin_x}, {ray_origin_y})")
            print(f"ray_end:    ({ray_end_x}, {ray_end_y})")

        # calculate the direction ray
        ray_direction_x = ray_end_x - ray_origin_x
        ray_direction_y = ray_end_y - ray_origin_y

        if debug:
            print(f"ray_direction: ({ray_direction_x}, {ray_direction_y})")

            for i in range(11):
                point_x = ray_origin_x + ray_direction_x * (i / 10)
                point_y = ray_origin_y + ray_direction_y * (i / 10)

                print(f"ray(t = {i / 10}): ({point_x}, {point_y})")

        # calculate the near and far t values for x and y
        # ADD FIX FOR PARALLEL VECTORS (DIVISION BY 0)
        if ray_direction_x == 0:
            ray_direction_x = division_threshold_x

        if ray_direction_y == 0:
            ray_direction_y = division_threshold_y

        # if ray_direction_x == 0 or ray_direction_y == 0:
        #     return False

        # calculate the near and far collision "times" on the x and y axis

        near_x_t = (rect_x - ray_origin_x) / ray_direction_x
        far_x_t = (rect_x + rect_w - ray_origin_x) / ray_direction_x

        near_y_t = (rect_y + rect_h- ray_origin_y) / ray_direction_y
        far_y_t = (rect_y - ray_origin_y) / ray_direction_y



        # swap the near and far values in case they don't make sense
        if near_x_t > far_x_t:
            tmp = near_x_t
            near_x_t = far_x_t
            far_x_t = tmp

        if near_y_t > far_y_t:
            tmp = near_y_t
            near_y_t = far_y_t
            far_y_t = tmp

        if debug:
            print(f"near_x_t = {near_x_t}")
            print(f"far_x_t  = {far_x_t}")
            print(f"near_y_t = {near_y_t}")
            print(f"far_y_t  = {far_y_t}")

        # condition for the ray to not collide with the rectangle
        if near_x_t > far_y_t or near_y_t > far_x_t:
            if debug:
                print("no collision")
            return False

        # calculating the near and far hit t
        hit_near_t = max(near_x_t, near_y_t)
        hit_far_t = min(far_x_t, far_y_t)

        if debug:
            print(f"hit_near_t = {hit_near_t}")
            print(f"hit_far_t = {hit_far_t}")

        # case in which the collision happens behind the vector and past the vector
        if hit_far_t < 0 or hit_near_t > 1 or hit_near_t < 0:
            if debug:
                print("no collision")
            return False

        # collision detected

        # calculate the contact point
        contact_point_x = ray_origin_x + ray_direction_x * hit_near_t
        contact_point_y = ray_origin_y + ray_direction_y * hit_near_t

        if debug:
            print(f"contact point: ({contact_point_x}, {contact_point_y})")

        contact_normal_x = 0
        contact_normal_y = 0

        # calculate the normal vector of the contact
        if near_x_t > near_y_t:
            if ray_direction_x < 0:
                contact_normal_x = 1
                contact_normal_y = 0
            else:
                contact_normal_x = -1
                contact_normal_y = 0
        elif near_x_t < near_y_t:
            if ray_direction_y < 0:
                contact_normal_x = 0
                contact_normal_y = 1
            else:
                contact_normal_x = 0
                contact_normal_y = -1

        return((contact_point_x, contact_point_y, contact_normal_x, contact_normal_y, hit_near_t))

    # function to check collision between a moving rectangle and a stationary rectangle
    def collision_dynamicRect_rect(self, current_x, current_y, current_w, current_h, current_speed, target_x, target_y, target_w, target_h):
        # if the dynamic rectangle is not moving, there is no collision
        if current_speed[0] == 0 and current_speed[1] == 0:
            return(False)

        # expand the target rectangle to make the borders of the dynamic rectangle match with the borders of the stationary rectangle
        expanded_target_x = target_x - current_w / 2
        expanded_target_y = target_y - current_h / 2

        expanded_target_w = target_w + current_w
        expanded_target_h = target_h + current_h

        # calculate the collision of the ray that goes from the center of the dynamic rectangle with the direction and module of the rectangle speed and the stationary rectangle
        collision_result = self.collision_ray_rect(current_x + current_w / 2, current_y + current_h / 2, current_x + current_w / 2 + current_speed[0], current_y + current_h / 2 + current_speed[1], expanded_target_x, expanded_target_y, expanded_target_w, expanded_target_h)

        # if there was a collision
        if not collision_result is None and not collision_result == False:
            # return it
            return(collision_result)
