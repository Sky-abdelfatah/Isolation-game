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