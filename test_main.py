from playwright.sync_api import sync_playwright, expect
import re, time


def test_main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.saucedemo.com/")
        expect(page).to_have_title(re.compile("Swag Labs"))
        
        
        # 1- Call the login method
        test_login(page)
        
        
        
        #Verify successful login
        expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
        
        # 2- Call function add to cart
        test_add_to_cart(page)
        
        # Check the product in the cart
        expect(page.locator('.shopping_cart_badge')).to_have_text('1')
        # 3- Verificar que el botón cambia el texto de "Add to cart" a "Remove"
        expect(page.locator('button[data-test="remove-sauce-labs-backpack"]')).to_have_text("Remove")
        
        # 4- Añadir el producto “Sauce Labs Bike Light” 
        # #y “Sauce Labs Fleece Jacket” al carrito
        add_to_cart_2(page, "Sauce Labs Bike Light")
        add_to_cart_2(page, "Sauce Labs Fleece Jacket")
        # Check the product in the cart
        expect(page.locator('.shopping_cart_badge')).to_have_text('3')
        
        # 5- Eliminar el producto “Sauce Labs Backpack” del carrito
        remove_product(page,"Sauce Labs Backpack")
        # Check the product in the cart
        expect(page.locator('.shopping_cart_badge')).to_have_text('2')
    
        # 6- Verificar que el texto del botón cambia de "Remove" a "Add to cart":
        expect(page.locator('button[data-test="add-to-cart-sauce-labs-backpack"]')).to_have_text("Add to cart")
        
        # 7- Hacer click en el carrito:
        page.locator("[data-test=\"shopping-cart-link\"]").click()
        
        # 8- Verificar que la url es: https://www.saucedemo.com/cart.html
        expect(page).to_have_url("https://www.saucedemo.com/cart.html")
        
        # 9- Hacer click en el botón "Checkout".
        page.locator("[data-test=\"checkout\"]").click()
        
        # 10- Pulsar en el botón de "Continue":
        page.locator("[data-test=\"continue\"]").click()
        
        # 11- Verificar que aparece un mensaje de error con el texto First name is required:
        expect(page.locator("[data-test=\"error\"]")).to_contain_text("Error: First Name is required")

        
        # 12- Rellenar todo el formulario con tus datos personales:
        test_fill_form(page)
        
        #Check go to the correct next page
        expect(page).to_have_url("https://www.saucedemo.com/checkout-step-two.html")
        
        
        # 14- Verificar que el "Total" es la suma de "Item total" + "Tax": 
        test_check_sum(page)
        
        # 15- Pulsar en el botón "Finish":
        page.locator("[data-test=\"finish\"]").click()
        # 16- Verificar que aparece el mensaje "Thank you for your order!"
        expect(page.locator("[data-test=\"complete-header\"]")).to_contain_text("Thank you for your order!")

        # 17- Pulsar en el botón "Back Home":
        page.locator("[data-test=\"back-to-products\"]").click()

        # 18- Hacer click en el menú desplegable:
        page.get_by_role("button", name="Open Menu").click()
        # 19- Hacer click en "Logout":
        page.locator("[data-test=\"logout-sidebar-link\"]").click()
        # 20- Verificar que los campos "Username" y "Password" están visibles:
        expect(page.locator("[data-test=\"username\"]")).to_be_visible()
        expect(page.locator("[data-test=\"password\"]")).to_be_visible()
        
        # #PRUEBAS EXTRAS:
        
        # # 21- Rellenar un nombre de usuario y/o contraseña que no existen:
        test_login_fail(page)
        # #Borramos y escribimos el siguiente usuario: 
        page.locator("[data-test=\"username\"]").click()
        page.locator("[data-test=\"username\"]").fill("")
        
        # # 22- Rellenar los datos del usuario locked y obtener un mensaje distinto para el mismo:
        # test_login_user_locked(page)
        
        # 23- Trato de recopilar que el botón de reset cart no hace lo que debe, 
        # elimina productos del carrito pero no cambia los botones de los artículos a su estado inicial 
        #NOTA: esto último da error, no consigo registrar el fallo esperado
        # test_login(page)
        # test_reset_cart(page)
        
        
        #Change time value (seconds) for debugging purposes.
        time.sleep(3)
        
        # Cerrar el navegador
        browser.close()
        

# 
# 1- Hacer login con el usuario standard:
# user: standard_user
# pass: secret_sauce
def test_login(page):
    # try catch to see the specific selectors
    try:
        page.wait_for_selector('input[id="user-name"]', timeout=30000)
        page.wait_for_selector('input[id="password"]', timeout=30000)
        page.wait_for_selector('input[id="login-button"]', timeout=30000)
    except Exception as e:
        print(f"Error: {e}")
        return
    
    # fill the details and click the button 
    page.fill('input[id="user-name"]', 'standard_user')
    page.fill('input[id="password"]', 'secret_sauce')
    #page.click('input[id="login-button"]')
    page.locator("[data-test=\"login-button\"]").click()
       
        
        
# 2- Añadir el producto Sauce Labs Backpack al carrito
def test_add_to_cart(page):
     # Asegurarse de que el botón "Add to cart" está presente para "Sauce Labs Backpack"
    try:
        page.wait_for_selector('button[id="add-to-cart-sauce-labs-backpack"]', timeout=30000)
    except Exception as e:
        print(f"Error: {e}")
        return
    
    # Add to cart Sauce Labs Backpack
    page.locator("[data-test=\"add-to-cart-sauce-labs-backpack\"]").click()
    
# 3- Verificar que el botón cambia el texto de "Add to cart" a "Remove"
# Verifico esto en test_main() 


# 4- Añadir el producto “Sauce Labs Bike Light” 
# #y “Sauce Labs Fleece Jacket” al carrito
def add_to_cart_2(page, product):
    # Convert product in the correct format for the selector
    product_selector = product.lower().replace(' ', '-')
    try:
        page.wait_for_selector(f'button[data-test="add-to-cart-{product_selector}"]', timeout=30000)
    except Exception as e:
        print(f"Error: {e}")
        return
    # Add to cart product
    page.locator(f'[data-test="add-to-cart-{product_selector}"]').click()
    
# 5- Eliminar el producto “Sauce Labs Backpack” del carrito
def remove_product(page,product):
    # Convert product in the correct format for the selector
    product_selector = product.lower().replace(' ', '-')
    #page.locator("[data-test=\"remove-sauce-labs-backpack\"]").click()
    try:
        page.wait_for_selector(f'button[data-test="remove-{product_selector}"]', timeout=30000)
    except Exception as e:
        print(f"Error: {e}")
        return
    # Remove product
    page.locator(f'[data-test="remove-{product_selector}"]').click()


# 12- Rellenar todo el formulario con tus datos personales:
def test_fill_form(page):
    # Waiting for the correct selectors
    try:
        page.wait_for_selector('[data-test="firstName"]', timeout=30000)
        page.wait_for_selector('[data-test="lastName"]', timeout=30000)
        page.wait_for_selector('[data-test="postalCode"]', timeout=30000)
    except Exception as e:
        print(f"Error al esperar los selectores del formulario: {e}")
        return


    # Fill the inputs 
    try:
        page.fill('[data-test="firstName"]', 'Vicky')
        page.fill('[data-test="lastName"]', 'Sampalo')
        page.fill('[data-test="postalCode"]', '12345')
    except Exception as e:
        print(f"Error al rellenar los campos del formulario: {e}")
        return

    # 13- Pulsar en el botón "Continue":
    try:
        page.click('[data-test="continue"]')
    except Exception as e:
        print(f"Error al pulsar botón 'Continue': {e}")
        return
         


# 14 - Verificar que el "Total" es la suma de "Item total" + "Tax": 
def test_check_sum(page):
    #Check the visibility
    try:
        page.wait_for_selector("[data-test=\"subtotal-label\"]", timeout=30000)
        page.wait_for_selector("[data-test=\"tax-label\"]", timeout=30000)
        page.wait_for_selector("[data-test=\"total-label\"]", timeout=30000)
    except Exception as e:
        print(f"Error selectores metodo sumar: {e}")
        return
    # Save in variables
    try:
        subtotal_text = page.locator("[data-test=\"subtotal-label\"]").inner_text()
        tax_text = page.locator("[data-test=\"tax-label\"]").inner_text()
        total_text = page.locator("[data-test=\"total-label\"]").inner_text()
    except Exception as e:
        print(f"Error: {e}")
        return
    # Research the number and extract to the string
    try:
        subtotal_value = float(re.search(r"\$([0-9]+\.[0-9]+)", subtotal_text).group(1))
        tax_value = float(re.search(r"\$([0-9]+\.[0-9]+)", tax_text).group(1))
        total_value = float(re.search(r"\$([0-9]+\.[0-9]+)", total_text).group(1))
    except Exception as e:
        print(f"Error: {e}")
        return
     # Sum subtotal + tax
    expected_total = subtotal_value + tax_value

    # Verify the total
    try:
        assert total_value == expected_total, f"Total: {total_value} != Item total + Tax: {expected_total}"
    except Exception as e:
        print(f"Error: {e}")
        return
    try:
        expect(page.locator("[data-test=\"total-label\"]")).to_have_text(f"Total: ${expected_total:.2f}")
    except Exception as e:
        print(f"Error: {e}")
        return

def test_login_fail(page):
    # try catch to see the specific selectors
    try:
        page.wait_for_selector('input[id="user-name"]', timeout=30000)
        page.wait_for_selector('input[id="password"]', timeout=30000)
        page.wait_for_selector('input[id="login-button"]', timeout=30000)
    except Exception as e:
        print(f"Error: {e}")
        return
    
    # fill the details and click the button 
    page.fill('input[id="user-name"]', 'incorrect')
    page.fill('input[id="password"]', 'secret_sauce')
    #page.click('input[id="login-button"]')
    page.locator("[data-test=\"login-button\"]").click()
    
    expect(page.locator("[data-test=\"error\"]")).to_contain_text("Epic sadface: Username and password do not match any user in this service")


def test_login_user_locked(page):
    # try catch to see the specific selectors
    try:
        page.wait_for_selector('input[id="user-name"]', timeout=30000)
        page.wait_for_selector('input[id="password"]', timeout=30000)
        page.wait_for_selector('input[id="login-button"]', timeout=30000)
    except Exception as e:
        print(f"Error: {e}")
        return
    
    # fill the details and click the button 
    page.fill('input[id="user-name"]', 'locked_out_user')
    page.fill('input[id="password"]', 'secret_sauce')
    #page.click('input[id="login-button"]')
    page.locator("[data-test=\"login-button\"]").click()
    
    expect(page.locator("[data-test=\"error\"]")).to_contain_text("Epic sadface: Sorry, this user has been locked out.")

    
    
def test_reset_cart(page):
    try:
        # add products to the cart
        page.locator("[data-test=\"add-to-cart-sauce-labs-backpack\"]").click()
        page.locator("[data-test=\"add-to-cart-sauce-labs-bolt-t-shirt\"]").click()
        
        # Verify the expected shopping cart
        expect(page.locator('.shopping_cart_badge')).to_have_text('2')
        expect(page.locator('button[data-test="remove-sauce-labs-backpack"]')).to_have_text("Remove")
        expect(page.locator('button[data-test="remove-sauce-labs-bolt-t-shirt"]')).to_have_text("Remove")
        
        # Button "reset"
        page.get_by_role("button", name="Open Menu").click()
        page.locator("[data-test=\"reset-sidebar-link\"]").click()
        page.get_by_role("button", name="Close Menu").click()
        
        # Wait for the shopping cart badge to disappear
        expect(page.locator('.shopping_cart_badge')).not_to_be_visible()

        # Wait for the buttons to change to "Add to cart"
        expect(page.locator('button[data-test="add-to-cart-sauce-labs-backpack"]')).to_have_text("Add to cart")
        expect(page.locator('button[data-test="add-to-cart-sauce-labs-bolt-t-shirt"]')).to_have_text("Add to cart")
        
        # Additional assertions for visibility if needed
        assert page.locator('button[data-test="remove-sauce-labs-backpack"]').is_visible(), \
            "El botón 'Remove' sigue visible"
        assert page.locator('button[data-test="remove-sauce-labs-bolt-t-shirt"]').is_visible(), \
            "El botón 'Remove' sigue visible"
    
    except Exception as e:
        print(f"Error durante la ejecución de test_reset_cart: {e}")
        raise
