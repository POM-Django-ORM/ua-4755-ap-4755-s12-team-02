from django.db import models


class Order(models.Model):
    book = models.ForeignKey('book.Book', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(
        'authentication.CustomUser', on_delete=models.CASCADE, null=True)
    created_at = models.IntegerField(default=0)
    end_at = models.IntegerField(null=True, default=None)
    plated_end_at = models.IntegerField(default=0)

    def __str__(self):
        return (f'book id: {self.book.id},'
                f'book name: {self.book.name},'
                f'book description: {self.book.description},'
                f'book count: {self.book.count},'
                f'book aauthors: {self.book.authors}')

    def __repr__(self):
        return (f'class: {self.__class__.__name__},'
                f'id: {self.id}')

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
        return Order.objects.all()

    @staticmethod
    def get_not_returned_books():
        return Order.objects.filter(end_at=None)

    @staticmethod
    def delete_by_id(order_id):
        order = Order.get_by_id(order_id)
        if order:
            order.delete()
            return True
        return False
