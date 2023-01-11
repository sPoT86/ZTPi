import os
import ruamel.yaml


with open("config.yaml", "r") as f:
    yml = ruamel.yaml.YAML(typ="rt", pure=True)
    _cfg = yml.load(f)


STAGING_BN = os.environ.get('ZTP_STAGING_BN') or _cfg.get('staging_bn')
STAGING_PW = os.environ.get('ZTP_STAGING_PW') or _cfg.get('staging_pw')
STAGING_DOMAIN = os.environ.get('ZTP_STAGING_DOMAIN') or _cfg.get('staging_domain')
TFTP_ROOT = os.environ.get('TFTP_ROOT') or _cfg.get('tftp_root')
KEYSTORE = os.environ.get('ZTP_KEYSTORE') or _cfg.get('keystore')
TEMPLATE_DIR = os.environ.get('ZTP_TEMPLATES') or _cfg.get('templates_dir')
CACHE_DIR = os.environ.get('ZTP_CACHE_DIR') or _cfg.get('cache_dir')
CONFIG_DIR = os.environ.get('ZTP_CONFIGS_DIR') or _cfg.get('configs_dir')
LOG_DIR = os.environ.get('ZTP_LOG_DIR') or _cfg.get('log_dir')
LOG_FILENAME = os.environ.get('ZTP_LOG_FILENAME') or _cfg.get('log_filename')
REDIS_SERVER = os.environ.get('ZTP_REDIS_SERVER') or _cfg.get('redis_server')
