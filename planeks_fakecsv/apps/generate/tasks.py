"""
This module provides with `generate` app's tasks for `celery`

Functions:
    - update_csv: shared `celery` task
"""

from celery import shared_task

from .models import DataSet


@shared_task
def update_csv(dset_id: int, *, num_rows: int):
    """
    Update csv in data set.

    Args:
        dset_id (int): id of data set
        num_rows (int): number of rows of CSV file
    """
    dset = DataSet.objects.get(id=dset_id)
    dset.update_csv(num_rows=num_rows)
    dset.save()
