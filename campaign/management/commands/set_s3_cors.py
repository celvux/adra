"""Management command: configure CORS on the Supabase S3 bucket.

Run once after deployment:
    python manage.py set_s3_cors
"""
from django.core.management.base import BaseCommand
from django.conf import settings


CORS_RULES = [
    {
        'AllowedHeaders': ['Content-Type'],
        'AllowedMethods': ['PUT', 'GET'],
        'AllowedOrigins': [
            'https://*.vercel.app',
            'https://adradiallo.frondeg.co',
            'http://localhost:*',
            'http://127.0.0.1:*',
        ],
        'MaxAgeSeconds': 3600,
        'ExposeHeaders': ['ETag'],
    }
]


class Command(BaseCommand):
    help = 'Configure S3 CORS on the Supabase bucket for direct browser uploads.'

    def handle(self, *args, **options):
        if not getattr(settings, 'USE_S3', False):
            self.stderr.write(self.style.WARNING('USE_S3 is False — nothing to do.'))
            return

        import boto3
        from botocore.exceptions import ClientError

        client = boto3.client(
            's3',
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
        )

        bucket = settings.AWS_STORAGE_BUCKET_NAME
        try:
            client.put_bucket_cors(
                Bucket=bucket,
                CORSConfiguration={'CORSRules': CORS_RULES},
            )
            self.stdout.write(self.style.SUCCESS(
                f'CORS configured on bucket "{bucket}".'
            ))
        except ClientError as exc:
            code = exc.response['Error']['Code']
            self.stderr.write(self.style.ERROR(
                f'S3 API returned "{code}". '
                'Supabase may not support PutBucketCors via the S3 API.\n'
                'Configure CORS manually in the Supabase dashboard:\n'
                '  Storage → Policies → Edit CORS\n'
                '  Allowed origins: https://*.vercel.app  https://adradiallo.frondeg.co  http://localhost:*\n'
                '  Allowed methods: PUT GET\n'
                '  Allowed headers: Content-Type'
            ))
