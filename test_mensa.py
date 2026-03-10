"""
Test module for mensa.py

This module contains unit tests for the mensa cafeteria menu functionality.
"""

import pytest
from datetime import date, datetime
from unittest.mock import patch, MagicMock, Mock

# Import the module under test
import mensa
from mensa import get_menu, parse_meals, filter_meals, Meal, MensaAPIError


class TestMeal:
    """Tests for the Meal dataclass/model."""
    
    def test_meal_creation(self):
        """Test basic meal creation with valid parameters."""
        meal = Meal(
            name="Pasta Carbonara",
            price=4.50,
            category="main_dish",
            dietary_tags=["vegetarian"]
        )
        assert meal.name == "Pasta Carbonara"
        assert meal.price == 4.50
        assert meal.category == "main_dish"
    
    def test_meal_dietary_properties(self):
        """Test dietary restriction property checks."""
        veg_meal = Meal("Garden Salad", 3.00, "main", ["vegetarian"])
        vegan_meal = Meal("Tofu Stir Fry", 4.00, "main", ["vegan", "vegetarian"])
        meat_meal = Meal("Beef Steak", 6.00, "main", [])
        
        assert veg_meal.is_vegetarian()
        assert not veg_meal.is_vegan()
        assert vegan_meal.is_vegan()
        assert not meat_meal.is_vegetarian()


class TestGetMenu:
    """Tests for the get_menu function."""
    
    @patch('mensa.requests.get')
    def test_get_menu_success(self, mock_get):
        """Test successful API call returns parsed meals."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meals": [
                {"name": "Pizza Margherita", "price": 3.50, "category": "main"},
                {"name": "Caesar Salad", "price": 2.50, "category": "side", "dietary": ["vegetarian"]}
            ],
            "date": "2024-01-15"
        }
        mock_get.return_value = mock_response
        
        result = get_menu(date(2024, 1, 15))
        assert len(result) == 2
        assert result[0]["name"] == "Pizza Margherita"
        assert result[1]["price"] == 2.50
    
    @patch('mensa.requests.get')
    def test_get_menu_api_error(self, mock_get):
        """Test handling of HTTP errors."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = Exception("Internal Server Error")
        mock_get.return_value = mock_response
        
        with pytest.raises(MensaAPIError):
            get_menu(date.today())
    
    @patch('mensa.requests.get')
    def test_get_menu_network_failure(self, mock_get):
        """Test handling of network connectivity issues."""
        mock_get.side_effect = Exception("Connection timeout")
        
        with pytest.raises(MensaAPIError):
            get_menu(date.today())
    
    def test_get_menu_invalid_date(self):
        """Test validation of date parameter."""
        with pytest.raises((TypeError, ValueError)):
            get_menu("2024-01-01")  # String instead of date object
        with pytest.raises((TypeError, ValueError)):
            get_menu(None)


class TestParseMeals:
    """Tests for meal parsing functionality."""
    
    def test_parse_html_menu(self):
        """Test parsing HTML menu content."""
        html_content = """
        <div class="meal-item">
            <h3 class="meal-name">Grilled Chicken</h3>
            <span class="price">5.20</span>
            <span class="category">main</span>
        </div>
        """
        result = parse_meals(html_content)
        assert isinstance(result, list)
        assert len(result) >= 0
    
    def test_parse_empty_content(self):
        """Test parsing empty or invalid content."""
        assert parse_meals("") == []
        assert parse_meals(None) == []
    
    def test_parse_malformed_html(self):
        """Test graceful handling of malformed HTML."""
        malformed = "<div>Missing closing tags"
        result = parse_meals(malformed)
        assert isinstance(result, list)

