import json
from behave import given, when, then
from resources.test.unit.testmod import mock


@given('the {mediumType} "{mediumTitle}" has been added to {repoType}')
def step_given_a_new_named_medium_in_repo(context, mediumType, mediumTitle, repoType):
    # @TODO : mock add medium in repo with event
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
    with mock.patch('resources.lib.infra.betaseries.Http'), \
            mock.patch(f'resources.lib.adapter.betaseries.{mediumType.title()}Repository'), \
            mock.patch(f'resources.lib.adapter.kodi.{mediumType.title()}Repository'):

        kodiRepoMock = context.dependencyInjector.get(f'kodi.{mediumType}.repository')
        bsRepoMock = context.dependencyInjector.get(f'betaseries.{mediumType}.repository')

        kodiRepoMock.retrieveById = mock.Mock(return_value=_retrieveMediumFromRepo(context, 'Kodi'))
        bsRepoMock.retrieveByUniqueId = mock.Mock(return_value=_retrieveMediumFromRepo(context, 'BetaSeries'))

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
    with mock.patch(f'resources.lib.adapter.betaseries.{mediumType.title()}Repository'), \
            mock.patch(f'resources.lib.adapter.kodi.{mediumType.title()}Repository'):

        kodiRepoMock = context.dependencyInjector.get(f'kodi.{mediumType}.repository')
        bsRepoMock = context.dependencyInjector.get(f'betaseries.{mediumType}.repository')

        kodiRepoMock.retrieveAll = mock.Mock(return_value=[_retrieveMediumFromRepo(context, 'Kodi')])
        bsRepoMock.retrieveById = mock.Mock(return_value=_retrieveMediumFromRepo(context, 'BetaSeries'))
        bsRepoMock.retrieveUpdatedIdsFrom = mock.Mock(return_value=[{}])

        context.dependencyInjector.get(f'{mediumType}.sync').synchronizeRecentlyUpdatedOnBetaseries()


@then('this {mediumType} should be marked as "{watchedMark}" on {repoType}')
def step_then_assert_medium_should_have_watched_mark(context, mediumType, watchedMark, repoType):
    assert _buildIsWatch(watchedMark) == _retrieveMediumFromRepo(context, repoType).get('isWatched')


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
