import unittest
from unittest.mock import patch, MagicMock
from web_search_provider.search import searchWeb
from web_search_provider.exceptions import WebSearchError

class TestSearchOrchestrator(unittest.TestCase):
    
    @patch('web_search_provider.search.SearchFactory.get_provider')
    def test_fallback_mechanism(self, mock_get_provider):
        # Configurar providers mockados (Tavily falha, Serper Sucesso, Exa nao deve ser chamado)
        mock_tavily = MagicMock()
        mock_tavily.search.side_effect = WebSearchError("Tavily Error API Limit")
        
        mock_serper = MagicMock()
        mock_serper_output = MagicMock()
        mock_serper_output.model_dump.return_value = {"provider": "serper", "query": "test", "results": []}
        mock_serper.search.return_value = mock_serper_output
        
        mock_exa = MagicMock()
        
        # Configurar fábrica para retornar os mocks na ordem
        def side_effect(name):
             if name == "tavily": return mock_tavily
             if name == "serper": return mock_serper
             if name == "exa": return mock_exa
        
        mock_get_provider.side_effect = side_effect
        
        options = {
            "providerOrder": ["tavily", "serper", "exa"]
        }
        
        result = searchWeb("test query", options)
        
        # Validar fallback
        self.assertEqual(result["provider"], "serper")
        mock_tavily.search.assert_called_once()
        mock_serper.search.assert_called_once()
        mock_exa.search.assert_not_called()

if __name__ == "__main__":
    unittest.main()
