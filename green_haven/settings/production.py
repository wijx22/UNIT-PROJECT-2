from .base import DEBUG, MIDDLEWARE, env

if not DEBUG:
    ADMINS = [
        ("Admin", env("ADMIN_EMAIL") ),
    ]
      
    STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
    MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

    # Cloudinary Settings For Media Files
    CLOUDINARY_STORAGE = {
        "CLOUD_NAME": env("CLOUD_NAME"),
        "API_KEY": env("API_KEY"),
        "API_SECRET": env("API_SECRET"),
    }
    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
