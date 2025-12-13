<<<<<<< HEAD
def human_move(player_name, position, board, other_pos):
    # انهي بلاير a ولا b
    # المكان اللي واقف فيه حاليا
    # شكل البورد ايه المربعات المتاحة وايه اتلغى
    # موقع اللاعب التاني

    moves = get_moves(position, board, other_pos)
    # بجيب كل الحركات اللي اللاعب يقدر يتحركها

    if not moves:
        return None  # no moves (loss)
    # لو مفيش حركة متاحة اللاعب يخسر

    print(f"{player_name}, your possible moves (using arrows):")

    # mapping direction to arrow
    direction_map = {
        (-1, 0): "↑",
        (1, 0): "↓",
        (0, -1): "←",
        (0, 1): "→"
    }
    # نحسب الفرق بين المكان الحالي والمكان الجديد (من الاماكن المتاحة) وبعدين نحول الفرق ده لاسهم للتسهيل

    arrows = []
    # نعمل ليست فاضية هيتحط فيها بعدين الاسهم اللي اللاعب يقدر يتحركهم

    r, c = position
    # بيفك مكان اللاعب الى row و column
    # علشان نستخدم r و c بسهولة بعدين بدل pos[0] و pos[1]

    for move in moves:
        # moves  قائمة فيها كل الاماكن اللي اللاعب يقدر يتحركها
        # r,c مكان اللاعب الحالي

        mr, mc = move
        # mr الصف الجديد
        # mc العمود الجديد

        dr = mr - r
        # بيحسب اتجاه الحركة الجديدة (من الحركات المتاحة )

        dc = mc - c
        # نفس الكلام للعمود بدل الصف

        arrow = direction_map.get((dr, dc), "?")
        # direction map جدول التحويل من حركة لسهم
        arrows.append(arrow)
        # بحط السهم في الليست اللي هتظهر للاعب

    print("Your options:")

    options = []
    # ليست بحط فيها كل الاوبشنات اللي اللاعب يقدر يتحرك فيها

    for i, move in enumerate(moves):
        # بنعمل لوب على كل الحركات الممكنة- موف بتظهر الاحداثيات بتاعت الحركات والi بتعد رقم الحركة
        mr, mc = move
        # بنفصل الصف والعمود
        dr = mr - r
        # نفس الكلام بنحسب اتجاه الحركة الجديدة للصف
        dc = mc - c
        # نفس الكلام بنحسب اتجاه الحركة للعمود
        arrow = direction_map.get((dr, dc), "?")
        # بنحول الحركة من حركة لسهم لو ملقاش حركة من الاربعة يحط "؟"
        print(f"{i + 1}) {arrow}")
        # بطبع رقم الحركة وجنبها السهم

        options.append(move)
        # خزن احداثيات الحركة في قائمة اوبشنز علشان تظهر للاعب

    choice = input("Choose option number: ").strip()  # بيشيل المسافات والزوايد

    if not choice.isdigit() or not (1 <= int(choice) <= len(options)):
        # choice.isdigit بتشيك إذا النص اللي دخله اللاعب كله أرقام فقط (يعني مش حروف أو رموز)
        # int(choice) حولنا النص اللي دخله اللاعب لرقم عشان نقدر نقارنه
        # (1 <= int(choice) <= len(options))  بتشيك إذا الرقم اللي دخله اللاعب موجود ضمن خياراته (مثلاً لو عنده 3 خيارات، لازم الرقم يكون 1، 2 أو 3)
        # not ... or not ...  لو أي شرط من دول مش متحقق، يبقى الاختيار غير صحيح
        print("Invalid choice! Try again.")
        return human_move(player_name, position, board, other_pos)

    return options[int(choice) - 1]
    # بعد ما اللاعب يختار حركة نعرضله الاوبشنات المتاحة من قائمة اوبشنز
=======
def human_move(player_name, position, board, other_pos):
    # انهي بلاير a ولا b
    # المكان اللي واقف فيه حاليا
    # شكل البورد ايه المربعات المتاحة وايه اتلغى
    # موقع اللاعب التاني

    moves = get_moves(position, board, other_pos)
    # بجيب كل الحركات اللي اللاعب يقدر يتحركها

    if not moves:
        return None  # no moves (loss)
    # لو مفيش حركة متاحة اللاعب يخسر

    print(f"{player_name}, your possible moves (using arrows):")

    # mapping direction to arrow
    direction_map = {
        (-1, 0): "↑",
        (1, 0): "↓",
        (0, -1): "←",
        (0, 1): "→"
    }
    # نحسب الفرق بين المكان الحالي والمكان الجديد (من الاماكن المتاحة) وبعدين نحول الفرق ده لاسهم للتسهيل

    arrows = []
    # نعمل ليست فاضية هيتحط فيها بعدين الاسهم اللي اللاعب يقدر يتحركهم

    r, c = position
    # بيفك مكان اللاعب الى row و column
    # علشان نستخدم r و c بسهولة بعدين بدل pos[0] و pos[1]

    for move in moves:
        # moves  قائمة فيها كل الاماكن اللي اللاعب يقدر يتحركها
        # r,c مكان اللاعب الحالي

        mr, mc = move
        # mr الصف الجديد
        # mc العمود الجديد

        dr = mr - r
        # بيحسب اتجاه الحركة الجديدة (من الحركات المتاحة )

        dc = mc - c
        # نفس الكلام للعمود بدل الصف

        arrow = direction_map.get((dr, dc), "?")
        # direction map جدول التحويل من حركة لسهم
        arrows.append(arrow)
        # بحط السهم في الليست اللي هتظهر للاعب

    print("Your options:")

    options = []
    # ليست بحط فيها كل الاوبشنات اللي اللاعب يقدر يتحرك فيها

    for i, move in enumerate(moves):
        # بنعمل لوب على كل الحركات الممكنة- موف بتظهر الاحداثيات بتاعت الحركات والi بتعد رقم الحركة
        mr, mc = move
        # بنفصل الصف والعمود
        dr = mr - r
        # نفس الكلام بنحسب اتجاه الحركة الجديدة للصف
        dc = mc - c
        # نفس الكلام بنحسب اتجاه الحركة للعمود
        arrow = direction_map.get((dr, dc), "?")
        # بنحول الحركة من حركة لسهم لو ملقاش حركة من الاربعة يحط "؟"
        print(f"{i + 1}) {arrow}")
        # بطبع رقم الحركة وجنبها السهم

        options.append(move)
        # خزن احداثيات الحركة في قائمة اوبشنز علشان تظهر للاعب

    choice = input("Choose option number: ").strip()  # بيشيل المسافات والزوايد

    if not choice.isdigit() or not (1 <= int(choice) <= len(options)):
        # choice.isdigit بتشيك إذا النص اللي دخله اللاعب كله أرقام فقط (يعني مش حروف أو رموز)
        # int(choice) حولنا النص اللي دخله اللاعب لرقم عشان نقدر نقارنه
        # (1 <= int(choice) <= len(options))  بتشيك إذا الرقم اللي دخله اللاعب موجود ضمن خياراته (مثلاً لو عنده 3 خيارات، لازم الرقم يكون 1، 2 أو 3)
        # not ... or not ...  لو أي شرط من دول مش متحقق، يبقى الاختيار غير صحيح
        print("Invalid choice! Try again.")
        return human_move(player_name, position, board, other_pos)

    return options[int(choice) - 1]
    # بعد ما اللاعب يختار حركة نعرضله الاوبشنات المتاحة من قائمة اوبشنز
>>>>>>> 978c7833a4b98c4b45f94f6dd4b3ee16f699f867
    # نستخدم int(choice)-1 لأن القوائم في بايثون تبدأ من 0 لكن احنا عرضنا للاعب الأرقام من 1