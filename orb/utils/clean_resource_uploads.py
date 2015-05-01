'''
Script to validate urls
'''
import django
import os
 
from django.conf import settings
from orb.models import ResourceFile



def run(): 
    rootDir = os.path.join(settings.MEDIA_ROOT, 'resource')
    for dirName, subdirList, fileList in os.walk(rootDir):
        relative_dir = dirName.replace(settings.MEDIA_ROOT,'')
        for fname in fileList:
            file_name = '%s/%s' % (relative_dir,fname)
            
            try:
                resource_file = ResourceFile.objects.get(file=file_name)
            except ResourceFile.DoesNotExist:
                print file_name + " not found in database "
                try:
                    os.remove(os.path.join(dirName,fname))
                    print fname + ": DELETED"
                except OSError:
                    print "could not delete: " + fname
            
                print "---"
    return

if __name__ == "__main__":
    django.setup()
    run() 