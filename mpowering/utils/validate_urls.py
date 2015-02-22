
import urllib2 
from mpowering.models import ResourceURL


def run(): 
    urls = ResourceURL.objects.all()
    for u in urls:
        response = urllib2.urlopen(u.url)
        if response.getcode() is not 200:
            print u.url



if __name__ == "__main__":
    run() 
    
    
    


