from numpy import linalg as LA
from math import atan

def move_laser(current_position_X,current_position_Y,target_position_X,target_position_Y,step_size):
  if(current_position_X > (target_position_X + step_size)):
      current_position_X -= step_size
  elif(current_position_X < (target_position_X - step_size)):
      current_position_X += step_size

  if(current_position_Y > (target_position_Y + step_size)):
      current_position_Y -= step_size
  elif(current_position_Y < (target_position_Y - step_size)):
      current_position_Y += step_size

  if LA.norm([current_position_X - target_position_X,current_position_Y - target_position_Y]) < 2*step_size:
      return (True,current_position_X,current_position_Y)
  else:
      return (False,current_position_X,current_position_Y)

def convert_to_stepper_coordinates(x,y,height,max_X,max_Y):
    stepper_Y = 0
    stepper_X = 0
    if x < max_X/2:
        tg = (max_X/2 - x)/height
        stepper_X =  -1*atan(tg)

    else:
        tg = (x - max_X/2)/height
        stepper_X =  atan(tg)

    if y < max_Y/2:
        tg = (max_Y/2 - y)/height
        stepper_y =  -1*atan(tg)
    else:
        tg = (y - max_Y/2)/height
        stepper_Y = atan(tg)

    return (stepper_X,stepper_Y)
