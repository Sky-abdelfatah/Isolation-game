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
        result = simulate_game_with_heuristic(node.state, root_turn)       
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
