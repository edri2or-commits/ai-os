# Judge Agent - Full Automation with Selenium (Improved)
# This script opens n8n in browser, connects workflow to credential, and activates it

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def activate_judge_agent():
    print("=== Judge Agent - Full Browser Automation ===")
    print("")
    
    # Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--start-maximized')
    
    print("Step 1: Starting Chrome browser...")
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 30)  # Increased timeout
    
    try:
        # Step 2: Open n8n
        print("Step 2: Opening n8n at http://localhost:5678...")
        driver.get("http://localhost:5678")
        time.sleep(5)  # Wait for n8n to load
        
        print("DEBUG: Taking screenshot of loaded page...")
        driver.save_screenshot("C:\\Users\\edri2\\Desktop\\AI\\ai-os\\temp\\n8n_loaded.png")
        print("Screenshot saved: temp/n8n_loaded.png")
        
        # Step 3: Try multiple selectors for Workflows link
        print("Step 3: Navigating to Workflows...")
        
        # Try different selectors
        selectors = [
            "//a[contains(@href, 'workflows')]",
            "//a[contains(text(), 'Workflows')]",
            "//*[contains(text(), 'Workflows')]",
            "//button[contains(text(), 'Workflows')]",
            "//*[@class='el-menu-item' and contains(text(), 'Workflows')]"
        ]
        
        workflows_link = None
        for selector in selectors:
            try:
                print(f"Trying selector: {selector}")
                workflows_link = wait.until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                print(f"SUCCESS: Found workflows link with selector: {selector}")
                break
            except:
                continue
        
        if not workflows_link:
            # Try direct URL
            print("Trying direct URL navigation...")
            driver.get("http://localhost:5678/workflows")
            time.sleep(3)
        else:
            workflows_link.click()
            time.sleep(3)
        
        print("DEBUG: Taking screenshot after navigation...")
        driver.save_screenshot("C:\\Users\\edri2\\Desktop\\AI\\ai-os\\temp\\workflows_page.png")
        
        # Step 4: Find Judge Agent workflow
        print("Step 4: Finding 'Judge Agent' workflow...")
        
        # Try multiple selectors
        judge_selectors = [
            "//*[contains(text(), 'Judge Agent')]",
            "//div[contains(text(), 'Judge Agent')]",
            "//span[contains(text(), 'Judge Agent')]",
            "//a[contains(text(), 'Judge Agent')]"
        ]
        
        judge_workflow = None
        for selector in judge_selectors:
            try:
                print(f"Trying selector: {selector}")
                judge_workflow = wait.until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                print(f"SUCCESS: Found workflow with selector: {selector}")
                break
            except:
                continue
        
        if not judge_workflow:
            raise Exception("Could not find Judge Agent workflow")
        
        judge_workflow.click()
        time.sleep(5)
        
        print("DEBUG: Taking screenshot of workflow...")
        driver.save_screenshot("C:\\Users\\edri2\\Desktop\\AI\\ai-os\\temp\\workflow_open.png")
        
        # Step 5: Find and click on the OpenAI HTTP Request node
        print("Step 5: Looking for OpenAI node...")
        
        # n8n nodes are usually in SVG or specific divs
        node_selectors = [
            "//*[contains(@class, 'node')]",
            "//*[contains(@class, 'nodeView')]",
            "//*[name()='g' and contains(@class, 'node')]",
            "//div[contains(@class, 'node-wrapper')]"
        ]
        
        for selector in node_selectors:
            try:
                print(f"Trying node selector: {selector}")
                nodes = driver.find_elements(By.XPATH, selector)
                print(f"Found {len(nodes)} nodes")
                if nodes:
                    # Click first node (likely HTTP Request)
                    nodes[0].click()
                    time.sleep(2)
                    break
            except Exception as e:
                print(f"Failed with selector {selector}: {e}")
                continue
        
        print("DEBUG: Taking screenshot after clicking node...")
        driver.save_screenshot("C:\\Users\\edri2\\Desktop\\AI\\ai-os\\temp\\node_clicked.png")
        
        # Step 6: At this point, we need manual intervention
        print("")
        print("=== PARTIALLY AUTOMATED ===")
        print("")
        print("Browser is open with Judge Agent workflow.")
        print("Screenshot saved in temp/ folder for debugging.")
        print("")
        print("Manual steps remaining:")
        print("1. Click on the HTTP Request (OpenAI) node")
        print("2. In the right panel, find 'Credential' dropdown")
        print("3. Select 'Judge Agent OpenAI'")
        print("4. Click 'Save'")
        print("5. Toggle 'Active' at the top")
        print("")
        print("Browser will close in 60 seconds...")
        print("Press Ctrl+C to keep it open longer.")
        
        time.sleep(60)
        
    except KeyboardInterrupt:
        print("\nBrowser kept open by user.")
        input("Press Enter to close browser...")
        
    except Exception as e:
        print(f"ERROR: {e}")
        print("")
        print("Troubleshooting:")
        print("1. Check screenshots in temp/ folder")
        print("2. Make sure n8n is running: http://localhost:5678")
        print("3. Verify workflow exists: 'Judge Agent - Faux Pas Detection'")
        print("4. Verify credential exists: 'Judge Agent OpenAI'")
        print("")
        driver.save_screenshot("C:\\Users\\edri2\\Desktop\\AI\\ai-os\\temp\\error_screenshot.png")
        print("Error screenshot saved: temp/error_screenshot.png")
        
    finally:
        print("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    activate_judge_agent()
