# Modelling Underreported Spatio-temporal Crime Events
### Álvaro J. Riascos Villegas, Jose Sebastian Ñungo, Lucas Gómez Tobón, Mateo Dulce Rubio and Francisco Gómez

This repository contains all the instructions to replicate the paper "Modelling Underreported Spatio-temporal Crime Events" including its results, tables, and figures. To do so, first, it is necessary to download all the data from our [Zenodo repository](https://zenodo.org/record/7868622#.ZElgsHbMJD8) and locate it in the "Data" folder to facilitate the exercise of running the code. 

This repository has three main folders. The content of each one is outlined below:
- **Data:** This folder contains "files_dictionary.txt" which is a file with the description of the files that are in our [Zenodo repository](https://zenodo.org/record/7868622#.ZElgsHbMJD8). The purpose of this folder is to store all the data from [Zenodo](https://zenodo.org/record/7868622#.ZElgsHbMJD8), therefore you must download them and put them in there. 
- **Scripts:** This folder contains all the Python codes to develop our research. It is divided into three subfolders:
  - *1_preprocess_data:* This folder contains three scripts that are used to transform the raw data of citizens' crime reports and the official dataset of crime from the Colombian National Police into our clean matrices of events. Each script is a Jupyter Notebook with a detailed description of the process made. **The raw data used in our analysis is not provided as it contains sensitive information about crimes, victims and complainants. For this reason, some dummy observations are provided to run the code.**
  - *2_modeling:* It contains two Python files to create the functions to perform the algorithms described in Section 2 of our paper. 
  - *3_create_outputs:* It contains Jupyter Notebooks to produce all the results of our research. The data needed for those codes are located in our [Zenodo repository](https://zenodo.org/record/7868622#.ZElgsHbMJD8) so it is important to download all the files and located them in the "Data" folder. The following is the list of outputs produced by each script on this folder:
    - figure_8_Bogota_jurisdiction_grid.ipynb: produces [Figure 8](Outputs/Figures/figure_8_bogota_grilla.png).
    - figure_9_crimes_by_source_of_information.ipynb: produces [Figure 9](Outputs/Figures/figure_9_unique_crimes_by_source_of_information.png).
    - figure_15_Bogota_heatmap.ipynb: produces [Figure 15](Outputs/Figures/figure_15_CUCB_crime_estimates.png)
    - results_graphs.ipynb: produces [Figure 10](Outputs/Figures/figure_10_convergencia_global_mu2.png), [Figure 11](Outputs/Figures/figure_11_convergencia_global_q2.png), [Figure 12](Outputs/Figures/figure_12_convergencia_global_q_ultimo_periodo2.png), [Figure 13](Outputs/Figures/figure_13_convergencia_global_reporte(Nxrho)_mensual.png') and [Figure 14](Outputs/Figures/figure_14_convergencia_global_subreporte(Nxqxrho)_mensual.png).
- **Outputs:** This folder contains the results of our research in the form of Data, Figures, and Tables. Therefore, this folder is divided into those three categories:
  - *Data:*
  - *Figures:*
  - *Tables:*
 
### Abstract
<p align = "justify">
Crime observations are one of the principal inputs used by governments for designing citizens' security strategies. However, crime measurements are obscured by underreporting biases, resulting in the so-called "dark figure of crime". Current approaches for estimating the "true" crime rate do not account for underreporting temporal crime dynamics. This work studies the possibility of recovering "true" crime incident rates over time using data from underreported crime observations and complementary crime-related measurements acquired online. For this, a novel underreporting model of spatiotemporal events based on the combinatorial multi-armed bandit framework was proposed. Through extensive simulations, the proposed methodology was validated for identifying the fundamental parameters of the proposed model: the "true" rates of incidence and underreporting of events. Once the proposed model was validated,  crime data from a large city, Bogotá (Colombia), was used to estimate the "true" crime and underreporting rates. Our results suggest that this methodology could be used to rapidly estimate the underreporting rates of spatiotemporal events, which is a critical problem in public policy design.
</p>
