-------------------------------------------------
-- |
-- Module      : Data.SpaceFillingCurves
-- Copyright   : (c) Raphael 'kena' Poss 2014
-- License     : Public domain (Unlicense)
--
-- Maintainer  : knz@thaumogen.net
-- Stability   : experimental
-- Portability : portable
--
-- Generators of space-filling curves.
-------------------------------------------------

module Data.SpaceFillingCurves (
  hilbert
, moore
) where

import Control.Applicative (Applicative(..), Alternative(..))

-- | Generate a Hilbert space-filling curve. (open curve)
--
-- The function generates 4^@n@ points, shifted from the origin
-- by (@x0@, @y0@). The pair (@xi@, @yi@) determines the planar
-- coordinates of the I vector ("X axis") and the pair (@xj@, @yj@)
-- the coordinates of the J vector ("Y axis").
hilbert :: (Eq n, Num n, Fractional f, Alternative p) => n -> f -> f -> f -> f -> f -> f -> p (f,f)
hilbert 0 x0 y0 xi xj yi yj = pure (x0 + (xi + yi) / 2, y0 + (xj + yj) / 2)
hilbert n x0 y0 xi xj yi yj = a <|> b <|> c <|> d
   where
     a = hilbert (n-1) (x0)           (y0)           (yi/2)  (yj/2)  (xi/2)  (xj/2)
     b = hilbert (n-1) (x0+xi/2)      (y0+xj/2)      (xi/2)  (xj/2)  (yi/2)  (yj/2)
     c = hilbert (n-1) (x0+xi/2+yi/2) (y0+xj/2+yj/2) (xi/2)  (xj/2)  (yi/2)  (yj/2)
     d = hilbert (n-1) (x0+xi/2+yi)   (y0+xj/2+yj)   (-yi/2) (-yj/2) (-xi/2) (-xj/2)

-- | Generate a Moore space-filling curve. (closed curve)
--
-- The function generates 4^@n@ points, shifted from the origin
-- by (@x0@, @y0@). The pair (@xi@, @yi@) determines the planar
-- coordinates of the I vector ("X axis") and the pair (@xj@, @yj@)
-- the coordinates of the J vector ("Y axis").
moore :: (Eq n, Num n, Fractional f, Alternative p) => n -> f -> f -> f -> f -> f -> f -> p (f,f)
moore 0 x0 y0 xi xj yi yj = pure (x0 + (xi + yi) / 2, y0 + (xj + yj) / 2)
moore n x0 y0 xi xj yi yj = a <|> b <|> c <|> d
   where
     a = hilbert (n-1) (x0+xi/2)       (y0+xj/2)      (-xi/2) (xj/2) (yi/2) (yj/2)
     b = hilbert (n-1) (x0+xi/2+yi/2)  (y0+xj/2+yj/2) (-xi/2) (xj/2) (yi/2) (yj/2)
     c = hilbert (n-1) (x0+xi/2+yi)    (y0+xj/2+yj)   (xi/2)  (xj/2) (yi/2) (-yj/2)
     d = hilbert (n-1) (x0+xi/2+yi/2)  (y0+xj/2+yj/2) (xi/2)  (xj/2) (yi/2) (-yj/2)
