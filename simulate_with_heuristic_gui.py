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
