from pydantic import BaseModel,Field

class Wallet(BaseModel):
    id: str
    owner: str
    balance_cents: int

class CreateWalletRequest(BaseModel):
    owner: str

class AmountRequest(BaseModel):
    amount_cents: int = Field(gt=0)

class TransferRequest(BaseModel):
    from_id: str
    to_id: str
    amount_cents: int = Field(gt=0)
    

    