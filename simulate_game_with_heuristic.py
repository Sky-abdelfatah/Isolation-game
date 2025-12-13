def simulate_game_with_heuristic(state, root_turn):
    # تعريف دالة اسمها simulate_game_with_heuristic
    # state: حالة اللعبة (اللوحة + أماكن اللاعبين + الدور الحالي)
    # root_turn: اللاعب اللي بنقيّم النتيجة من وجهة نظره (A أو B). غالبا A

    board, posA, posB, turn = state
    # turn: مين دوره يلعب الآن ("A" أو "B")

    while True:
        # حلقة لا نهائية… اللعبة هتستمر لحد ما حد يخسر

        current_pos = posA if turn == "A" else posB
        # current_pos = موقع اللاعب اللي دوره يلعب الآن

        other_pos = posB if turn == "A" else posA
        # other_pos = موقع اللاعب الآخر (الخصم)

        moves = get_moves(current_pos, board, other_pos)
        # بنحسب كل الحركات المتاحة للاعب الحالي بناءً على مكانه الحالي وحالة اللوحة ومكان الخصم

        if not moves:
            # لو مفيش أي حركة متاحة…

            winner = "B" if turn == "A" else "A"
            # يبقى اللاعب اللي مش دوره هو اللي كسب

            return 1 if winner == root_turn else 0
            # 1 لو اللاعب اللي كسب هو نفس اللاعب اللي بنقيّم من وجهة نظره (غالبا A)

        # Use heuristic to choose move
        move = heuristic_move(board, posA, posB, turn)
        # بنستخدم دالة heuristic_move علشان تختار أفضل حركة بناءً على heuristic معين

        if move is None:
            # لو الـ heuristic مقدرش يختار حركة…

            move = random.choice(moves)
            # نختار حركة عشوائية من الحركات المتاحة

        board = [row[:] for row in board]
        # بنعمل نسخة جديدة من اللوحة (deep copy بسيط) علشان ما نعدّلش في النسخة الأصلية
        # يمنع تعديل اللوحة الأصلية، يسمح لكل محاكاة تبدأ من نفس الحالة،
        # يمنع تداخل المحاكاة مع بعضها، يحافظ على صحة الـ MCTS، ويحافظ على صحة اللعبة نفسها

        board[current_pos[0]][current_pos[1]] = BLOCK
        # بنحوّل مكان اللاعب الحالي إلى BLOCK لأنه بعد ما يتحرك، المكان القديم بيتقفل

        if turn == "A":
            posA = move
            turn = "B"
            # لو الدور كان على A:
            # نحدّث مكانه إلى الحركة الجديدة
            # نغيّر الدور إلى B
        else:
            posB = move
            turn = "A"
            # لو الدور كان على B:
            # نحدّث مكانه
            # نرجّع الدور لـ A
