def copy_data(apps, schema_editor, app_name, metas):
    LookupTableItem = apps.get_model('lookup_tables', 'LookupTableItem')
    for meta in metas:
        Model = apps.get_model(app_name, meta[1])
        lookup_table_app = app_name
        lookup_table = meta[2].split('.')
        if len(lookup_table) > 1:
            lookup_table_app, lookup_table_name = lookup_table
        else:
            lookup_table_app, lookup_table_name = app_name, lookup_table[0]
        LookupTable = apps.get_model(lookup_table_app, lookup_table_name)
        for value_old in LookupTableItem.objects.filter(table__table_ref=meta[0]):
            value_new, created = LookupTable.objects.get_or_create(name=value_old.name)
            if created:
                value_new.sort_order = value_old.sort_order
            for field_name_old in meta[3].split(','):
                field_name_new = '{0}_new'.format(field_name_old)
                update = {field_name_old: value_old}
                for entity in Model.objects.filter(**update):
                    setattr(entity, field_name_new, value_new)
                    entity.save()


def delete_data(apps, schema_editor, metas):
    LookupTable = apps.get_model('lookup_tables', 'LookupTable')
    for meta in metas:
        table = LookupTable.objects.filter(table_ref=meta[0]).first()
        if table:
            for item in table.lookuptableitem_set.all():
                item.delete()
            table.delete()
