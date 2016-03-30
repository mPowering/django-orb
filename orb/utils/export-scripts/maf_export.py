
import tablib


def run():

    from orb.models import Tag, Resource

    tag = Tag.objects.get(name='Medical Aid Films')
    resources = Resource.objects.filter(
        resourcetag__tag=tag, status=Resource.APPROVED).order_by('title')
    print resources

    headers = ('Resource Title', 'Tags')
    data = []
    data = tablib.Dataset(*data, headers=headers)

    for resource in resources:

        tags = Tag.objects.filter(
            resourcetag__resource=resource).values_list('name', flat=True)
        data.append(
            (
                resource.title,
                ', '.join(tags)
            )
        )

    with open("/home/alex/temp/maf.xls", 'wb') as f:
        f.write(data.xls)

if __name__ == "__main__":
    import django
    django.setup()
    run()
