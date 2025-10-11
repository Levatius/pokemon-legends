from python_scripts.models import TTSObject

class Deck(TTSObject):
    def __init__(self, deck_id: int):
        self.id = deck_id
        self.face_url = input(f"Enter the cloud URL for the FACE image of deck {self.id}:\n")
        self.back_url = input(f"Enter the cloud URL for the BACK image of deck {self.id}:\n")

    def get_json(self):
        return {
            "FaceURL": self.face_url,
            "BackURL": self.back_url,
            "NumWidth": 10,
            "NumHeight": 7,
            "BackIsHidden": True,
            "UniqueBack": True,
            "Type": 0
        }