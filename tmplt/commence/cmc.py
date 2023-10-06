import win32com.client




class Table:
    def __init__(self, name, fields, conv):
        self.name = name
        self.fields:list = self.get_all_fields()

    def get_all_fields(self, conv, table):
        fields = conv.Request(f"[GetFieldNames({table}, ;)]")
        field_list = fields.split(';')
        return field_list

class Record:
    ...


class CmcField:
    ...



class Commence:
    def __init__(self, tables: list):
        self.conv = self.get_conversation()
        self.tables = [self.get_table(t) for t in tables]


    def get_conversation(self):
        cmc = win32com.client.Dispatch("Commence.DB")
        conv = cmc.GetConversation("Commence", "GetData")
        return conv

    def get_table(self, table):
        return self.conv.Request(f"[ViewCategory({table})]")


def go(table_names):
    ...
