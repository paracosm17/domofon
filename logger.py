import logging
import betterlogging as bl

logger = logging.getLogger(__name__)
log_level = logging.WARNING
bl.basic_colorized_config(level=log_level)
logging.basicConfig(
    level=logging.INFO,
    format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
)
