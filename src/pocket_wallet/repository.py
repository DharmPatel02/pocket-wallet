from pocket_wallet.schemas import Wallet 
import uuid

class InMemoryWalletRepository:
    def __init__(self):
        self.wallets: dict[str, Wallet] = {} 

    def create(self, owner: str) -> Wallet:
        wallet = Wallet(id=str(uuid.uuid4()), owner=owner, balance_cents=0)
        self.wallets[wallet.id] = wallet
        return wallet 
    
    def get(self, wallet_id: str) -> Wallet | None:
        return self.wallets.get(wallet_id)
    
    def save(self, wallet: Wallet) -> None:
        self.wallets[wallet.id] = wallet    
    
