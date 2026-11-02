from pocket_wallet.errors import InsufficientFunds, SameWalletTransfer, WalletNotFound
from pocket_wallet.schemas import Wallet

class WalletService:
    def __init__(self, repo):
        self.repo = repo

    def create_wallet(self, owner: str) -> Wallet:
        return self.repo.create(owner)

    def get_wallet(self, wallet_id: str) -> Wallet:
        wallet = self.repo.get(wallet_id)
        if wallet is None:
            raise WalletNotFound(wallet_id)
        return wallet

    def deposit(self, wallet_id: str, amount_cents: int) -> Wallet:
        wallet = self.get_wallet(wallet_id)
        wallet.balance_cents += amount_cents
        self.repo.save(wallet)
        return wallet

    def withdraw(self, wallet_id: str, amount_cents: int) -> Wallet:
        wallet = self.get_wallet(wallet_id)
        if wallet.balance_cents < amount_cents:
            raise InsufficientFunds(wallet_id)
        wallet.balance_cents -= amount_cents
        self.repo.save(wallet)
        return wallet

    def transfer(self, from_id: str, to_id: str, amount_cents: int) -> None:
        if from_id == to_id:
            raise SameWalletTransfer(from_id)
        sender = self.get_wallet(from_id)
        receiver = self.get_wallet(to_id)
        if sender.balance_cents < amount_cents:
            raise InsufficientFunds(from_id)
        sender.balance_cents -= amount_cents
        receiver.balance_cents += amount_cents
        self.repo.save(sender)
        self.repo.save(receiver)