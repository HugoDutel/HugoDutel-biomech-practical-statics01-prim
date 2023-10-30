import streamlit as st
import pandas as pd
import numpy as np
from . import fun_static_model as fsm
import altair as alt

st.set_page_config(
    page_title="Analyses",
    page_icon=":bar_chart:",
    layout="wide"
)

st.title('Analyses')

st.header('Jaw muscle morphology of primates  :monkey_face:')
st.markdown("Our objective is to calculate the forces and joint moment acting on the mandible during an incisor bite. Prior to modelling, data on the morphology of the species were collected during quantitative dissections and CT-scans of the head of each species were performed. The **head width** and **lower jaw length** (in mm) and **muscle physiological cross section areas** (PCSA, cm<sup>2</sup>) for the three muscle groups in each species are listed in the table below.", unsafe_allow_html=True)

data_morpho = pd.DataFrame({'species':['M. fascicularis', 'M. murinus'], 'head_width':[58, 22], 'lower_jaw_length':[53, 22], 'pcsa_masseter':[2.417, 0.664*1.2], 'pcsa_pterygoid_medial':[1.11, 0.146*1.2], 'pcsa_temporalis':[3.596*1.1, 0.623*1.2], 'pcsa_total':[7.123, 1.433*1.2]})
st.table(data_morpho)

st.header('Load your measurements  :straight_ruler:')
st.write("First upload the table containing the muscule coordinates and PCSA, and then the table containing the coordinates of the jaw joint and bite point.")
muscle_file = st.file_uploader("Table containing the muscle data", accept_multiple_files=False)
geom_file = st.file_uploader("Table containing the joint data", accept_multiple_files=False)

column1, column2 = st.columns(2)

if (muscle_file and geom_file) is not None:
    
    df_muscle = pd.read_csv(muscle_file)
    df_geom = pd.read_csv(geom_file)

    grouped_pcsa = data_morpho.groupby(['species'])
    grouped_muscle = df_muscle.groupby(['species'])
    grouped_geom = df_geom.groupby(['species'])

    # add the pcsa to the coordinate table
    
    list_df_muscle_pcsa = []
    for i in grouped_muscle.groups:
        df_muscle_pcsa_i = fsm.fun_insert_pcsa(grouped_muscle.get_group(i), grouped_pcsa.get_group(i))
        list_df_muscle_pcsa.append(df_muscle_pcsa_i)
        
    df_muscle_pcsa = pd.concat(list_df_muscle_pcsa)

    st.write("---")
    st.header('Overview of the uploaded data  :mag_right:')
    st.write("You can assess in each tab the measurements you uploaded. For each muscle, the PCSA was divided by the number of strands representing the line of action and added as the last column in Muscle Table.")
    tab1, tab2 = st.tabs(['Muscle Tabe', 'Point Table'])
    with tab1:
        st.write(df_muscle_pcsa)   
    with tab2:
        st.write(df_geom)

    # static model: initial conditions
    with st.sidebar:
        st.title("Simulation Parameter  :gear:")
        st.markdown("Define the initial conditions and parameters of your model:")
        measur_sides = st.selectbox('**Number of sides** on the cranium where the measurments have been made', (1, 2))
        gape_max = st.number_input('**Maximum gape angle (degrees)**: the model calculates the static equilibrium for each degree from 0 to the maximum gape angle.', value=0, min_value=0, step=1)
        f_fibre_max = st.number_input('**Maximum muscle fibre strength (N/cm²)**: how much force an individual muscle fibre can generate.', value=25, min_value=18, step=1)
        
    # st.write("---")
    # st.header('Static model parameters')
    # st.write("Once you have checked that your data tables are fine, you can define the initial conditions and parameters of your model.")
    # measur_sides = st.selectbox('**Number of sides** on the cranium where the measurments have been made', (1, 2))
    # gape_max = st.number_input('**Maximum gape angle (degrees)**: the model calculates the static equilibrium for each degree from 0 to the maximum gape angle.', value=0, min_value=0, step=1)
    # f_fibre_max = st.number_input('**Maximum muscle fibre strength (N/cm^2)**: how much force an individual muscle fibre can generate.', value=25, min_value=18, step=1)

    grouped_df_muscle_pcsa = df_muscle_pcsa.groupby(['species'])
    
    list_freac = []
    list_muscle_force = []
    list_muscle_resultant = []
    list_muscle_strain = []
    list_muscle_mom = []
    list_muscle_mom_arm = []
    
    for i in grouped_df_muscle_pcsa.groups:
       freac, muscle_force, muscle_resultant, muscle_strain, muscle_mom, muscle_mom_arm = fsm.bite_model(grouped_df_muscle_pcsa.get_group(i), grouped_geom.get_group(i), gape_max, f_fibre_max, measur_sides)
       list_freac.append(freac)
       list_muscle_force.append(muscle_force)
       list_muscle_resultant.append(muscle_resultant)
       list_muscle_strain.append(muscle_strain)
       list_muscle_mom.append(muscle_mom)
       list_muscle_mom_arm.append(muscle_mom_arm)

    df_freac = pd.concat(list_freac)
    df_muscle_force = pd.concat(list_muscle_force)
    df_muscle_resultant = pd.concat(list_muscle_resultant)
    df_muscle_strain = pd.concat(list_muscle_strain)
    df_muscle_mom = pd.concat(list_muscle_mom)
    df_muscle_mom_arm = pd.concat(list_muscle_mom_arm)

    # summary table of the static model
    
    df_bite_model_summary = fsm.LeverParamMaxBiteForce(df_freac, df_muscle_force)
    df_bite_model_summary_melt = df_bite_model_summary.melt(id_vars=['species', 'gape_angle', 'gape_h', 'variable'], 
                                                        value_vars=df_bite_model_summary.drop(['species', 'gape_angle', 'gape_h', 'variable'], axis=1).columns,
                                                        var_name='bite_point', value_name='value')
    #st.write(df_bite_model_summary_melt)
    
    # plots absolute values
    
    plot_pcsa = alt.Chart(data_morpho).mark_bar(size=60, opacity=0.8
    ).encode(
        x=alt.X('species', axis=alt.Axis(title='Species', domain=False, tickSize=0, labelPadding=10, titlePadding=20)),
        y=alt.Y('pcsa_total', axis=alt.Axis(title='PCSA total (cm²)', domain=False, tickSize=5, labelPadding=10, titlePadding=20)),
        color = alt.Color('species', legend=None).scale(scheme='dark2'),
        text='species'
    ).properties(
        width=500,
        height=400
    ).configure_axis(
        labelFontSize=14,
        titleFontSize=16,
        labelAngle = 0
    )

    plot_Biteforce = alt.Chart(np.round(df_bite_model_summary_melt[df_bite_model_summary_melt['variable'] == 'BfMag'], 2)).mark_bar(size=60, opacity=0.8
    ).encode(
        x=alt.X('species', axis=alt.Axis(title='Species', domain=False, tickSize=0, labelPadding=10, titlePadding=20)),
        y=alt.Y('value', axis=alt.Axis(title='Bite force (N)', domain=False, tickSize=5, labelPadding=10, titlePadding=20)),
        color = alt.Color('species', legend=None).scale(scheme='dark2'),
        text='species'
    ).properties(
        width=500,
        height=400
    ).configure_axis(
        labelFontSize=14,
        titleFontSize=16,
        labelAngle = 0
    )

    st.write("---")
    st.header('Results  :bar_chart:')
    st.write("We start examining the first results.\n 1) What can you say about the feeding function of each species based on the plots below?\n 2) Based on the *in vivo* measurements presented in [Chazeau et al. (2012) *J. Zoology*](http://www.anthonyherrel.fr/publications/Chazeau%20et%20al%202013%20J%20Zool.pdf) (hint: look at Figure 2), how would you evaluate the validity of the model of *M. murinus*?\n 3) Do you think that the measurements plotted below are comparable between the different species?")
    
    cc1, cc2 = st.columns([1,1])
    with cc1:
        st.altair_chart(plot_pcsa, theme=None)
    with cc2:
        st.altair_chart(plot_Biteforce, theme=None)

    answer_1 = st.text_area("Type your answer and validate with Crtl+Enter", max_chars = 500, key = "answer_1")
    st.write(f'You wrote {len(answer_1)} characters.')

    button_clicked = False
    if st.button('Next'):
        st.write("Comparing the muscle PCSA and bite force is a bit difficult here because of important differences in head dimensions between the two species. For instance, the head width of the macaque is more than twice that of the mouse lemur. We hence need to standardise our measurements to interpret the results.\n Here, we will choose the lower jaw length (in mm) to standardise the results. The biting efficiency was calculated by dividing the bite force by the total muscle force: this is equivalent to the mechanical advantage. \n 1) How has the standardisation changed the previous results?\n 2) One of the two species shows a greater scaled bite force, how do you think it is achieved?\n")

        # select a measurment to normalise the data
        
        option_head_measurment = data_morpho.columns[2]
  
        # # normalise data to head dimension

        df_morpho_norm = fsm.fun_normalise_pcsa_hw(data_morpho, option_head_measurment)
        df_morpho_norm['pcsa_total'] = np.round(df_morpho_norm['pcsa_total'], 2)
        
        df_freac_norm = fsm.fun_batch_normalise_with_hw(df_freac, data_morpho, option_head_measurment)
        
        df_muscle_force_norm = fsm.fun_batch_normalise_with_hw(df_muscle_force, data_morpho, option_head_measurment)

        df_muscle_mom_arm_norm = fsm.fun_batch_normalise_with_hw(df_muscle_mom_arm, data_morpho, option_head_measurment)
        
        df_bite_model_norm_summary = fsm.LeverParamMaxBiteForce(df_freac_norm, df_muscle_force_norm)
        df_bite_model_norm_summary_melt = df_bite_model_norm_summary.melt(id_vars=['species', 'gape_angle', 'gape_h', 'variable'], 
                                                        value_vars=df_bite_model_norm_summary.drop(['species', 'gape_angle', 'gape_h', 'variable'], axis=1).columns,
                                                        var_name='bite_point', value_name='value')


        #st.write(df_freac, df_muscle_mom, df_muscle_mom_arm, df_muscle_mom_arm_norm.groupby('species').first())

        # plot the normalised data 

        plot_pcsa_norm = alt.Chart(df_morpho_norm).mark_bar(
            size=60, opacity=0.8
        ).encode(
            x=alt.X('species', axis=alt.Axis(title='Species', domain=False, tickSize=0, labelPadding=10, titlePadding=20)),
            y=alt.Y('pcsa_total', axis=alt.Axis(title='PCSA^0.5/Lower jaw length', domain=False, tickSize=5, labelPadding=10, titlePadding=20)),
            color = alt.Color('species', legend=None).scale(scheme='dark2'),
            text='species'
        ).properties(
            width=500,
            height=400
        ).configure_axis(
            labelFontSize=14,
            titleFontSize=16,
            labelAngle = 0
        )

        plot_Biteforce_norm = alt.Chart(np.round(df_bite_model_norm_summary_melt[df_bite_model_norm_summary_melt['variable'] == 'BfMag'], 2)).mark_bar(
            size=60, opacity=0.8
        ).encode(
            x=alt.X('species', axis=alt.Axis(title='Species', domain=False, tickSize=0, labelPadding=10, titlePadding=20)),
            y=alt.Y('value', axis=alt.Axis(title='Bite force/Lower jaw length', domain=False, tickSize=5, labelPadding=10, titlePadding=20)),
            color = alt.Color('species', legend=None).scale(scheme='dark2'),
            text='species'
        ).properties(
            width=500,
            height=400
        ).configure_axis(
            labelFontSize=14,
            titleFontSize=16,
            labelAngle = 0
        )

        plot_BitingEff = alt.Chart(np.round(df_bite_model_summary_melt[df_bite_model_summary_melt['variable'] == 'BitingEff'], 2)).mark_bar(
            size=60, opacity=0.8
        ).encode(
            x=alt.X('species', axis=alt.Axis(title='Species', domain=False, tickSize=0, labelPadding=10, titlePadding=20)),
            y=alt.Y('value', axis=alt.Axis(title='Biting efficiency', domain=False, tickSize=5, labelPadding=10, titlePadding=20)),
            color = alt.Color('species', legend=None).scale(scheme='dark2'),
            text='species'
        ).properties(
            width=500,
            height=400
        ).configure_axis(
            labelFontSize=14,
            titleFontSize=16,
            labelAngle = 0
        )

        df_muscle_mom_arm_norm_sb = df_muscle_mom_arm_norm.drop_duplicates('species')
        plot_outLeverLengthNorm = alt.Chart(np.round(df_muscle_mom_arm_norm_sb, 2)).mark_bar(
            size=60, opacity=0.8
        ).encode(
            x=alt.X('species', axis=alt.Axis(title='Species', domain=False, tickSize=0, labelPadding=10, titlePadding=20)),
            y=alt.Y('outlever_length', axis=alt.Axis(title='Out-lever length/Lower jaw length', domain=False, tickSize=5, labelPadding=10, titlePadding=20)),
            color = alt.Color('species', legend=None).scale(scheme='dark2'),
            text='species'
        ).properties(
            width=500,
            height=400
        ).configure_axis(
            labelFontSize=14,
            titleFontSize=16,
            labelAngle = 0
        )
        
        plot_scatter_mom_arm = alt.Chart(df_muscle_mom_arm_norm).mark_circle(
            size=60, opacity=0.8
        ).encode(
            x=alt.X('gape_angle', axis=alt.Axis(title='Gape angle (degree)', domain=False, tickSize=0, labelPadding=10, titlePadding=20)),
            y=alt.Y('total_muscle_moment_arm', scale=alt.Scale(zero=False), axis=alt.Axis(title='Muscle moment arm/Lower jaw length', domain=False, tickSize=5, labelPadding=10, titlePadding=20)),
            color = alt.Color('species', legend=None).scale(scheme='dark2'),
            text='species'
        ).properties(
            width=500,
            height=400
        ).configure_axis(
            labelFontSize=14,
            titleFontSize=16,
            labelAngle = 0
        )       

        cc3, cc4, cc5 = st.columns([1,1,1])
        with cc3:
            st.altair_chart(plot_pcsa_norm, theme=None, use_container_width=True)
        with cc4:
            st.altair_chart(plot_Biteforce_norm, theme=None, use_container_width=True)
        with cc5:
            st.altair_chart(plot_BitingEff, theme=None, use_container_width=True)

        answer_2 = st.text_area("Type your answer and validate with Crtl+Enter", max_chars = 500, key = "answer_2")
        st.write(f'You wrote {len(answer_2)} characters.')
    
        st.write("We have just seen that *M. fascicularis* has a greater biting efficiency than *M. murinus*. We can assess what is allowing for a more efficient muscle force transmission in this species.\n 1) What are the two measurements that we have plotted below?\n 2) What do these two plots tell us about adductor muscle force transmission?\n 3) What could be the limitations of the musculoskeletal models we have just made?")
        
        cc6, cc7 = st.columns(2)
        with cc6:
            st.altair_chart(plot_outLeverLengthNorm, theme=None, use_container_width=True)
        with cc7:
            st.altair_chart(plot_scatter_mom_arm, theme=None, use_container_width=True)

        answer_3 = st.text_area("Type your answer and validate with Crtl+Enter", max_chars = 500, key = "answer_3")
        st.write(f'You wrote {len(answer_3)} characters.')
