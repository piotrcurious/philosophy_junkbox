{-# LANGUAGE DeriveGeneric #-}
module Main where

import GHC.Generics
import Data.List (intercalate)
import System.IO
import System.Environment (getArgs)
import Text.Read (readMaybe)

-- High dimensional psychogeographical node point (10 dimensional manifold vector)
data DriftPoint = DriftPoint
  { pointId      :: String
  , pointName    :: String
  , posX         :: Double
  , posY         :: Double
  , posZ         :: Double
  , temperature  :: Double
  , humidity     :: Double
  , commercialVal:: Double
  , accessibility:: Double
  , symbolicVal  :: Double
  , thermalStress:: Double
  , flowDensity  :: Double
  } deriving (Show, Generic)

-- Archetype Trajectories
data Archetype = Tourist | Worker | Resident | Surveillance | CustomArchetype String
  deriving (Eq)

instance Show Archetype where
  show Tourist = "Tourist"
  show Worker  = "Worker"
  show Resident = "Resident"
  show Surveillance = "Surveillance"
  show (CustomArchetype name) = name

nodeData :: [DriftPoint]
nodeData =
  [ DriftPoint "underground" "Underground Metro Connection"         0.0  (-10.0) 0.0  24.5 0.75 0.20 0.90 0.20 0.30 0.85
  , DriftPoint "boulevard"   "Boulevard Haussmann Ground Entrance" 10.0   0.0   5.0  33.0 0.45 0.90 0.85 0.80 0.85 0.95
  , DriftPoint "vip_salon"   "VIP Personal Shopping Salons"       15.0  20.0  12.0  21.0 0.50 0.95 0.20 0.90 0.15 0.25
  , DriftPoint "coupole"     "Historic Glass Coupole Dome"         0.0  40.0   8.0  28.5 0.55 0.70 0.70 0.95 0.55 0.75
  , DriftPoint "glasswalk"   "Glasswalk Suspended Runway"          5.0  50.0  10.0  29.5 0.50 0.85 0.40 0.90 0.60 0.80
  , DriftPoint "rooftop"     "Rooftop Terrace & Microclimate"      0.0  70.0  15.0  36.0 0.30 0.40 0.60 0.85 0.90 0.60
  ]

-- Distance in 10D space
distance10D :: DriftPoint -> DriftPoint -> Double
distance10D p1 p2 = sqrt $ sum
  [ (posX p1 - posX p2)**2
  , (posY p1 - posY p2)**2
  , (posZ p1 - posZ p2)**2
  , (temperature p1 - temperature p2)**2
  , (humidity p1 - humidity p2)**2
  , (commercialVal p1 - commercialVal p2)**2
  , (accessibility p1 - accessibility p2)**2
  , (symbolicVal p1 - symbolicVal p2)**2
  , (thermalStress p1 - thermalStress p2)**2
  , (flowDensity p1 - flowDensity p2)**2
  ]

-- Cumulative trajectory path length
trajectoryPathLength :: [DriftPoint] -> Double
trajectoryPathLength points = sum $ zipWith distance10D points (tail points)

-- Non-linear interpolation between 2 points in 10D space with non-linear warping factor
interpolate10D :: DriftPoint -> DriftPoint -> Double -> Double -> DriftPoint
interpolate10D p1 p2 t warp =
  let tWarped = t ** warp
      interp a b = a + (b - a) * tWarped
  in DriftPoint
       { pointId       = pointId p1 ++ "_" ++ pointId p2 ++ "_" ++ show (floor (t * 100) :: Int)
       , pointName     = "Interpolated Waypoint"
       , posX          = interp (posX p1) (posX p2)
       , posY          = interp (posY p1) (posY p2)
       , posZ          = interp (posZ p1) (posZ p2)
       , temperature   = interp (temperature p1) (temperature p2)
       , humidity      = interp (humidity p1) (humidity p2)
       , commercialVal = interp (commercialVal p1) (commercialVal p2)
       , accessibility = interp (accessibility p1) (accessibility p2)
       , symbolicVal   = interp (symbolicVal p1) (symbolicVal p2)
       , thermalStress = interp (thermalStress p1) (thermalStress p2)
       , flowDensity   = interp (flowDensity p1) (flowDensity p2)
       }

-- Generate full trajectory curve for a given archetype path with configurable step resolution
generateTrajectory :: Archetype -> [DriftPoint] -> Double -> Double -> [DriftPoint]
generateTrajectory arch points stepRes warp =
  let steps = [0.0, stepRes .. 0.999]
      pairs = zip points (tail points)
  in concatMap (\(p1, p2) -> map (\t -> interpolate10D p1 p2 t warp) steps) pairs ++ [last points]

pointToCSVRow :: Archetype -> DriftPoint -> String
pointToCSVRow arch p = intercalate ","
  [ show arch
  , pointId p
  , "\"" ++ pointName p ++ "\""
  , show (posX p)
  , show (posY p)
  , show (posZ p)
  , show (temperature p)
  , show (humidity p)
  , show (commercialVal p)
  , show (accessibility p)
  , show (symbolicVal p)
  , show (thermalStress p)
  , show (flowDensity p)
  ]

csvHeader :: String
csvHeader = "archetype,id,name,posX,posY,posZ,temperature,humidity,commercialVal,accessibility,symbolicVal,thermalStress,flowDensity"

main :: IO ()
main = do
  args <- getArgs
  let stepRes = case args of
                  (s:_) -> maybe 0.25 id (readMaybe s)
                  _     -> 0.25
      outFile = case args of
                  (_:f:_) -> f
                  _       -> "high_dim_trajectories.csv"

  let getNodes ids = map (\i -> head [n | n <- nodeData, pointId n == i]) ids
      touristPath      = generateTrajectory Tourist (getNodes ["boulevard", "coupole", "glasswalk", "rooftop"]) stepRes 1.2
      workerPath       = generateTrajectory Worker (getNodes ["underground", "boulevard", "rooftop"]) stepRes 0.8
      residentPath     = generateTrajectory Resident (getNodes ["underground", "boulevard", "rooftop"]) stepRes 1.5
      surveillancePath = generateTrajectory Surveillance (getNodes ["underground", "vip_salon", "glasswalk", "rooftop"]) stepRes 1.0

      tLen = trajectoryPathLength touristPath
      wLen = trajectoryPathLength workerPath

  putStrLn $ "[Haskell Engine] Tourist path 10D cumulative length: " ++ show tLen
  putStrLn $ "[Haskell Engine] Worker path 10D cumulative length: "  ++ show wLen

  let allRows = map (pointToCSVRow Tourist) touristPath
             ++ map (pointToCSVRow Worker) workerPath
             ++ map (pointToCSVRow Resident) residentPath
             ++ map (pointToCSVRow Surveillance) surveillancePath

  writeFile outFile (unlines (csvHeader : allRows))
  putStrLn $ "Successfully generated " ++ outFile ++ " with step resolution " ++ show stepRes
