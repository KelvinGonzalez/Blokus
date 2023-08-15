class Transition:

  def __init__(self, key: str, target_id: int, listener=None, condition=None):
    self.key = key
    self.target_id = target_id
    self.listener = listener
    self.condition = condition


class State:

  def __init__(self, function=None, transitions: list[Transition] = None):
    if transitions is None:
      transitions = []
    self.function = function
    self.transitions = transitions

  def add_transition(self, transition: Transition):
    self.transitions.append(transition)
    return True

  def remove_transition(self, transition: Transition):
    if transition not in self.transitions:
      return False
    self.transitions.remove(transition)
    return True


class App:

  def __init__(self,
               states: list[State] = None,
               current_state: int = 0,
               data: dict = None):
    if states is None:
      states = []
    if data is None:
      data = {}
    self.states = states
    self.current_state = current_state
    self.data = data

  def add_state(self, state: State):
    i = 0
    while i < len(self.states):
      if self.states[i] is None:
        self.states[i] = state
        return i
      i += 1
    self.states.append(state)
    return len(self.states) - 1

  def remove_state(self, state_id: int):
    if state_id < 0 or state_id >= len(self.states):
      return False
    self.states[state_id] = None
    return True

  def add_transition(self, state_id: int, transition: Transition):
    if state_id < 0 or state_id >= len(self.states):
      return False
    return self.states[state_id].add_transition(transition)

  def remove_transition(self, state_id: int, transition: Transition):
    if state_id < 0 or state_id >= len(self.states):
      return False
    state = self.states[state_id]
    return state.remove_transition(transition)

  def call(self):
    if self.current_state < 0 or self.current_state >= len(self.states):
      return False
    state = self.states[self.current_state]
    if state.function is None:
      return False
    state.function(self.data)
    return True

  def transition(self, key: str):
    if self.current_state < 0 or self.current_state >= len(self.states):
      return False
    state = self.states[self.current_state]
    for transition in state.transitions:
      if transition.key == key:
        if transition.condition is not None:
          if not transition.condition(self.data):
            return False
        self.current_state = transition.target_id
        self.set_key("key", key)
        if transition.listener is not None:
          transition.listener(self.data)
        return True

  def get_key(self, key: str):
    if self.data is None:
      return None
    return self.data.get(key)

  def set_key(self, key: str, val):
    if self.data is None:
      return
    self.data[key] = val

  def clear(self):
    if self.data is None:
      return False
    self.data.clear()
    return True

  def get_current_state(self):
    if self.current_state < 0 or self.current_state >= len(self.states):
      return None
    return self.states[self.current_state]

  def get_state_id(self, state: State):
    for i, st in enumerate(self.states):
      if st == state:
        return i
