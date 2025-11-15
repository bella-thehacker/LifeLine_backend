# hospital_api/management/commands/seed.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from hospital_api.models import Patient, Doctor, Appointment, InventoryItem, Department
from datetime import datetime, date

class Command(BaseCommand):
    help = "Seeds the database with sample data for hospital_api"

    def handle(self, *args, **kwargs):

        # ---- Admin user ----
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@hospital.com", "admin123")
            self.stdout.write(self.style.SUCCESS("✔ Admin user created (admin / admin123)"))

        # ---- Staff user ----
        if not User.objects.filter(username="staff1").exists():
            User.objects.create_user("staff1", "staff@hospital.com", "staff123")
            self.stdout.write(self.style.SUCCESS("✔ Staff user created (staff1 / staff123)"))

        # ---- Departments ----
        cardiology, _ = Department.objects.get_or_create(name="Cardiology", location="Block A")
        pediatrics, _ = Department.objects.get_or_create(name="Pediatrics", location="Block B")
        neurology, _ = Department.objects.get_or_create(name="Neurology", location="Block C")
        orthopedics, _ = Department.objects.get_or_create(name="Orthopedics", location="Block D")
        dermatology, _ = Department.objects.get_or_create(name="Dermatology", location="Block E")

        # ---- Doctors ----
        doctors_data = [
            {"username": "dr_njoroge", "first_name": "Njoroge", "last_name": "Mwangi", "email": "njoroge.m@hospital.com", "password": "doctor123", "phone": "+254711222333", "department": cardiology, "specialization": "Cardiologist"},
            {"username": "dr_amina", "first_name": "Amina", "last_name": "Hassan", "email": "amina.h@hospital.com", "password": "doctor123", "phone": "+254711222334", "department": pediatrics, "specialization": "Pediatrician"},
            {"username": "dr_kimani", "first_name": "Kimani", "last_name": "Kariuki", "email": "kimani.k@hospital.com", "password": "doctor123", "phone": "+254711222335", "department": orthopedics, "specialization": "Orthopedic Surgeon"},
            {"username": "dr_fatuma", "first_name": "Fatuma", "last_name": "Mohamed", "email": "fatuma.m@hospital.com", "password": "doctor123", "phone": "+254711222336", "department": neurology, "specialization": "Neurologist"},
            {"username": "dr_mutua", "first_name": "Mutua", "last_name": "Musyoka", "email": "mutua.m@hospital.com", "password": "doctor123", "phone": "+254711222337", "department": dermatology, "specialization": "Dermatologist"},
        ]

        doctors = []
        for doc in doctors_data:
            user, created = User.objects.get_or_create(
                username=doc["username"],
                defaults={"first_name": doc["first_name"], "last_name": doc["last_name"], "email": doc["email"]}
            )
            if created:
                user.set_password(doc["password"])
                user.save()
            doctor, _ = Doctor.objects.get_or_create(
                user=user,
                phone=doc["phone"],
                specialization=doc["specialization"]
            )
            doctors.append(doctor)
        self.stdout.write(self.style.SUCCESS("✔ Doctors added"))

        # ---- Patients ----
        patients_data = [
            {"first_name": "Wanjiku", "last_name": "Kamau", "dob": date(1990,5,15), "gender": "Female", "phone": "+254712345678", "email": "wanjiku.k@email.com"},
            {"first_name": "Kipchoge", "last_name": "Rotich", "dob": date(1985,3,12), "gender": "Male", "phone": "+254712345679", "email": "kipchoge.r@email.com"},
            {"first_name": "Akinyi", "last_name": "Odhiambo", "dob": date(2015,7,8), "gender": "Female", "phone": "+254712345680", "email": "akinyi.o@email.com"},  # child
            {"first_name": "Omondi", "last_name": "Otieno", "dob": date(1988,11,23), "gender": "Male", "phone": "+254712345681", "email": "omondi.o@email.com"},
            {"first_name": "Chebet", "last_name": "Koech", "dob": date(1995,2,14), "gender": "Female", "phone": "+254712345682", "email": "chebet.k@email.com"},
            {"first_name": "Kamau", "last_name": "Njuguna", "dob": date(2017,8,30), "gender": "Male", "phone": "+254712345683", "email": "kamau.n@email.com"},  # child
            {"first_name": "Fatuma", "last_name": "Mohamed", "dob": date(1993,6,19), "gender": "Female", "phone": "+254712345684", "email": "fatuma.m@email.com"},
            {"first_name": "Jelimo", "last_name": "Cheruiyot", "dob": date(2018,4,2), "gender": "Female", "phone": "+254712345685", "email": "jelimo.c@email.com"},  # child
            {"first_name": "Peter", "last_name": "Wachira", "dob": date(1991,12,11), "gender": "Male", "phone": "+254712345686", "email": "peter.w@email.com"},
            {"first_name": "Mary", "last_name": "Wambui", "dob": date(1989,1,20), "gender": "Female", "phone": "+254712345687", "email": "mary.w@email.com"},
        ]

        patients = []
        for pat in patients_data:
            patient, _ = Patient.objects.get_or_create(**pat)
            patients.append(patient)
        self.stdout.write(self.style.SUCCESS("✔ Patients added"))

        # ---- Appointments ----
        appointments_data = [
            {"patient": patients[0], "doctor": doctors[0], "scheduled_at": datetime(2024,1,20,9,0), "type": "Cardiology Checkup", "status": "confirmed"},
            {"patient": patients[1], "doctor": doctors[1], "scheduled_at": datetime(2024,1,20,10,30), "type": "Pediatric Consultation", "status": "pending"},
            {"patient": patients[2], "doctor": doctors[1], "scheduled_at": datetime(2024,1,20,11,0), "type": "Pediatric Vaccination", "status": "confirmed"},
            {"patient": patients[3], "doctor": doctors[2], "scheduled_at": datetime(2024,1,20,14,0), "type": "Orthopedic Follow-up", "status": "pending"},
            {"patient": patients[4], "doctor": doctors[4], "scheduled_at": datetime(2024,1,21,9,30), "type": "Dermatology Consultation", "status": "confirmed"},
            {"patient": patients[5], "doctor": doctors[1], "scheduled_at": datetime(2024,1,21,11,0), "type": "Pediatric Checkup", "status": "completed"},
            {"patient": patients[6], "doctor": doctors[0], "scheduled_at": datetime(2024,1,21,13,0), "type": "Heart Checkup", "status": "cancelled"},
            {"patient": patients[7], "doctor": doctors[1], "scheduled_at": datetime(2024,1,22,9,0), "type": "Growth Monitoring", "status": "confirmed"},
            {"patient": patients[8], "doctor": doctors[3], "scheduled_at": datetime(2024,1,22,10,0), "type": "Neurology Consultation", "status": "pending"},
            {"patient": patients[9], "doctor": doctors[2], "scheduled_at": datetime(2024,1,22,11,30), "type": "Bone Density Scan", "status": "confirmed"},
        ]

        for apt in appointments_data:
            Appointment.objects.get_or_create(**apt)
        self.stdout.write(self.style.SUCCESS("✔ Appointments added"))

        # ---- Inventory Items ----
               # ---- Inventory Items ----
        medicines_data = [
            # Analgesics
            {"sku": "M001", "name": "Paracetamol", "category": "Analgesic", "uses": "Pain relief and fever reduction", "stock": 450, "min_stock": 200, "unit": "tablets", "expiry_date": date(2025,6,15)},
            {"sku": "M002", "name": "Ibuprofen", "category": "NSAID", "uses": "Pain relief, inflammation reduction", "stock": 180, "min_stock": 150, "unit": "tablets", "expiry_date": date(2026,1,10)},

            # Antibiotics
            {"sku": "M003", "name": "Amoxicillin", "category": "Antibiotic", "uses": "Treat bacterial infections", "stock": 300, "min_stock": 100, "unit": "capsules", "expiry_date": date(2025,8,10)},
            {"sku": "M004", "name": "Ciprofloxacin", "category": "Antibiotic", "uses": "Treat respiratory and urinary infections", "stock": 120, "min_stock": 80, "unit": "tablets", "expiry_date": date(2025,11,22)},

            # Syrups (Pediatrics)
            {"sku": "M005", "name": "Calpol Syrup", "category": "Pediatric Analgesic", "uses": "Pain and fever relief for children", "stock": 90, "min_stock": 40, "unit": "bottles", "expiry_date": date(2024,12,30)},
            {"sku": "M006", "name": "Amoxicillin Syrup", "category": "Pediatric Antibiotic", "uses": "Bacterial infections in children", "stock": 60, "min_stock": 30, "unit": "bottles", "expiry_date": date(2025,3,18)},

            # IV Medicines
            {"sku": "M007", "name": "Normal Saline (0.9%)", "category": "IV Fluid", "uses": "Rehydration and IV medication dilution", "stock": 250, "min_stock": 100, "unit": "bags", "expiry_date": date(2026,5,20)},
            {"sku": "M008", "name": "Dextrose 5%", "category": "IV Fluid", "uses": "Energy supply and fluid replacement", "stock": 140, "min_stock": 70, "unit": "bags", "expiry_date": date(2026,3,12)},
            {"sku": "M009", "name": "Ringer’s Lactate", "category": "IV Fluid", "uses": "Electrolyte replenishment and dehydration", "stock": 80, "min_stock": 60, "unit": "bags", "expiry_date": date(2025,7,5)},

            # Emergency / Consumables
            {"sku": "M010", "name": "ORS Sachets", "category": "Oral Rehydration", "uses": "Treat dehydration and diarrhea", "stock": 40, "min_stock": 50, "unit": "sachets", "expiry_date": date(2024,10,1)},  # low
            {"sku": "M011", "name": "Hydrocortisone Injection", "category": "Steroid Injection", "uses": "Severe allergic reactions and inflammation", "stock": 30, "min_stock": 20, "unit": "vials", "expiry_date": date(2025,4,20)},
            {"sku": "M012", "name": "Adrenaline (Epinephrine)", "category": "Emergency Injection", "uses": "Anaphylaxis treatment", "stock": 15, "min_stock": 10, "unit": "vials", "expiry_date": date(2025,1,15)},
        ]

        for med in medicines_data:
            InventoryItem.objects.get_or_create(**med)

        self.stdout.write(self.style.SUCCESS("✔ Inventory items added"))


        self.stdout.write(self.style.SUCCESS("🎉 Database seeded successfully!"))
