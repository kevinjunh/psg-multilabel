import argparse
import logging
from typing import Any, Dict
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from sklearn.neighbors import KNeighborsClassifier
from skmultilearn.problem_transform import BinaryRelevance, ClassifierChain, LabelPowerset
from sklearn.naive_bayes import GaussianNB
from skmultilearn.ensemble import RakelD, MajorityVotingClassifier, LabelSpacePartitioningClassifier
from skmultilearn.adapt import MLARAM
from skmultilearn.cluster import FixedLabelSpaceClusterer


from lib.base_models import (
    DependantBinaryRelevance,
    PatchedClassifierChain,
    StackedGeneralization,
)
from lib.classifiers import (
    ClassifierChainWithFTestOrdering,
    ClassifierChainWithGeneticAlgorithm,
    ClassifierChainWithLOP,
    PartialClassifierChainWithLOP,
    StackingWithFTests,
)
from metrics.pipeline import (
    DatasetsLoaderNormalized,
    MetricsPipeline,
    MetricsPipelineRepository,
)

from metrics.analysis import analyse_summarized_metrics


def setup_logging() -> None:
    LOGGING_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"
    logging.basicConfig(level=logging.INFO, format=LOGGING_FORMAT)


N_FOLDS = 10
BASE_FILE_NAME = f"knn_normalized_n_folds={N_FOLDS}"
PIPELINE_RESULTS_FILE = f"./data/metrics_{BASE_FILE_NAME}.csv"
SUMMARIZED_RESULTS_FILE = f"./data/summarized_result_{BASE_FILE_NAME}.csv"
RANKED_FILE_NAME = "./data/ranked_for_{score_name}.csv"

def build_repository() -> MetricsPipelineRepository:
    return MetricsPipelineRepository(PIPELINE_RESULTS_FILE)


def build_dataset_loader() -> DatasetsLoaderNormalized:
    return DatasetsLoaderNormalized(
        [
            # [done] fast datasets
            "birds",
            "emotions",
            "scene",
            # [done] not so fast datasets
            "yeast",
            "enron",
            "genbase",
            "medical",
            # # [done] slow datasets
            "tmc2007_500",
            # impossibly slow datasets
            # "delicious",
            # "bibtex",
            # "mediamill",
            # "./data/ariane.arff"
        ]
    )

def build_models_list() -> Dict[str, Any]:
    return {
        # "baseline_binary_relevance_model": BinaryRelevance(
        #     classifier=KNeighborsClassifier(), require_dense=[False, True]
        # ),
        # "baseline_stacked_generalization": StackedGeneralization(
        #     base_classifier=KNeighborsClassifier(),
        # ),
        # "baseline_dependant_binary_relevance": DependantBinaryRelevance(
        #     base_classifier=KNeighborsClassifier(),
        # ),
        # "baseline_classifier_chain": PatchedClassifierChain(
        #     base_classifier=KNeighborsClassifier(),
        # ),
        # "stacking_with_f_tests-alpha=0.25": StackingWithFTests(
        #     base_classifier=KNeighborsClassifier(),
        #     alpha=0.25,
        # ),
        # "stacking_with_f_tests-alpha=0.50": StackingWithFTests(
        #     base_classifier=KNeighborsClassifier(),
        #     alpha=0.50,
        # ),
        # "stacking_with_f_tests-alpha=0.75": StackingWithFTests(
        #     base_classifier=KNeighborsClassifier(),
        #     alpha=0.75,
        # ),
        # "classifier_chain_with_f_test_ordering-ascending_chain=False": ClassifierChainWithFTestOrdering(
        #     base_classifier=KNeighborsClassifier(),
        #     ascending_chain=False,
        # ),
        # "classifier_chain_with_f_test_ordering-ascending_chain=True": ClassifierChainWithFTestOrdering(
        #     base_classifier=KNeighborsClassifier(),
        #     ascending_chain=True,
        # ),
        # "classifier_chain_with_lop-num_generations=10": ClassifierChainWithLOP(
        #     base_classifier=KNeighborsClassifier(),
        #     num_generations=10,
        # ),
        # "classifier_chain_with_lop-num_generations=25": ClassifierChainWithLOP(
        #     base_classifier=KNeighborsClassifier(),
        #     num_generations=25,
        # ),
        # "classifier_chain_with_lop-num_generations=50": ClassifierChainWithLOP(
        #     base_classifier=KNeighborsClassifier(),
        #     num_generations=50,
        # ),
        # "partial_classifier_chain_with_lop-num_generations=50-threshold=0.01": PartialClassifierChainWithLOP(
        #     base_classifier=KNeighborsClassifier(),
        #     num_generations=50,
        #     threshold=0.01,
        # ),
        # "partial_classifier_chain_with_lop-num_generations=25-threshold=0.01": PartialClassifierChainWithLOP(
        #     base_classifier=KNeighborsClassifier(),
        #     num_generations=25,
        #     threshold=0.01,
        # ),
        # "partial_classifier_chain_with_lop-num_generations=10-threshold=0.01": PartialClassifierChainWithLOP(
        #     base_classifier=KNeighborsClassifier(),
        #     num_generations=10,
        #     threshold=0.01,
        # ),
        # "partial_classifier_chain_with_lop-num_generations=10-threshold=0.001": PartialClassifierChainWithLOP(
        #     base_classifier=KNeighborsClassifier(),
        #     num_generations=10,
        #     threshold=0.001,
        # ),
        # "partial_classifier_chain_with_lop-num_generations=10-threshold=0.025": PartialClassifierChainWithLOP(
        #     base_classifier=KNeighborsClassifier(),
        #     num_generations=10,
        #     threshold=0.025,
        # ),
        # "partial_classifier_chain_with_lop-num_generations=10-threshold=0.05": PartialClassifierChainWithLOP(
        #     base_classifier=KNeighborsClassifier(),
        #     num_generations=10,
        #     threshold=0.05,
        # ),
        # "partial_classifier_chain_with_lop-num_generations=10-threshold=0.1": PartialClassifierChainWithLOP(
        #     base_classifier=KNeighborsClassifier(),
        #     num_generations=10,
        #     threshold=0.1,
        # ),
        # "classifier_chain_with_genetic_algorithm-num_generations=5": ClassifierChainWithGeneticAlgorithm(
        #     base_classifier=KNeighborsClassifier(),
        #     num_generations=5,
        # ),
        "binary_relevance": BinaryRelevance(
            classifier=KNeighborsClassifier(),
            require_dense=[False, True]
        ),
        "classifier_chain": ClassifierChain(
            classifier=KNeighborsClassifier()
        ),
        "label_powerset": LabelPowerset(
            classifier=KNeighborsClassifier()
        ),
        "rakeld": RakelD(
            base_classifier=GaussianNB(),
            base_classifier_require_dense=[True, True],
            labelset_size=1
        ),
        "mlaram": MLARAM(
            vigilance=0.8,
            threshold=0.01
        ),
        "majority_voting_classifier": MajorityVotingClassifier(
            classifier = ClassifierChain(classifier=GaussianNB()),
            clusterer=FixedLabelSpaceClusterer(clusters = [[0, 1, 2, 3, 4], [0, 2, 4], [3, 4]])
        ),
        "label_space_partition_classifier": LabelSpacePartitioningClassifier(
            clusterer=FixedLabelSpaceClusterer(clusters = [[0, 1, 2, 3, 4], [0, 2, 4], [3, 4]]),
            classifier=ClassifierChain(classifier=GaussianNB())
        )
    }


DATASETS_INFO_TO_CSV = "datasets_info_to_csv"
DESCRIBE_DATASETS = "describe_datasets"
DESCRIBE_METRICS = "describe_metrics"
METRICS_TO_CSV = "metrics_to_csv"
SUMMARIZED_METRICS_ANALYSIS = "summarized_metrics_analysis"
RUN_MODELS = "run_models"

if __name__ == "__main__":
    setup_logging()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "task",
        default=DESCRIBE_DATASETS,
        help="action to be executed",
        choices=[
            DATASETS_INFO_TO_CSV,
            DESCRIBE_DATASETS,
            DESCRIBE_METRICS,
            METRICS_TO_CSV,
            RUN_MODELS,
            SUMMARIZED_METRICS_ANALYSIS,
        ],
        action="store",
    )

    args = parser.parse_args()

    repository = build_repository()
    loader = build_dataset_loader()
    models = build_models_list()

    if args.task == DESCRIBE_DATASETS:
        loader.load()
        loader.describe_log()

    if args.task == DATASETS_INFO_TO_CSV:
        loader.load()
        result = loader.describe_json()

        df = pd.DataFrame(result)
        df.to_csv("./data/datasets_info.csv", index=False)

    if args.task == DESCRIBE_METRICS:
        repository.load_from_file()
        repository.describe_log()

    if args.task == METRICS_TO_CSV:
        repository.load_from_file()
        result = repository.describe_dict()

        df = pd.DataFrame(result)
        df.to_csv(SUMMARIZED_RESULTS_FILE, index=False)

    if args.task == SUMMARIZED_METRICS_ANALYSIS:
        df = pd.read_csv(SUMMARIZED_RESULTS_FILE)
        analyse_summarized_metrics(df, RANKED_FILE_NAME)

    if args.task == RUN_MODELS:
        pipe = MetricsPipeline(repository, loader, models, N_FOLDS)
        pipe.run()

