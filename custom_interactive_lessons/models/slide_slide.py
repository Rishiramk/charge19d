from odoo import models, fields

class Slide(models.Model):
    _inherit = 'slide.slide'

    is_interactive_lesson = fields.Boolean(
        "Interactive Lesson",
        default=False,
        help="Check this box if this slide contains a custom interactive lesson."
    )
    interactive_html = fields.Html(
        "Interactive HTML",
        help="Paste the full HTML content for the interactive lesson here.",
        translate=False
    )
