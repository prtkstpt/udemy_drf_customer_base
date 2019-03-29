from django.contrib import admin
from .models import (Document, Customer,
                    Profession, DataSheet
                    )

# Register your models here.

admin.site.register(Document)
admin.site.register(Customer)
admin.site.register(Profession)
admin.site.register(DataSheet)