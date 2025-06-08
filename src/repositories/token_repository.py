from typing import Optional, List
from datetime import datetime, timezone

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import RefreshToken

class RefreshTokenRepository:
    async def create(
        self,
        session: AsyncSession,
        token: str,
        user_id: int,
        expires_at: datetime,
        is_revoked: bool = False
    ) -> RefreshToken:
        refresh_token = RefreshToken(
            token=token,
            user_id=user_id,
            expires_at=expires_at,
            is_revoked=is_revoked,
        )
        session.add(refresh_token)
        await session.commit()
        await session.refresh(refresh_token)
        return refresh_token

    async def get_by_token(
        self,
        session: AsyncSession,
        token: str,
        active_only: bool = True
    ) -> Optional[RefreshToken]:
        stmt = select(RefreshToken).where(RefreshToken.token == token)
        if active_only:
            stmt = stmt.where(RefreshToken.is_revoked == False)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def revoke(
        self,
        session: AsyncSession,
        token: str
    ) -> bool:
        refresh_token = await self.get_by_token(session, token, active_only=True)
        if not refresh_token:
            return False
        refresh_token.is_revoked = True
        await session.commit()
        await session.refresh(refresh_token)
        return True
