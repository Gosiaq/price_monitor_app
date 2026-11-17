# products/tasks.py
import subprocess
import logging
from celery import shared_task

logger = logging.getLogger(__name__)

@shared_task(name="run_spider_task")
def run_spider(spider_name="shop_spider", category="all"):
    work_dir = "/app"
    """
    Zadanie Celery uruchamiające pająka Scrapy.
    """
    logger.info(f"Rozpoczynanie zadania scrapingu dla: {spider_name}")

    try:
        subprocess.run(
            ["scrapy", "crawl", spider_name, "-a", f"category={category}"],
            check=True,
            stdout=None,
            stderr=None,
            cwd=work_dir
        )
        logger.info(f"Zadanie {spider_name} zakończone sukcesem.")
        return f"Sukces: Pająk {spider_name} zakończył pracę."

    except subprocess.CalledProcessError as e:
        logger.error(f"Błąd podczas pracy pająka: {e.stderr}")
        return f"Błąd: {e.stderr}"