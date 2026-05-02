class MurojaatAI:
    def __init__(self):
        # Toifalar va ularga xos kalit so'zlar
        self.categories = {
            "Elektr energiyasi": ["svet", "tok", "elektr", "transformator", "chiroq", "uzilish"],
            "Suv ta'minoti": ["suv", "truba", "quvur", "ichimlik suvi", "kanalizatsiya"],
            "Gaz ta'minoti": ["gaz", "metan", "propan", "bosim", "plitka"],
            "Yo'l qurilishi": ["yo'l", "asfalt", "chuqur", "trotuar", "ko'prik"],
            "Ta'lim": ["maktab", "bog'cha", "darslik", "o'qituvchi", "institut"]
        }

    def predict(self, text: str):
        text = text.lower()
        for category, keywords in self.categories.items():
            if any(word in text for word in keywords):
                return category
        return "Boshqa toifa"
