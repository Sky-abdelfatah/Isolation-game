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
