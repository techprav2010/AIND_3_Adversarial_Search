
from sample_players import DataPlayer


class CustomPlayer(DataPlayer):
    """ Implement your own agent to play knight's Isolation

    The get_action() method is the only *required* method. You can modify
    the interface for get_action by adding named parameters with default
    values, but the function MUST remain compatible with the default
    interface.

    **********************************************************************
    NOTES:
    - You should **ONLY** call methods defined on your agent class during
      search; do **NOT** add or call functions outside the player class.
      The isolation library wraps each method of this class to interrupt
      search when the time limit expires, but the wrapper only affects
      methods defined on this class.

    - The test cases will NOT be run on a machine with GPU access, nor be
      suitable for using any other machine learning techniques.
    **********************************************************************
    """
    def get_action(self, state):
        """ Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller is responsible for
        cutting off the function after the search time limit has expired. 

        See RandomPlayer and GreedyPlayer in sample_players for more examples.

        **********************************************************************
        NOTE: 
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        # TODO: Replace the example implementation below with your own search
        #       method by combining techniques from lecture
        #
        # EXAMPLE: choose a random move without any search--this function MUST
        #          call self.queue.put(ACTION) at least once before time expires
        #          (the timer is automatically managed for you)
        import random
        # self.queue.put(random.choice(state.actions()))
        if state.ply_count < 2:
            self.queue.put(random.choice(state.actions()))
        else:
            self.queue.put(self.minmax(state, depth=100))

    def minmax(self, state, depth):
        alpha = float("-inf")
        beta = float('inf')
        best_score = float("-inf")
        best_move = None
        for action in state.actions():
            value = self.min_value(state.result(action), depth - 1, alpha, beta)
            alpha = max(alpha, value)
            if value > best_score:
                best_score = value
                best_move = action
        return best_move


    def max_value(self, state, depth, alpha, beta):
        if state.terminal_test() or depth <= 0:
            return self.score(state)
        v = float('-inf')
        for action in state.actions():
            v = max(v,self.min_value(state.result(action), depth - 1, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)

        return v

    def min_value(self, state, depth, alpha, beta):
        if state.terminal_test() or depth <= 0:
            return self.score(state)
        v = float('inf')
        for action in state.actions():
            v = min(v, self.max_value(state.result(action), depth - 1, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    def score(self, state):
        self_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        self_liberties = state.liberties(self_loc)
        opp_liberties = state.liberties(opp_loc)
        if len(self_liberties) < len(opp_liberties):
            return 2 * len(self_liberties) - len(opp_liberties)
        else:
            return len(self_liberties) - 2 * len(opp_liberties)