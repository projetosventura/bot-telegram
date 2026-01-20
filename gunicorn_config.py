"""
Configuração do Gunicorn para deploy em produção do webhook
"""
import multiprocessing

# Bind
bind = "0.0.0.0:5000"

# Workers
workers = multiprocessing.cpu_count() * 2 + 1

# Logging
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = "info"

# Timeout
timeout = 120
