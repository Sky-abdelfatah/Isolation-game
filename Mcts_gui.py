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