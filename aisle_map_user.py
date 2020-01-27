#import modules
import pandas as pd
import numpy as np
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
from matplotlib.colors import rgb2hex

#declare shelf break upcs
shelf_breaks = [77985, 77986, 77987, 77988, 77989, 77990, 77991, 77992, 77993, 77994, 77995, 77996, 77997, 77998, 77999]

#declare main function
def generate_heatmap():

    #read txt file containing UPC, amount of facings, brand, name, and size
    df = pd.read_csv('store_scan.txt', header=None, delimiter='\t')
    #counter for duplicate_upcs variable
    df_counter = 0

    #determine which upcs were scanned more than once, and copy them below each match
    duplicate_upcs = [df[1][df_counter] if df[1][df_counter] != 1 else 1 for df[1][df_counter] in df[1]]
    df = df.loc[np.repeat(df.index.values, duplicate_upcs)]

    #since the duplicate upcs have the same index, reset it
    df = df.reset_index()

    #drop previous index column
    df = df.drop(df.columns[[0]], axis=1)

    #name columns
    df.columns = ['UPC', 'Quantity', 'Brand', 'Name', 'Size']

    #declare columns for xciks abd yrows
    df['Yrows'] = 'Yrows'
    df['Xcols'] = 'XCols'

    #declare variables for following for loop.
    xcols = 1
    shelf_counter = 1

    #finds shelf breaks and increments xcols and shelf_counter based off the results of the if statement
    for idx, val in enumerate(df.itertuples()):
        if df.loc[idx, 'UPC'] in shelf_breaks:
            #If 599999333348 is found, then we're on a new shelf. Set its x and y value to 0, 0
            shelf_counter += 1
            xcols = 1
            df.loc[idx, 'Yrows'] = 0
            df.loc[idx, 'Xcols'] = 0
        else:
            #use shelf_counter as the yrow value and xcols as the xcol, then increment xcols
            df.loc[idx, 'Yrows'] = shelf_counter
            df.loc[idx, 'Xcols'] = xcols
            xcols += 1

    #remove values with shelf indicator UPCs and reindex the dataframe.
    df = df[(df !=77985).all(axis=1)]
    df = df[(df !=77986).all(axis=1)]
    df = df[(df !=77987).all(axis=1)]
    df = df[(df !=77988).all(axis=1)]
    df = df[(df !=77989).all(axis=1)]
    df = df[(df !=77990).all(axis=1)]
    df = df[(df !=77991).all(axis=1)]
    df = df[(df !=77992).all(axis=1)]
    df = df[(df !=77993).all(axis=1)]
    df = df[(df !=77994).all(axis=1)]
    df = df[(df !=77995).all(axis=1)]
    df = df[(df !=77996).all(axis=1)]
    df = df[(df !=77997).all(axis=1)]
    df = df[(df !=77998).all(axis=1)]
    df = df[(df !=77999).all(axis=1)]

    #reset the index once more
    df = df.reset_index()

    #declare df2, which reads text file containing UPCs and Sales quantity
    df2 = pd.read_csv('sales_data.txt', header=None, delimiter='\t')

    #name columns
    df2.columns = ['UPC', 'Sales']

    #set the index equal to the UPC column
    df2.set_index('UPC', inplace=True)
    #create new column in df mapped to df2 on UPC
    df['Sales'] = df.UPC.map(df2.Sales)

    #declare numpy array with UPC and Sales column
    upc = np.array(df['UPC'])
    sold = np.array(df['Sales'])
    #pivot the result using Yrows and Xcols columns
    result = df.pivot(index='Yrows', columns='Xcols', values='Sales')
    #establish figure
    fig, ax = plt.subplots(figsize=(12,7))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')
    sns.heatmap(result, annot_kws={"size": 7}, fmt="", cmap='RdYlGn', linewidths=2, ax = ax, square=True)

    #now that the figure is generated, declare colour_data, which will hold the values for each colour
    colour_data = sns.heatmap(result)

    im = colour_data.collections[0]

    #pull colour data using cmap
    rgba_values = im.cmap(im.norm(im.get_array()))
    rgba_values = np.delete(rgba_values, np.s_[3], axis=1)

    #rgba is now equal to a numpy array containing the rgb values
    rgba = np.array(rgba_values*255, dtype=int)

    #declare html
    html = """
<!DOCTYPE html>
<html>
<head>
<title>POM Aisle - Heat Map </title>
<style>
body {
  background-color: white;
  font-family: Verdana;
}

a {
 color: black;
}

a:link {
  text-decoration: none;
}

a:visited {
  text-decoration: none;
}

a:hover {
  text-decoration: none;
  }

a:active {
  text-decoration: none;
}

.topnav {
  background-color: #32393f;
  overflow: hidden;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
}

.topnav a {
  float: left;
  color: #f2f2f2;
  text-align: center;
  padding: 14px 16px;
  text-decoration: none;
  font-size: 16px;
}

.container {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.grid {
  display: grid;
  grid-template-columns: repeat("""+str(df['Xcols'].max()) + """, 100px );
  grid-template-rows: repeat("""+ str(df['Yrows'].max()) + """, 85px);
  position: fixed;
  top: 60px;
}

.grid span {
  overflow: hidden;
  padding: 2px; 2px;
  margin: 2px;
  font-size: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  justify-content: space-evenly;
}

</style>
</head>
<body>

<div class="topnav">
<a>Store Name</a>
</div>

<div class="container">
<div class="grid">
"""

    html_counter = 0

    for x in rgba:
        if x[0] == 0 and x[1] ==0 and x[2] == 0:

            html += """\
            <span style="background-color:rgba(160,173,173)"></span>"""

        else:

            html += """\
            <span style="background-color:rgba(""" + str(x[0]) + """,""" + str(x[1]) + """,""" + str(x[2]) + """)"><center> """+ str(df['Brand'][html_counter]) + """<br>""" + str(df['Name'][html_counter]) + """<br> """ + str(df['Size'][html_counter]) + """<br>""" + str(df['Sales'][html_counter]) + """</center></span>"""

            html_counter += 1

    html += """</div></div></body></html>"""
    html_file = open("heatmap.html", "w")
    html_file.write(html)
    html_file.close()


#call the function
generate_heatmap()
