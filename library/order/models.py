from django.db import models


class Order(models.Model):
    book = models.ForeignKey('book.Book', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(
        'authentication.CustomUser', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    end_at = models.DateTimeField(null=True, default=None)
    plated_end_at = models.DateTimeField(null=True, default=None)

    def __str__(self):
        end_at_str = f"'{self.end_at}'" if self.end_at is not None else "None"
        return (f"'id': {self.id}, 'user': {repr(self.user)}, 'book': {repr(self.book)}, "
                f"'created_at': '{self.created_at}', 'end_at': {end_at_str}, "
                f"'plated_end_at': '{self.plated_end_at}'")

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id})'

    def to_dict(self):
        return {'id': self.id,
                'book': self.book.id,
                'user': self.user.id,
                'created_at': self.created_at,
                'end_at': self.end_at,
                'plated_end_at': self.plated_end_at
                }

    @staticmethod
    def create(user, book, plated_end_at):
        # Check if user is saved
        if user.id is None:
            return None
        
        # Check if book has available copies (not all copies are currently checked out)
        active_orders = Order.objects.filter(book=book, end_at=None).count()
        if active_orders >= book.count:
            return None
        
        order = Order.objects.create(
            user=user,
            book=book,
            plated_end_at=plated_end_at
        )
        return order

    @staticmethod
    def get_by_id(order_id):
        try:
            return Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return None

    def update(self, plated_end_at=None, end_at=None):
        if plated_end_at is not None:
            self.plated_end_at = plated_end_at
        if end_at is not None:
            self.end_at = end_at
        self.save()

    @staticmethod
    def get_all():
        return list(Order.objects.all())

    @staticmethod
    def get_not_returned_books():
        return list(Order.objects.filter(end_at=None))

    @staticmethod
    def delete_by_id(order_id):
        order = Order.get_by_id(order_id)
        if order:
            order.delete()
            return True
        return False
