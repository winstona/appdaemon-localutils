

class ADSwitch:
  def __init__(self, base_obj, entity_name, initial_state='retain', event_handler=None):
    self.entity_id = f"switch.{entity_name}"
    self.event_handler = event_handler
    self.base_obj = base_obj
    if initial_state == 'retain':
      initial_state = base_obj.get_state(self.entity_id)

    if initial_state == 'retain' or initial_state == None:
      initial_state = 'off'
    base_obj.set_state(self.entity_id, state=initial_state)
    base_obj.listen_event(self.event_listen, event="call_service", domain='switch', service_data={'entity_id': self.entity_id})

  def event_listen(self, event_name, *args):
    self.base_obj.log(f"got event: {args}")
    new_state = None
    if args[0]['service'] == 'turn_on':
       self.base_obj.log("setting enable to true")
       new_state = 'on'
    elif args[0]['service'] == 'turn_off':
       self.base_obj.log("setting enable to false")
       new_state = 'off'
    
    if new_state != None:
      self.base_obj.set_state(self.entity_id, state=new_state)

      if self.event_handler:
        self.event_handler(self.entity_id, 'state', None, new_state, {})

  def get_state(self):
    return self.base_obj.get_state(self.entity_id)

  def set_state(self, state):
    return self.base_obj.set_state(self.entity_id, state=state)




class ADSelect:
  def __init__(self, base_obj, entity_name, options, initial_state='retain', event_handler=None, call_event_handler_on_init=False, attributes={}):
    self.entity_id = f"select.{entity_name}"
    self.event_handler = event_handler
    self.base_obj = base_obj
    if initial_state == 'retain':
      initial_state = base_obj.get_state(self.entity_id)

    if initial_state == 'retain' or initial_state == None:
      initial_state = options[0]
    base_obj.set_state(self.entity_id, state=initial_state, attributes={**{'options': options}, **attributes})
    base_obj.listen_event(self.event_listen, event="call_service", domain="select")

    if call_event_handler_on_init and event_handler is not None:
      self.event_handler(self.entity_id, 'state', None, initial_state, {})

  def event_listen(self, event_name, *args):
    if self.entity_id not in args[0]['service_data']['entity_id']:
      return

    self.base_obj.log(f"got event2: {args}")
    new_state = args[0]['service_data']['option']
    
    self.base_obj.set_state(self.entity_id, state=new_state)

    if self.event_handler:
      self.event_handler(self.entity_id, 'state', None, new_state, {})

  def get_state(self):
    return self.base_obj.get_state(self.entity_id)

  def set_state(self, state):
    return self.base_obj.set_state(self.entity_id, state=state)
