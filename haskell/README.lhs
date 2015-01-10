===============================
 Algorithms.SpaceFillingCurves
===============================

How to use
----------

> import Data.SpaceFillingCurves
>
> -- An example Hilbert curve
> h :: [(Float, Float)]
> h = hilbert 2 0 0 4 0 0 4
>
> -- An example Moore curve
> m :: [(Float, Float)]
> m = moore 2 0 0 4 0 0 4

Printing the two curves:

> showCoords :: [(Float, Float)] -> String
> showCoords xs = concatMap format xs
>  where
>    format (a, b) = (show a) ++ " " ++ (show b) ++ "\n"
>
> main :: IO ()
> main = do
>    putStrLn "Hilbert:"
>    putStr (showCoords $ h)
>    putStrLn "Moore:"
>    putStr (showCoords $ m)
