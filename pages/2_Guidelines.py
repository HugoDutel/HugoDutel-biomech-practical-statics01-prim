import streamlit as st

st.set_page_config(
    page_title="Guidelines",
    page_icon=":compass:",
    layout="wide"
)

st.title("Guidelines and tutorials 	:compass:")

st.markdown('''
You will find in this page resources for using Blender. 


**Blender** (https://www.blender.org/) is a free and open-source 3D computer graphic software application used for creating films, visual effects, etc. Blender has been already installed on the university computers. A live introduction to Blender will be done at the beginning of the practical. 


We will use Blender to **model the 3D morphology of the musculoskeletal system** based on surfaces of the skull generated from CT-scans. You are given a Blender project for each species that already contains the 3D surface of the mandible and cranium. We will build around these “dry skulls” the muscles, the joints, and the contact points where external forces are applied (i.e., in our case the bite point). 
The data extracted from Blender are the:
-	The 3D coordinates of the temporomandibular joint (TMJ);
-	The 3D coordinates of the bite point;
-	The 3D coordinates of the origin and insertion of muscles as well as their length.


These data will serve as an input for our static analysis (see Analyses page). You will save the measurements made in Blender into two **.csv files**: one for the geometrical data of the skeleton (joint and contact points), and one for the muscles. Templates of these .csv files are provided.
''')


st.image('mouse_lemur_muscles_small.jpg', caption='Musculoskeletal model of the mouse lemur. The muscles are represented by a series of strands. The different strand colours correspond to the different muscle groupes.')


st.header('Blender part 1: Building joints and contact points')
st.markdown('''This pdf provide you with a step-by-step tutorial for building the TMJ and bite point in Blender.

Link to the pdf: [Blender part 1 - Building joints and contact points](https://drive.google.com/file/d/1V6LiAphv5fxq8xOLHUP7zReVLdNn1cr4/view?usp=sharing)''') 

st.header('Blender part 2: Building muscles')
st.markdown('''
Muscles can insert on large areas and can have complex arrangements in 3D. To be modelled, they hence should be discretised into a **series of strands** that represent their **lines of action**, like in the figure above. The way these springs are set on the bones should reflect the area of origin and insertion of the muscle. Anatomical observations based on dissections and scans are therefore important to make modelling choices, and understand the limitations of the model (for instance see [Goening et al. 2013]( https://royalsocietypublishing.org/doi/full/10.1098/rsif.2013.0216?rfr_dat=cr_pub++0pubmed&url_ver=Z39.88-2003&rfr_id=ori%3Arid%3Acrossref.org)]. In our model, we will represent the muscles as straight lines connecting the origin (on the cranium) and insertion (on the mandible) areas.


Link to the pdf: [Blender part 2 - Building muscles](https://drive.google.com/file/d/1FxNO8gFp4NwPa3_4D678Ymdfz3p6Z0E9/view?usp=sharing)''') 

