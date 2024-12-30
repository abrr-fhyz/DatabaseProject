import oracledb
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import asyncio

from config import database_config  

def plot_coordinates(planet_names, ra_values, dec_values, star_system, image_path):
    """
    This function handles the blocking matplotlib code in a separate thread to avoid async issues.
    """
    plt.figure(figsize=(10, 6))
    plt.scatter(ra_values, dec_values, color='skyblue')
    for i, planet in enumerate(planet_names):
        plt.text(ra_values[i], dec_values[i], planet, fontsize=9, ha='right')

    plt.xlabel('Right Ascension (RA) in Degree')
    plt.ylabel('Declination (DEC) in Degree')
    plt.title(f'Planet Coordinates in the {star_system}')
    plt.tight_layout()

    plt.savefig(image_path)
    plt.close()

async def Coordinateshow(star_system: str):
    image_path = 'D:/Year-2 Semester-2/CSE 2201/Project/images/Coordinate_plot.png'

    try:
        with database_config.get_connection() as conn:
            with conn.cursor() as cur:
                # Check if the star system exists
                cur.execute("SELECT COUNT(*) FROM star_system WHERE system_name = :1", [star_system])
                if cur.fetchone()[0] == 0:
                    return {"message": f"Star system '{star_system}' does not exist."}

                # Query the planet coordinates
                sql_query = """
                    select planet_name, ra_coord right_ascension, dec_coord declination
                    from planet p
                    join coordinates c on p.object_id = c.object_id
                    where p.origin_system = :1
                """
                cur.execute(sql_query, [star_system])
                result = cur.fetchall()

                if not result:
                    return {"message": "No data available for the given star system."}

                planet_names = [row[0] for row in result]
                ra_values = [row[1] for row in result]
                dec_values = [row[2] for row in result]

                # Run the plotting code in the main thread using asyncio
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(None, plot_coordinates, planet_names, ra_values, dec_values, star_system, image_path)

                return {
                    "message": "Image created successfully"
                    # "image_path": "http://127.0.0.1:8000/view-image-Coordinate"
                }

    except Exception as e:
        return {"message": f"An error occurred during processing: {e}"}
