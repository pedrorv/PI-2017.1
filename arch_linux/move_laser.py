from numpy import linalg as LA
from math import atan
from math import tan

#da uma passo em direcao a posicao desejada
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

#converte para as coordenadas em radianos do stepper, todas as dimensoes estao em pixels sera necessario converter a altura de metros para pixels
def convert_to_stepper_coordinates(x,y,max_X,max_Y,webcam_angle):
    stepper_Y = 0
    stepper_X = 0
    distance = max_X/tan(webcam_angle)

    stepper_X = -2*22.6*x/max_X + 22.6
    stepper_Y = 2*17.5*y/max_Y - 17.5

    return (stepper_X,stepper_Y)
