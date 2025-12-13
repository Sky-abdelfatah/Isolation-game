<<<<<<< HEAD
def ai_move(position, board, other_pos, turn):
    #مكان الai في اللعبة
    #شكل البورد وايه المربعات الملغية وايه متاح
    #الخصم مكانه فين
    #الدور الحالي

    """ MCTS AI with heuristic simulation """
    # Create root state
    posA = position if turn == "A" else other_pos
    posB = other_pos if turn == "A" else position
    state = ([row[:] for row in board], posA, posB, turn)
    #بنعمل رسمة تخيلية للبورد علشان الai يجرب عليها الاحتمالات
    root = MCTSNode(state)
    #بنعمل الروت لاجوريزم الmtcs وهى عبارة عن تقنية بتجرب احتمالات كتير لحد ما توصل لافضل احتمال
    #كل نود فيها (حالة اللعبة يعني كأنها رسمة مصغرة لشكل البورد -الحركات moves - الاب والاولاد وعدد الزيارات والانتصارات)
    best_move = mcts(root, turn, iterations=3000)
    #علشان احدد احسن حركة هطبق الجوريزم الmtcs على الجذر وهيعمل محاكاة للعبة 3000 مرة علشان يوصل لافضل حركة
    return best_move
=======
def ai_move(position, board, other_pos, turn):
    #مكان الai في اللعبة
    #شكل البورد وايه المربعات الملغية وايه متاح
    #الخصم مكانه فين
    #الدور الحالي

    """ MCTS AI with heuristic simulation """
    # Create root state
    posA = position if turn == "A" else other_pos
    posB = other_pos if turn == "A" else position
    state = ([row[:] for row in board], posA, posB, turn)
    #بنعمل رسمة تخيلية للبورد علشان الai يجرب عليها الاحتمالات
    root = MCTSNode(state)
    #بنعمل الروت لاجوريزم الmtcs وهى عبارة عن تقنية بتجرب احتمالات كتير لحد ما توصل لافضل احتمال
    #كل نود فيها (حالة اللعبة يعني كأنها رسمة مصغرة لشكل البورد -الحركات moves - الاب والاولاد وعدد الزيارات والانتصارات)
    best_move = mcts(root, turn, iterations=3000)
    #علشان احدد احسن حركة هطبق الجوريزم الmtcs على الجذر وهيعمل محاكاة للعبة 3000 مرة علشان يوصل لافضل حركة
    return best_move
>>>>>>> 978c7833a4b98c4b45f94f6dd4b3ee16f699f867
    #افضل حركة الai وصلها بعد حلل كل الاحتمالات