import json

from behave import given
from behave import then
from behave import when
from behave.runner import Context

from resources.lib.entity import MediumEntity


@given('the {mediumType} "{mediumTitle}" has been added to {repoType}')
def step_given_a_new_named_medium_in_repo(context: Context, mediumType: str, mediumTitle: str, repoType: str) -> None:
    medium = _buildMedium(mediumTitle, False)

    context.inputs = {
        'medium': medium,
        'isNew': True,
        'repository': {
            'type': repoType
        }
    }
    step_given_a_medium_exists_in_repo(context, mediumType, repoType)


@given('this {mediumType} is marked as "{watchedMark}" on {repoType}')
def step_given_a_medium_has_watched_mark(context: Context, mediumType: str, watchedMark: str, repoType: str) -> None:
    _retrieveMediumFromRepo(context, repoType).isWatched = _buildIsWatch(watchedMark)


@given('the {mediumType} "{mediumTitle}" is marked as "{watchedMark}" on {repoType}')
def step_given_a_named_medium_has_watched_mark(
    context: Context,
    mediumType: str,
    mediumTitle: str,
    watchedMark: str,
    repoType: str
) -> None:
    context.inputs = {
        'medium': _buildMedium(mediumTitle, False)
    }
    step_given_a_medium_has_watched_mark(context, mediumType, watchedMark, repoType)


@given('this {mediumType} exists in {repoType}')
def step_given_a_medium_exists_in_repo(context: Context, mediumType: str, repoType: str) -> None:
    _retrieveMediumFromRepo(context, repoType)


@when('this {mediumType} triggers a Kodi notification')
def step_when_kodi_notification_is_triggered(context: Context, mediumType: str) -> None:
    bearerRepoMock = context.dependencyInjector.get('betaseries.bearer.repository')
    kodiRepoMock = context.dependencyInjector.get(f'kodi.{mediumType}.repository')
    bsRepoMock = context.dependencyInjector.get(f'betaseries.{mediumType}.repository')

    bearerRepoMock.isActive.return_value = True
    kodiRepoMock.retrieveById.return_value = _retrieveMediumFromRepo(context, 'Kodi')
    bsRepoMock.retrieveByUniqueId.return_value = _retrieveMediumFromRepo(context, 'BetaSeries')

    context.dependencyInjector.get('daemon.sync').onNotification(
        None,
        'VideoLibrary.OnUpdate',
        json.dumps({
            'item': vars(context.inputs.get('medium')) | {'type': mediumType},
            'added': context.inputs.get('isNew')
        })
    )


@when('the complementary scan runs to synchonize {mediumType}s')
def step_when_run_complementary_scan_sync(context: Context, mediumType: str) -> None:
    cacheRepoMock = context.dependencyInjector.get('cache.repository')
    bearerRepoMock = context.dependencyInjector.get('betaseries.bearer.repository')
    kodiRepoMock = context.dependencyInjector.get(f'kodi.{mediumType}.repository')
    bsRepoMock = context.dependencyInjector.get(f'betaseries.{mediumType}.repository')

    cacheRepoMock.getBetaseriesEndpoint.return_value = 'endpoint-id'
    bearerRepoMock.isActive.return_value = True
    kodiRepoMock.retrieveAll.return_value = [_retrieveMediumFromRepo(context, 'Kodi')]
    bsRepoMock.retrieveById.return_value = _retrieveMediumFromRepo(context, 'BetaSeries')
    bsRepoMock.retrieveUpdatedIdsFrom.return_value = [{}]

    context.dependencyInjector.get(f'{mediumType}.sync').synchronize()


@then('this {mediumType} should be marked as "{watchedMark}" on {repoType}')
def step_then_assert_medium_should_have_watched_mark(
    context: Context,
    mediumType: str,
    watchedMark: str,
    repoType: str
) -> None:
    expectedIsWatched = _buildIsWatch(watchedMark)
    actualIsWatched = _retrieveMediumFromRepo(context, repoType).isWatched

    assert expectedIsWatched == actualIsWatched, \
        'The {} should be marked as {}, but it is not'.format(mediumType, watchedMark)


def _buildMedium(title: str, isWatched: bool) -> MediumEntity:
    return MediumEntity(1, 1, title, isWatched)


def _buildIsWatch(watchedMark: str) -> bool:
    return 'watched' == watchedMark


def _retrieveMediumFromRepo(context: Context, repoType: str) -> MediumEntity:
    if not context.inputs.get(f'{repoType}Medium'):
        context.inputs[f'{repoType}Medium'] = context.inputs.get('medium').clone()
    return context.inputs.get(f'{repoType}Medium')
