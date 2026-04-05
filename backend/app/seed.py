from sqlalchemy.orm import Session
from app.models.models import Disease, Symptom, Treatment
from app.database import SessionLocal


def seed_database():
    db = SessionLocal()
    try:
        if db.query(Disease).first():
            print("Database already seeded.")
            return

        diseases_data = [
            {
                "name": "Malaria",
                "description": "A mosquito-borne infectious disease caused by Plasmodium parasites. It is transmitted through the bite of infected female Anopheles mosquitoes.",
                "causes": "Bite of infected Anopheles mosquitoes, exposure to stagnant water, living in or traveling to tropical regions",
                "prevention": "Use insecticide-treated bed nets, apply mosquito repellent, wear long sleeves, eliminate standing water, take prophylactic medication when traveling to endemic areas",
                "symptoms": ["Fever", "Chills", "Headache", "Nausea", "Muscle Pain", "Fatigue", "Sweating", "Vomiting", "Diarrhea"],
                "immediate_action": "Seek medical attention immediately. Get a blood test for malaria. Stay hydrated. Use fever-reducing medication as directed by a doctor.",
                "medications": "Antimalarial drugs (artemisinin-based combination therapy), acetaminophen for fever. Consult a doctor for proper dosage.",
            },
            {
                "name": "Influenza (Flu)",
                "description": "A viral respiratory infection that can cause mild to severe illness. It spreads through droplets when infected people cough, sneeze, or talk.",
                "causes": "Influenza virus (Types A, B, C), close contact with infected individuals, touching contaminated surfaces",
                "prevention": "Get annual flu vaccine, wash hands frequently, avoid close contact with sick people, cover coughs and sneezes, stay home when sick",
                "symptoms": ["Fever", "Cough", "Sore Throat", "Runny Nose", "Body Aches", "Headache", "Fatigue", "Chills", "Nausea"],
                "immediate_action": "Rest and stay hydrated. Take over-the-counter fever reducers. Isolate to prevent spread. See a doctor if symptoms worsen or persist beyond a week.",
                "medications": "Oseltamivir (Tamiflu) if prescribed, acetaminophen or ibuprofen for fever and pain, decongestants. Consult a doctor.",
            },
            {
                "name": "Dengue Fever",
                "description": "A mosquito-borne viral infection common in tropical and subtropical regions. Can progress to severe dengue (dengue hemorrhagic fever) which is life-threatening.",
                "causes": "Dengue virus transmitted by Aedes mosquitoes, exposure in tropical/subtropical areas, standing water near homes",
                "prevention": "Use mosquito repellent, wear protective clothing, eliminate breeding sites, use window screens, community fogging programs",
                "symptoms": ["High Fever", "Severe Headache", "Pain Behind Eyes", "Joint Pain", "Muscle Pain", "Rash", "Nausea", "Vomiting", "Fatigue"],
                "immediate_action": "Seek immediate medical care. Avoid aspirin and NSAIDs (can increase bleeding risk). Stay hydrated. Monitor for warning signs like bleeding or severe abdominal pain.",
                "medications": "Acetaminophen for fever and pain (avoid aspirin/ibuprofen), oral rehydration solutions. Hospitalization may be needed for severe cases.",
            },
            {
                "name": "Typhoid Fever",
                "description": "A bacterial infection caused by Salmonella typhi, typically spread through contaminated food and water. Common in areas with poor sanitation.",
                "causes": "Consumption of contaminated food or water, poor sanitation, close contact with infected person",
                "prevention": "Drink safe/boiled water, eat well-cooked food, wash hands regularly, get vaccinated before traveling to endemic areas",
                "symptoms": ["Fever", "Headache", "Stomach Pain", "Weakness", "Loss of Appetite", "Diarrhea", "Constipation", "Rash", "Fatigue"],
                "immediate_action": "See a doctor for antibiotic treatment. Drink plenty of fluids. Eat bland, easy-to-digest foods. Complete full course of antibiotics.",
                "medications": "Antibiotics (azithromycin, ciprofloxacin, ceftriaxone) as prescribed by doctor. Oral rehydration salts. Consult a healthcare provider.",
            },
            {
                "name": "Common Cold",
                "description": "A mild viral infection of the upper respiratory tract. It is the most common infectious disease in humans, caused by various viruses.",
                "causes": "Rhinovirus, coronavirus, or other respiratory viruses; close contact with infected individuals; touching contaminated surfaces",
                "prevention": "Wash hands frequently, avoid touching face, stay away from sick people, maintain good hygiene, boost immune system",
                "symptoms": ["Runny Nose", "Sneezing", "Sore Throat", "Cough", "Mild Headache", "Mild Fatigue", "Congestion", "Watery Eyes"],
                "immediate_action": "Rest and drink plenty of fluids. Use saline nasal spray. Gargle with warm salt water. Use a humidifier. Symptoms usually resolve in 7-10 days.",
                "medications": "Decongestants, antihistamines, cough suppressants, acetaminophen or ibuprofen for discomfort. Consult a pharmacist.",
            },
            {
                "name": "Pneumonia",
                "description": "An infection that inflames the air sacs in one or both lungs, which may fill with fluid. Can be caused by bacteria, viruses, or fungi.",
                "causes": "Bacterial infection (Streptococcus pneumoniae), viral infection, fungal infection, weakened immune system, smoking",
                "prevention": "Get pneumococcal vaccine, quit smoking, wash hands regularly, maintain healthy immune system, avoid close contact with sick people",
                "symptoms": ["Cough", "Fever", "Difficulty Breathing", "Chest Pain", "Fatigue", "Chills", "Nausea", "Sweating", "Muscle Pain"],
                "immediate_action": "Seek medical attention promptly, especially if breathing is difficult. Rest, stay hydrated, and follow doctor's treatment plan.",
                "medications": "Antibiotics (for bacterial pneumonia), antiviral medications (for viral), cough medicine, fever reducers. Hospitalization may be required.",
            },
            {
                "name": "Cholera",
                "description": "An acute diarrheal disease caused by ingestion of food or water contaminated with the bacterium Vibrio cholerae. Can be fatal if untreated.",
                "causes": "Contaminated water or food, poor sanitation, flooding, inadequate sewage treatment",
                "prevention": "Drink safe water, eat properly cooked food, wash hands, ensure proper sanitation, oral cholera vaccine in endemic areas",
                "symptoms": ["Watery Diarrhea", "Vomiting", "Dehydration", "Muscle Cramps", "Nausea", "Rapid Heart Rate", "Low Blood Pressure", "Fatigue"],
                "immediate_action": "Seek emergency medical care. Begin oral rehydration immediately. Drink ORS solution. Do not delay treatment.",
                "medications": "Oral rehydration salts (ORS), IV fluids in severe cases, antibiotics (doxycycline, azithromycin) as prescribed. Emergency care may be needed.",
            },
            {
                "name": "Tuberculosis (TB)",
                "description": "A bacterial infection that primarily affects the lungs. It spreads through the air when infected people cough or sneeze. Can be latent or active.",
                "causes": "Mycobacterium tuberculosis bacteria, prolonged close contact with infected person, weakened immune system, overcrowded living conditions",
                "prevention": "Get BCG vaccine (in endemic areas), ensure good ventilation, wear masks in high-risk settings, complete TB treatment if diagnosed",
                "symptoms": ["Persistent Cough", "Chest Pain", "Coughing Blood", "Fatigue", "Weight Loss", "Fever", "Night Sweats", "Loss of Appetite", "Chills"],
                "immediate_action": "See a doctor immediately for testing. TB is curable with proper treatment. Isolate to prevent spread. Complete full treatment course.",
                "medications": "Multi-drug regimen (isoniazid, rifampin, ethambutol, pyrazinamide) for 6-9 months. Must be prescribed and monitored by a doctor.",
            },
            {
                "name": "Hepatitis A",
                "description": "A highly contagious liver infection caused by the hepatitis A virus. It is usually spread through contaminated food or water.",
                "causes": "Ingesting contaminated food or water, close contact with infected person, poor hygiene, traveling to endemic areas",
                "prevention": "Get hepatitis A vaccine, wash hands thoroughly, drink safe water, eat well-cooked food, practice good hygiene",
                "symptoms": ["Fatigue", "Nausea", "Abdominal Pain", "Loss of Appetite", "Fever", "Dark Urine", "Jaundice", "Joint Pain", "Vomiting"],
                "immediate_action": "See a doctor for evaluation. Rest and avoid alcohol. Eat small, light meals. Most people recover fully within weeks to months.",
                "medications": "No specific antiviral treatment. Supportive care: rest, hydration, avoid alcohol and liver-toxic medications. Consult a doctor.",
            },
            {
                "name": "Asthma",
                "description": "A chronic condition in which the airways narrow, swell, and produce extra mucus, making breathing difficult. It can be triggered by various factors.",
                "causes": "Allergens (dust, pollen, pet dander), air pollution, cold air, exercise, respiratory infections, stress, smoke",
                "prevention": "Identify and avoid triggers, use prescribed inhalers regularly, keep environment clean, manage allergies, have an asthma action plan",
                "symptoms": ["Difficulty Breathing", "Wheezing", "Cough", "Chest Tightness", "Shortness of Breath", "Fatigue", "Anxiety"],
                "immediate_action": "Use rescue inhaler as prescribed. Sit upright and stay calm. If symptoms don't improve, seek emergency care immediately.",
                "medications": "Bronchodilators (albuterol), inhaled corticosteroids, leukotriene modifiers. Must be prescribed by a doctor. Carry rescue inhaler always.",
            },
            {
                "name": "Diabetes (Type 2)",
                "description": "A chronic condition that affects how the body processes blood sugar (glucose). It develops when the body becomes resistant to insulin or doesn't produce enough.",
                "causes": "Obesity, sedentary lifestyle, genetics, poor diet, age, family history, high blood pressure",
                "prevention": "Maintain healthy weight, exercise regularly, eat balanced diet, limit sugar and refined carbs, get regular check-ups",
                "symptoms": ["Frequent Urination", "Excessive Thirst", "Fatigue", "Blurred Vision", "Slow Healing", "Tingling Hands", "Weight Loss", "Hunger", "Headache"],
                "immediate_action": "See a doctor for blood sugar testing. Monitor blood glucose levels. Follow dietary guidelines. Start regular physical activity.",
                "medications": "Metformin, insulin (if needed), other oral medications as prescribed. Must be managed by a healthcare provider.",
            },
            {
                "name": "Hypertension (High Blood Pressure)",
                "description": "A condition in which blood pressure in the arteries is persistently elevated. Often called the 'silent killer' as it may have no symptoms for years.",
                "causes": "Obesity, high salt intake, stress, lack of exercise, genetics, excessive alcohol, smoking, age",
                "prevention": "Reduce salt intake, exercise regularly, maintain healthy weight, limit alcohol, manage stress, avoid smoking, regular BP monitoring",
                "symptoms": ["Headache", "Dizziness", "Shortness of Breath", "Chest Pain", "Nosebleeds", "Fatigue", "Blurred Vision", "Irregular Heartbeat"],
                "immediate_action": "Monitor blood pressure regularly. If BP is dangerously high (180/120+), seek emergency care. Reduce salt intake. Manage stress.",
                "medications": "ACE inhibitors, beta-blockers, diuretics, calcium channel blockers. Must be prescribed and monitored by a doctor.",
            },
            {
                "name": "Gastroenteritis",
                "description": "An inflammation of the stomach and intestines, typically resulting from bacterial toxins or viral infection. Commonly known as stomach flu.",
                "causes": "Norovirus, rotavirus, bacterial infection (E. coli, Salmonella), contaminated food or water, close contact with infected person",
                "prevention": "Wash hands thoroughly, ensure food safety, drink safe water, avoid sharing utensils, disinfect contaminated surfaces",
                "symptoms": ["Diarrhea", "Vomiting", "Nausea", "Stomach Pain", "Fever", "Headache", "Muscle Pain", "Fatigue", "Dehydration"],
                "immediate_action": "Stay hydrated with ORS or clear fluids. Rest. Eat bland foods (BRAT diet). Seek medical care if dehydration signs appear.",
                "medications": "Oral rehydration salts, antiemetics (for vomiting), probiotics. Avoid anti-diarrheal medications if fever or bloody stool is present.",
            },
            {
                "name": "Migraine",
                "description": "A neurological condition characterized by intense, debilitating headaches often accompanied by other symptoms. Can last hours to days.",
                "causes": "Genetics, hormonal changes, certain foods, stress, bright lights, weather changes, lack of sleep, strong smells",
                "prevention": "Identify and avoid triggers, maintain regular sleep schedule, manage stress, stay hydrated, regular exercise, keep a headache diary",
                "symptoms": ["Severe Headache", "Nausea", "Sensitivity to Light", "Sensitivity to Sound", "Vomiting", "Blurred Vision", "Dizziness", "Fatigue"],
                "immediate_action": "Rest in a dark, quiet room. Apply cold compress. Take pain reliever early. Avoid triggers. See a doctor if migraines are frequent.",
                "medications": "Triptans, NSAIDs, anti-nausea medications, preventive medications for chronic migraines. Consult a neurologist.",
            },
            {
                "name": "Anemia",
                "description": "A condition in which the body lacks enough healthy red blood cells to carry adequate oxygen to tissues. Iron deficiency is the most common cause.",
                "causes": "Iron deficiency, vitamin B12 deficiency, chronic disease, blood loss, genetic disorders (sickle cell), poor diet",
                "prevention": "Eat iron-rich foods, consume vitamin C with iron sources, get adequate B12 and folate, treat underlying conditions",
                "symptoms": ["Fatigue", "Weakness", "Pale Skin", "Shortness of Breath", "Dizziness", "Cold Hands", "Headache", "Irregular Heartbeat", "Chest Pain"],
                "immediate_action": "See a doctor for blood tests. Increase iron-rich foods. Do not self-diagnose as anemia has multiple causes requiring different treatments.",
                "medications": "Iron supplements, vitamin B12 supplements, folic acid. Treatment depends on the type of anemia. Must be guided by a doctor.",
            },
        ]

        for disease_data in diseases_data:
            disease = Disease(
                name=disease_data["name"],
                description=disease_data["description"],
                causes=disease_data["causes"],
                prevention=disease_data["prevention"],
            )

            treatment = Treatment(
                immediate_action=disease_data["immediate_action"],
                medications=disease_data["medications"],
            )
            disease.treatments = treatment

            db.add(disease)
            db.flush()

            for symptom_name in disease_data["symptoms"]:
                symptom = db.query(Symptom).filter(Symptom.name == symptom_name).first()
                if not symptom:
                    symptom = Symptom(name=symptom_name)
                    db.add(symptom)
                    db.flush()
                disease.symptoms.append(symptom)

        db.commit()
        print(f"Database seeded with {len(diseases_data)} diseases.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()
