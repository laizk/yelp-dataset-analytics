import os


def get_env(name: str, default: str) -> str:
    value = os.getenv(name, default)
    return value


def kafka_bootstrap() -> str:
    return get_env("KAFKA_BOOTSTRAP_SERVERS", "broker:29092")


def kafka_starting_offsets() -> str:
    return get_env("KAFKA_STARTING_OFFSETS", "latest")


def kafka_max_offsets_per_trigger() -> str:
    return get_env("KAFKA_MAX_OFFSETS_PER_TRIGGER", "")


def kafka_trigger_seconds() -> str:
    return get_env("KAFKA_TRIGGER_SECONDS", "")


def mongo_database() -> str:
    return get_env("MONGO_DB", "yelp")


def checkpoint_path(name: str, default: str) -> str:
    return get_env(name, default)
