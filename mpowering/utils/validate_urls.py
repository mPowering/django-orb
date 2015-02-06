

from mpowering.models import ResourceURL


def run(): 
    urls = Resource.objects.all().value_list(url)
    for u in urls:
        print u



if __name__ == "__main__":
    run() 