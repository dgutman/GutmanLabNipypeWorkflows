## To do list
Basic steps are:

1)  Load a sparse matrix encoded .DOT file file...  this has 3 values per row,  srcID, tgtID and Connectivity
For now, we want to load this into a regular numpy array, although in the future we may want to consider using 
a specific class of Numpy array that is optimized for Sparse Matrices...

2)  I think we want to scan for the MAX value of the connectivity matrix and recase the entire matrix accordingly.. most
likely uint8 or uint16 should work, the 0.5's in the connectivity scores are meaningless


3)  Want to evaluate a couple of things..

   a) Keep track of how long it takes to load the .DOT files  (aka timeit)
   b) Look into saving the matrices as hdf files (will be DASK friendly)
   
4)  There are MULTIPLE ways we can do "sanity" checks on the arrays--- 
   Want to experiment with
      1) Simple MatPlotLib/interact widget to look at the array data sliced various ways...
      
      2)  Look into PAPAYA  
      https://github.com/akeshavan/nbpapaya
      
      also check out:
      https://gist.github.com/armaneshaghi/2645723a28df96795aaa
      
      and 
      https://www.datacamp.com/community/tutorials/matplotlib-3d-volumetric-data
      
      https://github.com/rii-mango/Papaya   We already got this working in Juputer, although probably should add to readme
      exactly how we did this
       and..
       http://kevin-keraudren.blogspot.com/2013/12/xtk-and-mutant-mice-embryos.html
      
5)  Need to work on a separate function that maps the "matrix encoded" data back into an actual brain space.. so
rembember in the DOT file I referenced above, we essentially have a srcID, tgtID and then connectivity
srcID is actually a label inded and references back to a specific x,y,z coordinate in the original brain space.

What we need to be able to do, is for a given srcID, I want to plot every tgtID it reaches.... so first
  a) We do it in the goofy matrix space, this is those plots I showed yesterday
  b) more interestingly, we have a separate npArray that is in the proper 'shape'.. basically this should be a 3d matrix that 
  is the original brain we used for all of our analysis..
  
  We want to EFFICIENTLY slice the connectivity MAtrix and then copy/map the relevent data into the BRAIN space array
  
  
  So what you see is the actual lab map... which is stored in coords_for_fdt_matrix3   So let's say we slice the connecitivty matrix referenced about at srcID = 10;  this means the connectivity matrix was seeded from/initiated at coordinates 10,28,3 
  
  What we want to do is put a BLUE dot at this original seed point, and then for every other regoin that this seed connects to we want to put a RED dot (or more likely use a color map)...  this represents the connectivity matrix from srcID=10 to the rest of the brain... having a widget that allows us to play around with this data will be VERY helpful
  
<b>coords_for_fdt_matrix3  </b>
  
16  22  1  0  1  
11  31  2  0  2  
12  31  2  0  3  
11  32  2  0  4  
12  32  2  0  5  
11  33  2  0  6  
12  33  2  0  7  
10  27  3  0  8  
9  28  3  0  9  
10  28  3  0  10  


   
