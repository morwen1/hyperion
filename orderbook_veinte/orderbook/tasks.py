from celery.task import task
from config import celery_app


@celery_app.task()
def AsincronicOrderProces (ob,order):
    ob.processOrder(order)

    