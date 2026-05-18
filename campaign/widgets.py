from django import forms
from django.conf import settings
from django.utils.html import format_html, mark_safe


class S3DirectUploadWidget(forms.ClearableFileInput):
    """ImageField widget that uploads the file directly to S3 from the browser.

    When USE_S3 is False (local dev), falls back to standard file upload.
    When USE_S3 is True, the JS in s3_direct_upload.js intercepts the file
    selection, PUTs it directly to Supabase via a pre-signed URL, and stores
    the resulting S3 key in a hidden input — so no file data passes through
    the Vercel function.
    """

    class Media:
        js = ['admin/js/s3_direct_upload.js']

    def __init__(self, folder='uploads', *args, **kwargs):
        self.folder = folder
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        if not getattr(settings, 'USE_S3', False):
            return super().render(name, value, attrs, renderer)

        if attrs is None:
            attrs = {}
        attrs['class'] = (attrs.get('class', '') + ' s3-file-input').strip()
        attrs['data-folder'] = self.folder

        file_html = super().render(name, value, attrs, renderer)
        extra = format_html(
            '<input type="hidden" name="_s3key_{}" value="">'
            '<div class="s3-upload-status"'
            ' style="margin-top:5px;font-size:12px;font-weight:600;"></div>',
            name,
        )
        return mark_safe(f'<div class="s3-upload-wrapper">{file_html}{extra}</div>')
