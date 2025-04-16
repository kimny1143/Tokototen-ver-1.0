from celery import Celery

celery_app = Celery(
    "tokoroten",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
    include=[
        "app.tasks.audio_analysis",
        "app.tasks.source_separation",
        "app.tasks.transcription",
        "app.tasks.ai_analysis_reporting",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)
