import os
import oracledb
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from config import database_config

async def analyze_stellar_dist():
    conn = database_config.get_connection()
    cur = conn.cursor()

    sql_query = """
    with star_discoveries as (
        select s.stellar_class as stellar_class,
               count(*) as star_count,
               avg(s.solar_mass) as avg_mass,
               avg(s.luminosity) as avg_luminosity,
               max(d.discovery_year) as latest_discovery
        from star s
        left join discovery d on s.object_id = d.object_id
        group by s.stellar_class
    ),
    system_stats as (
        select ss.system_type,
               count(DISTINCT s.object_id) as total_stars,
               count(DISTINCT p.object_id) as total_planets
        from star_system ss
        left join star s on ss.system_name = s.origin_system
        left join planet p on ss.system_name = p.origin_system
        group by ss.system_type
        having count(DISTINCT s.object_id) > 0
    )
    select sd.stellar_class,
           sd.star_count,
           sd.avg_mass,
           sd.avg_luminosity,
           sd.latest_discovery,
           ss.total_planets
    from star_discoveries sd
    join system_stats ss on 1=1
    order by sd.stellar_class
    """

    try:
        cur.execute(sql_query)
        col_names = [desc[0] for desc in cur.description]  
        results = cur.fetchall()
        df = pd.DataFrame(results, columns=col_names) 
        #print(df.head())
        #print(df.columns)


    except Exception as e:
        print(f"Problem executing SQL query from StellarDistFile: {e}")
        return
    finally:
        cur.close()
        conn.close()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    df.columns = [col.lower() for col in df.columns]
    sns.scatterplot(
        data=df,
        x='avg_mass',
        y='avg_luminosity',
        size='star_count',
        hue='stellar_class',
        ax=ax1,
        palette='viridis'
    )
    ax1.set_title('Star Distribution by Mass and Luminosity')
    ax1.set_xlabel('Average Solar Mass')
    ax1.set_ylabel('Average Luminosity')
    ax1.legend(title='Stellar Class', bbox_to_anchor=(1.05, 1), loc='upper left')

    sns.barplot(
        data=df,
        x='stellar_class',
        y='latest_discovery',
        palette='coolwarm',
        ax=ax2
    )
    ax2.set_title('Latest Discovery Year by Stellar Class')
    ax2.set_xlabel('Stellar Class')
    ax2.set_ylabel('Year')

    plt.tight_layout()

    image_path = 'D:/Year-2 Semester-2/CSE 2201/Project/images/StellerDist.png'

    if not os.path.exists(os.path.dirname(image_path)):
        os.makedirs(os.path.dirname(image_path))

    try:
        plt.savefig(image_path)
        print(f"Image saved to {image_path}")
    except Exception as e:
        print(f"Error saving image: {e}")

    plt.close()

    return {
        "message": "Image created successfully"
        # "image_path": "http://127.0.0.1:8000/show-image-Planetsys"
    }
