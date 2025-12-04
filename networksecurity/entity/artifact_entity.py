from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    """
    Data class for storing the artifact of data ingestion.
    """
    trained_file_path: str
    test_file_path: str


@dataclass
class DataValidationArtifact:
    """
    Data class for storing the artifact of data validation.
    """
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str
    validation_status: bool = False

@dataclass
class DataTransformationArtifact:
    transformed_object_file_path: str
    transformed_train_file_path: str
    transformed_test_file_path: str