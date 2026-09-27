#!/usr/bin/env python
# Olivier Georgeon, 2021.
# This code is used to teach Developmental AI.

# TODO: Uncomment the environment to test your agent in one of these more complex environment
# from turtlepy_enacter import TurtlePyEnacter
# from PetitCatEnacter import PetitCatEnacter
# from turtlesim_enacter import TurtleSimEnacter # requires ROS


class Agent:
    def __init__(self, _valence_table):
        """ Creating our agent """
        self._valence_table = _valence_table
        self._action = None
        self._anticipated_outcome = None

    def action(self, _outcome):
        """ tracing the previous cycle """
        if self._action is not None:
            print("Action: " + str(self._action) +
                  ", Anticipation: " + str(self._anticipated_outcome) +
                  ", Outcome: " + str(_outcome) +
                  ", Satisfaction: (anticipation: " + str(self._anticipated_outcome == _outcome) +
                  ", valence: " + str(self._valence_table[self._action][_outcome]) + ")")

        """ Computing the next action to enact """
        # TODO: Implement the agent's decision mechanism
        self._action = 0
        # TODO: Implement the agent's anticipation mechanism
        self._anticipated_outcome = 0
        return self._action

class Agent1(Agent):
    def __init__(self, _valence_table):
        super().__init__(_valence_table)
        self._memory = {}
        self._nb_correct = 0
        self._boredom_threshold = 4

    def action(self, _outcome):
        if self._action is not None:
            correct_prediction = (self._anticipated_outcome == _outcome)
            print("Action: " + str(self._action) +
                  ", Anticipation: " + str(self._anticipated_outcome) +
                  ", Outcome: " + str(_outcome) +
                  ", Satisfaction: (anticipation: " + str(correct_prediction) +
                  ", valence: " + str(self._valence_table[self._action][_outcome]) + ")")

            self._memory[self._action] = _outcome

            if correct_prediction:
                self._nb_correct += 1
            else:
                self._nb_correct = 0

        nb_actions = len(self._valence_table)
        if self._nb_correct >= self._boredom_threshold:
            self._action = (self._action + 1) % nb_actions
            self._nb_correct = 0
        elif self._action is None:
            self._action = 0

        self._anticipated_outcome = self._memory.get(self._action, 0)
        return self._action

class Environment1:
    """ In Environment 1, action 0 yields outcome 0, action 1 yields outcome 1 """
    def outcome(self, _action):
        # return int(input("entre 0 1 ou 2"))
        if _action == 0:
            return 0
        else:
            return 1


class Environment2:
    """ In Environment 2, action 0 yields outcome 1, action 1 yields outcome 0 """
    def outcome(self, _action):
        if _action == 0:
            return 1
        else:
            return 0


class Environment3:
    """ Environment 3 yields outcome 1 only when the agent alternates actions 0 and 1 """
    def __init__(self):
        """ Initializing Environment3 """
        self.previous_action = 0

    def outcome(self, _action):
        _outcome = 1
        if _action == self.previous_action:
            _outcome = 0
        self.previous_action = _action
        return _outcome


# TODO Define the valance of interactions (action, outcome)
valences = [[-1, 1], [-1, 1]]
# valences = [[1, -1], [1, -1]]
# TODO Choose an agent
#a = Agent(valences)
a = Agent1(valences)
# TODO Choose an environment
e = Environment1()
# e = Environment2()
# e = Environment3()
# e = TurtlePyEnacter()
# e = TurtleSimEnacter()

if __name__ == '__main__':
    """ The main loop controlling the interaction of the agent with the environment """
    outcome = 0
    for i in range(20):
        action = a.action(outcome)
        outcome = e.outcome(action)
