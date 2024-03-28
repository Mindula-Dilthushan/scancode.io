# Generated by Django 5.0.2 on 2024-03-01 16:09

from django.db import migrations, models
from django.db.models import Q


def update_package_datasource_ids(apps, schema_editor):
    """
    Compute DiscoveredPackage `datasource_ids` from the previously
    present `datasource_id` field.
    """
    DiscoveredPackage = apps.get_model("scanpipe", "DiscoveredPackage")
    queryset = DiscoveredPackage.objects.filter(~Q(datasource_id=""))

    object_count = queryset.count()
    print(f"\nCompute datasource_ids for {object_count:,} packages.")

    chunk_size = 2000
    iterator = queryset.iterator(chunk_size=chunk_size)

    unsaved_objects = []
    for index, package in enumerate(iterator, start=1):
        datasource_id = package.datasource_id
        package.datasource_ids = [datasource_id]
        unsaved_objects.append(package)

        if not (index % chunk_size) and unsaved_objects:
            print(f"  {index:,} / {object_count:,} computed")

    print("Updating DB objects...")
    DiscoveredPackage.objects.bulk_update(
        objs=unsaved_objects,
        fields=["datasource_ids"],
        batch_size=1000,
    )


class Migration(migrations.Migration):

    dependencies = [
        ("scanpipe", "0054_rename_pipeline"),
    ]

    operations = [
        migrations.AddField(
            model_name="discoveredpackage",
            name="datasource_ids",
            field=models.JSONField(
                blank=True,
                default=list,
                help_text="The identifiers for the datafile handlers used to obtain this package.",
            ),
        ),
        migrations.RunPython(
            update_package_datasource_ids,
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.RemoveField(
            model_name='discoveredpackage',
            name='datasource_id',
        ),
        migrations.AddField(
            model_name="discoveredpackage",
            name="datafile_paths",
            field=models.JSONField(
                blank=True,
                default=list,
                help_text="A list of Resource paths for package datafiles which were used to assemble this pacakage.",
            ),
        ),   
    ]