Cards :- Upgrades 1-7, Traps 8-14
```python
cards = {1:"V8 Engine", 2:"Carbon-fiber Chassis", 3:"Fix", 4:"Repair", 5:"Camera", 6:"Spare Parts", 7:"Asset", 
8: "Spikes", 9:"Weight", 10:"Explosive", 11:"Overheat", 12:"Reporter", 13:"Speed Limit", 14:"Liability"}
```
<h4>
  
  - V8Engine: +20 speed

  - Carbon-fiber Chassis: +30 speed, -10 health

  - Fix: removes DoT

  - Repair: +20 health

  - Camera: See opponent's hand

  - Spare Parts: Refresh deck

  - Asset: increase in all initial effects by +10. Doesn't work with Camera. If used with Spare Parts, allows you to play with refreshed cards. With Fix, protects from all traps

  - Spikes: -10 speed, -15, and -20 on subsequent turns
  - Hammer: -20 health
  - Explosive: -30 health, but, 50% chance on -10 on own health
  - Overheat: -25 health, then -10, and -5 on subsequent turns
  - Reporter: Remove rando card from opp
  - Speed Limit: If opp speed is above random limit, -30 speed. 50% chance to reduce your -10 of your speed if you're above limit
  - Liability: increases all initial effects by +10%. Doesn't increase recurring spikes effect and overheat effect
</h4>

## Inspiration
Our inspiration was merging two incompatible genres.
There are many card-based games, and a large amount of racing games.
We thought to combine these genres in a Card-Based Racing Game.

## What it does
The premise of the game is a race between two cars.
Each round, the player gets 3 random cards to choose from.
These cards can be used to upgrade & buff your car, or lay traps for your opponent.

## How we built it
Our game is built from scratch using the language Python.

## Challenges we ran into
Collaborating on a complex project was a challenge. 

## Accomplishments that we're proud of
We are proud of our comprehensive and efficient card system. 
Which allows for the game to be easily expanded.

## What we learned
We learnt about the importance of prior planning and strategy.

## What's next for Race of the Cards
We hope to expand the game with many more cards and game-modes,
and hope to bring life to it through better graphics.
