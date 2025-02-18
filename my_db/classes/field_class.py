class Field:
    def __init__(self, name, field_type, unique = False, nullable = False, default=None, max_size=None, min_size=None, foreign_key=None):
        '''
        foreign_key = (reference_table, reference_column)
        '''
        self.name = name
        self.type = field_type
        self.unique = unique
        self.nullable = nullable
        self.default = default
        self.max_size = max_size if field_type == "str" else None
        self.min_size = min_size if field_type == "str" else None
        self.foreign_key = foreign_key
    
    def to_dict(self):
        field_dict = {
            "name": self.name,
            "type": self.type,
            "unique": self.unique,
            "nullable": self.nullable,
            "default": self.default,
        }
        if self.max_size is not None:
            field_dict["max_size"] = self.max_size
        if self.min_size is not None:
            field_dict["min_size"] = self.min_size
        if self.foreign_key is not None:
            field_dict["foreign_key"] = {"table": self.foreign_key[0], "column": self.foreign_key[1]}
        return field_dict