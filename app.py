import streamlit as st
from datetime import datetime

st.set_page_config(page_title="e-FarMar", page_icon="🌾", layout="wide")

# Step 1: Install dependencies
print("📦 Installing dependencies...")


# Step 2: Create the app file
print("📝 Creating app file...")

app_code = '''
import streamlit as st
import json
from datetime import datetime
import random

# Page configuration
st.set_page_config(
    page_title="e-FarMar",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for mobile-responsive design
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    
    .app-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .product-card {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
    }
    
    .message-bubble {
        padding: 0.8rem;
        margin: 0.5rem 0;
        border-radius: 15px;
        max-width: 80%;
    }
    
    .message-sent {
        background: #667eea;
        color: white;
        margin-left: auto;
    }
    
    .message-received {
        background: #f0f0f0;
        color: black;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'splash'
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'users_db' not in st.session_state:
    st.session_state.users_db = {}
if 'products' not in st.session_state:
    st.session_state.products = []
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'posts' not in st.session_state:
    st.session_state.posts = []
if 'is_seller' not in st.session_state:
    st.session_state.is_seller = False
if 'current_location' not in st.session_state:
    st.session_state.current_location = "Near Umiam, Meghalaya"

# Crops and their value-added products
CROPS_DATA = {
    "Jackfruit": ["Chips", "Flour", "Papad", "Crackers, Cookies and Cakes", "Squash", "Powders", "Pickle", "RTC Tender Jackfruit"],
    "Pumpkin": ["Chips", "Flour", "Candy", "Pickle", "Jam", "Powder"],
    "Ginger": ["Pickle", "Candy", "Powder", "Tea", "Oil", "Juice"],
    "Root Vegetables": ["Chips", "Pickle", "Powder", "Curry"],
    "Vegetable Crops": ["Pickle", "Chips", "Dried Vegetables", "Powder"],
    "Millets": ["Flour", "Cookies", "Bread", "Noodles", "Pasta"]
}

# Sample products
SAMPLE_PRODUCTS = [
    {"name": "Jackfruit Chips", "price": 150, "quantity": "500g", "location": "Tura", "rating": 4.5, "brand": "Megha Organics", "seller": "Ram Kumar", "image": "🥔"},
    {"name": "Ginger Pickle", "price": 200, "quantity": "250g", "location": "Shillong", "rating": 4.8, "brand": "Hills Fresh", "seller": "Mary Lyngdoh", "image": "🥒"},
    {"name": "Pumpkin Flour", "price": 120, "quantity": "1kg", "location": "Nongpoh", "rating": 4.3, "brand": "Farm Direct", "seller": "David Singh", "image": "🎃"},
    {"name": "Millet Cookies", "price": 180, "quantity": "300g", "location": "Umiam", "rating": 4.6, "brand": "Healthy Bites", "seller": "Priya Das", "image": "🍪"},
]

if not st.session_state.products:
    st.session_state.products = SAMPLE_PRODUCTS.copy()

def navigate_to(page):
    st.session_state.page = page
    st.rerun()

def splash_screen():
    st.markdown("""
    <div style='text-align: center; padding: 5rem 2rem;'>
        <h1 style='font-size: 3rem; color: #667eea;'>🌾 e-FarMar 🌾</h1>
        <p style='font-size: 1.2rem; color: #666; margin-top: 1rem;'>
            Connecting Farmers & Buyers in Meghalaya
        </p>
        <p style='font-size: 0.9rem; color: #999; margin-top: 2rem;'>
            A Joint Initiative of Two Universities
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Enter App", use_container_width=True):
        navigate_to('home')

def show_login():
    st.markdown("<div class='app-header'><h2>🌾 e-FarMar Login</h2></div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login")
        mobile = st.text_input("Mobile Number", key="login_mobile")
        otp = st.text_input("OTP", type="password", key="login_otp")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Send OTP", key="send_otp"):
                st.success("OTP sent: 123456")
        with col2:
            if st.button("Login", key="login_btn"):
                if mobile in st.session_state.users_db:
                    st.session_state.logged_in = True
                    st.session_state.user_data = st.session_state.users_db[mobile]
                    st.success("Login successful!")
                    navigate_to('home')
                else:
                    st.error("User not found. Please register first.")
    
    with tab2:
        st.subheader("Register")
        name = st.text_input("Name", key="reg_name")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="reg_gender")
        age = st.number_input("Age", min_value=18, max_value=100, key="reg_age")
        mobile = st.text_input("Mobile Number", key="reg_mobile")
        address = st.text_area("Address", key="reg_address")
        location = st.text_input("Location", value=st.session_state.current_location, key="reg_location")
        id_type = st.selectbox("Govt. ID Type", ["Aadhar", "Voter ID", "Pan Card", "Others"], key="reg_id")
        id_number = st.text_input("ID Number", key="reg_id_num")
        gst_no = st.text_input("GST No. (If Any)", key="reg_gst")
        
        if st.button("Register", key="register_btn"):
            if name and mobile and address:
                st.session_state.users_db[mobile] = {
                    "name": name, "gender": gender, "age": age, "mobile": mobile,
                    "address": address, "location": location, "id_type": id_type,
                    "id_number": id_number, "gst_no": gst_no
                }
                st.session_state.logged_in = True
                st.session_state.user_data = st.session_state.users_db[mobile]
                st.success("Registration successful!")
                navigate_to('home')
            else:
                st.error("Please fill all required fields")

def home_page():
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("☰", key="menu_btn"):
            st.session_state.show_sidebar = not st.session_state.get('show_sidebar', False)
    with col2:
        st.markdown("<div class='app-header'><h2>🌾 e-FarMar</h2></div>", unsafe_allow_html=True)
    with col3:
        if st.button("🛒", key="cart_icon"):
            navigate_to('cart')
    
    st.info(f"📍 {st.session_state.current_location}")
    search_query = st.text_input("🔍 Search products...", key="search")
    
    st.markdown("### Filters")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.checkbox("Location", key="filter_loc")
    with col2:
        st.checkbox("Price", key="filter_price")
    with col3:
        st.checkbox("Bestseller", key="filter_best")
    with col4:
        st.checkbox("Crop", key="filter_crop")
    
    st.markdown("### Available Products")
    
    products_to_display = st.session_state.products
    if search_query:
        products_to_display = [p for p in products_to_display if search_query.lower() in p['name'].lower()]
    
    for product in products_to_display:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown(f"<div style='font-size: 4rem; text-align: center;'>{product['image']}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"**{product['name']}**")
            st.markdown(f"💰 ₹{product['price']} | 📦 {product['quantity']}")
            st.markdown(f"📍 {product['location']} | ⭐ {product['rating']}")
            st.markdown(f"🏷️ Brand: {product.get('brand', 'N/A')}")
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                if st.button("📞 Call", key=f"call_{product['name']}"):
                    st.success("Calling...")
            with col_b:
                if st.button("💬 WhatsApp", key=f"wa_{product['name']}"):
                    st.success("Opening WhatsApp...")
            with col_c:
                if st.button("🛒 Add", key=f"add_{product['name']}"):
                    st.session_state.cart.append(product)
                    st.success("Added to cart!")
        st.markdown("---")

def general_procedure():
    st.markdown("<div class='app-header'><h2>📋 General Procedures</h2></div>", unsafe_allow_html=True)
    
    crop_selected = st.selectbox("Choose Crop", list(CROPS_DATA.keys()))
    
    if crop_selected:
        st.markdown(f"### Value-Added Products from {crop_selected}")
        products = CROPS_DATA[crop_selected]
        
        for product in products:
            if st.button(f"📄 {product}", key=f"proc_{product}"):
                st.info(f"Showing procedure for {product} from {crop_selected}")
                st.markdown(f"""
                **General Procedure for {product}**
                
                Recommended by CCS, Tura
                
                *Steps include:*
                1. Raw material preparation
                2. Processing methods
                3. Packaging guidelines
                4. Storage recommendations
                5. Quality standards
                """)

def sell_products():
    st.markdown("<div class='app-header'><h2>🏪 Sell Your Products</h2></div>", unsafe_allow_html=True)
    
    if not st.session_state.is_seller:
        st.markdown("### Register as a Seller")
        name = st.text_input("Name")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        mobile = st.text_input("Mobile Number")
        address = st.text_area("Address")
        
        if st.button("Register as Seller"):
            st.session_state.is_seller = True
            st.success("Registered as seller!")
            st.rerun()
    else:
        st.markdown("### Upload Product")
        product_name = st.text_input("Product Name")
        price = st.number_input("Price (₹)", min_value=0)
        quantity = st.text_input("Quantity")
        brand_name = st.text_input("Brand Name")
        product_image = st.selectbox("Icon", ["🥔", "🥒", "🎃", "🍪", "🌾"])
        
        if st.button("Upload Product"):
            new_product = {
                "name": product_name, "price": price, "quantity": quantity,
                "location": st.session_state.current_location, "rating": 0,
                "brand": brand_name, "seller": st.session_state.user_data.get('name', 'Anonymous'),
                "image": product_image
            }
            st.session_state.products.append(new_product)
            st.success("Product uploaded!")

def messages_page():
    st.markdown("<div class='app-header'><h2>💬 Messages</h2></div>", unsafe_allow_html=True)
    
    contacts = ["Ram Kumar", "Mary Lyngdoh", "David Singh"]
    selected_contact = st.selectbox("Select Contact", contacts)
    
    if selected_contact:
        st.markdown(f"### Chat with {selected_contact}")
        messages = [
            {"sender": "other", "text": "Hello! Is the product available?"},
            {"sender": "me", "text": "Yes, it's available!"}
        ]
        
        for msg in messages:
            if msg['sender'] == 'me':
                st.markdown(f"<div class='message-bubble message-sent'>{msg['text']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='message-bubble message-received'>{msg['text']}</div>", unsafe_allow_html=True)
        
        new_message = st.text_input("Type message...", key="new_msg")
        if st.button("Send"):
            st.success("Message sent!")

def posts_page():
    st.markdown("<div class='app-header'><h2>📝 Post Requirements</h2></div>", unsafe_allow_html=True)
    
    with st.expander("➕ Create New Post", expanded=True):
        product_type = st.text_input("Product Type")
        price_range = st.text_input("Price Range")
        required_quantity = st.text_input("Required Quantity")
        
        if st.button("Post Requirement"):
            new_post = {
                "product": product_type, "price_range": price_range,
                "quantity": required_quantity,
                "poster": st.session_state.user_data.get('name', 'Anonymous'),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            st.session_state.posts.append(new_post)
            st.success("Posted!")
    
    st.markdown("### Recent Requirements")
    if st.session_state.posts:
        for post in reversed(st.session_state.posts):
            st.markdown(f"""
            **{post['poster']}**
            🛒 {post['product']} | 💰 {post['price_range']} | 📦 {post['quantity']}
            🕒 {post['timestamp']}
            """)
            st.button("📞 Respond", key=f"respond_{post['timestamp']}")
            st.markdown("---")
    else:
        st.info("No posts yet!")

def cart_page():
    st.markdown("<div class='app-header'><h2>🛒 Your Cart</h2></div>", unsafe_allow_html=True)
    
    if not st.session_state.cart:
        st.info("Cart is empty!")
        if st.button("← Back to Home"):
            navigate_to('home')
    else:
        total = 0
        for idx, item in enumerate(st.session_state.cart):
            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown(f"<div style='font-size: 3rem;'>{item['image']}</div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"**{item['name']}** - ₹{item['price']}")
                if st.button("🗑️ Remove", key=f"remove_{idx}"):
                    st.session_state.cart.pop(idx)
                    st.rerun()
            total += item['price']
            st.markdown("---")
        
        st.markdown(f"### Total: ₹{total}")
        st.info("💡 Contact sellers directly for payment.")
        if st.button("Contact Sellers"):
            st.success("Contact details shared!")

def show_sidebar():
    with st.sidebar:
        st.markdown("### 👤 Profile")
        if st.session_state.logged_in:
            user = st.session_state.user_data
            st.markdown(f"**{user.get('name', 'Guest')}**")
            st.markdown(f"📱 {user.get('mobile', 'N/A')}")
        else:
            if st.button("Login/Register"):
                navigate_to('login')
        
        st.markdown("---")
        if st.button("🏠 Home", use_container_width=True):
            navigate_to('home')
        if st.button("📋 General Procedure", use_container_width=True):
            navigate_to('procedure')
        if st.button("🏪 Sell Products", use_container_width=True):
            navigate_to('sell')
        
        st.markdown("---")
        st.selectbox("🌐 Language", ["English", "Hindi", "Khasi", "Garo"])

def bottom_nav():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🏠 Home", key="nav_home", use_container_width=True):
            navigate_to('home')
    with col2:
        if st.button("💬 Messages", key="nav_msg", use_container_width=True):
            navigate_to('messages')
    with col3:
        if st.button("📝 Post", key="nav_post", use_container_width=True):
            navigate_to('posts')
    with col4:
        cart_count = len(st.session_state.cart)
        if st.button(f"🛒 ({cart_count})", key="nav_cart", use_container_width=True):
            navigate_to('cart')

def main():
    if st.session_state.get('show_sidebar', False):
        show_sidebar()
    
    if st.session_state.page == 'splash':
        splash_screen()
    elif st.session_state.page == 'login':
        show_login()
        if st.button("← Back"):
            navigate_to('home')
    elif st.session_state.page == 'home':
        home_page()
        bottom_nav()
    elif st.session_state.page == 'procedure':
        general_procedure()
        if st.button("← Back"):
            navigate_to('home')
    elif st.session_state.page == 'sell':
        sell_products()
        if st.button("← Back"):
            navigate_to('home')
    elif st.session_state.page == 'messages':
        messages_page()
        bottom_nav()
    elif st.session_state.page == 'posts':
        posts_page()
        bottom_nav()
    elif st.session_state.page == 'cart':
        cart_page()
        bottom_nav()

if __name__ == "__main__":
    main()
'''

with open('app.py', 'w') as f:
    f.write(app_code)

print("✅ App file created!")

# Step 3: Run the app
print("\n🚀 Starting e-FarMar app...")
print("⏳ Please wait 10-15 seconds...\n")

import subprocess
import threading
import time

def run_streamlit():
    subprocess.Popen(['streamlit', 'run', 'app.py', '--server.port=8501', '--server.headless=true'])

def run_localtunnel():
    time.sleep(10)
    subprocess.run(['npx', 'localtunnel', '--port', '8501'])

# Start streamlit in background
streamlit_thread = threading.Thread(target=run_streamlit)
streamlit_thread.start()

# Start localtunnel
print("🌐 Creating public URL...")
run_localtunnel()
