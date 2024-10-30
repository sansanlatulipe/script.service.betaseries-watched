Feature: Synchronize watched movies between BetaSeries and Kodi
    In order to know what movies I still have to play
    As a memory-impaired movie-lover
    I want Kodi and BetaSeries to show me the movies I already watched

    Scenario: A new movie is added to Kodi
        Given the movie "Avatar (2009)" has been added to Kodi
        And this movie is marked as "watched" on BetaSeries
        When this movie triggers a Kodi notification
        Then this movie should be marked as "watched" on Kodi

    Scenario: A new movie is marked as watched on Kodi
        Given the movie "Avatar (2009)" is marked as "watched" on Kodi
        When this movie triggers a Kodi notification
        Then this movie should be marked as "watched" on BetaSeries

    Scenario: A new movie is marked as watched on BetaSeries
        Given the movie "Avatar (2009)" is marked as "watched" on BetaSeries
        And this movie exists in Kodi
        When the complementary scan runs to synchonize movies
        Then this movie should be marked as "watched" on Kodi
