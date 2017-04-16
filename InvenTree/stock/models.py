from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.db import models
from django.core.validators import MinValueValidator

from supplier.models import SupplierPart
from part.models import Part
from InvenTree.models import InvenTreeTree


class StockLocation(InvenTreeTree):
    """ Organization tree for StockItem objects
    """

    @property
    def items(self):
        stock_list = self.stockitem_set.all()
        return stock_list


class StockItem(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='locations')
    supplier_part = models.ForeignKey(SupplierPart, blank=True, null=True, on_delete=models.SET_NULL)
    location = models.ForeignKey(StockLocation, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    updated = models.DateField(auto_now=True)

    # last time the stock was checked / counted
    last_checked = models.DateField(blank=True, null=True)

    review_needed = models.BooleanField(default=False)

    # Stock status types
    ITEM_IN_STOCK = 10
    ITEM_INCOMING = 15
    ITEM_IN_PROGRESS = 20
    ITEM_COMPLETE = 25
    ITEM_ATTENTION = 50
    ITEM_DAMAGED = 55
    ITEM_DESTROYED = 60

    ITEM_STATUS_CODES = {
        ITEM_IN_STOCK: _("In stock"),
        ITEM_INCOMING: _("Incoming"),
        ITEM_IN_PROGRESS: _("In progress"),
        ITEM_COMPLETE: _("Complete"),
        ITEM_ATTENTION: _("Attention needed"),
        ITEM_DAMAGED: _("Damaged"),
        ITEM_DESTROYED: _("Destroyed")
    }

    status = models.PositiveIntegerField(
        default=ITEM_IN_STOCK,
        choices=ITEM_STATUS_CODES.items(),
        validators=[MinValueValidator(0)])

    notes = models.CharField(max_length=100, blank=True)

    # If stock item is incoming, an (optional) ETA field
    expected_arrival = models.DateField(null=True, blank=True)

    def __str__(self):
        return "{n} x {part} @ {loc}".format(
            n=self.quantity,
            part=self.part.name,
            loc=self.location.name)


class StockTracking(models.Model):
    """ Tracks a single movement of stock
    - Used to track stock being taken from a location
    - Used to track stock being added to a location
    - "Pending" flag shows that stock WILL be taken / added
    """

    item = models.ForeignKey(StockItem, on_delete=models.CASCADE, related_name='tracking')
    quantity = models.IntegerField()
    when = models.DateTimeField(auto_now=True)
