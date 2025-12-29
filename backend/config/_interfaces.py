from __future__ import annotations

from typing import TYPE_CHECKING, Literal, TypedDict, Unpack

type Any = any

if TYPE_CHECKING:
    from dynaconf.contrib import DynaconfConfig


class _CeleryDefaults(TypedDict):
    accept_content: Literal["json"]
    result_accept_content: Any
    enable_utc: True
    imports: tuple[str, ...]
    include: tuple[str, ...]
    timezone: Any
    beat_max_loop_interval: 0
    beat_schedule: dict
    beat_scheduler: Literal["celery.beat:PersistentScheduler"]
    beat_schedule_filename: Literal["celerybeat-schedule"]
    beat_sync_every: 0
    beat_cron_starting_deadline: Any
    broker_url: Any
    broker_read_url: Any
    broker_write_url: Any
    broker_transport: Any
    broker_transport_options: dict
    broker_connection_timeout: 4
    broker_connection_retry: True
    broker_connection_retry_on_startup: Any
    broker_connection_max_retries: 100
    broker_channel_error_retry: False
    broker_failover_strategy: Any
    broker_heartbeat: 120
    broker_heartbeat_checkrate: 3.0
    broker_login_method: Any
    broker_native_delayed_delivery_queue_type: Literal["quorum"]
    broker_pool_limit: 10
    broker_use_ssl: False
    broker_host: Any
    broker_port: Any
    broker_user: Any
    broker_password: Any
    broker_vhost: Any
    cache_backend: Any
    cache_backend_options: dict
    cassandra_entry_ttl: Any
    cassandra_keyspace: Any
    cassandra_port: Any
    cassandra_read_consistency: Any
    cassandra_servers: Any
    cassandra_bundle_path: Any
    cassandra_table: Any
    cassandra_write_consistency: Any
    cassandra_auth_provider: Any
    cassandra_auth_kwargs: Any
    cassandra_options: dict
    s3_access_key_id: Any
    s3_secret_access_key: Any
    s3_bucket: Any
    s3_base_path: Any
    s3_endpoint_url: Any
    s3_region: Any
    azureblockblob_container_name: Literal["celery"]
    azureblockblob_retry_initial_backoff_sec: 2
    azureblockblob_retry_increment_base: 2
    azureblockblob_retry_max_attempts: 3
    azureblockblob_base_path: str
    azureblockblob_connection_timeout: 20


class CeleryConfig:
    """Configure variáveis do celery dinamicamente."""

    def __init__(
        self,
        values: DynaconfConfig,
        **kwargs: Unpack[_CeleryDefaults],
    ) -> None:
        """Inicialize a configuração do celery com valores dinâmicos.

        Args:
            values (DynaconfConfig): Configurações dinâmicas.
            **kwargs (_CeleryDefaults): Configurações padrão do celery.

        """
        for k, v in list(values.items()):
            if str(k).isupper():
                setattr(self, k.lower(), v)

        self.worker_hijack_root_logger = False
