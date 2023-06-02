class ToggleRange:
  def __init__(self, base_obj, watched_entity, toggled_entity, lower=None, upper=None, lower_action="off", upper_action="on"):
    self.base_obj = base_obj

    self.toggled_entity = toggled_entity

    self.lower = lower
    self.upper = upper
    self.lower_action = lower_action
    self.upper_action = upper_action

    self.base_obj.listen_state(self.process_new_value, watched_entity)
    self.process_new_value(watched_entity, {}, None, self.base_obj.get_state(watched_entity), None)

  def turn_on_or_off(self, toggled_entity, desired_state):
    self.base_obj.log(f"turning {toggled_entity}: {desired_state}")
    if desired_state == 'on':
      self.base_obj.turn_on(toggled_entity)
    elif desired_state == 'off':
      self.base_obj.turn_off(toggled_entity)

  def process_new_value(self, entity, attribute, old, new, kwargs):
    self.base_obj.log(f"got new data: {entity}, {attribute}, {old}, {new}, {kwargs}")
    current_state = self.base_obj.get_state(self.toggled_entity)

    self.base_obj.log(f"current_state: {current_state}")

    if new == 'unavailable':
      return

    new = float(new)

    if new < self.lower and current_state != self.lower_action:
      self.turn_on_or_off(self.toggled_entity, self.lower_action)
    elif new > self.upper and current_state != self.upper_action:
      self.turn_on_or_off(self.toggled_entity, self.upper_action)

