from abc import ABC, abstractmethod
from enum import Enum

class ItemStatus(Enum):
    AVAILABLE = "AVAILABLE"
    CHECKED_OUT = "CHECKED_OUT"
    LOST = "LOST"

class LibraryItem(ABC):
    item_types = {}

    def __init_subclass__(cls):
        LibraryItem.item_types[cls.__name__] = cls

    def __init__(self, title, status=ItemStatus.AVAILABLE):
        self.title = title
        if isinstance(status, str):
            status = ItemStatus(status)
        self._status = status

    @property
    def status(self):
        return self._status

    def checkout(self):
        if self._status != ItemStatus.AVAILABLE:
            raise ValueError("Item is not available")
        self._status = ItemStatus.CHECKED_OUT

    def return_item(self):
        if self._status != ItemStatus.CHECKED_OUT:
            raise ValueError("Item was not checked out")
        self._status = ItemStatus.AVAILABLE

    def mark_lost(self):
        if self._status == ItemStatus.LOST:
            raise ValueError("Item is already lost")
        self._status = ItemStatus.LOST

    @property
    @abstractmethod
    def loan_period(self):
        pass

    def __lt__(self, other):
        return self.title.lower() < other.title.lower()

    def __str__(self):
        status = self.status.value.replace("_", " ").title()
        return f"{self.title} ({self.__class__.__name__}) — {status}"

    def __repr__(self):
        return f"{self.__class__.__name__}(title='{self.title}', status='{self.status.value}')"

    @classmethod
    def from_dict(cls, data):
        item_type = data["type"]

        if item_type not in cls.item_types:
            raise ValueError("Unknown item type")

        item_class = cls.item_types[item_type]
        data = data.copy()
        del data["type"]

        return item_class(**data)

    @staticmethod
    def validate_isbn(isbn):
        isbn = isbn.replace("-", "").replace(" ", "")

        if len(isbn) != 13 or not isbn.isdigit():
            return False

        total = 0

        for i in range(13):
            number = int(isbn[i])

            if i % 2 == 0:
                total += number
            else:
                total += number * 3

        return total % 10 == 0


class Book(LibraryItem):
    def __init__(self, title, author, isbn, status=ItemStatus.AVAILABLE):
        super().__init__(title, status)

        if not self.validate_isbn(isbn):
            raise ValueError("Invalid ISBN")

        self.author = author
        self.isbn = isbn

    @property
    def loan_period(self):
        return 21

    def __repr__(self):
        return f"Book(title='{self.title}', author='{self.author}', isbn='{self.isbn}')"


class DVD(LibraryItem):
    def __init__(self, title, director, status=ItemStatus.AVAILABLE):
        super().__init__(title, status)
        self.director = director

    @property
    def loan_period(self):
        return 5

    def __repr__(self):
        return f"DVD(title='{self.title}', director='{self.director}')"


class Magazine(LibraryItem):
    def __init__(self, title, issue, status=ItemStatus.AVAILABLE):
        super().__init__(title, status)
        self.issue = issue

    @property
    def loan_period(self):
        return 14

    def __repr__(self):
        return f"Magazine(title='{self.title}', issue='{self.issue}')"


class Library:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        if not isinstance(item, LibraryItem):
            raise TypeError("This is not a library item")
        self.items.append(item)

    def find_by_title(self, title):
        for item in self.items:
            if item.title.lower() == title.lower():
                return item
        return None

    def checkout(self, title):
        item = self.find_by_title(title)

        if item is None:
            raise ValueError("Item not found")

        item.checkout()

    def return_item(self, title):
        item = self.find_by_title(title)

        if item is None:
            raise ValueError("Item not found")

        item.return_item()

    def mark_lost(self, title):
        item = self.find_by_title(title)

        if item is None:
            raise ValueError("Item not found")

        item.mark_lost()

    def list_available(self):
        available_items = []

        for item in self.items:
            if item.status == ItemStatus.AVAILABLE:
                available_items.append(item)

        return available_items

    def list_all(self):
        return sorted(self.items)


class Database:
    _instance = None

    def __new__(cls, filename="database.txt"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.filename = filename
        return cls._instance

    def parse_line(self, line):
        data = {}
        parts = line.strip().split("|")

        for part in parts:
            if "=" in part:
                key, value = part.split("=", 1)
                data[key] = value

        return data

    def load(self):
        items = []

        try:
            with open(self.filename, "r") as file:
                for line in file:
                    if line.strip():
                        data = self.parse_line(line)
                        item = LibraryItem.from_dict(data)
                        items.append(item)

        except FileNotFoundError:
            print("Database file not found")

        return items

    def save(self, items):
        with open(self.filename, "w") as file:
            for item in items:
                line = f"type={item.__class__.__name__}|title={item.title}"

                if isinstance(item, Book):
                    line += f"|author={item.author}|isbn={item.isbn}"
                elif isinstance(item, DVD):
                    line += f"|director={item.director}"
                elif isinstance(item, Magazine):
                    line += f"|issue={item.issue}"

                line += f"|status={item.status.value}"
                file.write(line + "\n")


db = Database("task_3/databasetest.txt")
library = Library()

items = db.load()

for item in items:
    library.add_item(item)

print("All items:")

for item in library.list_all():
    print(item)

print("\nAvailable items:")

for item in library.list_available():
    print(item)

library.checkout("Dune")

print("\nAfter checkout:")
print(library.find_by_title("Dune"))

library.return_item("Dune")

print("\nAfter return:")
print(library.find_by_title("Dune"))

db.save(library.items)