from django import forms
from django.conf import settings

from .models import SiteSettings, Publication, HeroSlide, NewsArticle
from .widgets import S3DirectUploadWidget


def _s3_widget(folder):
    return S3DirectUploadWidget(folder=folder)


def _s3key(data, field_name, prefix=None):
    """Return the S3 key posted for a given field, or ''."""
    key = f'_s3key_{prefix}-{field_name}' if prefix else f'_s3key_{field_name}'
    return data.get(key, '').strip()


class SiteSettingsAdminForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = '__all__'
        widgets = {
            'candidate_photo': _s3_widget('candidate'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if getattr(settings, 'USE_S3', False):
            self.fields['candidate_photo'].required = False

    def clean_candidate_photo(self):
        if getattr(settings, 'USE_S3', False) and _s3key(self.data, 'candidate_photo'):
            return self.instance.candidate_photo
        return self.cleaned_data.get('candidate_photo')


class HeroSlideInlineForm(forms.ModelForm):
    class Meta:
        model = HeroSlide
        fields = '__all__'
        widgets = {'image': _s3_widget('candidate')}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if getattr(settings, 'USE_S3', False):
            self.fields['image'].required = False

    def _get_s3key(self):
        return _s3key(self.data, 'image', prefix=self.prefix)

    def has_changed(self):
        return super().has_changed() or bool(self._get_s3key())

    def clean_image(self):
        if getattr(settings, 'USE_S3', False) and self._get_s3key():
            return self.instance.image if (self.instance and self.instance.pk) else None
        return self.cleaned_data.get('image')

    def save(self, commit=True):
        instance = super().save(commit=False)
        if getattr(settings, 'USE_S3', False):
            key = self._get_s3key()
            if key:
                instance.image = key
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class PublicationAdminForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = '__all__'
        widgets = {
            'cover_image': _s3_widget('publications/covers'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if getattr(settings, 'USE_S3', False):
            self.fields['cover_image'].required = False

    def clean_cover_image(self):
        if getattr(settings, 'USE_S3', False) and _s3key(self.data, 'cover_image'):
            return self.instance.cover_image
        return self.cleaned_data.get('cover_image')


class NewsArticleAdminForm(forms.ModelForm):
    class Meta:
        model = NewsArticle
        fields = '__all__'
        widgets = {
            'cover_image': _s3_widget('news/covers'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if getattr(settings, 'USE_S3', False):
            self.fields['cover_image'].required = False

    def clean_cover_image(self):
        if getattr(settings, 'USE_S3', False) and _s3key(self.data, 'cover_image'):
            return self.instance.cover_image
        return self.cleaned_data.get('cover_image')
