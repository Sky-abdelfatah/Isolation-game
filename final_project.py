import tkinter as tk
from tkinter import messagebox
import threading
from playsound import playsound
import random
import math
import threading
import time

# ---- Config ----
SIZE = 7
CELL = 60  # pixel size
BOARD_COLOR_1 = "#0f1d5e"
BOARD_COLOR_2 = "#ab2d42"
PIECE_A_COLOR = "#ffffff"  # white-like
PIECE_B_COLOR = "#333333"  # black-like

# ---- Game state ----
board = [[0] * SIZE for _ in range(SIZE)]  # 0 empty, 1 blocked
posA = (0, 0)
posB = (SIZE - 1, SIZE - 1)
turn = "A"  # "A" or "B"
mode = "pvp"  # "pvp", "pvai", "aivai"
running = False
ai_thinking = False

# ---- AI difficulty (iterations for Hard only) ----
ai_iterations = 2000  # fixed for Hard

# ---- Helpers ----
def get_moves(position, other_pos, board_state=None):
    # دي دالة بتجيب الحركات المسموح بيها من مكان اللاعب الحالي
    # بتاخد مكان اللاعب (position)، مكان الخصم (other_pos)، وحالة البورد لو موجودة

    b = board_state if board_state is not None else board  
    # لو فيه بورد اتبعت للدالة هنستخدمه، لو لأ هنستخدم البورد الأساسي (global)

    r, c = position  
    # هنا بفك مكان اللاعب لصف (r) وعمود (c) عشان أسهل الحسابات

    moves = []  
    # دي قائمة فاضية هنحط فيها كل الحركات اللي تنفع

    # هنلف على الأربع اتجاهات الأساسية: فوق، تحت، شمال، يمين
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc  
        # بنحسب الصف والعمود الجديدين بعد ما نتحرك خطوة واحدة في الاتجاه ده

        if 0 <= nr < SIZE and 0 <= nc < SIZE:  
            # بنتأكد إن المكان الجديد جوه حدود البورد ومش خارجها

            if b[nr][nc] == 0 and (nr, nc) != other_pos:  
                # بنتأكد إن الخانة فاضية (0 يعني مش محجوزة) وكمان مش مكان الخصم

                moves.append((nr, nc))  
                # لو الشرطين اتحققوا، نضيف الحركة دي للقائمة

    return moves  
    # في الآخر بنرجع كل الحركات اللي تنفع من المكان الحالي

def apply_move(player, newpos):
    # الدالة دي مسؤولة عن تنفيذ الحركة فعليًا على الـ board
    # player: اللاعب اللي بيعمل الحركة ("A" أو "B")
    # newpos: المكان الجديد اللي اللاعب هيروحه (row, column)

    global posA, posB, turn
    # بنستخدم المتغيرات دي كـ global لأننا هنعدل قيمهم
    # posA و posB: أماكن اللاعبين
    # turn: لتغيير الدور بعد الحركة

    if player == "A":
        # لو اللاعب اللي بيلعب هو A

        r, c = posA
        # نخزن المكان القديم للاعب A (الصف والعمود)

        board[r][c] = 1
        # نخلي الخانة القديمة Blocked / مقفولة
        # (يعني اللاعب مش هيقدر يرجع يقف عليها تاني)

        posA = newpos
        # نحدث مكان اللاعب A بالمكان الجديد

        turn = "B"
        # بعد ما A يخلص حركته، الدور ينتقل لـ B

    else:
        # لو اللاعب اللي بيلعب هو B

        r, c = posB
        # نخزن المكان القديم للاعب B

        board[r][c] = 1
        # نقفل الخانة القديمة للاعب B

        posB = newpos
        # نحدث مكان اللاعب B بالمكان الجديد

        turn = "A"
        # بعد ما B يخلص حركته، الدور يرجع لـ A

    redraw()
    # نعيد رسم واجهة اللعبة بعد تنفيذ الحركة
    # عشان التغييرات تظهر للمستخدم
def play_sound(file):
    # إنشاء Thread جديد لتشغيل الصوت بدون ما يوقف البرنامج الأساسي
    threading.Thread(
        # الكود اللي هيتنفذ في الـ Thread: تشغيل ملف الصوت
        target=lambda: playsound(file),     
        # daemon=True معناها إن الـ Thread يقف تلقائي لما البرنامج يقفل
        daemon=True
    ).start()  # بدء تشغيل 
###
def check_terminal_and_show():
    # الدالة دي بتشيّك هل اللعبة خلصت ولا لسه
    # يعني هل اللاعب الحالي معندوش أي حركات ممكنة؟
    # ولو اللعبة خلصت، بتحدد الفايز وتطلع رسالة

    global turn
    # بنستخدم المتغير turn كـ global عشان نعرف مين اللاعب اللي دوره دلوقتي (A أو B)

    cur = posA if turn == "A" else posB
    # cur بيمثل مكان اللاعب الحالي
    # لو الدور على A يبقى cur = posA
    # لو الدور على B يبقى cur = posB

    other = posB if turn == "A" else posA
    # other بيمثل مكان اللاعب التاني
    # بنحتاجه عشان نعرف الحركات المسموح بيها بدون ما نتصادم معاه

    if not get_moves(cur, other):
        # get_moves بترجع كل الحركات المتاحة للاعب الحالي
        # لو رجعت ليست فاضية → مفيش أي حركة ممكنة
        # وده معناه إن اللاعب الحالي خسر

        winner = "B" if turn == "A" else "A"
        # بما إن اللاعب الحالي خسر،
        # يبقى اللاعب التاني هو اللي كسب

        if winner == "A":
            # لو اللاعب A هو الفائز
            play_sound("barca (mp3cut.net).mp3")
            # نشغل صوت احتفال (اختياري حسب اللعبة)

        messagebox.showinfo("Game Over", f"Player {winner} wins!")
        # نطلع Message Box فيها رسالة إن اللعبة انتهت
        # ونوضح مين اللاعب اللي كسب

        return True
        # نرجع True عشان نبلغ باقي البرنامج إن اللعبة خلصت

    return False
    # لو لسه في حركات متاحة، اللعبة مكملة
    # فنرجع False
 
# ---- Heuristic AI ----
def heuristic_move_state(bd, posA_s, posB_s, turn_s):#بياخد البورد ومكان اللاعبين ودور مين دلوقت 
    """Heuristic: maximize distance + own mobility - opponent mobility"""
    current = posA_s if turn_s == "A" else posB_s#اللعاب الي عليه الدور 
    other = posB_s if turn_s == "A" else posA_s#الللاعب الاخر 
    moves = get_moves(current, other, board_state=bd)#التحركات الممكنة لللاعب الي عليه الدور
    if not moves:
        return None#لو مفيش حركات متاحه

    best_move = None#تعريف مبدائي 
    best_score = -1e9#تعريف مبدائي قليل عشان اي سكور تاني يبقا اعلي منه
    for mv in moves:#كل الحركات الممكنه
        # simulate
        tmp = [row[:] for row in bd]#نسخه من البورد الحاليه عشان تحسب الحركه الاحسن  بناء علي الحركات التخيليه 
        tmp[current[0]][current[1]] = 1#تحدد مكان اللعبه القديمه وتعملها بلوك 
        tA = mv if turn_s == "A" else posA_s#بعمل تمب اخزن فيه الموف الحاليه بتاعت A
        tB = mv if turn_s == "B" else posB_s#بعمل تمب اخزن فيه الموف الحاليه بتاعت B

        dist = abs(tA[0] - tB[0]) + abs(tA[1] - tB[1])#المسافه بين اللعبتين بعد الحركه التخيليه
        own = len(get_moves(tA if turn_s == "A" else tB, tB if turn_s == "A" else tA, board_state=tmp))#الحركات المتاحه لللاعب بعد الحركه التخيليه
        opp = len(get_moves(tB if turn_s == "A" else tA, tA if turn_s == "A" else tB, board_state=tmp))#الحركات المتاحه للخصم بعد الحركه التخيليه

#زياده حريه الخصم بتقلل السكور
        score = dist + own * 1.5 - opp * 2.0#ازنق علي خصمي احسن من حريتي 
        #السكور بيتحدد بعاملين المسافه بيني وبين خصمي ومتاح ليا كام حركه مقارنه بالخصم بتاعي 

        if score > best_score:#لو السكور الحالي اعلي من الافضل
            best_score = score#حدث الافضل
            best_move = mv#حدث الموف الافضل
    return best_move#ارجع افضل موف
# ---- MCTS AI ----
class MCTSNode:
    def __init__(self, state, parent=None, move=None):#بناء الروت
        # state: (board, posA, posB, turn)
        self.state = state#الselfدي الاوبجكت 
        self.parent = parent
        self.move = move#اخر حركه اتلعبت
        self.children = []#ليست هنحط فيها كل الابناء
        self.visits = 0#اتزارت كام مره 
        self.wins = 0#بنحسب كام مره فزت لما عديت ع النود دي في تخيلي 

    def is_fully_expanded(self):#هل كل الحركات اتعملت ليها نود
        bd, pA, pB, tr = self.state
        cur = pA if tr == "A" else pB#اللعب الي عليه الدور
        other = pB if tr == "A" else pA#اللاعب الاخر
        moves = get_moves(cur, other, board_state=bd)#الحركات الممكنه لللاعب الي عليه الدور
        return len(self.children) == len(moves)#لو عدد الابناء بيساوي عدد الحركات يبقا مفيش حركات جديده

    def best_child(self, c=1.4):#ال1.4 افضل خيار للعبه دي بناء علي سيرش
        # UCT
        scores = []#احسب السكور لكل ابن
        for ch in self.children:#كل ابن
            if ch.visits == 0:#لو الابن مزارش خالص
                scores.append(float('inf'))#خليه يختار الابن ده
            else:
                scores.append((ch.wins / ch.visits) + c * math.sqrt(2 * math.log(self.visits) / ch.visits))#اول حته اكبليوتيشن بيشوف انهي نسبه فوز اعلي بستغل القيمه الي واثق انها صح,الي بعد كده اكبلوريشن بيطلع بناء علي الي انا حافظه عندي
        return self.children[scores.index(max(scores))]#ارجع الابن الي عنده اعلي سكور

    def expand(self):
        bd, pA, pB, tr = self.state#الحاله الحاليه
        cur = pA if tr == "A" else pB#اللعب الي عليه الدور
        other = pB if tr == "A" else pA#اللاعب الاخر
        moves = get_moves(cur, other, board_state=bd)#الحركات الممكنه لللاعب الي عليه الدور
        used = [c.move for c in self.children]#الحركات الي اتعملت ليها نود
        for mv in moves:#كل الحركات الممكنه
            if mv not in used:#لو الحركه دي مفيش ليها نود
                new_bd = [row[:] for row in bd]#نسخه من البورد الحالي
                new_bd[cur[0]][cur[1]] = 1#اعمل بلوك في مكان اللاعب القديم
                new_pA = mv if tr == "A" else pA#لو الدور علي A اعمل الموف الجديد بتاع A
                new_pB = mv if tr == "B" else pB#لو الدور علي B اعمل الموف الجديد بتاع B
                new_tr = "B" if tr == "A" else "A"#لو الدور علي A اعمل الموف الجديد بتاع B
                child = MCTSNode((new_bd, new_pA, new_pB, new_tr), parent=self, move=mv)#اعمل نود جديده
                self.children.append(child)#ضيف الابن للقائمه
                return child#ارجع الابن الجديد
        return None

def simulate_game_with_heuristic_state(state, root_turn):
    # الدالة دي بتعمل محاكاة للعبة باستخدام heuristic (قاعدة ذكية لاختيار الحركة)
    # بتاخد الحالة الحالية للعبة (state) واللاعب اللي بدأ من الجذر (root_turn)

    bd, pA, pB, tr = state  
    # هنا بفك الحالة (state) لأربع حاجات:
    # bd = البورد (المصفوفة اللي فيها أماكن اللعب)
    # pA = مكان اللاعب A
    # pB = مكان اللاعب B
    # tr = الدور الحالي (مين اللي هيلعب دلوقتي)

    # بعمل نسخة محلية من البورد عشان ما أعدلش في الأصل
    bd = [row[:] for row in bd]
    posA_s = pA   # مكان اللاعب A في المحاكاة
    posB_s = pB   # مكان اللاعب B في المحاكاة
    turn_s = tr   # الدور الحالي في المحاكاة

    while True:  
        # حلقة لا نهائية لحد ما اللعبة تخلص (حد يخسر)

        cur = posA_s if turn_s == "A" else posB_s  
        # لو الدور على A يبقى المكان الحالي هو posA_s
        # لو الدور على B يبقى المكان الحالي هو posB_s

        other = posB_s if turn_s == "A" else posA_s  
        # العكس: ده مكان الخصم اللي لازم أتجنبه

        moves = get_moves(cur, other, board_state=bd)  
        # بجيب كل الحركات المسموح بيها من المكان الحالي

        if not moves:  
            # لو مفيش أي حركة متاحة (اللاعب اتحاصر)
            winner = "B" if turn_s == "A" else "A"  
            # اللي مش دوره هو اللي كسب
            return 1 if winner == root_turn else 0  
            # لو الفائز هو نفس اللاعب اللي بدأ من الجذر → رجع 1
            # لو لأ → رجع 0

        mv = heuristic_move_state(bd, posA_s, posB_s, turn_s)  
        # بجرب أجيب حركة ذكية باستخدام heuristic

        if mv is None:  
            # لو الـ heuristic مش لاقي حركة مناسبة
            mv = random.choice(moves)  
            # اختار حركة عشوائية من الحركات المتاحة

        bd[cur[0]][cur[1]] = 1  
        # بعلم إن المكان اللي كنت واقف فيه اتقفل (اتحجز)

        if turn_s == "A":  
            posA_s = mv   # حدّث مكان اللاعب A
            turn_s = "B"  # الدور يروح لـ B
        else:
            posB_s = mv   # حدّث مكان اللاعب B
            turn_s = "A"  # الدور يروح لـ A

def backpropagate(node, result):
    # طول ما لسه في نود (لسه مطلعناش فوق خالص)
    while node is not None:
        # نزود عدد الزيارات للنود دي
        node.visits += 1
                # نزود عدد المكسب/النتيجة حسب نتيجة اللعب
        node.wins += result        
        # نطلع على الأب بتاع النود دي
        node = node.parent
def mcts(root, root_turn, iterations=3000):
    # نكرر الجوريزم عدد مرات معين (افتراضي 3000 مرة)
    for _ in range(iterations):
        # نبدأ من الرووت
        node = root      
        # -------- Selection --------
        # طول ما النود متوسعة بالكامل وليها أولاد
        while node.is_fully_expanded() and node.children:
            # نختار أحسن ابن حسب الـ UCT أو أي معيار معمول
            node = node.best_child()
       # -------- Expansion --------
        # لو النود لسه مش متوسعة بالكامل
        if not node.is_fully_expanded():
            # نعمل توسيع ونضيف حركة جديدة
            node = node.expand()       
        # -------- Simulation --------
        # نشغل لعبة وهمية من الحالة دي باستخدام heuristic
        result = simulate_game_with_heuristic_state(node.state, root_turn)       
        # -------- Backpropagation --------
        # نرجع النتيجة لفوق ونحدث الزيارات والمكسب لكل النودز
        backpropagate(node, result)   
    # -------- اختيار أحسن حركة --------
    # لو الرووت ليه أولاد
    if root.children:
        # نختار الابن اللي اتزار أكتر حاجة
        best_child = max(root.children, key=lambda c: c.visits)       
        # نرجع الحركة المرتبطة بالابن ده
        return best_child.move    
    # لو مفيش ولا حركة متاحة
    return None

def ai_move(position, board_state, other_pos, turn_player, iterations=800):
    #مكان اللاعب اللي عليه الدور
    #شكل البورد
    # مكان الخصم
    # الدور الحالي على انهي لاعب
    #عدد الاحتمالات

    pA = position if turn_player == "A" else other_pos
    pB = other_pos if turn_player == "A" else position
    #بنحدد اللاعب اللي عليه الدور ونحطه في position ونحط التاني في other pos

    state = ([row[:] for row in board_state], pA, pB, turn_player)
    # بنعمل رسمة تخيلية للبورد علشان الai يجرب عليها الاحتمالات

    root = MCTSNode(state)
    #بنعمل الروت لاجوريزم الmtcs وهى عبارة عن تقنية بتجرب احتمالات كتير لحد ما توصل لافضل احتمال
    #كل نود فيها (حالة اللعبة يعني كأنها رسمة مصغرة لشكل البورد -الحركات moves - الاب والاولاد وعدد الزيارات والانتصارات)

    return mcts(root, turn_player, iterations=iterations)
    #علشان احدد احسن حركة هطبق الجوريزم الmtcs على الجذر وهيعمل محاكاة للعبة 800 مرة علشان يوصل لافضل حركة
# ---- AI Wrapper with levels ----
# ---- AI Wrapper with levels ----
def ai_move_wrapper(player):
    #اللاعب اللي عليه الدور
    global posA, posB, board, ai_iterations
    # مكان اللاعب a
    # مكان اللاعب b
    # شكل البورد
    # عدد الاحتمالات

    position = posA if player == "A" else posB
    other = posB if player == "A" else posA
    #بنحدد اللاعب اللي عليه الدور ونحطه في position ونحط التاني في other pos

    level = level_label.cget("text").split(":")[-1].strip()  # Easy/Medium/Hard
    #هناخد من الlabel كلمة صعب ولا متوسط ولا سهل ونعملها split و strip

    if level == "Easy":
        moves = get_moves(position, other)
        return random.choice(moves) if moves else None
    # لو الليفل سهل هيلعب بشكل عشوائي بالكامل

    elif level == "Medium":
        if random.random() < 0.5:
            moves = get_moves(position, other)
            return random.choice(moves) if moves else None
        else:
            return heuristic_move_state(board, posA, posB, player)
    # 50% من الوقت بيلعب بشكل عشوائي و 50% من الوقت بيلعب ب huristic move

    else:  # Hard
        return ai_move(position, board, other, player, iterations=ai_iterations)
    #بيلعب طول الوقت ب MCTS (Monte Carlo Tree Search) بيجرب الاف من الالعاب الوهمية ويشوف انهي هتناسب اكتر
    # عدد الiteration هو عدد الاحتمالات كل ما زاد كل ما كان اذكى بس ابطأ

# ---- GUI ----
root = tk.Tk()
# بإنشاء نافذة رئيسية جديدة لتطبيق Tkinter (دي أساس الواجهة)

root.title("Isolation Game (MCTS AI)")
# بنحط عنوان للنافذة يظهر في شريط العنوان

main_frame = tk.Frame(root)
# بنعمل إطار (Frame) جوه النافذة علشان ننظم العناصر فيه

main_frame.pack(padx=8, pady=8)
# بنضيف الإطار للنافذة باستخدام pack مع مسافات خارجية (padding) حوالينه

canvas = tk.Canvas(main_frame, width=SIZE*CELL, height=SIZE*CELL, bg="white")
# بنعمل لوحة رسم (Canvas) جوه الإطار، حجمها بيتحسب من حجم الشبكة (SIZE) وحجم الخلية (CELL)، والخلفية أبيض

canvas.grid(row=0, column=0, rowspan=20)
# بنحط الـ Canvas في شبكة (grid) عند الصف 0 والعمود 0، وبتاخد 20 صف لتحت عشان تفضل طويلة جنب عناصر التحكم

controls = tk.Frame(main_frame)
# بنعمل إطار تاني مخصوص لعناصر التحكم (الأزرار والاختيارات)

controls.grid(row=0, column=1, sticky="n", padx=12)
# بنحط إطار التحكم في العمود 1 جنب الـ Canvas، ومثبتينه لأعلى ("n") مع مسافة خارجية في الاتجاه الأفقي

# Mode selection
tk.Label(controls, text="Mode:").pack(anchor="w")
# بنضيف عنوان صغير "Mode:" جوه منطقة التحكم، ومثبتينه ناحية الشمال (left)

mode_var = tk.StringVar(value="pvp")
# متغير نصي هيمثل الوضع المختار، ابتديناه بقيمة "pvp" (لاعب ضد لاعب)

tk.Radiobutton(controls, text="Player vs Player", variable=mode_var, value="pvp").pack(anchor="w")
# زر اختيار للراديو لوضع لاعب ضد لاعب، بيربط القيمة "pvp" بالمتغير mode_var

tk.Radiobutton(controls, text="Player vs AI", variable=mode_var, value="pvai").pack(anchor="w")
# زر اختيار لوضع لاعب ضد ذكاء اصطناعي، القيمة "pvai"

tk.Radiobutton(controls, text="AI vs AI", variable=mode_var, value="aivai").pack(anchor="w")
# زر اختيار لوضع ذكاء اصطناعي ضد ذكاء اصطناعي، القيمة "aivai"

def on_mode_change():
    # دالة بتشتغل لما الوضع يتغير، هدفها تفعيل/تعطيل أزرار الصعوبة حسب الوضع
    sel = mode_var.get()
    # بنقرأ القيمة الحالية للوضع من المتغير mode_var
    if sel == "pvp":
        # لو الوضع لاعب ضد لاعب، مفيش ذكاء اصطناعي، يبقى نوقف أزرار الصعوبة
        btn_easy.config(state="disabled")
        # تعطيل زر السهلة
        btn_medium.config(state="disabled")
        # تعطيل زر المتوسطة
        btn_hard.config(state="disabled")
        # تعطيل زر الصعبة
    else:
        # لو الوضع فيه AI (pvai أو aivai)، نفعل أزرار الصعوبة
        btn_easy.config(state="normal")
        # تفعيل زر السهلة
        btn_medium.config(state="normal")
        # تفعيل زر المتوسطة
        btn_hard.config(state="normal")
        # تفعيل زر الصعبة

mode_var.trace_add("write", lambda *args: on_mode_change())
# بنوصل المتغير mode_var بـ "مراقبة" تغيراته: كل ما يتكتب فيه قيمة جديدة، ننادي on_mode_change

# Difficulty buttons
tk.Label(controls, text="Difficulty:").pack(anchor="w", pady=(8,0))
# عنوان لقسم الصعوبة، بمسافة علوية بسيطة قبل العنوان

def set_easy():
    # دالة تُغير مستوى الصعوبة إلى سهل
    if not running:
        # بنفحص إن اللعبة مش شغالة دلوقتي (عشان ما نغيرش الصعوبة أثناء التشغيل)
        level_label.config(text="Level: Easy")
        # بنحدّث اللابل اللي بيعرض مستوى الصعوبة ليظهر "Easy"

def set_medium():
    if not running:
        level_label.config(text="Level: Medium")
# دي دالة بتغير مستوى الصعوبة لـ Medium
# الشرط بيتأكد إن اللعبة مش شغالة (running = False) قبل ما يغير اللابل

def set_hard():
    if not running:
        level_label.config(text="Level: Hard")
# نفس الفكرة لكن بتغير مستوى الصعوبة لـ Hard

btn_easy = tk.Button(controls, text="Easy", width=12, bg="#0f1d5e", fg="white", command=set_easy)
btn_medium = tk.Button(controls, text="Medium", width=12, bg="#0f1d5e", fg="white", command=set_medium)
btn_hard = tk.Button(controls, text="Hard", width=12, bg="#0f1d5e", fg="white", command=set_hard)
# هنا بنعمل 3 أزرار للصعوبة (Easy, Medium, Hard)
# كل زر مربوط بدالة معينة تغير مستوى الصعوبة
# اللون الخلفي غامق (#0f1d5e) والكتابة بيضا

btn_easy.pack(pady=2)
btn_medium.pack(pady=2)
btn_hard.pack(pady=2)
# بنرتب الأزرار تحت بعض باستخدام pack مع مسافة صغيرة بين كل زر والتاني

level_label = tk.Label(controls, text="Level: Medium", font=("Arial", 10))
level_label.pack(pady=(4,8))
# لابل بيعرض المستوى الحالي، افتراضيًا مكتوب "Medium"
# الخط Arial بحجم 10

def reset_game():
    global board, posA, posB, turn, running, ai_thinking, game_over_shown
    board = [[0]*SIZE for _ in range(SIZE)]
    posA = (0,0)
    posB = (SIZE-1,SIZE-1)
    turn = "A"
    running = False
    ai_thinking = False
    game_over_shown = False  # إعادة تعيين العلم عشان الـ MessageBox ما يظهرش أكتر من مرة
    redraw()
    # دي دالة لإعادة اللعبة من الأول
    # بتصفر البورد، ترجع اللاعبين لمواقع البداية، وتعيد كل الفلاجز لحالتها الأصلية
    # بعدين بتنادي redraw عشان ترسم البورد من جديد

    # إعادة تفعيل أزرار الصعوبة
    btn_easy.config(state="normal")
    btn_medium.config(state="normal")
    btn_hard.config(state="normal")

    # إعادة تفعيل اختيار الـ Mode (الراديو بوتونز)
    for child in controls.winfo_children():
        if isinstance(child, tk.Radiobutton):
            child.config(state="normal")

tk.Button(controls, text="Start", width=12, bg="#0f1d5e", fg="white", command=lambda: start_game()).pack(pady=(8,4))
tk.Button(controls, text="Reset", width=12, bg="#0f1d5e", fg="white", command=reset_game).pack(pady=(0,8))
# زرار Start يبدأ اللعبة (بينادي start_game)
# زرار Reset يعيد اللعبة من الأول (بينادي reset_game)

# Arrow pad
pad = tk.Frame(controls)
pad.pack(pady=6)
# بنعمل إطار صغير للأزرار اللي تتحكم في الاتجاهات (↑ ← → ↓)

btn_up = tk.Button(pad, text="↑", width=4, height=2, bg="#0f1d5e", fg="white", command=lambda: on_arrow("up"))
btn_left = tk.Button(pad, text="←", width=4, height=2, bg="#0f1d5e", fg="white", command=lambda: on_arrow("left"))
btn_right = tk.Button(pad, text="→", width=4, height=2, bg="#0f1d5e", fg="white", command=lambda: on_arrow("right"))
btn_down = tk.Button(pad, text="↓", width=4, height=2, bg="#0f1d5e", fg="white", command=lambda: on_arrow("down"))
# كل زرار هنا بيرمز لاتجاه معين
# لما اللاعب يضغط عليه، بينادي الدالة on_arrow مع الاتجاه المناسب

btn_up.grid(row=0, column=1)
btn_left.grid(row=1, column=0)
btn_right.grid(row=1, column=2)
btn_down.grid(row=2, column=1)
# بنرتب الأزرار في شكل سهم (↑ فوق، ← يسار، → يمين، ↓ تحت)

info_label = tk.Label(controls, text="Turn: A", font=("Arial", 12))
info_label.pack(pady=(8,0))
# لابل بيعرض الدور الحالي (افتراضيًا "Turn: A")
# الخط Arial بحجم 12

# ---- Drawing / Interaction ----
def redraw():
    canvas.delete("all")
    # أول حاجة نمسح كل الرسومات القديمة من الـ Canvas

    for r in range(SIZE):
        for c in range(SIZE):
            # بنلف على كل الصفوف والأعمدة في البورد

            x1 = c*CELL
            y1 = r*CELL
            x2 = x1+CELL
            y2 = y1+CELL
            # بنحسب إحداثيات المستطيل (الخانة) على حسب مكانه وحجم الخلية

            fill = BOARD_COLOR_1 if (r+c)%2==0 else BOARD_COLOR_2
            # بنحدد اللون: لو مجموع الصف+العمود زوجي يبقى اللون الأول، لو فردي يبقى اللون التاني
            # ده بيعمل تأثير "شطرنج" في البورد

            canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="black")
            # نرسم المستطيل بالخلفية والحدود السوداء

            if board[r][c]==1:
                canvas.create_text(x1+CELL/2, y1+CELL/2, text="X", fill="yellow", font=("Arial",20,"bold"))
                # لو الخانة مقفولة (قيمتها 1)، نكتب فيها "X" باللون الأصفر

    draw_piece(posA, PIECE_A_COLOR, "A")
    draw_piece(posB, PIECE_B_COLOR, "B")
    # بعد ما نرسم البورد، نرسم قطع اللاعبين A و B في أماكنهم

    info_label.config(text=f"Turn: {turn}")
    # نحدث اللابل اللي بيعرض الدور الحالي (A أو B)

def draw_piece(pos, color, label):
    r, c = pos
    # نفك مكان القطعة لصف وعمود

    x = c*CELL + CELL/2
    y = r*CELL + CELL/2
    # نحسب مركز الخلية اللي فيها القطعة

    radius = CELL*0.35
    # نصف قطر الدائرة اللي بتمثل القطعة

    canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill=color, outline="black")
    # نرسم دائرة تمثل القطعة باللون المحدد

    canvas.create_text(x, y, text=label, fill="black" if label=="A" else "white", font=("Arial",12,"bold"))
    # نكتب حرف القطعة (A أو B) جوه الدائرة بلون مناسب عشان يبقى واضح

selected = None
# متغير عالمي بيخزن القطعة اللي اللاعب اختارها (لو فيه اختيار)

def on_canvas_click(event):
    global selected
    # نخلي المتغير selected عالمي عشان نقدر نغيره

    c = int(event.x // CELL)
    r = int(event.y // CELL)
    # نحسب الصف والعم

def on_arrow(direction):
    global selected, turn, ai_thinking
    # بنستخدم المتغيرات العامة: القطعة المختارة، الدور الحالي، وحالة الـ AI (بيفكر ولا لأ)

    if ai_thinking: return
    # لو الـ AI شغال بيفكر، نوقف أي حركة من اللاعب لحد ما يخلص

    cur = selected if selected else (posA if turn=="A" else posB)
    # بنحدد مكان القطعة اللي هتتحرك:
    # لو فيه قطعة متحددة (selected) نستخدمها
    # لو لأ، نستخدم مكان اللاعب الحالي حسب الدور (A أو B)

    dr, dc = 0, 0
    # متغيرات لحركة الصف والعمود (delta row, delta col)

    if direction=="up": dr=-1
    elif direction=="down": dr=1
    elif direction=="left": dc=-1
    elif direction=="right": dc=1
    # بنحدد التغيير في الصف أو العمود حسب الاتجاه اللي اتضغط عليه

    nr, nc = cur[0]+dr, cur[1]+dc
    # بنحسب المكان الجديد بعد الحركة

    other = posB if turn=="A" else posA
    # بنجيب مكان الخصم عشان نتأكد إننا مش هنمشي عليه

    if 0<=nr<SIZE and 0<=nc<SIZE and board[nr][nc]==0 and (nr,nc)!=other:
        # شرط: المكان الجديد جوه حدود البورد، فاضي (0)، ومش مكان الخصم

        apply_move(turn,(nr,nc))
        # لو الشرط اتحقق، نطبق الحركة ونحدث البورد

        selected=None
        # نلغي التحديد بعد الحركة

        if check_terminal_and_show(): return
        # لو اللعبة خلصت (حد اتحاصر)، نوقف هنا

        if mode_var.get()=="pvai" and turn=="B":
            root.after(100, lambda: start_ai_move("B"))
        # لو الوضع Player vs AI والدور على B (الذكاء الاصطناعي)،
        # نستنى 100ms وبعدين نخلي الـ AI يبدأ حركته

def start_ai_move(player):
    global ai_thinking
    ai_thinking=True
    # بنقول إن الـ AI دلوقتي بيفكر

    def worker():
        global ai_thinking
        move = ai_move_wrapper(player)
        # بنجيب الحركة اللي الـ AI اختارها

        time.sleep(0.02)
        # تأخير بسيط عشان يبان طبيعي

        if move is None:
            root.after(0, check_terminal_and_show)
            # لو الـ AI مالقاش حركة، نتحقق من نهاية اللعبة
        else:
            root.after(0, lambda m=move, p=player: apply_move(p,m))
            # نطبق الحركة اللي الـ AI اختارها
            root.after(0, check_terminal_and_show)
            # بعد الحركة، نتحقق هل اللعبة خلصت

        ai_thinking=False
        # نرجع نقول إن الـ AI خلص تفكيره

    threading.Thread(target=worker, daemon=True).start()
    # نشغل الـ worker في Thread منفصل عشان ما يوقفش واجهة Tkinter

def start_game():
    global running
    running = True
    # نخلي اللعبة شغالة

    redraw()
    # نرسم البورد من جديد

    btn_easy.config(state="disabled")
    btn_medium.config(state="disabled")
    btn_hard.config(state="disabled")
    # نعطل أزرار الصعوبة بعد بدء اللعبة

    for child in controls.winfo_children():
        if isinstance(child, tk.Radiobutton):
            child.config(state="disabled")
    # نعطل أزرار اختيار الـ Mode (Player vs Player / Player vs AI / AI vs AI)

    sel = mode_var.get()
    if sel == "aivai":
        start_aivai_loop()
    # لو الوضع المختار هو AI ضد AI، نبدأ حلقة الـ AI

# Initial draw
redraw()
# نرسم البورد لأول مرة قبل بدء اللعبة

root.mainloop()
# نشغل الحلقة الرئيسية لتطبيق Tkinter (الواجهة تفضل شغالة وتستقبل أحداث)

