"""
PharmaLogic – FastAPI entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
import os
import sys

from database import engine, SessionLocal
import models
from routers import auth, users, drugs, analysis


# ── Lifespan (startup / shutdown) ─────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all tables
    print("🔄 Creating database tables...")
    models.Base.metadata.create_all(bind=engine)
    # Seed sample data
    seed_data()
    print("✅ Server started successfully!")
    yield
    print("🛑 Server shutting down...")


def seed_data():
    """Insert sample drugs and interactions if the DB is empty."""
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(models.Drug).count() > 0:
            print("📊 Database already has data, skipping seed...")
            return

        print("🌱 Seeding database with expanded sample data...")

        # --- Drugs (موسعة) ---
        drug_data = [
            # الأدوية الأساسية (مضافة مسبقاً)
            ("Aspirin", "Common pain reliever and blood thinner (NSAID)."),
            ("Warfarin", "Anticoagulant (blood thinner) used to prevent clots."),
            ("Ibuprofen", "NSAID used for pain, fever, and inflammation."),
            ("Methotrexate", "Immunosuppressant used for cancer and autoimmune diseases."),
            ("Acetaminophen", "Analgesic and antipyretic (Tylenol)."),
            ("Lisinopril", "ACE inhibitor used to treat high blood pressure."),
            ("Potassium", "Essential mineral supplement."),
            ("Metformin", "Oral diabetes medicine that controls blood sugar."),
            ("Simvastatin", "Statin used to lower cholesterol."),
            ("Amiodarone", "Antiarrhythmic medication for heart rhythm problems."),
            ("Clopidogrel", "Antiplatelet agent used to prevent blood clots."),
            ("Fluoxetine", "SSRI antidepressant (Prozac)."),
            ("Tramadol", "Opioid pain medication."),
            ("Digoxin", "Cardiac glycoside for heart failure and arrhythmia."),
            ("Ciprofloxacin", "Broad-spectrum antibiotic (fluoroquinolone)."),
            
            # أدوية جديدة - القلب والضغط
            ("Amlodipine", "Calcium channel blocker for high blood pressure and chest pain."),
            ("Atorvastatin", "Statin used to lower cholesterol and prevent cardiovascular disease."),
            ("Losartan", "Angiotensin II receptor blocker for high blood pressure."),
            ("Carvedilol", "Beta-blocker for heart failure and high blood pressure."),
            ("Furosemide", "Loop diuretic for fluid retention and high blood pressure."),
            
            # أدوية جديدة - السكري
            ("Glipizide", "Sulfonylurea for type 2 diabetes."),
            ("Sitagliptin", "DPP-4 inhibitor for type 2 diabetes."),
            ("Insulin", "Hormone for diabetes management."),
            
            # أدوية جديدة - مضادات حيوية
            ("Amoxicillin", "Penicillin antibiotic for bacterial infections."),
            ("Azithromycin", "Macrolide antibiotic for bacterial infections."),
            ("Doxycycline", "Tetracycline antibiotic for bacterial infections."),
            
            # أدوية جديدة - مضادات التخثر
            ("Apixaban", "Direct factor Xa inhibitor anticoagulant."),
            ("Rivaroxaban", "Direct factor Xa inhibitor anticoagulant."),
            ("Enoxaparin", "Low molecular weight heparin anticoagulant."),
            
            # أدوية جديدة - أعصاب ونفسية
            ("Sertraline", "SSRI antidepressant (Zoloft)."),
            ("Venlafaxine", "SNRI antidepressant."),
            ("Diazepam", "Benzodiazepine for anxiety and seizures."),
            ("Gabapentin", "Anticonvulsant for neuropathic pain and seizures."),
            
            # أدوية جديدة - مسكنات
            ("Naproxen", "NSAID for pain and inflammation."),
            ("Celecoxib", "COX-2 inhibitor NSAID."),
            ("Morphine", "Opioid analgesic for severe pain."),
            
            # أدوية جديدة - معدة وجهاز هضمي
            ("Omeprazole", "Proton pump inhibitor for GERD and ulcers."),
            ("Metoclopramide", "Prokinetic agent for nausea and gastroparesis."),
            ("Loperamide", "Antidiarrheal agent."),
            
            # أدوية جديدة - تنفس
            ("Albuterol", "Beta-agonist bronchodilator for asthma."),
            ("Prednisone", "Corticosteroid for inflammation and immune conditions."),
            ("Montelukast", "Leukotriene receptor antagonist for asthma."),
        ]

        drugs: dict[str, models.Drug] = {}
        for name, desc in drug_data:
            d = models.Drug(name=name, description=desc)
            db.add(d)
            db.flush()
            drugs[name] = d

        # --- Interactions (موسعة) ---
        interactions_data = [
            # التفاعلات الأساسية
            ("Aspirin", "Warfarin", "high", "Concurrent use significantly increases bleeding risk. Avoid unless under close medical supervision."),
            ("Ibuprofen", "Methotrexate", "high", "NSAIDs can increase methotrexate toxicity and cause serious adverse effects. Use alternative pain relief."),
            ("Acetaminophen", "Warfarin", "moderate", "Regular use of acetaminophen may enhance anticoagulant effect. Monitor INR closely."),
            ("Lisinopril", "Potassium", "moderate", "ACE inhibitors raise potassium levels; combined with potassium supplements may cause hyperkalemia."),
            ("Simvastatin", "Amiodarone", "high", "Amiodarone inhibits simvastatin metabolism, increasing risk of myopathy and rhabdomyolysis."),
            ("Warfarin", "Ciprofloxacin", "high", "Ciprofloxacin inhibits warfarin metabolism, dramatically increasing anticoagulation and bleeding risk."),
            ("Clopidogrel", "Aspirin", "moderate", "Dual antiplatelet therapy increases bleeding risk. Often used intentionally—requires medical supervision."),
            ("Fluoxetine", "Tramadol", "high", "Combination risk of serotonin syndrome and decreased tramadol efficacy (CYP2D6 inhibition)."),
            ("Digoxin", "Amiodarone", "high", "Amiodarone raises digoxin levels significantly, increasing toxicity risk. Reduce digoxin dose by 50%."),
            ("Ibuprofen", "Lisinopril", "moderate", "NSAIDs can reduce antihypertensive effect of ACE inhibitors and impair renal function."),
            ("Metformin", "Ciprofloxacin", "low", "Fluoroquinolones may disturb blood glucose regulation when combined with antidiabetic agents."),
            ("Aspirin", "Ibuprofen", "low", "Ibuprofen may reduce aspirin's cardioprotective effect. Take aspirin at least 30 min before ibuprofen."),
            
            # تفاعلات جديدة - القلب والضغط
            ("Amlodipine", "Simvastatin", "moderate", "Amlodipine increases simvastatin levels, increasing risk of myopathy. Limit simvastatin dose to 20mg/day."),
            ("Losartan", "Potassium", "moderate", "ARBs can increase potassium levels. Monitor potassium when used with supplements or potassium-sparing diuretics."),
            ("Carvedilol", "Insulin", "moderate", "Beta-blockers may mask hypoglycemia symptoms and affect blood glucose control."),
            ("Furosemide", "Lisinopril", "moderate", "Combined use may cause excessive blood pressure reduction and renal impairment."),
            ("Atorvastatin", "Amiodarone", "high", "Amiodarone increases atorvastatin levels, increasing myopathy risk. Consider lower statin dose."),
            
            # تفاعلات جديدة - السكري
            ("Metformin", "Furosemide", "moderate", "Furosemide may increase metformin levels, risk of lactic acidosis."),
            ("Glipizide", "Ciprofloxacin", "moderate", "Fluoroquinolones may alter blood glucose; monitor closely."),
            ("Sitagliptin", "Insulin", "low", "Combination may increase hypoglycemia risk; monitor blood glucose."),
            
            # تفاعلات جديدة - مضادات حيوية
            ("Amoxicillin", "Warfarin", "moderate", "Antibiotics may alter gut flora and increase INR; monitor closely."),
            ("Azithromycin", "Warfarin", "moderate", "Macrolides may increase warfarin effect; monitor INR."),
            ("Doxycycline", "Warfarin", "low", "May slightly increase anticoagulant effect; monitor INR."),
            ("Ciprofloxacin", "Theophylline", "high", "Ciprofloxacin increases theophylline levels, risk of toxicity."),
            
            # تفاعلات جديدة - مضادات التخثر
            ("Apixaban", "Aspirin", "moderate", "Combined anticoagulant and antiplatelet therapy increases bleeding risk."),
            ("Rivaroxaban", "Clopidogrel", "moderate", "Increased bleeding risk with dual therapy."),
            ("Enoxaparin", "Aspirin", "moderate", "Increased bleeding risk; use with caution."),
            
            # تفاعلات جديدة - أعصاب ونفسية
            ("Sertraline", "Tramadol", "high", "Increased risk of serotonin syndrome."),
            ("Venlafaxine", "Tramadol", "high", "Increased risk of serotonin syndrome and seizures."),
            ("Diazepam", "Tramadol", "high", "Increased CNS depression, respiratory depression risk."),
            ("Gabapentin", "Morphine", "moderate", "Increased CNS depression and respiratory depression."),
            ("Fluoxetine", "Sertraline", "high", "Combined SSRIs increase serotonin syndrome risk."),
            
            # تفاعلات جديدة - مسكنات
            ("Naproxen", "Warfarin", "high", "NSAIDs increase bleeding risk with anticoagulants."),
            ("Celecoxib", "Warfarin", "moderate", "May increase bleeding risk; monitor INR."),
            ("Morphine", "Tramadol", "moderate", "Increased CNS depression; monitor for respiratory depression."),
            
            # تفاعلات جديدة - معدة وجهاز هضمي
            ("Omeprazole", "Metformin", "low", "PPIs may reduce B12 absorption; monitor B12 levels."),
            ("Metoclopramide", "Tramadol", "moderate", "Increased CNS depression risk."),
            
            # تفاعلات جديدة - تنفس
            ("Albuterol", "Carvedilol", "moderate", "Beta-agonists may reduce beta-blocker effectiveness."),
            ("Prednisone", "Metformin", "low", "Corticosteroids may increase blood glucose levels."),
        ]

        for drug1_name, drug2_name, severity, description in interactions_data:
            if drug1_name in drugs and drug2_name in drugs:
                interaction = models.Interaction(
                    drug1_id=drugs[drug1_name].id,
                    drug2_id=drugs[drug2_name].id,
                    severity=severity,
                    description=description
                )
                db.add(interaction)

        # --- Lab Alerts ---
        # Note: Lab alerts can be created after commits if needed
        lab_alerts_data = [
            (0, "Monitor PT/INR at least weekly when Aspirin + Warfarin are co-administered."),
            (1, "Check CBC and renal/hepatic function before and during Ibuprofen + Methotrexate therapy."),
            (2, "Monitor INR every 3–5 days when initiating or changing Acetaminophen dose with Warfarin."),
            (3, "Check serum potassium levels within 1–2 weeks of starting or adjusting Lisinopril with potassium."),
            (4, "Monitor CK (creatine kinase) levels if Simvastatin + Amiodarone are co-prescribed."),
            (5, "Perform INR check within 3–5 days of starting Ciprofloxacin in patients on Warfarin."),
            (7, "Monitor for serotonin syndrome symptoms: agitation, confusion, rapid heart rate, high blood pressure."),
            (8, "Measure serum digoxin level within 1 week of starting Amiodarone; target levels 0.5–0.9 ng/mL."),
        ]

        db.commit()
        print(f"✅ Seed data inserted successfully! Total drugs: {len(drug_data)}, Total interactions: {len(interactions_data)}")
    except Exception as e:
        db.rollback()
        print(f"⚠️ Seed error (non-fatal): {e}")
    finally:
        db.close()

# ── App ───────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="PharmaLogic API",
    description="Smart Drug Interaction Analysis",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware - يسمح للواجهة الأمامية بالتواصل مع الخادم
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # في الإنتاج، حدد النطاقات المسموحة فقط
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Static Files (Frontend) ───────────────────────────────────────────────────

# تحديد مسار مجلد frontend
# البحث في عدة مسارات محتملة
def find_frontend_path():
    """Find frontend folder in multiple possible locations"""
    # على Render والـ development environments المختلفة
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "..", "frontend"),  # backend/../frontend
        os.path.join(os.path.dirname(__file__), "frontend"),        # backend/frontend
        os.path.join(os.getcwd(), "frontend"),                      # current dir/frontend
        os.path.join(os.getcwd(), "..", "frontend"),                # parent dir/frontend
        "/opt/render/project/src/frontend",                         # Render specific path
    ]
    
    for path in possible_paths:
        try:
            if os.path.exists(path) and os.path.isdir(path):
                print(f"✅ Frontend folder found at: {path}")
                return path
        except Exception as e:
            print(f"⚠️ Error checking path {path}: {e}")
    
    return None

frontend_path = find_frontend_path()

if frontend_path:
    try:
        # تقديم الملفات الثابتة (CSS, JS, images)
        app.mount("/static", StaticFiles(directory=frontend_path), name="static")
        print("✅ Frontend static files configured")
        
        # تقديم الصفحة الرئيسية
        @app.get("/", response_class=HTMLResponse)
        async def serve_frontend():
            index_path = os.path.join(frontend_path, "index.html")
            if os.path.exists(index_path):
                with open(index_path, "r", encoding="utf-8") as f:
                    html_content = f.read()
                return html_content
            return HTMLResponse(
                content=f"""
                <html>
                    <head><title>PharmaLogic</title></head>
                    <body>
                        <h1>index.html not found</h1>
                        <p>Looking for: {index_path}</p>
                        <p>Please make sure index.html exists in the frontend folder.</p>
                    </body>
                </html>
                """, 
                status_code=404
            )
    except Exception as e:
        print(f"⚠️ Error mounting frontend: {e}")
        frontend_path = None

if not frontend_path:
    print("⚠️ Frontend folder not found!")
    print("   Looking in these paths:")
    for path in [
        os.path.join(os.path.dirname(__file__), "..", "frontend"),
        os.path.join(os.path.dirname(__file__), "frontend"),
        os.path.join(os.getcwd(), "frontend"),
        os.path.join(os.getcwd(), "..", "frontend"),
    ]:
        print(f"     - {path}")
    
    # نقطة نهاية بديلة إذا لم يتم العثور على frontend
    @app.get("/", response_class=HTMLResponse)
    async def root_info():
        return """
        <html>
            <head><title>PharmaLogic API</title></head>
            <body>
                <h1>PharmaLogic API is running! ✅</h1>
                <p>API Documentation: <a href="/docs">/docs</a></p>
                <p>Health Check: <a href="/health">/health</a></p>
                <p>Status: <a href="/api/status">/api/status</a></p>
                <p>⚠️ Frontend folder not found. Make sure to include it in your deployment.</p>
            </body>
        </html>
        """


# ── Mount Routers ────────────────────────────────────────────────────────────

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(drugs.router)
app.include_router(analysis.router)


# ── Additional Endpoints ─────────────────────────────────────────────────────

@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "ok", "frontend_available": frontend_path is not None}


@app.get("/api/status")
def api_status():
    """API status endpoint"""
    return {
        "status": "running",
        "message": "PharmaLogic API is operational",
        "version": "1.0.0",
        "frontend_available": frontend_path is not None
    }


@app.get("/api/info")
def api_info():
    """Get information about available endpoints"""
    return {
        "name": "PharmaLogic API",
        "endpoints": {
            "auth": {
                "register": "POST /auth/register",
                "login": "POST /auth/login"
            },
            "users": {
                "me": "GET /users/me",
                "update": "PUT /users/me"
            },
            "drugs": {
                "list": "GET /drugs",
                "create": "POST /drugs",
                "get": "GET /drugs/{id}"
            },
            "analysis": {
                "analyze": "POST /analyze",
                "analyze_me": "GET /analyze/me"
            },
            "docs": "GET /docs"
        }
    }