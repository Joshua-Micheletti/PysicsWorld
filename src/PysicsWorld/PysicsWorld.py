class PhysicsBody:

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


    def move(self, x, y):
        self.x = self.x + x
        self.y = self.y + y

        self.center = (self.x + (self.width / 2), self.y + (self.height / 2))

    def push(self, x, y):
        self.force = (self.force[0] + x, self.force[1] + y)


class PhysicsWorld:

    def __init__(self):
        self.collision_solve_speed = 0.01
        self.gravity = 1
        self.friction = 0.1
        self.physics_bodies = dict()

    def add_body(self, name = "", x = 0, y = 0, width = 1, height = 1, mass = 1, moving = True):
        if len(name) == 0:
            i = 0
            while True:
                key = "physics_body_" + str(i)

                if not key in self.physics_bodies:
                    self.physics_bodies[key] = PhysicsBody(x, y, width, height, mass, moving)
                    return(True)

                i += 1

        else:
            self.physics_bodies[name] = PhysicsBody(x, y, width, height, mass, moving)


    def update(self, sub_steps = 1):
        for body in self.physics_bodies.values():
            if body.movable:
                # calculate the forces applied on the X and Y components, according to air friction, velocity, mass and gravity
                totalForceX = body.force[0] + (self.friction * (-body.speed[0]))
                totalForceY = body.force[1] + (self.friction * (-body.speed[1])) - (body.mass * self.gravity)
                # calculate the acceleration by the formula: "a = F / m"
                acceleration_x = totalForceX / body.mass
                acceleration_y = totalForceY / body.mass
                # update the velocity according to the acceleration
                body.speed = (body.speed[0] + acceleration_x, body.speed[1] + acceleration_y)

                collisions = dict()

                for body_2 in self.physics_bodies.values():
                    if body_2 != body:
                        collision_result = self.collision_dynamicRect_rect(body.x, body.y, body.width, body.height, body.speed,
                                                                           body_2.x, body_2.y, body_2.width, body_2.height)

                        if not collision_result is None and not collision_result == False:
                            # collisions[physics_bodies.keys()[physics_bodies.values()]]
                            collisions[list(self.physics_bodies.keys())[list(self.physics_bodies.values()).index(body_2)]] = collision_result[4]

                if len(collisions) > 0:
                    sorted_collisions = sorted(collisions.items(), key = lambda x:x[1])

                    for collision in sorted_collisions:
                        current_body = self.physics_bodies[collision[0]]

                        collision_result = self.collision_dynamicRect_rect(body.x, body.y, body.width, body.height, body.speed,
                                                                           current_body.x, current_body.y, current_body.width, current_body.height)

                        if not collision_result is None and not collision_result == False:
                            body.speed = (body.speed[0] + (collision_result[2] * abs(body.speed[0]) * (1 - collision_result[4])), body.speed[1] + collision_result[3] * abs(body.speed[1]) * (1 - collision_result[4]))


                # update the position according to the velocity
                body.x += body.speed[0]
                body.y += body.speed[1]
                # reset the current force on the body
                body.force = (0, 0)

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


    def collision_rect_rect(self, r1x, r1y, r1w, r1h, r2x, r2y, r2w, r2h):
        # are the sides of one rectangle touching the other?
        return (r1x + r1w >= r2x and # r1 right edge past r2 left
                r1x <= r2x + r2w and # r1 left edge past r2 right
                r1y + r1h >= r2y and # r1 top edge past r2 bottom
                r1y <= r2y + r2h)     # r1 bottom edge past r2 top

    def collision_ray_rect(self, ray_origin_x, ray_origin_y, ray_end_x, ray_end_y, rect_x, rect_y, rect_w, rect_h):
        debug = False

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
            ray_direction_x = 0.000001

        if ray_direction_y == 0:
            ray_direction_y = 0.000001

        # if ray_direction_x == 0 or ray_direction_y == 0:
        #     return(False)

        # if ray_direction_x == 0 and ((rect_x - ray_origin_x) != 0 or (rect_x + rect_w - ray_origin_x) != 0):
        #     return(False)
        #
        # if ray_direction_y == 0 and ((rect_y + rect_h - ray_origin_y) != 0 or (rect_y - ray_origin_y) != 0):
        #     return(False)

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
        # if debug:
            # print("collision")

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


    def collision_dynamicRect_rect(self, current_x, current_y, current_w, current_h, current_speed, target_x, target_y, target_w, target_h):

        if current_speed[0] == 0 and current_speed[1] == 0:
            return(False)

        expanded_target_x = target_x - current_w / 2
        expanded_target_y = target_y - current_h / 2

        expanded_target_w = target_w + current_w
        expanded_target_h = target_h + current_h

        collision_result = self.collision_ray_rect(current_x + current_w / 2, current_y + current_h / 2, current_x + current_w / 2 + current_speed[0], current_y + current_h / 2 + current_speed[1], expanded_target_x, expanded_target_y, expanded_target_w, expanded_target_h)

        if not collision_result is None and not collision_result == False:
            return(collision_result)
