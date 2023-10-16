from dataclasses import dataclass

from managers.entities import Order


@dataclass
class HireOrder(Order):
    duration: int = 1

    def __str__(self):
        return f"Order for {self.duration} weeks with {len(self.line_items)} lines for £{self.total}"
