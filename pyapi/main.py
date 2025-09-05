import requests
import typing import List, Dict, Optional
import logging

class ProductRecommendationService:
    def __init__(self, ai_service_url: str, api_key: str):
        self.ai_service_url = ai_service_url
        self.api_key = api_key
        self.logger = loggin.getLogger(__name__)

    def get_recommendations(self, user_id: str, product_context: Dict)-> Lists[str]:
        """Get product recommendations for a user"""
        payload = {
            'user_id': user_id,
            'context': product_context
        }

        headers = {
            'Authorization': f'Bearer { self.api_key}',
            'content-Type': 'application/json'
        }

        try:
            response = requests.post(
                f"{self.ai_service_url}/recommendations",
                json=payload,
                headers=headers,
                timeout=5.0
            )
            response.raise_for_status()

            data = response.json()
            return data.get('product_ids', [])
        except Exception as e:
            self.logger.error(f"AI service call failed: {e}")
            return []
