def mcts(root, root_turn, iterations=3000):
    for _ in range(iterations):  # بلف عدد معين من المرات (iterations) عشان أعمل محاكاة كتير
        node = root  # ببدأ من النود الأساسي (الجذر)
        # Selection
        while node.is_fully_expanded() and node.children:  
            # طول ما النود اتوسع بالكامل ولسه عنده أطفال
            node = node.best_child()  # باختار أفضل طفل بناءً على UCT

        # Expansion
        if not node.is_fully_expanded():  
            # لو النود لسه فيه حركات ما اتوسعتش
            node = node.expand()  # أوسع النود وأضيف طفل جديد

        # Simulation
        result = simulate_game_with_heuristic(node.state, root_turn)  
        # بعمل محاكاة للعبة من الحالة دي باستخدام heuristic عشان أجيب نتيجة (مين كسب)

        # Backpropagation
        backpropagate(node, result)  
        # برجّع النتيجة دي للأب والأجداد (بحدث عدد الزيارات والمكاسب)

    # Return the best move
    if root.children:  # لو فيه children اتعملوا من الجذر
        best_child = max(root.children, key=lambda c: c.visits)  
        # باختار الchild اللي اتزور أكتر (أكتر تجربة)
        return best_child.move  # وأرجع الحركة اللي وصلتنا له
    return None  # لو مفيش children يبقى مفيش حركة

