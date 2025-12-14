import threading
from playsound import playsound

def play_sound(file):
    # إنشاء Thread جديد لتشغيل الصوت بدون ما يوقف البرنامج الأساسي
    threading.Thread(
        # الكود اللي هيتنفذ في الـ Thread: تشغيل ملف الصوت
        target=lambda: playsound(file),     
        # daemon=True معناها إن الـ Thread يقف تلقائي لما البرنامج يقفل
        daemon=True
    ).start()  # بدء تشغيل 
