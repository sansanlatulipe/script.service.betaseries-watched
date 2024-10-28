from behave import given, when, then


@given('the {mediumType} "{mediumTitle}" has been added to {repoType}')
def step_given_a_new_named_medium_in_repo(context, mediumType, mediumTitle, repoType):
    # @TODO : mock add medium in repo with event
    context.inputs = {
        "medium": {
            "uniqueId": 1,
            "title": mediumTitle,
            "isWatched": False
        },
        "repository": {
            "type": repoType
        }
    }


@given('this {mediumType} is marked as "{watchedMark}" on {repoType}')
def step_given_a_medium_has_watched_mark(context, mediumType, watchedMark, repoType):
    # @TODO : call mock
    context.inputs.get("medium")["isWatched"] = "watched" == watchedMark


@given('the {mediumType} "{mediumTitle}" is marked as "{watchedMark}" on {repoType}')
def step_given_a_named_medium_has_watched_mark(context, mediumType, mediumTitle, watchedMark, repoType):
    context.inputs = {
        "medium": {
            "uniqueId": 1,
            "title": mediumTitle,
            "isWatched": False
        }
    }
    step_given_a_medium_has_watched_mark(context, mediumType, watchedMark, repoType)


@given('this {mediumType} exists in {repoType}')
def step_given_a_medium_exists_in_repo(context, mediumType, repoType):
    # @TODO : mock add medium in repo
    pass


@when('the complementary scan runs to synchonize {mediumType}')
def step_when_run_complementary_scan_sync(context, mediumType):
    # @TODO : call sync
    pass


@then('this {mediumType} should be marked as "{watchedMark}" on {repoType}')
def step_then_assert_medium_should_have_watched_mark(context, mediumType, watchedMark, repoType):
    expectedIsWatched = "watched" == watchedMark
    assert context.inputs.get("medium").get("isWatched") == expectedIsWatched
