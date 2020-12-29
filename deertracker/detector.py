import numpy as np
import tensorflow as tf

from typing import Tuple

from deertracker import DEFAULT_DETECTOR_PATH


class MegaDetector:
    """
    Microsoft's MegaDetector. https://github.com/microsoft/CameraTraps
    """

    def __init__(self, filepath=DEFAULT_DETECTOR_PATH):
        """
        Load the protobuf file, massage from TF 1.13.1 to TF 2.x

        Inputs
        ------
        filepath
            Path to the saved megadetector protobuf file. See download links in
            https://github.com/microsoft/CameraTraps/blob/master/megadetector.md
            This was tested with version 4.1
        """
        with tf.io.gfile.GFile(str(filepath), "rb") as f:
            graph_def = tf.compat.v1.GraphDef()
            graph_def.ParseFromString(f.read())

        # Adapted from TF migration guide:
        # https://www.tensorflow.org/guide/migrate#a_graphpb_or_graphpbtxt
        def wrap_frozen_graph(graph_def, inputs, outputs):
            def _imports_graph_def():
                tf.compat.v1.import_graph_def(graph_def, name="")

            wrapped_import = tf.compat.v1.wrap_function(_imports_graph_def, [])
            import_graph = wrapped_import.graph
            return wrapped_import.prune(
                tf.nest.map_structure(import_graph.as_graph_element, inputs),
                tf.nest.map_structure(import_graph.as_graph_element, outputs),
            )

        # You can see the names of the input/output tensors here:
        # https://github.com/microsoft/CameraTraps/blob/master/detection/run_tf_detector.py#L150-L153
        self.model = wrap_frozen_graph(
            graph_def,
            "image_tensor:0",
            ["detection_boxes:0", "detection_classes:0", "detection_scores:0"],
        )

        self.labels = {
            1: "animal",
            2: "person",
            3: "vehicle",  # available in megadetector v4+
        }

    def predict(
        self, image: np.ndarray, confidence: float = 0.5
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Image -> bounding boxes.

        Inputs
        ------
        image : np.ndarray
            Input uint8 array with shape (width, height, 3)
        confidence : float
            Only bounding boxes with this level of confidence will be output.

        Outputs
        -------
        bboxes : np.ndarray
            Nx4 array of bounding boxes:
                bboxes[i][0]  # starting y coordinate
                bboxes[i][1]  # starting x coordinate
                bboxes[i][2]  # width
                bboxes[i][3]  # height
        classes : np.ndarray
            N-length array of class labels (str)
        scores : np.ndarray
            N-length array of bounding box scores. Higher is better.
            Use `confidence` to ignore bounding boxes below a confidence.
        """
        # model operates on batches, so add a singular dimension at the front.
        tensor_input = tf.convert_to_tensor(image[None, :, :, :])
        # the map below strips out the singular batch dimension
        bboxes, classes, scores = map(lambda x: x.numpy()[0], self.model(tensor_input))
        bboxes = bboxes[scores > confidence]
        classes = classes[scores > confidence].astype("uint16")
        scores = scores[scores > confidence]
        # Need to convert fractions -> pixels
        bboxes = np.round(bboxes * (image.shape[:2] * 2)).astype("uint16")
        # x, y, w, h
        bboxes = np.array([(b[1], b[0], b[3] - b[1], b[2] - b[0]) for b in bboxes])
        labels = np.array([self.labels[c] for c in classes])

        return bboxes, labels, scores
