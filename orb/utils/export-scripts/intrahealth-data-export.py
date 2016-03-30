
import tablib


def run():

    from orb.models import Tag, Resource

    HEALTH_DOMAIN = 'Nutrition'

    tag = Tag.objects.get(name=HEALTH_DOMAIN)
    resources = Resource.objects.filter(
        resourcetag__tag=tag, status=Resource.APPROVED).order_by('title')

    headers = ('Resource Title', 'Resource Link', 'Health Domain(s)', 'Date Published on ORB',
               'Language(s)', 'Audience', 'Length', 'Resource Type', 'Target Device(s)')
    data = []
    data = tablib.Dataset(*data, headers=headers)

    for resource in resources:

        domains = Tag.objects.filter(
            resourcetag__resource=resource, category__slug='health-domain').values_list('name', flat=True)
        langs = Tag.objects.filter(resourcetag__resource=resource,
                                   category__slug='language').values_list('name', flat=True)
        audience = Tag.objects.filter(
            resourcetag__resource=resource, category__slug='audience').values_list('name', flat=True)
        length = ""
        if resource.study_time_number:
            length = str(resource.study_time_number) + \
                " " + resource.study_time_unit

        types = Tag.objects.filter(
            resourcetag__resource=resource, category__slug='type').values_list('name', flat=True)
        devices = Tag.objects.filter(
            resourcetag__resource=resource, category__slug='device').values_list('name', flat=True)

        data.append(
            (
                resource.title,
                'http://health-orb.org/resource/view/' + resource.slug,
                ', '.join(domains),
                resource.create_date.strftime("%Y-%b-%d"),
                ', '.join(langs),
                ', '.join(audience),
                length,
                ', '.join(types),
                ', '.join(devices)
            )
        )

    with open("/home/alex/temp/intrahealth-fp.xls", 'wb') as f:
        f.write(data.xls)

if __name__ == "__main__":
    import django
    django.setup()
    run()
