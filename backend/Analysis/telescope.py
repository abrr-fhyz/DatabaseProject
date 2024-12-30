from pathlib import Path
from fastapi.responses import JSONResponse
import oracledb
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from config import database_config  


async def Telescope_image():
    
    image_path = 'D:/Year-2 Semester-2/CSE 2201/Project/images/Telescope_discovery.png'
    conn = database_config.get_connection() 
    cur = conn.cursor()

    sql_query = """
        select d.discovery_year, t.telescope_id, count(d.object_id) as number_of_discoveries
        from discovery d
        join telescope t on d.telescope_id = t.telescope_id
        group by d.discovery_year, t.telescope_id
        order by d.discovery_year, t.telescope_id
    """
    try:
        cur.execute(sql_query)
        result = cur.fetchall()
        data = [
            {'Discovery Year': i[0], 'Telescope Name': i[1], 'Number of Discoveries': i[2]}
            for i in result
        ]
        df = pd.DataFrame(data)
        df['Telescope-Year'] = df['Telescope Name'].astype(str) + '-' + df['Discovery Year'].astype(str)
        plt.figure(figsize=(12, 8))
        sns.set_theme(style="whitegrid")
        ax = sns.barplot(x='Telescope-Year', y='Number of Discoveries', data=df, palette='muted')
        ax.set_xlabel('Telescope and Discovery Year')
        ax.set_ylabel('Number of Discoveries')
        ax.set_title('Telescope Discoveries Over Time')
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(image_path)
        plt.close()

    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()

    return {
        "message": "Image created successfully"
        #"image_path": "http://127.0.0.1:8000/view-image"  
    }
