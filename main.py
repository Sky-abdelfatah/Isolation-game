# ===============================
# Isolation Game - Complete GUI + AI + Sound
# ===============================

import sys, math, random, threading
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QGridLayout, QFrame
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from playsound import playsound
from PyQt5.QtWidgets import QStackedLayout
import random
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon

class ToggleButton(QPushButton):
    def __init__(self, text, group=None):
        super().__init__(text)
        self.group = group
        self.setCheckable(True)
        self.setFont(QFont("Arial", 16, QFont.Bold))
        self.setStyleSheet("""
            QPushButton {
                background:#1e1e2f;
                color:white;
                border-radius:15px;
                padding:10px;
            }
            QPushButton:checked {
                background:#EDBB00;
                color:black;
                font-weight:bold;
            }
        """)
        self.clicked.connect(self.on_clicked)
        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(150)
        self.anim.setEasingCurve(QEasingCurve.OutQuad)

    def on_clicked(self):
        # تفصل الباقي في نفس المجموعة
        if self.group:
            for btn in self.group:
                if btn != self:
                    btn.setChecked(False)
        # Animation خفيف
        geom = self.geometry()
        self.anim.stop()
        self.anim.setStartValue(geom)
        self.anim.setEndValue(geom.adjusted(-5,-5,5,5))
        self.anim.start()


# -------- COLORS --------
BLUE = "#004D98"
RED = "#A50044"
YELLOW = "#EDBB00"
DARK_BG = "#0B1C2D"
BOARD_COLOR_1 = "#0f1d5e"
BOARD_COLOR_2 = "#ab2d42"

# -------- BUTTON STYLE --------
def button_style():
    return f"""
        QPushButton {{
            background:{RED};
            color:white;
            font-size:18px;
            font-weight:bold;
            border-radius:18px;
        }}
        QPushButton:hover {{
            background:{YELLOW};
            color:black;
        }}
    """

def toggle_style():
    return """
        QPushButton {
            background:#1e1e2f;
            color:white;
            font-size:16px;
            padding:10px;
            border-radius:15px;
        }
        QPushButton:checked {
            background:#EDBB00;
            color:black;
            font-weight:bold;
        }
    """

# -------- HoverButton for Menu --------
class HoverButton(QPushButton):
    def __init__(self, text, width=250, height=60):
        super().__init__(text)
        self.default_width = width
        self.default_height = height
        self.setFixedSize(self.default_width, self.default_height)
        self.setStyleSheet(button_style())

    def enterEvent(self, event):
        self.setFixedSize(int(self.default_width*1.2), int(self.default_height*1.2))

    def leaveEvent(self, event):
        self.setFixedSize(self.default_width, self.default_height)


def play_click_sound():
    threading.Thread(
        target=lambda: playsound("click.mp3"),
        daemon=True
    ).start()

# =========================================
# MENU SCREEN
# =========================================

class MenuScreen(QWidget):
    def __init__(self, main):
        super().__init__()
        self.bg_label = QLabel()
        self.bg_label.setPixmap(QPixmap("3 .png"))
        self.bg_label.setScaledContents(True)  # <<< دي أهم سطر

        self.main = main



        #Difficulty Buttons
        diff_label = QLabel("Select Difficulty")
        diff_label.setAlignment(Qt.AlignCenter)
        diff_label.setFont(QFont("Arial", 20, QFont.Bold))
        diff_label.setStyleSheet("color:white;")

        self.diff_buttons = []
        diff_layout = QVBoxLayout()
        diff_layout.addWidget(diff_label)

        for text in ["Easy", "Medium", "Hard"]:
            btn = ToggleButton(text, group=self.diff_buttons)
            self.diff_buttons.append(btn)
            diff_layout.addWidget(btn)
        self.diff_buttons[0].setChecked(True)



        #Mode Buttons
        mode_label = QLabel("Select Game Mode")
        mode_label.setAlignment(Qt.AlignCenter)
        mode_label.setFont(QFont("Arial", 20, QFont.Bold))
        mode_label.setStyleSheet("color:white;")

        self.mode_buttons = []
        mode_layout = QVBoxLayout()
        mode_layout.addWidget(mode_label)

        for text in ["Player vs Player", "Player vs AI", "AI vs AI"]:
            btn = ToggleButton(text, group=self.mode_buttons)
            self.mode_buttons.append(btn)
            mode_layout.addWidget(btn)
        self.mode_buttons[0].setChecked(True)

        # Buttons
        start_btn = HoverButton("START GAME")
        start_btn.clicked.connect(self.start_game)
        how_btn = HoverButton("HOW TO PLAY")
        how_btn.clicked.connect(self.show_how_to_play)
        exit_btn = HoverButton("EXIT")
        exit_btn.clicked.connect(sys.exit)
        btn_layout = QVBoxLayout()
        btn_layout.addWidget(start_btn)
        btn_layout.addSpacing(15)
        btn_layout.addWidget(how_btn)
        btn_layout.addSpacing(15)
        btn_layout.addWidget(exit_btn)
        btn_layout.setAlignment(Qt.AlignCenter)
        start_btn.clicked.connect(play_click_sound)
        how_btn.clicked.connect(play_click_sound)
        exit_btn.clicked.connect(play_click_sound)

        # Top layout: Difficulty + Mode
        top_layout = QHBoxLayout()
        top_layout.addLayout(diff_layout)
        top_layout.addSpacing(50)
        top_layout.addLayout(mode_layout)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addStretch()
        main_layout.addLayout(top_layout)
        main_layout.addSpacing(30)
        main_layout.addLayout(btn_layout)
        main_layout.setContentsMargins(50,50,50,50)
        content = QWidget()
        content.setLayout(main_layout)

        content.setAttribute(Qt.WA_StyledBackground, True)
        content.setStyleSheet("background: transparent;")

        root = QStackedLayout()
        root.setStackingMode(QStackedLayout.StackAll)  # <<< دي المهمة جدًا
        root.addWidget(self.bg_label)
        root.addWidget(content)

        self.setLayout(root)

        self.setLayout(root)
        self.setContentsMargins(0, 0, 0, 0)
        self.setMinimumSize(1, 1)

    def start_game(self):
        selected_diff = next(b.text() for b in self.diff_buttons if b.isChecked())
        selected_mode = next(b.text() for b in self.mode_buttons if b.isChecked())
        self.main.game_screen.difficulty = selected_diff
        self.main.game_screen.game_mode = selected_mode

        # reset + redraw icons
        self.main.game_screen.reset_game()
        self.main.game_screen.update_board()

        # مهم: نفتح Game Screen بس بدون بدء اللعبة
        self.main.go_to_game()

        # Game Screen ما تبدأش اللعبة إلا بعد الضغط على START داخله
        self.main.game_screen.game_started = False

    def show_how_to_play(self):
        self.how_window = QWidget()
        self.how_window.setWindowTitle("How to Play")
        label = QLabel(self.how_window)
        pixmap = QPixmap("how_to_play.png")
        screen_geom = QApplication.primaryScreen().availableGeometry()
        max_width = int(screen_geom.width() * 0.8)
        max_height = int(screen_geom.height() * 0.8)
        if pixmap.width() > max_width or pixmap.height() > max_height:
            pixmap = pixmap.scaled(max_width, max_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.how_window.setLayout(layout)
        self.how_window.resize(pixmap.width(), pixmap.height())
        self.how_window.show()



# =========================================
# AI LOGIC
# =========================================
def get_moves(current, other, board_state):
    moves=[]
    dirs=[(-1,0),(1,0),(0,-1),(0,1)]
    for dr,dc in dirs:
        nr,nc=current[0]+dr,current[1]+dc
        if 0<=nr<7 and 0<=nc<7 and not board_state[nr][nc] and [nr,nc]!=other:
            moves.append([nr,nc])
    return moves

def heuristic_move_state(bd,posA,posB,turn):
    current = posA if turn=="A" else posB
    other = posB if turn=="A" else posA
    moves = get_moves(current,other,bd)
    if not moves: return None
    best_score=-1e9; best_move=None
    for mv in moves:
        tmp=[row[:] for row in bd]; tmp[current[0]][current[1]]=True
        tA = mv if turn=="A" else posA
        tB = mv if turn=="B" else posB
        dist = abs(tA[0]-tB[0])+abs(tA[1]-tB[1])
        own = len(get_moves(tA if turn=="A" else tB, tB if turn=="A" else tA, tmp))
        opp = len(get_moves(tB if turn=="A" else tA, tA if turn=="A" else tB, tmp))
        score = dist+own*1.5-opp*2
        if score>best_score: best_score=score; best_move=mv
    return best_move

class MCTSNode:
    def __init__(self,state,parent=None,move=None):
        self.state=state; self.parent=parent; self.move=move; self.children=[]; self.visits=0; self.wins=0
    def is_fully_expanded(self):
        bd,pA,pB,tr=self.state
        cur=pA if tr=="A" else pB; other=pB if tr=="A" else pA
        return len(self.children)==len(get_moves(cur,other,bd))
    def best_child(self,c=1.4):
        scores=[(float('inf') if ch.visits==0 else ch.wins/ch.visits+c*math.sqrt(2*math.log(self.visits)/ch.visits)) for ch in self.children]
        return self.children[scores.index(max(scores))]
    def expand(self):
        bd,pA,pB,tr=self.state
        cur=pA if tr=="A" else pB; other=pB if tr=="A" else pA
        moves=get_moves(cur,other,bd); used=[c.move for c in self.children]
        for mv in moves:
            if mv not in used:
                new_bd=[row[:] for row in bd]; new_bd[cur[0]][cur[1]]=True
                new_pA=mv if tr=="A" else pA; new_pB=mv if tr=="B" else pB
                child=MCTSNode((new_bd,new_pA,new_pB,"B" if tr=="A" else "A"),parent=self,move=mv)
                self.children.append(child)
                return child
        return None

def mcts_ai_move(bd,posA,posB,turn,simulations=30):
    root=MCTSNode((bd,posA,posB,turn))
    for _ in range(simulations):
        node=root
        while node.children and node.is_fully_expanded(): node=node.best_child()
        child=node.expand() or node
        sim_bd=[row[:] for row in child.state[0]]; simA=child.state[1][:]; simB=child.state[2][:]; simT=child.state[3]
        winner=None
        for _ in range(20):
            moves=get_moves(simA,simB,sim_bd) if simT=="A" else get_moves(simB,simA,sim_bd)
            if not moves: winner="B" if simT=="A" else "A"; break
            move=random.choice(moves)
            if simT=="A": sim_bd[simA[0]][simA[1]]=True; simA=move; simT="B"
            else: sim_bd[simB[0]][simB[1]]=True; simB=move; simT="A"
        node_=child
        while node_:
            node_.visits+=1
            if winner==turn: node_.wins+=1
            node_=node_.parent
    return root.best_child(c=0).move if root.children else None

# =========================================

from PyQt5.QtWidgets import QDialog

class WinDialog(QDialog):
    def __init__(self, winner, main):
        super().__init__()
        self.main = main
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(400, 300)

        bg = QFrame(self)
        bg.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0f1d5e, stop:1 #ab2d42
                );
                border-radius:25px;
            }
        """)
        bg.setGeometry(0, 0, 400, 300)

        title = QLabel("🎉 CONGRATULATIONS 🎉")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #EDBB00; font-size:22px; font-weight:bold;")

        winner_lbl = QLabel(f"Player {winner} Wins!")
        winner_lbl.setAlignment(Qt.AlignCenter)
        winner_lbl.setStyleSheet("color:white; font-size:20px;")

        play_again = QPushButton("🔁 Play Again")
        menu_btn = QPushButton("🏠 Main Menu")

        for b in (play_again, menu_btn):
            b.setStyleSheet("""
                QPushButton {
                    background:#EDBB00;
                    color:black;
                    font-size:16px;
                    font-weight:bold;
                    border-radius:15px;
                    padding:10px;
                }
                QPushButton:hover {
                    background:white;
                }
            """)

        play_again.clicked.connect(self.restart)
        menu_btn.clicked.connect(self.go_menu)

        btns = QVBoxLayout()
        btns.addWidget(play_again)
        btns.addWidget(menu_btn)

        layout = QVBoxLayout(bg)
        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(winner_lbl)
        layout.addSpacing(20)
        layout.addLayout(btns)
        layout.addStretch()

    def restart(self):
        self.close()
        self.main.game_screen.reset_game()  # بس Reset
        self.main.go_to_game()  # نرجع للجيم سكرين

    def go_menu(self):
        self.close()
        self.main.game_screen.reset_game()
        self.main.go_to_menu()

# GAME SCREEN
# =========================================
class GameScreen(QWidget):
    def __init__(self, main):
        # Load icons
        self.icons = {
            "player_A": QPixmap("player_A.png"),
            "player_B": QPixmap("player_B.png"),
            "robot_A": QPixmap("robot_A.png"),
            "robot_B": QPixmap("robot_B.png"),
            "footprint": QPixmap("footprint.png")
        }

        #cheer messages
        self.cheer_messages = [
            "🔥 Nice move!",
            "🎉 Great choice!",
            "🥳 Well played!",
            "💪 Keep going!",
            "😎 Smart move!",
            "⚡ You're on fire!"
        ]



        super().__init__()
        self.main = main
        self.grid_size = 7
        self.board_colors = [BOARD_COLOR_1, BOARD_COLOR_2]
        self.posA = [0, 0]
        self.posB = [6, 6]
        self.visited = [[False] * self.grid_size for _ in range(self.grid_size)]
        self.current_player = "A"
        self.game_mode = "Player vs Player"
        self.difficulty = "Easy"

        self.game_started = False  # <<< هنا نضيف Flag للعبة
        self.game_active = False

        header=QLabel("ISOLATION GAME"); header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet(f"background:{BLUE}; color:{YELLOW}; font-size:26px; font-weight:bold; padding:15px;")

        # Board
        self.board_grid=QGridLayout(); self.board_grid.setSpacing(0)
        self.squares=[]
        for r in range(self.grid_size):
            row_squares=[]
            for c in range(self.grid_size):
                btn=QPushButton(); btn.setFixedSize(80,80)
                color=self.board_colors[(r+c)%2]
                btn.setStyleSheet(f"background:{color}; border:1px solid black; font-size:24px; font-weight:bold;")
                self.board_grid.addWidget(btn,r,c)
                row_squares.append(btn)
            self.squares.append(row_squares)

        self.update_board()
        self.info_label=QLabel(""); self.info_label.setStyleSheet("color:white; font-size:18px;"); self.info_label.setAlignment(Qt.AlignCenter)

        # Arrow buttons
        arrows_layout=QGridLayout(); arrows_layout.setSpacing(10)
        self.arrow_up=self.arrow_btn("↑"); self.arrow_down=self.arrow_btn("↓")
        self.arrow_left=self.arrow_btn("←"); self.arrow_right=self.arrow_btn("→")
        arrows_layout.addWidget(self.arrow_up,0,1); arrows_layout.addWidget(self.arrow_left,1,0)
        arrows_layout.addWidget(self.arrow_right,1,2); arrows_layout.addWidget(self.arrow_down,2,1)
        self.arrow_up.clicked.connect(lambda: self.arrow_move(-1,0))
        self.arrow_down.clicked.connect(lambda: self.arrow_move(1,0))
        self.arrow_left.clicked.connect(lambda: self.arrow_move(0,-1))
        self.arrow_right.clicked.connect(lambda: self.arrow_move(0,1))

        self.set_arrows_enabled(False)




        # Control buttons
        self.start_btn = QPushButton("START"); self.reset_btn=QPushButton("RESET"); self.back_btn=QPushButton("BACK TO MENU")
        for b in (self.start_btn,self.reset_btn,self.back_btn):
            b.setStyleSheet(button_style()); b.setFixedHeight(40)
        self.back_btn.clicked.connect(self.exit_to_menu)
        self.start_btn.clicked.connect(self.start_game_loop)
        self.reset_btn.clicked.connect(self.start_game_loop)

        side=QVBoxLayout(); side.addWidget(self.info_label); side.addSpacing(20)

        side.addLayout(arrows_layout); side.addSpacing(20)
        self.feedback_label = QLabel("")
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.feedback_label.setWordWrap(True)
        self.feedback_label.setStyleSheet("""
            color:#EDBB00;
            font-size:16px;
            font-weight:bold;
        """)
        self.start_btn.clicked.connect(play_click_sound)
        self.reset_btn.clicked.connect(play_click_sound)
        self.back_btn.clicked.connect(play_click_sound)
        self.feedback_label.setStyleSheet("""
                           color:#EDBB00;
                           font-size:16px;
                           font-weight:bold;
                           background: rgba(0,0,0,0.4);
                           padding:8px;
                           border-radius:10px;
                       """)

        side.addWidget(self.feedback_label)
        side.addSpacing(15)

        side.addWidget(self.start_btn); side.addWidget(self.reset_btn); side.addWidget(self.back_btn)
        side.addStretch()

        board_frame=QFrame(); board_frame.setLayout(self.board_grid)
        body=QHBoxLayout(); body.addWidget(board_frame); body.addLayout(side)

        layout=QVBoxLayout(); layout.addWidget(header); layout.addLayout(body)
        self.setLayout(layout)



    def exit_to_menu(self):
        self.game_active = False
        self.game_started = False
        self.set_arrows_enabled(False)
        self.main.go_to_menu()

    def show_feedback(self):
        # نختار بشكل احتمالي هل نعرض الرسالة ونعمل الصوت
        if random.random() < 0.5:  # 50% احتمال تشغيل الصوت
            msg = random.choice(self.cheer_messages)
            self.feedback_label.setText(msg)

            # تشغيل الصوت في Thread عشان مش يوقف اللعبة
            threading.Thread(
                target=lambda: playsound("crowd-cheering-sound-effect-258730.mp3"),
                daemon=True
            ).start()

            # يخفي الرسالة بعد 1.2 ثانية
            QTimer.singleShot(1200, lambda: self.feedback_label.setText(""))

    def get_player_icon(self, player):
        if self.game_mode == "Player vs Player":
            return self.icons["player_A"] if player == "A" else self.icons["player_B"]
        elif self.game_mode == "Player vs AI":
            return self.icons["player_A"] if player == "A" else self.icons["robot_A"]
        elif self.game_mode == "AI vs AI":
            return self.icons["robot_A"] if player == "A" else self.icons["robot_B"]


    def arrow_btn(self,text):
        btn=QPushButton(text); btn.setFixedSize(80,80)
        btn.setStyleSheet(f"""
            QPushButton {{
                background:{RED}; color:{YELLOW}; font-size:32px; font-weight:bold; border-radius:20px;
            }}
            QPushButton:hover {{
                background:{YELLOW}; color:{RED};
            }}
        """)
        return btn

    def set_arrows_enabled(self, enabled):
        for btn in [self.arrow_up, self.arrow_down, self.arrow_left, self.arrow_right]:
            btn.setEnabled(enabled)
            btn.setStyleSheet(
                f"""
                QPushButton {{
                    background:{RED if enabled else '#555'};
                    color:{YELLOW if enabled else '#aaa'};
                    font-size:32px;
                    font-weight:bold;
                    border-radius:20px;
                }}
                """
            )

    def arrow_move(self,dr,dc):
        pos = self.posA if self.current_player=="A" else self.posB
        other = self.posB if self.current_player=="A" else self.posA
        moves = get_moves(pos,other,self.visited)
        target = [pos[0]+dr,pos[1]+dc]
        if target in moves: self.make_move(target)

    def start_game_loop(self):
        # reset board and players
        self.visited = [[False] * self.grid_size for _ in range(self.grid_size)]
        self.posA = [0, 0]
        self.posB = [6, 6]
        self.current_player = "A"

        self.update_board()
        self.update_info_label()

        # اللعبة تبدأ
        self.reset_game()
        self.game_started = True
        self.game_active = True  # <<< جديد

        self.set_arrows_enabled(True)  # <<< تفعيل الأسهم

        # لو فيه AI يلعب أول حركة
        QTimer.singleShot(300, self.ai_turn)

    def update_board(self):
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                btn=self.squares[r][c]; color=self.board_colors[(r+c)%2]; btn.setText("")
                if self.visited[r][c]:
                    btn.setIcon(QIcon(self.icons["footprint"]))  # <<< QIcon بدل QPixmap
                    btn.setIconSize(btn.size())
                else:
                    btn.setIcon(QIcon())  # <<< هنا نمسح أي أيقونة بشكل صحيح

        self.draw_player(self.posA,'A'); self.draw_player(self.posB,'B')

    def draw_player(self, pos, player):
        r, c = pos
        btn = self.squares[r][c]
        icon = self.get_player_icon(player)
        btn.setIcon(QIcon(icon))  # <<< QIcon بدل QPixmap
        btn.setIconSize(btn.size())
        btn.setText("")


    def update_info_label(self):
        self.info_label.setText(f"{self.game_mode} | {self.difficulty} | Turn: {self.current_player}")

    def reset_game(self):
        self.visited = [[False] * self.grid_size for _ in range(self.grid_size)]
        self.posA = [0, 0]
        self.posB = [6, 6]
        self.current_player = "A"
        self.game_active = False  # <<< مهم
        self.game_started = False
        self.update_board()
        self.update_info_label()
        self.set_arrows_enabled(False)

    def make_move(self,new_pos):
        pos=self.posA if self.current_player=="A" else self.posB
        self.visited[pos[0]][pos[1]]=True
        pos[0],pos[1]=new_pos[0],new_pos[1]
        self.update_board()
        if self.game_mode != "AI vs AI" and self.current_player == "A":
            self.show_feedback()
        self.current_player="B" if self.current_player=="A" else "A"
        self.update_info_label()
        if self.check_winner():
            return
        QTimer.singleShot(300,self.ai_turn)

    def check_winner(self):
        movesA = get_moves(self.posA, self.posB, self.visited)
        movesB = get_moves(self.posB, self.posA, self.visited)

        if not movesA:
            threading.Thread(
                target=lambda: playsound("lose_sound.mp3"),
                daemon=True
            ).start()
            self.show_win("B")
            return True

        if not movesB:
            threading.Thread(target=lambda: playsound("win_sound.mp3")).start()
            self.show_win("A")
            return True

        return False

    def show_win(self, winner):
        if not self.game_active:
            return
        dialog = WinDialog(winner, self.main)
        dialog.exec_()

    def ai_turn(self):
        if not self.game_active or not self.game_started:
            return

        if (self.game_mode == "Player vs AI" and self.current_player == "B") or self.game_mode == "AI vs AI":
            if self.difficulty == "Easy":
                move = heuristic_move_state(self.visited, self.posA, self.posB, self.current_player)
            else:
                move = mcts_ai_move(self.visited, self.posA, self.posB, self.current_player,
                                    simulations=30 if self.difficulty == "Medium" else 80)
            if move:
                self.make_move(move)


# =========================================
# MAIN WINDOW
# =========================================
class IsolationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Isolation Game")
        screen = QApplication.primaryScreen().availableGeometry()
        self.resize(int(screen.width()*0.7),int(screen.height()*0.7))
        self.setStyleSheet(f"background-color:{DARK_BG};")
        self.stack = QStackedWidget()
        self.menu_screen = MenuScreen(self)
        self.game_screen = GameScreen(self)
        self.stack.addWidget(self.menu_screen)
        self.stack.addWidget(self.game_screen)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # <<< ده المهم
        layout.addWidget(self.stack)
        self.setLayout(layout)

    def go_to_game(self):
        self.stack.setCurrentWidget(self.game_screen)

    def go_to_menu(self):
        self.stack.setCurrentWidget(self.menu_screen)

# =========================================
# RUN APPLICATION
# =========================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IsolationApp()
    window.show()
    sys.exit(app.exec_())
