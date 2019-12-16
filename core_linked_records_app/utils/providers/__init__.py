""" Handle system abstract class
"""
from abc import ABC, abstractmethod


class AbstractIdProvider(ABC):
    def __init__(self, base_url, cdcs_base_url, username, password):
        self.provider_url = base_url
        self.local_url = cdcs_base_url
        self.auth_token = self.encode_token(username, password)

    @abstractmethod
    def encode_token(self, username, password):
        raise NotImplementedError()

    @abstractmethod
    def get(self, record):
        raise NotImplementedError()

    @abstractmethod
    def create(self, prefix, record=None):
        raise NotImplementedError()

    @abstractmethod
    def update(self, record):
        raise NotImplementedError()

    @abstractmethod
    def delete(self, record):
        raise NotImplementedError()
