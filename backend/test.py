import asyncio
from Analysis.Coordinate_plot import Coordinateshow
from Analysis.stellarDist import analyze_stellar_dist
from Analysis.telescope import Telescope_image
from Analysis.planetsys import analyze_planetary_systems

async def coor():
    star_system = "Omega Nexus"
    result = await Coordinateshow(star_system)
    print(result)

async def stdist():
    result = await analyze_stellar_dist()
    print(result)

async def tele():
    result = await Telescope_image()
    print(result)

async def plnt():
    result = await analyze_planetary_systems()
    print(result)

if __name__ == "__main__":
    asyncio.run(coor())