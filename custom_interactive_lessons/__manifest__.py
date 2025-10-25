{
    'name': 'Interactive eLearning Lessons',
    'version': '19.0.1.0.0',
    'category': 'eLearning',
    'summary': 'Scalable interactive HTML lessons for courses (CodeMirror, simulations, etc.)',
    'description': """
        Supports 20+ unique lessons per course with shared JS/CSS.
        Paste HTML per slide; auto-inits sliders, editors, themes.
    """,
    'depends': ['website_slides'],
    'data': [
        'views/slide_slide_views.xml',
        'views/interactive_lesson_template.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.15/codemirror.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.15/mode/python/python.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.15/theme/dracula.min.css',
            'custom_interactive_lessons/static/src/js/interactive_lesson.js',
        ],
        'web.assets_frontend.css': [
            'custom_interactive_lessons/static/src/css/interactive_lesson.css',
        ],
    },
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
