import os
import sys
import pytest
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from SentimentModel import SentimentAnalyzerModel


@pytest.fixture
def model():
    return SentimentAnalyzerModel()


def test_analyze_output(model):
    label, score = model.analyze("To był świetny film!")
    assert isinstance(label, str)
    assert isinstance(score, float)
    assert 0.0 <= score <= 1.0


def test_analyze_mocked_label_and_score():
    with patch('SentimentModel.pipeline') as mock_pipeline:
        mock_pipeline.return_value = lambda text: [
            {
                'label': 'Positive',
                'score': 0.99
            }
        ]
        model = SentimentAnalyzerModel()
        label, score = model.analyze("Test")
        assert label == 'Positive'
        assert score == 0.99


@pytest.mark.parametrize("mock_label, mock_score", [
    ("Positive", 0.8),
    ("Negative", 0.1),
    ("Neutral", 0.5),
])
def test_analyze_mocked_various(mock_label, mock_score):
    with patch('SentimentModel.pipeline') as mock_pipeline:
        mock_pipeline.return_value = lambda text: [
            {
                'label': mock_label,
                'score': mock_score
            }
        ]
        model = SentimentAnalyzerModel()
        label, score = model.analyze("Dowolny tekst")
        assert label == mock_label
        assert score == mock_score
