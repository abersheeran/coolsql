class Field:
    def __init__(self, field_name: str) -> None:
        if "'" in field_name or '"' in field_name:
            raise ValueError("Field name cannot contain quotes")

        self.field_name = field_name

    def __format__(self, __format_spec: str) -> str:
        return f'"{self.field_name}"'  # Use double quotes for field names in SQL
