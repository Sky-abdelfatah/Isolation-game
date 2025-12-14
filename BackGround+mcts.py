{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "94536d82-ad3b-46ce-abf3-80cb486072ef",
   "metadata": {},
   "outputs": [],
   "source": [
    "def backpropagate(node, result):\n",
    "    # طول ما لسه في نود (لسه مطلعناش فوق خالص)\n",
    "    while node is not None:\n",
    "        # نزود عدد الزيارات للنود دي\n",
    "        node.visits += 1        \n",
    "        # نزود عدد المكسب/النتيجة حسب نتيجة اللعب\n",
    "        node.wins += result     \n",
    "        # نطلع على الأب بتاع النود دي\n",
    "        node = node.parent\n",
    "def mcts(root, root_turn, iterations=3000):\n",
    "    # نكرر الجوريزم عدد مرات معين (افتراضي 3000 مرة)\n",
    "    for _ in range(iterations):\n",
    "        # نبدأ من الرووت\n",
    "        node = root        \n",
    "        # -------- Selection --------\n",
    "        # طول ما النود متوسعة بالكامل وليها أولاد\n",
    "        while node.is_fully_expanded() and node.children:\n",
    "            # نختار أحسن ابن حسب الـ UCT أو أي معيار معمول\n",
    "            node = node.best_child()\n",
    "        # -------- Expansion --------\n",
    "        # لو النود لسه مش متوسعة بالكامل\n",
    "        if not node.is_fully_expanded():\n",
    "            # نعمل توسيع ونضيف حركة جديدة\n",
    "            node = node.expand()\n",
    "        \n",
    "        # -------- Simulation --------\n",
    "        # نشغل لعبة وهمية من الحالة دي باستخدام heuristic\n",
    "        result = simulate_game_with_heuristic(node.state, root_turn)\n",
    "        \n",
    "        # -------- Backpropagation --------\n",
    "        # نرجع النتيجة لفوق ونحدث الزيارات والمكسب لكل النودز\n",
    "        backpropagate(node, result)   \n",
    "    # -------- اختيار أحسن حركة --------\n",
    "    # لو الرووت ليه أولاد\n",
    "    if root.children:\n",
    "        # نختار الابن اللي اتزار أكتر حاجة\n",
    "        best_child = max(root.children, key=lambda c: c.visits)        \n",
    "        # نرجع الحركة المرتبطة بالابن ده\n",
    "        return best_child.move\n",
    "    # لو مفيش ولا حركة متاحة\n",
    "    return None\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
