
import os
import textract

from django.conf import settings
from mpowering.models import ResourceFile

def run(): 
    files = ResourceFile.objects.filter(file_full_text=None)
    for f in files:
        print os.path.join(settings.MEDIA_ROOT,f.file.name)
        text = textract.process(os.path.join(settings.MEDIA_ROOT,f.file.name))
        f.file_full_text = text
        f.save()
        # this just triggers the search indexing
        f.resource.save()



if __name__ == "__main__":
    import django
    django.setup()
    run()