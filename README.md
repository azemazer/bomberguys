# Bomberguys 💣

 Bomberguys is a top-down bomberman-like made with the core rules of PytactX, a game engine developed to help learn development by Jusdeliens. Visit them [here](https://jusdeliens.com)

## Context 🔭

During my development courses, we had to create a game using Jusdeliens' PytactX. It came with a set of constraints, as using any game engine does. I decided to go with a Bomberman-like since the rules are quite simple and I really like this kind of game. 

## Rules 📜

### Components of the game

[Maquette](./bomberguys_maquette.JPG)

In this preview of the arena, you can see the multiple elements composing Bomberguys:

- 🔴: Team 1 agents
- 🟢: Team 2 agents
- ⬛: Iron blocks (unbreakable)
- 🟫: Stone block (breakable)
- ⬛ (but blacker): Bomb
- 🟥: Explosion radius

(the two empty squares at the far right and far left are meant for the pysical version of the game)

### How to play

You are a bomberguy and you and your team have to get rid of the other team. How? By placing bombs that kill players and destroy stone blocks!

$Be$ $careful!$ Friendly fire is enabled, and you can also kill yourself!

### Endgame
The game ends when a team is the last team standing. This team wins, and the game is then restarted.

## Use cases 👨‍👧

### Admin

As an admin of the game, you need to go to src/serv/main.py, fill in your credentials at the Referee creation and you're good to go. You can also put: 
- a custom rate of stone block spawn (from 0.0 to 1, but it' recommended to put a value between 0.2 and 0.5. Default 0.4). Name of the parameter: stoneBlockFrequency
- a custom bomb lifetime (any int from 1 to 100 is accepted, but 100 is very long. recommended between 5 to 20. Default: 10). Name of the parameter: bombCountdown

### Player

Players should read the Player readme (COMING SOON).

## Material architecture 🏢

The material arcitecture of the game and PytactX can be represented by this diagram: 

[![](https://mermaid.ink/img/pako:eNrNVttuGjEQ_ZWJpbSgbhIIt2alJkoaHpAaJRLpJS19MLsDrNi1qe2F0Cj_3rF3CRtCbm0qhQdkjeecmTnHBl-xQIbIfKbxV4oiwOOIDxVPegLos7kJhwoF_xLhDNXW_v67IyXHqHxoa8P7caRHkRjCDPtaBmM0EEghMDCRFDcEGWKLwFsFLh_OU0qNARdEGGaQVGeVTqf88KzjLyhL5Ww7Cxdb6aIIQdn2tYFSnp5n58UL2R9HGIxdEcETBE7YCdd6JlW4CumimrpOFRc6iYyxs95TKMstorJCnWOIxECuJh0OUZgTUj6mRIXcoAZuY5RNgpAPtxBWvOK4tpGhbZ9yDd7quyjd50lI2yAHOfebB0C3zVkilwg3iEq4dReMhDDSk5jPe2K9b4mc4lNNs7nl58lfgNzVPuDihPbhAwhpwGCME6mM69xzIZkaO1xfpiLUWagf2yMcPkZ5kJcG36Hs2oM0k2tV3fV-59p-c2fv4l6fde5zQXX9Op2eSI1HMuk_1e1F_jMdX4GtF5dsOsvzrFWBlHEoZ4JYeDjPkct8q8aNwe4aWqDbL5Vhxzm8KPuYy6_du4Izlsia6EMHBkg_wkM7uzuPoRRImBCI767yG4sjcPd-WL6O7oj25SSW2hY_cLHjCOmq_Jt0UJrLFLiizshGr_Bd_itVobQW-9Lino9kOhwZsM0TJcJIGg-GpKmG2YjTmnbeUpyO2QPKShHPTwWeI0-69Nfg1DmAmGtTDH2ljl5G5xkx7QCZuPLfVrzQnSJqKQSUfhjq6afleIo1RUumUWCkmlNpG22L_-_PBQ1Lsu24xSead4N5LEHCRyG9iK4srMfMCBPsMZ-WIVfjHuuJa8rjqZHduQiYP-CxRo9l0ufPp5vohAvmX7FL5te291rVZrVS2a3Xdlt71WbLY3Pm1xvbjVqr1mw1q81KtVKrX3vst5TEUN2uVRoE2a3uVd43G_VKzdF9d5tGpcSOYUSanWQvOPeQu_4Dc6dExw?type=png)](https://mermaid.live/edit#pako:eNrNVttuGjEQ_ZWJpbSgbhIIt2alJkoaHpAaJRLpJS19MLsDrNi1qe2F0Cj_3rF3CRtCbm0qhQdkjeecmTnHBl-xQIbIfKbxV4oiwOOIDxVPegLos7kJhwoF_xLhDNXW_v67IyXHqHxoa8P7caRHkRjCDPtaBmM0EEghMDCRFDcEGWKLwFsFLh_OU0qNARdEGGaQVGeVTqf88KzjLyhL5Ww7Cxdb6aIIQdn2tYFSnp5n58UL2R9HGIxdEcETBE7YCdd6JlW4CumimrpOFRc6iYyxs95TKMstorJCnWOIxECuJh0OUZgTUj6mRIXcoAZuY5RNgpAPtxBWvOK4tpGhbZ9yDd7quyjd50lI2yAHOfebB0C3zVkilwg3iEq4dReMhDDSk5jPe2K9b4mc4lNNs7nl58lfgNzVPuDihPbhAwhpwGCME6mM69xzIZkaO1xfpiLUWagf2yMcPkZ5kJcG36Hs2oM0k2tV3fV-59p-c2fv4l6fde5zQXX9Op2eSI1HMuk_1e1F_jMdX4GtF5dsOsvzrFWBlHEoZ4JYeDjPkct8q8aNwe4aWqDbL5Vhxzm8KPuYy6_du4Izlsia6EMHBkg_wkM7uzuPoRRImBCI767yG4sjcPd-WL6O7oj25SSW2hY_cLHjCOmq_Jt0UJrLFLiizshGr_Bd_itVobQW-9Lino9kOhwZsM0TJcJIGg-GpKmG2YjTmnbeUpyO2QPKShHPTwWeI0-69Nfg1DmAmGtTDH2ljl5G5xkx7QCZuPLfVrzQnSJqKQSUfhjq6afleIo1RUumUWCkmlNpG22L_-_PBQ1Lsu24xSead4N5LEHCRyG9iK4srMfMCBPsMZ-WIVfjHuuJa8rjqZHduQiYP-CxRo9l0ufPp5vohAvmX7FL5te291rVZrVS2a3Xdlt71WbLY3Pm1xvbjVqr1mw1q81KtVKrX3vst5TEUN2uVRoE2a3uVd43G_VKzdF9d5tGpcSOYUSanWQvOPeQu_4Dc6dExw)

Python was used to program the agents since PytactX requires it.

## Pre-requisites ☑

- Python 3.12 or higher
- An arena in Pytactx

## Installation 🔧

Installation of necesary packages automatically occur when an agent is created.

## Test 🧪

No tests implemented yet. (SOON™)

## Author

PytactX : Julien Arné

Bomberguys: Azemazer

## Licence

MIT License.