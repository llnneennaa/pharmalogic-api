"""
Rules Engine for Drug Interaction Analysis
"""

from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
import models


def check_allergy_warnings(drug_names: List[str], allergies: str) -> List[str]:
    """
    Check for allergy warnings based on patient allergies
    Returns list of warnings for drugs that may cause allergic reactions
    """
    warnings = []
    
    print(f"🔍 Checking allergies: {allergies}")
    print(f"🔍 Against drugs: {drug_names}")
    
    if not allergies:
        return warnings
    
    # تحويل الحساسيات إلى قائمة
    allergy_list = [a.strip().lower() for a in allergies.split(",") if a.strip()]
    print(f"🔍 Parsed allergies: {allergy_list}")
    
    # قاعدة بيانات الحساسيات الشائعة والأدوية المرتبطة بها
    allergy_rules = {
        # مضادات حيوية
        "penicillin": ["amoxicillin", "ampicillin", "penicillin", "amoxicillin-clavulanate", "piperacillin", "dicloxacillin"],
        "cephalosporin": ["cephalexin", "cefazolin", "cefuroxime", "ceftriaxone", "cefepime", "ceftazidime"],
        "sulfa": ["trimethoprim-sulfamethoxazole", "sulfamethoxazole", "sulfasalazine", "sulfadiazine"],
        "macrolide": ["azithromycin", "clarithromycin", "erythromycin"],
        "fluoroquinolone": ["ciprofloxacin", "levofloxacin", "moxifloxacin", "ofloxacin"],
        "tetracycline": ["doxycycline", "minocycline", "tetracycline"],
        "vancomycin": ["vancomycin"],
        "metronidazole": ["metronidazole"],
        
        # مضادات التهاب غير ستيرويدية
        "nsaids": ["aspirin", "ibuprofen", "naproxen", "diclofenac", "celecoxib", "ketorolac", "meloxicam", "indomethacin"],
        "aspirin": ["aspirin"],
        "ibuprofen": ["ibuprofen"],
        "naproxen": ["naproxen"],
        
        # مسكنات أفيونية
        "opioid": ["morphine", "codeine", "oxycodone", "hydrocodone", "fentanyl", "hydromorphone", "methadone", "tramadol"],
        "codeine": ["codeine"],
        "morphine": ["morphine"],
        
        # أدوية قلب
        "ace inhibitor": ["lisinopril", "enalapril", "ramipril", "captopril", "perindopril", "quinapril", "fosinopril"],
        "arb": ["losartan", "valsartan", "irbesartan", "candesartan", "olmesartan", "telmisartan"],
        "statin": ["simvastatin", "atorvastatin", "rosuvastatin", "pravastatin", "lovastatin", "fluvastatin", "pitavastatin"],
        "beta blocker": ["metoprolol", "atenolol", "propranolol", "carvedilol", "bisoprolol", "nadolol", "labetalol"],
        
        # أدوية سكري
        "metformin": ["metformin"],
        "sulfonylurea": ["glipizide", "glyburide", "glimepiride"],
        "insulin": ["insulin", "insulin regular", "insulin nph", "insulin glargine", "insulin detemir", "insulin aspart", "insulin lispro"],
        
        # أدوية أعصاب
        "ssri": ["fluoxetine", "sertraline", "paroxetine", "citalopram", "escitalopram", "fluvoxamine"],
        "snri": ["venlafaxine", "duloxetine", "desvenlafaxine"],
        "benzodiazepine": ["diazepam", "lorazepam", "alprazolam", "clonazepam", "chlordiazepoxide"],
        "antipsychotic": ["quetiapine", "olanzapine", "risperidone", "aripiprazole", "ziprasidone", "haloperidol", "clozapine"],
        
        # أدوية أخرى
        "allopurinol": ["allopurinol"],
        "methotrexate": ["methotrexate"],
        "warfarin": ["warfarin"],
        "heparin": ["heparin", "enoxaparin"],
    }
    
    # فحص كل حساسية مع الأدوية المدخلة
    for allergy in allergy_list:
        for drug in drug_names:
            drug_lower = drug.lower()
            print(f"🔍 Checking: allergy='{allergy}' vs drug='{drug_lower}'")
            
            # فحص المطابقة المباشرة
            if allergy in drug_lower:
                warnings.append(f"⚠️ {drug} contains '{allergy}' which you are allergic to. Avoid use.")
                print(f"   ✅ Direct match found!")
                continue
            
            # فحص القواعد
            for allergen, drug_list in allergy_rules.items():
                if allergy in allergen or allergen in allergy:
                    for rule_drug in drug_list:
                        if rule_drug in drug_lower or drug_lower in rule_drug:
                            warnings.append(f"⚠️ {drug} belongs to the {allergen.upper()} class. You have a documented allergy to {allergen}. Use with extreme caution or avoid.")
                            print(f"   ✅ Rule match: {allergy} -> {allergen} -> {rule_drug}")
                            break
    
    print(f"🔍 Total warnings found: {len(warnings)}")
    return warnings


def calculate_risk_percentage(interactions: List[Dict]) -> int:
    """
    Calculate numerical risk percentage based on interactions
    """
    if not interactions:
        return 0
    
    total_score = 0
    for interaction in interactions:
        severity = interaction["severity"].lower()
        if severity == "high":
            total_score += 85
        elif severity == "moderate":
            total_score += 55
        elif severity == "low":
            total_score += 25
    
    avg_score = total_score / len(interactions)
    return int(avg_score)


def analyze_drugs(db: Session, drug_names: List[str], user: Optional[models.User] = None) -> Dict[str, Any]:
    """
    Analyze drug interactions for a list of medications
    """
    
    # Get drug objects from database
    drugs = []
    for name in drug_names:
        drug = db.query(models.Drug).filter(models.Drug.name.ilike(name)).first()
        if drug:
            drugs.append(drug)
    
    # Find interactions between all pairs of drugs
    interactions = []
    lab_alerts = []
    
    for i in range(len(drugs)):
        for j in range(i + 1, len(drugs)):
            drug1 = drugs[i]
            drug2 = drugs[j]
            
            interaction = find_interaction(db, drug1.id, drug2.id)
            if interaction:
                interactions.append({
                    "drug1": drug1.name,
                    "drug2": drug2.name,
                    "severity": interaction.severity,
                    "description": interaction.description
                })
                
                for alert in interaction.lab_alerts:
                    lab_alerts.append({
                        "id": alert.id,
                        "alert_text": alert.alert_text
                    })
    
    # Determine overall risk level
    risk_level = determine_risk_level(interactions)
    
    # Calculate risk percentage
    risk_percentage = calculate_risk_percentage(interactions)
    
    # Generate recommendation
    recommendation = generate_recommendation(risk_level, interactions, user)
    
    # Add condition-based warnings if user is provided
    condition_warnings = []
    if user and user.conditions:
        condition_warnings = check_condition_warnings(drug_names, user.conditions)
    
    # Add allergy warnings if user is provided
    allergy_warnings = []
    if user and user.allergies:
        print(f"🔍 User allergies from DB: {user.allergies}")
        allergy_warnings = check_allergy_warnings(drug_names, user.allergies)
    else:
        print("🔍 No allergies found for user")
    
    return {
        "interactions": interactions,
        "risk_level": risk_level,
        "risk_percentage": risk_percentage,
        "recommendation": recommendation,
        "lab_alerts": lab_alerts,
        "condition_warnings": condition_warnings,
        "allergy_warnings": allergy_warnings
    }


def find_interaction(db: Session, drug1_id: int, drug2_id: int) -> Optional[models.Interaction]:
    """Find interaction between two drugs regardless of order"""
    
    interaction = db.query(models.Interaction).filter(
        models.Interaction.drug1_id == drug1_id,
        models.Interaction.drug2_id == drug2_id
    ).first()
    
    if not interaction:
        interaction = db.query(models.Interaction).filter(
            models.Interaction.drug1_id == drug2_id,
            models.Interaction.drug2_id == drug1_id
        ).first()
    
    return interaction


def determine_risk_level(interactions: List[Dict]) -> str:
    """Determine overall risk level based on interactions"""
    
    if not interactions:
        return "none"
    
    for interaction in interactions:
        if interaction["severity"].lower() == "high":
            return "high"
    
    for interaction in interactions:
        if interaction["severity"].lower() == "moderate":
            return "moderate"
    
    return "low"


def generate_recommendation(risk_level: str, interactions: List[Dict], user: Optional[models.User] = None) -> str:
    """Generate recommendation based on risk level"""
    
    if risk_level == "high":
        if interactions:
            drugs = f"{interactions[0]['drug1']} and {interactions[0]['drug2']}"
            return f"⚠️ HIGH RISK: Significant interaction detected between {drugs}. Immediate medical consultation required. Consider alternative medications."
        return "⚠️ HIGH RISK: Significant drug interactions detected. Please consult your healthcare provider immediately."
    
    elif risk_level == "moderate":
        return "⚠️ MODERATE RISK: Potential interactions detected. Monitor for adverse effects and consult your healthcare provider."
    
    elif risk_level == "low":
        return "ℹ️ LOW RISK: Minor interactions possible. Generally safe but monitor for any unusual symptoms."
    
    else:
        return "✓ No significant interactions detected. Always consult your healthcare provider about your medications."


def check_condition_warnings(drug_names: List[str], conditions: str) -> List[str]:
    """
    Check for warnings based on patient conditions
    """
    
    warnings = []
    condition_list = [c.strip().lower() for c in conditions.split(",") if c.strip()]
    
    condition_rules = {
        "diabetes": ["prednisone", "steroids"],
        "hypertension": ["pseudoephedrine", "nsaids"],
        "kidney disease": ["nsaids", "ibuprofen", "naproxen"],
        "liver disease": ["acetaminophen", "paracetamol"],
        "heart disease": ["nsaids", "ibuprofen"],
        "pregnancy": ["warfarin", "methotrexate", "accutane"],
        "asthma": ["aspirin", "nsaids", "beta-blockers"],
        "bleeding disorder": ["aspirin", "warfarin", "clopidogrel", "nsaids"],
    }
    
    for condition in condition_list:
        if condition in condition_rules:
            for drug in drug_names:
                if drug.lower() in condition_rules[condition]:
                    warnings.append(f"⚠️ {drug} may be problematic for patients with {condition}. Monitor closely.")
    
    return warnings


def analyze_with_user_profile(db: Session, user: models.User) -> Dict[str, Any]:
    """
    Analyze all medications in user profile
    """
    
    if not user.medications:
        return {
            "interactions": [],
            "risk_level": "none",
            "risk_percentage": 0,
            "recommendation": "No medications in your profile. Add medications to check for interactions.",
            "lab_alerts": [],
            "condition_warnings": [],
            "allergy_warnings": []
        }
    
    drug_names = [d.strip() for d in user.medications.split(",") if d.strip()]
    
    return analyze_drugs(db, drug_names, user)