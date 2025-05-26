import streamlit as st
import time
import platform
import os
import subprocess
import asyncio
from playwright.async_api import async_playwright

# Configure Streamlit page
st.set_page_config(
    page_title="تبدیل شبا به سپرده - بانک پاسارگاد",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Persian styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        font-size: 2.5rem;
        margin-bottom: 2rem;
        direction: rtl;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .service-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
        text-align: center;
        direction: rtl;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
    }
    .result-box {
        background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%);
        border: 3px solid #4CAF50;
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        direction: rtl;
        box-shadow: 0 8px 32px rgba(76, 175, 80, 0.2);
        position: relative;
        overflow: hidden;
    }
    .result-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #4CAF50, #45a049, #4CAF50);
        animation: shimmer 2s infinite;
    }
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    .result-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2E86AB;
        margin-bottom: 1rem;
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
    }
    .result-content {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #4CAF50;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    }
    .result-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem;
        margin: 0.5rem 0;
        background: #f8f9fa;
        border-radius: 8px;
        border-right: 4px solid #4CAF50;
        transition: all 0.3s ease;
    }
    .result-item:hover {
        background: #e8f5e8;
        transform: translateX(-5px);
    }
    .result-label {
        font-weight: bold;
        color: #2c3e50;
        font-size: 1.1rem;
    }
    .result-value {
        font-family: 'Courier New', monospace;
        background: #2c3e50;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-size: 1rem;
        letter-spacing: 1px;
        direction: ltr;
        text-align: left;
    }
    .copy-button {
        background: #17a2b8;
        color: white;
        border: none;
        padding: 0.3rem 0.8rem;
        border-radius: 4px;
        cursor: pointer;
        font-size: 0.9rem;
        transition: all 0.3s ease;
    }
    .copy-button:hover {
        background: #138496;
        transform: scale(1.05);
    }
    .error-box {
        background: linear-gradient(135deg, #ffe6e6 0%, #ffcccc 100%);
        border: 3px solid #f44336;
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        direction: rtl;
        box-shadow: 0 8px 32px rgba(244, 67, 54, 0.2);
        position: relative;
    }
    .error-box::before {
        content: '⚠️';
        position: absolute;
        top: 1rem;
        right: 1rem;
        font-size: 2rem;
        opacity: 0.7;
    }
    .stButton > button {
        background: linear-gradient(90deg, #4CAF50, #45a049);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.8rem 2rem;
        font-size: 1.2rem;
        direction: rtl;
        font-weight: bold;
        box-shadow: 0 4px 16px rgba(76, 175, 80, 0.3);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
    }
    .input-section {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border: 1px solid #e0e0e0;
    }
    .success-icon {
        color: #4CAF50;
        font-size: 2rem;
        animation: bounce 1s infinite;
    }
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        60% { transform: translateY(-5px); }
    }
    .info-card {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-right: 5px solid #3498db;
        direction: rtl;
        color: white;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    }
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-left: 8px;
    }
    .status-success { background-color: #4CAF50; }
    .status-warning { background-color: #ff9800; }
    .status-error { background-color: #f44336; }
</style>
""", unsafe_allow_html=True)

def install_playwright_browsers():
    """Install Playwright browsers automatically"""
    try:
        st.info("در حال نصب مرورگر Chromium...")
        
        # Install Playwright browsers
        result = subprocess.run(
            ["python", "-m", "playwright", "install", "chromium"], 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            st.success("✅ مرورگر Chromium با موفقیت نصب شد!")
            return True
        else:
            st.error(f"خطا در نصب مرورگر: {result.stderr}")
            return False
            
    except Exception as e:
        st.error(f"خطا در نصب مرورگر: {str(e)}")
        return False

def check_playwright_installation():
    """Check if Playwright browsers are installed"""
    try:
        result = subprocess.run(
            ["python", "-m", "playwright", "install-deps"], 
            capture_output=True, 
            text=True
        )
        return True
    except:
        return False

async def automate_iban_to_deposit(iban_number, headless=False):
    """Automate IBAN to deposit conversion using Playwright"""
    try:
        async with async_playwright() as p:
            # Launch browser with better settings
            browser = await p.chromium.launch(
                headless=headless,
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-web-security",
                    "--disable-features=VizDisplayCompositor"
                ],
                slow_mo=1000 if not headless else 0  # Slow down for visibility when not headless
            )
            
            # Create new page
            page = await browser.new_page()
            
            # Set viewport
            await page.set_viewport_size({"width": 1920, "height": 1080})
            
            # Navigate to the IBAN to deposit URL
            url = "https://vbank.bpi.ir/public/inquiries/iban-to-deposit"
            st.info(f"🌐 در حال اتصال به: {url}")
            await page.goto(url, wait_until="networkidle")
            
            # Wait for page to load
            await page.wait_for_timeout(3000)
            st.info("⏳ صفحه بارگذاری شد، در حال جستجوی فیلد ورودی...")
            
            # Find the IBAN input field using multiple selectors
            input_field = None
            input_selectors = [
                "input[name='destSheba_part_1']",
                "input[id='destSheba_part_1']",
                "#destSheba_part_1",
                "input[maxlength='24']",
                "account-number-cmp input[type='tel']",
                "section input[type='tel']",
                ".card-input input[type='tel']",
                "input[persiantoenglishnumber]",
                "input[onlynumber='true']"
            ]
            
            for selector in input_selectors:
                try:
                    input_field = await page.wait_for_selector(selector, timeout=5000)
                    if await input_field.is_visible():
                        st.info(f"✅ فیلد ورودی با selector '{selector}' یافت شد")
                        break
                except:
                    continue
            
            if not input_field:
                await browser.close()
                return None, "فیلد ورودی شماره شبا یافت نشد"
            
            # Clear the input field using proper Playwright methods
            st.info("🧹 در حال پاک کردن فیلد ورودی...")
            await input_field.click()
            await page.keyboard.press("Control+a")  # Select all
            await page.keyboard.press("Delete")     # Delete selected text
            await page.wait_for_timeout(1000)
            
            # Enter the IBAN number
            st.info(f"⌨️ در حال وارد کردن شماره شبا: {iban_number}")
            await input_field.fill(iban_number)
            await page.wait_for_timeout(2000)
            
            # Find and click the convert button
            submit_button = None
            submit_selectors = [
                "input[value='تبدیل']",
                "input[type='button'][value='تبدیل']",
                ".btn.btn-success",
                "button:has-text('تبدیل')",
                "input:has-text('تبدیل')",
                "[value='تبدیل']"
            ]
            
            for selector in submit_selectors:
                try:
                    submit_button = await page.wait_for_selector(selector, timeout=5000)
                    if await submit_button.is_visible():
                        st.info(f"✅ دکمه تبدیل با selector '{selector}' یافت شد")
                        break
                except:
                    continue
            
            if not submit_button:
                await browser.close()
                return None, "دکمه تبدیل یافت نشد"
            
            # Click the convert button
            st.info("🔄 در حال کلیک روی دکمه تبدیل...")
            await submit_button.click()
            
            # Wait for results to load
            st.info("⏳ در انتظار نتایج...")
            await page.wait_for_timeout(5000)
            
            # Try to find the success modal or result
            result_text = ""
            result_selectors = [
                ".modal.modal-wrapper2.in .modal-body",
                ".receipt-container",
                ".content-row-content",
                ".modal-body",
                ".panel-wrapper",
                "div:has-text('شماره سپرده')",
                ".content-row:has-text('شماره سپرده') .content-row-content"
            ]
            
            for selector in result_selectors:
                try:
                    result_element = await page.wait_for_selector(selector, timeout=5000)
                    if result_element:
                        element_text = await result_element.text_content()
                        if element_text and element_text.strip():
                            result_text += element_text.strip() + "\n"
                            st.info(f"✅ نتیجه با selector '{selector}' یافت شد")
                except:
                    continue
            
            # Enhanced result extraction - get all content from modal
            if not result_text or not result_text.strip():
                try:
                    # Look for the modal content more broadly
                    modal_selectors = [
                        ".modal-body",
                        ".receipt-container",
                        ".panel-wrapper.clearfix",
                        ".content-row"
                    ]
                    
                    for selector in modal_selectors:
                        try:
                            elements = await page.query_selector_all(selector)
                            for element in elements:
                                text = await element.text_content()
                                if text and text.strip():
                                    result_text += text.strip() + "\n"
                        except:
                            continue
                    
                    # Also try to get specific fields
                    field_selectors = [
                        ".content-row-caption",
                        ".content-row-content"
                    ]
                    
                    for selector in field_selectors:
                        try:
                            elements = await page.query_selector_all(selector)
                            for element in elements:
                                text = await element.text_content()
                                if text and text.strip():
                                    result_text += text.strip() + " "
                        except:
                            continue
                            
                except Exception as e:
                    st.warning(f"خطا در استخراج نتیجه: {str(e)}")
            
            # If still no result, get page content for debugging
            if not result_text or not result_text.strip():
                try:
                    # Check if success message exists
                    success_message = await page.query_selector("h3:has-text('موفقیت')")
                    if success_message:
                        result_text = "تبدیل با موفقیت انجام شد اما جزئیات نتیجه استخراج نشد.\n"
                        
                        # Try to get all visible text
                        body_text = await page.text_content("body")
                        lines = body_text.split('\n')
                        relevant_lines = []
                        for line in lines:
                            line = line.strip()
                            if any(keyword in line for keyword in ['شماره سپرده', 'شماره شبا', '361', 'IR380570', 'نام', 'خانوادگی']):
                                relevant_lines.append(line)
                        
                        if relevant_lines:
                            result_text += '\n'.join(relevant_lines[:10])
                    else:
                        result_text = "عملیات انجام شد اما نتیجه‌ای یافت نشد"
                except:
                    result_text = "خطا در استخراج نتیجه"
            
            st.info("✅ عملیات تکمیل شد، در حال بستن مرورگر...")
            await browser.close()
            return result_text.strip(), None
            
    except Exception as e:
        return None, f"خطا در اجرای عملیات: {str(e)}"

def run_automation(iban_number, headless=False):
    """Wrapper to run async automation function"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(automate_iban_to_deposit(iban_number, headless))
    except Exception as e:
        return None, f"خطا در اجرای عملیات: {str(e)}"

def display_result(result_text, iban_input):
    """Display the automation result using Streamlit components"""
    if not result_text:
        st.error("❌ نتیجه‌ای دریافت نشد")
        return
    
    # Extract deposit number and other info from result
    deposit_number = ""
    iban_number = ""
    customer_name = ""
    
    lines = result_text.split('\n')
    for line in lines:
        line = line.strip()
        if 'شماره سپرده' in line:
            if ':' in line:
                deposit_number = line.split(':')[-1].strip()
            else:
                # Look for number after the text
                parts = line.split('شماره سپرده')
                if len(parts) > 1:
                    potential_number = parts[1].strip()
                    if potential_number and any(c.isdigit() for c in potential_number):
                        deposit_number = potential_number
        elif 'شماره شبا' in line:
            if ':' in line:
                iban_number = line.split(':')[-1].strip()
            else:
                # Look for IR number after the text
                parts = line.split('شماره شبا')
                if len(parts) > 1:
                    potential_iban = parts[1].strip()
                    if 'IR' in potential_iban:
                        iban_number = potential_iban
        elif any(name_keyword in line for name_keyword in ['نام و نام خانوادگی', 'نام خانوادگی', 'نام صاحب']):
            if ':' in line:
                customer_name = line.split(':')[-1].strip()
            else:
                # Look for name after the keyword
                for keyword in ['نام و نام خانوادگی', 'نام خانوادگی', 'نام صاحب']:
                    if keyword in line:
                        parts = line.split(keyword)
                        if len(parts) > 1:
                            potential_name = parts[1].strip()
                            if potential_name and not any(c.isdigit() for c in potential_name):
                                customer_name = potential_name
                                break
        elif line and any(char in line for char in ['361', '.']) and len(line) > 10 and not deposit_number:
            # Try to extract deposit number from unstructured text
            if '361' in line and not any(keyword in line for keyword in ['شماره شبا', 'IR']):
                deposit_number = line.strip()
    
    # If no structured data found, look for patterns
    if not deposit_number:
        import re
        # Look for deposit pattern like 361.8100.16016016.1
        deposit_pattern = r'361[\.\s]*\d+[\.\s]*\d+[\.\s]*\d+'
        match = re.search(deposit_pattern, result_text)
        if match:
            deposit_number = match.group().replace(' ', '')
    
    if not iban_number:
        # Look for IR pattern
        import re
        iban_pattern = r'IR\d{22,24}'
        match = re.search(iban_pattern, result_text)
        if match:
            iban_number = match.group()
        else:
            # Use the input IBAN with IR prefix
            iban_number = f"IR{iban_input}"
    
    # Look for customer name in unstructured text
    if not customer_name:
        # Look for Persian names (words that don't contain numbers or special chars)
        import re
        lines = result_text.split('\n')
        for line in lines:
            line = line.strip()
            # Skip lines with numbers, IBAN, or deposit info
            if not any(keyword in line for keyword in ['شماره', 'IR', '361', ':', 'تبدیل', 'موفقیت']):
                # Look for Persian text that could be a name
                persian_text = re.findall(r'[\u0600-\u06FF\s]+', line)
                for text in persian_text:
                    text = text.strip()
                    if len(text) > 3 and len(text) < 50 and ' ' in text:  # Likely a full name
                        customer_name = text
                        break
                if customer_name:
                    break
    
    # Display success message
    st.markdown("""
    <div class="result-box">
        <div class="result-header">
            <span class="success-icon">✅</span>
            تبدیل با موفقیت انجام شد
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display results in organized columns
    if deposit_number or customer_name:
        col1, col2 = st.columns(2)
        
        with col1:
            if deposit_number:
                st.markdown("**شماره سپرده:**")
                st.code(deposit_number, language=None)
                if st.button("📋 کپی شماره سپرده", key="copy_deposit"):
                    st.success("شماره سپرده کپی شد!")
        
        with col2:
            if iban_number:
                st.markdown("**شماره شبا:**")
                st.code(iban_number, language=None)
                if st.button("📋 کپی شماره شبا", key="copy_iban"):
                    st.success("شماره شبا کپی شد!")
        
        if customer_name:
            st.markdown("**نام صاحب حساب:**")
            st.info(f"👤 {customer_name}")
        
        # Show raw result for debugging
        with st.expander("🔍 مشاهده جزئیات کامل"):
            st.text_area("نتیجه خام:", value=result_text, height=200, disabled=True)
    else:
        # Show raw result if no structured data found
        st.markdown("**نتیجه:**")
        st.text_area("", value=result_text, height=150, disabled=True)
    
    st.success("💡 عملیات با موفقیت تکمیل شد!")

def main():
    # Header
    st.markdown('<h1 class="main-header">🏦 تبدیل شماره شبا به سپرده - بانک پاسارگاد</h1>', unsafe_allow_html=True)
    
    # Show environment info
    env_info = f"محیط: {platform.system()}"
    st.sidebar.info(env_info)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="service-card"><h3>تبدیل شماره شبا به شماره سپرده</h3></div>', unsafe_allow_html=True)
        
        # Input field for IBAN number
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        st.markdown("### 📝 ورود اطلاعات")
        
        # Add headless option
        col_input, col_headless = st.columns([3, 1])
        with col_input:
            iban_input = st.text_input(
                "شماره شبا:",
                placeholder="123456789012345678901234",
                help="شماره شبا 24 رقمی را بدون IR وارد کنید",
                max_chars=24
            )
        with col_headless:
            st.markdown("<br>", unsafe_allow_html=True)  # Add spacing
            headless_mode = st.checkbox("مرورگر مخفی", value=False, help="اگر فعال باشد، مرورگر نمایش داده نمی‌شود")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Submit button
        if st.button("🚀 تبدیل شبا به سپرده", use_container_width=True):
            if iban_input:
                if len(iban_input) != 24:
                    st.warning("⚠️ شماره شبا باید دقیقاً 24 رقم باشد")
                elif not iban_input.isdigit():
                    st.warning("⚠️ شماره شبا باید فقط شامل اعداد باشد")
                else:
                    with st.spinner("در حال پردازش... لطفاً صبر کنید"):
                        result, error = run_automation(iban_input, headless_mode)
                        
                        if error:
                            st.markdown(f'<div class="error-box"><h4>❌ خطا در عملیات</h4><p>{error}</p></div>', unsafe_allow_html=True)
                            
                            # Show browser installation option if needed
                            if "playwright" in error.lower() or "browser" in error.lower():
                                if st.button("🔧 نصب مرورگر Chromium"):
                                    install_playwright_browsers()
                                    st.experimental_rerun()
                        else:
                            # Parse and format the result beautifully
                            display_result(result, iban_input)
            else:
                st.warning("لطفاً شماره شبا را وارد کنید.")
    
    with col2:
        st.markdown("### 📋 راهنمای استفاده")
        st.markdown("""
        <div class="info-card">
        <strong>مراحل استفاده:</strong><br>
        1️⃣ شماره شبا 24 رقمی را وارد کنید<br>
        2️⃣ دکمه تبدیل را بزنید<br>
        3️⃣ منتظر نتیجه بمانید<br><br>
        
        <strong>نکات مهم:</strong><br>
        ✅ شماره شبا باید 24 رقم باشد<br>
        ✅ IR را وارد نکنید<br>
        ✅ فقط اعداد وارد کنید<br>
        ✅ اتصال اینترنت لازم است<br><br>
        
        <strong>مثال:</strong><br>
        <code style="background: #f0f0f0; padding: 5px; border-radius: 3px;">380570036181016016016101</code>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🔧 وضعیت سیستم")
        
        # System status with indicators
        st.markdown("""
        <div class="info-card">
        <div style="display: flex; align-items: center; margin: 0.5rem 0;">
            <span class="status-indicator status-success"></span>
            <strong>Streamlit آماده</strong>
        </div>
        <div style="display: flex; align-items: center; margin: 0.5rem 0;">
            <span class="status-indicator status-success"></span>
            <strong>Playwright آماده</strong>
        </div>
        """, unsafe_allow_html=True)
        
        # Check Playwright installation
        if check_playwright_installation():
            st.markdown("""
            <div style="display: flex; align-items: center; margin: 0.5rem 0;">
                <span class="status-indicator status-success"></span>
                <strong>مرورگر Chromium آماده</strong>
            </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="display: flex; align-items: center; margin: 0.5rem 0;">
                <span class="status-indicator status-warning"></span>
                <strong>مرورگر نصب نشده</strong>
            </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🔧 نصب مرورگر"):
                install_playwright_browsers()
                st.experimental_rerun()
        
        if st.button("🧪 تست اتصال"):
            with st.spinner("در حال تست..."):
                try:
                    result, error = run_automation("380570036181016016016101", False)  # Always show browser for test
                    if not error:
                        st.success("✅ اتصال به سایت موفق")
                    else:
                        st.error("❌ خطا در اتصال")
                        if st.button("🔧 نصب مرورگر Chromium"):
                            install_playwright_browsers()
                            st.experimental_rerun()
                except:
                    st.error("❌ خطا در تست اتصال")

if __name__ == "__main__":
    main()
