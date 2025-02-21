import pytest
import sklearn.metrics
import numpy as np

from confidenceinterval import accuracy_score, \
                               ppv_score, \
                               npv_score, \
                               tpr_score, \
                               fpr_score, \
                               tnr_score, \
                               precision_score, \
                               recall_score, \
                               f1_score, \
                               roc_auc_score
from confidenceinterval.delong import compute_midrank, compute_midrank_weight

@pytest.mark.parametrize("data",
    [ ( [0, 0, 0, 0, 1, 1, 1, 1, 0],
        [0, 0, 1, 0, 1, 0, 1, 1, 0] )])        
def test_accuracy(data):
    y_true, y_pred = data
    sklearn_result = sklearn.metrics.accuracy_score(y_true, y_pred)
    accuracy, ci = accuracy_score(y_true, y_pred)
    assert sklearn_result == accuracy

@pytest.mark.parametrize("data",
    [ ( [0, 0, 0, 0, 1, 1, 1, 1, 0],
        [0, 0, 1, 0, 1, 0, 1, 1, 0] )])
def test_micro_precision(data):
    y_true, y_pred = data
    sklearn_result = sklearn.metrics.precision_score(y_true, y_pred, average='micro')
    precision, ci = precision_score(y_true, y_pred, average='micro')
    assert sklearn_result == precision
    
@pytest.mark.parametrize("data",
[ ( [0, 0, 0, 0, 1, 1, 1, 1, 0],
    [0, 0, 1, 0, 1, 0, 1, 1, 0] )])
@pytest.mark.parametrize("metric",
    [accuracy_score, ppv_score, npv_score, tpr_score, fpr_score, tnr_score, precision_score, recall_score, roc_auc_score])
def test_run_metrics(data, metric):
    y_true, y_pred = data
    result, ci = metric(y_true, y_pred)

@pytest.mark.parametrize("data",
[ ( [0, 0, 0, 0, 1, 1, 1, 1, 0],
    [0, 0, 1, 0, 1, 0, 1, 1, 0] )])
@pytest.mark.parametrize("metric",
    [accuracy_score, ppv_score, npv_score, tpr_score, fpr_score, tnr_score, precision_score])
def test_run_metrics_bootstrap(data, metric):
    y_true, y_pred = data
    result, ci = metric(y_true, y_pred, method="bootstrap_bca", n_resamples=100)

@pytest.mark.parametrize("data",
    [ ( [0, 0, 0, 0, 1, 1, 1, 1, 0],
        [0, 0, 1, 0, 1, 0, 1, 1, 0] )])
def test_macro_f1(data):
    y_true, y_pred = data
    sklearn_result = sklearn.metrics.f1_score(y_true, y_pred, average='macro')
    f1, ci = f1_score(y_true, y_pred, average='macro')
    assert pytest.approx(sklearn_result, 0.01) == f1

def test_auc():
    y_true =  np.array([0, 0, 0, 0, 1, 1, 1, 1, 0] * 10)
    y_pred = y_true + np.random.randn(len(y_true)) * 1
    y_pred = np.maximum(y_pred, 0)
    y_pred = np.minimum(y_pred, 1)
    
    auc, ci = roc_auc_score(y_true, y_pred, method='delong')
    auc_bootstrap, ci_bootstrap = roc_auc_score(y_true, y_pred, method='bootstrap_bca')
    assert pytest.approx(auc, 0.01) == auc_bootstrap
    print(auc, ci, auc_bootstrap, ci_bootstrap)

# Test for compute_midrank
@pytest.mark.parametrize("input_array, expected_output_array", [
    (np.array([0, 1, 2, 2, 4, 5, 5, 5, 8]), np.array([0.5, 2.0, 3.5, 3.5, 5.5, 7.0, 7.0, 7.0, 8.5])),
    (np.array([0, 0, 0, 1, 1, 1]), np.array([1.0, 2.0, 3.0, 4.5, 4.5, 4.5])),
    (np.array([1, 2, 3, 4]), np.array([1.5, 2.5, 3.5, 4.5])),
    (np.array([1, 1, 1, 1]), np.array([2.5, 2.5, 2.5, 2.5]))
])
def test_compute_midrank(input_array, expected_output_array):
    actual_output = compute_midrank(input_array)
    assert np.allclose(actual_output, expected_output_array)

# Added test for compute_midrank_weight
@pytest.mark.parametrize("x, sample_weight, expected", [
    (np.array([1, 2, 2, 3, 4]), np.array([1, 2, 1, 1, 1]), np.array([1.0, 3.5, 3.5, 4.0, 5.0])),
    (np.array([0, 1, 2, 3, 4]), np.array([1, 1, 1, 1, 1]), np.array([0.5, 1.5, 2.5, 3.5, 4.5])),
    (np.array([1, 1, 1, 1, 1]), np.array([2, 1, 1, 1, 1]), np.array([2.0, 2.0, 2.0, 2.0, 2.0])),
])
def test_compute_midrank_weight(x, sample_weight, expected):
    result = compute_midrank_weight(x, sample_weight)
    assert np.allclose(result, expected, atol=1e-6)

