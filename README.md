# myUmuganda

## 📌 **Project Overview**
**myUmuganda** is a nationwide platform built with **Django** for the backend and an integrated **Admin Panel** that uses **Django templates** as the frontend for administrative users.  

Citizens access the system using the **myUmuganda Mobile App**, while all administrative actions are performed via the web-based admin panel.  

The platform follows Rwanda’s full administrative hierarchy:  
**Province → District → Sector → Cell → Village**  

### 🔑 **Key Concepts**
- **SuperAdmin** is the highest user level and is the only one who can create admin accounts.  
- **Sector Officers** accounts are created by the SuperAdmin to keep the system manageable and confidential. 
- **Sector Officers** creates the  **Cell Officers** accounts
- **Citizens** can create their own accounts through the **myUmuganda App**.  
- **Umuganda activities** are managed at the **Sector level** but executed at the **Cell level** so participants can work locally.  but the system is build in way such that all sectors nationwide will have access to management of their umuganda activity

---

## 🚀 **Features**

### 👤 **User & Account Management**
- **SuperAdmin**
  - Creates all admin accounts (**Sector Officers**)  
  - Assigns officers to specific Sectors or Cells (one-to-one assignment).  
  - Views action logs of all admins.  
  - Handles Sectors with duplicate names by displaying them as:  
    **sector_name (district_name, province_name)**.  

- **Sector Officers**
  - Manage **Umuganda** at the sector level. 
  - **Sector Officers** creates  **Cell Officers** account. 
  - Set the **Umuganda date** for the whole sector.  
  - Assign Cell Officers to cells within their sector.  
  - View activities done by Cell Officers and filter them per cell.  

- **Cell Officers**
  - Receive automatic notifications when a Sector Officer sets a sector-wide date.  
  - Add detailed session info at the **Cell level**, including:  
    - **Village location** where Umuganda will take place.  
    - **Tools needed** for the activity.  
    - **Fine policy** for absentees.  
    - **Description** of the session.  
  - View the list of citizens in their cell scheduled to attend.  
  - Mark attendance and manage fines.  

- **Citizens**
  - Register using the **myUmuganda App**.  
  - Automatically linked to their **Province, District, Sector, Cell, and Village** using dropdown filtering.  
  - See **Umuganda** sessions planned for their **specific cell**.  
  - Even if two citizens are in the same sector, they only share the **date** if they are in different cells; all other details (village, tools, fines, description) depend on the **Cell Officer**.  

---

### 🛠️ **Umuganda Management Workflow**
1. **Sector Officer** sets the sector-wide **Umuganda date**.  
2. **Cell Officers**:
   - Automatically notified via in-app and email notifications.  
   - Add specific details at the cell level (village, tools, description, fines).  
3. **Citizens**:
   - Receive session info relevant to their cell only.  
   - Are notified if the session is within 3 days (automatic Celery scheduled reminders twice a day).  
4. **Attendance & Fines**:
   - Cell Officers mark attendance filtered by user’s **Sector and Cell**.  
   - If the **Umuganda date passes** and some users have no attendance marked, a signal automatically fines them based on the fine policy.  
   - Another signal detects new fines and sends **email + SMS notifications** via **Celery + Redis**.  

---

### 📍 **Administrative Hierarchy Integration**
- Full database of **Provinces, Districts, Sectors, Cells, Villages** preloaded.  
- Dropdown-based selection to avoid manual typing of location names.  
- Automatic filtering ensures users and admins are linked to correct administrative levels.  

---

### 📢 **Notifications**
- Citizens are notified when:  
  - A Sector Officer sets a new **Umuganda** date.  
  - A session is 3 days away (Celery scheduled reminders).  
  - They are fined for missing attendance (email + SMS via Celery).  

---

### 💸 **Payments**
- Citizens can pay fines via **Mobile Money (MTN & Airtel)**.  
- Payment API integration is planned for production.  

---

### 🔐 **Account Management**
- Citizens and admins can update their profile information.  
- Password reset via **OTP sent to email** using **Celery + Redis**.  


## 📌 Sample Login Credentials

### 🟣 SuperAdmin
- **Email:** fidelensanzumuhire9@gmail.com  
  **Password:** 11223344  

---

### 🟢 Sector Officers
- **Email:** kagarama@kagarama.com  
  **Password:** 11223344  

- **Email:** kigoma@kigoma.com  
  **Password:** 11223344  

- **Email:** muhoza@muhoza.com  
  **Password:** 11223344  

- **Email:** nyamata@nyamata.com  
  **Password:** 11223344  

---

### 🔵 Cell Officers
- **Email:** kanazi@kanazi.com  
  **Password:** 11223344  

- **Email:** maranyundo1@maranyundo.com  
  **Password:** 11223344  

- **Email:** mpenge@mpenge.com  
  **Password:** 11223344  

- **Email:** kigombe@kigombe.com  
  **Password:** 11223344  

---

### 🟠 Citizens




## 🔑 Creating Additional Users

✅ **Apart from SuperAdmin only, you can create other user accounts yourself:**  

1. **Create Sector Officer Accounts**  
   - Go to the **SuperAdmin Dashboard**.  
   - **First add the Sector** the officer will lead by clicking the **"Add Sector"** button.  
   - After adding the sector, create the Sector Officer account with login credentials and assign it to that sector.  

2. **Create Cell Officer Accounts**  
   - Go to the **Sector Officer Dashboard**.  
   - Add a new Cell Officer and select the **Cell he will lead** from the list of cells in the sector.  

3. **Create Citizen Accounts**  
   - You can register citizens directly from the **myUmuganda Mobile App**.  
   - There is no limit on the number of citizens you can create.  


## 🔗 Deployed Links

- 🌐 **Backend & Admin Panel:** [https://umuganda.onrender.com](https://umuganda.onrender.com)  
- 📥 **Citizen App APK Download:** [https://www.mediafire.com/file/iocxm8nxi3q2y28/app-release.apk/file](https://www.mediafire.com/file/iocxm8nxi3q2y28/app-release.apk/file)  
