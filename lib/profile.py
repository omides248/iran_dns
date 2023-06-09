from tinydb import TinyDB
from tinydb.table import Document


class Profile:
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

    @property
    def set_dns_1(self):
        try:
            return self.collection.get(doc_id=1).get("set_dns_1", 1)
        except Exception as e:
            return 1

    @property
    def set_dns_2(self):
        try:
            return self.collection.get(doc_id=1).get("set_dns_2", 1)
        except Exception as e:
            return 1

    @classmethod
    def insert(cls, profile_interface_remember=None, interface_option=None, set_dns_1=None, set_dns_2=None):
        profile_dict = {}
        if profile_interface_remember is not None:
            if profile_interface_remember == 0:
                cls.collection.upsert(Document(cls.default_values, doc_id=1))
            else:
                profile_dict["profile_interface_remember"] = profile_interface_remember
                cls.collection.upsert(Document(profile_dict, doc_id=1))

        profile_dict = {}
        profile = cls.collection.get(doc_id=1)
        if profile.get("profile_interface_remember") == 1:
            if profile_interface_remember is not None and profile_interface_remember == 1:
                profile_dict["profile_interface_remember"] = profile_interface_remember

            if interface_option:
                profile_dict["interface_option_menu_choice"] = interface_option

        if set_dns_1 is not None:
            profile_dict["set_dns_1"] = set_dns_1

        if set_dns_2 is not None:
            profile_dict["set_dns_2"] = set_dns_2

        if profile_dict:
            cls.collection.upsert(Document(profile_dict, doc_id=1))

    @classmethod
    def read(cls):
        if cls.collection.get(doc_id=1) is None:
            # Default value
            cls.collection.insert(Document(cls.default_values, doc_id=1))

        return cls.collection.get(doc_id=1) if cls.collection.get(doc_id=1) is not None else {}
