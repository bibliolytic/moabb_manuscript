from moabb.contexts.evaluations import CrossSubjectEvaluation, WithinSessionEvaluation
from moabb.contexts.motor_imagery import LeftRightImagery
from pyriemann.estimation import Covariances
from pyriemann.spatialfilters import CSP
from pyriemann.classification import TSclassifier, MDM
from sklearn.pipeline import make_pipeline
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.svm import SVC
import os
from collections import OrderedDict
from moabb import utils
from moabb.viz import meta_analysis as ma
from moabb.viz import analyze


def RHvsLH_within(out_dir, pipelines):
    name = 'RHvsLH_within'
    datasets = utils.dataset_search('imagery', events=['right_hand', 'left_hand'],
                                    has_all_events=True, min_subjects=2, multi_session=False)

    print(datasets)
    pipelines = OrderedDict()
    pipelines['TS'] = make_pipeline(Covariances('oas'), TSclassifier())
    pipelines['CSP+LDA'] = make_pipeline(Covariances('oas'), CSP(6), LDA())
    pipelines['CSP+SVM'] = make_pipeline(Covariances('oas'), CSP(6), SVC())  #

    context = LeftRightImagery(
        pipelines, WithinSessionEvaluation(n_jobs=10), datasets)

    results = context.process()


def OnlyC3C4_within(out_dir, pipelines):
    name = 'OnlyC3C4_within'
    datasets = utils.dataset_search('imagery', events=['right_hand', 'left_hand'],
                                    has_all_events=True, min_subjects=2,
                                    multi_session=False, channels=['C3', 'C4'])
    print(datasets)
    context = LeftRightImagery(pipelines, WithinSessionEvaluation(
        n_jobs=10), datasets, channels=['C3', 'C4'])
    results = context.process(suffix='C3C4')


def RHvsLH_cross(out_dir, pipelines):
    name = 'RHvsLH_cross'
    datasets = utils.dataset_search('imagery', events=['right_hand', 'left_hand'],
                                    has_all_events=True, min_subjects=2,
                                    multi_session=False)

    print(datasets)
    pipelines = OrderedDict()
    pipelines['TS'] = make_pipeline(Covariances('oas'), TSclassifier())
    pipelines['CSP+LDA'] = make_pipeline(Covariances('oas'), CSP(6), LDA())
    pipelines['CSP+SVM'] = make_pipeline(Covariances('oas'), CSP(6), SVC())  #

    context = LeftRightImagery(
        pipelines, CrossSubjectEvaluation(n_jobs=10), datasets)

    results = context.process()


def OnlyC3C4_cross(out_dir, pipelines):
    name = 'OnlyC3C4_cross'
    datasets = utils.dataset_search('imagery', events=['right_hand', 'left_hand'],
                                    has_all_events=True, min_subjects=2,
                                    multi_session=False, channels=['C3', 'C4'])
    print(datasets)
    context = LeftRightImagery(pipelines, CrossSubjectEvaluation(
        n_jobs=10), datasets, channels=['C3', 'C4'])
    results = context.process(suffix='C3C4')


def run_analyses(out_dir):
    for suffix in ['', 'C3C4']:
        for ev in [CrossSubjectEvaluation, WithinSessionEvaluation]:
            analyze((ev, LeftRightImagery), out_dir,
                    suffix=suffix, name='{}_{}'.format(ev.__name__, suffix))


if __name__ == '__main__':
    import mne
    # alter mne directories
    mne.utils.set_config(
        'MNE_DATA', '/agbs/bcigroup/Studies/z008_ExternalDatasets/data')
    out_dir = os.path.dirname(os.path.realpath(__file__))

    pipelines = OrderedDict()
    pipelines['TS'] = make_pipeline(Covariances('oas'), TSclassifier())
    pipelines['CSP+LDA'] = make_pipeline(Covariances('oas'), CSP(8), LDA())
    pipelines['CSP+SVM'] = make_pipeline(Covariances('oas'), CSP(8), SVC())  #

    # OnlyC3C4_cross(out_dir, pipelines)
    # OnlyC3C4_within(out_dir, pipelines)
    # # RHvsLH_cross(out_dir, pipelines)
    # RHvsLH_within(out_dir, pipelines)
    run_analyses('/agbs/bcigroup/_Share/Vinay/MOABB')
