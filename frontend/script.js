renderGuestMedical()// ============================================================
//  PharmaLogic – Frontend (API-connected version)
//  Version: 4.0 - Added Vitamin Deficiency Warnings
// ============================================================

// Dynamically resolve API base
const API_BASE = 'https://pharmalogic-api.onrender.com';
// ── Global state ─────────────────────────────────────────────
let currentPage = 'home';
let currentUser = null;
let userRole    = null;
let lastInteractionResults = null;
let editingProfile = false;
let editFormData   = null;
let drugCache = null;

// ── Auth helpers ──────────────────────────────────────────────

function getToken()          { return localStorage.getItem('pharma_token'); }
function setToken(t)         { localStorage.setItem('pharma_token', t); }
function clearToken()        { localStorage.removeItem('pharma_token'); }

function authHeaders() {
    const token = getToken();
    return token
        ? { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` }
        : { 'Content-Type': 'application/json' };
}

async function apiFetch(path, options = {}) {
    let res;
    try {
        res = await fetch(`${API_BASE}${path}`, {
            headers: authHeaders(),
            ...options,
        });
    } catch (networkErr) {
        throw new Error(
            'Cannot reach the server. Make sure the backend is running:\n' +
            'cd backend  →  uvicorn main:app --reload'
        );
    }

    let data;
    try { data = await res.json(); } catch { data = null; }

    if (!res.ok) {
        const msg = data?.detail || `Request failed (${res.status})`;
        throw new Error(typeof msg === 'string' ? msg : JSON.stringify(msg));
    }
    return data;
}

// ── Professional error messages ──────────────────────────────

function getProfessionalErrorMessage(err) {
    const errorMessage = err.message || '';
    
    if (errorMessage.toLowerCase().includes('not found') || 
        errorMessage.toLowerCase().includes('drug')) {
        return `⚠️ The medication you entered is not registered in our database. 
                Please check the spelling or contact our support team to add this medication.
                You can also try using the generic name of the drug.`;
    }
    
    if (errorMessage.toLowerCase().includes('cannot reach') || 
        errorMessage.toLowerCase().includes('server')) {
        return `⚠️ Unable to connect to the server. Please check your internet connection and try again.`;
    }
    
    return `⚠️ ${errorMessage}`;
}

// ── Show non-blocking toast notification ─────────────────────

function showToast(msg, type = 'info') {
    const existing = document.getElementById('pharma-toast');
    if (existing) existing.remove();

    const colors = {
        success : '#16a34a',
        error   : '#dc2626',
        warning : '#d97706',
        info    : '#1B5E9D',
    };

    const toast = document.createElement('div');
    toast.id = 'pharma-toast';
    Object.assign(toast.style, {
        position   : 'fixed',
        bottom     : '1.5rem',
        right      : '1.5rem',
        background : colors[type] || colors.info,
        color      : 'white',
        padding    : '0.875rem 1.5rem',
        borderRadius: '0.75rem',
        boxShadow  : '0 4px 16px rgba(0,0,0,.2)',
        zIndex     : '9999',
        fontWeight : '600',
        fontSize   : '0.9rem',
        maxWidth   : '340px',
        transition : 'opacity .4s',
    });
    toast.textContent = msg;
    document.body.appendChild(toast);
    setTimeout(() => { toast.style.opacity = '0'; setTimeout(() => toast.remove(), 400); }, 3500);
}

// ── Navigation ────────────────────────────────────────────────

function navigateTo(page, anchor = null) {
    currentPage = page;
    if (page !== 'patient-dashboard') { editingProfile = false; }
    closeMenu();
    renderPage();
    window.scrollTo(0, 0);
    if (anchor) {
        setTimeout(() => {
            const el = document.getElementById(anchor);
            if (el) el.scrollIntoView({ behavior: 'smooth' });
        }, 100);
    }
}

function toggleMenu() { document.getElementById('mobileMenu').classList.toggle('active'); }
function closeMenu()  { document.getElementById('mobileMenu').classList.remove('active'); }

// ── Page router ───────────────────────────────────────────────

function renderPage() {
    const content = document.getElementById('page-content');
    switch (currentPage) {
        case 'home':              content.innerHTML = renderHome();             break;
        case 'login':             content.innerHTML = renderLogin();            break;
        case 'signup':            content.innerHTML = renderSignup();           break;
        case 'patient-dashboard': content.innerHTML = renderPatientDashboard(); break;
        case 'medical-dashboard': content.innerHTML = renderMedicalDashboard(); break;
        case 'guest-medical':     
            content.innerHTML = renderGuestMedical(); 
            setTimeout(() => initAutocompleteForGuest(), 100);
            break;
        case 'about':             content.innerHTML = renderAbout();            break;
        default:                  content.innerHTML = renderHome();
    }
    updateNavbar();
}

// ── Updated Navbar with conditional buttons ───────────────────

function updateNavbar() {
    const navBtns = document.querySelector('.nav-buttons');
    const mobileMenu = document.getElementById('mobileMenu');
    if (!navBtns) return;

    const isHomePage = currentPage === 'home';

    if (currentUser) {
        navBtns.innerHTML = `
            <span style="color:#2d2d47;font-weight:500;font-size:0.9rem;">Hi, ${currentUser.name?.split(' ')[0] || 'User'}</span>
            <a class="btn btn-secondary" onclick="navigateTo('patient-dashboard')" style="cursor:pointer;padding:0.4rem 1.2rem;background:#1B5E9D;color:white;border-radius:0.5rem;font-weight:500;">Dashboard</a>
            <a class="btn btn-secondary" onclick="handleLogout()" style="cursor:pointer;padding:0.4rem 1.2rem;background:#f3f4f6;border-radius:0.5rem;font-weight:500;">Sign Out</a>
        `;
        if (mobileMenu && mobileMenu.querySelector('div')) {
            mobileMenu.querySelector('div').innerHTML = `
                <a href="#" onclick="navigateTo('home'); return false;">Home</a>
                <a href="#" onclick="navigateTo('about'); return false;">About</a>
                <a href="#" onclick="navigateTo('guest-medical'); return false;">Medical Team (Guest)</a>
                <a href="#" onclick="navigateTo('patient-dashboard'); return false;">Dashboard</a>
                <a href="#" onclick="handleLogout(); return false;">Sign Out</a>
            `;
        }
    } else {
        if (isHomePage) {
            navBtns.innerHTML = ``;
            if (mobileMenu && mobileMenu.querySelector('div')) {
                mobileMenu.querySelector('div').innerHTML = `
                    <a href="#" onclick="navigateTo('home'); return false;">Home</a>
                    <a href="#" onclick="navigateTo('about'); return false;">About</a>
                    <a href="#" onclick="navigateTo('guest-medical'); return false;">Medical Team (Guest)</a>
                `;
            }
        } else {
            navBtns.innerHTML = `
                <a class="signin" onclick="navigateTo('login')" style="cursor:pointer;padding:0.5rem 1rem;color:#1B5E9D;font-weight:500;">Sign In</a>
                <a class="signup" onclick="navigateTo('signup')" style="cursor:pointer;padding:0.5rem 1.25rem;background:#FF8C00;color:white;border-radius:0.5rem;font-weight:500;">Get Started</a>
            `;
            if (mobileMenu && mobileMenu.querySelector('div')) {
                mobileMenu.querySelector('div').innerHTML = `
                    <a href="#" onclick="navigateTo('home'); return false;">Home</a>
                    <a href="#" onclick="navigateTo('about'); return false;">About</a>
                    <a href="#" onclick="navigateTo('guest-medical'); return false;">Medical Team (Guest)</a>
                    <a href="#" onclick="navigateTo('login'); return false;">Sign In</a>
                    <a href="#" onclick="navigateTo('signup'); return false;">Get Started</a>
                `;
            }
        }
    }
}

// ── Logout ────────────────────────────────────────────────────

function handleLogout() {
    clearToken();
    currentUser = null;
    userRole    = null;
    showToast('Signed out successfully.', 'info');
    navigateTo('home');
}

// ── Auto-login from stored token ──────────────────────────────

async function tryAutoLogin() {
    const token = getToken();
    if (!token) return;
    try {
        const user = await apiFetch('/users/me');
        currentUser = user;
        userRole    = user.role;
        console.log("✅ Auto-login successful, user allergies:", user.allergies);
    } catch {
        clearToken();
    }
}

// ── Autocomplete Functions ────────────────────────────────────

async function getDrugList() {
    if (drugCache) return drugCache;
    
    try {
        const drugs = await apiFetch('/drugs');
        drugCache = drugs.map(d => d.name);
        return drugCache;
    } catch (err) {
        console.error('Failed to fetch drugs:', err);
        return [];
    }
}

function createAutocompleteInput(inputId, placeholder) {
    return `
        <div class="autocomplete-container" style="position:relative;width:100%;">
            <input type="text" id="${inputId}" placeholder="${placeholder}" autocomplete="off">
            <div id="${inputId}-suggestions" class="autocomplete-suggestions" style="display:none;position:absolute;top:100%;left:0;right:0;background:white;border:1px solid #e5e7eb;border-radius:.5rem;max-height:200px;overflow-y:auto;z-index:1000;box-shadow:0 4px 6px rgba(0,0,0,0.1);"></div>
        </div>
    `;
}

function setupAutocomplete(inputId, drugList) {
    const input = document.getElementById(inputId);
    const suggestionsDiv = document.getElementById(`${inputId}-suggestions`);
    if (!input || !suggestionsDiv) return;

    const showSuggestions = (filter) => {
        const filtered = drugList.filter(d => 
            d.toLowerCase().includes(filter.toLowerCase())
        ).slice(0, 8);

        if (filtered.length > 0 && filter.length >= 2) {
            suggestionsDiv.innerHTML = filtered.map(d => 
                `<div style="padding:.75rem;cursor:pointer;border-bottom:1px solid #f3f4f6;transition:background 0.2s;" 
                      onmouseover="this.style.backgroundColor='#f3f4f6'" 
                      onmouseout="this.style.backgroundColor='white'"
                      onclick="document.getElementById('${inputId}').value='${d.replace(/'/g, "\\'")}'; document.getElementById('${inputId}-suggestions').style.display='none';">
                    ${d}
                </div>`
            ).join('');
            suggestionsDiv.style.display = 'block';
        } else {
            suggestionsDiv.style.display = 'none';
        }
    };

    input.addEventListener('input', (e) => {
        const value = e.target.value.trim();
        if (value.length >= 2) {
            showSuggestions(value);
        } else {
            suggestionsDiv.style.display = 'none';
        }
    });

    input.addEventListener('blur', () => {
        setTimeout(() => {
            suggestionsDiv.style.display = 'none';
        }, 200);
    });
}

async function initAutocompleteForGuest() {
    const drugs = await getDrugList();
    setupAutocomplete('guestDrug1', drugs);
    setupAutocomplete('guestDrug2', drugs);
}

// ============================================================
//  HOME PAGE
// ============================================================

function renderHome() {
    return `
        <div class="page-container">
            <div class="hero">
                <div class="hero-content">
                    <div class="badge"><span>Smart Drug Interaction Analysis</span></div>
                    <h1>Safer Prescriptions, <span class="highlight">Smarter Care</span></h1>
                    <p>PharmaLogic uses intelligent analysis to detect potential drug interactions instantly, helping healthcare professionals and patients make informed medication decisions.</p>
                    <div class="hero-buttons">
                        <button class="btn btn-primary" onclick="navigateTo('signup')">Get Started →</button>
                        <button class="btn btn-secondary" onclick="navigateTo('login')">Sign In</button>
                    </div>
                </div>
                <div class="hero-visual">
                    <div class="hero-card">
                        <div>
                            <div class="hero-icon icon-green">✓</div>
                            <div>
                                <h3>Safe Interaction Check</h3>
                                <p>Instant analysis of drug combinations</p>
                            </div>
                        </div>
                        <div>
                            <div class="hero-icon icon-amber">!</div>
                            <div>
                                <h3>Risk Assessment</h3>
                                <p>Clear risk levels and explanations</p>
                            </div>
                        </div>
                        <div>
                            <div class="hero-icon icon-blue">📄</div>
                            <div>
                                <h3>PDF Reports</h3>
                                <p>Export data for healthcare professionals</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <section class="user-types">
                <div class="user-types-container">
                    <div class="section-header">
                        <h2>Built for Every Role</h2>
                        <p>Tailored interfaces for patients and healthcare professionals</p>
                    </div>
                    <div class="user-grid">
                        <div class="user-card patient">
                            <div class="user-card-icon">👤</div>
                            <h3>For Patients</h3>
                            <p>Manage your medications and check for potential interactions with your current prescriptions.</p>
                            <ul class="user-features">
                                <li><span class="checkmark">✓</span> Personal medication history</li>
                                <li><span class="checkmark">✓</span> Real-time interaction checking</li>
                                <li><span class="checkmark">✓</span> PDF export functionality</li>
                            </ul>
                        </div>
                        <div class="user-card doctor">
                            <div class="user-card-icon">⚕️</div>
                            <h3>For Medical Professionals</h3>
                            <p>Fast and reliable medical analysis to search for drug interactions and enhance clinical decisions.</p>
                            <ul class="user-features">
                                <li><span class="checkmark">✓</span> Fast interaction search</li>
                                <li><span class="checkmark">✓</span> Reliable medical analysis</li>
                                <li><span class="checkmark">✓</span> Enhanced clinical knowledge</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </section>

            <section class="features" id="features">
                <div class="features-container">
                    <div class="section-header">
                        <h2>Powerful Features</h2>
                        <p>Everything you need for safe medication management</p>
                    </div>
                    <div class="features-grid">
                        <div class="feature-item">
                            <div class="feature-icon blue">⚡</div>
                            <div><h3>Instant Analysis</h3><p>Real-time interaction checks powered by your database</p></div>
                        </div>
                        <div class="feature-item">
                            <div class="feature-icon teal">🔒</div>
                            <div><h3>Secure & Private</h3><p>JWT-secured with strict role-based access controls</p></div>
                        </div>
                        <div class="feature-item">
                            <div class="feature-icon blue">📊</div>
                            <div><h3>Reliable Medical Analysis</h3><p>Comprehensive rules engine with lab alert system</p></div>
                        </div>
                        <div class="feature-item">
                            <div class="feature-icon teal">📋</div>
                            <div><h3>Report Export</h3><p>Download and share comprehensive PDF reports</p></div>
                        </div>
                    </div>
                </div>
            </section>

            <section class="cta">
                <div class="cta-container">
                    <h2>Ready to Get Started?</h2>
                    <p>Join patients and healthcare professionals who trust PharmaLogic for safer prescriptions</p>
                    <button class="btn btn-primary" onclick="navigateTo('signup')" style="background:white;color:#2B8EFF;">Create Your Account →</button>
                </div>
            </section>
        </div>
    `;
}

// ============================================================
//  LOGIN PAGE
// ============================================================

function renderLogin() {
    return `
        <div class="page-container">
            <div class="form-container">
                <h1>Welcome Back</h1>
                <p>Sign in to your PharmaLogic account to continue</p>

                <form id="loginForm" onsubmit="handleLogin(event)">
                    <div class="form-group">
                        <label for="loginEmail">Email Address</label>
                        <input type="email" id="loginEmail" placeholder="you@example.com" required>
                    </div>
                    <div class="form-group">
                        <label for="loginPassword">Password</label>
                        <input type="password" id="loginPassword" placeholder="••••••••" required>
                    </div>

                    <div id="loginError" style="display:none;color:#dc2626;background:#fef2f2;padding:.75rem;border-radius:.5rem;margin-bottom:1rem;font-size:.9rem;"></div>

                    <button type="submit" class="form-button" id="loginBtn">Sign In</button>
                </form>

                <div class="signup-link">
                    Don't have an account? <a onclick="navigateTo('signup'); return false;">Create one now</a>
                </div>
                <button class="back-button" onclick="navigateTo('home')" style="margin-top:1rem;">← Back to Home</button>
            </div>
        </div>
    `;
}

async function handleLogin(event) {
    event.preventDefault();
    const email    = document.getElementById('loginEmail').value.trim();
    const password = document.getElementById('loginPassword').value;
    const errDiv   = document.getElementById('loginError');
    const btn      = document.getElementById('loginBtn');

    errDiv.style.display = 'none';
    btn.disabled  = true;
    btn.textContent = 'Signing in…';

    try {
        const data = await apiFetch('/auth/login', {
            method : 'POST',
            body   : JSON.stringify({ email, password }),
        });
        setToken(data.access_token);

        const user = await apiFetch('/users/me');
        currentUser = user;
        userRole    = user.role;
        console.log("✅ Logged in, user allergies:", user.allergies);

        showToast('Signed in successfully!', 'success');
        navigateTo(user.role === 'patient' ? 'patient-dashboard' : 'medical-dashboard');
    } catch (err) {
        errDiv.textContent  = getProfessionalErrorMessage(err);
        errDiv.style.display = 'block';
        btn.disabled  = false;
        btn.textContent = 'Sign In';
    }
}

// ============================================================
//  SIGNUP PAGE (Modified: removed doctor/pharmacist roles)
// ============================================================

function renderSignup() {
    return `
        <div class="page-container">
            <div class="form-container">
                <h1>Create Account</h1>
                <p>Join PharmaLogic to check drug interactions safely</p>

                <form id="signupForm" onsubmit="handleSignup(event)">
                    <input type="hidden" id="selectedRole" value="patient">

                    <div class="form-group">
                        <label for="fullName">Full Name</label>
                        <input type="text" id="fullName" placeholder="John Doe" required>
                    </div>
                    <div class="form-group">
                        <label for="signupEmail">Email Address</label>
                        <input type="email" id="signupEmail" placeholder="you@example.com" required>
                    </div>
                    <div class="form-group">
                        <label for="signupPassword">Password</label>
                        <input type="password" id="signupPassword" placeholder="••••••••" required minlength="6">
                    </div>
                    <div class="form-group">
                        <label for="confirmPassword">Confirm Password</label>
                        <input type="password" id="confirmPassword" placeholder="••••••••" required>
                    </div>

                    <div id="patientFields">
                        <div class="form-group">
                            <label for="age">Age</label>
                            <input type="number" id="age" placeholder="30" min="1" max="130">
                        </div>
                        <div class="form-group">
                            <label for="gender">Gender</label>
                            <select id="gender">
                                <option value="">Select gender</option>
                                <option value="male">Male</option>
                                <option value="female">Female</option>
                                <option value="other">Other</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="medicalConditions">Chronic Conditions (comma-separated)</label>
                            <input type="text" id="medicalConditions" placeholder="e.g., Diabetes, Hypertension">
                        </div>
                        <div class="form-group">
                            <label for="allergies">Allergies (comma-separated)</label>
                            <input type="text" id="allergies" placeholder="e.g., Penicillin, Aspirin">
                        </div>
                        <div class="form-group">
                            <label for="currentMedications">Current Medications (comma-separated)</label>
                            <input type="text" id="currentMedications" placeholder="e.g., Aspirin, Metformin">
                        </div>
                    </div>

                    <div class="checkbox-group">
                        <input type="checkbox" id="termsAgree" required>
                        <label for="termsAgree">I agree to the <a href="#" onclick="showTermsOfService(); return false;">Terms of Service</a> and <a href="#" onclick="showPrivacyPolicy(); return false;">Privacy Policy</a></label>
                    </div>

                    <div id="signupError" style="display:none;color:#dc2626;background:#fef2f2;padding:.75rem;border-radius:.5rem;margin-bottom:1rem;font-size:.9rem;"></div>

                    <button type="submit" class="form-button" id="signupBtn">Create Account</button>
                </form>

                <div class="signup-link">
                    Already have an account? <a onclick="navigateTo('login'); return false;">Sign in here</a>
                </div>
                <button class="back-button" onclick="navigateTo('home')" style="margin-top:1rem;">← Back to Home</button>
            </div>
        </div>
    `;
}

async function handleSignup(event) {
    event.preventDefault();
    const errDiv = document.getElementById('signupError');
    const btn    = document.getElementById('signupBtn');
    errDiv.style.display = 'none';

    const role            = 'patient';
    const name            = document.getElementById('fullName').value.trim();
    const email           = document.getElementById('signupEmail').value.trim();
    const password        = document.getElementById('signupPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    if (password !== confirmPassword) {
        errDiv.textContent  = '⚠️ Passwords do not match';
        errDiv.style.display = 'block';
        return;
    }
    if (password.length < 6) {
        errDiv.textContent  = '⚠️ Password must be at least 6 characters';
        errDiv.style.display = 'block';
        return;
    }

    const payload = { name, email, password, role };

    payload.age        = parseInt(document.getElementById('age').value) || null;
    payload.gender     = document.getElementById('gender').value || null;
    payload.conditions = document.getElementById('medicalConditions').value.trim() || null;
    payload.allergies  = document.getElementById('allergies').value.trim() || null;
    payload.medications= document.getElementById('currentMedications').value.trim() || null;

    btn.disabled    = true;
    btn.textContent = 'Creating account…';

    try {
        const data = await apiFetch('/auth/register', {
            method : 'POST',
            body   : JSON.stringify(payload),
        });
        setToken(data.access_token);

        const user = await apiFetch('/users/me');
        currentUser = user;
        userRole    = user.role;
        console.log("✅ Account created, user allergies:", user.allergies);

        showToast('Account created successfully!', 'success');
        navigateTo('patient-dashboard');
    } catch (err) {
        errDiv.textContent  = getProfessionalErrorMessage(err);
        errDiv.style.display = 'block';
        btn.disabled    = false;
        btn.textContent = 'Create Account';
    }
}

// ============================================================
//  PATIENT DASHBOARD (Modified: Removed profile box)
// ============================================================

function renderPatientDashboard() {
    if (!currentUser) {
        return `<div class="page-container"><p>Please <a onclick="navigateTo('login')">sign in</a> to view your dashboard.</p></div>`;
    }
    return `
        <div class="page-container">
            <div class="dashboard-header">
                <h1>Welcome, ${currentUser.name || 'Patient'}</h1>
                <p>Manage your medications and check for interactions</p>
            </div>

            <!-- Profile Summary Box with Edit Button -->
            <div style="max-width:1280px;margin:2rem auto;background:linear-gradient(135deg,rgba(255,140,0,.1) 0%,rgba(27,94,157,.1) 100%);border-radius:1rem;padding:2rem;box-shadow:0 2px 8px rgba(0,0,0,.1);border:2px solid #FFE4CC;">
                ${editingProfile ? renderEditProfileForm() : renderViewProfileSummary()}
            </div>

            <div class="dashboard-grid">
                <div class="card" onclick="showPatientFeature('medications')" style="background:linear-gradient(135deg,rgba(255,140,0,.15) 0%,rgba(255,220,180,.1) 100%);border:2px solid #FFD580;cursor:pointer;">
                    <div class="card-icon" style="background:#FF8C00;">💊</div>
                    <h3>My Medications</h3>
                    <p>View and manage your current medications</p>
                </div>
                <div class="card" onclick="showPatientFeature('medical-state')" style="background:linear-gradient(135deg,rgba(27,94,157,.15) 0%,rgba(173,216,230,.1) 100%);border:2px solid #87CEEB;cursor:pointer;">
                    <div class="card-icon" style="background:#1B5E9D;">🏥</div>
                    <h3>Medical State</h3>
                    <p>View your health status and medicine effects</p>
                </div>
                <div class="card" onclick="showPatientFeature('interactions')" style="background:linear-gradient(135deg,rgba(27,94,157,.15) 0%,rgba(173,216,230,.1) 100%);border:2px solid #87CEEB;cursor:pointer;">
                    <div class="card-icon" style="background:#1B5E9D;">🔍</div>
                    <h3>Check Interactions</h3>
                    <p>Verify interactions with your medications</p>
                </div>
            </div>

            <div id="patientFeatureContent"></div>
        </div>
    `;
}

// Helper function to get vitamin warnings for medications
function getVitaminWarningsForMeds(meds) {
    const vitaminRules = {
        "Metformin": { deficiency: "Vitamin B12", recommendation: "Check Vitamin B12 levels annually" },
        "Omeprazole": { deficiency: "Vitamin B12, Magnesium", recommendation: "Monitor Vitamin B12 and Magnesium levels" },
        "Pantoprazole": { deficiency: "Vitamin B12, Magnesium", recommendation: "Monitor Vitamin B12 and Magnesium levels" },
        "Esomeprazole": { deficiency: "Vitamin B12, Magnesium", recommendation: "Monitor Vitamin B12 and Magnesium levels" },
        "Lansoprazole": { deficiency: "Vitamin B12, Magnesium", recommendation: "Monitor Vitamin B12 and Magnesium levels" },
        "Methotrexate": { deficiency: "Folate (Vitamin B9)", recommendation: "Supplement with Folic acid and monitor levels" },
        "Phenytoin": { deficiency: "Vitamin D, Calcium, Folate", recommendation: "Monitor Vitamin D, Calcium, and Folate levels" },
        "Carbamazepine": { deficiency: "Vitamin D, Calcium, Folate", recommendation: "Monitor Vitamin D, Calcium, and Folate levels" },
        "Valproate": { deficiency: "Carnitine, Folate", recommendation: "Monitor Carnitine and Folate levels" },
        "Hydrochlorothiazide": { deficiency: "Potassium, Magnesium, Sodium", recommendation: "Monitor electrolytes (Potassium, Magnesium, Sodium)" },
        "Furosemide": { deficiency: "Potassium, Magnesium, Sodium, Calcium", recommendation: "Monitor electrolytes (Potassium, Magnesium, Sodium, Calcium)" },
        "Colchicine": { deficiency: "Vitamin B12", recommendation: "Monitor Vitamin B12 levels with long-term use" }
    };
    
    const warnings = [];
    for (const med of meds) {
        if (vitaminRules[med]) {
            warnings.push({
                drug: med,
                deficiency: vitaminRules[med].deficiency,
                recommendation: vitaminRules[med].recommendation
            });
        }
    }
    return warnings;
}

function showPatientFeature(feature) {
    const content = document.getElementById('patientFeatureContent');
    const meds    = parseMeds(currentUser?.medications);

    if (feature === 'medications') {
        // Get vitamin warnings for current medications
        const vitaminWarnings = getVitaminWarningsForMeds(meds);
        
        let medsHTML = '';
        for (const med of meds) {
            const warning = vitaminWarnings.find(w => w.drug.toLowerCase() === med.toLowerCase());
            medsHTML += `
                <li style="padding:.75rem;background:#FFE4CC;margin-bottom:.5rem;border-radius:.5rem;border-left:4px solid #FF8C00;color:#1B5E9D;font-weight:500;">
                    <div>💊 ${med}</div>
                    ${warning ? `
                        <div style="margin-top:.5rem;padding:.5rem;background:#fff3e0;border-radius:.5rem;font-size:.875rem;font-weight:normal;">
                            <div style="color:#d97706;">🧪 Vitamin Deficiency Warning:</div>
                            <div>Long-term use may cause ${warning.deficiency} deficiency</div>
                            <div style="color:#1B5E9D;margin-top:.25rem;">→ ${warning.recommendation}</div>
                        </div>
                    ` : ''}
                </li>
            `;
        }
        
        const medHTML = meds.length
            ? `<ul style="list-style:none;padding:0;margin:1rem 0;">${medsHTML}</ul>`
            : '<p style="color:#4b5563;font-style:italic;padding:1rem;background:#f9fafb;border-radius:.5rem;">No medications added yet</p>';

        content.innerHTML = `
            <div class="interaction-checker" style="border:2px solid #FFE4CC;">
                <h2 style="color:#FF8C00;">My Current Medications</h2>
                <p style="color:#4b5563;margin-bottom:1.5rem;">Your active medications and prescriptions</p>
                <div style="background:white;padding:1.5rem;border-radius:.75rem;margin-bottom:1.5rem;">${medHTML}</div>
                <button class="back-button" onclick="document.getElementById('patientFeatureContent').innerHTML=''" style="background:#FF8C00;">← Back</button>
            </div>
        `;

    } else if (feature === 'medical-state') {
        content.innerHTML = `
            <div class="interaction-checker" style="border:2px solid #87CEEB;">
                <h2 style="color:#1B5E9D;">Your Medical State</h2>
                <p style="color:#4b5563;margin-bottom:1.5rem;">Health status and medication effects</p>
                <div style="background:white;padding:1.5rem;border-radius:.75rem;margin-bottom:1.5rem;">
                    <div style="display:grid;gap:1rem;">
                        ${infoCard('Chronic Conditions', currentUser?.conditions || 'None reported', '#1B5E9D', '#1B5E9D')}
                        ${infoCard('Allergies',           currentUser?.allergies  || 'None reported', '#FF8C00', '#FF8C00')}
                        ${infoCard('Current Medications',`${meds.length} medication(s)`,            '#00d9b7', '#00d9b7')}
                    </div>
                </div>
                <button class="back-button" onclick="document.getElementById('patientFeatureContent').innerHTML=''" style="background:#1B5E9D;">← Back</button>
            </div>
        `;

    } else if (feature === 'interactions') {
        content.innerHTML = `
            <div class="interaction-checker" style="border:2px solid #1B5E9D;">
                <h2 style="color:#1B5E9D;">Check Drug Interactions</h2>
                <p style="color:#4b5563;margin-bottom:1.5rem;">Enter a new medication to check against your current medications via the live database</p>
                ${meds.length ? `
                    <div style="background:#E0FFFF;padding:1rem;border-radius:.75rem;margin-bottom:1.5rem;border-left:4px solid #1B5E9D;">
                        <p style="font-size:.875rem;color:#1B5E9D;font-weight:600;margin-bottom:.5rem;">Your Current Medications:</p>
                        <div style="display:flex;flex-wrap:wrap;gap:.5rem;">
                            ${meds.map(m => `<span style="background:#1B5E9D;color:white;padding:.25rem .75rem;border-radius:.25rem;font-size:.875rem;font-weight:500;">${m}</span>`).join('')}
                        </div>
                    </div>` : '<p style="color:#4b5563;font-style:italic;margin-bottom:1.5rem;">No current medications in your profile.</p>'}
                <div class="checker-form">
                    ${createAutocompleteInput('newDrug', 'Enter new medication')}
                    <button onclick="checkNewDrugInteractions()" style="background:#1B5E9D;">Check Interactions</button>
                </div>
                <div id="newDrugResults"></div>
                <button class="back-button" onclick="document.getElementById('patientFeatureContent').innerHTML=''" style="background:#1B5E9D;margin-top:1rem;">← Back</button>
            </div>
        `;
        setTimeout(async () => {
            const drugs = await getDrugList();
            setupAutocomplete('newDrug', drugs);
        }, 100);
    }
}

async function checkNewDrugInteractions() {
    const newDrug = document.getElementById('newDrug').value.trim();
    const meds    = parseMeds(currentUser?.medications);
    const results = document.getElementById('newDrugResults');

    if (!newDrug) { showToast('Please enter a medication', 'warning'); return; }

    const btn = document.querySelector('#patientFeatureContent .checker-form button');
    btn.disabled = true;
    btn.textContent = 'Analyzing…';
    results.innerHTML = '<p style="color:#4b5563;margin-top:1rem;">⏳ Checking database…</p>';

    const allDrugs = meds.length ? [...meds, newDrug] : [newDrug];

    try {
        const data = await apiFetch('/analyze', {
            method : 'POST',
            body   : JSON.stringify({ drugs: allDrugs }),
        });

        console.log("🔍 API Response Data:", data);
        console.log("🔍 Vitamin warnings from API:", data.vitamin_warnings);

        lastInteractionResults = { patient: currentUser, newDrug, apiResult: data, timestamp: new Date().toLocaleString() };
        results.innerHTML = renderAnalysisResult(data, newDrug);
        addExportButton(results);
    } catch (err) {
        results.innerHTML = `<div class="results severe" style="margin-top:1.5rem;"><h3>⚠️ Error</h3><p>${getProfessionalErrorMessage(err)}</p></div>`;
    } finally {
        btn.disabled    = false;
        btn.textContent = 'Check Interactions';
    }
}

// ============================================================
//  GUEST MEDICAL PAGE (with autocomplete)
// ============================================================

function renderGuestMedical() {
    return `
        <div class="page-container">
            <div class="dashboard-header">
                <h1>Medical Team Access</h1>
                <p>Professional tools for healthcare providers</p>
            </div>

            <!-- Tab Navigation -->
            <div style="max-width:1280px;margin:0 auto 2rem auto;display:flex;gap:0.5rem;border-bottom:2px solid #e5e7eb;">
                <button id="tabInteractionsBtn" onclick="switchMedicalTab('interactions')" style="padding:0.75rem 1.5rem;background:#1B5E9D;color:white;border:none;border-radius:0.5rem 0.5rem 0 0;font-weight:600;cursor:pointer;">💊 Drug Interaction Analyzer</button>
                <button id="tabInfoBtn" onclick="switchMedicalTab('info')" style="padding:0.75rem 1.5rem;background:#f3f4f6;color:#4b5563;border:none;border-radius:0.5rem 0.5rem 0 0;font-weight:600;cursor:pointer;">📋 Drug Information Viewer</button>
            </div>

            <!-- Tab 1: Drug Interaction Analyzer -->
            <div id="interactionsTab" style="display:block;">
                <div style="max-width:800px;margin:0 auto;background:white;border-radius:1rem;padding:2rem;box-shadow:0 2px 8px rgba(0,0,0,.1);border:1px solid #e5e7eb;text-align:center;margin-bottom:2rem;">
                    <p style="color:#4b5563;font-size:1.125rem;margin-bottom:1rem;">Welcome to PharmaLogic Medical Team Access</p>
                    <p style="color:#4b5563;">Use our drug interaction checker to analyze medications for your patients. No registration required.</p>
                </div>

                <div class="interaction-checker">
                    <h2>Drug Interaction Analyzer</h2>
                    <p>Check for potential drug interactions</p>

                    <div id="medCountSelector" style="margin-bottom:2rem;padding:1.5rem;background:#f9fafb;border-radius:.75rem;">
                        <p style="font-weight:600;margin-bottom:1rem;color:#2d2d47;">How many medications?</p>
                        <div style="display:flex;gap:2rem;justify-content:center;flex-wrap:wrap;">
                            <label style="display:flex;align-items:center;gap:.5rem;cursor:pointer;">
                                <input type="radio" name="medCount" value="2" checked onchange="showMedInputs()"> 2 medications
                            </label>
                            <label style="display:flex;align-items:center;gap:.5rem;cursor:pointer;">
                                <input type="radio" name="medCount" value="more" onchange="showMedInputs()"> More than 2
                            </label>
                        </div>
                    </div>

                    <div id="twoMedInputs">
                        <div class="checker-form">
                            ${createAutocompleteInput('guestDrug1', 'First medication')}
                            ${createAutocompleteInput('guestDrug2', 'Second medication')}
                            <button id="guestAnalyzeBtn" onclick="checkGuestInteractions()" style="background:#1B5E9D;">Analyze</button>
                        </div>
                    </div>

                    <div id="multiMedInputs" style="display:none;">
                        <p style="margin-bottom:.75rem;color:#4b5563;">Enter all medications separated by commas:</p>
                        <textarea id="guestDrugsList" rows="4" style="width:100%;padding:.75rem;border:2px solid #e5e7eb;border-radius:.5rem;margin-bottom:1rem;" placeholder="e.g., Aspirin, Metformin, Lisinopril"></textarea>
                        <button id="guestMultiBtn" onclick="checkGuestMultiInteractions()" style="padding:.75rem 2rem;background:#1B5E9D;color:white;border:none;border-radius:.5rem;font-weight:600;cursor:pointer;">Analyze All</button>
                    </div>

                    <div id="guestResults"></div>
                </div>
            </div>

            <!-- Tab 2: Drug Information Viewer -->
            <div id="infoTab" style="display:none;">
                <div class="interaction-checker">
                    <h2>📋 Drug Information Viewer</h2>
                    <p>Search for a medication to view comprehensive clinical information</p>

                    <div class="checker-form">
                        ${createAutocompleteInput('infoDrugName', 'Enter medication name (e.g., Metformin, Aspirin)')}
                        <button id="infoSearchBtn" onclick="searchDrugInformation()" style="background:#1B5E9D;">Search</button>
                    </div>

                    <div id="drugInfoResults" style="margin-top:2rem;"></div>
                </div>
            </div>
        </div>
    `;
}


let currentMedicalTab = 'interactions';

function switchMedicalTab(tab) {
    currentMedicalTab = tab;
    
    const interactionsTab = document.getElementById('interactionsTab');
    const infoTab = document.getElementById('infoTab');
    const tabInteractionsBtn = document.getElementById('tabInteractionsBtn');
    const tabInfoBtn = document.getElementById('tabInfoBtn');
    
    if (tab === 'interactions') {
        interactionsTab.style.display = 'block';
        infoTab.style.display = 'none';
        tabInteractionsBtn.style.background = '#1B5E9D';
        tabInteractionsBtn.style.color = 'white';
        tabInfoBtn.style.background = '#f3f4f6';
        tabInfoBtn.style.color = '#4b5563';
    } else {
        interactionsTab.style.display = 'none';
        infoTab.style.display = 'block';
        tabInteractionsBtn.style.background = '#f3f4f6';
        tabInteractionsBtn.style.color = '#4b5563';
        tabInfoBtn.style.background = '#1B5E9D';
        tabInfoBtn.style.color = 'white';
        
        // Initialize autocomplete for the info tab
        setTimeout(async () => {
            const drugs = await getDrugList();
            setupAutocomplete('infoDrugName', drugs);
        }, 100);
    }
}


async function searchDrugInformation() {
    const drugName = document.getElementById('infoDrugName').value.trim();
    const resultsDiv = document.getElementById('drugInfoResults');
    
    if (!drugName) {
        showToast('Please enter a medication name', 'warning');
        return;
    }
    
    resultsDiv.innerHTML = '<p style="text-align:center;color:#4b5563;">⏳ Loading drug information...</p>';
    
    try {
        // First, search for the drug in the database
        const drugs = await apiFetch('/drugs');
        const foundDrug = drugs.find(d => d.name.toLowerCase() === drugName.toLowerCase());
        
        if (!foundDrug) {
            resultsDiv.innerHTML = `
                <div style="background:#fef2f2;border:2px solid #dc2626;border-radius:.75rem;padding:1.5rem;text-align:center;">
                    <h3 style="color:#dc2626;">⚠️ Drug Not Found</h3>
                    <p style="color:#4b5563;">"${drugName}" is not in our database. Please check the spelling or try another medication.</p>
                    <p style="font-size:.875rem;color:#6b7280;margin-top:1rem;">Available drugs: Aspirin, Metformin, Warfarin, Lisinopril, Omeprazole, Amoxicillin, and more.</p>
                </div>
            `;
            return;
        }
        
        // Get detailed information
        const detailedInfo = await apiFetch(`/drugs/${foundDrug.id}/detailed`);
        
        resultsDiv.innerHTML = renderDrugInformation(detailedInfo);
        
    } catch (err) {
        resultsDiv.innerHTML = `
            <div style="background:#fee2e2;border:2px solid #dc2626;border-radius:.75rem;padding:1.5rem;text-align:center;">
                <h3 style="color:#dc2626;">⚠️ Error Loading Information</h3>
                <p style="color:#4b5563;">${getProfessionalErrorMessage(err)}</p>
            </div>
        `;
    }
}


function renderDrugInformation(drug) {
    return `
        <div style="background:white;border-radius:1rem;box-shadow:0 4px 12px rgba(0,0,0,0.1);overflow:hidden;">
            <!-- Header -->
            <div style="background:linear-gradient(135deg,#1B5E9D,#FF8C00);padding:1.5rem;color:white;">
                <h2 style="margin:0;font-size:1.75rem;">💊 ${drug.name}</h2>
                <p style="margin:.5rem 0 0;opacity:0.9;">${drug.description || 'No description available'}</p>
            </div>
            
            <div style="padding:1.5rem;">
                <!-- Common Uses -->
                <div style="margin-bottom:1.5rem;padding:1rem;background:#f0fdf4;border-radius:.75rem;border-left:4px solid #16a34a;">
                    <h3 style="color:#16a34a;margin:0 0 .5rem 0;">💊 Common Uses</h3>
                    <ul style="margin:0;padding-left:1.25rem;">
                        ${drug.common_uses.map(use => `<li style="margin-bottom:.25rem;">${use}</li>`).join('')}
                    </ul>
                </div>
                
                <!-- Side Effects -->
                <div style="margin-bottom:1.5rem;padding:1rem;background:#fffbeb;border-radius:.75rem;border-left:4px solid #d97706;">
                    <h3 style="color:#d97706;margin:0 0 .5rem 0;">⚠️ Common Side Effects</h3>
                    <ul style="margin:0;padding-left:1.25rem;">
                        ${drug.side_effects.map(effect => `<li style="margin-bottom:.25rem;">${effect}</li>`).join('')}
                    </ul>
                </div>
                
                <!-- Contraindications -->
                <div style="margin-bottom:1.5rem;padding:1rem;background:#fef2f2;border-radius:.75rem;border-left:4px solid #dc2626;">
                    <h3 style="color:#dc2626;margin:0 0 .5rem 0;">🚫 Contraindications</h3>
                    <ul style="margin:0;padding-left:1.25rem;">
                        ${drug.contraindications.map(ci => `<li style="margin-bottom:.25rem;">${ci}</li>`).join('')}
                    </ul>
                </div>
                
                <!-- Drug Interactions -->
                ${drug.interactions && drug.interactions.length > 0 ? `
                <div style="margin-bottom:1.5rem;padding:1rem;background:#eff6ff;border-radius:.75rem;border-left:4px solid #3b82f6;">
                    <h3 style="color:#3b82f6;margin:0 0 .5rem 0;">💊 Drug Interactions</h3>
                    <ul style="margin:0;padding-left:1.25rem;">
                        ${drug.interactions.map(interaction => `
                            <li style="margin-bottom:.5rem;">
                                <strong>${interaction.drug}</strong> (${interaction.severity} severity)<br>
                                <span style="font-size:.875rem;color:#4b5563;">${interaction.description}</span>
                            </li>
                        `).join('')}
                    </ul>
                </div>
                ` : ''}
                
                <!-- Vitamin Depletions -->
                ${drug.vitamin_depletions && drug.vitamin_depletions.length > 0 ? `
                <div style="margin-bottom:1.5rem;padding:1rem;background:#f3e8ff;border-radius:.75rem;border-left:4px solid #9333ea;">
                    <h3 style="color:#9333ea;margin:0 0 .5rem 0;">🧪 Vitamin/Nutrient Depletions</h3>
                    <ul style="margin:0;padding-left:1.25rem;">
                        ${drug.vitamin_depletions.map(vd => `<li style="margin-bottom:.25rem;">${vd}</li>`).join('')}
                    </ul>
                </div>
                ` : ''}
                
                <!-- Pregnancy & Lactation -->
                <div style="margin-bottom:1.5rem;padding:1rem;background:#fef3c7;border-radius:.75rem;border-left:4px solid #f59e0b;">
                    <h3 style="color:#f59e0b;margin:0 0 .5rem 0;">📋 Pregnancy & Lactation</h3>
                    <p style="margin:0;">${drug.pregnancy_safety}</p>
                </div>
                
                <!-- Counseling Points -->
                <div style="margin-bottom:1.5rem;padding:1rem;background:#f0fdf4;border-radius:.75rem;border-left:4px solid #10b981;">
                    <h3 style="color:#10b981;margin:0 0 .5rem 0;">💡 Key Counseling Points</h3>
                    <ul style="margin:0;padding-left:1.25rem;">
                        ${drug.counseling_points.map(point => `<li style="margin-bottom:.25rem;">${point}</li>`).join('')}
                    </ul>
                </div>
                
                <!-- References -->
                <div style="padding:1rem;background:#f3f4f6;border-radius:.75rem;">
                    <h3 style="color:#4b5563;margin:0 0 .5rem 0;">🔗 References</h3>
                    <ul style="margin:0;padding-left:1.25rem;">
                        ${drug.references.map(ref => `<li style="margin-bottom:.25rem;font-size:.875rem;">${ref}</li>`).join('')}
                    </ul>
                    <p style="font-size:.75rem;color:#9ca3af;margin-top:1rem;">⚠️ For professional reference only. Not a substitute for clinical judgment.</p>
                </div>
            </div>
        </div>
    `;
}

function showMedInputs() {
    const selected = document.querySelector('input[name="medCount"]:checked').value;
    document.getElementById('twoMedInputs').style.display   = selected === '2'    ? 'block' : 'none';
    document.getElementById('multiMedInputs').style.display = selected === 'more' ? 'block' : 'none';
    document.getElementById('guestResults').innerHTML = '';
}

async function checkGuestInteractions() {
    const d1  = document.getElementById('guestDrug1').value.trim();
    const d2  = document.getElementById('guestDrug2').value.trim();
    const btn = document.getElementById('guestAnalyzeBtn');
    if (!d1 || !d2) { showToast('Please enter both medications', 'warning'); return; }

    btn.disabled = true;
    btn.textContent = 'Analyzing…';
    await runGuestAnalysis([d1, d2]);
    btn.disabled    = false;
    btn.textContent = 'Analyze';
}

async function checkGuestMultiInteractions() {
    const val = document.getElementById('guestDrugsList').value;
    const btn = document.getElementById('guestMultiBtn');
    const drugs = val.split(',').map(d => d.trim()).filter(d => d);
    if (drugs.length < 2) { showToast('Please enter at least two medications', 'warning'); return; }

    btn.disabled    = true;
    btn.textContent = 'Analyzing…';
    await runGuestAnalysis(drugs);
    btn.disabled    = false;
    btn.textContent = 'Analyze All';
}

async function runGuestAnalysis(drugs) {
    const div = document.getElementById('guestResults');
    div.innerHTML = '<p style="color:#4b5563;margin-top:1rem;">⏳ Querying database…</p>';
    try {
        const data = await apiFetch('/analyze', {
            method : 'POST',
            body   : JSON.stringify({ drugs }),
        });
        div.innerHTML = renderAnalysisResult(data);
    } catch (err) {
        div.innerHTML = `
            <div class="results severe" style="margin-top:1.5rem;">
                <h3>⚠️ Unable to Complete Analysis</h3>
                <p>${getProfessionalErrorMessage(err)}</p>
                <p style="font-size:.875rem;margin-top:.5rem;">Need help? Contact our support team at support@pharmalogic.com</p>
            </div>
        `;
    }
}

// ============================================================
//  MEDICAL PROFESSIONAL DASHBOARD
// ============================================================

function renderMedicalDashboard() {
    if (!currentUser) {
        return `<div class="page-container"><p>Please <a onclick="navigateTo('login')">sign in</a>.</p></div>`;
    }
    const roleCap = cap(currentUser.role || 'Medical Professional');
    return `
        <div class="page-container">
            <div class="dashboard-header">
                <h1>Welcome, ${currentUser.name || roleCap}</h1>
                <p>Drug Interaction Analysis · Role: <strong>${roleCap}</strong></p>
            </div>

            <div class="interaction-checker">
                <h2>Drug Interaction Checker</h2>
                <p>Enter medications to analyze potential interactions via the live database</p>
                <div class="checker-form">
                    ${createAutocompleteInput('medDrug1', 'First medication')}
                    ${createAutocompleteInput('medDrug2', 'Second medication')}
                    <button id="medAnalyzeBtn" onclick="checkMedicalInteractions()">Analyze</button>
                </div>
                <p style="margin:.5rem 0;color:#4b5563;font-size:.875rem;text-align:center;">— or check multiple drugs at once —</p>
                <div style="display:flex;gap:.5rem;margin-top:.5rem;">
                    <input type="text" id="medMultiDrugs" placeholder="Aspirin, Warfarin, Lisinopril…" style="flex:1;padding:.75rem;border:2px solid #e5e7eb;border-radius:.5rem;">
                    <button onclick="checkMedicalMulti()" style="padding:.75rem 1.5rem;background:#1B5E9D;color:white;border:none;border-radius:.5rem;font-weight:600;cursor:pointer;">Analyze All</button>
                </div>
                <div id="medicalResults" style="margin-top:1.5rem;"></div>
            </div>

            ${(currentUser.role === 'doctor' || currentUser.role === 'pharmacist') ? renderAddDrugPanel() : ''}
        </div>
    `;
}

function renderAddDrugPanel() {
    return `
        <div class="interaction-checker" style="margin-top:2rem;border:2px solid #FFD580;">
            <h2 style="color:#FF8C00;">Add New Drug to Database</h2>
            <p style="color:#4b5563;margin-bottom:1.5rem;">As a ${cap(currentUser.role)}, you can add drugs to the system.</p>
            <div class="form-group">
                <label for="newDrugName">Drug Name</label>
                ${createAutocompleteInput('newDrugName', 'Enter drug name')}
            </div>
            <div class="form-group">
                <label for="newDrugDesc">Description</label>
                <input type="text" id="newDrugDesc" placeholder="Brief description of the drug" style="padding:.75rem;border:2px solid #e5e7eb;border-radius:.5rem;width:100%;">
            </div>
            <div id="addDrugMsg"></div>
            <button onclick="handleAddDrug()" style="padding:.75rem 2rem;background:#FF8C00;color:white;border:none;border-radius:.5rem;font-weight:600;cursor:pointer;margin-top:1rem;" id="addDrugBtn">Add Drug</button>
        </div>
    `;
}

async function handleAddDrug() {
    const name = document.getElementById('newDrugName').value.trim();
    const desc = document.getElementById('newDrugDesc').value.trim();
    const msg  = document.getElementById('addDrugMsg');
    const btn  = document.getElementById('addDrugBtn');

    if (!name) { showToast('Please enter a drug name', 'warning'); return; }

    btn.disabled    = true;
    btn.textContent = 'Adding…';
    msg.innerHTML   = '';

    try {
        const drug = await apiFetch('/drugs', {
            method : 'POST',
            body   : JSON.stringify({ name, description: desc }),
        });
        msg.innerHTML = `<p style="color:#16a34a;font-weight:600;margin-top:.75rem;">✓ Drug "${drug.name}" added to database!</p>`;
        document.getElementById('newDrugName').value = '';
        document.getElementById('newDrugDesc').value = '';
        drugCache = null;
    } catch (err) {
        msg.innerHTML = `<p style="color:#dc2626;font-weight:600;margin-top:.75rem;">⚠️ ${getProfessionalErrorMessage(err)}</p>`;
    } finally {
        btn.disabled    = false;
        btn.textContent = 'Add Drug';
    }
}

async function checkMedicalInteractions() {
    const d1  = document.getElementById('medDrug1').value.trim();
    const d2  = document.getElementById('medDrug2').value.trim();
    const btn = document.getElementById('medAnalyzeBtn');
    if (!d1 || !d2) { showToast('Please enter both medications', 'warning'); return; }

    btn.disabled    = true;
    btn.textContent = 'Analyzing…';
    await runMedAnalysis([d1, d2]);
    btn.disabled    = false;
    btn.textContent = 'Analyze';
}

async function checkMedicalMulti() {
    const val   = document.getElementById('medMultiDrugs').value;
    const drugs = val.split(',').map(d => d.trim()).filter(d => d);
    if (drugs.length < 2) { showToast('Enter at least 2 medications', 'warning'); return; }
    await runMedAnalysis(drugs);
}

async function runMedAnalysis(drugs) {
    const div = document.getElementById('medicalResults');
    div.innerHTML = '<p style="color:#4b5563;">⏳ Querying database…</p>';
    try {
        const data = await apiFetch('/analyze', {
            method : 'POST',
            body   : JSON.stringify({ drugs }),
        });
        div.innerHTML = renderAnalysisResult(data);
    } catch (err) {
        div.innerHTML = `
            <div class="results severe">
                <h3>⚠️ Error</h3>
                <p>${getProfessionalErrorMessage(err)}</p>
            </div>
        `;
    }
}

// ============================================================
//  SHARED ANALYSIS RESULT RENDERER (with allergy + vitamin warnings)
// ============================================================

function renderAnalysisResult(data, highlightDrug = null) {
    console.log("🚨 renderAnalysisResult called with data:", data);
    console.log("🚨 allergy_warnings value:", data.allergy_warnings);
    console.log("🚨 vitamin_warnings value:", data.vitamin_warnings);
    
    // التأكد من وجود risk_percentage
    let risk_percentage = data.risk_percentage;
    if (risk_percentage === undefined || risk_percentage === null) {
        const riskLevel = data.risk_level;
        if (riskLevel === 'high') risk_percentage = 85;
        else if (riskLevel === 'moderate') risk_percentage = 55;
        else if (riskLevel === 'low') risk_percentage = 25;
        else risk_percentage = 0;
    }
    
    const { interactions, risk_level, recommendation, lab_alerts } = data;
    
    const riskColors = {
        high     : { bg:'#fef2f2', border:'#dc2626', icon:'🚨', label:'High Risk' },
        moderate : { bg:'#fffbeb', border:'#d97706', icon:'⚠️', label:'Moderate Risk' },
        low      : { bg:'#f0fdf4', border:'#16a34a', icon:'ℹ️', label:'Low Risk' },
        none     : { bg:'#f0fdf4', border:'#16a34a', icon:'✓',  label:'No Interactions Found' },
    };
    const rc = riskColors[risk_level] || riskColors.none;

    let html = `
        <div style="margin-top:1.5rem;">
            <!-- Risk banner with percentage -->
            <div style="padding:1.25rem;background:${rc.bg};border:2px solid ${rc.border};border-radius:.75rem;margin-bottom:1.5rem;">
                <div style="display:flex;align-items:center;gap:1rem;flex-wrap:wrap;">
                    <span style="font-size:2rem;">${rc.icon}</span>
                    <div style="flex:1;">
                        <p style="font-size:1.1rem;font-weight:700;color:#1B5E9D;margin-bottom:.25rem;">${rc.label}</p>
                        <p style="color:#4b5563;margin:0;">${recommendation}</p>
                    </div>
                    ${risk_level !== 'none' && risk_percentage > 0 ? `
                    <div style="text-align:center;min-width:100px;">
                        <div style="font-size:2rem;font-weight:800;color:${rc.border};">${risk_percentage}%</div>
                        <div style="font-size:.75rem;color:#4b5563;">Risk Level</div>
                    </div>
                    ` : ''}
                </div>
                ${risk_level !== 'none' && risk_percentage > 0 ? `
                <div style="margin-top:1rem;background:white;border-radius:.5rem;height:8px;overflow:hidden;">
                    <div style="width:${risk_percentage}%;height:100%;background:${rc.border};transition:width 0.5s ease;"></div>
                </div>
                ` : ''}
            </div>
    `;
    
    // ========== عرض تحذيرات الحساسية ==========
    if (data.allergy_warnings && data.allergy_warnings.length > 0) {
        html += `
            <div style="background:#fee2e2;border:2px solid #dc2626;border-radius:.75rem;padding:1.25rem;margin-bottom:1.5rem;">
                <h3 style="color:#dc2626;margin-bottom:0.75rem;">🚨 Allergy Warnings (${data.allergy_warnings.length})</h3>
                <ul style="list-style:none;padding:0;">
                    ${data.allergy_warnings.map(w => `<li style="padding:.5rem 0;border-bottom:1px solid #fecaca;color:#991b1b;">⚠️ ${w}</li>`).join('')}
                </ul>
                <p style="font-size:.875rem;color:#991b1b;margin-top:.75rem;">Please consult your healthcare provider before taking these medications.</p>
            </div>
        `;
    }
    
    // ========== عرض تحذيرات نقص الفيتامينات ==========
    if (data.vitamin_warnings && data.vitamin_warnings.length > 0) {
        html += `
            <div style="background:#eff6ff;border:2px solid #3b82f6;border-radius:.75rem;padding:1.25rem;margin-bottom:1.5rem;">
                <h3 style="color:#1d4ed8;margin-bottom:0.75rem;">🧪 Vitamin/Nutrient Deficiency Warnings (${data.vitamin_warnings.length})</h3>
                <ul style="list-style:none;padding:0;">
                    ${data.vitamin_warnings.map(w => `
                        <li style="padding:.5rem 0;border-bottom:1px solid #bfdbfe;color:#1e40af;">
                            <strong>⚠️ ${w.drug}</strong>: Long-term use may cause ${w.deficiency} deficiency<br>
                            <span style="font-size:.875rem;">→ Recommendation: ${w.recommendation}</span>
                        </li>
                    `).join('')}
                </ul>
            </div>
        `;
    }
    
    // ========== عرض التفاعلات ==========
    if (interactions.length > 0) {
        html += `
            <h3 style="color:#1B5E9D;margin-bottom:1rem;">Interactions Detected (${interactions.length})</h3>
            <ul style="list-style:none;padding:0;margin-bottom:1.5rem;">
        `;
        interactions.forEach(i => {
            const sev = i.severity === 'high' ? '#dc2626' : i.severity === 'moderate' ? '#d97706' : '#16a34a';
            html += `
                <li style="margin-bottom:.75rem;padding:1rem;background:white;border-radius:.5rem;border-left:4px solid ${sev};box-shadow:0 1px 4px rgba(0,0,0,.07);">
                    <p style="font-weight:700;color:#1B5E9D;margin-bottom:.5rem;">💊 ${i.drug1} + ${i.drug2}</p>
                    <p style="margin:.25rem 0;color:#374151;">${i.description}</p>
                    <span style="display:inline-block;padding:.2rem .75rem;border-radius:999px;background:${sev};color:white;font-size:.8rem;font-weight:600;text-transform:capitalize;">
                        ${i.severity} severity
                    </span>
                </li>
            `;
        });
        html += `</ul>`;
    } else {
        html += `<p style="color:#4b5563;font-style:italic;margin-bottom:1.5rem;">No interactions found in the database for the entered medications.</p>`;
    }
    
    // ========== عرض تحذيرات المختبر ==========
    if (lab_alerts && lab_alerts.length > 0) {
        html += `
            <div style="background:#eff6ff;border:2px solid #3b82f6;border-radius:.75rem;padding:1.25rem;margin-bottom:1.5rem;">
                <h3 style="color:#1d4ed8;margin-bottom:1rem;">🧪 Lab Monitoring Alerts (${lab_alerts.length})</h3>
                <ul style="list-style:none;padding:0;">
                    ${lab_alerts.map(a => `<li style="padding:.5rem 0;border-bottom:1px solid #bfdbfe;color:#1e40af;">• ${a.alert_text}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    html += `</div>`;
    return html;
}

function addExportButton(container) {
    const old = document.getElementById('exportPDFBtn');
    if (old) old.remove();
    const btn       = document.createElement('button');
    btn.id          = 'exportPDFBtn';
    btn.textContent = '📄 Export PDF Report';
    btn.className   = 'back-button';
    btn.style.marginTop = '1rem';
    btn.onclick     = exportToPDF;
    container.appendChild(btn);
}

// ============================================================
//  PDF EXPORT
// ============================================================

function exportToPDF() {
    if (!lastInteractionResults) { showToast('No interaction results to export', 'warning'); return; }
    const { patient, newDrug, apiResult, timestamp } = lastInteractionResults;
    const { interactions, risk_level, risk_percentage, recommendation, lab_alerts, allergy_warnings, vitamin_warnings } = apiResult;
    const meds = parseMeds(patient?.medications);

    const pdfContent = `<!DOCTYPE html><html><head><meta charset="UTF-8">
<title>PharmaLogic Interaction Report</title>
<style>
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;max-width:800px;margin:0 auto;padding:2rem;color:#2d2d47;}
.header{text-align:center;border-bottom:2px solid #1B5E9D;padding-bottom:1rem;margin-bottom:2rem;}
.logo{font-size:1.5rem;font-weight:700;color:#1B5E9D;}
.section{margin-bottom:2rem;padding:1.5rem;background:#f9fafb;border-radius:.75rem;border-left:4px solid #FF8C00;}
.section h3{color:#1B5E9D;margin-top:0;}
.tag{display:inline-block;background:#FFE4CC;color:#1B5E9D;padding:.25rem .75rem;border-radius:.25rem;margin:.2rem;font-size:.875rem;font-weight:500;}
.risk-badge{display:inline-block;padding:.5rem 1rem;border-radius:.5rem;font-weight:700;margin-top:.5rem;}
.risk-high{background:#fef2f2;color:#dc2626;border:1px solid #dc2626;}
.risk-moderate{background:#fffbeb;color:#d97706;border:1px solid #d97706;}
.risk-low{background:#f0fdf4;color:#16a34a;border:1px solid #16a34a;}
.allergy-box{background:#fee2e2;border:2px solid #dc2626;border-radius:.5rem;padding:1rem;margin-top:1rem;}
.alert-box{background:#eff6ff;border:2px solid #3b82f6;border-radius:.5rem;padding:1rem;margin-top:1rem;}
.footer{margin-top:3rem;padding-top:1rem;border-top:1px solid #e5e7eb;text-align:center;color:#6b7280;font-size:.875rem;}
@media print{.no-print{display:none;}}
</style></head><body>
<div class="header"><div class="logo">PharmaLogic</div><h1>Drug Interaction Report</h1><p>${timestamp}</p></div>
<div class="section"><h3>Patient Information</h3>
  <p><strong>Name:</strong> ${patient.name || '—'}</p>
  <p><strong>Age:</strong> ${patient.age || '—'}</p>
  <p><strong>Gender:</strong> ${patient.gender ? cap(patient.gender) : '—'}</p>
  <p><strong>Conditions:</strong> ${patient.conditions || 'None'}</p>
  <p><strong>Allergies:</strong> ${patient.allergies || 'None'}</p>
  <p><strong>Current Medications:</strong></p>
  <div>${meds.length ? meds.map(m => `<span class="tag">${m}</span>`).join('') : '<em>None</em>'}</div>
</div>
<div class="section"><h3>New Medication Analyzed</h3>
  <span class="tag" style="background:#1B5E9D;color:white;">${newDrug}</span>
</div>
${allergy_warnings && allergy_warnings.length > 0 ? `
<div class="allergy-box"><h3 style="color:#dc2626;">🚨 Allergy Warnings</h3>
  <ul>${allergy_warnings.map(w => `<li>⚠️ ${w}</li>`).join('')}</ul>
</div>` : ''}
${vitamin_warnings && vitamin_warnings.length > 0 ? `
<div class="alert-box" style="background:#eff6ff;border:2px solid #3b82f6;">
  <h3 style="color:#1d4ed8;">🧪 Vitamin/Nutrient Deficiency Warnings</h3>
  <ul>${vitamin_warnings.map(w => `<li><strong>${w.drug}</strong>: Long-term use may cause ${w.deficiency} deficiency<br>→ ${w.recommendation}</li>`).join('')}</ul>
</div>` : ''}
<div class="section"><h3>Risk Assessment</h3>
  <p><strong>Overall Risk:</strong> ${cap(risk_level)}</p>
  <p><strong>Risk Percentage:</strong> ${risk_percentage}%</p>
  <div class="risk-badge risk-${risk_level}">Risk Level: ${cap(risk_level)} (${risk_percentage}%)</div>
  <p style="margin-top:1rem;"><strong>Recommendation:</strong> ${recommendation}</p>
</div>
<div class="section"><h3>Interaction Results (${interactions.length})</h3>
  ${interactions.length === 0
    ? '<p style="color:#16a34a;">✓ No known interactions found.</p>'
    : interactions.map(i => `
        <div style="margin-bottom:1rem;padding:1rem;border-left:4px solid ${i.severity==='high'?'#dc2626':i.severity==='moderate'?'#d97706':'#16a34a'};background:white;border-radius:.5rem;">
          <p><strong>${i.drug1} + ${i.drug2}</strong> — <em>${i.severity} severity</em></p>
          <p>${i.description}</p>
        </div>`).join('')}
</div>
${lab_alerts && lab_alerts.length ? `
<div class="alert-box"><h3 style="color:#1d4ed8;">🧪 Lab Monitoring Alerts</h3>
  <ul>${lab_alerts.map(a => `<li>${a.alert_text}</li>`).join('')}</ul>
</div>` : ''}
<div class="footer">
  <p>For informational purposes only. Always consult your healthcare provider.</p>
  <p>© ${new Date().getFullYear()} PharmaLogic. All rights reserved.</p>
  <button class="no-print" onclick="window.print()" style="margin-top:1rem;padding:.5rem 1rem;background:#1B5E9D;color:white;border:none;border-radius:.5rem;cursor:pointer;">Print Report</button>
</div>
</body></html>`;

    const win = window.open('', '_blank');
    win.document.write(pdfContent);
    win.document.close();
    win.focus();
    setTimeout(() => win.print(), 250);
}

// ============================================================
//  ABOUT PAGE
// ============================================================

function renderAbout() {
    return `
        <div class="page-container">
            <div class="about-container">
                <h1>About PharmaLogic</h1>
                <p>Making medication safety intelligent for everyone</p>
                <div class="content-card">
                    <h2>Our Mission</h2>
                    <p>At PharmaLogic, we believe that medication safety should be intelligent, accessible, and reliable. Our mission is to empower patients, doctors, and pharmacists with cutting-edge drug interaction analysis technology that helps prevent adverse drug events.</p>
                </div>
                <div class="mission-grid">
                    <div class="mission-item">
                        <h3>What We Do</h3>
                        <p>We provide a comprehensive drug interaction checking system backed by a real database, a robust rules engine, and lab-alert monitoring — all accessible via a secured REST API.</p>
                    </div>
                    <div class="mission-item secondary">
                        <h3>Why It Matters</h3>
                        <p>Drug interactions are a leading cause of preventable adverse events. Our intelligent system reduces medication errors and provides peace of mind to healthcare providers and patients alike.</p>
                    </div>
                </div>
                <div class="content-card">
                    <h2>Our Technology</h2>
                    <p>PharmaLogic is built with FastAPI + SQLite on the backend and a fully connected vanilla JS frontend. Authentication is secured with JWT tokens, and all interaction data is stored and queried from a real relational database.</p>
                </div>
                <button class="back-button" onclick="navigateTo('home')">← Back to Home</button>
            </div>
        </div>
    `;
}

// ============================================================
//  LEGAL PAGES
// ============================================================

function showPrivacyPolicy() {
    const content = document.getElementById('page-content');
    content.innerHTML = getPrivacyPolicyHTML();
    updateNavbar();
    window.scrollTo(0, 0);
}

function showTermsOfService() {
    const content = document.getElementById('page-content');
    content.innerHTML = getTermsOfServiceHTML();
    updateNavbar();
    window.scrollTo(0, 0);
}

function getPrivacyPolicyHTML() {
    return `
        <div class="page-container">
            <div class="legal-container" style="max-width:900px;margin:0 auto;padding:2rem;background:white;border-radius:1rem;box-shadow:0 2px 8px rgba(0,0,0,0.1);">
                <h1 style="color:#1B5E9D;margin-bottom:1rem;font-size:2rem;">Privacy Policy</h1>
                <p>At PharmaLogic, we take your privacy seriously. This Privacy Policy explains how we collect, use, disclose, and safeguard your information.</p>
                <h2 style="color:#FF8C00;margin-top:2rem;">1. Information We Collect</h2>
                <p>We collect personal information including name, email, age, gender, medical conditions, allergies, and current medications.</p>
                <h2 style="color:#FF8C00;margin-top:2rem;">2. How We Use Your Information</h2>
                <p>We use your information to provide drug interaction analysis, improve our services, and maintain your account security.</p>
                <h2 style="color:#FF8C00;margin-top:2rem;">3. Data Security</h2>
                <p>All data is encrypted using SSL/TLS. Passwords are hashed and never stored in plain text.</p>
                <h2 style="color:#FF8C00;margin-top:2rem;">4. Contact Us</h2>
                <p>Email: privacy@pharmalogic.com</p>
                <div style="color:#9ca3af;margin-top:2rem;padding-top:1rem;border-top:1px solid #e5e7eb;">Last Updated: April 2, 2026</div>
                <button class="back-button" onclick="navigateTo('home')" style="margin-top:2rem;">← Back to Home</button>
            </div>
        </div>
    `;
}

function getTermsOfServiceHTML() {
    return `
        <div class="page-container">
            <div class="legal-container" style="max-width:900px;margin:0 auto;padding:2rem;background:white;border-radius:1rem;box-shadow:0 2px 8px rgba(0,0,0,0.1);">
                <h1 style="color:#1B5E9D;margin-bottom:1rem;font-size:2rem;">Terms of Service</h1>
                <h2 style="color:#FF8C00;margin-top:2rem;">1. Medical Disclaimer</h2>
                <p><strong>IMPORTANT:</strong> PharmaLogic is for informational purposes only. It is not a substitute for professional medical advice. Always consult your healthcare provider.</p>
                <h2 style="color:#FF8C00;margin-top:2rem;">2. User Accounts</h2>
                <p>You are responsible for maintaining the confidentiality of your account.</p>
                <h2 style="color:#FF8C00;margin-top:2rem;">3. Limitation of Liability</h2>
                <p>PharmaLogic shall not be liable for any damages arising from your use of the platform.</p>
                <h2 style="color:#FF8C00;margin-top:2rem;">4. Contact Us</h2>
                <p>Email: legal@pharmalogic.com</p>
                <div style="color:#9ca3af;margin-top:2rem;padding-top:1rem;border-top:1px solid #e5e7eb;">Last Updated: April 2, 2026</div>
                <button class="back-button" onclick="navigateTo('home')" style="margin-top:2rem;">← Back to Home</button>
            </div>
        </div>
    `;
}

// ============================================================
//  UTILITIES
// ============================================================

function parseMeds(str) {
    if (!str) return [];
    return str.split(',').map(m => m.trim()).filter(m => m.length > 0);
}

function cap(str) {
    return str ? str.charAt(0).toUpperCase() + str.slice(1) : '';
}

function infoCard(label, value, borderColor, textColor) {
    return `
        <div style="background:white;padding:1rem;border-radius:.75rem;border-left:4px solid ${borderColor};">
            <p style="font-size:.875rem;color:#4b5563;margin-bottom:.25rem;font-weight:600;">${label}</p>
            <p style="font-size:1.125rem;font-weight:600;color:${textColor};">${value}</p>
        </div>
    `;
}

// ============================================================
//  BOOTSTRAP
// ============================================================

document.addEventListener('DOMContentLoaded', async () => {
    await tryAutoLogin();
    renderPage();
});