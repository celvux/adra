from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html

from .forms import (
    SiteSettingsAdminForm, HeroSlideInlineForm,
    PublicationAdminForm, NewsArticleAdminForm,
)
from .models import (
    SiteSettings, HeroSlide, KeyStat, BioDimension, TimelineStep,
    ProgramAxis, Commitment, Publication, ComparativeAnalysis,
    ComparisonPoint, NewsArticle,
)


# ─── Inline ───────────────────────────────────────────────────────────────────

class HeroSlideInline(admin.TabularInline):
    model = HeroSlide
    form = HeroSlideInlineForm
    extra = 2
    ordering = ('order',)
    fields = ('image', 'caption', 'order')
    verbose_name = "Photo du carousel"
    verbose_name_plural = "Photos du carousel — défilement 3 s/image"


class ComparisonPointInline(admin.TabularInline):
    model = ComparisonPoint
    extra = 2
    ordering = ('order',)
    fields = ('theme', 'promise_text', 'reality_text', 'order')
    verbose_name = "Point de comparaison"
    verbose_name_plural = "Points de comparaison"


# ─── SiteSettings ─────────────────────────────────────────────────────────────

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    form = SiteSettingsAdminForm
    inlines = [HeroSlideInline]

    def save_model(self, request, obj, form, change):
        if getattr(settings, 'USE_S3', False):
            key = request.POST.get('_s3key_candidate_photo', '').strip()
            if key:
                obj.candidate_photo = key
        super().save_model(request, obj, form, change)

    fieldsets = (
        ('📸 Photo du candidat', {
            'fields': ('candidate_photo',),
            'description': (
                'Portrait vertical recommandé (3:4 ou 2:3). '
                'Quand une photo est chargée, elle remplace le cercle "AD" dans le hero.'
            ),
        }),
        ('🏷️ Informations générales', {
            'fields': ('candidate_name', 'slogan', 'bio_short', 'party_name', 'election_date', 'meta_description'),
        }),
        ('🏷️ Bandeau tag', {
            'fields': ('hero_tag',),
        }),
        ('✏️ Grand titre (3 lignes)', {
            'fields': ('hero_title_line1', 'hero_title_line2', 'hero_title_accent'),
            'description': "La ligne 3 s'affiche en couleur d'accent — c'est le mot fort du slogan.",
        }),
        ('👤 Nom, rôle & description', {
            'fields': (
                'hero_candidate_name', 'hero_role',
                'hero_desc_before', 'hero_desc_strong', 'hero_desc_after',
            ),
        }),
        ('🔘 Boutons', {
            'fields': ('hero_btn_primary', 'hero_btn_secondary'),
        }),
        ('🖼️ Panneau droit (placeholder sans photo)', {
            'fields': ('hero_placeholder_initials', 'hero_placeholder_name', 'hero_placeholder_role'),
            'classes': ('collapse',),
        }),
        ('📅 Bandeau date (bas du hero)', {
            'fields': ('hero_banner_label1', 'hero_banner_date', 'hero_banner_label2', 'hero_banner_label3'),
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# ─── KeyStat ──────────────────────────────────────────────────────────────────

@admin.register(KeyStat)
class KeyStatAdmin(admin.ModelAdmin):
    list_display = ('number', 'suffix', 'label', 'icon', 'order')
    list_editable = ('order',)
    ordering = ('order',)


# ─── BioDimension ─────────────────────────────────────────────────────────────

@admin.register(BioDimension)
class BioDimensionAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'order')
    list_editable = ('order',)
    ordering = ('order',)


# ─── TimelineStep ─────────────────────────────────────────────────────────────

@admin.register(TimelineStep)
class TimelineStepAdmin(admin.ModelAdmin):
    list_display = ('year', 'title', 'icon', 'order')
    list_editable = ('order',)
    ordering = ('order',)
    search_fields = ('title', 'description')


# ─── ProgramAxis ──────────────────────────────────────────────────────────────

@admin.register(ProgramAxis)
class ProgramAxisAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured_badge', 'icon', 'order')
    list_editable = ('order',)
    ordering = ('order',)
    search_fields = ('title', 'description')

    @admin.display(description="Axe vedette ?", boolean=True)
    def featured_badge(self, obj):
        return obj.is_featured


# ─── Commitment ───────────────────────────────────────────────────────────────

@admin.register(Commitment)
class CommitmentAdmin(admin.ModelAdmin):
    list_display = ('text_short', 'icon', 'order')
    list_editable = ('order',)
    ordering = ('order',)

    @admin.display(description="Engagement")
    def text_short(self, obj):
        return obj.text[:80]


# ─── Publication ──────────────────────────────────────────────────────────────

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    form = PublicationAdminForm
    list_display = ('title', 'badge_category', 'year', 'institution', 'is_featured', 'order')
    list_filter = ('category', 'is_featured', 'year')
    search_fields = ('title', 'summary', 'institution')
    list_editable = ('is_featured', 'order')
    ordering = ('-year', 'order')
    fieldsets = (
        ('Informations principales', {
            'fields': ('title', 'category', 'year', 'institution', 'is_featured', 'order'),
        }),
        ('Contenu', {
            'fields': ('summary', 'pdf_url'),
        }),
        ('📸 Image de couverture', {
            'fields': ('cover_image',),
        }),
    )

    def save_model(self, request, obj, form, change):
        if getattr(settings, 'USE_S3', False):
            key = request.POST.get('_s3key_cover_image', '').strip()
            if key:
                obj.cover_image = key
        super().save_model(request, obj, form, change)

    @admin.display(description="Catégorie")
    def badge_category(self, obj):
        couleurs = {
            'academic':    ('background:#1a2744;color:#c8d8f0',),
            'report':      ('background:#2c5f2e;color:#c8f0cc',),
            'opinion':     ('background:#7a2c00;color:#f0c8a0',),
            'comparative': ('background:#4a1a6b;color:#e0c8f0',),
        }
        style = couleurs.get(obj.category, ('',))[0]
        return format_html(
            '<span style="{}; padding:2px 8px; border-radius:3px; font-size:11px; font-weight:700;">{}</span>',
            style, obj.get_category_display()
        )


# ─── ComparativeAnalysis ──────────────────────────────────────────────────────

@admin.register(ComparativeAnalysis)
class ComparativeAnalysisAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'published_at')
    list_editable = ('is_published',)
    inlines = [ComparisonPointInline]
    fieldsets = (
        ('En-tête', {
            'fields': ('title', 'subtitle', 'is_published'),
        }),
        ('Contenu', {
            'fields': ('intro', 'promise_column_title', 'reality_column_title', 'conclusion'),
        }),
        ('📸 Image', {
            'fields': ('cover_image',),
            'classes': ('collapse',),
        }),
    )


# ─── NewsArticle ──────────────────────────────────────────────────────────────

@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    form = NewsArticleAdminForm
    list_display = ('title', 'published_at', 'is_published')
    list_filter = ('is_published', 'published_at')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    ordering = ('-published_at',)
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Informations principales', {
            'fields': ('title', 'slug', 'published_at', 'is_published'),
        }),
        ('Contenu', {
            'fields': ('content',),
        }),
        ('📸 Image de couverture', {
            'fields': ('cover_image',),
        }),
    )

    def save_model(self, request, obj, form, change):
        if getattr(settings, 'USE_S3', False):
            key = request.POST.get('_s3key_cover_image', '').strip()
            if key:
                obj.cover_image = key
        super().save_model(request, obj, form, change)


# ─── Libellés français ────────────────────────────────────────────────────────

admin.site.site_title = "FRONDEG · Adra Diallo"
admin.site.site_header = "FRONDEG — Espace de gestion"
admin.site.index_title = "Contenu du site de campagne — Adra Diallo"
