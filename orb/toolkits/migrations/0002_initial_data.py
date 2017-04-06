# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core import management
from django.db import migrations, models




def add_initial_toolkits(apps, schema_editor):
    Toolkit = apps.get_model("toolkits", "Toolkit")
    Toolkit.objects.bulk_create([
        Toolkit(
            order_by=0,
            title="Making Content Meaningful: A Guide to Adapting Existing Global Health Content for Different Audiences",
            title_es="Crear contenido significativo: una guía para adaptar el contenido sobre salud global existente para diferentes audiencias",
            url="http://www.mhealthknowledge.org/resources/making-content-meaningful-guide-adapting-existing-global-health-content-different",
            description="""
            <p>
            The abundance of openly accessible health content—from eLearning courses and multimedia resources to guidance documents and research papers—presents a remarkable opportunity for teaching, learning, and sharing. Open health content, however, is not sufficient by itself. It is important to provide it in the appropriate context and the language of the people who will use it. The Knowledge for Health (K4Health)project developed this adaptation guide to expand the reach, usefulness, and use of evidence-based global health content, specifically as it relates to family planning. The guide outlines a framework with key steps and questions for consideration as well as activity sheets and an illustrative as well as real-life case studies that will help a user in making informed decisions in the content adaptation process.
            </p>
            """,
            description_es="""
            <p>
            La abundancia de contenido sobre salud accesible (desde cursos de aprendizaje electrónico y recursos multimedia, hasta documentos de guía y artículos de investigación) presenta una magnífica oportunidad para enseñar, aprender y compartir. No obstante, el contenido abierto sobre salud no es suficiente por sí mismo. Es importante brindarlo en el contexto adecuado y en el idioma de las personas que lo usarán. El proyecto Knowledge for Health (K4Health) desarrolló esta guía de adaptación para ampliar el alcance, la utilidad y el uso del contenido de salud global basado en evidencias,especialmente porque se relaciona con la planificación familiar. La guía presenta un marco con pasos clave y preguntas para consideración, así como hojas de actividades y un estudio de caso ilustrativo y de la vida real que ayudará al usuario a tomar decisiones informadas durante el proceso de adaptación de contenido.
            </p>
            """,
            external_image="/static/orb/images/toolkit/making-content-meaningful.png",
        ),
        Toolkit(
            order_by=1,
            title="Community Health Framework",
            title_es="Marco de salud comunitaria",
            url="http://mpoweringhealth.org/the-community-health-framework/",
            description="""
            <p>
            The Community Health Framework assists non-technical audiences in understanding community health and how it can be strengthened. An interactive power point, published under a Creative Commons license, it depicts the community health ecosystem as heath-specific and health-enabling actors and structures (formal and informal) working together to ensure that each has the agency, access, and resources to ensure the health of community members. It also includes a Toolkit with models and case studies as examples of good practice.
            </p><p>
            Download the <a href="http://mpoweringhealth.org/wp-content/uploads/2015/11/USAID-Community-Health-Framework_Version-1-0_October-28th-2015.pdf">PDF version</a> [4.7 Mb] or <a href="http://mpoweringhealth.org/wp-content/uploads/2015/11/USAID-Community-Health-Framework_Version-1-0_October-28th-2015.pptx">PPT version</a> [7.7 Mb]
            </p>
            """,
            description_es="""
            <p>
            El Marco de salud comunitaria ayuda a las audiencias no técnicas a comprender la salud comunitaria y cómo puede fortalecerse. Una presentación interactiva de Power Point, publicada bajo una licencia de Creative Commons, muestra el ecosistema de la salud comunitaria como actores y estructuras específicas de salud y que la facilitan (formales e informales), que trabajan en forma conjunta para garantizar que cada uno tenga la representación, el acceso y los recursos para garantizar la salud de los miembros de la comunidad. También incluye un kit de herramientas conmodelos y estudios de caso como ejemplos de buenas prácticas.
            </p><p>
            Descargue la <a href="http://mpoweringhealth.org/wp-content/uploads/2015/11/USAID-Community-Health-Framework_Version-1-0_October-28th-2015.pdf">versión en PDF</a> [4.7 Mb] o <a href="http://mpoweringhealth.org/wp-content/uploads/2015/11/USAID-Community-Health-Framework_Version-1-0_October-28th-2015.pptx">en PPT</a> [7.7 Mb]
            </p>
            """,
            external_image="/static/orb/images/toolkit/comm-health-frame.resized.png",
        ),
        Toolkit(
            order_by=2,
            title="Principles for Digital Development",
            title_es="Principios para el desarrollo digital",
            url="http://digitalprinciples.org/",
            description="""
            <p>
            The Principles for Digital Development (in English, Español, Français, or Português) find their roots in the efforts of individuals, development organizations, and donors alike who have called for a more concerted effort by donors and implementing partners to institutionalize lessons learned in the use of information and communication technologies (ICTs) in development projects. They were written by and for international development donors and their implementing partners, but are freely available for use by all. ThePrinciples are intended to serve as guidance rather than edict, and to be updated and refined over time.
            </p>
            """,
            description_es="""
            <p>
            Los Principios para el desarrollo digital (en inglés, español, francés o portugués) tienen sus orígenes en los esfuerzos de individuos, organizaciones de desarrollo y donantes por igual que han exigido un esfuerzo más coordinado por parte de los donantes y los socios de implementación para institucionalizar las lecciones aprendidas en el uso de información y tecnologías de la comunicación (TIC) en proyectos de desarrollo. Fueron escritos por y para donantes internacionales de desarrollo y sus socios de implementación, pero están disponibles para que todos los usen. Los Principios tienen el objetivo de servir como guía más que como mandato, y para ser actualizados y mejorados con el tiempo.
            </p>
            """,
            external_image="/static/orb/images/toolkit/digital-development.resized.png",
        ),
        Toolkit(
            order_by=3,
            title="Financing Framework to End Preventable Child and Maternal Deaths (EPCMD)",
            title_es="Marco de financiación para erradicar muertes infantiles y maternas prevenibles (End Preventable Child and Maternal Deaths, EPCMD)",
            url="https://www.usaid.gov/cii/financing-framework-end-preventable-child-and-maternal-deaths-epcmd",
            description="""
            <p>
            The U.S. Government is committed to achieving the once unimaginable goal of Ending Preventable Child and Maternal Deaths (EPCMD) by 2035. Achieving this goal in a sustainable fashion implies a gradual move toward solutions that mobilize both domestic and international resources, with the objective of putting developing country health systems on a trajectory toward financial sustainability.
            </p><p>
            The Financing Framework is designed to outline ways in which additional financial resources and tools can be utilized to support sustainability. The Framework draws on inspiration from best practices used throughout the U.S. Agency for International Development and with our health partners around the world.
            </p>
            """,
            description_es="""
            <p>
            El gobierno de los Estados Unidos está comprometido a lograr el objetivo alguna vez inimaginable de poner fin a las muertes infantiles y maternas que se pueden prevenir (Ending Preventable Child and Maternal Deaths, EPCMD) en 2035. Lograr este objetivo de manera sustentable implica un avance gradual hacia soluciones que movilizan recursos domésticos e internacionales, con el objetivo de ubicar a los sistemas de salud de países en desarrollo en una trayectoria hacia la sustentabilidad financiera.
            </p><p>
            El Marco de financiación está diseñado para establecer maneras en las que pueden utilizarse recursos y herramientas financieras adicionales para respaldar la sustentabilidad. El Marco se basa en la inspiración en las mejores prácticas usadas a través de la Agencia de los Estados Unidos para el Desarrollo Internacional y con nuestro socios de salud de todo el mundo.
            </p>
            """,
            external_image="/static/orb/images/toolkit/financing-framework-for-EPCMD.resized.jpg",
        )
    ])
    management.call_command("update_translation_fields")


class Migration(migrations.Migration):

    dependencies = [
        ('toolkits', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_initial_toolkits),
    ]
