import random
import numpy as np

BOARD_SIZE = 19
NUM_OBSTACLES = 4
WIN_REWARD = 100

class Game:
    EMPTY = 0
    PLAYER = 1
    ENEMY = 2
    OBSTACLE = 3

    CONTINUE = 0
    PLAYER_WIN = 1
    PLAYER_LOSE = 2

    def __init__(self, show_game=True, initial_player=True):
        self.board = [[Game.EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.num_obstacles = 0
        self._generate_obstacles()
        self.initial_player = initial_player
        self.turn_count = 0
        self.total_reward = 0.
        self.current_reward = 0.
        self.total_game = 0
        self.show_game = show_game
        if show_game:
            self.prepare_display()

    def _generate_obstacles(self, num_obstacles=NUM_OBSTACLES):
        while self.num_obstacles < num_obstacles:
            x, y = random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1)
            if self.board[x][y] == Game.EMPTY:
                self.num_obstacles += 1
                self.board[x][y] = Game.OBSTACLE

    def reset(self):
        self.current_reward = 0
        self.board = [[Game.EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.num_obstacles = 0
        self._generate_obstacles()
        self.turn_count = 0
        self.total_game += 1

    def prepare_display(self):
        for r in self.board:
            s = "|"
            for c in r:
                if c == Game.EMPTY:
                    s += " "
                elif c == Game.PLAYER:
                    s += "o"
                elif c == Game.ENEMY:
                    s += "x"
                else:
                    s += "-"
            s += "|"
            print(s)

    def _get_state(self):
        # 현재 2 차원 배열로 반환됨
        state = np.array(self.board)
        return state

    def _update_stone(self, moves, player=True):
        reward = 0.
        connected = 0
        for m in moves:
            x, y = m[0], m[1]
            if not self._is_valid_index(x, y):
                print("Error : trying to put at invalid slot", x, y)
                return -WIN_REWARD
            elif self.board[x][y] != Game.EMPTY:
                print("Error : trying to put stone in unempty slot", x, y, self.board[x][y])
                return -WIN_REWARD
            else:
                self.board[x][y] = Game.PLAYER if player else Game.ENEMY

            xx = x - 1
            while self._is_valid_index(xx, y) and self.board[xx][y] == Game.PLAYER:
                connected += 1
                xx -= 1
            xx = x + 1
            while self._is_valid_index(xx, y) and self.board[xx][y] == Game.PLAYER:
                connected += 1
                xx += 1
            yy = y - 1
            while self._is_valid_index(x, yy) and self.board[x][yy] == Game.PLAYER:
                connected += 1
                yy -= 1
            yy = y + 1
            while self._is_valid_index(x, yy) and self.board[x][yy] == Game.PLAYER:
                connected += 1
                yy += 1
            xx, yy = x - 1, y - 1
            while self._is_valid_index(xx, yy) and self.board[xx][yy] == Game.PLAYER:
                connected += 1
                xx, yy = xx - 1, yy - 1
            xx, yy = x + 1, y + 1
            while self._is_valid_index(xx, yy) and self.board[xx][yy] == Game.PLAYER:
                connected += 1
                xx, yy = xx + 1, yy + 1
            xx, yy = x - 1, y + 1
            while self._is_valid_index(xx, yy) and self.board[xx][yy] == Game.PLAYER:
                connected += 1
                xx, yy = xx - 1, yy + 1
            xx, yy = x + 1, y - 1
            while self._is_valid_index(xx, yy) and self.board[xx][yy] == Game.PLAYER:
                connected += 1
                xx, yy = xx + 1, yy - 1
        if player:
            self.turn_count += 1
        return connected / 100.

    def _is_valid_index(self, x, y):
        return x >= 0 and x < BOARD_SIZE and y >= 0 and y < BOARD_SIZE

    def _get_end_state(self, last_moves):
        for m in last_moves:
            x, y = m[0], m[1]
            connected = 1
            xx = x - 1
            while self._is_valid_index(xx, y) and self.board[xx][y] == Game.PLAYER:
                connected += 1
                xx -= 1
            xx = x + 1
            while self._is_valid_index(xx, y) and self.board[xx][y] == Game.PLAYER:
                connected += 1
                xx += 1
            if connected == 6:
                return Game.PLAYER_WIN
            elif connected > 6:
                return Game.PLAYER_LOSE

            connected = 1
            yy = y - 1
            while self._is_valid_index(x, yy) and self.board[x][yy] == Game.PLAYER:
                connected += 1
                yy -= 1
            yy = y + 1
            while self._is_valid_index(x, yy) and self.board[x][yy] == Game.PLAYER:
                connected += 1
                yy += 1
            if connected == 6:
                return Game.PLAYER_WIN
            elif connected > 6:
                return Game.PLAYER_LOSE

            connected = 1
            xx, yy = x - 1, y - 1
            while self._is_valid_index(xx, yy) and self.board[xx][yy] == Game.PLAYER:
                connected += 1
                xx, yy = xx - 1, yy - 1
            xx, yy = x + 1, y + 1
            while self._is_valid_index(xx, yy) and self.board[xx][yy] == Game.PLAYER:
                connected += 1
                xx, yy = xx + 1, yy + 1
            if connected == 6:
                return Game.PLAYER_WIN
            elif connected > 6:
                return Game.PLAYER_LOSE

            connected = 1
            xx, yy = x - 1, y + 1
            while self._is_valid_index(xx, yy) and self.board[xx][yy] == Game.PLAYER:
                connected += 1
                xx, yy = xx - 1, yy + 1
            xx, yy = x + 1, y - 1
            while self._is_valid_index(xx, yy) and self.board[xx][yy] == Game.PLAYER:
                connected += 1
                xx, yy = xx + 1, yy - 1
            if connected == 6:
                return Game.PLAYER_WIN
            elif connected > 6:
                return Game.PLAYER_LOSE
        return Game.CONTINUE

    def step(self, action):
        reward = self._update_stone(action)
        if reward < 0:
            return self._get_state(), reward, Game.PLAYER_LOSE # game over
        reward += 1. / ((self.turn_count + 1) ** 2)
        end_state = self._get_end_state(action)
        if end_state == Game.PLAYER_LOSE:
            reward = -WIN_REWARD
            return self._get_state(), reward, Game.PLAYER_LOSE
        elif end_state == Game.PLAYER_WIN:
            reward += WIN_REWARD
            return self._get_state(), reward, Game.PLAYER_WIN
        else:
            return self._get_state(), reward, Game.CONTINUE

    def random_empty_slots(self, count):
        rt = []
        for i in range(count):
            x, y = 0, 0
            order = random.randint(1, BOARD_SIZE * BOARD_SIZE)
            while order > 0:
                x = (x + 1) % BOARD_SIZE
                if x == 0:
                    y = (y + 1) % BOARD_SIZE
                if self.board[x][y] == Game.EMPTY and (len(rt) == 0 or rt[-1][0] != x or rt[-1][1] != y):
                    order -= 1
            rt.append([x, y])
        return rt

if __name__ == '__main__':
    g1, g2 = Game(), Game()
    for i in range(len(g1.board)):
        for j in range(len(g1.board[0])):
            g2.board[i][j] = g1.board[i][j]

    for i in range(1000):
        mv1 = g1.random_empty_slots(min(i+1, 2))
        state, reward, game_over = g1.step(mv1)
        g2._update_stone(mv1, False)
        if game_over != Game.CONTINUE:
            print("first player : ", game_over, mv1)
            break
        mv2 = g2.random_empty_slots(2)
        state, reward, game_over = g2.step(mv2)
        g1._update_stone(mv2, False)
        if game_over != Game.CONTINUE:
            print("second player : ", game_over, mv2)
            break
    g1.prepare_display()
    print(reward, game_over)
