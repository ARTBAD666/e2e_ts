# 


from typing import List

from sklearn.base import ClassifierMixin
from typing_extensions import Annotated
from zenml import get_step_context, step
from zenml.logger import get_logger

logger = get_logger(__name__)


@step
def hp_tuning_select_best_model(
    step_names: List[str],
) -> Annotated[ClassifierMixin, "best_model"]:
    """Find best model across all HP tuning attempts.

    This is an example of a model hyperparameter tuning step that loops
    other artifacts linked to model version in Model Control Plane to find
    the best hyperparameter tuning output model of all according to the metric.

    Returns:
        The best possible model class and its' parameters.
    """
    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
    model = get_step_context().model

    best_model = None
    best_metric = -1
    # consume artifacts attached to current model version in Model Control Plane
    for step_name in step_names:
        hp_output = model.get_data_artifact("hp_result")
        model_: ClassifierMixin = hp_output.load()
        # fetch metadata we attached earlier
        metric = float(hp_output.run_metadata["metric"].value)
        if best_model is None or best_metric < metric:
            best_model = model_
    ### YOUR CODE ENDS HERE ###
    return best_model
