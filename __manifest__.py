# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Academic Timetable',
    'version': '0.0.1',
    'sequence': 15,
    'summary': 'Manage Timetable for School',
    'description': "",
    'author': 'drbr-odoo',
    'category':  'Kawiil/Custom Modules',
    'website': 'https://www.odoo.com/page/crm',
    'depends': ['base','hr'],
    'data': [
            'security/ir.model.access.csv',
            'views/academic_timetable_views.xml',
            'report/academic_timetable_reports.xml',
            'report/academic_timetable_templates.xml'
            ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}

