

import PID

class ExpoPID(PID.PID):
  expo = 0.0

  def __init__(self, *args, scale_max=4.0, **kwargs):
    self.scale_max = scale_max
    return super().__init__(*args, **kwargs)

  def expo_func(self, error):
    if error is None:
      return 1.0
    error = abs(error)
    if error <= self.scale_max:
      return pow(10, error - self.scale_max)
    elif error > self.scale_max:
      return 1.0

  def update(self, *args, **kwargs):
    print(f"got args: {args}, kwargs: {kwargs}")
    super().update(*args, **kwargs)

    error = self.PTerm/self.Kp
    self.expo = self.expo_func(error)

    print(f"vals: {self.PTerm}, kp: {self.Kp}, error: {error}")

    print(f"got expo return value: {self.expo}")

    self.output *= self.expo


  def getExpo(self):
    return self.expo
