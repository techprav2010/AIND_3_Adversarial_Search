from sample_players import DataPlayer
import random
from math import sqrt
from math import exp, expm1

# SCORE_TYPE="ADVANCED" #""BASE" # "ADVANCED"
SCORE_TYPE= "BASE" # "ADVANCED"

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
        if SCORE_TYPE == "BASE": #SCORE_TYPE == "BASE":
            if state.ply_count < 2: self.queue.put(random.choice(state.actions()))
            self.queue.put(self.alpha_beta(state, depth=3))
        else:
            if self.player_id == self.player_id and 57 in state.actions():
                self.queue.put(57)
            for d in range(1, 9):
                move = self.alpha_beta(state, depth=d)
                self.queue.put(move)




    def alpha_beta(self, state, depth, alpha=float("-inf"), beta=float("inf")):

        def min_value(state, depth, alpha, beta, index):
            if state.terminal_test():
                return state.utility(self.player_id)
            if depth <= 0:
                return self.score(state)
            val = float("inf")
            for action in state.actions():
                val = min(val, max_value(state.result(action), depth - 1, alpha, beta, index))
                # print("MIN state=",state , " val=",val ,"depth=",depth ,"alpha=",alpha ,"beta=",beta , ", state.result(action)=",state.result(action))
                if val <= alpha:
                    return val
                beta = min(beta, val)
            return val

        def max_value(state, depth, alpha, beta, index):
            if state.terminal_test():
                return state.utility(self.player_id)
            if depth <= 0:
                return self.score(state)
            val = float("-inf")
            for action in state.actions():
                val = max(val, min_value(state.result(action), depth - 1, alpha, beta, index))
                # print("MAX state=", state, " val=", val, "depth=", depth, "alpha=", alpha, "beta=", beta,  ", state.result(action)=",state.result(action))
                if val >= beta:
                    return val
                alpha = max(alpha, val)
            return val

        best_score = float("-inf")
        best_move = random.choice(state.actions())
        # print("alpha_beta best_move=", best_move, "depth=", depth, "alpha=", alpha, "beta=", beta, "state=", state)
        for index, action in enumerate(state.actions()):
            val = min_value(state.result(action), depth - 1, alpha, beta, index)
            alpha = max(alpha, val)
            # print( "^^^^^^^^^^^^^^^^^^^^^^^ alpha_beta val=", val, "depth=", depth, "alpha=", alpha, "beta=", beta, "action-best_move=", action)
            if val > best_score:
                best_score = val
                best_move = action

        return best_move




    def score(self, state):
        if SCORE_TYPE == "BASE": #SCORE_TYPE == "BASE":
            return self.score_base(state)
        else:
            return self.score_advanced(state)

    def score_base(self, state):
        # moves available
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        own_moves = len(own_liberties)
        opp_moves = len(opp_liberties)
        # game over?
        if own_moves == 0:
            return float("inf")
        if opp_moves == 0:
            return float("-inf")

        val = (own_moves - opp_moves)
        return val

    def score_advanced(self, state):
        # count moves available
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        own_moves = len(own_liberties)
        opp_moves = len(opp_liberties)
        ply_count = state.ply_count
        #game over?
        if own_moves == 0:
            return float("inf")
        if opp_moves == 0:
            return float("-inf")
        own_center = self._center_dist_normalized(own_loc)
        opp_center = self._center_dist_normalized(opp_loc)
        center_weight = (opp_center - own_center)
        if  ply_count > 20  or center_weight > 0.8 :
            center_factor =  2 * center_weight
        elif center_weight < -0.5 :
            center_factor = center_weight
        else:
            center_factor = 0
        return (own_moves  - opp_moves) + center_factor

    def score_advanced2(self, state):
        # moves available
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties= state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        own_moves = len(own_liberties)
        opp_moves = len(opp_liberties)
        ply_count = state.ply_count

        # game over?
        if own_moves == 0:
            return float("inf")
        if opp_moves == 0:
            return float("-inf")


        # common moves -- shared moves first
        interects = len([value for value in opp_liberties if value in own_liberties])
        own_moves_future  = sum(len(state.liberties(liberty)) for liberty in own_liberties)
        opp_moves_future = sum(len(state.liberties(liberty)) for liberty in opp_liberties)


        # high score for staying close to center = advantage - more moves
        own_center = self._center_dist_normalized(own_loc)
        opp_center = self._center_dist_normalized(opp_loc)


        # 1: =>
        # #center position
        # center_weight = (own_center - opp_center ) #/ 90 #00.0 * moves_factor * interects / ply_count #(own_moves + opp_moves + ply_count ) / (own_moves + opp_moves) # (100/ply_count) #exp(ply_count)
        # if ply_count < 5:
        #     center_weight =  2.0 * center_weight
        # elif ply_count < 15:
        #     center_weight =  1.0 * center_weight
        # elif ply_count < 20:
        #     center_weight = 0.6 * center_weight
        # elif ply_count < 25:
        #     center_weight =  0.25 * center_weight
        # elif ply_count < 50:
        #     center_weight = 0.15 * center_weight
        # else:
        #     center_weight = 0

        # if own_moves > opp_moves :
        #     moves_factor=(2*own_moves - opp_moves)
        # else:
        #     moves_factor = (own_moves - 2*opp_moves)
        #
        # if self.player_id == 0 and interects > 0 and moves_factor > 0:
        #     interect_weight = 0.7 * moves_factor
        # else:
        #     interect_weight = 0
        # print("score ",val,", ply_count=",ply_count,
        #       ", moves_factor=",moves_factor,
        #       ", center_weight=",center_weight,  ", opp_center=",opp_center,", own_center=",own_center
        #       )
        # print("score ",val,", ply_count=",ply_count,
        #       ", moves_factor=",moves_factor,", own_moves=",own_moves,", opp_moves=",opp_moves,
        #       ", center_weight=",center_weight,  ", opp_center=",opp_center,", own_center=",own_center,
        #        ", (opp_center - own_center)=",(opp_center - own_center),
        #       ", center score=",(center_weight * (opp_center - own_center)),
        #       ", interect_weight=",interect_weight)
        # 2: =>
        # move_f=2
        # if own_moves > opp_moves :
        #     moves_factor=(move_f*own_moves - opp_moves)
        # else:
        #     moves_factor = (own_moves - move_f*opp_moves)
        # #center_weight = (own_center - opp_center) #center_weight = 0  #/ 90 #00.0 * moves_factor * interects / ply_count #(own_moves + opp_moves + ply_count ) / (own_moves + opp_moves) # (100/ply_count) #exp(ply_count)
        # center_weight = (opp_center - own_center) #center_weight = 0  #/ 90 #00.0 * moves_factor * interects / ply_count #(own_moves + opp_moves + ply_count ) / (own_moves + opp_moves) # (100/ply_count) #exp(ply_count)
        # # moves_factor = own_moves - opp_moves
        # if  moves_factor < 0 and center_weight > 0.8 :
        #     moves_factor += move_f #its ok to prefer center if the moves_factor is small
        # if moves_factor >=0 or  center_weight > 0 :
        #     # moves_factor +=1
        #     if interects > 0:
        #         moves_factor += 1
        #     if center_weight > 0:
        #         if ply_count < 5:
        #             center_weight = 2.0 * center_weight
        #         elif ply_count < 15:
        #             center_weight = 1.5 * center_weight
        #         elif ply_count < 20:
        #             center_weight = 1 * center_weight
        #         elif ply_count < 25:
        #             center_weight = 0.25 * center_weight
        #         elif ply_count < 50:
        #             center_weight = 0.025 * center_weight
        #         else:
        #             center_weight = 0
        #     moves_factor += center_weight
        # elif center_weight <= 0:
        #     moves_factor -= 1

        # 3: =>
        # moves
        # moves_factor =  (own_moves -  opp_moves)
        # center_weight = (  opp_center - own_center)
        # moves_factor_future = (opp_moves_future -  own_moves_future)
        # if moves_factor >= -1 :
        #     if ply_count < 20 and center_weight > 0.3:
        #         moves_factor += center_weight
        #     if center_weight > 0.8:
        #         moves_factor += 0.5
        #     if interects > 0 :
        #         moves_factor += 0.25
        #     if moves_factor_future > 0:
        #         moves_factor += 0.5 #* moves_factor_future
        # elif  center_weight < 0:
        #     moves_factor -=  center_weight
        # val= moves_factor  #+ center_weight  + interect_weight

        # 4a: =>  keep it simple
        # center_weight2 = (opp_center - own_center)
        # center_weight  = 0
        # interect_weight = 0
        # moves_factor = 10 * (own_moves - opp_moves)
        # if ply_count < 20 or center_weight2 > 0.8:
        #     center_weight = 5 * center_weight2 #(2 * opp_center - own_center)
        # moves_factor_future =  (opp_moves_future - own_moves_future) / 5
        # if interects  > 0:
        #     interect_weight = 0.5
        # val = moves_factor + center_weight + moves_factor_future  + interect_weight

        # 4: =>  keep it simple
        # moves
        cur_score=0
        center_weight  = (opp_center - own_center)
        moves_factor =   (own_moves - opp_moves)
        moves_factor_future = (own_moves_future - opp_moves_future)
        cur_score += moves_factor
        if ply_count < 20 or center_weight  > 0.8:
            cur_score +=  center_weight
        if interects  > 0:
            cur_score +=  interects * 0.2
        if moves_factor_future  > 0:
            cur_score += moves_factor_future * 0.2

        # print("score ",val,", ply_count=",ply_count,
        #       ", moves_factor=",moves_factor,
        #       ", center_weight=",center_weight, "opp_center=",opp_center,", own_center=",own_center,
        #       ", moves_factor_future=",moves_factor_future,
        #       ", interect_weight=",interect_weight
        #       )

        return cur_score

    def _center_dist_normalized(self, location):
        if location:
            x = (location - 1) % 11
            y = (location - 1) / 11
        else:
            x, y = (6, 5)
        width = 11
        height = 9
        dist = (((width / 2) - x) ** 2) + (((height / 2) - y) ** 2)
        dist_normalized = (sqrt(dist) / sqrt(((width / 2) ** 2) + ((height / 2) ** 2)))
        return dist_normalized

