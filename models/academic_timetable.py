# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta

class SchoolTimetable(models.Model):
    _name = 'school.timetable'
    _description = 'School Timetable'

    name = fields.Char(string='Timetable Name')
    standard = fields.Many2one('school.standard', string='Standard')
    semester = fields.Many2one('school.semester', string='Semester')
    entry_ids = fields.One2many('school.timetable.entry', 'timetable_id', string='Timetable Entries')


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    course_id = fields.Many2one('school.course', required=True)
    working_type = fields.Selection([('half-time','Half Time'),
                                    ('full-time','Full Time')])

class TimetableEntry(models.Model):
    _name = 'school.timetable.entry'
    _description = 'Timetable Entry'
    _rec_name = 'id'

    timetable_id = fields.Many2one('school.timetable', string='Timetable')
    teacher_id = fields.Many2one('hr.employee', string='Teacher', required=True)
    course_id = fields.Many2one('school.course', string='Course', required=True)
    time_slot_id = fields.Many2one('school.timeslot', string='Time Slot', required=True)
    room_id = fields.Many2one('school.room', string='Room', required=True)
    # day_id = fields.Many2one('day.of.week')
    day = fields.Selection([
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ], string='Day', required=True)


    @api.onchange('teacher_id')
    def _onchange_teacher_id(self):
        if self.teacher_id and self.teacher_id.course_id:
            self.course_id = self.teacher_id.course_id.id
        else:
            self.course_id = False

    @api.constrains('time_slot_id', 'day', 'teacher_id', 'timetable_id.standard', 'room_id.location')
    def _check_teacher_day_slot_standard(self):
        for entry in self:
            conflict_entries = self.env['school.timetable.entry'].search([
                '&','&',
                ('day', '=', entry.day),
                ('teacher_id', '=', entry.teacher_id.id),
                ('time_slot_id', '=', entry.time_slot_id.id),
                ('room_id.location', '=', entry.room_id.location),  # Uncomment this line if you want to include room in the check
                ('timetable_id.standard', '=', entry.timetable_id.standard.id),
                ('id', '!=', entry.id),  # Exclude the current entry
            ])

            if conflict_entries:
                raise ValidationError('Teacher is already assigned during this time slot on this day for the same standard and room!')

    @api.constrains('time_slot_id', 'day', 'timetable_id.standard')
    def _check_timeslot_visibility(self):
        for entry in self:
            visible_entries = self.env['school.timetable.entry'].search([
                '&', '&',
                ('day', '=', entry.day),
                ('time_slot_id', '=', entry.time_slot_id.id),
                ('timetable_id.standard', '=', entry.timetable_id.standard.id),
                ('id', '!=', entry.id),  # Exclude the current entry
            ])

            if visible_entries:
                raise ValidationError('This timeslot is already assigned for the same day and standard. Please choose another timeslot.')

class SchoolStandard(models.Model):
    _name = 'school.standard'
    _description = 'School Standard'

    name = fields.Char(string='Standard Name')
    description = fields.Text()

class SchoolSemester(models.Model):
    _name = 'school.semester'
    _description = 'School Semester'

    name = fields.Char(string='Semester Name')
    description = fields.Text()

class SchoolTimeslot(models.Model):
    _name = 'school.timeslot'
    _description = 'School Timeslot'

    name = fields.Char(string='Timeslot Name')
    description = fields.Text()

class SchoolCourse(models.Model):
    _name = 'school.course'
    _description = 'School Course'
    _rec_name = 'code'

    code = fields.Char(string='Course Code')
    name = fields.Char(string='Course Name')

class SchoolRoom(models.Model):
    _name = 'school.room'
    _description = 'School Room'
    _rec_name = 'location'

    location = fields.Char()
    capacity = fields.Char(string='Room Capacity')


