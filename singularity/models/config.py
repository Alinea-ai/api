from typing import Any

from pydantic import BaseModel
from pynamodb.attributes import ListAttribute, MapAttribute, NumberAttribute, UnicodeAttribute
from pynamodb.models import Model

from src.common.types import DatabaseType


class Config(BaseModel):
    username: str
    password: str
    host: str
    database_name: str
    port: int
    type: DatabaseType
    alias: str
    description: str = ''

    @staticmethod
    def get_driver(db_type: DatabaseType) -> str:
        """Map database type to the appropriate driver."""
        drivers = {
            DatabaseType.postgresql: 'postgresql+psycopg2',
            DatabaseType.mysql: 'mysql+pymysql',
        }
        return drivers.get(db_type, 'postgresql+psycopg2')

    def get_database_uri(self) -> str:
        """Generate the database URI based on the config."""
        driver = self.get_driver(self.type)
        return f'{driver}://{self.username}:{self.password}@{self.host}:' f'{self.port}/{self.database_name}'

    @classmethod
    def from_config_map(cls, config_map: Any) -> 'Config':
        config = cls(
            username=config_map.username,
            password=config_map.password,
            host=config_map.host,
            database_name=config_map.database_name,
            port=config_map.port,
            type=config_map.type,
            alias=config_map.alias,
            description=config_map.description,
        )
        return config


class ConfigMap(MapAttribute):
    username = UnicodeAttribute()
    password = UnicodeAttribute()
    host = UnicodeAttribute()
    database_name = UnicodeAttribute()
    port = NumberAttribute()
    type = UnicodeAttribute()
    alias = UnicodeAttribute()
    description = UnicodeAttribute()


class MerchantConfig(Model):
    class Meta:
        table_name = 'MerchantsConfigs'
        region = 'us-west-2'

    uid = UnicodeAttribute(hash_key=True)
    version = NumberAttribute(default=1)
    name = UnicodeAttribute()
    db_configs = ListAttribute(of=ConfigMap)


class SingularityConfig(Model):
    class Meta:
        table_name = 'SingularityConfig'
        region = 'us-west-2'

    uid = UnicodeAttribute(hash_key=True)
    version = NumberAttribute(default=1)
    settings = MapAttribute()


class AlignedConfig(Model):
    class Meta:
        table_name = 'AlignedConfig'
        region = 'us-west-2'

    id = UnicodeAttribute(hash_key=True)
    version = NumberAttribute(default=1)
    settings = MapAttribute()


class TestSingularityConfig:
    class Settings:
        OPEN_AI_KEY = 'test-open-ai-key'

    uid = 'test-uid'
    version = '1'
    settings = Settings


class TestMerchantConfig:
    class Meta:
        table_name = 'MerchantsConfigs'
        region = 'us-west-2'

    uid = 'test-uid'
    version = '1'
    name = 'test-name'
    db_configs = []
