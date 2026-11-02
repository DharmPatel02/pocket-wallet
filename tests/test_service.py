import pytest

from pocket_wallet.errors import InsufficientFunds, SameWalletTransfer
from pocket_wallet.repository import InMemoryWalletRepository
from pocket_wallet.service import WalletService

@pytest.fixture
def service():
    repo = InMemoryWalletRepository()          # make a new empty repository
    return WalletService(repo)          # build a WalletService with that repo

def test_deposit_increases_balance(service):
    wallet = service.create_wallet("alice")
    service.deposit(wallet.id, 500)
    assert service.get_wallet(wallet.id).balance_cents == 500