Shrinkage
=========

Todo:
Save to file, CSV

1. Specify File
1. Intergers or Numbers with Decimals
1. Show boards or not
1. Specify Shrinkage desired


## The Challenge 

Calculate the green composition for a load of lumber given the
dried composition for the same load of lumber and a desired shrinkage factor.

## Definitions   

Dried Composition = the lengths, thicknesses and count of all
actual boards in a load   Green Composition = the lengths, thicknesses and count
of all boards approximated prior to shrinking the load of lumber. Note: this
composition needs to work mathematically, not necessarily logically as one might
assume boards shrink :)   Load = a set of data describing a quantity of lumber
Bundle = a subset of a load   Board Feet = WIDTH/12*INCH*LENGTH*PIECES


## Inputs   

  1. A Load of Dried Composition lumber detailing the following data:

  2. Desired Shrinkage rate expressed as a percentage of total board feet for a
  load.

  3. Tolerances for results achieved outside of the desired shrinkage rate,
  likely to be expressed +/- 1% at both the load and bundle level.

## Outputs   

  1. A Load of Green Composition lumber "bloated" or pre-shrink.

  2. Actual Shrinkage rate for the load and for all bundles within the load.

## Restraints & Liberties   

  All outputs must be whole numbers.   Not all boards
must shrink. This is quite obviously, counterintuitive to how lumber must
actually shrink.   The desired shrinkage rate must be applied to each bundle
within a load and the desired tolerances must remain true at both the bundle and
load level.   The steps are written for inches being a constant of 2. Other
iterations are possible and may be needed to be factored into the steps later.
(I'm not sure if it is always 2, it just is in this example.

## Steps   

  1. If any of the INCH entries contain a number other than 2, give an
  error message saying so. If all entries contain 2, move to step 2.

  2. Calculate the board feet for the first bundle (or following bundle, if
  after the first iteration. in the Dried Composition load (the bundle ID will
  change when the next bundle starts..

  3. Calculate the desired board feet range for the Green Composition for the
  first bundle using the Desired Shrinkage Rate and Tolerance at the bundle
  level.

  4. Make the next to the widest board one foot wider (if after the first
  iteration, use the previous widest board you are considering.. Note that the
  total board feet for the bundle will change by a quantity of WIDTH/6 (this is
  the thing that would change if INCH entries vary from 2..

  5. Calculate the board feet resulting. If the board feet resulting is within
  the desired range, move onto the next bundle starting at step 2. If the result
  is lower than the desired range, repeat 4 using another of the longest pieces
  of lumber. If the result is higher than the desired range, move onto 6.

  6. Add one foot of length to the board that is smaller than the board you were
  just considering, then move to 5.

  7. When an iteration provides an answer within the desired tolerance, display
  the iteration's Green Composition along with the actual shrinkage as an output
  along with the actual shrinkage. If no iterations within a bundle provide an
  answer within the desired tolerance, display as an output the closest
  iteration's Green Composition along with the actual shrinkage.

  8. Perform steps 2-7 for each bundle within a load, then display a final total
  shrinkage and whether or not it meets the desired rate.
