import os.path
from tinydb import TinyDB
from tinydb.table import Document


class Profile:
    # from iran_dns import Windows
    # file = os.path.join(Windows.root_directory, "iran_dns.json")
    file = "./iran_dns.json"
    collection = TinyDB(file).table("profile")
    default_values = {"profile_interface_remember": 0,
                      "interface_option_menu_choice": "Select Your Internet"}

    @property
    def profile_interface_remember(self):
        try:
            return self.collection.get(doc_id=1).get("profile_interface_remember", 0)
        except Exception as e:
            return 0

    @property
    def interface_name(self):
        try:
            return self.collection.get(doc_id=1).get("interface_option_menu_choice", "Select Your Internet")
        except Exception as e:
            return "Select Your Internet"

    @classmethod
    def insert(cls, profile_interface_remember=None, interface_option=None):
        print("DB location:", cls.file)
        print("insert", profile_interface_remember, ",", interface_option)
        profile_dict = {}
        if profile_interface_remember is not None:
            if profile_interface_remember == 0:
                cls.collection.upsert(Document(cls.default_values, doc_id=1))
                print(11111)
            else:
                profile_dict["profile_interface_remember"] = profile_interface_remember
                cls.collection.upsert(Document(profile_dict, doc_id=1))
                print(2222)

        profile_dict = {}
        profile = cls.collection.get(doc_id=1)
        if profile.get("profile_interface_remember") == 1:
            print(3333)
            if profile_interface_remember is not None and profile_interface_remember == 1:
                print(4444)
                profile_dict["profile_interface_remember"] = profile_interface_remember

            if interface_option:
                print(55555)
                profile_dict["interface_option_menu_choice"] = interface_option

        if profile_dict:
            print(66666, profile_dict)
            cls.collection.upsert(Document(profile_dict, doc_id=1))

        print("inserted", profile_interface_remember, ",", interface_option, ",", cls.collection.get(doc_id=1))
        print("----------------------")

    @classmethod
    def read(cls):
        if cls.collection.get(doc_id=1) is None:
            # Default value
            cls.collection.insert(Document(cls.default_values, doc_id=1))

        return cls.collection.get(doc_id=1) if cls.collection.get(doc_id=1) is not None else {}
