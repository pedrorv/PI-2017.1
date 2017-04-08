from numpy import linalg as LA

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
