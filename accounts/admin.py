from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import User

# Register your models here.


class CustomLibrarianAdmin(UserAdmin):
    # Campos de Leitura
    readonly_fields = ("date_joined", "last_login", "updated_at")

    # Campos na edição de informações do usuario
    fieldsets = (
        ("Credentials", {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("bio", "birthdate")}),
        (
            "Permissions",
            {"fields": ("is_superuser", "is_active", "is_critic")},
        ),
        (
            "Important Dates",
            {"fields": ("date_joined", "last_login", "updated_at")},
        ),
    )

    # Colunas da tabela de filtro
    list_display = ("username", "is_superuser", "is_critic")


admin.site.register(User, CustomLibrarianAdmin)
