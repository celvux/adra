from datetime import date
from django.core.management.base import BaseCommand
from campaign.models import (
    SiteSettings, KeyStat, BioDimension, TimelineStep,
    ProgramAxis, Commitment, Publication,
)


class Command(BaseCommand):
    help = 'Charge les données initiales de la campagne Adra Diallo — FRONDEG Liste Nationale 2026'

    def handle(self, *args, **options):
        self._seed_site_settings()
        self._seed_key_stats()
        self._seed_bio_dimensions()
        self._seed_timeline()
        self._seed_programme()
        self._seed_commitments()
        self._seed_publications()
        self.stdout.write(self.style.SUCCESS('✓ Données Adra Diallo chargées avec succès.'))

    def _seed_site_settings(self):
        obj, created = SiteSettings.objects.get_or_create(pk=1)
        obj.candidate_name = "Abdourahamane « Adra » Diallo"
        obj.slogan = "La connaissance au service de la Guinée"
        obj.bio_short = "Juriste, politologue, chercheur — une expertise académique au service de la Guinée."
        obj.party_name = "FRONDEG"
        obj.election_date = date(2026, 5, 24)
        obj.meta_description = (
            "Adra Diallo, juriste et politologue, candidat FRONDEG sur la liste nationale "
            "aux élections législatives guinéennes du 24 mai 2026."
        )
        obj.save()
        self.stdout.write("  → SiteSettings configuré.")

    def _seed_key_stats(self):
        KeyStat.objects.all().delete()
        data = [
            ('10', 10, '+', 0, "Ans de recherche", 'fas fa-flask', 0),
            ('5', 5, '', 0, "Axes programmatiques", 'fas fa-layer-group', 1),
            ('15', 15, '+', 0, "Publications académiques", 'fas fa-book', 2),
            ('2026', None, '', 0, "La Guinée en marche", 'fas fa-flag', 3),
        ]
        for number, numeric_value, suffix, start_value, label, icon, order in data:
            KeyStat.objects.create(
                number=number,
                numeric_value=numeric_value,
                suffix=suffix,
                start_value=start_value,
                label=label,
                icon=icon,
                order=order,
            )
        self.stdout.write("  → 4 chiffres clés créés.")

    def _seed_bio_dimensions(self):
        BioDimension.objects.all().delete()
        dimensions = [
            {
                'title': "L'Intellectuel Engagé",
                'icon': 'fas fa-graduation-cap',
                'description': (
                    "Juriste et politologue formé à l'Université Cheikh Anta Diop de Dakar, "
                    "Adra Diallo est chercheur au Centre de Documentation et de Prospective sur "
                    "les Institutions et l'Action Collective (CDPIAC) de l'Université Toulouse "
                    "Capitole depuis 2015. Ses travaux portent sur la gouvernance institutionnelle, "
                    "les conflits africains, la sociologie militaire comparée et les usages de "
                    "l'intelligence artificielle dans les sociétés en développement. "
                    "Plus de 15 publications académiques attestent d'une rigueur scientifique rare."
                ),
                'order': 0,
            },
            {
                'title': "L'Homme de Terrain",
                'icon': 'fas fa-hands-helping',
                'description': (
                    "Médiateur communautaire reconnu, conseiller estudiantin et pilier de la "
                    "diaspora guinéenne à Toulouse, Adra Diallo est ancré dans les réalités "
                    "humaines et sociales de la Guinée. Son engagement pour la jeunesse, "
                    "la paix sociale et le leadership citoyen traverse toute sa vie publique. "
                    "Il connaît les aspirations de sa génération en Europe comme celles des "
                    "jeunes restés au pays — une double lecture indispensable pour légiférer "
                    "avec pertinence et humanité."
                ),
                'order': 1,
            },
        ]
        for dim_data in dimensions:
            BioDimension.objects.create(**dim_data)
        self.stdout.write("  → 2 dimensions biographiques créées.")

    def _seed_timeline(self):
        TimelineStep.objects.all().delete()
        steps = [
            (
                '2010',
                'Université Cheikh Anta Diop — Dakar',
                'Formation en droit et sciences politiques · Rapport Guinée–Sénégal',
                'fas fa-university', 0,
            ),
            (
                '2010',
                'Rôle de l\'armée guinéenne (1984–2010)',
                'Première publication académique sur la construction de l\'État guinéen',
                'fas fa-book', 1,
            ),
            (
                '2012',
                'Immigration clandestine & fuite des cerveaux',
                'Étude sur les dynamiques migratoires en Afrique de l\'Ouest',
                'fas fa-globe-africa', 2,
            ),
            (
                '2015',
                'Direction Cellule Afrique — CDPIAC',
                'Université Toulouse Capitole · Expert conflits & gouvernance africaine',
                'fas fa-landmark', 3,
            ),
            (
                '2019',
                'Intelligence artificielle vs intelligence humaine',
                'Publication sur les enjeux technologiques pour les sociétés africaines',
                'fas fa-robot', 4,
            ),
            (
                '2020 – 2024',
                'Sociologie militaire comparée',
                'Recherches approfondies sur les transitions et ruptures institutionnelles',
                'fas fa-chess-rook', 5,
            ),
            (
                '2024 – 2025',
                'Engagement communautaire diaspora',
                'Conseiller estudiantin · Médiateur interculturel à Toulouse',
                'fas fa-hands-helping', 6,
            ),
            (
                '2026',
                'Candidature FRONDEG — Liste nationale',
                'Mettre la connaissance au service de la représentation guinéenne',
                'fas fa-flag', 7,
            ),
        ]
        for year, title, description, icon, order in steps:
            TimelineStep.objects.create(
                year=year, title=title, description=description, icon=icon, order=order,
            )
        self.stdout.write("  → 8 étapes du parcours créées.")

    def _seed_programme(self):
        ProgramAxis.objects.all().delete()
        axes = [
            {
                'title': 'Gouvernance responsable & réforme institutionnelle',
                'icon': 'fas fa-balance-scale',
                'description': (
                    "Fort d'une décennie de recherche sur la gouvernance africaine, Adra Diallo "
                    "portera des réformes fondées sur des données et des comparaisons internationales — "
                    "pas sur des idéologies. La loi comme outil de stabilisation, pas de domination."
                ),
                'points': (
                    "Réforme du cadre électoral pour garantir des scrutins transparents et crédibles\n"
                    "Loi sur la transparence budgétaire et la redevabilité des institutions\n"
                    "Renforcement de l'indépendance de la justice guinéenne\n"
                    "Décentralisation effective des pouvoirs et des ressources"
                ),
                'is_featured': True,
                'order': 0,
            },
            {
                'title': 'Paix sociale & cohésion nationale',
                'icon': 'fas fa-dove',
                'description': (
                    "La Guinée est un pays multi-ethnique dont la cohésion est la première richesse. "
                    "L'expertise d'Adra Diallo en médiation et en conflits africains sera mise au "
                    "service d'une politique active de réconciliation nationale."
                ),
                'points': (
                    "Création d'un Haut Comité pour la Réconciliation nationale\n"
                    "Programmes de médiation intercommunautaire financés par l'État\n"
                    "Intégration de la culture de paix dans les curricula scolaires"
                ),
                'is_featured': False,
                'order': 1,
            },
            {
                'title': 'Emploi des jeunes & formation professionnelle',
                'icon': 'fas fa-briefcase',
                'description': (
                    "La jeunesse guinéenne est la première ressource nationale. "
                    "Adra Diallo défendra des politiques d'insertion ambitieuses, "
                    "fondées sur les besoins réels du marché du travail guinéen et régional."
                ),
                'points': (
                    "Cadre législatif pour les partenariats universités–entreprises\n"
                    "Programme national de formation aux métiers du numérique et de l'artisanat\n"
                    "Fonds d'investissement jeunesse doté d'un mécanisme de microcrédit\n"
                    "Reconnaissance des diplômes de la diaspora"
                ),
                'is_featured': False,
                'order': 2,
            },
            {
                'title': 'Sécurité & stabilité régionale',
                'icon': 'fas fa-shield-alt',
                'description': (
                    "Chercheur spécialisé en conflits et en sociologie militaire comparée, "
                    "Adra Diallo dispose d'une compréhension unique des dynamiques sécuritaires "
                    "en Afrique de l'Ouest — une expertise directement mobilisable à l'Assemblée nationale."
                ),
                'points': (
                    "Politique de défense fondée sur la doctrine et non sur les intérêts des clans\n"
                    "Coopération régionale CEDEAO en matière de sécurité transfrontalière\n"
                    "Réforme du secteur de la sécurité avec contrôle parlementaire renforcé"
                ),
                'is_featured': False,
                'order': 3,
            },
            {
                'title': 'Innovation, sciences & développement humain',
                'icon': 'fas fa-atom',
                'description': (
                    "Un pays qui n'investit pas dans la connaissance est condamné à subir les "
                    "décisions des autres. Adra Diallo défendra un plan national pour la science, "
                    "l'enseignement supérieur et l'innovation technologique."
                ),
                'points': (
                    "Loi cadre pour la recherche scientifique et l'enseignement supérieur\n"
                    "Programme national d'accès au numérique pour les zones rurales\n"
                    "Attractivité pour les chercheurs de la diaspora guinéenne\n"
                    "Partenariats académiques internationaux en faveur de la Guinée"
                ),
                'is_featured': False,
                'order': 4,
            },
        ]
        for axis_data in axes:
            ProgramAxis.objects.create(**axis_data)
        self.stdout.write("  → 5 axes du programme créés.")

    def _seed_commitments(self):
        Commitment.objects.all().delete()
        commitments = [
            ("Porter la rigueur académique dans chaque débat législatif", 'fas fa-book-open', 0),
            ("Rendre compte publiquement de mon action tous les trimestres", 'fas fa-chart-bar', 1),
            ("Défendre sans relâche les intérêts de la Guinée face aux pressions étrangères", 'fas fa-flag', 2),
            ("Placer la science et la connaissance au cœur des politiques publiques", 'fas fa-flask', 3),
            ("Être la voix de la diaspora guinéenne et des jeunes sans tribune", 'fas fa-microphone', 4),
            ("Refuser tout compromis sur l'état de droit et la séparation des pouvoirs", 'fas fa-gavel', 5),
        ]
        for text, icon, order in commitments:
            Commitment.objects.create(text=text, icon=icon, order=order)
        self.stdout.write("  → 6 engagements créés.")

    def _seed_publications(self):
        publications = [
            {
                'title': "Le rapport entre la Guinée et le Sénégal",
                'category': 'report',
                'year': '2010',
                'institution': "Université Cheikh Anta Diop",
                'summary': (
                    "Étude des relations diplomatiques, économiques et culturelles entre la "
                    "République de Guinée et la République du Sénégal. Analyse des flux "
                    "migratoires, des échanges commerciaux et des convergences institutionnelles "
                    "entre les deux États voisins."
                ),
                'is_featured': False,
                'order': 4,
            },
            {
                'title': "L'impact de l'immigration clandestine en Afrique de l'Ouest — fuite des cerveaux",
                'category': 'academic',
                'year': '2012',
                'institution': "",
                'summary': (
                    "Analyse des dynamiques de l'émigration irrégulière depuis l'Afrique de "
                    "l'Ouest vers l'Europe et les pays du Golfe. Évaluation de l'impact de la "
                    "fuite des cerveaux sur les capacités institutionnelles et économiques des "
                    "pays d'origine, avec focus sur la Guinée."
                ),
                'is_featured': True,
                'order': 2,
            },
            {
                'title': "Le rôle de l'armée guinéenne dans la construction de l'État guinéen (1984–2010)",
                'category': 'academic',
                'year': '2010',
                'institution': "",
                'summary': (
                    "Étude de la sociologie de l'institution militaire guinéenne depuis le coup "
                    "d'État de 1984 jusqu'aux événements de 2009. Analyse des relations "
                    "entre pouvoir militaire, élites politiques et société civile dans la "
                    "construction — et la déstabilisation — de l'État guinéen."
                ),
                'is_featured': True,
                'order': 0,
            },
            {
                'title': "La limite entre intelligence artificielle et intelligence humaine",
                'category': 'academic',
                'year': '2019',
                'institution': "",
                'summary': (
                    "Réflexion épistémologique sur les frontières entre les capacités cognitives "
                    "humaines et les systèmes d'intelligence artificielle. Implications pour les "
                    "sociétés africaines en développement : risques, opportunités et enjeux "
                    "éthiques de l'adoption des technologies d'IA."
                ),
                'is_featured': False,
                'order': 3,
            },
            {
                'title': "Sociologie militaire comparée — Transitions institutionnelles en Afrique subsaharienne",
                'category': 'comparative',
                'year': '2026',
                'institution': "CDPIAC — Université Toulouse Capitole",
                'summary': (
                    "Étude comparative des transitions militaro-civiles dans plusieurs États "
                    "d'Afrique subsaharienne. Analyse des facteurs qui favorisent ou entravent "
                    "la consolidation démocratique après une rupture institutionnelle, "
                    "avec applications à la situation guinéenne contemporaine."
                ),
                'is_featured': True,
                'order': 1,
            },
        ]
        for pub_data in publications:
            Publication.objects.get_or_create(
                title=pub_data['title'],
                defaults=pub_data,
            )
        self.stdout.write(f"  → {len(publications)} publications académiques chargées.")
