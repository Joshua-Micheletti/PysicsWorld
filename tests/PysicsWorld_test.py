import sys
sys.path.insert(0, 'src/PysicsWorld')
from PysicsWorld import PhysicsWorld

import unittest
import logging
import random


class TestPhysics(unittest.TestCase):

    def setUp(self):
        self.physics_world = PhysicsWorld()

    def test_PhysicsWorld_creation(self):
        self.assertEqual(self.physics_world.gravity, 1)
        self.assertEqual(self.physics_world.friction, 0.1)
        self.assertEqual(len(self.physics_world.physics_bodies), 0)

    def test_collision_ray_rect(self):
        # ray coming from bottom left to top right
        collision_result = self.physics_world.collision_ray_rect(0, 10, 100, 100, 20, 20, 30, 30)

        self.assertFalse(collision_result == False or collision_result == None)

        self.assertTrue(collision_result[4] <= 1)
        self.assertTrue(collision_result[4] >= 0)

        self.assertEqual(collision_result[2], -1)
        self.assertEqual(collision_result[3], 0)

        # ray coming from left to right (parallel x)
        collision_result = self.physics_world.collision_ray_rect(0, 30, 100, 30, 20, 20, 20, 20)

        self.assertFalse(collision_result == False or collision_result == None)

        self.assertTrue(collision_result[4] <= 1)
        self.assertTrue(collision_result[4] >= 0)

        self.assertEqual(collision_result[2], -1)
        self.assertEqual(collision_result[3], 0)

        # ray coming from right to left (parallel x)
        collision_result = self.physics_world.collision_ray_rect(100, 30, 0, 30, 20, 20, 20, 20)

        self.assertFalse(collision_result == False or collision_result == None)

        self.assertTrue(collision_result[4] <= 1)
        self.assertTrue(collision_result[4] >= 0)

        self.assertEqual(collision_result[2], 1)
        self.assertEqual(collision_result[3], 0)

        # ray coming from up to down (parallel y)
        collision_result = self.physics_world.collision_ray_rect(30, 100, 30, 0, 20, 20, 20, 20)

        self.assertFalse(collision_result == False or collision_result == None)

        self.assertTrue(collision_result[4] <= 1)
        self.assertTrue(collision_result[4] >= 0)

        self.assertEqual(collision_result[2], 0)
        self.assertEqual(collision_result[3], 1)

    def test_collision_dynamicRect_rect(self):
        collision_result = self.physics_world.collision_dynamicRect_rect(0, 0, 20, 20, (100, 0), 25, 0, 20, 20)

        self.assertFalse(collision_result == False or collision_result == None)

        self.assertEqual(collision_result[2], -1)
        self.assertEqual(collision_result[3], 0)

    def test_update(self):
        self.physics_world.add_body("dynamic", 0, 100, 20, 20, 1, True)
        self.physics_world.add_body("static", 0, 0, 100, 1, 1, False)

        self.assertEqual(len(self.physics_world.physics_bodies), 2)

        self.physics_world.update(1)

        self.assertTrue(self.physics_world.physics_bodies["dynamic"].y < 100)

        for i in range(2000):
            self.physics_world.update(1)

            if self.physics_world.physics_bodies["dynamic"].speed[1] == 0:
                break

        # truncate the value of y to the 14th decimal place
        self.assertEqual(float('%.14f'%(self.physics_world.physics_bodies["dynamic"].y)), 1)

    def test_time(self):
        log = logging.getLogger("TestPhysics.test_time")

        for i in range(50):
            self.physics_world.add_body("dynamic_" + str(i), random.randint(-50, 50), random.randint(20, 100), 40, 40, random.randint(1, 10), True)
            self.physics_world.physics_bodies["dynamic_" + str(i)].push(random.randint(-100, 100), random.randint(-10, 100))

        self.physics_world.add_body("static", -2000, -5, 4000, 10, 1, False)

        self.assertEqual(len(self.physics_world.physics_bodies), 51)

        self.physics_world.update(1)
        
        self.assertTrue(self.physics_world.elapsed_time < 0.016)



if __name__ == '__main__':
    logging.basicConfig(stream = sys.stderr)
    logging.getLogger("TestPhysics.test_time").setLevel(logging.DEBUG)

    unittest.main()
