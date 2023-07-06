from clamp import clamp

class LinearRamp:

  def __init__(self, base_obj, watched_entity, target=None, deadband=None, lower=None, upper=None, output_range=[0,1]):
    self.base_obj = base_obj

    self.watched_entity = watched_entity
    self.current_value = None

    self.target = target
    self.deadband = deadband
    if target and deadband:
      self.lower = target - deadband
      self.upper = target + deadband

    if lower:
      self.lower = lower
    if upper:
      self.upper = upper

    self.output_range = output_range

    self.base_obj.listen_state(self.process_new_value, watched_entity)
    self.trigger()

  def log(self, *args, **kwargs):
    self.base_obj.log(f"{self.watched_entity}: {args[0]}", *args[1:], **kwargs)

  def set_target(self, target):
    self.target = target

    self.lower = self.target - self.deadband
    self.upper = self.target + self.deadband

  def trigger(self):
    self.process_new_value(self.watched_entity, {}, None, self.base_obj.get_state(self.watched_entity), None)

  def get_output(self):
    range_percent = (self.current_value - self.lower)/(self.upper-self.lower)

    range_percent = clamp(range_percent, 0.0, 1.0)

    return ( range_percent * (self.output_range[1] - self.output_range[0]) ) + self.output_range[0]

  def process_new_value(self, entity, attribute, old, new, kwargs):
    self.log(f"got new data: {entity}, {attribute}, {old}, {new}, {kwargs}")

    self.log(f"current_state: {self.lower} < {new} < {self.upper}")

    if new == 'unavailable':
      return

    self.current_value = float(new)
