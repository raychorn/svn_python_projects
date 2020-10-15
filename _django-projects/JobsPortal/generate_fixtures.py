from django.core.management.base import BaseCommand, CommandError
from django.core import serializers

from optparse import make_option

class Command(BaseCommand):   
    """ 
        Generate a fixture file for a specific model.
        Useage: ./manage.py generate_fixtures app.models.MyModel --file=MyModelsOutputFile.json                                                                                              
    """
    option_list = BaseCommand.option_list + ( 
        make_option('--file',
                    action='store',
                    dest='file',
                    default=None,
                    help='Sets the file to store the fixture in'),
    )   
    def handle(self, *args, **options):
        app = '.'.join(args[0].split('.')[:-1])
        model_str = args[0].split('.')[-1]

        models = __import__(app, globals(), locals(), [model_str], -1) 
        model = getattr(models, model_str)

        if not options['file']:
            output_file = model_str + '.json'
        else:
            output_file = options['file'] 

        data = serializers.serialize("json", indent=4, model.objects.all())
        out = open(output_file, "w")
        out.write(data)
        out.close()

        print "Wrote file `{0}` for model `{1}.{2}`.".format(output_file, app, model_str)