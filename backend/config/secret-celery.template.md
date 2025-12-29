# .secrets.celery.yaml Template

Use este template para criar o arquivo de segredos do Celery. Preencha os campos entre < > conforme o ambiente.

## Estrutura do arquivo

```yaml
default:
  SECRET_KEY: "<sua_secret_key_aqui>"
  DATABASE_URI: "postgresql+pg8000://<usuario>:<senha>@<host>:<porta>/<database>"

  # Flask-Mail
  MAIL_SERVER: "<mail_server>"
  MAIL_PORT: <porta>
  MAIL_USE_TLS: <true_ou_false>
  MAIL_USE_SSL: <true_ou_false>
  MAIL_USERNAME: "<usuario_email>"
  MAIL_PASSWORD: "<senha_email>"
  MAIL_DEBUG: true
  MAIL_DEFAULT_SENDER: "<remetente_email>"
  MAIL_MAX_EMAILS: 5
  MAIL_SUPPRESS_SEND: false
  MAIL_ASCII_ATTACHMENTS: true

  # Redis / Celery
  BROKER_URL: "redis://:<senha>@<host>:<porta>/<db>"
  RESULT_BACKEND: "redis://:<senha>@<host>:<porta>/<db>"
  REDIS_PASSWORD: "<senha_redis>"

  # MinIO
  MINIO_ENDPOINT: "<minio_host>:<minio_porta>"
  MINIO_ACCESS_KEY: "<minio_access_key>"
  MINIO_SECRET_KEY: "<minio_secret_key>"
  MINIO_BUCKET_NAME: "<minio_bucket>"

  SQLALCHEMY_DATABASE_URI: "@format {this.DATABASE_URI}"
  API_URL: "<api_url>"
  WEB_URL: "<web_url>"
```

---

## Dicas

- Use nomes claros para variáveis e domínios.
- Não compartilhe este arquivo publicamente.
- Consulte a documentação do projeto para mais detalhes sobre cada campo.
