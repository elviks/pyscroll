"""PyScroll feed package: one module per category, each numbering its tips from 1."""

from .python_core_feed import TIPS as PYTHON_CORE_FEED_TIPS
from .django_feed import TIPS as DJANGO_FEED_TIPS
from .fast_api_feed import TIPS as FAST_API_FEED_TIPS
from .flask_feed import TIPS as FLASK_FEED_TIPS
from .pytorch_feed import TIPS as PYTORCH_FEED_TIPS
from .tensor_flow_feed import TIPS as TENSORFLOW_TIPS
from .scikit_learn_feed import TIPS as SCIKIT_LEARN_TIPS
from .pandas_feed import TIPS as PANDAS_FEED_TIPS
from .numpy_feed import TIPS as NUMPY_FEED_TIPS
from .scrapy_feed import TIPS as SCRAPY_FEED_TIPS
from .requests_httpx_feed import TIPS as REQUESTS_HTTPX_FEED_TIPS
from .sqlalchemy_feed import TIPS as SQLALCHEMY_FEED_TIPS
from .pytest_feed import TIPS as PYTEST_TIPS
from .asyncio_feed import TIPS as ASYNCIO_TIPS
from .celery_feed import TIPS as CELERY_TIPS
from .airflow_feed import TIPS as AIRFLOW_TIPS
from .pydantic_feed import TIPS as PYDANTIC_TIPS
from .streamlit_feed import TIPS as STREAMLIT_TIPS

ALLOCATION = (
    (PYTHON_CORE_FEED_TIPS, (1, 121)),
    (DJANGO_FEED_TIPS, (121, 146)),
    (FAST_API_FEED_TIPS, (146, 171)),
    (FLASK_FEED_TIPS, (171, 221)),
    (PYTORCH_FEED_TIPS, (221, 271)),
    (TENSORFLOW_TIPS, (271, 321)),
    (SCIKIT_LEARN_TIPS, (321, 371)),
    (PANDAS_FEED_TIPS, (371, 421)),
    (NUMPY_FEED_TIPS[0:40], (421, 461)),
    (SCRAPY_FEED_TIPS[0:30], (461, 491)),
    (REQUESTS_HTTPX_FEED_TIPS[0:30], (491, 521)),
    (NUMPY_FEED_TIPS[40:50], (521, 531)),
    (SCRAPY_FEED_TIPS[30:50], (531, 551)),
    (REQUESTS_HTTPX_FEED_TIPS[30:50], (551, 571)),
    (SQLALCHEMY_FEED_TIPS, (571, 621)),
    (PYTEST_TIPS, (621, 671)),
    (ASYNCIO_TIPS, (671, 721)),
    (CELERY_TIPS, (721, 771)),
    (AIRFLOW_TIPS, (771, 821)),
    (PYDANTIC_TIPS, (821, 871)),
    (STREAMLIT_TIPS, (871, 921)),
)

def _aggregate():
    result = []
    for part, (start, end) in ALLOCATION:
        assert len(part) == end - start, (start, end, len(part))
        for tip, gid in zip(part, range(start, end)):
            merged = dict(tip)
            merged["id"] = gid
            result.append(merged)
    return result

TIPS = _aggregate()
