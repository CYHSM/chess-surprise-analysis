# Analysis of Carlsen-Firouzja Bullet marathon
Not too much to do during these times, so here I analysed the recent bullet marathon between Magnus Carlsen and Alireza Firouzja which was played on lichess. They played for over 4 hours and it was really interesting to see both players playing high quality chess with 60s each on the clock (viewing pleasure was possibly enhanced given current sport deprivation). I downloaded the bullet games they played (194 games) and had some fun with xkcd style graphics which I always thought should be used more regularly. Overall this analysis is not directly related to the goal of the repository it resides in but it also does not warrant the creation of a new one.

First off we can plot all games vs. their evaluation for each move: 
![Alt text](./all_games.png?raw=true "All games")

Each line represents one game where the x-axis is depicting the half-move number while y-axis shows the engine evaluation, which is cut at +-10. Engine evaluation is positive if white is winning and negative if black side is winning. You can already see that there are some outliers in this graph, lets just look at two of them:

![Alt text](./mouseslip.png?raw=true "All games")
This game went from a eval of around 0 to over 10 and back. Looking at the board at this position tells us that this was a clear mouse slip by Carlsen, wanting to take the pawn on G2. Firouzja did not take advantage of that (either because he already premoved Rook to G1 or because he clearly knew that it was a mouse slip). 

![Alt text](./cheekytactics.png?raw=true "All games")
In this game something similar happened but it was taken advantage off and Carlsen resigned after Firouzja took the bishop. It might a cheeky try at preventing Firouzja from fianchetto-ing the bishop as he was expecting pawn to B6 and hoped that Firouzja is in pre-move mode. 

Now we can also look at the average evaluation over all games:

![Alt text](./average_centipawn.png?raw=true "All games")
On average it seems that white will gain an advantage around move 35 (half-move 70). This holds true, also if we split the games based on the outcome (Win Carlsen vs Win Firouzja).

![Alt text](./average_centipawn_outcome.png?raw=true "All games")
We can look at the same graph split for winning color. White seems to be at maximum evaluation around move 40 (half-move 80) while it seems black is more often winning the long games (however there are far less games after we go beyond 60 moves (120 half-moves)). 

The games of this bullet marathon also includes the exact clock times of both Carlsen and Firouzja (thanks lichess!), so we can have some fun with them: 

![Alt text](./average_clock.png?raw=true "All games")
Each line here is representing one game, where the red color is depicting the games of Carlsen and blueish color is depicting the games of Firouzja. The averages are shown in thick lines. The timing difference is not as big as I had expected after seeing the games (it felt like Firouzja was much faster). As I always wanted to zoom in on a graph and see how weird but beautiful this feature is, we can now appreciate that there is a roughly 1.5s gap between the two around move 34, meaning on average Firouzja has 1.5s more on his clock than Carlsen. 

One last plot showing the difference in time based on move number:

![Alt text](./diff_clock.png?raw=true "All games")
Here the black line is showing the difference between the two thick lines in the plot before and the colored thick lines show the average time difference when Carlsen wins the game (red) or Firouzja wins the game (blue). Interesting to see that the gap is widening around move 10, possibly indicating at what point both players start to think about the position. 