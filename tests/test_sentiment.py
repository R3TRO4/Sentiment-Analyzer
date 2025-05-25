import sys
import os
import pytest
from unittest.mock import patch
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from SentimentModel import SentimentAnalyzerModel


@pytest.fixture(scope="module")
def model():
    return SentimentAnalyzerModel()


def test_analyze_output_real_model(model):
    label, score = model.analyze("To był fantastyczny film!")
    assert (label in
            ["Very Positive",
             "Positive",
             "Neutral",
             "Negative",
             "Very Negative"])
    assert isinstance(score, float)


@pytest.mark.parametrize("text, expected_labels", [
    ("To był fantastyczny film!",
     ["Very Positive",
      "Positive",
      "Neutral",
      "Negative",
      "Very Negative"]),
    ("To był okropny film!",
     ["Very Positive",
      "Positive",
      "Neutral",
      "Negative",
      "Very Negative"]),
    ("",
     ["Very Positive",
      "Positive",
      "Neutral",
      "Negative",
      "Very Negative"]),  # puste wejście
])
def test_analyze_various_texts_real_model(model, text, expected_labels):
    label, score = model.analyze(text)
    assert label in expected_labels
    assert isinstance(score, float)


def test_score_range_real_model(model):
    label, score = model.analyze("Średni film.")
    assert 0.0 <= score <= 1.0


def test_analyze_mocked():
    # Mockujemy pipeline, aby zwracał zdefiniowany wynik
    with patch('SentimentModel.pipeline') as mock_pipeline:
        mock_pipeline.return_value = lambda text: [{'label': 'Positive',
                                                    'score': 0.99}]
        model = SentimentAnalyzerModel()
        label, score = model.analyze("Cokolwiek")
        assert label == "Positive"
        assert score == 0.99


@pytest.mark.parametrize("mock_label, mock_score", [
    ("Very Positive", 0.95),
    ("Neutral", 0.5),
    ("Negative", 0.1),
])
def test_analyze_mocked_various_outputs(mock_label, mock_score):
    with patch('SentimentModel.pipeline') as mock_pipeline:
        mock_pipeline.return_value = lambda text: [{'label': mock_label,
                                                    'score': mock_score}]
        model = SentimentAnalyzerModel()
        label, score = model.analyze("Test")
        assert label == mock_label
        assert score == mock_score
