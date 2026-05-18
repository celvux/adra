import os
import uuid

from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .models import (
    SiteSettings, HeroSlide, KeyStat, BioDimension, TimelineStep,
    ProgramAxis, Commitment, Publication, ComparativeAnalysis, NewsArticle,
)


@staff_member_required
@require_POST
def presign_upload(request):
    """Return a pre-signed S3 PUT URL so the browser can upload directly to Supabase."""
    from django.conf import settings

    if not getattr(settings, 'USE_S3', False):
        return JsonResponse({'error': 'S3 non configuré'}, status=400)

    import boto3
    from botocore.config import Config

    filename = request.POST.get('filename', 'upload')
    folder = request.POST.get('folder', 'uploads')
    content_type = request.POST.get('content_type', 'image/jpeg')

    ext = os.path.splitext(filename)[1].lower()
    if ext not in {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.pdf'}:
        return JsonResponse({'error': 'Type de fichier non autorisé'}, status=400)

    key = f"{folder}/{uuid.uuid4().hex}{ext}"

    client = boto3.client(
        's3',
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
        config=Config(signature_version='s3v4'),
    )
    presigned_url = client.generate_presigned_url(
        'put_object',
        Params={
            'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
            'Key': key,
            'ContentType': content_type,
        },
        ExpiresIn=300,
    )
    return JsonResponse({'url': presigned_url, 'key': key})


def index(request):
    analysis = ComparativeAnalysis.objects.filter(is_published=True).prefetch_related('points').first()
    context = {
        'site_settings': SiteSettings.load(),
        'hero_slides': HeroSlide.objects.filter(site_id=1),
        'key_stats': KeyStat.objects.all(),
        'bio_dimensions': BioDimension.objects.all(),
        'timeline_steps': TimelineStep.objects.all(),
        'program_axes': ProgramAxis.objects.all(),
        'commitments': Commitment.objects.all(),
        'publications': Publication.objects.all(),
        'analysis': analysis,
        'news_articles': NewsArticle.objects.filter(is_published=True),
    }
    return render(request, 'campaign/index.html', context)


def publications_json(request):
    qs = Publication.objects.all()

    category = request.GET.get('category', '').strip().lower()
    if category and category != 'all':
        qs = qs.filter(category=category)

    q = request.GET.get('q', '').strip()
    if q:
        from django.db.models import Q
        qs = qs.filter(
            Q(title__icontains=q) | Q(summary__icontains=q) | Q(institution__icontains=q)
        )

    data = [
        {
            'id': p.pk,
            'title': p.title,
            'category': p.category,
            'category_label': p.get_category_display(),
            'year': p.year,
            'institution': p.institution,
            'summary': p.summary,
            'cover': p.cover_url(),
            'pdf_url': p.pdf_url,
            'is_featured': p.is_featured,
        }
        for p in qs[:30]
    ]
    return JsonResponse({'publications': data})
