# 📣 Influencify – Influencer Engagement and Sponsorship Coordination Platform

**Influencify** is a multi-user web application that bridges the gap between **Sponsors** and **Influencers**. It provides a dynamic platform where brands can promote their products/services through the reach of online influencers, and influencers can monetize their reach and content creation skills.

---

## 🌟 Key Highlights

- 🎯 Sponsors can **create, manage, and monitor** ad campaigns.
- 🤝 Influencers can **explore public campaigns**, send collaboration requests, and **receive private campaign invitations**.
- 🔍 Powerful **search and filter tools** based on username, niche, follower count, and more.
- 📊 Visual insights into platform activity and trends using **Matplotlib charts**.
- 🧑‍💼 Personalized dashboards for each user type.

---

## 🧰 Technologies Used

### 🔧 Backend
- **Flask** – Lightweight and flexible Python web framework  
- **Flask-SQLAlchemy** – ORM for managing and querying SQLite database  
- **Flask-RESTful** – For building REST APIs  
- **sqlite3** – Simple file-based database for development  
- **Matplotlib** – Used for generating graphical insights and analytics  

### 🎨 Frontend
- **Jinja2** – Templating engine for rendering dynamic HTML  
- **Bootstrap 5** – For responsive and mobile-friendly design  
- **HTML5, CSS3, JavaScript** – For UI interactivity and layout  

---

## 💡 Features

### 👥 Multi-User System
- Role-based authentication (Sponsor / Influencer)
- Custom dashboards for each user type
- Secure login and session handling

### 📢 Sponsors
- Create, update, and delete marketing campaigns
- View requests from influencers for collaboration
- Send **private campaign invites** to specific influencers
- Monitor campaign performance with visual stats

### 🌐 Influencers
- Browse **public campaigns** from various sponsors
- Send campaign participation requests
- Accept/reject private campaign invitations
- Track approved campaigns and earnings

### 🔎 Search and Discover
- Search other users by:
  - Username
  - Niche/Category
  - Follower count
- View basic analytics of influencer engagement

### 📊 Insights
- Histogram plots showing:
  - Active campaigns
  - Top-performing influencers
  - Sponsor activity levels

---

## 🖼️ Screenshots

| Home Page | Login Page |
|-----------|-------------|
| ![Home](https://github.com/user-attachments/assets/9f2477bb-c13b-434e-8e4f-ef70487acc31) | ![Login](https://github.com/user-attachments/assets/af245814-bfeb-4617-8f4b-8ae50d4a71c5) |

| Sponsor Dashboard | Influencer Dashboard |
|--------------------|----------------------|
| ![Sponsor](https://github.com/user-attachments/assets/070e555e-6063-4fb5-99a1-2ae0e7c9304b) | ![Influencer](https://github.com/user-attachments/assets/0e89a5e5-b404-4449-89b7-031cade930ed) |

---

## 🚀 How to Run the Project Locally

```bash
# Clone the repository
git clone https://github.com/shreyasaxena21/Influencer-Sponsor-Engagement-Coordination-Platform---MAD1-Project
cd Influencer-Sponsor-Engagement-Coordination-Platform---MAD1-Project

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask application
python app.py
```

## 🔒 Security Features
- Session management with Flask

- Role-based access to features

- CSRF protection for forms


## 🔮 Future Improvements
- ✅ Email notifications for request approvals and campaign updates

- 📱 Mobile-responsive version of dashboards

- 🗂️ Admin dashboard for platform overview and moderation

- 💬 In-app messaging between sponsors and influencers

- 🌍 OAuth login (Google/Facebook) support

## 📬 Contact
- For questions or feedback:
  - 📧 Email: shreyasaxena2104@gmail.com
  - 🌐 GitHub: https://github.com/shreyasaxena21