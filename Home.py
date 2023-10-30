import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="👋",
    layout="wide"
)

st.title("Musculoskeletal modelling")
st.markdown("Dr Hugo Dutel")
st.markdown("h.dutel (at) bristol (dot) ac (dot) uk")

st.markdown("The objective of this practical is to discover and understand how principles from physics and engineering can be used to understand how animals work. As a case study, we will focus on two primate species: the mouse lemur (*Microcebus murinus*) and the crab-eating macaque (*Macaca fascicularis*). These two primate species belong to lineages that diverged at least 74 million-years ago during the Cretaceous period, and show conspicuous differences in morphology, ecology and diet.\n This webapp will allow you to calculate and compare the function of the jaw-closing system in these two species based on measurements made on 3D virtual models available during the practical, as well as data collected from quantitative dissections (see table in the Analysis section).\n You are encouraged to have a look at the maths behind the app before using it during the practical.")

st.image('primates.jpg', caption='Mouse lemur (left) and crab-eating macaque (right)', width=600, clamp=False, channels="RGB", output_format="auto")
