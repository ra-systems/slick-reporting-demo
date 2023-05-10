from django.db import models

# Create your models here.
from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    slug = models.SlugField(_('Code'), max_length=50, unique=True, db_index=True)
    name = models.CharField(_('Name'), max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.name


class Client(models.Model):
    slug = models.SlugField(_('Code'), max_length=50, unique=True, db_index=True, blank=True)
    name = models.CharField(_('Name'), max_length=255, unique=True, db_index=True)


    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')

    def __str__(self):
        return self.name


class Expense(models.Model):
    slug = models.SlugField(_('Identifier slug'), help_text=_('For fast recall'), max_length=50,
                            unique=True, db_index=True, blank=True)
    name = models.CharField(_('Name'), max_length=255, unique=True, db_index=True)
    notes = models.TextField(_('Notes'), null=True, blank=True)

    class Meta:
        verbose_name = _('Expense')
        verbose_name_plural = _('Expenses')

    def __str__(self):
        return self.name


class ExpenseTransaction(models.Model):
    slug = models.SlugField(_('refer code'), max_length=50, db_index=True, validators=[], blank=True)
    transaction_date = models.DateTimeField(_('date'), db_index=True)
    doc_type = models.CharField(max_length=30, db_index=True)
    notes = models.TextField(_('notes'), null=True, blank=True)
    value = models.DecimalField(_('value'), max_digits=19, decimal_places=2, default=0)

    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Sale')
        verbose_name_plural = _('Sales')


class SalesTransaction(models.Model):
    slug = models.SlugField(_('refer code'), max_length=50, db_index=True, validators=[], blank=True)
    transaction_date = models.DateTimeField(_('date'), db_index=True)
    doc_type = models.CharField(max_length=30, db_index=True)
    notes = models.TextField(_('notes'), null=True, blank=True)
    value = models.DecimalField(_('value'), max_digits=19, decimal_places=2, default=0)

    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Sale')
        verbose_name_plural = _('Sales')


class SalesLineTransaction(models.Model):
    """
    Sales Log
    """
    slug = models.SlugField(_('Code'), max_length=50, db_index=True, validators=[], blank=True)
    transaction_date = models.DateTimeField(_('Date'), db_index=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(_('Quantity'), max_digits=19, decimal_places=2, default=0)
    price = models.DecimalField(_('Price'), max_digits=19, decimal_places=2, default=0)
    value = models.DecimalField(_('Value'), max_digits=19, decimal_places=2, default=0)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.value = self.price * self.quantity
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = _('Sale log')
        verbose_name_plural = _('Sales logs')
