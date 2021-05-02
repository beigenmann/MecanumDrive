import machine


class L298N( object ):
  maxpwm = 1023
  minpwm = -1023

  def __init__( self, pin2, pin1) :
    self._pwm_forward = machine.PWM(machine.Pin(pin1))
    self._pwm_backward = machine.PWM(machine.Pin(pin2))
    self._speed = 0
    self._pwm_forward.freq(500)
    self._pwm_forward.duty(0)
    self._pwm_backward.freq(500)
    self._pwm_backward.duty(0)
    
  def __del__(self):  
    print (" del")
    self.delete()
    
  def delete(self):
    self._pwm_forward.deinit()
    self._pwm_backward.deinit() 
  @property
  def speed( self ) : return self._speed

 
  @speed.setter
  def speed( self, value ) :
    if value < self.minpwm :
      value = self.minpwm
    if value > self.maxpwm :
      value = self.maxpwm

    if value >= 0 :
      if self._speed < 0:
        print ("Bw 0")
        self._pwm_backward.duty(0)
      print ("Fw " ,value)
      self._pwm_forward.duty(value)
    else :
      if self._speed >= 0:
        print ("Fw 0")
        self._pwm_forward.duty(0)
      print ("Bw " , abs(value))
      self._pwm_backward.duty(abs(value))

    self._speed = value
    print ("Speed " , self._speed)

  def brake( self ) :
    """ Brake the motor by sending power both directions. """
    self._pwm_forward.duty(L298N.maxpwm)
    self._pwm_backward.duty(L298N.maxpwm)
    
  def stop (self) :  
    self._pwm_forward.duty(0)
    self._pwm_backward.duty(0)
    