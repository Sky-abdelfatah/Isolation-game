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