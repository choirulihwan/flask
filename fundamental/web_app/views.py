from flask import request, url_for
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from werkzeug.utils import redirect
from wtforms import TextAreaField
from wtforms.widgets import TextArea


class CKEditorWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += " ckeditor"
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKEditorWidget, self).__call__(field, **kwargs)


class CKEditorField(TextAreaField):
    widget = CKEditorWidget()

class SecureAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect(request.full_path)
        return redirect(url_for('security.login'), next=request.full_path)

class AdminOnlyView(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect(request.full_path)
        return redirect(url_for('security.login'), next=request.full_path)

class PageAdminView(AdminOnlyView):
    # pass
    form_overrides = dict(content=CKEditorField)
    create_template = 'admin/ckeditor.html'
    edit_template = 'admin/ckeditor.html'
    column_list = ('title', 'slug')

class MenuAdminView(AdminOnlyView):
    pass

