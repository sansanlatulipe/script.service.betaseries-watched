Feature: Synchronize watched TV shows between BetaSeries and Kodi
    In order to know what is the next episode to play
    As a couch potato
    I want Kodi and BetaSeries to show me the TV shows I already watched

    Scenario: A new episode is added to Kodi
        Given the episode "Game of Thrones (2011) S01E01" has been added to Kodi
        And this episode is marked as "watched" on BetaSeries
        When this episode triggers a Kodi notification
        Then this episode should be marked as "watched" on Kodi

    Scenario: A new episode is marked as watched on Kodi
        Given the episode "Game of Thrones (2011) S01E01" is marked as "watched" on Kodi
        When this episode triggers a Kodi notification
        Then this episode should be marked as "watched" on BetaSeries

    Scenario: A new episode is marked as watched on BetaSeries
        Given the episode "Game of Thrones (2011) S01E01" is marked as "watched" on BetaSeries
        And this episode exists in Kodi
        When the complementary scan runs to synchonize episodes
        Then this episode should be marked as "watched" on Kodi
