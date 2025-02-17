from dynamic_gridworld import DynamicGridWorldEnv

env = DynamicGridWorldEnv(size=5)
env.create_room()

env.move_right()
env.move_right()
env.move_right()
env.move_right()
env.move_down()
env.move_down()
env.move_left()
env.move_left()
env.move_left()
env.move_down()

env.pick_up()

env.move_up()
env.move_right()
env.move_right()
env.move_right()
env.move_up()
env.move_up()
env.move_left()
env.move_left()
env.move_left()
env.move_left()

env.place()

env.keep_window_open()
