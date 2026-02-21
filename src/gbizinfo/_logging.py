"""ロガー定義。"""

import logging

logger = logging.getLogger("gbizinfo")
logger.addHandler(logging.NullHandler())
