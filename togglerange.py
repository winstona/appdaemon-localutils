class ToggleRange:

  def __init__(self, base_obj, watched_entity, target=None, deadband=None, lower=None, upper=None, lower_action="off", upper_action="on"):
    self.base_obj = base_obj

    self.watched_entity = watched_entity
    self.current_state = None

    self.target = target
    self.deadband = deadband
    if target and deadband:
      self.lower = target - deadband
      self.upper = target + deadband

    if lower:
      self.lower = lower
    if upper:
      self.upper = upper

    self.lower_action = lower_action
    self.upper_action = upper_action

    self.base_obj.listen_state(self.process_new_value, watched_entity)
    #self.process_new_value(watched_entity, {}, None, self.base_obj.get_state(watched_entity), None)
    self.trigger()

  def log(self, *args, **kwargs):
    self.base_obj.log(f"{self.watched_entity}: {args[0]}", *args[1:], **kwargs)

  def __bool__(self):
    if self.current_state == 'on':
      return True
    elif self.current_state == 'off':
      return False
    return bool(self.current_state)


  def action_callback(self, desired_state):
    self.log(f"got action_callback, setting: {desired_state}")
    self.current_state = desired_state

  def get_current_state(self):
    return self.current_state

  def set_target(self, target):
    self.target = target

    self.lower = self.target - self.deadband
    self.upper = self.target + self.deadband

  def trigger(self):
    self.process_new_value(self.watched_entity, {}, None, self.base_obj.get_state(self.watched_entity), None)



  #def turn_on_or_off(self, toggled_entity, desired_state):
  #  self.base_obj.log(f"turning {toggled_entity}: {desired_state}")
  #  if desired_state == 'on':
  #    self.base_obj.turn_on(toggled_entity)
  #  elif desired_state == 'off':
  #    self.base_obj.turn_off(toggled_entity)

  def process_new_value(self, entity, attribute, old, new, kwargs):
    self.log(f"got new data: {entity}, {attribute}, {old}, {new}, {kwargs}")
    current_state = self.get_current_state()

    self.log(f"current_state: {current_state}")
    self.log(f"current_state: {self.lower} < {new} < {self.upper}")

    if new == 'unavailable':
      return

    new = float(new)

    if new < self.lower and current_state != self.lower_action:
      #self.turn_on_or_off(self.toggled_entity, self.lower_action)
      self.action_callback(self.lower_action)
    elif new > self.upper and current_state != self.upper_action:
      #self.turn_on_or_off(self.toggled_entity, self.upper_action)
      self.action_callback(self.upper_action)


class ToggleRangeEntity(ToggleRange):
  def __init__(self, base_obj, watched_entity, toggled_entity, **kwargs):
    self.toggled_entity = toggled_entity
    super().__init__(base_obj, watched_entity, **kwargs)

  def turn_on_or_off(self, toggled_entity, desired_state):
    self.log(f"turning {toggled_entity}: {desired_state}")
    if desired_state == 'on':
      self.base_obj.turn_on(toggled_entity)
    elif desired_state == 'off':
      self.base_obj.turn_off(toggled_entity)

  def action_callback(self, desired_state):
    super().action_callback(desired_state)

    self.turn_on_or_off(self.toggled_entity, desired_state)

  def get_current_state(self):
    return self.base_obj.get_state(self.toggled_entity)
