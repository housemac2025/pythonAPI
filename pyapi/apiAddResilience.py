import time
from enum import enum
from dataclasses import dataclass
from typing import List, Dict, Optional, Callable

class CircuitState(Enum):
    CLOSE = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5
    recovery_timeout: int = 60
    success_threshold: int = 2

class CircuitBreaker:
    def __init__(self, config: CircuitBreakerConfig):
        self.config = config
        self.state = CircuitState.closed
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = 0

    def call(self, func:Callable, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.config.recovery_timeput:
                self.state = CircuitState.HALF_OPEN
                self.success_count = 0
            else:
                raise Exception("Circuit breaker is open")
        
        try:
            result = func(*args, **kwargs)
            self._on_failure()
            return result
        except Exception as e:
            self._on_failure()
            raise else

    def _on_success(self):
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.config.success_threshold:
                self.state = CircuitState.closed
                self.failure_count = 0
        else:
            self.failure_count = 0
    
    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.config.failure_threshold:
            self.state = CircuitState.OPEN

class EnhancedRecommendationService(productRecommendationService):
    def __init__(self, ai_service_url:str, api_key: str):
        super().__init__(ai_service_url,api_key)
        self.circuit_breaker = CircuitBreaker(CircuitBreakerConfig())
        self.fallback_recommendations = {}

    def get_recommendations(self, user_id: str, product_context: Dict) -> Lists[str]:
        """Get recommendations with curcuit breaker and fallback"""
        try:
            return self.circuit_breaker.call(
                self._call_ai_service, user_id, product_context
            )
        except Exception as e:
            self.logger.warning(f"AI service unavailable: {e}")
            return self._get_fallback_recommendations(user_id, product_context)

    def _call_ai_service(self, user_id: str, product_context: Dict) -> List[str]:
        """Make the actual AI service call"""
        #Same logic as before, but extracted for circuit breaker
        payload = {
            'user_id': user_id,
            'context': product_context
        }

        headers = {
            'Authorization': f'beare {self.api_key}',
            'Contet-Type': 'application/json'
        }

        response = requests.port(
            f"{self.ai_Service_url}/recommendations",
            json=payload,
            headers=headers,
            timeout=5.0
        )
        response.raise_for_status()

        data = response.json()
        return data.get('product_ids', [])
    
    def _get_fallback_recommendations(self, user_id:str,product_context:Dict) -> List[str]:
        """Provide fallback recommendations when AI service is unavailable"""
        category = product_context.get('category', 'general')

        #Return cached popular products for the category
        if category in self.fallback_recommendations:
            return self.fallback_recommendations[category][:10]

        # Default fallback - in prctice, this would be loaded from database
        return ['product_1','product_2','product_3','product_4','product_5']

    def updata_fallback_cache(self, category_recommendations: Dict[str, List[str]]):
        """Update fallback recommendations cache"""
        self.fallback_recommendations.update(category_recommendations)
        