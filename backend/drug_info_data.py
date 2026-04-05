"""
Drug information database for Medical Team reference
"""

DRUG_INFO = {
    "Metformin": {
        "common_uses": [
            "Type 2 diabetes mellitus",
            "Polycystic ovary syndrome (PCOS)",
            "Prediabetes",
            "Gestational diabetes"
        ],
        "side_effects": [
            "Gastrointestinal: nausea, diarrhea, abdominal pain (most common)",
            "Metallic taste in mouth",
            "Vitamin B12 deficiency with long-term use",
            "Lactic acidosis (rare but serious)",
            "Weight loss (beneficial effect)"
        ],
        "contraindications": [
            "Severe renal impairment (eGFR < 30 mL/min)",
            "Metabolic acidosis",
            "Severe liver disease",
            "Acute conditions with risk of tissue hypoxia (sepsis, dehydration, heart failure)",
            "Hypersensitivity to metformin"
        ],
        "vitamin_depletions": [
            "Vitamin B12 deficiency with long-term use (monitor annually)"
        ],
        "pregnancy_safety": "Category B. Generally considered safe, but insulin is preferred if needed for glycemic control.",
        "counseling_points": [
            "Take with meals to reduce GI side effects",
            "Monitor kidney function annually",
            "Check Vitamin B12 levels annually",
            "Discontinue temporarily before contrast dye procedures",
            "Report symptoms of lactic acidosis: muscle pain, trouble breathing, dizziness"
        ],
        "references": [
            "FDA Labeling Information",
            "UpToDate: Metformin drug information",
            "Lexicomp: Metformin monograph"
        ]
    },
    
    "Aspirin": {
        "common_uses": [
            "Pain relief (headache, toothache, muscle pain)",
            "Fever reduction",
            "Inflammation reduction",
            "Cardiovascular protection (low dose)",
            "Prevention of recurrent stroke or heart attack"
        ],
        "side_effects": [
            "Gastrointestinal bleeding",
            "Heartburn and upset stomach",
            "Nausea and vomiting",
            "Ringing in ears (tinnitus) with high doses",
            "Reye's syndrome in children with viral illness",
            "Bruising and bleeding"
        ],
        "contraindications": [
            "Active peptic ulcer disease",
            "Bleeding disorders (hemophilia, von Willebrand)",
            "Severe hepatic impairment",
            "Children with viral illness (Reye's syndrome risk)",
            "Gout (can increase uric acid)",
            "Third trimester of pregnancy"
        ],
        "vitamin_depletions": [
            "Vitamin C (may increase excretion)",
            "Folate (with high doses)"
        ],
        "pregnancy_safety": "Category C (first and second trimester), Category D (third trimester - avoid).",
        "counseling_points": [
            "Take with food or full glass of water to reduce stomach upset",
            "Do not give to children with fever or flu-like symptoms",
            "Report signs of bleeding: black/tarry stools, blood in urine, easy bruising",
            "Stop 7 days before surgery",
            "Do not drink alcohol while taking aspirin"
        ],
        "references": [
            "FDA Labeling Information",
            "UpToDate: Aspirin drug information"
        ]
    },
    
    "Warfarin": {
        "common_uses": [
            "Prevention of stroke in atrial fibrillation",
            "Treatment of deep vein thrombosis (DVT)",
            "Treatment of pulmonary embolism (PE)",
            "Prevention of recurrent DVT/PE",
            "Mechanical heart valves",
            "Prevention of blood clots after surgery"
        ],
        "side_effects": [
            "Bleeding (most serious)",
            "Skin necrosis (rare, early therapy)",
            "Purple toes syndrome",
            "Nausea and vomiting",
            "Hair loss",
            "Calciphylaxis"
        ],
        "contraindications": [
            "Active bleeding",
            "Pregnancy (teratogenic)",
            "Severe uncontrolled hypertension",
            "Recent or planned surgery",
            "Bleeding disorders",
            "Thrombocytopenia"
        ],
        "vitamin_depletions": [
            "Vitamin K (interaction, not depletion - maintain consistent intake)"
        ],
        "pregnancy_safety": "Category X - CONTRAINDICATED (teratogenic). Use alternative anticoagulants.",
        "counseling_points": [
            "Monitor INR regularly (target 2-3 for most indications)",
            "Maintain consistent Vitamin K intake (avoid sudden changes in green leafy vegetables)",
            "Report signs of bleeding: bruising, dark stool, blood in urine, headache",
            "Use soft toothbrush and electric razor",
            "Avoid alcohol and OTC medications (especially NSAIDs)",
            "Wear medical alert bracelet"
        ],
        "references": [
            "FDA Labeling Information",
            "UpToDate: Warfarin drug information"
        ]
    },
    
    "Omeprazole": {
        "common_uses": [
            "Gastroesophageal reflux disease (GERD)",
            "Peptic ulcer disease",
            "Erosive esophagitis",
            "Zollinger-Ellison syndrome",
            "Helicobacter pylori eradication (part of combination therapy)",
            "Stress ulcer prophylaxis"
        ],
        "side_effects": [
            "Headache",
            "Nausea and vomiting",
            "Diarrhea or constipation",
            "Abdominal pain",
            "Vitamin B12 deficiency with long-term use",
            "Magnesium deficiency with long-term use",
            "Increased risk of Clostridioides difficile infection",
            "Increased risk of bone fractures with long-term high-dose use"
        ],
        "contraindications": [
            "Hypersensitivity to omeprazole or other PPIs",
            "Concurrent use with rilpivirine-containing products",
            "Severe hepatic impairment (use lower doses)"
        ],
        "vitamin_depletions": [
            "Vitamin B12 deficiency (long-term use)",
            "Magnesium deficiency (long-term use)",
            "Calcium malabsorption (may affect bone density)"
        ],
        "pregnancy_safety": "Category C. Use only if clearly needed.",
        "counseling_points": [
            "Take 30-60 minutes before first meal of the day",
            "Do not crush or chew capsules (swallow whole)",
            "Long-term use may require Vitamin B12 and magnesium monitoring",
            "Report persistent diarrhea (possible C. diff infection)",
            "Do not stop abruptly - taper if possible"
        ],
        "references": [
            "FDA Labeling Information",
            "UpToDate: Omeprazole drug information"
        ]
    },
    
    "Amoxicillin": {
        "common_uses": [
            "Upper respiratory tract infections (sinusitis, pharyngitis, tonsillitis)",
            "Lower respiratory tract infections (bronchitis, pneumonia)",
            "Otitis media (middle ear infection)",
            "Urinary tract infections",
            "Skin and soft tissue infections",
            "Helicobacter pylori eradication (with other agents)",
            "Dental infections",
            "Lyme disease (early stage)"
        ],
        "side_effects": [
            "Diarrhea (most common)",
            "Nausea and vomiting",
            "Rash (including non-allergic amoxicillin rash)",
            "Oral or vaginal candidiasis (thrush)",
            "Allergic reactions (rash, urticaria, anaphylaxis - rare)",
            "Antibiotic-associated colitis"
        ],
        "contraindications": [
            "Penicillin allergy (cross-reactivity with cephalosporins)",
            "Infectious mononucleosis (risk of amoxicillin rash)"
        ],
        "vitamin_depletions": [
            "May disrupt gut microbiome, affecting Vitamin K synthesis"
        ],
        "pregnancy_safety": "Category B. Generally considered safe.",
        "counseling_points": [
            "Complete full course even if feeling better",
            "Take with or without food",
            "Report severe diarrhea (possible C. diff infection)",
            "Inform healthcare provider of any rash (possible allergy)",
            "Use reliable contraception (may reduce efficacy of oral contraceptives)"
        ],
        "references": [
            "FDA Labeling Information",
            "UpToDate: Amoxicillin drug information"
        ]
    },
    
    "Lisinopril": {
        "common_uses": [
            "Hypertension (high blood pressure)",
            "Heart failure",
            "Post-myocardial infarction (heart attack)",
            "Diabetic nephropathy (kidney protection in diabetes)"
        ],
        "side_effects": [
            "Dry, persistent cough (common reason for discontinuation)",
            "Dizziness and hypotension",
            "Headache",
            "Hyperkalemia (high potassium)",
            "Acute kidney injury",
            "Angioedema (swelling of face, lips, tongue - rare but serious)",
            "Rash"
        ],
        "contraindications": [
            "History of angioedema with previous ACE inhibitor use",
            "Bilateral renal artery stenosis",
            "Pregnancy (second and third trimesters - Category D)",
            "Concurrent use with aliskiren in diabetics"
        ],
        "vitamin_depletions": [
            "No significant vitamin depletions"
        ],
        "pregnancy_safety": "Category D (second and third trimesters) - CONTRAINDICATED. Use alternative antihypertensives.",
        "counseling_points": [
            "May cause dizziness, especially with first dose - rise slowly",
            "Report persistent dry cough (may need to switch to ARB)",
            "Report signs of angioedema (swelling of face, lips, tongue, difficulty breathing)",
            "Avoid potassium supplements and salt substitutes",
            "Monitor blood pressure and kidney function regularly",
            "Avoid dehydration"
        ],
        "references": [
            "FDA Labeling Information",
            "UpToDate: Lisinopril drug information"
        ]
    }
}


def get_common_uses(drug_name: str) -> list:
    return DRUG_INFO.get(drug_name, {}).get("common_uses", ["Information not available in database"])


def get_side_effects(drug_name: str) -> list:
    return DRUG_INFO.get(drug_name, {}).get("side_effects", ["Information not available in database"])


def get_contraindications(drug_name: str) -> list:
    return DRUG_INFO.get(drug_name, {}).get("contraindications", ["Information not available in database"])


def get_vitamin_depletions(drug_name: str) -> list:
    return DRUG_INFO.get(drug_name, {}).get("vitamin_depletions", ["None reported in database"])


def get_pregnancy_safety(drug_name: str) -> str:
    return DRUG_INFO.get(drug_name, {}).get("pregnancy_safety", "Information not available in database. Consult healthcare provider.")


def get_counseling_points(drug_name: str) -> list:
    return DRUG_INFO.get(drug_name, {}).get("counseling_points", ["Consult healthcare provider for counseling information"])


def get_references(drug_name: str) -> list:
    return DRUG_INFO.get(drug_name, {}).get("references", ["Standard drug references"])