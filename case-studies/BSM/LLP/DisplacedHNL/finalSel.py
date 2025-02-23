import sys, os
import ROOT

###Input directory where the files produced at the pre-selection level are
baseDir  = "read_EDM4HEP/"

###Link to the dictonary that contains all the cross section informations etc...
procDict = "myFCCee_procDict_spring2021_IDEA.json"
process_list=[
    #'HNL_50'
    #'HNL_50_old'
    'HNL_eenu_40GeV_1e-3Ve',
    'HNL_eenu_40GeV_1e-4Ve',
    'HNL_eenu_40GeV_1e-5Ve',
    #'HNL_eenu_5GeV_1p41e-6Ve',
    #'HNL_eenu_10GeV_1p41e-6Ve',
    #'HNL_eenu_12GeV_1p41e-6Ve',
    #'HNL_eenu_15GeV_1p41e-6Ve',
    #'HNL_eenu_20GeV_1p41e-6Ve',
    #'HNL_eenu_30GeV_1p41e-6Ve',
    #'HNL_eenu_40GeV_1p41e-6Ve',
    #'HNL_eenu_50GeV_1p41e-6Ve',
    #'HNL_eenu_70GeV_1p41e-6Ve',
    #'HNL_eenu_90GeV_1p41e-6Ve',
]

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file

cut_list = {
    #"sel1":"zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 80 &&  zed_leptonic_m[0] < 100"
    "selNone": "n_RecoTracks > -1",
    "sel0": "GenHNL_mass.size() > 0",
    "sel1": "GenHNL_mass.size() > 0 && n_RecoElectrons > 1",
}


###Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.

variables = {

    #gen variables
    "All_n_GenHNL":                    {"name":"All_n_GenHNL",                   "title":"Total number of gen HNLs",                   "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "AllGenHNL_mass":                  {"name":"AllGenHNL_mass",                 "title":"All gen N mass [GeV]",                       "bin":100,"xmin":0 ,"xmax":100},
    "AllGenHNL_e":                     {"name":"AllGenHNL_e",                    "title":"All gen N energy [GeV]",                     "bin":100,"xmin":0 ,"xmax":100},
    "AllGenHNL_p":                     {"name":"AllGenHNL_p",                    "title":"All gen N p [GeV]",                          "bin":100,"xmin":0 ,"xmax":50},
    "AllGenHNL_pt":                    {"name":"AllGenHNL_pt",                   "title":"All gen N p_{T} [GeV]",                      "bin":100,"xmin":0 ,"xmax":50},
    "AllGenHNL_pz":                    {"name":"AllGenHNL_pz",                   "title":"All gen N p_{z} [GeV]",                      "bin":100,"xmin":0 ,"xmax":50},
    "AllGenHNL_eta":                   {"name":"AllGenHNL_eta",                  "title":"All gen N #eta",                             "bin":60, "xmin":-3,"xmax":3},
    "AllGenHNL_theta":                 {"name":"AllGenHNL_theta",                "title":"All gen N #theta",                           "bin":64, "xmin":0,"xmax":3.2},
    "AllGenHNL_phi":                   {"name":"AllGenHNL_phi",                  "title":"All gen N #phi",                             "bin":64, "xmin":-3.2,"xmax":3.2},

    "n_FSGenElectron":                 {"name":"n_FSGenElectron",                "title":"Number of final state gen electrons",        "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "n_FSGenPositron":                 {"name":"n_FSGenPositron",                "title":"Number of final state gen positrons",        "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "n_FSGenNeutrino":                 {"name":"n_FSGenNeutrino",                "title":"Number of final state gen neutrinos",        "bin":5,"xmin":-0.5 ,"xmax":4.5},
    #"n_FSGenAntiNeutrino":             {"name":"n_FSGenAntiNeutrino",            "title":"Number of final state gen anti-neutrinos",   "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "n_FSGenPhoton":                   {"name":"n_FSGenPhoton",                  "title":"Number of final state gen photons",          "bin":5,"xmin":-0.5 ,"xmax":4.5},

    "FSGenElectron_e":                 {"name":"FSGenElectron_e",                "title":"Final state gen electrons energy [GeV]",     "bin":100,"xmin":0 ,"xmax":50},
    "FSGenElectron_p":                 {"name":"FSGenElectron_p",                "title":"Final state gen electrons p [GeV]",          "bin":100,"xmin":0 ,"xmax":50},
    "FSGenElectron_pt":                {"name":"FSGenElectron_pt",               "title":"Final state gen electrons p_{T} [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "FSGenElectron_pz":                {"name":"FSGenElectron_pz",               "title":"Final state gen electrons p_{z} [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "FSGenElectron_eta":               {"name":"FSGenElectron_eta",              "title":"Final state gen electrons #eta",             "bin":60, "xmin":-3,"xmax":3},
    "FSGenElectron_theta":             {"name":"FSGenElectron_theta",            "title":"Final state gen electrons #theta",           "bin":64, "xmin":0,"xmax":3.2},
    "FSGenElectron_phi":               {"name":"FSGenElectron_phi",              "title":"Final state gen electrons #phi",             "bin":64, "xmin":-3.2,"xmax":3.2},

    "FSGenPositron_e":                 {"name":"FSGenPositron_e",                "title":"Final state gen positrons energy [GeV]",     "bin":100,"xmin":0 ,"xmax":50},
    "FSGenPositron_p":                 {"name":"FSGenPositron_p",                "title":"Final state gen positrons p [GeV]",          "bin":100,"xmin":0 ,"xmax":50},
    "FSGenPositron_pt":                {"name":"FSGenPositron_pt",               "title":"Final state gen positrons p_{T} [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "FSGenPositron_pz":                {"name":"FSGenPositron_pz",               "title":"Final state gen positrons p_{z} [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "FSGenPositron_eta":               {"name":"FSGenPositron_eta",              "title":"Final state gen positrons #eta",             "bin":60, "xmin":-3,"xmax":3},
    "FSGenPositron_theta":             {"name":"FSGenPositron_theta",            "title":"Final state gen positrons #theta",           "bin":64, "xmin":0,"xmax":3.2},
    "FSGenPositron_phi":               {"name":"FSGenPositron_phi",              "title":"Final state gen positrons #phi",             "bin":64, "xmin":-3.2,"xmax":3.2},

    "FSGenNeutrino_e":                 {"name":"FSGenNeutrino_e",                "title":"Final state gen neutrino energy [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "FSGenNeutrino_p":                 {"name":"FSGenNeutrino_p",                "title":"Final state gen neutrino p [GeV]",           "bin":100,"xmin":0 ,"xmax":50},
    "FSGenNeutrino_pt":                {"name":"FSGenNeutrino_pt",               "title":"Final state gen neutrino p_{T} [GeV]",       "bin":100,"xmin":0 ,"xmax":50},
    "FSGenNeutrino_pz":                {"name":"FSGenNeutrino_pz",               "title":"Final state gen neutrino p_{z} [GeV]",       "bin":100,"xmin":0 ,"xmax":50},
    "FSGenNeutrino_eta":               {"name":"FSGenNeutrino_eta",              "title":"Final state gen neutrinos #eta",             "bin":60, "xmin":-3,"xmax":3},
    "FSGenNeutrino_theta":             {"name":"FSGenNeutrino_theta",            "title":"Final state gen neutrinos #theta",           "bin":64, "xmin":0,"xmax":3.2},
    "FSGenNeutrino_phi":               {"name":"FSGenNeutrino_phi",              "title":"Final state gen neutrinos #phi",             "bin":64, "xmin":-3.2,"xmax":3.2},

    # "FSGenAntiNeutrino_e":             {"name":"FSGenAntiNeutrino_e",            "title":"Final state gen anti-neutrino energy [GeV]", "bin":100,"xmin":0 ,"xmax":50},
    # "FSGenAntiNeutrino_p":             {"name":"FSGenAntiNeutrino_p",            "title":"Final state gen anti-neutrino p [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    # "FSGenAntiNeutrino_pt":            {"name":"FSGenAntiNeutrino_pt",           "title":"Final state gen anti-neutrino p_{T} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    # "FSGenAntiNeutrino_pz":            {"name":"FSGenAntiNeutrino_pz",           "title":"Final state gen anti-neutrino p_{z} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    # "FSGenAntiNeutrino_eta":           {"name":"FSGenAntiNeutrino_eta",          "title":"Final state gen anti-neutrinos #eta",        "bin":60, "xmin":-3,"xmax":3},
    # "FSGenAntiNeutrino_theta":         {"name":"FSGenAntiNeutrino_theta",        "title":"Final state gen anti-neutrinos #theta",      "bin":64, "xmin":0,"xmax":3.2},
    # "FSGenAntiNeutrino_phi":           {"name":"FSGenAntiNeutrino_phi",          "title":"Final state gen anti-neutrinos #phi",        "bin":64, "xmin":-3.2,"xmax":3.2},

    "FSGenPhoton_e":                   {"name":"FSGenPhoton_e",                  "title":"Final state gen photons energy [GeV]",       "bin":100,"xmin":0 ,"xmax":50},
    "FSGenPhoton_p":                   {"name":"FSGenPhoton_p",                  "title":"Final state gen photons p [GeV]",            "bin":100,"xmin":0 ,"xmax":50},
    "FSGenPhoton_pt":                  {"name":"FSGenPhoton_pt",                 "title":"Final state gen photons p_{T} [GeV]",        "bin":100,"xmin":0 ,"xmax":50},
    "FSGenPhoton_pz":                  {"name":"FSGenPhoton_pz",                 "title":"Final state gen photons p_{z} [GeV]",        "bin":100,"xmin":0 ,"xmax":50},
    "FSGenPhoton_eta":                 {"name":"FSGenPhoton_eta",                "title":"Final state gen photons #eta",               "bin":60, "xmin":-3,"xmax":3},
    "FSGenPhoton_theta":               {"name":"FSGenPhoton_theta",              "title":"Final state gen photons #theta",             "bin":64, "xmin":0,"xmax":3.2},
    "FSGenPhoton_phi":                 {"name":"FSGenPhoton_phi",                "title":"Final state gen photons #phi",               "bin":64, "xmin":-3.2,"xmax":3.2},

    "FSGenElectron_vertex_x": {"name":"FSGenElectron_vertex_x", "title":"Final state gen e^{#font[122]{\55}} production vertex x [mm]",      "bin":100,"xmin":-1000 ,"xmax":1000},
    "FSGenElectron_vertex_y": {"name":"FSGenElectron_vertex_y", "title":"Final state gen e^{#font[122]{\55}} production vertex y [mm]",      "bin":100,"xmin":-1000 ,"xmax":1000},
    "FSGenElectron_vertex_z": {"name":"FSGenElectron_vertex_z", "title":"Final state gen e^{#font[122]{\55}} production vertex z [mm]",      "bin":100,"xmin":-1000 ,"xmax":1000},

    "FSGen_lifetime": {"name":"FSGen_lifetime", "title":"Gen HNL (FS eles) #tau [s]",        "bin":100,"xmin":0 ,"xmax":2E-9},
    "FSGen_Lxy":      {"name":"FSGen_Lxy",      "title":"Gen HNL (FS eles) L_{xy} [mm]",     "bin":100,"xmin":0 ,"xmax":100},

    "FSGen_lifetimeLxyz": {"name":"FSGen_lifetimeLxyz", "title":"Gen HNL (FS eles) #tau [s]",        "bin":100,"xmin":0 ,"xmax":2E-9},
    "FSGen_Lxyz":      {"name":"FSGen_Lxyz",      "title":"Gen HNL (FS eles) L_{xyz} [mm]",     "bin":100,"xmin":0 ,"xmax":0.01},

    "FSGen_ee_invMass":   {"name":"FSGen_ee_invMass",   "title":"Gen FS m_{ee} [GeV]",           "bin":100,"xmin":0, "xmax":100},
    "FSGen_eenu_invMass": {"name":"FSGen_eenu_invMass", "title":"Gen FS m_{ee#nu} [GeV]",        "bin":100,"xmin":0, "xmax":100},

    "GenHNL_mass":     {"name":"GenHNL_mass",     "title":"Gen N mass [GeV]",      "bin":100,"xmin":0 ,"xmax":100},
    "GenHNL_p":        {"name":"GenHNL_p",        "title":"Gen N p [GeV]",         "bin":100,"xmin":0 ,"xmax":50},
    "GenHNL_pt":       {"name":"GenHNL_pt",       "title":"Gen N p_{T} [GeV]",     "bin":100,"xmin":0 ,"xmax":50},
    "GenHNL_pz":       {"name":"GenHNL_pz",       "title":"Gen N p_{z} [GeV]",     "bin":100,"xmin":0 ,"xmax":50},
    "GenHNL_eta":      {"name":"GenHNL_eta",      "title":"Gen N #eta",            "bin":60, "xmin":-3,"xmax":3},
    "GenHNL_theta":    {"name":"GenHNL_theta",    "title":"Gen N #theta",          "bin":64, "xmin":0,"xmax":3.2},
    "GenHNL_phi":      {"name":"GenHNL_phi",      "title":"Gen N #phi",            "bin":64, "xmin":-3.2,"xmax":3.2},
    "GenHNL_lifetime": {"name":"GenHNL_lifetime", "title":"Gen N #tau [s]",        "bin":100,"xmin":0 ,"xmax":2E-9},
    "GenHNL_Lxy":      {"name":"GenHNL_Lxy",      "title":"Gen N L_{xy} [mm]",     "bin":100,"xmin":0 ,"xmax":100},
    "GenHNL_lifetimeLxyz": {"name":"GenHNL_lifetimeLxyz", "title":"Gen N #tau [s]",        "bin":100,"xmin":0 ,"xmax":2E-9},
    "GenHNL_Lxyz":      {"name":"GenHNL_Lxyz",      "title":"Gen N L_{xyz} [mm]",     "bin":100,"xmin":0 ,"xmax":0.01},
    "GenHNL_vertex_x": {"name":"GenHNL_vertex_x", "title":"Gen N production vertex x [mm]",   "bin":100,"xmin":-1000 ,"xmax":1000},
    "GenHNL_vertex_y": {"name":"GenHNL_vertex_y", "title":"Gen N production vertex y [mm]",   "bin":100,"xmin":-1000 ,"xmax":1000},
    "GenHNL_vertex_z": {"name":"GenHNL_vertex_z", "title":"Gen N production vertex z [mm]",   "bin":100,"xmin":-1000 ,"xmax":1000},

    "GenHNLElectron_e":        {"name":"GenHNLElectron_e",        "title":"Gen e^{#font[122]{\55}} energy [GeV]",                  "bin":100,"xmin":0 ,"xmax":50},
    "GenHNLPositron_e":        {"name":"GenHNLPositron_e",        "title":"Gen e^{+} energy [GeV]",                                "bin":100,"xmin":0 ,"xmax":50},
    "GenHNLNeutrino_e":        {"name":"GenHNLNeutrino_e",        "title":"Gen #nu energy [GeV]",                                  "bin":100,"xmin":0 ,"xmax":50},
    "GenHNLElectron_p":        {"name":"GenHNLElectron_p",        "title":"Gen e^{#font[122]{\55}} p [GeV]",                       "bin":100,"xmin":0 ,"xmax":50},
    "GenHNLPositron_p":        {"name":"GenHNLPositron_p",        "title":"Gen e^{+} p [GeV]",                                     "bin":100,"xmin":0 ,"xmax":50},
    "GenHNLNeutrino_p":        {"name":"GenHNLNeutrino_p",        "title":"Gen #nu p [GeV]",                                       "bin":100,"xmin":0 ,"xmax":50},
    "GenHNLElectron_pt":       {"name":"GenHNLElectron_pt",       "title":"Gen e^{#font[122]{\55}} p_{T} [GeV]",                   "bin":100,"xmin":0 ,"xmax":50},
    "GenHNLPositron_pt":       {"name":"GenHNLPositron_pt",       "title":"Gen e^{+} p_{T} [GeV]",                                 "bin":100,"xmin":0 ,"xmax":50},
    "GenHNLNeutrino_pt":       {"name":"GenHNLNeutrino_pt",       "title":"Gen #nu p_{T} [GeV]",                                   "bin":100,"xmin":0 ,"xmax":50},
    "GenHNLElectron_pz":       {"name":"GenHNLElectron_pz",       "title":"Gen e^{#font[122]{\55}} p_{z} [GeV]",                   "bin":100,"xmin":0 ,"xmax":50},
    "GenHNLPositron_pz":       {"name":"GenHNLPositron_pz",       "title":"Gen e^{+} p_{z} [GeV]",                                 "bin":100,"xmin":0 ,"xmax":50},
    "GenHNLNeutrino_pz":       {"name":"GenHNLNeutrino_pz",       "title":"Gen #nu p_{z} [GeV]",                                   "bin":100,"xmin":0 ,"xmax":50},
    "GenHNLElectron_eta":      {"name":"GenHNLElectron_eta",      "title":"Gen e^{#font[122]{\55}} #eta",                          "bin":60, "xmin":-3,"xmax":3},
    "GenHNLPositron_eta":      {"name":"GenHNLPositron_eta",      "title":"Gen e^{+} #eta",                                        "bin":60, "xmin":-3,"xmax":3},
    "GenHNLNeutrino_eta":      {"name":"GenHNLNeutrino_eta",      "title":"Gen #nu #eta",                                          "bin":60, "xmin":-3,"xmax":3},
    "GenHNLElectron_theta":    {"name":"GenHNLElectron_theta",    "title":"Gen e^{#font[122]{\55}} #theta",                        "bin":64, "xmin":0,"xmax":3.2},
    "GenHNLPositron_theta":    {"name":"GenHNLPositron_theta",    "title":"Gen e^{+} #theta",                                      "bin":64, "xmin":0,"xmax":3.2},
    "GenHNLNeutrino_theta":    {"name":"GenHNLNeutrino_theta",    "title":"Gen #nu #theta",                                        "bin":64, "xmin":0,"xmax":3.2},
    "GenHNLElectron_phi":      {"name":"GenHNLElectron_phi",      "title":"Gen e^{#font[122]{\55}} #phi",                          "bin":64, "xmin":-3.2,"xmax":3.2},
    "GenHNLPositron_phi":      {"name":"GenHNLPositron_phi",      "title":"Gen e^{+} #phi",                                        "bin":64, "xmin":-3.2,"xmax":3.2},
    "GenHNLNeutrino_phi":      {"name":"GenHNLNeutrino_phi",      "title":"Gen #nu #phi",                                          "bin":64, "xmin":-3.2,"xmax":3.2},

    "GenHNLElectron_vertex_x": {"name":"GenHNLElectron_vertex_x", "title":"Gen e^{#font[122]{\55}} production vertex x [mm]",      "bin":100,"xmin":-1000 ,"xmax":1000},
    "GenHNLElectron_vertex_y": {"name":"GenHNLElectron_vertex_y", "title":"Gen e^{#font[122]{\55}} production vertex y [mm]",      "bin":100,"xmin":-1000 ,"xmax":1000},
    "GenHNLElectron_vertex_z": {"name":"GenHNLElectron_vertex_z", "title":"Gen e^{#font[122]{\55}} production vertex z [mm]",      "bin":100,"xmin":-1000 ,"xmax":1000},

    "GenHNL_ee_invMass":   {"name":"GenHNL_ee_invMass",   "title":"Gen m_{ee} (from HNL) [GeV]",           "bin":100,"xmin":0, "xmax":100},
    "GenHNL_eenu_invMass": {"name":"GenHNL_eenu_invMass", "title":"Gen m_{ee#nu} (from HNL) [GeV]",        "bin":100,"xmin":0, "xmax":100},

    #reco variables
    "n_RecoTracks":                    {"name":"n_RecoTracks",                   "title":"Total number of reco tracks",           "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "n_RecoHNLTracks":                 {"name":"n_RecoHNLTracks",                "title":"Number of reco HNL tracks",             "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "RecoHNL_DecayVertex_x":           {"name":"RecoHNLDecayVertex.position.x",  "title":"Reco N decay vertex x [mm]",            "bin":100,"xmin":-1000 ,"xmax":1000},
    "RecoHNL_DecayVertex_y":           {"name":"RecoHNLDecayVertex.position.y",  "title":"Reco N decay vertex y [mm]",            "bin":100,"xmin":-1000 ,"xmax":1000},
    "RecoHNL_DecayVertex_z":           {"name":"RecoHNLDecayVertex.position.z",  "title":"Reco N decay vertex z [mm]",            "bin":100,"xmin":-1000 ,"xmax":1000},
    "RecoHNL_DecayVertex_chi2":        {"name":"RecoHNLDecayVertex.chi2",        "title":"Reco N decay vertex #chi^{2}",          "bin":100,"xmin":0 ,"xmax":3},
    "RecoHNL_DecayVertex_probability": {"name":"RecoHNLDecayVertex.probability", "title":"Reco N decay vertex probability",       "bin":100,"xmin":0 ,"xmax":10},

    "RecoHNLElectron_e":        {"name":"RecoHNLElectron_e",        "title":"Reco e^{#font[122]{\55}} (from HNL) energy [GeV]", "bin":100,"xmin":0 ,"xmax":50},
    "RecoHNLPositron_e":        {"name":"RecoHNLPositron_e",        "title":"Reco e^{+} (from HNL) energy [GeV]",               "bin":100,"xmin":0 ,"xmax":50},
    "RecoHNLElectron_p":        {"name":"RecoHNLElectron_p",        "title":"Reco e^{#font[122]{\55}} (from HNL) p [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "RecoHNLPositron_p":        {"name":"RecoHNLPositron_p",        "title":"Reco e^{+} (from HNL) p [GeV]",                    "bin":100,"xmin":0 ,"xmax":50},
    "RecoHNLElectron_pt":       {"name":"RecoHNLElectron_pt",       "title":"Reco e^{#font[122]{\55}} (from HNL) p_{T} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoHNLPositron_pt":       {"name":"RecoHNLPositron_pt",       "title":"Reco e^{+} (from HNL) p_{T} [GeV]",                "bin":100,"xmin":0 ,"xmax":50},
    "RecoHNLElectron_pz":       {"name":"RecoHNLElectron_pz",       "title":"Reco e^{#font[122]{\55}} (from HNL) p_{z} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoHNLPositron_pz":       {"name":"RecoHNLPositron_pz",       "title":"Reco e^{+} (from HNL) p_{z} [GeV]",                "bin":100,"xmin":0 ,"xmax":50},
    "RecoHNLElectron_eta":      {"name":"RecoHNLElectron_eta",      "title":"Reco e^{#font[122]{\55}} (from HNL) #eta",         "bin":60, "xmin":-3,"xmax":3},
    "RecoHNLPositron_eta":      {"name":"RecoHNLPositron_eta",      "title":"Reco e^{+} (from HNL) #eta",                       "bin":60, "xmin":-3,"xmax":3},
    "RecoHNLElectron_theta":    {"name":"RecoHNLElectron_theta",    "title":"Reco e^{#font[122]{\55}} (from HNL) #theta",       "bin":64, "xmin":0,"xmax":3.2},
    "RecoHNLPositron_theta":    {"name":"RecoHNLPositron_theta",    "title":"Reco e^{+} (from HNL) #theta",                     "bin":64, "xmin":0,"xmax":3.2},
    "RecoHNLElectron_phi":      {"name":"RecoHNLElectron_phi",      "title":"Reco e^{#font[122]{\55}} (from HNL) #phi",         "bin":64, "xmin":-3.2,"xmax":3.2},
    "RecoHNLPositron_phi":      {"name":"RecoHNLPositron_phi",      "title":"Reco e^{+} (from HNL) #phi",                       "bin":64, "xmin":-3.2,"xmax":3.2},
    "RecoHNLElectron_charge":   {"name":"RecoHNLElectron_charge",   "title":"Reco e^{#font[122]{\55}} (from HNL) charge",       "bin":3, "xmin":-1.5,"xmax":1.5},
    "RecoHNLPositron_charge":   {"name":"RecoHNLPositron_charge",   "title":"Reco e^{+} (from HNL) charge",                     "bin":3, "xmin":-1.5,"xmax":1.5},

    "RecoHNL_ee_invMass":   {"name":"RecoHNL_ee_invMass",   "title":"Reco m_{ee} (from HNL) [GeV]",           "bin":100,"xmin":0, "xmax":100},

    "n_RecoJets":       {"name":"n_RecoJets",      "title":"Total number of reco jets",         "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "n_RecoPhotons":    {"name":"n_RecoPhotons",   "title":"Total number of reco photons",      "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "n_RecoElectrons":  {"name":"n_RecoElectrons", "title":"Total number of reco electrons",    "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "n_RecoMuons":      {"name":"n_RecoMuons",     "title":"Total number of reco muons",        "bin":5,"xmin":-0.5 ,"xmax":4.5},

    "RecoJet_e":        {"name":"RecoJet_e",        "title":"Reco jet energy [GeV]", "bin":100,"xmin":0 ,"xmax":50},
    "RecoJet_p":        {"name":"RecoJet_p",        "title":"Reco jet p [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "RecoJet_pt":       {"name":"RecoJet_pt",       "title":"Reco jet p_{T} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoJet_pz":       {"name":"RecoJet_pz",       "title":"Reco jet p_{z} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoJet_eta":      {"name":"RecoJet_eta",      "title":"Reco jet #eta",         "bin":60, "xmin":-3,"xmax":3},
    "RecoJet_theta":    {"name":"RecoJet_theta",    "title":"Reco jet #theta",       "bin":64, "xmin":0,"xmax":3.2},
    "RecoJet_phi":      {"name":"RecoJet_phi",      "title":"Reco jet #phi",         "bin":64, "xmin":-3.2,"xmax":3.2},
    "RecoJet_charge":   {"name":"RecoJet_charge",   "title":"Reco jet charge",       "bin":3, "xmin":-1.5,"xmax":1.5},

    "RecoElectron_e":        {"name":"RecoElectron_e",        "title":"Reco electron energy [GeV]", "bin":100,"xmin":0 ,"xmax":50},
    "RecoElectron_p":        {"name":"RecoElectron_p",        "title":"Reco electron p [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "RecoElectron_pt":       {"name":"RecoElectron_pt",       "title":"Reco electron p_{T} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoElectron_pz":       {"name":"RecoElectron_pz",       "title":"Reco electron p_{z} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoElectron_eta":      {"name":"RecoElectron_eta",      "title":"Reco electron #eta",         "bin":60, "xmin":-3,"xmax":3},
    "RecoElectron_theta":    {"name":"RecoElectron_theta",    "title":"Reco electron #theta",       "bin":64, "xmin":0,"xmax":3.2},
    "RecoElectron_phi":      {"name":"RecoElectron_phi",      "title":"Reco electron #phi",         "bin":64, "xmin":-3.2,"xmax":3.2},
    "RecoElectron_charge":   {"name":"RecoElectron_charge",   "title":"Reco electron charge",       "bin":3, "xmin":-1.5,"xmax":1.5},

    "RecoPhoton_e":        {"name":"RecoPhoton_e",        "title":"Reco photon energy [GeV]", "bin":100,"xmin":0 ,"xmax":50},
    "RecoPhoton_p":        {"name":"RecoPhoton_p",        "title":"Reco photon p [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "RecoPhoton_pt":       {"name":"RecoPhoton_pt",       "title":"Reco photon p_{T} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoPhoton_pz":       {"name":"RecoPhoton_pz",       "title":"Reco photon p_{z} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoPhoton_eta":      {"name":"RecoPhoton_eta",      "title":"Reco photon #eta",         "bin":60, "xmin":-3,"xmax":3},
    "RecoPhoton_theta":    {"name":"RecoPhoton_theta",    "title":"Reco photon #theta",       "bin":64, "xmin":0,"xmax":3.2},
    "RecoPhoton_phi":      {"name":"RecoPhoton_phi",      "title":"Reco photon #phi",         "bin":64, "xmin":-3.2,"xmax":3.2},
    "RecoPhoton_charge":   {"name":"RecoPhoton_charge",   "title":"Reco photon charge",       "bin":3, "xmin":-1.5,"xmax":1.5},

    "RecoMuon_e":        {"name":"RecoMuon_e",        "title":"Reco muon energy [GeV]", "bin":100,"xmin":0 ,"xmax":50},
    "RecoMuon_p":        {"name":"RecoMuon_p",        "title":"Reco muon p [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "RecoMuon_pt":       {"name":"RecoMuon_pt",       "title":"Reco muon p_{T} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoMuon_pz":       {"name":"RecoMuon_pz",       "title":"Reco muon p_{z} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoMuon_eta":      {"name":"RecoMuon_eta",      "title":"Reco muon #eta",         "bin":60, "xmin":-3,"xmax":3},
    "RecoMuon_theta":    {"name":"RecoMuon_theta",    "title":"Reco muon #theta",       "bin":64, "xmin":0,"xmax":3.2},
    "RecoMuon_phi":      {"name":"RecoMuon_phi",      "title":"Reco muon #phi",         "bin":64, "xmin":-3.2,"xmax":3.2},
    "RecoMuon_charge":   {"name":"RecoMuon_charge",   "title":"Reco muon charge",       "bin":3, "xmin":-1.5,"xmax":1.5},

    "RecoMET":       {"name":"RecoMET",       "title":"Reco MET [GeV]",    "bin":100,"xmin":0 ,"xmax":50},
    "RecoMET_x":     {"name":"RecoMET_x",     "title":"Reco MET x [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoMET_y":     {"name":"RecoMET_y",     "title":"Reco MET y [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoMET_phi":   {"name":"RecoMET_phi",   "title":"Reco MET #phi",     "bin":64,"xmin":-3.2 ,"xmax":3.2},

    #gen-reco
    "GenMinusRecoHNLElectron_e":    {"name":"GenMinusRecoHNLElectron_e",    "title":"Gen e^{#font[122]{\55}} energy - Reco e^{#font[122]{\55}} energy [GeV]","bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoHNLPositron_e":    {"name":"GenMinusRecoHNLPositron_e",    "title":"Gen e^{+} energy - Reco e^{+} energy [GeV]",                            "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoHNLElectron_p":    {"name":"GenMinusRecoHNLElectron_p",    "title":"Gen e^{#font[122]{\55}} p - Reco e^{#font[122]{\55}} p [GeV]",          "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoHNLPositron_p":    {"name":"GenMinusRecoHNLPositron_p",    "title":"Gen e^{+} p - Reco e^{+} p [GeV]",                                      "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoHNLElectron_pt":   {"name":"GenMinusRecoHNLElectron_pt",   "title":"Gen e^{#font[122]{\55}} p_{T} - Reco e^{#font[122]{\55}} p_{T} [GeV]",  "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoHNLPositron_pt":   {"name":"GenMinusRecoHNLPositron_pt",   "title":"Gen e^{+} p_{T} - Reco e^{+} p_{T} [GeV]",                              "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoHNLElectron_pz":   {"name":"GenMinusRecoHNLElectron_pz",   "title":"Gen e^{#font[122]{\55}} p_{z} - Reco e^{#font[122]{\55}} p_{z} [GeV]",  "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoHNLPositron_pz":   {"name":"GenMinusRecoHNLPositron_pz",   "title":"Gen e^{+} p_{z} - Reco e^{+} p_{z} [GeV]",                              "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoHNLElectron_eta":  {"name":"GenMinusRecoHNLElectron_eta",  "title":"Gen e^{#font[122]{\55}} #eta - Reco e^{#font[122]{\55}} #eta",          "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoHNLPositron_eta":  {"name":"GenMinusRecoHNLPositron_eta",  "title":"Gen e^{+} #eta - Reco e^{+} #eta",                                      "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoHNLElectron_theta":{"name":"GenMinusRecoHNLElectron_theta","title":"Gen e^{#font[122]{\55}} #theta - Reco e^{#font[122]{\55}} #theta",      "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoHNLPositron_theta":{"name":"GenMinusRecoHNLPositron_theta","title":"Gen e^{+} #theta - Reco e^{+} #theta",                                  "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoHNLElectron_phi":  {"name":"GenMinusRecoHNLElectron_phi",  "title":"Gen e^{#font[122]{\55}} #phi - Reco e^{#font[122]{\55}} #phi",          "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoHNLPositron_phi":  {"name":"GenMinusRecoHNLPositron_phi",  "title":"Gen e^{+} #phi - Reco e^{+} #phi",                                      "bin":100,"xmin":-5 ,"xmax":5},

    "GenMinusRecoHNL_DecayVertex_x":  {"name":"GenMinusRecoHNL_DecayVertex_x",  "title":"Gen N decay vertex x - Reco N decay vertex x [mm]",              "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoHNL_DecayVertex_y":  {"name":"GenMinusRecoHNL_DecayVertex_y",  "title":"Gen N decay vertex y - Reco N decay vertex y [mm]",              "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoHNL_DecayVertex_z":  {"name":"GenMinusRecoHNL_DecayVertex_z",  "title":"Gen N decay vertex z - Reco N decay vertex z [mm]",              "bin":100,"xmin":-5 ,"xmax":5},
}

###Number of CPUs to use
NUM_CPUS = 2

###Produce TTrees
DO_TREE=False

###This part is standard to all analyses
import config.runDataFrameFinal as rdf
myana=rdf.runDataFrameFinal(baseDir,procDict,process_list,cut_list,variables)
myana.run(ncpu=NUM_CPUS, doTree=DO_TREE)
