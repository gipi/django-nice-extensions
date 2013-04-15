from django.core.management.base import BaseCommand, CommandError
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType

FLAGS_DICT = {
    ADDITION: "+",
    CHANGE:   "*",
    DELETION: "-",
}

class Command(BaseCommand):
    args="[appname.modelname1] [appname.modelname2] ..."
    help = "Create a summary of the last actions in the admin"""

    def handle(self, *args, **options):
        all_entries = LogEntry.objects.all()
        filtered_entries = all_entries

        for arg in args:
            app_label, model = arg.split(".")

            try:
                content_type = ContentType.objects.get(app_label=app_label, model=model)
            except ContentType.DoesNotExist:
                raise CommandError("the application '%s', doesn't exist" % (arg))

            filtered_entries = all_entries.filter(
                content_type=content_type
            )
            print '%d actions for %s\n---' % (
                len(filtered_entries),
                arg,
            )
            for entry in filtered_entries:
                print FLAGS_DICT[entry.action_flag], str(entry.action_time), entry.object_repr

            print
