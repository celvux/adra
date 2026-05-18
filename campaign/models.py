import json
from datetime import date

from django.db import models
from django.utils.html import escape, mark_safe
from django.utils.text import slugify


class SiteSettings(models.Model):
    candidate_name = models.CharField(
        max_length=200, default="Abdourahamane Adra Diallo",
        verbose_name="Nom du candidat",
    )
    slogan = models.CharField(
        max_length=300, default="La connaissance au service de la Guinée",
        verbose_name="Slogan",
    )
    bio_short = models.TextField(
        default="Juriste, politologue, chercheur — une expertise académique au service de la Guinée.",
        verbose_name="Accroche hero (bio courte)",
    )
    candidate_photo = models.ImageField(
        upload_to='candidate/', blank=True, null=True,
        verbose_name="Photo du candidat",
        help_text="Portrait vertical recommandé (3:4). Remplace le cercle AD dans le hero.",
    )
    party_name = models.CharField(
        max_length=100, default="FRONDEG",
        verbose_name="Nom du parti",
    )
    election_date = models.DateField(
        default=date(2026, 5, 24),
        verbose_name="Date de l'élection",
    )
    meta_description = models.TextField(
        blank=True,
        default=(
            "Adra Diallo, juriste et politologue, candidat FRONDEG sur la liste nationale "
            "aux élections législatives guinéennes du 24 mai 2026."
        ),
        verbose_name="Description méta (SEO)",
    )

    # ── Hero fields ───────────────────────────────────────────────────────────
    hero_tag = models.CharField(
        max_length=100, default="FRONDEG · Liste Nationale 2026",
        verbose_name="Bandeau tag",
    )
    hero_title_line1 = models.CharField(max_length=100, default="La Guinée", verbose_name="Titre — ligne 1")
    hero_title_line2 = models.CharField(max_length=100, default="mérite", verbose_name="Titre — ligne 2")
    hero_title_accent = models.CharField(
        max_length=100, default="l'excellence.",
        verbose_name="Titre — ligne 3 (accent)",
        help_text="Affiché en couleur d'accent — le mot-clé fort du slogan.",
    )
    hero_candidate_name = models.CharField(
        max_length=200, default="Abdourahamane « Adra » Diallo",
        verbose_name="Nom du candidat (hero)",
    )
    hero_role = models.CharField(
        max_length=300, default="Juriste · Politologue · Candidat FRONDEG",
        verbose_name="Rôle / titre (sous le nom)",
    )
    hero_desc_before = models.CharField(
        max_length=300, default="Chercheur au CDPIAC depuis 2015, ",
        verbose_name="Description — texte avant le gras", blank=True,
    )
    hero_desc_strong = models.CharField(
        max_length=150, default="expert en gouvernance et conflits africains",
        verbose_name="Description — texte en gras", blank=True,
    )
    hero_desc_after = models.CharField(
        max_length=500,
        default=(
            ", Adra Diallo porte une vision ancrée dans la science et l'engagement citoyen. "
            "Il se présente devant vous avec la rigueur du chercheur et la chaleur de l'homme de terrain."
        ),
        verbose_name="Description — texte après le gras", blank=True,
    )
    hero_btn_primary = models.CharField(
        max_length=100, default="Découvrir le programme",
        verbose_name="Bouton principal",
    )
    hero_btn_secondary = models.CharField(
        max_length=100, default="Mon parcours",
        verbose_name="Bouton secondaire",
    )
    hero_placeholder_initials = models.CharField(
        max_length=5, default="AD",
        verbose_name="Initiales (cercle placeholder)",
    )
    hero_placeholder_name = models.CharField(
        max_length=200, default="Adra Diallo",
        verbose_name="Nom (panneau droit)",
    )
    hero_placeholder_role = models.CharField(
        max_length=200, default="Juriste · Politologue · Chercheur",
        verbose_name="Rôle (panneau droit)",
    )
    hero_banner_label1 = models.CharField(
        max_length=100, default="Élections législatives",
        verbose_name="Bandeau — libellé 1",
    )
    hero_banner_date = models.CharField(
        max_length=50, default="24 mai 2026",
        verbose_name="Bandeau — date",
    )
    hero_banner_label2 = models.CharField(
        max_length=100, default="Liste nationale",
        verbose_name="Bandeau — libellé 2",
    )
    hero_banner_label3 = models.CharField(
        max_length=100, default="FRONDEG",
        verbose_name="Bandeau — libellé 3",
    )

    class Meta:
        verbose_name = "Paramètres du site"
        verbose_name_plural = "Paramètres du site"

    def __str__(self):
        return "Paramètres du site"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def hero_description_html(self):
        before = escape(self.hero_desc_before)
        strong = escape(self.hero_desc_strong)
        after = escape(self.hero_desc_after)
        if strong:
            return mark_safe(f'{before}<strong>{strong}</strong>{after}')
        return mark_safe(f'{before}{after}')


class HeroSlide(models.Model):
    site = models.ForeignKey('SiteSettings', on_delete=models.CASCADE, related_name='slides')
    image = models.ImageField(
        upload_to='candidate/',
        help_text="Photo défilante du hero (format portrait 3:4 recommandé).",
    )
    caption = models.CharField(max_length=200, blank=True, verbose_name="Légende (optionnelle)")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Photo du carousel hero"
        verbose_name_plural = "Carousel hero — Photos"

    def __str__(self):
        return f"Slide {self.order + 1}"


class BioDimension(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre de la dimension")
    icon = models.CharField(
        max_length=60, default='fas fa-user',
        verbose_name="Icône FontAwesome",
        help_text="Ex : fas fa-graduation-cap",
    )
    description = models.TextField(verbose_name="Description")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Dimension biographique"
        verbose_name_plural = "Portrait — Double dimension"

    def __str__(self):
        return self.title


class TimelineStep(models.Model):
    year = models.CharField(max_length=30, verbose_name="Année / période")
    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(blank=True, verbose_name="Description")
    icon = models.CharField(
        max_length=60, default='fas fa-circle',
        verbose_name="Icône FontAwesome",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Étape du parcours"
        verbose_name_plural = "Parcours — Étapes"

    def __str__(self):
        return f"{self.year} — {self.title}"


class ProgramAxis(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre de l'axe")
    icon = models.CharField(
        max_length=60, default='fas fa-check-circle',
        verbose_name="Icône FontAwesome",
    )
    description = models.TextField(verbose_name="Description")
    points = models.TextField(
        blank=True,
        verbose_name="Points du programme",
        help_text="Un point par ligne.",
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Axe vedette ?",
        help_text="Affichage pleine largeur en tête de grille.",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Axe du programme"
        verbose_name_plural = "Programme — Axes"

    def __str__(self):
        return self.title

    def points_list(self):
        return [p.strip() for p in self.points.splitlines() if p.strip()]


class Commitment(models.Model):
    text = models.TextField(verbose_name="Texte de l'engagement")
    icon = models.CharField(
        max_length=60, default='fas fa-check',
        verbose_name="Icône FontAwesome",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Engagement"
        verbose_name_plural = "Engagements"

    def __str__(self):
        return self.text[:80]


class KeyStat(models.Model):
    number = models.CharField(max_length=20, verbose_name="Valeur affichée")
    numeric_value = models.IntegerField(
        null=True, blank=True,
        verbose_name="Valeur numérique (animation)",
        help_text="Entier pour l'animation compteur. Laisser vide pour désactiver.",
    )
    suffix = models.CharField(
        max_length=20, blank=True,
        verbose_name="Suffixe",
        help_text="Ex : +, ans, publications",
    )
    start_value = models.IntegerField(
        default=0,
        verbose_name="Valeur de départ",
    )
    label = models.CharField(max_length=100, verbose_name="Libellé")
    icon = models.CharField(
        max_length=60, default='fas fa-star',
        verbose_name="Icône FontAwesome",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Chiffre clé"
        verbose_name_plural = "Chiffres clés"

    def __str__(self):
        return f"{self.number}{self.suffix} — {self.label}"


class Publication(models.Model):
    CATEGORY_CHOICES = [
        ('academic', 'Article académique'),
        ('report', 'Rapport / Étude'),
        ('opinion', 'Tribune / Opinion'),
        ('comparative', 'Étude comparative'),
    ]
    title = models.CharField(max_length=300, verbose_name="Titre")
    category = models.CharField(
        max_length=30, choices=CATEGORY_CHOICES,
        verbose_name="Catégorie",
    )
    year = models.CharField(max_length=10, verbose_name="Année")
    institution = models.CharField(
        max_length=200, blank=True,
        verbose_name="Institution",
        help_text="Ex : Université Cheikh Anta Diop",
    )
    summary = models.TextField(verbose_name="Résumé")
    cover_image = models.ImageField(
        upload_to='publications/covers/', blank=True,
        verbose_name="Image de couverture",
    )
    pdf_url = models.URLField(
        blank=True,
        verbose_name="Lien PDF",
        help_text="URL externe ou Supabase Storage",
    )
    is_featured = models.BooleanField(default=False, verbose_name="Mise en avant ?")
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-year', 'order']
        verbose_name = "Publication académique"
        verbose_name_plural = "Publications & Travaux académiques"

    def __str__(self):
        return f"{self.year} — {self.title}"

    def cover_url(self):
        return self.cover_image.url if self.cover_image else ''


class ComparativeAnalysis(models.Model):
    title = models.CharField(max_length=300, verbose_name="Titre")
    subtitle = models.CharField(max_length=300, blank=True, verbose_name="Sous-titre")
    intro = models.TextField(verbose_name="Introduction")
    promise_column_title = models.CharField(
        max_length=100, default="La Promesse — L'inexpérience",
        verbose_name="Titre colonne Promesse",
    )
    reality_column_title = models.CharField(
        max_length=100, default="Le Vécu — La réalité",
        verbose_name="Titre colonne Réalité",
    )
    conclusion = models.TextField(verbose_name="Conclusion")
    cover_image = models.ImageField(
        upload_to='analyses/', blank=True,
        verbose_name="Image de couverture",
    )
    published_at = models.DateField(auto_now_add=True)
    is_published = models.BooleanField(default=False, verbose_name="Publié ?")

    class Meta:
        verbose_name = "Analyse comparative"
        verbose_name_plural = "Analyse comparative — Doumbouya"

    def __str__(self):
        return self.title


class ComparisonPoint(models.Model):
    analysis = models.ForeignKey(
        ComparativeAnalysis, related_name='points', on_delete=models.CASCADE,
    )
    theme = models.CharField(max_length=200, verbose_name="Thème")
    promise_text = models.TextField(verbose_name="Texte — Promesse")
    reality_text = models.TextField(verbose_name="Texte — Réalité")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Point de comparaison"
        verbose_name_plural = "Points de comparaison"

    def __str__(self):
        return self.theme


class NewsArticle(models.Model):
    title = models.CharField(max_length=300, verbose_name="Titre")
    slug = models.SlugField(max_length=320, unique=True, blank=True)
    cover_image = models.ImageField(
        upload_to='news/covers/', blank=True,
        verbose_name="Image de couverture",
    )
    content = models.TextField(verbose_name="Contenu")
    published_at = models.DateField(default=date.today, verbose_name="Date de publication")
    is_published = models.BooleanField(default=True, verbose_name="Publié ?")

    class Meta:
        ordering = ['-published_at']
        verbose_name = "Actualité de campagne"
        verbose_name_plural = "Actualités de campagne"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug = base
            n = 1
            while NewsArticle.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def cover_url(self):
        return self.cover_image.url if self.cover_image else ''
