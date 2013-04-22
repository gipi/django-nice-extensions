from django.core.management.base import BaseCommand, CommandError
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.db.models import get_app, get_models

import datetime
from optparse import make_option


class LogEntryCommand(BaseCommand):
    """This is the class that you could think to subclass in order to
    modify its behaviour.
    """
    option_list = BaseCommand.option_list + (
        make_option('--last-day', action='store_true', default=False, dest='is_daily',
            help='output only the last day logs'),
    )
    args="[appname] [appname.modelname] ..."
    help = "Create a summary of the last actions in the admin"""

    flags_dict = {
        ADDITION: "+",
        CHANGE:   "*",
        DELETION: "-",
    }

    _range = None

    def print_logs_header(self, app_label, modelname, filtered_entries):
        print '%d actions for %s in %s\n---' % (
            len(filtered_entries),
            modelname,
            app_label,
        )

    def print_logs(self, filtered_entries):
        for entry in filtered_entries:
            print self.flags_dict[entry.action_flag], str(entry.action_time), entry.object_repr


    def handle_app_model(self, app_label, modelname):
        try:
            content_type = ContentType.objects.get(app_label=app_label, model=modelname)
        except ContentType.DoesNotExist:
            raise CommandError("the model '%s' in app '%s', doesn't exist" % (app_label, modelname))

        filtered_entries = LogEntry.objects.filter(
            content_type=content_type,
        )
        if self._range:
            filtered_entries = filtered_entries.filter(
                action_time__range=self._range
            )

        self.print_logs_header(app_label, modelname, filtered_entries)
        self.print_logs(filtered_entries)

    def handle(self, *args, **options):
        is_daily = options.get('is_daily')
        if is_daily:
            now = datetime.datetime.now()
            then = now + datetime.timedelta(days=-1)

            self._range = (then, now)

        items = []
        for arg in args:
            # first of all we build up the list of app_label and modelname
            try:
                app_label, modelname = arg.split(".")
                items.append((app_label, modelname,))
            except ValueError:
                app = get_app(arg)
                for model in get_models(app):
                    items.append((arg, model._meta.object_name.lower()))

        # then we use the list for dump the log entries
        for app_label, model in items:
            self.handle_app_model(app_label, model)

            print

class Command(LogEntryCommand):
    pass
