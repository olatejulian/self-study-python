from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    classification_report,
    confusion_matrix,
    f1_score,
    log_loss,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)


class Evaluating:
    def __init__(self, y_true, y_pred, y_proba):
        self.prediction_metrics = {
            "f1": f1_score(y_true, y_pred),
            "log_loss": log_loss(y_true, y_pred),
            "recall": recall_score(y_true, y_pred),
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred),
            "confusion_matrix": confusion_matrix(y_true, y_pred),
            "classification_report": classification_report(y_true, y_pred),
        }

        self.probabilistic_metrics = {
            "roc_curve": roc_curve(y_true, y_proba),
            "roc_auc_score": roc_auc_score(y_true, y_proba),
            "precision_recall_curve": precision_recall_curve(y_true, y_proba),
            "average_precision_score": average_precision_score(y_true, y_proba),
        }
