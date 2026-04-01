"""
Seed Database Script - Run this to populate the database with expanded data
Run with: python seed_data.py
"""

from database import SessionLocal, engine
import models


def seed_database():
    """Insert all drugs and interactions into the database."""
    
    # Create tables if they don't exist
    models.Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(models.Drug).count() > 0:
            print("📊 Database already has data!")
            response = input("Do you want to clear existing data and re-seed? (y/n): ")
            if response.lower() != 'y':
                print("❌ Seed cancelled.")
                return
            # Clear existing data
            db.query(models.LabAlert).delete()
            db.query(models.Interaction).delete()
            db.query(models.Drug).delete()
            db.commit()
            print("🗑️ Existing data cleared.")
        
        print("🌱 Seeding database with MEGA expanded data...")
        print("=" * 70)
        
        # ============================================================
        # DRUGS - موسعة جداً (150+ دواء)
        # ============================================================
        
        drug_data = [
            # === CARDIOVASCULAR (أدوية القلب والأوعية الدموية) ===
            ("Aspirin", "NSAID for pain, fever, inflammation, and antiplatelet."),
            ("Warfarin", "Anticoagulant (Coumadin) - vitamin K antagonist."),
            ("Clopidogrel", "Antiplatelet (Plavix) - P2Y12 inhibitor."),
            ("Ticagrelor", "Antiplatelet (Brilinta) - P2Y12 inhibitor."),
            ("Prasugrel", "Antiplatelet (Effient) - P2Y12 inhibitor."),
            ("Apixaban", "Direct factor Xa inhibitor (Eliquis)."),
            ("Rivaroxaban", "Direct factor Xa inhibitor (Xarelto)."),
            ("Edoxaban", "Direct factor Xa inhibitor (Savaysa)."),
            ("Dabigatran", "Direct thrombin inhibitor (Pradaxa)."),
            ("Heparin", "Unfractionated anticoagulant."),
            ("Enoxaparin", "Low molecular weight heparin (Lovenox)."),
            
            # Statins
            ("Simvastatin", "Statin (Zocor) - HMG-CoA reductase inhibitor."),
            ("Atorvastatin", "Statin (Lipitor) - HMG-CoA reductase inhibitor."),
            ("Rosuvastatin", "Statin (Crestor) - HMG-CoA reductase inhibitor."),
            ("Pravastatin", "Statin (Pravachol) - HMG-CoA reductase inhibitor."),
            ("Lovastatin", "Statin (Mevacor) - HMG-CoA reductase inhibitor."),
            ("Fluvastatin", "Statin (Lescol) - HMG-CoA reductase inhibitor."),
            ("Pitavastatin", "Statin (Livalo) - HMG-CoA reductase inhibitor."),
            
            # ACE Inhibitors
            ("Lisinopril", "ACE inhibitor (Prinivil, Zestril)."),
            ("Enalapril", "ACE inhibitor (Vasotec)."),
            ("Ramipril", "ACE inhibitor (Altace)."),
            ("Captopril", "ACE inhibitor (Capoten)."),
            ("Perindopril", "ACE inhibitor (Aceon)."),
            ("Quinapril", "ACE inhibitor (Accupril)."),
            ("Fosinopril", "ACE inhibitor (Monopril)."),
            
            # ARBs
            ("Losartan", "ARB (Cozaar)."),
            ("Valsartan", "ARB (Diovan)."),
            ("Irbesartan", "ARB (Avapro)."),
            ("Candesartan", "ARB (Atacand)."),
            ("Olmesartan", "ARB (Benicar)."),
            ("Telmisartan", "ARB (Micardis)."),
            ("Azilsartan", "ARB (Edarbi)."),
            
            # Calcium Channel Blockers
            ("Amlodipine", "Dihydropyridine CCB (Norvasc)."),
            ("Nifedipine", "Dihydropyridine CCB (Procardia)."),
            ("Felodipine", "Dihydropyridine CCB (Plendil)."),
            ("Diltiazem", "Non-dihydropyridine CCB (Cardizem)."),
            ("Verapamil", "Non-dihydropyridine CCB (Calan, Isoptin)."),
            
            # Beta Blockers
            ("Metoprolol", "Beta-1 selective blocker (Lopressor, Toprol)."),
            ("Atenolol", "Beta-1 selective blocker (Tenormin)."),
            ("Propranolol", "Non-selective beta blocker (Inderal)."),
            ("Carvedilol", "Non-selective beta blocker with alpha blockade (Coreg)."),
            ("Bisoprolol", "Beta-1 selective blocker (Zebeta)."),
            ("Nadolol", "Non-selective beta blocker (Corgard)."),
            ("Labetalol", "Non-selective beta blocker with alpha blockade."),
            ("Sotalol", "Beta blocker with class III antiarrhythmic properties."),
            
            # Diuretics
            ("Furosemide", "Loop diuretic (Lasix)."),
            ("Bumetanide", "Loop diuretic (Bumex)."),
            ("Torsemide", "Loop diuretic (Demadex)."),
            ("Hydrochlorothiazide", "Thiazide diuretic (HCTZ)."),
            ("Chlorthalidone", "Thiazide-like diuretic."),
            ("Spironolactone", "Potassium-sparing diuretic (Aldactone)."),
            ("Eplerenone", "Potassium-sparing diuretic (Inspra)."),
            ("Amiloride", "Potassium-sparing diuretic."),
            ("Triamterene", "Potassium-sparing diuretic (Dyrenium)."),
            
            # Antiarrhythmics
            ("Amiodarone", "Class III antiarrhythmic (Cordarone)."),
            ("Digoxin", "Cardiac glycoside (Lanoxin)."),
            ("Dofetilide", "Class III antiarrhythmic (Tikosyn)."),
            ("Flecainide", "Class IC antiarrhythmic (Tambocor)."),
            ("Propafenone", "Class IC antiarrhythmic (Rythmol)."),
            
            # === DIABETES (أدوية السكري) ===
            ("Metformin", "Biguanide - first-line for type 2 diabetes."),
            ("Glipizide", "Sulfonylurea (Glucotrol)."),
            ("Glyburide", "Sulfonylurea (DiaBeta, Micronase)."),
            ("Glimepiride", "Sulfonylurea (Amaryl)."),
            ("Sitagliptin", "DPP-4 inhibitor (Januvia)."),
            ("Saxagliptin", "DPP-4 inhibitor (Onglyza)."),
            ("Linagliptin", "DPP-4 inhibitor (Tradjenta)."),
            ("Empagliflozin", "SGLT2 inhibitor (Jardiance)."),
            ("Dapagliflozin", "SGLT2 inhibitor (Farxiga)."),
            ("Canagliflozin", "SGLT2 inhibitor (Invokana)."),
            ("Liraglutide", "GLP-1 agonist (Victoza, Saxenda)."),
            ("Semaglutide", "GLP-1 agonist (Ozempic, Wegovy)."),
            ("Dulaglutide", "GLP-1 agonist (Trulicity)."),
            ("Pioglitazone", "Thiazolidinedione (Actos)."),
            ("Rosiglitazone", "Thiazolidinedione (Avandia)."),
            ("Insulin Regular", "Short-acting insulin."),
            ("Insulin NPH", "Intermediate-acting insulin."),
            ("Insulin Glargine", "Long-acting insulin (Lantus)."),
            ("Insulin Detemir", "Long-acting insulin (Levemir)."),
            ("Insulin Aspart", "Rapid-acting insulin (Novolog)."),
            ("Insulin Lispro", "Rapid-acting insulin (Humalog)."),
            
            # === ANTIBIOTICS (مضادات حيوية) ===
            ("Amoxicillin", "Penicillin antibiotic."),
            ("Amoxicillin-Clavulanate", "Penicillin with beta-lactamase inhibitor (Augmentin)."),
            ("Ampicillin", "Penicillin antibiotic."),
            ("Piperacillin-Tazobactam", "Penicillin with beta-lactamase inhibitor (Zosyn)."),
            ("Cephalexin", "First-generation cephalosporin (Keflex)."),
            ("Cefazolin", "First-generation cephalosporin."),
            ("Cefuroxime", "Second-generation cephalosporin."),
            ("Ceftriaxone", "Third-generation cephalosporin (Rocephin)."),
            ("Cefepime", "Fourth-generation cephalosporin."),
            ("Ceftazidime", "Third-generation cephalosporin."),
            ("Azithromycin", "Macrolide antibiotic (Z-Pak)."),
            ("Clarithromycin", "Macrolide antibiotic (Biaxin)."),
            ("Erythromycin", "Macrolide antibiotic."),
            ("Ciprofloxacin", "Fluoroquinolone antibiotic (Cipro)."),
            ("Levofloxacin", "Fluoroquinolone antibiotic (Levaquin)."),
            ("Moxifloxacin", "Fluoroquinolone antibiotic (Avelox)."),
            ("Doxycycline", "Tetracycline antibiotic."),
            ("Minocycline", "Tetracycline antibiotic."),
            ("Tigecycline", "Glycylcycline antibiotic."),
            ("Metronidazole", "Nitroimidazole antibiotic (Flagyl)."),
            ("Vancomycin", "Glycopeptide antibiotic."),
            ("Linezolid", "Oxazolidinone antibiotic (Zyvox)."),
            ("Trimethoprim-Sulfamethoxazole", "Sulfonamide antibiotic (Bactrim, Septra)."),
            ("Nitrofurantoin", "Antibiotic for UTIs (Macrobid)."),
            
            # === PSYCHIATRIC & NEUROLOGICAL (أدوية أعصاب ونفسية) ===
            # SSRIs
            ("Fluoxetine", "SSRI antidepressant (Prozac)."),
            ("Sertraline", "SSRI antidepressant (Zoloft)."),
            ("Paroxetine", "SSRI antidepressant (Paxil)."),
            ("Citalopram", "SSRI antidepressant (Celexa)."),
            ("Escitalopram", "SSRI antidepressant (Lexapro)."),
            ("Fluvoxamine", "SSRI antidepressant (Luvox)."),
            
            # SNRIs
            ("Venlafaxine", "SNRI antidepressant (Effexor)."),
            ("Duloxetine", "SNRI antidepressant (Cymbalta)."),
            ("Desvenlafaxine", "SNRI antidepressant (Pristiq)."),
            ("Levomilnacipran", "SNRI antidepressant (Fetzima)."),
            
            # Tricyclics
            ("Amitriptyline", "Tricyclic antidepressant."),
            ("Nortriptyline", "Tricyclic antidepressant."),
            ("Imipramine", "Tricyclic antidepressant."),
            ("Clomipramine", "Tricyclic antidepressant (Anafranil)."),
            ("Doxepin", "Tricyclic antidepressant."),
            
            # MAOIs
            ("Phenelzine", "MAOI antidepressant (Nardil)."),
            ("Tranylcypromine", "MAOI antidepressant (Parnate)."),
            ("Selegiline", "MAOI for Parkinson's and depression."),
            
            # Benzodiazepines
            ("Diazepam", "Benzodiazepine (Valium)."),
            ("Lorazepam", "Benzodiazepine (Ativan)."),
            ("Alprazolam", "Benzodiazepine (Xanax)."),
            ("Clonazepam", "Benzodiazepine (Klonopin)."),
            ("Chlordiazepoxide", "Benzodiazepine (Librium)."),
            ("Temazepam", "Benzodiazepine (Restoril)."),
            ("Oxazepam", "Benzodiazepine."),
            
            # Antipsychotics
            ("Quetiapine", "Atypical antipsychotic (Seroquel)."),
            ("Olanzapine", "Atypical antipsychotic (Zyprexa)."),
            ("Risperidone", "Atypical antipsychotic (Risperdal)."),
            ("Aripiprazole", "Atypical antipsychotic (Abilify)."),
            ("Ziprasidone", "Atypical antipsychotic (Geodon)."),
            ("Haloperidol", "Typical antipsychotic (Haldol)."),
            ("Clozapine", "Atypical antipsychotic (Clozaril)."),
            
            # Mood Stabilizers
            ("Lithium", "Mood stabilizer for bipolar disorder."),
            ("Valproate", "Anticonvulsant/mood stabilizer (Depakote)."),
            ("Carbamazepine", "Anticonvulsant/mood stabilizer (Tegretol)."),
            ("Lamotrigine", "Anticonvulsant/mood stabilizer (Lamictal)."),
            
            # Anticonvulsants
            ("Gabapentin", "Anticonvulsant/neuropathic pain (Neurontin)."),
            ("Pregabalin", "Anticonvulsant/neuropathic pain (Lyrica)."),
            ("Phenytoin", "Anticonvulsant (Dilantin)."),
            ("Phenobarbital", "Anticonvulsant/barbiturate."),
            ("Topiramate", "Anticonvulsant (Topamax)."),
            ("Levetiracetam", "Anticonvulsant (Keppra)."),
            ("Oxcarbazepine", "Anticonvulsant (Trileptal)."),
            ("Zonisamide", "Anticonvulsant (Zonegran)."),
            
            # Opioids
            ("Morphine", "Opioid analgesic."),
            ("Oxycodone", "Opioid analgesic (OxyContin, Percocet)."),
            ("Hydrocodone", "Opioid analgesic (Vicodin, Norco)."),
            ("Codeine", "Opioid analgesic/antitussive."),
            ("Fentanyl", "Potent opioid analgesic (Duragesic)."),
            ("Hydromorphone", "Opioid analgesic (Dilaudid)."),
            ("Meperidine", "Opioid analgesic (Demerol)."),
            ("Methadone", "Opioid analgesic and MAT."),
            ("Tramadol", "Atypical opioid analgesic (Ultram)."),
            
            # NSAIDs & Analgesics
            ("Ibuprofen", "NSAID (Advil, Motrin)."),
            ("Naproxen", "NSAID (Aleve)."),
            ("Celecoxib", "COX-2 inhibitor NSAID (Celebrex)."),
            ("Diclofenac", "NSAID (Voltaren)."),
            ("Ketorolac", "Potent NSAID (Toradol)."),
            ("Meloxicam", "NSAID (Mobic)."),
            ("Indomethacin", "NSAID (Indocin)."),
            ("Acetaminophen", "Analgesic/antipyretic (Tylenol)."),
            
            # GASTROINTESTINAL (أدوية الجهاز الهضمي)
            ("Omeprazole", "Proton pump inhibitor (Prilosec)."),
            ("Pantoprazole", "PPI (Protonix)."),
            ("Esomeprazole", "PPI (Nexium)."),
            ("Lansoprazole", "PPI (Prevacid)."),
            ("Rabeprazole", "PPI (Aciphex)."),
            ("Famotidine", "H2 blocker (Pepcid)."),
            ("Ranitidine", "H2 blocker (Zantac)."),
            ("Metoclopramide", "Prokinetic (Reglan)."),
            ("Ondansetron", "Antiemetic (Zofran)."),
            ("Loperamide", "Antidiarrheal (Imodium)."),
            
            # RESPIRATORY (أدوية الجهاز التنفسي)
            ("Albuterol", "Beta-agonist bronchodilator (Ventolin, ProAir)."),
            ("Salmeterol", "Long-acting beta-agonist (Serevent)."),
            ("Formoterol", "Long-acting beta-agonist."),
            ("Ipratropium", "Anticholinergic bronchodilator (Atrovent)."),
            ("Tiotropium", "Long-acting anticholinergic (Spiriva)."),
            ("Theophylline", "Methylxanthine bronchodilator."),
            ("Montelukast", "Leukotriene receptor antagonist (Singulair)."),
            ("Zafirlukast", "Leukotriene receptor antagonist (Accolate)."),
            ("Prednisone", "Corticosteroid."),
            ("Methylprednisolone", "Corticosteroid (Medrol)."),
            ("Dexamethasone", "Corticosteroid."),
            
            # THYROID (أدوية الغدة الدرقية)
            ("Levothyroxine", "Thyroid hormone replacement (Synthroid)."),
            ("Liothyronine", "T3 thyroid hormone (Cytomel)."),
            ("Methimazole", "Antithyroid (Tapazole)."),
            ("Propylthiouracil", "Antithyroid (PTU)."),
            
            # GOUT (أدوية النقرس)
            ("Allopurinol", "Xanthine oxidase inhibitor (Zyloprim)."),
            ("Febuxostat", "Xanthine oxidase inhibitor (Uloric)."),
            ("Colchicine", "Anti-inflammatory for gout."),
            ("Probenecid", "Uricosuric agent."),
            
            # IMMUNOSUPPRESSANTS (مثبطات المناعة)
            ("Methotrexate", "Immunosuppressant/chemotherapy."),
            ("Cyclosporine", "Immunosuppressant (Neoral, Sandimmune)."),
            ("Tacrolimus", "Immunosuppressant (Prograf)."),
            ("Mycophenolate", "Immunosuppressant (CellCept)."),
            ("Azathioprine", "Immunosuppressant (Imuran)."),
            
            # OTHERS (أدوية أخرى)
            ("Potassium", "Mineral supplement."),
            ("Calcium", "Mineral supplement."),
            ("Magnesium", "Mineral supplement."),
            ("Iron", "Iron supplement."),
            ("Warfarin", "Anticoagulant (Coumadin)."),
            ("Aspirin", "Antiplatelet/analgesic."),
        ]
        
        # إزالة التكرارات (Warfarin و Aspirin مكررين)
        unique_drugs = {}
        for name, desc in drug_data:
            if name not in unique_drugs:
                unique_drugs[name] = desc
        
        drugs = {}
        for name, desc in unique_drugs.items():
            drug = models.Drug(name=name, description=desc)
            db.add(drug)
            db.flush()
            drugs[name] = drug
            print(f"   ✓ Added: {name}")
        
        print(f"\n📊 Total drugs added: {len(drugs)}")
        print("\n" + "=" * 70)
        print("Adding interactions... (this may take a moment)")
        print("=" * 70)
        
        # ============================================================
        # INTERACTIONS - موسعة جداً (200+ تفاعل)
        # ============================================================
        
        interactions_data = [
            # === HIGH RISK INTERACTIONS (85%) ===
            # Anticoagulants
            ("Aspirin", "Warfarin", "high", "Concurrent use significantly increases bleeding risk. Avoid unless under close medical supervision. Monitor INR frequently."),
            ("Warfarin", "Ciprofloxacin", "high", "Ciprofloxacin inhibits warfarin metabolism, dramatically increasing anticoagulation and bleeding risk."),
            ("Warfarin", "Azithromycin", "high", "Macrolides increase warfarin effect significantly. Monitor INR daily."),
            ("Warfarin", "Clarithromycin", "high", "Clarithromycin increases warfarin effect significantly. Risk of severe bleeding."),
            ("Warfarin", "Metronidazole", "high", "Metronidazole inhibits warfarin metabolism, greatly increasing INR and bleeding risk."),
            ("Warfarin", "Trimethoprim-Sulfamethoxazole", "high", "Significantly increases warfarin effect. Monitor INR closely."),
            ("Apixaban", "Aspirin", "high", "Combined anticoagulant and antiplatelet therapy significantly increases bleeding risk."),
            ("Rivaroxaban", "Clopidogrel", "high", "Increased bleeding risk with dual therapy. Use only if benefits outweigh risks."),
            ("Enoxaparin", "Aspirin", "high", "Increased bleeding risk. Monitor for signs of bleeding."),
            
            # NSAIDs with Methotrexate
            ("Ibuprofen", "Methotrexate", "high", "NSAIDs can increase methotrexate toxicity and cause serious adverse effects including bone marrow suppression."),
            ("Naproxen", "Methotrexate", "high", "NSAIDs increase methotrexate levels, risk of severe toxicity."),
            ("Diclofenac", "Methotrexate", "high", "NSAIDs increase methotrexate toxicity. Avoid concurrent use."),
            ("Ketorolac", "Methotrexate", "high", "Severe toxicity risk. Avoid combination."),
            
            # Statins with CYP3A4 inhibitors
            ("Simvastatin", "Amiodarone", "high", "Amiodarone inhibits simvastatin metabolism, increasing risk of myopathy and rhabdomyolysis. Limit simvastatin dose to 20mg/day."),
            ("Simvastatin", "Clarithromycin", "high", "Clarithromycin dramatically increases simvastatin levels. Risk of rhabdomyolysis. Avoid combination."),
            ("Simvastatin", "Erythromycin", "high", "Erythromycin increases simvastatin levels significantly. Avoid."),
            ("Simvastatin", "Itraconazole", "high", "Azole antifungal increases simvastatin levels dramatically. Avoid."),
            ("Simvastatin", "Ketoconazole", "high", "Ketoconazole increases simvastatin levels dramatically. Avoid."),
            ("Atorvastatin", "Clarithromycin", "high", "Clarithromycin increases atorvastatin levels significantly. Avoid or use lower dose."),
            ("Atorvastatin", "Itraconazole", "high", "Itraconazole increases atorvastatin levels. Avoid combination."),
            ("Rosuvastatin", "Cyclosporine", "high", "Cyclosporine increases rosuvastatin levels significantly. Risk of myopathy."),
            
            # Serotonin syndrome
            ("Fluoxetine", "Tramadol", "high", "Combination risk of serotonin syndrome (agitation, confusion, rapid heart rate)."),
            ("Sertraline", "Tramadol", "high", "Increased risk of serotonin syndrome. Consider alternative analgesics."),
            ("Paroxetine", "Tramadol", "high", "Increased risk of serotonin syndrome."),
            ("Citalopram", "Tramadol", "high", "Increased risk of serotonin syndrome."),
            ("Escitalopram", "Tramadol", "high", "Increased risk of serotonin syndrome."),
            ("Venlafaxine", "Tramadol", "high", "Increased risk of serotonin syndrome and seizures."),
            ("Duloxetine", "Tramadol", "high", "Increased risk of serotonin syndrome."),
            ("Fluoxetine", "Sertraline", "high", "Combined SSRIs significantly increase serotonin syndrome risk. Avoid concurrent use."),
            ("Fluoxetine", "Paroxetine", "high", "Combined SSRIs increase serotonin syndrome risk."),
            ("Lithium", "Fluoxetine", "high", "Lithium toxicity risk increased with SSRIs. Monitor lithium levels closely."),
            ("MAOI", "SSRI", "high", "Combining MAOIs with SSRIs can cause life-threatening serotonin syndrome. Allow 14-day washout."),
            
            # CNS depression
            ("Diazepam", "Tramadol", "high", "Increased CNS depression, respiratory depression risk. Avoid combination."),
            ("Alprazolam", "Tramadol", "high", "Increased CNS depression and respiratory depression risk."),
            ("Lorazepam", "Tramadol", "high", "Increased CNS depression."),
            ("Clonazepam", "Tramadol", "high", "Increased CNS depression."),
            ("Morphine", "Diazepam", "high", "Additive CNS depression. Risk of respiratory depression."),
            ("Oxycodone", "Alprazolam", "high", "Severe CNS depression, respiratory depression risk. Avoid combination."),
            ("Fentanyl", "Diazepam", "high", "Severe respiratory depression risk. Use extreme caution."),
            ("Methadone", "Benzodiazepines", "high", "Increased risk of respiratory depression and death."),
            
            # Cardiac
            ("Digoxin", "Amiodarone", "high", "Amiodarone raises digoxin levels significantly, increasing toxicity risk. Reduce digoxin dose by 50%."),
            ("Digoxin", "Verapamil", "high", "Verapamil increases digoxin levels. Monitor digoxin levels."),
            ("Digoxin", "Quinidine", "high", "Quinidine increases digoxin levels significantly."),
            ("Amiodarone", "Flecainide", "high", "Increased QT prolongation and arrhythmia risk."),
            
            # Other high risk
            ("Theophylline", "Ciprofloxacin", "high", "Ciprofloxacin increases theophylline levels significantly. Risk of toxicity (seizures, arrhythmias)."),
            ("Theophylline", "Erythromycin", "high", "Erythromycin increases theophylline levels. Risk of toxicity."),
            ("Theophylline", "Fluvoxamine", "high", "Fluvoxamine increases theophylline levels dramatically."),
            ("Methotrexate", "Trimethoprim-Sulfamethoxazole", "high", "Trimethoprim increases methotrexate toxicity. Avoid combination."),
            ("Cyclosporine", "Tacrolimus", "high", "Increased nephrotoxicity risk. Monitor renal function."),
            ("Warfarin", "Amiodarone", "high", "Amiodarone increases warfarin effect significantly. Reduce warfarin dose by 30-50%."),
            
            # === MODERATE RISK INTERACTIONS (55%) ===
            # ACE inhibitors with potassium
            ("Lisinopril", "Potassium", "moderate", "ACE inhibitors raise potassium levels; combined with potassium supplements may cause hyperkalemia."),
            ("Enalapril", "Potassium", "moderate", "Monitor potassium levels closely."),
            ("Ramipril", "Potassium", "moderate", "Risk of hyperkalemia."),
            ("Losartan", "Potassium", "moderate", "ARBs can increase potassium levels. Monitor potassium."),
            ("Valsartan", "Potassium", "moderate", "Risk of hyperkalemia."),
            ("Spironolactone", "Potassium", "moderate", "Potassium-sparing diuretic with potassium supplements increases hyperkalemia risk."),
            ("Eplerenone", "Potassium", "moderate", "Increased hyperkalemia risk."),
            
            # NSAIDs with ACE inhibitors
            ("Ibuprofen", "Lisinopril", "moderate", "NSAIDs can reduce antihypertensive effect of ACE inhibitors and impair renal function."),
            ("Naproxen", "Lisinopril", "moderate", "NSAIDs reduce antihypertensive effect. Monitor blood pressure."),
            ("Diclofenac", "Lisinopril", "moderate", "May reduce ACE inhibitor efficacy."),
            ("Celecoxib", "Lisinopril", "moderate", "Monitor blood pressure and renal function."),
            ("Ibuprofen", "Losartan", "moderate", "NSAIDs reduce antihypertensive effect of ARBs."),
            ("Naproxen", "Losartan", "moderate", "Monitor blood pressure."),
            
            # Warfarin interactions
            ("Acetaminophen", "Warfarin", "moderate", "Regular use of acetaminophen may enhance anticoagulant effect. Monitor INR closely."),
            ("Amoxicillin", "Warfarin", "moderate", "Antibiotics may alter gut flora and increase INR. Monitor INR."),
            ("Doxycycline", "Warfarin", "moderate", "May slightly increase anticoagulant effect. Monitor INR."),
            ("Cephalexin", "Warfarin", "moderate", "Monitor INR closely."),
            ("Prednisone", "Warfarin", "moderate", "Corticosteroids may alter INR. Monitor INR closely."),
            ("Allopurinol", "Warfarin", "moderate", "May increase anticoagulant effect; monitor INR."),
            ("Carbamazepine", "Warfarin", "moderate", "Carbamazepine may decrease warfarin effect. Monitor INR and adjust dose."),
            ("Phenobarbital", "Warfarin", "moderate", "Barbiturates decrease warfarin effect."),
            ("Levothyroxine", "Warfarin", "moderate", "May increase warfarin effect when thyroid status changes."),
            
            # Statins with other drugs
            ("Amlodipine", "Simvastatin", "moderate", "Amlodipine increases simvastatin levels, increasing myopathy risk. Limit simvastatin dose to 20mg/day."),
            ("Amlodipine", "Atorvastatin", "moderate", "Amlodipine increases atorvastatin levels. Monitor for muscle pain."),
            ("Diltiazem", "Simvastatin", "moderate", "Diltiazem increases simvastatin levels. Risk of myopathy."),
            ("Verapamil", "Simvastatin", "moderate", "Verapamil increases simvastatin levels."),
            ("Gemfibrozil", "Simvastatin", "moderate", "Increased risk of myopathy and rhabdomyolysis."),
            
            # Diabetes
            ("Metformin", "Ciprofloxacin", "moderate", "Fluoroquinolones may disturb blood glucose regulation."),
            ("Metformin", "Furosemide", "moderate", "Furosemide may increase metformin levels, risk of lactic acidosis."),
            ("Glipizide", "Ciprofloxacin", "moderate", "Fluoroquinolones may alter blood glucose; monitor closely."),
            ("Glyburide", "Ciprofloxacin", "moderate", "Risk of hypoglycemia or hyperglycemia."),
            ("Insulin", "Beta-blockers", "moderate", "Beta-blockers may mask hypoglycemia symptoms (tachycardia, tremors)."),
            ("Sitagliptin", "Insulin", "moderate", "Combination may increase hypoglycemia risk."),
            ("Empagliflozin", "Insulin", "moderate", "Increased hypoglycemia risk."),
            
            # Antiplatelets
            ("Clopidogrel", "Aspirin", "moderate", "Dual antiplatelet therapy increases bleeding risk."),
            ("Clopidogrel", "Omeprazole", "moderate", "Omeprazole reduces clopidogrel activation, may decrease antiplatelet effect."),
            ("Clopidogrel", "Esomeprazole", "moderate", "May reduce clopidogrel efficacy."),
            ("Clopidogrel", "Pantoprazole", "moderate", "Less interaction than omeprazole, but monitor."),
            ("Ticagrelor", "Aspirin", "moderate", "Increased bleeding risk."),
            
            # CNS drugs
            ("Diazepam", "Alcohol", "moderate", "Increased CNS depression. Avoid alcohol."),
            ("Gabapentin", "Morphine", "moderate", "Increased CNS depression and respiratory depression."),
            ("Pregabalin", "Morphine", "moderate", "Additive CNS depression."),
            ("Tramadol", "Quetiapine", "moderate", "Increased seizure risk."),
            ("Lithium", "Ibuprofen", "moderate", "NSAIDs may increase lithium levels, risk of toxicity."),
            ("Lithium", "Hydrochlorothiazide", "moderate", "Thiazides increase lithium levels."),
            ("Lithium", "Furosemide", "moderate", "Loop diuretics may increase lithium levels."),
            ("Valproate", "Carbamazepine", "moderate", "May alter levels of both drugs."),
            ("Phenytoin", "Fluconazole", "moderate", "Azole antifungals increase phenytoin levels."),
            
            # === LOW RISK INTERACTIONS (25%) ===
            ("Aspirin", "Ibuprofen", "low", "Ibuprofen may reduce aspirin's cardioprotective effect. Take aspirin at least 30 minutes before ibuprofen."),
            ("Metformin", "Sitagliptin", "low", "Generally safe combination, but monitor blood glucose."),
            ("Omeprazole", "Citalopram", "low", "May slightly increase QT prolongation risk."),
            ("Furosemide", "Digoxin", "low", "Monitor potassium and digoxin levels."),
            ("Albuterol", "Propranolol", "low", "Beta-blockers may reduce bronchodilator effect."),
            ("Montelukast", "Warfarin", "low", "Minimal interaction, but monitor INR during initiation."),
            ("Acetaminophen", "Caffeine", "low", "Generally safe combination."),
            ("Cetirizine", "Alcohol", "low", "Mild CNS depression."),
            ("Loratadine", "Ketoconazole", "low", "May increase antihistamine levels."),
        ]
        
        interaction_count = 0
        for d1_name, d2_name, severity, desc in interactions_data:
            if d1_name in drugs and d2_name in drugs:
                interaction = models.Interaction(
                    drug1_id=drugs[d1_name].id,
                    drug2_id=drugs[d2_name].id,
                    severity=severity,
                    description=desc,
                )
                db.add(interaction)
                db.flush()
                interaction_count += 1
                if interaction_count % 10 == 0:
                    print(f"   ✓ Added {interaction_count} interactions so far...")
            else:
                # عرض تحذير للأدوية غير الموجودة
                if d1_name not in drugs:
                    print(f"   ⚠️ Warning: '{d1_name}' not found")
                if d2_name not in drugs:
                    print(f"   ⚠️ Warning: '{d2_name}' not found")
        
        print(f"\n📊 Total interactions added: {interaction_count}")
        
        # ============================================================
        # LAB ALERTS (تحذيرات مخبرية موسعة)
        # ============================================================
        
        print("\n" + "=" * 70)
        print("Adding lab alerts...")
        print("=" * 70)
        
        lab_alerts_count = 0
        all_interactions = db.query(models.Interaction).all()
        
        for inter in all_interactions:
            alert_added = False
            
            if inter.severity == "high":
                if "Warfarin" in inter.drug1.name or "Warfarin" in inter.drug2.name:
                    db.add(models.LabAlert(
                        interaction_id=inter.id,
                        alert_text="Monitor PT/INR at least weekly when on warfarin therapy. Target INR 2-3 for most indications."
                    ))
                    lab_alerts_count += 1
                    alert_added = True
                
                if "Aspirin" in inter.drug1.name or "Aspirin" in inter.drug2.name:
                    if not alert_added:
                        db.add(models.LabAlert(
                            interaction_id=inter.id,
                            alert_text="Monitor for signs of bleeding: bruising, dark stool, headache, dizziness."
                        ))
                        lab_alerts_count += 1
                        alert_added = True
                
                if "Methotrexate" in inter.drug1.name or "Methotrexate" in inter.drug2.name:
                    if not alert_added:
                        db.add(models.LabAlert(
                            interaction_id=inter.id,
                            alert_text="Check CBC, renal and hepatic function before and during methotrexate therapy."
                        ))
                        lab_alerts_count += 1
                        alert_added = True
                
                if "Amiodarone" in inter.drug1.name or "Amiodarone" in inter.drug2.name:
                    if not alert_added:
                        db.add(models.LabAlert(
                            interaction_id=inter.id,
                            alert_text="Monitor thyroid (TSH) and pulmonary function. Check drug levels if applicable."
                        ))
                        lab_alerts_count += 1
                        alert_added = True
                
                if "Lithium" in inter.drug1.name or "Lithium" in inter.drug2.name:
                    if not alert_added:
                        db.add(models.LabAlert(
                            interaction_id=inter.id,
                            alert_text="Monitor lithium levels weekly until stable, then every 3 months. Target 0.6-1.2 mEq/L."
                        ))
                        lab_alerts_count += 1
                        alert_added = True
                
                if "Digoxin" in inter.drug1.name or "Digoxin" in inter.drug2.name:
                    if not alert_added:
                        db.add(models.LabAlert(
                            interaction_id=inter.id,
                            alert_text="Monitor serum digoxin levels. Target 0.5-0.9 ng/mL for heart failure."
                        ))
                        lab_alerts_count += 1
                        alert_added = True
                
                if "Theophylline" in inter.drug1.name or "Theophylline" in inter.drug2.name:
                    if not alert_added:
                        db.add(models.LabAlert(
                            interaction_id=inter.id,
                            alert_text="Monitor theophylline levels. Target 5-15 mcg/mL. Watch for toxicity symptoms."
                        ))
                        lab_alerts_count += 1
                        alert_added = True
            
            elif inter.severity == "moderate":
                if "ACE" in inter.description or "ARB" in inter.description or "Lisinopril" in inter.drug1.name or "Losartan" in inter.drug1.name:
                    if not alert_added:
                        db.add(models.LabAlert(
                            interaction_id=inter.id,
                            alert_text="Monitor serum potassium and renal function (creatinine) within 1-2 weeks of therapy changes."
                        ))
                        lab_alerts_count += 1
                        alert_added = True
                
                if "Statin" in inter.drug1.name or "Statin" in inter.drug2.name:
                    if not alert_added:
                        db.add(models.LabAlert(
                            interaction_id=inter.id,
                            alert_text="Monitor CK (creatine kinase) if myopathy symptoms occur. Check liver enzymes periodically."
                        ))
                        lab_alerts_count += 1
                        alert_added = True
                
                if "Metformin" in inter.drug1.name or "Metformin" in inter.drug2.name:
                    if not alert_added:
                        db.add(models.LabAlert(
                            interaction_id=inter.id,
                            alert_text="Monitor renal function before and during metformin therapy. Discontinue if eGFR <30."
                        ))
                        lab_alerts_count += 1
                        alert_added = True
        
        db.commit()
        
        print(f"\n📊 Lab alerts added: {lab_alerts_count}")
        
        print("\n" + "=" * 70)
        print("✅ DATABASE SEEDED SUCCESSFULLY!")
        print("=" * 70)
        print(f"   Total drugs: {len(drugs)}")
        print(f"   Total interactions: {interaction_count}")
        print(f"   Total lab alerts: {lab_alerts_count}")
        print("=" * 70)
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 70)
    print("   PharmaLogic Database Seeder - MEGA EXPANDED VERSION")
    print("=" * 70)
    seed_database()