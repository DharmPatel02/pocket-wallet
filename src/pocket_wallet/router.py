from fastapi import APIRouter, Depends, HTTPException

from pocket_wallet.errors import InsufficientFunds, SameWalletTransfer, WalletNotFound
from pocket_wallet.repository import InMemoryWalletRepository
from pocket_wallet.schemas import AmountRequest, CreateWalletRequest, TransferRequest, Wallet
from pocket_wallet.service import WalletService

router = APIRouter()

_repo = InMemoryWalletRepository()


def get_service() -> WalletService:
    return WalletService(_repo)


@router.post("/wallets", status_code=201)
def create_wallet(body: CreateWalletRequest, service: WalletService = Depends(get_service)) -> Wallet:
    return service.create_wallet(body.owner)


@router.get("/wallets/{wallet_id}")
def get_wallet(wallet_id: str, service: WalletService = Depends(get_service)) -> Wallet:
    try:
        return service.get_wallet(wallet_id)
    except WalletNotFound:
        raise HTTPException(status_code=404, detail="Wallet not found")


@router.post("/wallets/{wallet_id}/deposit")
def deposit(wallet_id: str, body: AmountRequest, service: WalletService = Depends(get_service)) -> Wallet:
    try:
        return service.deposit(wallet_id, body.amount_cents)
    except WalletNotFound:
        raise HTTPException(status_code=404, detail="Wallet not found")


@router.post("/wallets/{wallet_id}/withdraw")
def withdraw(wallet_id: str, body: AmountRequest, service: WalletService = Depends(get_service)) -> Wallet:
    try:
        return service.withdraw(wallet_id, body.amount_cents)
    except WalletNotFound:
        raise HTTPException(status_code=404, detail="Wallet not found")
    except InsufficientFunds:
        raise HTTPException(status_code=422, detail="Insufficient funds")


@router.post("/transfers")
def transfer(body: TransferRequest, service: WalletService = Depends(get_service)) -> dict:
    try:
        service.transfer(body.from_id, body.to_id, body.amount_cents)
    except WalletNotFound:
        raise HTTPException(status_code=404, detail="Wallet not found")
    except InsufficientFunds:
        raise HTTPException(status_code=422, detail="Insufficient funds")
    except SameWalletTransfer:
        raise HTTPException(status_code=422, detail="Cannot transfer to the same wallet")
    return {"status": "ok"}