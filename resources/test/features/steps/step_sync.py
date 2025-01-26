import json
import re

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
    context.dependencyInjector.get('betaseries.http').get.return_value = _buildBsMediumFromEntity(
        mediumType,
        _retrieveMediumFromRepo(context, 'BetaSeries')
    )
    context.dependencyInjector.get('kodi.jsonrpc').call.return_value = _buildKodiMediumFromEntity(
        mediumType,
        _retrieveMediumFromRepo(context, 'Kodi')
    )

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
    context.dependencyInjector.get('betaseries.http').get.side_effect = [
        {
            'member': {
                'id': 1
            }
        },
        {
            'events': [
                {
                    'ref_id': 3,
                    'id': _retrieveMediumFromRepo(context, 'BetaSeries').id
                }
            ]
        },
        _buildBsMediumFromEntity(
            mediumType,
            _retrieveMediumFromRepo(context, 'BetaSeries')
        )
    ]
    context.dependencyInjector.get('kodi.jsonrpc').call.return_value = _buildKodiMediumFromEntity(
        mediumType,
        _retrieveMediumFromRepo(context, 'Kodi'),
        isList=True
    )


    context.dependencyInjector.get(f'{mediumType}.sync').synchronize()


@then('this episode should be marked as "{watchedMark}" on BetaSeries')
def step_then_assert_episode_should_have_watched_mark_on_betaseries(
    context: Context,
    watchedMark: str
) -> None:
    expectedIsWatched = _buildIsWatch(watchedMark)
    actualEpisode = _retrieveMediumFromRepo(context, 'BetaSeries')

    if expectedIsWatched:
        context.dependencyInjector.get('betaseries.http').post.assert_any_call(
            '/episodes/watched',
            {'id': actualEpisode.id}
        ), \
            'The episode should be marked as {}, but it is not'.format(watchedMark)
    else:
        context.dependencyInjector.get('betaseries.http').delete.assert_any_call(
            '/episodes/watched',
            {'id': actualEpisode.id}
        ), \
            'The episode should be marked as {}, but it is not'.format(watchedMark)


@then('this movie should be marked as "{watchedMark}" on BetaSeries')
def step_then_assert_movie_should_have_watched_mark_on_betaseries(
    context: Context,
    watchedMark: str
) -> None:
    expectedIsWatched = _buildIsWatch(watchedMark)
    actualMovie = _retrieveMediumFromRepo(context, 'BetaSeries')

    context.dependencyInjector.get('betaseries.http').post.assert_any_call(
        '/movies/movie',
        {
            'id': actualMovie.id,
            'state': 1 if expectedIsWatched else 0,
            'mail': 0,
            'twitter': 0,
            'profile': 0
        }
    ), \
        'The movie should be marked as {}, but it is not'.format(watchedMark)


@then('this {mediumType} should be marked as "{watchedMark}" on Kodi')
def step_then_assert_medium_should_have_watched_mark_on_kodi(
    context: Context,
    mediumType: str,
    watchedMark: str
) -> None:
    expectedIsWatched = _buildIsWatch(watchedMark)
    expectedMethod = 'VideoLibrary.Set{}Details'.format(mediumType.capitalize())
    expectedMediumIdName = '{}id'.format(mediumType)
    actualMedium = _retrieveMediumFromRepo(context, 'Kodi')

    context.dependencyInjector.get('kodi.jsonrpc').call.assert_any_call(
        expectedMethod,
        {
            expectedMediumIdName: actualMedium.id,
            'playcount': 1 if expectedIsWatched else 0
        }
    ), \
        'The {} should be marked as {}, but it is not'.format(mediumType, watchedMark)


def _buildBsMediumFromEntity(type: str, medium: MediumEntity) -> dict:
    if 'episode' == type:
        return _buildBsEpisodeFromEntity(medium)
    else:
        return _buildBsMovieFromEntity(medium)


def _buildBsEpisodeFromEntity(medium: MediumEntity) -> dict:
    titleSplit = re.findall(r"(.+) S([0-9]{2})E([0-9]{2})", medium.title)[0]

    return {
        'episode': {
            'id': medium.id,
            'thetvdb_id': medium.uniqueId,
            'show': {
                'title': titleSplit[0]
            },
            'season': int(titleSplit[1]),
            'episode': int(titleSplit[2]),
            'user': {
                'seen': medium.isWatched
            }
        }
    }


def _buildBsMovieFromEntity(medium: MediumEntity) -> dict:
    return {
        'movie': {
            'id': medium.id,
            'tmdb_id': medium.uniqueId,
            'title': medium.title,
            'user': {
                'status': 1 if medium.isWatched else 0
            }
        }
    }


def _buildKodiMediumFromEntity(type: str, medium: MediumEntity, isList: bool = False) -> dict:
    if 'episode' == type:
        return _buildKodiEpisodeFromEntity(medium, isList)
    else:
        return _buildKodiMovieFromEntity(medium, isList)


def _buildKodiEpisodeFromEntity(medium: MediumEntity, isList: bool) -> dict:
    episode = {
        'episodeid': medium.id,
        'uniqueid': {
            'tvdb': medium.uniqueId
        },
        'showtitle': medium.title,
        'playcount': 1 if medium.isWatched else 0
    }

    if isList:
        return {
            'result': {
                'episodes': [episode]
            }
        }
    else:
        return {
            'result': {
                'episodedetails': episode
            }
        }


def _buildKodiMovieFromEntity(medium: MediumEntity, isList: bool) -> dict:
    movie = {
        'movieid': medium.id,
        'uniqueid': {
            'tmdb': medium.uniqueId
        },
        'sorttitle': medium.title,
        'playcount': 1 if medium.isWatched else 0
    }

    if isList:
        return {
            'result': {
                'movies': [movie]
            }
        }
    else:
        return {
            'result': {
                'moviedetails': movie
            }
        }


def _buildMedium(title: str, isWatched: bool) -> MediumEntity:
    return MediumEntity(1, 1, title, isWatched)


def _buildIsWatch(watchedMark: str) -> bool:
    return 'watched' == watchedMark


def _retrieveMediumFromRepo(context: Context, repoType: str) -> MediumEntity:
    if not context.inputs.get(f'{repoType}Medium'):
        context.inputs[f'{repoType}Medium'] = context.inputs.get('medium').clone()
    return context.inputs.get(f'{repoType}Medium')
