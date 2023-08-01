from . import logging
import config
import os


cogs = [f[:-3] for f in os.listdir(f"{config.Cogs_Dir}") if f.endswith('.py')]

