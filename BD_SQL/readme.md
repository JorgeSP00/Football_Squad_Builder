README: DATABASE EXPLANATION.
This database has been designed to store information for an application that enables users to create custom football squads. Users will choose players for their squad, each of whom has attributes such as market value, usual playing position, nationality, and the team they belong to. Based on this data (nationality, team, and market value), a set of limitations can be defined, which the user must follow when constructing their squad. By adhering to these limitations, users aim to build the best possible team, and other users can rate the quality of these squads.
Table Descriptions
•	User: This table stores login information for users. It is linked to the "Squad" and "Rating" tables, as each user can create multiple squads and rate the squads of other users.
•	Nationality: This table centralizes information about player nationalities. It is linked to both the "Player" and "Limitation" tables to establish relationships between a player’s nationality and squad-building limitations.
•	Player: This table contains detailed information about footballers, including their nationality (linked via nationality_id), team affiliation (linked via team_id), and market value. It connects to the "Team" table to identify which club a player belongs to and to the "Squad_Player" table to associate players with specific squads.
•	Team: The "Team" table stores data on football teams. It is linked to the "Competition" table (via competition_id) to identify the competition in which the team competes and to the "Player" table to associate players with their teams.
•	Competition: This table holds information about the various football competitions. It is connected to the "Team" table to list participating teams and to the "Limitation" table to set squad restrictions based on the competition.
•	Formation: This table stores the different tactical formations available for creating squads. It is connected to the "Squad" table, as each squad must have an associated formation.
•	Squad: This table records the squads created by users. It is linked to the "User" table to show which user created the squad, to the "Formation" table to specify the formation used, to the "Squad_Player" table to detail the selected players, to the "Limitation" table to outline any applied restrictions, and to the "Rating" table to track the ratings received by the squad.
•	Squad_Player: This junction table links players to the squads in which they are included, effectively connecting the "Squad" and "Player" tables.
•	Limitation: This table defines the constraints applied to a squad, such as maximum budget, permitted nationalities, and selectable teams. It is connected to the "Squad" and "Competition" tables.
•	Rating: This table stores the ratings that users give to squads created by others. It is connected to the "User" table to record who provided the rating and to the "Squad" table to indicate which squad was rated.
Explanation of Views
•	SquadDetails: This view offers a comprehensive overview of each squad, including details about the user who created it, the formation used, any applied limitations (like nationality and budget), the competition, and the creation date. This view enables easy retrieval of all relevant squad information in one query.
•	SquadPlayers: This view lists the players selected for each squad, showing their names, primary and alternate positions, and the specific roles they occupy within the squad. This makes it straightforward to review the composition and roles of players within each squad.
•	SquadRatings: This view displays the individual ratings for each squad, including the user who gave the rating, the score, the comment, and the rating date. This view is useful for analyzing the feedback and ratings squads receive from other users.
•	Squad_Average_Rating: This view shows the average rating of each squad, alongside the name of the user who created it. It is particularly useful for identifying the highest-rated squads within the application.
Explanation of Indexes
•	idx_player_name_position:
o	Purpose: To accelerate searches for players by name and position.
o	Utility: Enhances query performance when users are selecting specific players to include in their squad.
•	idx_squad_user_created_at:
o	Purpose: To expedite queries that filter squads by the user who created them and by creation date.
o	Utility: Optimizes access to squads, especially when filtering by user and date.
•	idx_limitation_competition_nationality:
o	Purpose: To quicken queries that filter limitations based on competition and nationality.
o	Utility: Improves performance when applying squad restrictions related to specific competitions and allowed nationalities.
•	idx_rating_squad:
o	Purpose: To speed up queries that search for ratings linked to a specific squad.
o	Utility: Optimizes the retrieval of squad ratings, allowing for quicker access to all ratings related to a squad.



My video:
https://youtu.be/IxFfsxkjHnc