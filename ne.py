# # arr = [
# #         'B-Organization', 'I-Organization', 'B-Health Care Related Organization', 'I-Health Care Related Organization',
# #         'B-Professional Society', 'I-Professional Society', 'B-Self-help or Relief Organization', 'I-Self-help or Relief Organization'
# #     ] + [
# #         'B-Organism', 'I-Organism', 'B-Bacterium', 'I-Bacterium', 
# #         'B-Virus', 'I-Virus', 'B-Fungus', 'I-Fungus', 
# #         'B-Eukaryote', 'I-Eukaryote', 'B-Archaeon', 'I-Archaeon',
# #         'B-Plant', 'I-Plant'
# #     ] + [
# #         'B-Animal', 'I-Animal', 'B-Mammal', 'I-Mammal', 'B-Bird', 'I-Bird', 
# #         'B-Fish', 'I-Fish', 'B-Amphibian', 'I-Amphibian', 'B-Reptile', 'I-Reptile',
# #         'B-Vertebrate', 'I-Vertebrate'
# #     ] + [
# #         'B-Entity', 'I-Entity', 
# #         'B-Conceptual Entity', 'I-Conceptual Entity'
# #     ] + [
# #         'B-Occupation or Discipline', 'I-Occupation or Discipline',
# #         'B-Professional or Occupational Group', 'I-Professional or Occupational Group',
# #         'B-Biomedical Occupation or Discipline', 'I-Biomedical Occupation or Discipline'
# #     ] + [
# #         'B-Biologic Function', 'I-Biologic Function',
# #         'B-Organ or Tissue Function', 'I-Organ or Tissue Function',
# #         'B-Physiologic Function', 'I-Physiologic Function',
# #         'B-Genetic Function', 'I-Genetic Function',
# #         'B-Molecular Function', 'I-Molecular Function',
# #         'B-Organism Function', 'I-Organism Function',
# #         'B-Cell Function', 'I-Cell Function'
# #     ] + [
# #         'B-Body Substance', 'I-Body Substance'
# #     ] + [
# #         'B-Medical Device', 'I-Medical Device',
# #         'B-Drug Delivery Device', 'I-Drug Delivery Device',
# #         'B-Research Device', 'I-Research Device'
# #     ] + [
# #         'B-Inorganic Chemical', 'I-Inorganic Chemical',
# #         'B-Organic Chemical', 'I-Organic Chemical',
# #         'B-Chemical Viewed Functionally', 'I-Chemical Viewed Functionally',
# #         'B-Chemical Viewed Structurally', 'I-Chemical Viewed Structurally',
# #         'B-Hazardous or Poisonous Substance', 'I-Hazardous or Poisonous Substance',
# #         'B-Element, Ion, or Isotope', 'I-Element, Ion, or Isotope'
# #     ] + [
# #         'B-Gene or Genome', 'I-Gene or Genome',
# #         'B-Nucleotide Sequence', 'I-Nucleotide Sequence',
# #         'B-Nucleic Acid, Nucleoside, or Nucleotide', 'I-Nucleic Acid, Nucleoside, or Nucleotide',
# #         'B-Amino Acid Sequence', 'I-Amino Acid Sequence'
# #     ] + [
# #         'B-Diagnostic Procedure', 'I-Diagnostic Procedure', 
# #         'B-Therapeutic or Preventive Procedure', 'I-Therapeutic or Preventive Procedure',
# #         'B-Laboratory Procedure', 'I-Laboratory Procedure'
# #     ] + [
# #         'B-Body Part, Organ, or Organ Component', 'I-Body Part, Organ, or Organ Component', 
# #         'B-Anatomical Structure', 'I-Anatomical Structure', 
# #         'B-Embryonic Structure', 'I-Embryonic Structure',
# #         'B-Tissue', 'I-Tissue',
# #         'B-Body Space or Junction', 'I-Body Space or Junction',
# #         'B-Body Location or Region', 'I-Body Location or Region'
# #     ] + [
# #         'B-Pharmacologic Substance', 'I-Pharmacologic Substance', 
# #         'B-Clinical Drug', 'I-Clinical Drug', 
# #         'B-Biologically Active Substance', 'I-Biologically Active Substance',
# #         'B-Antibiotic', 'I-Antibiotic', 
# #         'B-Chemical', 'I-Chemical'
# #     ] + [
# #         'B-Sign or Symptom', 'I-Sign or Symptom', 
# #         'B-Finding', 'I-Finding', 
# #         'B-Laboratory or Test Result', 'I-Laboratory or Test Result'
# #     ] + [
# #         'B-Disease or Syndrome', 'I-Disease or Syndrome',
# #         'B-Pathologic Function', 'I-Pathologic Function',
# #         'B-Neoplastic Process', 'I-Neoplastic Process',
# #         'B-Injury or Poisoning', 'I-Injury or Poisoning',
# #         'B-Congenital Abnormality', 'I-Congenital Abnormality',
# #         'B-Experimental Model of Disease', 'I-Experimental Model of Disease',
# #         'B-Cell or Molecular Dysfunction', 'I-Cell or Molecular Dysfunction',
# #         'B-Mental or Behavioral Dysfunction', 'I-Mental or Behavioral Dysfunction'
# #     ] + [
# #         'B-Human', 'I-Human', 'B-Population Group', 'I-Population Group', 
# #         'B-Patient or Disabled Group', 'I-Patient or Disabled Group', 
# #         'B-Family Group', 'I-Family Group'
# #     ]

# # print(len(arr))

# # Define the mappings
# # generalized_mappings = {
# #     "Person": [
# #         'B-Human', 'I-Human', 'B-Population Group', 'I-Population Group', 
# #         'B-Patient or Disabled Group', 'I-Patient or Disabled Group', 
# #         'B-Family Group', 'I-Family Group',
# #         'B-Age Group', 'I-Age Group'
# #     ],
# #     "Disease": [
# #         'B-Disease or Syndrome', 'I-Disease or Syndrome',
# #         'B-Pathologic Function', 'I-Pathologic Function',
# #         'B-Neoplastic Process', 'I-Neoplastic Process',
# #         'B-Injury or Poisoning', 'I-Injury or Poisoning',
# #         'B-Congenital Abnormality', 'I-Congenital Abnormality',
# #         'B-Experimental Model of Disease', 'I-Experimental Model of Disease',
# #         'B-Cell or Molecular Dysfunction', 'I-Cell or Molecular Dysfunction',
# #         'B-Mental or Behavioral Dysfunction', 'I-Mental or Behavioral Dysfunction',
# #         'B-Acquired Abnormality', 'I-Acquired Abnormality',
# #         'B-Anatomical Abnormality', 'I-Anatomical Abnormality'
# #     ],
# #     "Symptom": [
# #         'B-Sign or Symptom', 'I-Sign or Symptom', 
# #         'B-Finding', 'I-Finding', 
# #         'B-Laboratory or Test Result', 'I-Laboratory or Test Result',
# #         'B-Clinical Attribute', 'I-Clinical Attribute'
# #     ],
# #     "Drug": [
# #         'B-Pharmacologic Substance', 'I-Pharmacologic Substance', 
# #         'B-Clinical Drug', 'I-Clinical Drug', 
# #         'B-Biologically Active Substance', 'I-Biologically Active Substance',
# #         'B-Antibiotic', 'I-Antibiotic', 
# #         'B-Chemical', 'I-Chemical',
# #         'B-Hormone', 'I-Hormone',
# #         'B-Immunologic Factor', 'I-Immunologic Factor',
# #         'B-Indicator, Reagent, or Diagnostic Aid', 'I-Indicator, Reagent, or Diagnostic Aid',
# #         'B-Receptor', 'I-Receptor'
# #     ],
# #     "Organ": [
# #         'B-Body Part, Organ, or Organ Component', 'I-Body Part, Organ, or Organ Component', 
# #         'B-Anatomical Structure', 'I-Anatomical Structure', 
# #         'B-Embryonic Structure', 'I-Embryonic Structure',
# #         'B-Tissue', 'I-Tissue',
# #         'B-Body Space or Junction', 'I-Body Space or Junction',
# #         'B-Body Location or Region', 'I-Body Location or Region',
# #         'B-Fully Formed Anatomical Structure', 'I-Fully Formed Anatomical Structure',
# #         'B-Cell', 'I-Cell',
# #         'B-Cell Component', 'I-Cell Component'
# #     ],
# #     "Procedure": [
# #         'B-Diagnostic Procedure', 'I-Diagnostic Procedure', 
# #         'B-Therapeutic or Preventive Procedure', 'I-Therapeutic or Preventive Procedure',
# #         'B-Laboratory Procedure', 'I-Laboratory Procedure',
# #         'B-Health Care Activity', 'I-Health Care Activity',
# #         'B-Molecular Biology Research Technique', 'I-Molecular Biology Research Technique',
# #         'B-Research Activity', 'I-Research Activity'
# #     ],
# #     "Gene": [
# #         'B-Gene or Genome', 'I-Gene or Genome',
# #         'B-Nucleotide Sequence', 'I-Nucleotide Sequence',
# #         'B-Nucleic Acid, Nucleoside, or Nucleotide', 'I-Nucleic Acid, Nucleoside, or Nucleotide',
# #         'B-Amino Acid Sequence', 'I-Amino Acid Sequence',
# #         'B-Molecular Sequence', 'I-Molecular Sequence',
# #         'B-Amino Acid, Peptide, or Protein', 'I-Amino Acid, Peptide, or Protein'
# #     ],
# #     "Chemical": [
# #         'B-Inorganic Chemical', 'I-Inorganic Chemical',
# #         'B-Organic Chemical', 'I-Organic Chemical',
# #         'B-Chemical Viewed Functionally', 'I-Chemical Viewed Functionally',
# #         'B-Chemical Viewed Structurally', 'I-Chemical Viewed Structurally',
# #         'B-Hazardous or Poisonous Substance', 'I-Hazardous or Poisonous Substance',
# #         'B-Element, Ion, or Isotope', 'I-Element, Ion, or Isotope',
# #         'B-Substance', 'I-Substance',
# #         'B-Biomedical or Dental Material', 'I-Biomedical or Dental Material',
# #         'B-Vitamin','I-Vitamin'
# #     ],
# #     "Device": [
# #         'B-Medical Device', 'I-Medical Device',
# #         'B-Drug Delivery Device', 'I-Drug Delivery Device',
# #         'B-Research Device', 'I-Research Device',
# #         'B-Manufactured Object', 'I-Manufactured Object'
# #     ],
# #     "Body_Substance": [
# #         'B-Body Substance', 'I-Body Substance'
# #     ],
# #     "Function": [
# #         'B-Biologic Function', 'I-Biologic Function',
# #         'B-Organ or Tissue Function', 'I-Organ or Tissue Function',
# #         'B-Physiologic Function', 'I-Physiologic Function',
# #         'B-Genetic Function', 'I-Genetic Function',
# #         'B-Molecular Function', 'I-Molecular Function',
# #         'B-Organism Function', 'I-Organism Function',
# #         'B-Cell Function', 'I-Cell Function',
# #         'B-Functional Concept', 'I-Functional Concept',
# #         'B-Organism Attribute', 'I-Organism Attribute'
# #     ],
# #     "Profession": [
# #         'B-Occupation or Discipline', 'I-Occupation or Discipline',
# #         'B-Professional or Occupational Group', 'I-Professional or Occupational Group',
# #         'B-Biomedical Occupation or Discipline', 'I-Biomedical Occupation or Discipline',
# #         'B-Occupational Activity', 'I-Occupational Activity'
# #     ],
# #     "Entity": [
# #         'B-Entity', 'I-Entity', 
# #         'B-Conceptual Entity', 'I-Conceptual Entity',
# #         'B-Idea or Concept', 'I-Idea or Concept',
# #         'B-Intellectual Product', 'I-Intellectual Product',
# #         'B-Classification', 'I-Classification'
# #     ],
# #     "Animal": [
# #         'B-Animal', 'I-Animal', 'B-Mammal', 'I-Mammal', 'B-Bird', 'I-Bird', 
# #         'B-Fish', 'I-Fish', 'B-Amphibian', 'I-Amphibian', 'B-Reptile', 'I-Reptile',
# #         'B-Vertebrate', 'I-Vertebrate'
# #     ],
# #     "Organism": [
# #         'B-Organism', 'I-Organism', 'B-Bacterium', 'I-Bacterium', 
# #         'B-Virus', 'I-Virus', 'B-Fungus', 'I-Fungus', 
# #         'B-Eukaryote', 'I-Eukaryote', 'B-Archaeon', 'I-Archaeon',
# #         'B-Plant', 'I-Plant'
# #     ],
# #     "Organization": [
# #         'B-Organization', 'I-Organization', 'B-Health Care Related Organization', 'I-Health Care Related Organization',
# #         'B-Professional Society', 'I-Professional Society', 'B-Self-help or Relief Organization', 'I-Self-help or Relief Organization',
# #         'B-Group', 'I-Group'
# #     ],
# #     "Activity": [
# #         'B-Activity', 'I-Activity',
# #         'B-Daily or Recreational Activity', 'I-Daily or Recreational Activity',
# #         'B-Educational Activity', 'I-Educational Activity',
# #         'B-Governmental or Regulatory Activity', 'I-Governmental or Regulatory Activity',
# #         'B-Machine Activity', 'I-Machine Activity',
# #         'B-Event', 'I-Event',
# #         'B-Human-caused Phenomenon or Process', 'I-Human-caused Phenomenon or Process'
# #     ],
# #     "Behavior": [
# #         'B-Behavior', 'I-Behavior',
# #         'B-Individual Behavior', 'I-Individual Behavior',
# #         'B-Social Behavior', 'I-Social Behavior',
# #         'B-Mental Process', 'I-Mental Process'
# #     ],
# #     "Location": [
# #         'B-Geographic Area', 'I-Geographic Area',
# #         'B-Spatial Concept', 'I-Spatial Concept'
# #     ],
# #     "Food": [
# #         'B-Food', 'I-Food'
# #     ],
# #     "Phenomenon": [
# #         'B-Natural Phenomenon or Process', 'I-Natural Phenomenon or Process',
# #         'B-Phenomenon or Process', 'I-Phenomenon or Process',
# #         'B-Environmental Effect of Humans', 'I-Environmental Effect of Humans'
# #     ],
# #     "Concept": [
# #         'B-Qualitative Concept', 'I-Qualitative Concept',
# #         'B-Quantitative Concept', 'I-Quantitative Concept',
# #         'B-Temporal Concept', 'I-Temporal Concept',
# #         'B-Group Attribute', 'I-Group Attribute'
# #     ],
# #     "Language": [
# #         'B-Language', 'I-Language'
# #     ],
# #     "Regulation": [
# #         'B-Regulation or Law', 'I-Regulation or Law'
# #     ],
# #     "Body_System": [
# #         'B-Body System', 'I-Body System'
# #     ],
# #     "Physical_Object": [
# #         'B-Physical Object', 'I-Physical Object'
# #     ],
# #     "O": [
# #         'B-Other','I-Other','I-UnknownType','B-UnknownType'
# #     ]
# # }
# generalized_mappings = {
#     # 1. Diseases & Abnormalities
#     "Disease": [
#         'B-Disease or Syndrome', 'I-Disease or Syndrome',
#         'B-Pathologic Function', 'I-Pathologic Function',
#         'B-Neoplastic Process', 'I-Neoplastic Process',
#         'B-Injury or Poisoning', 'I-Injury or Poisoning',
#         'B-Congenital Abnormality', 'I-Congenital Abnormality',
#         'B-Experimental Model of Disease', 'I-Experimental Model of Disease',
#         'B-Cell or Molecular Dysfunction', 'I-Cell or Molecular Dysfunction',
#         'B-Mental or Behavioral Dysfunction', 'I-Mental or Behavioral Dysfunction',
#         'B-Acquired Abnormality', 'I-Acquired Abnormality',
#         'B-Anatomical Abnormality', 'I-Anatomical Abnormality'
#     ],

#     # 2. Symptoms & Clinical Findings
#     "Symptom": [
#         'B-Sign or Symptom', 'I-Sign or Symptom',
#         'B-Finding', 'I-Finding',
#         'B-Laboratory or Test Result', 'I-Laboratory or Test Result',
#         'B-Clinical Attribute', 'I-Clinical Attribute'
#     ],

#     # 3. Anatomy & Physiology
#     "Anatomy": [
#         'B-Body Part, Organ, or Organ Component', 'I-Body Part, Organ, or Organ Component',
#         'B-Anatomical Structure', 'I-Anatomical Structure',
#         'B-Embryonic Structure', 'I-Embryonic Structure',
#         'B-Tissue', 'I-Tissue',
#         'B-Body Space or Junction', 'I-Body Space or Junction',
#         'B-Body Location or Region', 'I-Body Location or Region',
#         'B-Fully Formed Anatomical Structure', 'I-Fully Formed Anatomical Structure',
#         'B-Cell', 'I-Cell',
#         'B-Cell Component', 'I-Cell Component',
#         'B-Body Substance', 'I-Body Substance',
#         'B-Body System', 'I-Body System',
#         'B-Physiologic Function', 'I-Physiologic Function',
#         'B-Organ or Tissue Function', 'I-Organ or Tissue Function'
#     ],

#     # 4. Drugs & Chemicals
#     "Chemical/Drug": [
#         'B-Pharmacologic Substance', 'I-Pharmacologic Substance',
#         'B-Clinical Drug', 'I-Clinical Drug',
#         'B-Biologically Active Substance', 'I-Biologically Active Substance',
#         'B-Antibiotic', 'I-Antibiotic',
#         'B-Chemical', 'I-Chemical',
#         'B-Hormone', 'I-Hormone',
#         'B-Immunologic Factor', 'I-Immunologic Factor',
#         'B-Indicator, Reagent, or Diagnostic Aid', 'I-Indicator, Reagent, or Diagnostic Aid',
#         'B-Receptor', 'I-Receptor',
#         'B-Inorganic Chemical', 'I-Inorganic Chemical',
#         'B-Organic Chemical', 'I-Organic Chemical',
#         'B-Hazardous or Poisonous Substance', 'I-Hazardous or Poisonous Substance',
#         'B-Element, Ion, or Isotope', 'I-Element, Ion, or Isotope',
#         'B-Substance', 'I-Substance',
#         'B-Biomedical or Dental Material', 'I-Biomedical or Dental Material',
#         'B-Vitamin', 'I-Vitamin'
#     ],

#     # 5. Procedures & Interventions
#     "Procedure": [
#         'B-Diagnostic Procedure', 'I-Diagnostic Procedure',
#         'B-Therapeutic or Preventive Procedure', 'I-Therapeutic or Preventive Procedure',
#         'B-Laboratory Procedure', 'I-Laboratory Procedure',
#         'B-Health Care Activity', 'I-Health Care Activity',
#         'B-Molecular Biology Research Technique', 'I-Molecular Biology Research Technique',
#         'B-Research Activity', 'I-Research Activity'
#     ],

#     # 6. Genetics & Molecular Biology
#     "Genetics": [
#         'B-Gene or Genome', 'I-Gene or Genome',
#         'B-Nucleotide Sequence', 'I-Nucleotide Sequence',
#         'B-Nucleic Acid, Nucleoside, or Nucleotide', 'I-Nucleic Acid, Nucleoside, or Nucleotide',
#         'B-Amino Acid Sequence', 'I-Amino Acid Sequence',
#         'B-Molecular Sequence', 'I-Molecular Sequence',
#         'B-Amino Acid, Peptide, or Protein', 'I-Amino Acid, Peptide, or Protein',
#         'B-Genetic Function', 'I-Genetic Function',
#         'B-Molecular Function', 'I-Molecular Function'
#     ],

#     # 7. People & Demographics
#     "Person": [
#         'B-Human', 'I-Human',
#         'B-Population Group', 'I-Population Group',
#         'B-Patient or Disabled Group', 'I-Patient or Disabled Group',
#         'B-Family Group', 'I-Family Group',
#         'B-Age Group', 'I-Age Group',
#         'B-Occupation or Discipline', 'I-Occupation or Discipline',
#         'B-Professional or Occupational Group', 'I-Professional or Occupational Group',
#         'B-Biomedical Occupation or Discipline', 'I-Biomedical Occupation or Discipline',
#         'B-Occupational Activity', 'I-Occupational Activity'
#     ],

#     # 8. Organizations
#     "Organization": [
#         'B-Organization', 'I-Organization',
#         'B-Health Care Related Organization', 'I-Health Care Related Organization',
#         'B-Professional Society', 'I-Professional Society',
#         'B-Self-help or Relief Organization', 'I-Self-help or Relief Organization',
#         'B-Group', 'I-Group'
#     ],

#     # 9. Organisms
#     "Organism": [
#         'B-Organism', 'I-Organism',
#         'B-Bacterium', 'I-Bacterium',
#         'B-Virus', 'I-Virus',
#         'B-Fungus', 'I-Fungus',
#         'B-Animal', 'I-Animal',
#         'B-Mammal', 'I-Mammal',
#         'B-Plant', 'I-Plant',
#         'B-Vertebrate', 'I-Vertebrate',
#         'B-Organism Function', 'I-Organism Function'
#     ],

#     # 10. Miscellaneous (Concepts, Behaviors, etc.)
#     "O": [
#         'B-Entity', 'I-Entity',
#         'B-Conceptual Entity', 'I-Conceptual Entity',
#         'B-Idea or Concept', 'I-Idea or Concept',
#         'B-Intellectual Product', 'I-Intellectual Product',
#         'B-Classification', 'I-Classification',
#         'B-Natural Phenomenon or Process', 'I-Natural Phenomenon or Process',
#         'B-Phenomenon or Process', 'I-Phenomenon or Process',
#         'B-Environmental Effect of Humans', 'I-Environmental Effect of Humans',
#         'B-Qualitative Concept', 'I-Qualitative Concept',
#         'B-Quantitative Concept', 'I-Quantitative Concept',
#         'B-Temporal Concept', 'I-Temporal Concept',
#         'B-Group Attribute', 'I-Group Attribute',
#         'B-Functional Concept', 'I-Functional Concept',
#         'B-Organism Attribute', 'I-Organism Attribute',
#         'B-Activity', 'I-Activity',
#         'B-Daily or Recreational Activity', 'I-Daily or Recreational Activity',
#         'B-Educational Activity', 'I-Educational Activity',
#         'B-Governmental or Regulatory Activity', 'I-Governmental or Regulatory Activity',
#         'B-Machine Activity', 'I-Machine Activity',
#         'B-Event', 'I-Event',
#         'B-Human-caused Phenomenon or Process', 'I-Human-caused Phenomenon or Process',
#         'B-Behavior', 'I-Behavior',
#         'B-Individual Behavior', 'I-Individual Behavior',
#         'B-Social Behavior', 'I-Social Behavior',
#         'B-Mental Process', 'I-Mental Process',
#         'B-Food', 'I-Food',
#         'B-Language', 'I-Language',
#         'B-Regulation or Law', 'I-Regulation or Law',
#         'B-Physical Object', 'I-Physical Object',
#         'B-Manufactured Object', 'I-Manufactured Object',
#         'B-Device', 'I-Device',
#         'B-Other', 'I-Other',
#         'O'
#     ]
# }

# generalized_mappings = {
#     # 1. Diseases & Abnormalities
#     "Disease": [
#         'B-Disease or Syndrome', 'I-Disease or Syndrome',
#         'B-Pathologic Function', 'I-Pathologic Function',
#         'B-Neoplastic Process', 'I-Neoplastic Process',
#         'B-Injury or Poisoning', 'I-Injury or Poisoning',
#         'B-Congenital Abnormality', 'I-Congenital Abnormality',
#         'B-Experimental Model of Disease', 'I-Experimental Model of Disease',
#         'B-Cell or Molecular Dysfunction', 'I-Cell or Molecular Dysfunction',
#         'B-Mental or Behavioral Dysfunction', 'I-Mental or Behavioral Dysfunction',
#         'B-Acquired Abnormality', 'I-Acquired Abnormality',
#         'B-Anatomical Abnormality', 'I-Anatomical Abnormality'
#     ],

#     # 2. Symptoms & Clinical Findings
#     "Symptom": [
#         'B-Sign or Symptom', 'I-Sign or Symptom',
#         'B-Finding', 'I-Finding',
#         'B-Laboratory or Test Result', 'I-Laboratory or Test Result',
#         'B-Clinical Attribute', 'I-Clinical Attribute'
#     ],

#     # 3. Anatomy & Physiology
#     "Anatomy": [
#         'B-Body Part, Organ, or Organ Component', 'I-Body Part, Organ, or Organ Component',
#         'B-Anatomical Structure', 'I-Anatomical Structure',
#         'B-Embryonic Structure', 'I-Embryonic Structure',
#         'B-Tissue', 'I-Tissue',
#         'B-Body Space or Junction', 'I-Body Space or Junction',
#         'B-Body Location or Region', 'I-Body Location or Region',
#         'B-Fully Formed Anatomical Structure', 'I-Fully Formed Anatomical Structure',
#         'B-Cell', 'I-Cell',
#         'B-Cell Component', 'I-Cell Component',
#         'B-Body Substance', 'I-Body Substance',
#         'B-Body System', 'I-Body System',
#         'B-Physiologic Function', 'I-Physiologic Function',
#         'B-Organ or Tissue Function', 'I-Organ or Tissue Function',
#         'B-Biologic Function', 'I-Biologic Function',  # Added
#         'B-Cell Function', 'I-Cell Function'  # Added
#     ],

#     # 4. Drugs & Chemicals
#     "Chemical/Drug": [
#         'B-Pharmacologic Substance', 'I-Pharmacologic Substance',
#         'B-Clinical Drug', 'I-Clinical Drug',
#         'B-Biologically Active Substance', 'I-Biologically Active Substance',
#         'B-Antibiotic', 'I-Antibiotic',
#         'B-Chemical', 'I-Chemical',
#         'B-Hormone', 'I-Hormone',
#         'B-Immunologic Factor', 'I-Immunologic Factor',
#         'B-Indicator, Reagent, or Diagnostic Aid', 'I-Indicator, Reagent, or Diagnostic Aid',
#         'B-Receptor', 'I-Receptor',
#         'B-Inorganic Chemical', 'I-Inorganic Chemical',
#         'B-Organic Chemical', 'I-Organic Chemical',
#         'B-Hazardous or Poisonous Substance', 'I-Hazardous or Poisonous Substance',
#         'B-Element, Ion, or Isotope', 'I-Element, Ion, or Isotope',
#         'B-Substance', 'I-Substance',
#         'B-Biomedical or Dental Material', 'I-Biomedical or Dental Material',
#         'B-Vitamin', 'I-Vitamin',
#         'B-Chemical Viewed Functionally', 'I-Chemical Viewed Functionally',  # Added
#         'B-Chemical Viewed Structurally', 'I-Chemical Viewed Structurally'  # Added
#     ],

#     # 5. Procedures & Interventions
#     "Procedure": [
#         'B-Diagnostic Procedure', 'I-Diagnostic Procedure',
#         'B-Therapeutic or Preventive Procedure', 'I-Therapeutic or Preventive Procedure',
#         'B-Laboratory Procedure', 'I-Laboratory Procedure',
#         'B-Health Care Activity', 'I-Health Care Activity',
#         'B-Molecular Biology Research Technique', 'I-Molecular Biology Research Technique',
#         'B-Research Activity', 'I-Research Activity'
#     ],

#     # 6. Genetics & Molecular Biology
#     "Genetics": [
#         'B-Gene or Genome', 'I-Gene or Genome',
#         'B-Nucleotide Sequence', 'I-Nucleotide Sequence',
#         'B-Nucleic Acid, Nucleoside, or Nucleotide', 'I-Nucleic Acid, Nucleoside, or Nucleotide',
#         'B-Amino Acid Sequence', 'I-Amino Acid Sequence',
#         'B-Molecular Sequence', 'I-Molecular Sequence',
#         'B-Amino Acid, Peptide, or Protein', 'I-Amino Acid, Peptide, or Protein',
#         'B-Genetic Function', 'I-Genetic Function',
#         'B-Molecular Function', 'I-Molecular Function'
#     ],

#     # 7. People & Demographics
#     "Person": [
#         'B-Human', 'I-Human',
#         'B-Population Group', 'I-Population Group',
#         'B-Patient or Disabled Group', 'I-Patient or Disabled Group',
#         'B-Family Group', 'I-Family Group',
#         'B-Age Group', 'I-Age Group',
#         'B-Occupation or Discipline', 'I-Occupation or Discipline',
#         'B-Professional or Occupational Group', 'I-Professional or Occupational Group',
#         'B-Biomedical Occupation or Discipline', 'I-Biomedical Occupation or Discipline',
#         'B-Occupational Activity', 'I-Occupational Activity'
#     ],

#     # 8. Organizations
#     "Organization": [
#         'B-Organization', 'I-Organization',
#         'B-Health Care Related Organization', 'I-Health Care Related Organization',
#         'B-Professional Society', 'I-Professional Society',
#         'B-Self-help or Relief Organization', 'I-Self-help or Relief Organization',
#         'B-Group', 'I-Group'
#     ],

#     # 9. Organisms
#     "Organism": [
#         'B-Organism', 'I-Organism',
#         'B-Bacterium', 'I-Bacterium',
#         'B-Virus', 'I-Virus',
#         'B-Fungus', 'I-Fungus',
#         'B-Animal', 'I-Animal',
#         'B-Mammal', 'I-Mammal',
#         'B-Bird', 'I-Bird',  # Added
#         'B-Fish', 'I-Fish',  # Added
#         'B-Amphibian', 'I-Amphibian',  # Added
#         'B-Reptile', 'I-Reptile',  # Added
#         'B-Vertebrate', 'I-Vertebrate',
#         'B-Plant', 'I-Plant',
#         'B-Eukaryote', 'I-Eukaryote',  # Added
#         'B-Archaeon', 'I-Archaeon',  # Added
#         'B-Organism Function', 'I-Organism Function'
#     ],

#     # 10. Miscellaneous (Concepts, Locations, Devices, etc.)
#     "Other": [
#         'B-Entity', 'I-Entity',
#         'B-Conceptual Entity', 'I-Conceptual Entity',
#         'B-Idea or Concept', 'I-Idea or Concept',
#         'B-Intellectual Product', 'I-Intellectual Product',
#         'B-Classification', 'I-Classification',
#         'B-Natural Phenomenon or Process', 'I-Natural Phenomenon or Process',
#         'B-Phenomenon or Process', 'I-Phenomenon or Process',
#         'B-Environmental Effect of Humans', 'I-Environmental Effect of Humans',
#         'B-Qualitative Concept', 'I-Qualitative Concept',
#         'B-Quantitative Concept', 'I-Quantitative Concept',
#         'B-Temporal Concept', 'I-Temporal Concept',
#         'B-Group Attribute', 'I-Group Attribute',
#         'B-Functional Concept', 'I-Functional Concept',
#         'B-Organism Attribute', 'I-Organism Attribute',
#         'B-Activity', 'I-Activity',
#         'B-Daily or Recreational Activity', 'I-Daily or Recreational Activity',
#         'B-Educational Activity', 'I-Educational Activity',
#         'B-Governmental or Regulatory Activity', 'I-Governmental or Regulatory Activity',
#         'B-Machine Activity', 'I-Machine Activity',
#         'B-Event', 'I-Event',
#         'B-Human-caused Phenomenon or Process', 'I-Human-caused Phenomenon or Process',
#         'B-Behavior', 'I-Behavior',
#         'B-Individual Behavior', 'I-Individual Behavior',
#         'B-Social Behavior', 'I-Social Behavior',
#         'B-Mental Process', 'I-Mental Process',
#         'B-Food', 'I-Food',
#         'B-Language', 'I-Language',
#         'B-Regulation or Law', 'I-Regulation or Law',
#         'B-Physical Object', 'I-Physical Object',
#         'B-Manufactured Object', 'I-Manufactured Object',
#         'B-Device', 'I-Device',
#         'B-Medical Device', 'I-Medical Device',  # Added
#         'B-Drug Delivery Device', 'I-Drug Delivery Device',  # Added
#         'B-Research Device', 'I-Research Device',  # Added
#         'B-Geographic Area', 'I-Geographic Area',  # Added
#         'B-Spatial Concept', 'I-Spatial Concept',  # Added
#         'B-UnknownType', 'I-UnknownType',  # Added
#         'B-Other', 'I-Other',
#         'O'
#     ]
# }
# # # Create a flat dictionary from the grouped mapping
# flat_mapping = {}
# for general_tag, specific_tags in generalized_mappings.items():
#     for tag in specific_tags:
#         flat_mapping[tag] = general_tag
# import pandas as pd

# # Load the Excel file
# df = pd.read_excel("C:/Users/Vaivaswatha/Downloads/final_test.xlsx")  # Replace with your file name

# # Function to convert tags
# def convert_tag(tag):
#     if tag == "O":
#         return "O"
#     if tag.startswith("B-"):
#         base = tag[2:]
#         return "B-" + flat_mapping.get(tag, tag)
#     elif tag.startswith("I-"):
#         base = tag[2:]
#         return "I-" + flat_mapping.get(tag, tag)
#     else:
#         return tag  # fallback if format is unexpected

# # Apply the conversion
# df["BIO_Tag"] = df["BIO_Tag"].apply(convert_tag)

# # Save to new Excel file
# df.to_excel("C:/Users/Vaivaswatha/Downloads/final_test_fix3.xlsx", index=False)

import pandas as pd

# Load the Excel file
df = pd.read_excel("C:/Users/Vaivaswatha/Downloads/final_train_fix3.xlsx")

# Ensure the column exists
if "BIO_Tag" not in df.columns:
    raise ValueError("The column 'BIO_Tag' is not in the Excel file.")

# Store cleaned tags (remove first two chars of suspicious tags)
cleaned_tags = []
for tag in df["BIO_Tag"].dropna():
    if isinstance(tag, str) and (tag.startswith("B-B-") or tag.startswith("I-I-")):
        cleaned_tags.append(tag[2:])  # Remove first two characters

# Optionally remove duplicates
cleaned_tags = list(set(cleaned_tags))

# Print result
print("Cleaned tags (without first two characters):")
for t in sorted(cleaned_tags):
    print(t)



