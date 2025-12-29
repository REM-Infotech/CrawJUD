# .secrets.flask.yaml Template

Use este template para criar o arquivo de segredos do Flask. Preencha os campos entre < > conforme o ambiente.

## Estrutura do arquivo

```yaml
default:
  SECRET_KEY: "<sua_secret_key_aqui>"
  APP_DOMAIN: "<dominio_da_aplicacao>"
  DATABASE_URI: "postgresql+pg8000://<usuario>:<senha>@<host>:<porta>/<database>"
  TRUSTED_HOSTS:
    - localhost
    - 127.0.0.1
    - <outros_hosts_confiaveis>

  # JWT
  JWT_ACCESS_TOKEN_EXPIRES: 86400
  JWT_CSRF_IN_COOKIES: true
  JWT_COOKIE_SECURE: true
  JWT_ACCESS_COOKIE_NAME: "access_token_cookie"
  JWT_COOKIE_DOMAIN: "@format {this.APP_DOMAIN}"
  JWT_COOKIE_SAMESITE: None
  JWT_ACCESS_CSRF_COOKIE_NAME: "x-xsrf-token"
  JWT_ACCESS_CSRF_HEADER_NAME: "x-xsrf-token"
  JWT_TOKEN_LOCATION:
    - "cookies"
    - "headers"

  # Flask-Mail
  MAIL_SERVER: "<mail_server>"
  MAIL_PORT: 587
  MAIL_USE_TLS: true
  MAIL_USE_SSL: false
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

  # Usuário root
  ROOT_DISPLAY_NAME: "<nome_root>"
  ROOT_USERNAME: "<usuario_root>"
  ROOT_PASSWORD: "<senha_root>"
  ROOT_EMAIL: "<email_root>"
  ROOT_CLIENT: "<cliente_root>"
  ROOT_CPF_CNPJ_CLIENT: "<cpf_cnpj_cliente>"

  # MinIO
  MINIO_ENDPOINT: "<minio_host>:<minio_porta>"
  MINIO_ACCESS_KEY: "<minio_access_key>"
  MINIO_SECRET_KEY: "<minio_secret_key>"
  MINIO_BUCKET_NAME: "<minio_bucket>"

  SQLALCHEMY_DATABASE_URI: "@format {this.DATABASE_URI}"
  SESSION_SQLALCHEMY: "@format {this.DATABASE_URI}"
  SESSION_COOKIE_DOMAIN: "@format {this.APP_DOMAIN}"

  # CORS
  CORS_ORIGINS:
    - "https://<frontend>"
    - "localhost"
    - "http://localhost:3000"
    - "http://localhost:5173"
    - "http://127.0.0.1:1473"
    - "http://localhost:1474"
    - "https://<outro_frontend>"
```

---

## Dicas

- Use nomes claros para variáveis e domínios.
- Não compartilhe este arquivo publicamente.
- Consulte a documentação do projeto para mais detalhes sobre cada campo.
