from django.contrib import admin


class ForeignKeyChoicesLimitAdminMixin:
    """


    """
    exclude_fk_fix = ()
    # https://github.com/whoisashish/django-admin-searchable-dropdown
    # https://stackoverflow.com/questions/41880634/django-admin-limit-the-choices-in-dropdown

    # def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
    #     # print(f' FK  {db_field.name}')
    #     if db_field.name not in self.exclude_fk_fix:
    #         kwargs["queryset"] = db_field.model.objects.all()[:50]
    #     #
    #     return super(ForeignKeyChoicesLimitAdminMixin, self).formfield_for_foreignkey(
    #         db_field, request, **kwargs
    #     )

    # https://stackoverflow.com/questions/7134207/django-admin-search-for-foreign-key-objects-rather-than-select
    # autocomplete_fields = ["owner"]
    # def get_autocomplete_fields(self, request):
    #     return set(self.get_autocomplete_fields(self.))
    @property
    def autocomplete_fields(self):
        # <class 'app02_chat_bots.admin.PersonalBotPlaceholderAdmin'>: (admin.E040)
        # TraitAdmin must define "search_fields", because it's referenced by PersonalBotPlaceholderAdmin.autocomplete_fields.
        # если использовать get_autocomplete_fields
        # то ошикби must define "search_fields" не будет
        # и можно долго искать где ошибка.
        return list(self._autocomplete_fields())

    def _autocomplete_fields(self):
        for field in self.model._meta.fields:
            if field.get_internal_type() in [
                'ForeignKey',
                'OneToOneField',
            ]:
                # print(f'autocomplete {self.model} {field} {field.name}')
                yield field.name
            #
        #


class ModelAdmin(ForeignKeyChoicesLimitAdminMixin, admin.ModelAdmin):
    """

    """
