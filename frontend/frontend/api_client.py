"""API client for communicating with the backend."""

import httpx
from typing import Dict, List, Optional, Any


class APIClient:
    """Client for communicating with the POS backend API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize API client."""
        self.base_url = base_url
        self.access_token: Optional[str] = None
    
    def set_token(self, token: str):
        """Set the access token for authenticated requests."""
        self.access_token = token
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests."""
        headers = {"Content-Type": "application/json"}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        return headers
    
    async def login(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Login user and return token data."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/auth/login",
                    data={"username": email, "password": password}
                )
                
                if response.status_code == 200:
                    return response.json()
                return None
        except Exception:
            return None
    
    async def get_user_info(self) -> Optional[Dict[str, Any]]:
        """Get current user information."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/auth/me",
                    headers=self._get_headers()
                )
                
                if response.status_code == 200:
                    return response.json()
                return None
        except Exception:
            return None
    
    async def get_products(self) -> List[Dict[str, Any]]:
        """Get list of products."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/products/",
                    headers=self._get_headers()
                )
                
                if response.status_code == 200:
                    return response.json()
                return []
        except Exception:
            return []
    
    async def create_product(self, product_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new product."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/products/",
                    json=product_data,
                    headers=self._get_headers()
                )
                
                if response.status_code == 200:
                    return response.json()
                return None
        except Exception:
            return None
    
    async def get_stock(self) -> List[Dict[str, Any]]:
        """Get list of stock items."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/stock/",
                    headers=self._get_headers()
                )
                
                if response.status_code == 200:
                    return response.json()
                return []
        except Exception:
            return []
    
    async def create_stock(self, stock_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new stock entry."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/stock/",
                    json=stock_data,
                    headers=self._get_headers()
                )
                
                if response.status_code == 200:
                    return response.json()
                return None
        except Exception:
            return None


# Global API client instance
api_client = APIClient() 