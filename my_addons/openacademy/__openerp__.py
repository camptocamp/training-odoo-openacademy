{'name': 'Open Academy',
 'author': 'Vous!',
 'version': '1.0',
 'category': 'Tools',
 'summary': 'Courses, Sessions, Subscriptions',
 'description': """,
Open Academy
============

Open Academy module for managing trainings:
- training courses
- training sessions
- attendees registration
 """,
 'depends': ['base'],
 'data': ['security/security.xml',
          'views/menus.xml',
          'views/course_views.xml',
          'views/session_views.xml',
          'views/res_partner_views.xml',
          'wizards/register_views.xml',
          'data/res_partner_category.xml',
          'security/ir.model.access.csv',
          ],
 'images': [],
 'demo': ['demo/course.xml',
          ],
 'application': True,
 }
