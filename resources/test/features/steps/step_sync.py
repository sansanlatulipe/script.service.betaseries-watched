import json
from behave import given, when, then


@given('the {mediumType} "{mediumTitle}" has been added to {repoType}')
def step_given_a_new_named_medium_in_repo(context, mediumType, mediumTitle, repoType):
    medium = _buildMedium(mediumType, mediumTitle, False)

    context.inputs = {
        'medium': medium,
        'isNew': True,
        'repository': {
            'type': repoType
        }
    }
    step_given_a_medium_exists_in_repo(context, mediumType, repoType)


@given('this {mediumType} is marked as "{watchedMark}" on {repoType}')
def step_given_a_medium_has_watched_mark(context, mediumType, watchedMark, repoType):
    _retrieveMediumFromRepo(context, repoType)['isWatched'] = _buildIsWatch(watchedMark)


@given('the {mediumType} "{mediumTitle}" is marked as "{watchedMark}" on {repoType}')
def step_given_a_named_medium_has_watched_mark(context, mediumType, mediumTitle, watchedMark, repoType):
    context.inputs = {
        'medium': _buildMedium(mediumType, mediumTitle, False)
    }
    step_given_a_medium_has_watched_mark(context, mediumType, watchedMark, repoType)


@given('this {mediumType} exists in {repoType}')
def step_given_a_medium_exists_in_repo(context, mediumType, repoType):
    _retrieveMediumFromRepo(context, repoType)


@when('this {mediumType} triggers a Kodi notification')
def step_when_kodi_notification_is_triggered(context, mediumType):
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
            'item': context.inputs.get('medium'),
            'added': context.inputs.get('isNew')
        })
    )


@when('the complementary scan runs to synchonize {mediumType}s')
def step_when_run_complementary_scan_sync(context, mediumType):
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
def step_then_assert_medium_should_have_watched_mark(context, mediumType, watchedMark, repoType):
    expectedIsWatched = _buildIsWatch(watchedMark)
    actualIsWatched = _retrieveMediumFromRepo(context, repoType).get('isWatched')

    assert expectedIsWatched == actualIsWatched, \
        'The {} should be marked as {}, but it is not'.format(mediumType, watchedMark)


def _buildMedium(type, title, isWatched):
    return {
        'type': type,
        'id': 1,
        'uniqueId': 1,
        'title': title,
        'isWatched': isWatched
    }


def _buildIsWatch(watchedMark):
    return 'watched' == watchedMark


def _retrieveMediumFromRepo(context, repoType):
    if not context.inputs.get(f'{repoType}Medium'):
        context.inputs[f'{repoType}Medium'] = context.inputs.get('medium').copy()
    return context.inputs.get(f'{repoType}Medium')
