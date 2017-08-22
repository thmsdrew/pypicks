# pypicks
A silly NFL pick scraper command line interface. Using nflpickwatch.com, grabs the percentages of picks for the coming week of NFL matches and sorts them by confidence points. Then allows you to manipulate the list to get it exactly how you want before you manually input it into your pick'em league.

## initial output
    > python pypicks.pl
    Getting initial scrape... (http://nflpickwatch.com/?text=1)
    Here are your picks...

    Points  Matchup Winner  Consensus
    ---------------------------------
    1       PHI@WAS WAS     (75%)
    2       KC@NE   NE      (80%)
    3       NYJ@BUF BUF     (80%)
    4       ATL@CHI ATL     (80%)
    5       BAL@CIN CIN     (80%)
    6       PIT@CLE PIT     (80%)
    7       AZ@DET  AZ      (80%)
    8       JAX@HOU HOU     (80%)
    9       TB@MIA  TB      (80%)
    10      OAK@TEN OAK     (80%)
    11      SEA@GB  GB      (80%)
    12      CAR@SF  CAR     (80%)
    13      NYG@DAL DAL     (80%)
    14      LAC@DEN DEN     (80%)

    Enter a command... (exit, swap, flip, ags, print, help)
    >

## commands
`swap x y` - Swaps point values between two matchups `x` and `y`, `x` and `y` being numbers between 1 and the total number of matchups. For example, `swap 13 1` will place the  NYG@DAL as the lowest confidence pick, and the PHI@WAS matchup as the 13^th^.

`flip x` - Flips the winner of the matchup with `x` confidence points from the current chosen winner to the loser. For example, `flip 10` will switch the 10^th^ confidence pick winner from OAK to TEN.

`ags x` - The Any Given Sunday command will randomly swap and flip `x` matchups. Naturally there are going to be upsets, and if you don't care to choose them yourself, let the Any Given Sunday take the burden off your shoulders. This could be modified with a weight or seed value possibly.

`print` - Outputs the current pick list. `swap`, `flip`, and `ags` will `print` the updated pick list when done.

## data format
The scraping portion of this script is pretty specific to the website I'm using, but the general data "format" that it utilizes could probably be scraped from any similar website.

I am using an array of arrays. Each sub-array is a pick. Each pick is an array of the following data points: `[confidence points, matchup, winner, consensus percentage]`

`confidence points` - Total number of points to assign to the pick. Lower number means a less confident pick. This is a number between 1 and the total number of matchups in the coming NFL week inclusive.

`matchup` - A text representation of the matchup in the form of "ABC@XYZ".

`winner` - The team that is chosen to win in the same format as shown in the `matchup`, "ABC" or "XYZ".

`consensus percentage` - The percentage of "professionals" that chose the given winner. Initially, lower percentages are assigned lower confidence points.

## aside
Obviously this is just silly. Every year I join an NFL pick'em league, and while I don't really care about football, I like to submit my picks each week and see how I do. This allows me to do it with as little effort as possible, consulting the experts and then making my own personal adjustments as I see fit.
