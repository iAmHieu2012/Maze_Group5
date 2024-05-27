import pygame
import json
import pygame.mixer as mixer

# Hàm để đọc dữ liệu từ tệp JSON
def read_accounts_from_json(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return {}  # Return an empty dictionary if the file is not found
    except json.JSONDecodeError:
        return {}  # Return an empty dictionary if there's an error parsing the JSON

# Hàm để kiểm tra tài khoản đăng nhập hoặc đăng kí có tồn tại trong file json trước đó hay không
def check_account(username, password, accounts):
    if username in accounts.keys():
        if accounts[username] == password:
            return True
    return False

# Hàm để kiểm tra username có tồn tại trong file json trước đó hay không
def check_username(username, password, accounts):
    if username in accounts.keys():
        return True
    return False

# Hàm thêm tài khoản đăng kí
def add_account(filename, username, password):
    data = read_accounts_from_json(filename)
    data[username] = password
    with open(filename, "w") as f:
        json.dump(data, f, indent = 4)

def login():
    # Định nghĩa màu sắc
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    DARK_RED = (139, 0, 0)  # Màu Dark Red
    YELLOW = (255, 255, 204)
    DARK_TEAL_ACCENT_1_DARKER_25 = (0, 63, 92)  # Màu Dark Teal, Accent 1, Darker 25%
    DARK_GREEN_ACCENT_3_DARKER_25 = (0, 73, 48)  # Màu Dark Green, Accent 3, Darker 25%

    # Tải ảnh nền
    background_image = pygame.image.load('img/background2.jpg')

    # Tải nhạc nền và phát lặp lại
    mixer.music.load('sound/login_music.mp3')
    mixer.music.play(-1)  # -1 để phát lặp lại liên tục

    # tải âm thanh khi click chuột và khi nhấn phím
    click_sound = mixer.Sound('sound/click.mp3')
    key_sound = mixer.Sound("sound/key.wav")

    # Tạo font chữ
    font_1 = pygame.font.Font("font/Shermlock.ttf", 50)
    font_2 = pygame.font.Font("font/Shermlock.ttf", 32)
    font_3 = pygame.font.Font("font/Shermlock.ttf", 24)
    font_4 = pygame.font.Font("font/Shermlock.ttf", 36)

    # Biến lưu trữ tên người dùng
    username_input = ""
    password_input = ""

    # Đặt cờ hiệu input hiện tại là username hay là password
    current_input = "None"

    # đặt cờ hiệu flag, nếu đăng nhập sai thì đổi thành false
    flag = None

    # Biến xác định vị trí ô vuông bên cạnh username, ô vuông bên cạnh password, ô Login và ô Reset
    username_rect = pygame.Rect(550, screen_height // 2 - font_2.get_height() // 2 - 80, 300, font_2.get_height() + 60) #username thuộc font_2 
    password_rect = pygame.Rect(550, screen_height // 2 - font_2.get_height() // 2 - 5, 300, font_2.get_height() + 60) #password thuộc font_2
    Login_rect = pygame.Rect(430, screen_height // 2 - font_3.get_height() // 2 + 140, 100, font_3.get_height() + 10) #Login thuộc font_3
    Reset_rect = pygame.Rect(530, screen_height // 2 - font_3.get_height() // 2 + 140, 100, font_3.get_height() + 10) #reset thuộc font_3
    createnewaccount_rect = pygame.Rect(480, screen_height // 2 - font_1.get_height() // 2 + 250, 230, font_2.get_height() + 10) #reset thuộc font_3

    # Hàm kiểm tra xem chuột có nằm trong ô vuông bên cạnh username hay không
    def is_over_username_box(mouse_pos):
        return username_rect.collidepoint(mouse_pos)
    # Hàm kiểm tra xem chuột có nằm trong ô vuông bên cạnh password hay không
    def is_over_password_box(mouse_pos):
        return password_rect.collidepoint(mouse_pos)
    # Hàm kiểm tra xem chuột có nằm trong ô Login hay không
    def is_over_Login_box(mouse_pos):
        return Login_rect.collidepoint(mouse_pos)
    # Hàm kiểm tra xem chuột có nằm trong ô Reset hay không
    def is_over_Reset_box(mouse_pos):
        return Reset_rect.collidepoint(mouse_pos)
    def is_over_CreateNewAccount_box(mouse_pos):
        return createnewaccount_rect.collidepoint(mouse_pos)

    blink_timer = 0
    blink_interval = 60  # Điều chỉnh khoảng thời gian nhấp nháy

    loginBox = pygame.image.load("img/LoginSignupBox.png").convert_alpha()
    loginBox = pygame.transform.scale(loginBox,(loginBox.get_width()+200, loginBox.get_height()+100))
    loginBox_rect = loginBox.get_rect()
    loginBox_rect.center = (screen_width // 2, screen_height//2)
    
    inputBox = pygame.image.load("img/Input.png").convert_alpha()
    inputBox = pygame.transform.scale(inputBox, (300, (font_2.get_height() + 60)))

    button = pygame.image.load("img/modebox.png").convert_alpha()
    button = pygame.transform.scale(button, (100, font_3.get_height()+10))
    button_pressed = pygame.image.load("img/modeboxpressed.png").convert_alpha()
    button_pressed = pygame.transform.scale(button_pressed, (100, font_3.get_height()+10))
    # Vòng lặp chính
    running = True
    while running:
        # Cập nhật timer của dấu nháy
        blink_timer += 1
        if blink_timer >= blink_interval:
            blink_timer = 0

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Thoát khỏi pygame khi nhấn nút tắt màn hình
                quit()  # Thoát khỏi chương trình
            # Bắt sự kiện nhấp chuột
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Kiểm tra xem chuột có nằm trong ô vuông bên cạnh username hay không
                if is_over_username_box(mouse_pos):
                    click_sound.play()
                    current_input = "username"
                if is_over_password_box(mouse_pos):
                    click_sound.play()
                    current_input = "password"
                if is_over_Reset_box(mouse_pos):
                    click_sound.play()
                    username_input = ""
                    password_input = ""
                    current_input = "None"
                if is_over_CreateNewAccount_box(mouse_pos):
                    click_sound.play()
                    mixer.music.stop()
                    return sign_up()
                if is_over_Login_box(mouse_pos):
                    click_sound.play()
                    filename = 'accounts.json'
                    # Đọc dữ liệu từ tệp JSON
                    accounts = read_accounts_from_json(filename)
                    # Xử lý sự kiện đăng nhập
                    if check_account(username_input, password_input, accounts):
                        flag = True
                        # khi ráp code thì return ra username_input
                        running = False
                        mixer.music.stop()
                        return username_input
                    else:
                        # Đăng nhập không thành công, đặt cờ hiệu không thành công
                        flag = False
            # Bắt sự kiện nhập văn bản vào ô username or password
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if current_input == "username":
                        key_sound.play()
                        # Nếu nhấn phím backspace, xóa ký tự cuối cùng trong username
                        username_input = username_input[:-1]
                    elif current_input == "password":
                        key_sound.play()
                        # Nếu nhấn phím backspace, xóa ký tự cuối cùng trong password
                        password_input = password_input[:-1]
                elif event.key == pygame.K_RETURN:
                    if current_input != "None":
                        key_sound.play()
                    current_input = "None"
                # phần thêm vào chức năng điều khiển nút up down
                elif event.key == pygame.K_UP:
                    key_sound.play()
                    if current_input == "None":
                        current_input = "password"
                    elif current_input == "username":
                        current_input = "password"
                    elif current_input == "password":
                        current_input = "username"
                elif event.key == pygame.K_DOWN: 
                    key_sound.play()
                    if current_input == "None":
                        current_input = "username"
                    elif current_input == "username":
                        current_input = "password"
                    elif current_input == "password":
                        current_input = "username"                           
                else:
                    if current_input == "username":
                        key_sound.play()
                        if len(username_input) < 20:
                            # Nếu nhấn một phím khác, thêm ký tự đó vào username
                            username_input += event.unicode
                        else:
                            # nếu độ dài bằng 20 thì lấy 20 kí tự cuối cùng
                            username_input += event.unicode
                            username_input = username_input[1:]
                    elif current_input == "password":
                        key_sound.play()
                        if len(password_input) < 20:
                            # Nếu nhấn một phím khác, thêm ký tự đó vào password
                            password_input += event.unicode
                        else:
                            password_input += event.unicode
                            password_input = password_input[1:]                 

        # Tô màu màn hình
        screen.fill(WHITE)
        # Vẽ ảnh nền
        screen.blit(background_image, (0, 0))

        # Render và vẽ các thành phần giao diện
        loginpage = font_1.render("Log in", True, DARK_RED, None)
        if current_input == "None":
            username = font_2.render("Username     ", True, BLACK, None)
            username_width = username.get_width()
            username_input_rendered = font_4.render(username_input, True, BLACK, None)
            password = font_2.render(f"Password     {'*' * len(password_input)}", True, BLACK, None)       
        elif current_input == "username":
            password = font_2.render(f"Password     {'*' * len(password_input)}", True, BLACK, None)
            if blink_timer < blink_interval / 2:
                username = font_2.render("Username     ", True, BLACK, None)
                username_width = username.get_width()
                username_input_rendered = font_4.render(username_input, True, BLACK, None)
            else:
                username = font_2.render("Username     ", True, BLACK, None)
                username_width = username.get_width()
                username_input_rendered = font_4.render(f"{username_input}|", True, BLACK, None)
        elif current_input == "password":
            username = font_2.render("Username    ", True, BLACK, None)
            username_width = username.get_width()
            username_input_rendered = font_4.render(username_input, True, BLACK, None)
            if blink_timer < blink_interval / 2:
                password = font_2.render(f"Password     {'*' * len(password_input)}", True, BLACK, None)
            else:
                password = font_2.render(f"Password     {'*' * len(password_input)}|", True, BLACK, None)

        Login = font_3.render("Login", True, DARK_GREEN_ACCENT_3_DARKER_25, None)
        Reset = font_3.render("Reset", True, DARK_GREEN_ACCENT_3_DARKER_25, None)
        donthaveaccount = font_2.render("Don't have account ?", True, BLACK, None)
        createnewaccount = font_2.render("Create New Account !!!", True, DARK_TEAL_ACCENT_1_DARKER_25, None)
        login_fail = font_3.render("Invalid username or password!", True, RED, None)  # Khi đăng nhập không thành công
        login_success = font_3.render("Login successful !", True, RED, None)  # Khi đăng nhập thành công

        # # Biến xác định vùng vàng xung quanh bao quát
        # yellow_rect = pygame.Rect(430, screen_height // 2 - 160, 420, 372) 

        # # Tô màu vàng ở vùng bao quát xung quanh
        # pygame.draw.rect(screen, YELLOW, yellow_rect)
        screen.blit(loginBox,loginBox_rect)
        screen.blit(inputBox, username_rect)
        screen.blit(inputBox, password_rect)
        if Login_rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(button_pressed,Login_rect) 
        else: 
            screen.blit(button,Login_rect) 
        if Reset_rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(button_pressed,Reset_rect) 
        else: 
            screen.blit(button,Reset_rect) 

        #Vẽ đối tượng văn bản lên màn hình ở vị trí mong muốn
        screen.blit(loginpage, (screen_width // 2 - loginpage.get_width() // 2, screen_height // 2 - loginpage.get_height() // 2 - 125))
        screen.blit(username, (400, screen_height // 2 - loginpage.get_height() // 2 - 35))
        screen.blit(username_input_rendered, (400 + username_width, screen_height // 2 - loginpage.get_height() // 2 - 35))
        screen.blit(password, (400, screen_height // 2 - loginpage.get_height() // 2+40))
        screen.blit(Login, (450, screen_height // 2 - loginpage.get_height() // 2 +Login.get_height()//2+ 145))
        screen.blit(Reset, (550, screen_height // 2 - loginpage.get_height() // 2 +Login.get_height()//2+ 145))
        screen.blit(donthaveaccount, (480, screen_height // 2 - loginpage.get_height() // 2 + 200))
        screen.blit(createnewaccount, (480, screen_height // 2 - loginpage.get_height() // 2 + 250))
        if flag == True:
            screen.blit(login_success, (480, screen_height // 2 - loginpage.get_height() // 2 + 100)) # Khi đăng nhập thành công
        elif flag == False:
            screen.blit(login_fail, (480, screen_height // 2 - loginpage.get_height() // 2 + 100)) # Khi đăng nhập không thành công

        # Vẽ hình chữ nhật xung quanh vùng nhập dữ liệu, ô login, ô reset
        # pygame.draw.rect(screen, BLACK, (600, screen_height // 2 - username.get_height() // 2 - 50 - 10, 170, username.get_height() + 10), 2)
        # pygame.draw.rect(screen, BLACK, (600, screen_height // 2 - password.get_height() // 2 - 10, 170, password.get_height() + 10), 2)
        # pygame.draw.rect(screen, DARK_GREEN_ACCENT_3_DARKER_25, (485 - 5, screen_height // 2 - Login.get_height() // 2 + 50 - 10 , 55, Login.get_height() + 10), 2)
        # pygame.draw.rect(screen, DARK_GREEN_ACCENT_3_DARKER_25, (585 - 5, screen_height // 2 - Reset.get_height() // 2 + 50 - 10, 55, Reset.get_height() + 10), 2)
      
        # Cập nhật màn hình
        pygame.display.flip()

        # Giới hạn tốc độ khung hình
        clock.tick(60)

def sign_up():
 
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    DARK_RED = (139, 0, 0)  # Màu Dark Red
    YELLOW = (255, 255, 204)
    DARK_GREEN_ACCENT_3_DARKER_25 = (0, 73, 48)  # Màu Dark Green, Accent 3, Darker 25%

    # Tải ảnh nền
    background_image = pygame.image.load('img/background3.jpg')

    # Tải nhạc nền và phát lặp lại
    mixer.music.load('sound/signup_music.mp3')
    mixer.music.play(-1)  # -1 để phát lặp lại liên tục

    # tải âm thanh khi click chuột và khi nhấn phím
    click_sound = mixer.Sound('sound/click.mp3')
    key_sound = mixer.Sound("sound/key.wav")

    # Tạo font chữ
    font_1 = pygame.font.Font("font/Shermlock.ttf", 50)
    font_2 = pygame.font.Font("font/Shermlock.ttf", 32)
    font_3 = pygame.font.Font("font/Shermlock.ttf", 24)
    font_4 = pygame.font.Font("font/Shermlock.ttf", 36)

    # Biến lưu trữ tên người dùng
    username_input = ""
    password_1_input = ""
    password_2_input = ""

    # Đặt cờ hiệu input hiện tại là username hay là password
    current_input = "None"

    # Đặt cờ hiệu sign up có thành công hay không
    flag_password = None
    flag_account = None
    flag_username = None

    # Biến xác định vị trí ô vuông bên cạnh username, ô vuông bên cạnh password, ô signup
    username_rect = pygame.Rect(550, screen_height // 2 - font_2.get_height() // 2 - 80, 300, font_2.get_height() + 60) #username thuộc font_2 
    password_1_rect = pygame.Rect(550, screen_height // 2 - font_2.get_height() // 2 -5, 300, font_2.get_height() + 60) #password thuộc font_2
    password_2_rect = pygame.Rect(550, screen_height // 2 - font_2.get_height() // 2 + 70, 300, font_2.get_height() + 60) #password thuộc font_2
    signup_rect = pygame.Rect(430, screen_height // 2 - font_3.get_height() // 2 + 200, 100, font_3.get_height() + 10) #Login thuộc font_3

    # Hàm kiểm tra xem chuột có nằm trong ô vuông bên cạnh username hay không
    def is_over_username_box(mouse_pos):
        return username_rect.collidepoint(mouse_pos)
    # Hàm kiểm tra xem chuột có nằm trong ô vuông bên cạnh password1 hay không
    def is_over_password_1_box(mouse_pos):
        return password_1_rect.collidepoint(mouse_pos)
    # Hàm kiểm tra xem chuột có nằm trong ô vuông bên cạnh password2 hay không
    def is_over_password_2_box(mouse_pos):
        return password_2_rect.collidepoint(mouse_pos)
    # Hàm kiểm tra xem chuột có nằm trong ô signup
    def is_over_signup_box(mouse_pos):
        return signup_rect.collidepoint(mouse_pos)

    blink_timer = 0
    blink_interval = 60  # Điều chỉnh khoảng thời gian nhấp nháy

    signupBox = pygame.image.load("img/LoginSignupBox.png").convert_alpha()
    signupBox = pygame.transform.scale(signupBox,(signupBox.get_width()+200, signupBox.get_height()+100))
    signupBox_rect = signupBox.get_rect()
    signupBox_rect.center = (screen_width // 2, screen_height//2)
    
    inputBox = pygame.image.load("img/Input.png").convert_alpha()
    inputBox = pygame.transform.scale(inputBox, (300, (font_2.get_height() + 60)))
    
    button = pygame.image.load("img/modebox.png").convert_alpha()
    button = pygame.transform.scale(button, (100, font_3.get_height()+10))
    button_pressed = pygame.image.load("img/modeboxpressed.png").convert_alpha()
    button_pressed = pygame.transform.scale(button_pressed, (100, font_3.get_height()+10))

    # Vòng lặp chính
    running = True
    while running:
        # Cập nhật timer của dấu nháy
        blink_timer += 1
        if blink_timer >= blink_interval:
            blink_timer = 0
        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Thoát khỏi pygame khi nhấn nút tắt màn hình
                quit()  # Thoát khỏi chương trình
            # Bắt sự kiện nhấp chuột
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Kiểm tra xem chuột có nằm trong ô vuông bên cạnh username hay không
                if is_over_username_box(mouse_pos):
                    click_sound.play()
                    current_input = "username"
                if is_over_password_1_box(mouse_pos):
                    click_sound.play()
                    current_input = "password_1"
                if is_over_password_2_box(mouse_pos):
                    click_sound.play()
                    current_input = "password_2"
                if is_over_signup_box(mouse_pos):
                    click_sound.play()
                    # Lưu ý, cho phép đăng kí mới True, còn không cho phép thì False, chưa biết thì None
                    if password_1_input != password_2_input:
                        flag_password = False
                        flag_account = None
                        flag_username = None
                        password_1_input = ""
                        password_2_input = ""                        
                    else:
                        flag_password = True
                        filename = "accounts.json"
                        accounts = read_accounts_from_json(filename)
                        if check_account(username_input, password_1_input, accounts):
                            # nếu đã tồn tại thì không cho phép sign up
                            flag_account = False
                            flag_username = None
                            username_input = ""
                            password_1_input = ""
                            password_2_input = ""
                        else: # không tồn tại tài khoản nhưng có thể trùng username
                            flag_account = True
                            if check_username(username_input, password_1_input, accounts):
                                flag_username = False
                                username_input = ""  
                            else:                
                                add_account(filename, username_input, password_1_input)
                                flag_account = True
                                # nếu ráp code muốn return ra chuỗi username mới thì return ngay chỗ này
                                running = False
                                # mixer.music.stop()
                                # print(username_input)                             
                                return username_input                    
          
            # Bắt sự kiện nhập văn bản vào ô username or password
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if current_input == "username":
                        key_sound.play()
                        # Nếu nhấn phím backspace, xóa ký tự cuối cùng trong username
                        username_input = username_input[:-1]
                    elif current_input == "password_1":
                        key_sound.play()
                        # Nếu nhấn phím backspace, xóa ký tự cuối cùng trong password
                        password_1_input = password_1_input[:-1]
                    elif current_input == "password_2":
                        key_sound.play()
                        # Nếu nhấn phím backspace, xóa ký tự cuối cùng trong password
                        password_2_input = password_2_input[:-1]
                elif event.key == pygame.K_RETURN:
                    if current_input != "None":
                        pass
                        key_sound.play()
                    current_input = "None"
                elif event.key == pygame.K_UP:
                    key_sound.play()
                    if current_input == "None":
                        current_input = "password_2"
                    elif current_input == "username":
                        current_input = "password_2"
                    elif current_input == "password_1":
                        current_input = "username"
                    elif current_input == "password_2":
                        current_input = "password_1"
                elif event.key == pygame.K_DOWN:
                    key_sound.play()
                    if current_input == "None":
                        current_input = "username"
                    elif current_input == "username":
                        current_input = "password_1"
                    elif current_input == "password_1":
                        current_input = "password_2"
                    elif current_input == "password_2":
                        current_input = "username"                    
                else:
                    if current_input == "username":
                        key_sound.play()
                        if len(username_input) < 20:
                            # Nếu nhấn một phím khác, thêm ký tự đó vào username
                            username_input += event.unicode
                        else:
                            # nếu độ dài bằng 20 thì lấy 20 kí tự cuối cùng
                            username_input += event.unicode
                            username_input = username_input[1:]
                    elif current_input == "password_1":
                        key_sound.play()
                        if len(password_1_input) < 20:
                            # Nếu nhấn một phím khác, thêm ký tự đó vào password
                            password_1_input += event.unicode
                        else:
                            password_1_input += event.unicode
                            password_1_input = password_1_input[1:]                 
                    elif current_input == "password_2":
                        key_sound.play()
                        if len(password_2_input) < 20:
                            # Nếu nhấn một phím khác, thêm ký tự đó vào password
                            password_2_input += event.unicode
                        else:
                            password_2_input += event.unicode
                            password_2_input = password_2_input[1:]                 


        # Tô màu màn hình
        screen.fill(WHITE)

        # Vẽ ảnh nền
        screen.blit(background_image, (0, 0))        

        # Render và vẽ các thành phần giao diện
        signuppage = font_1.render("Sign up", True, DARK_RED, None)
        if current_input == "None":
            username = font_2.render("Username  ", True, YELLOW, None)
            username_width = username.get_width()
            username_input_rendered = font_4.render(username_input, True, YELLOW, None)
            password_1 = font_2.render(f"Password     {'*' * len(password_1_input)}", True, YELLOW, None)
            password_2 = font_2.render(f"Confirm       {'*' * len(password_2_input)}", True, YELLOW, None)     
        elif current_input == "username":
            password_1 = font_2.render(f"Password     {'*' * len(password_1_input)}", True, YELLOW, None)
            password_2 = font_2.render(f"Confirm       {'*' * len(password_2_input)}", True, YELLOW, None)
            if blink_timer < blink_interval / 2:
                username = font_2.render("Username  ", True, YELLOW, None)
                username_width = username.get_width()
                username_input_rendered = font_4.render(username_input, True, YELLOW, None)
            else:
                username = font_2.render("Username  ", True, BLACK, None)
                username_width = username.get_width()
                username_input_rendered = font_4.render(f"{username_input}|", True, BLACK, None)
        elif current_input == "password_1":
            username = font_2.render("Username  ", True, YELLOW, None)
            username_width = username.get_width()
            username_input_rendered = font_4.render(username_input, True, YELLOW, None)
            password_2 = font_2.render(f"Confirm       {'*' * len(password_2_input)}", True, YELLOW, None)
            if blink_timer < blink_interval / 2:
                password_1 = font_2.render(f"Password     {'*' * len(password_1_input)}", True, YELLOW, None)
            else:
                password_1 = font_2.render(f"Password     {'*' * len(password_1_input)}|", True, BLACK, None)
        elif current_input == "password_2":
            username = font_2.render("Username  ", True, YELLOW, None)
            username_width = username.get_width()
            username_input_rendered = font_4.render(username_input, True, YELLOW, None)
            password_1 = font_2.render(f"Password     {'*' * len(password_1_input)}", True, YELLOW, None)
            if blink_timer < blink_interval / 2:
                password_2 = font_2.render(f"Confirm       {'*' * len(password_2_input)}", True, YELLOW, None)
            else:
                password_2 = font_2.render(f"Confirm       {'*' * len(password_2_input)}|", True, BLACK, None)

        signup = font_3.render("Sign up", True, DARK_GREEN_ACCENT_3_DARKER_25, None)
        wrong_password = font_3.render("Please check your password again !", True, RED, None)
        existed_account_1 = font_3.render("This account has been existed", True, RED, None)
        existed_account_2 = font_3.render("Please create a new account !", True, RED, None)
        existed_username_1 = font_3.render("This username has been existed", True, RED, None)
        existed_username_2 = font_3.render("Please create a new username !", True, RED, None)

        # # Biến xác định vùng vàng xung quanh bao quát
        # yellow_rect = pygame.Rect(430, screen_height // 2 - 160, 420, 372) 

        # # Tô màu vàng ở vùng bao quát xung quanh
        # pygame.draw.rect(screen, YELLOW, yellow_rect)
        
        screen.blit(signupBox,signupBox_rect)
        screen.blit(inputBox,username_rect)
        screen.blit(inputBox,password_1_rect)
        screen.blit(inputBox,password_2_rect)
        if signup_rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(button_pressed,signup_rect) 
        else: 
            screen.blit(button,signup_rect) 
        

        #Vẽ đối tượng văn bản lên màn hình ở vị trí mong muốn
        screen.blit(signuppage, (screen_width // 2 - signuppage.get_width() // 2, screen_height // 2 - signuppage.get_height() // 2 - 150))
        screen.blit(username, (400, screen_height // 2 - signuppage.get_height() // 2 - 35))
        screen.blit(username_input_rendered, (440 + username_width, screen_height // 2 - signuppage.get_height() // 2 - 35))
        screen.blit(password_1, (400, screen_height // 2 - signuppage.get_height() // 2 +40))
        screen.blit(password_2, (400, screen_height // 2 - signuppage.get_height() // 2 + 115))
        screen.blit(signup, (440, screen_height // 2 - signuppage.get_height() // 2 + signup.get_height() //2+ 205))
        if flag_password == False:
            screen.blit(wrong_password, (570, screen_height // 2 - signuppage.get_height() // 2 + 200))
        else:
            if flag_account == False:
                screen.blit(existed_account_1, (570, screen_height // 2 - signuppage.get_height() // 2 + 200))
                screen.blit(existed_account_2, (570, screen_height // 2 - signuppage.get_height() // 2 + 230))
            else:
                if flag_username == False:
                    screen.blit(existed_username_1, (570, screen_height // 2 - signuppage.get_height() // 2 + 200))
                    screen.blit(existed_username_2, (570, screen_height // 2 - signuppage.get_height() // 2 + 230))

        # Vẽ hình chữ nhật xung quanh vùng nhập dữ liệu
        # pygame.draw.rect(screen, BLACK, (600, screen_height // 2 - username.get_height() // 2 - 50 - 10, 170, username.get_height() + 10), 2)
        # pygame.draw.rect(screen, BLACK, (600, screen_height // 2 - password_1.get_height() // 2 - 22, 200, password_1.get_height() + 10), 2)
        # pygame.draw.rect(screen, BLACK, (600, screen_height // 2 - password_2.get_height() // 2 + 50 - 22, 200, password_2.get_height() + 10), 2)
        # pygame.draw.rect(screen, DARK_GREEN_ACCENT_3_DARKER_25, (485 - 5, screen_height // 2 - signup.get_height() // 2 + 100 - 22 , 70, signup.get_height() + 10), 2)
      
        # Cập nhật màn hình
        pygame.display.flip()

        # Giới hạn tốc độ khung hình
        clock.tick(60)

def start_all():
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    YELLOW = (255, 255, 204)
    DARK_RED = (139, 0, 0)  # Màu Dark Red

    # Tải ảnh nền
    background_image = pygame.image.load('img/background1.jpg')
    background_image = pygame.transform.scale(background_image,(1280,720))

    # tải âm thanh khi click chuột
    click_sound = mixer.Sound('sound/click.mp3')

    # Tải nhạc nền và phát lặp lại
    mixer.music.load('sound/startall_music.mp3')
    mixer.music.play(-1)  # -1 để phát lặp lại liên tục

    #return login trả về tên đăng nhập
    tendangnhap = ''

    # Tạo font chữ
    font_1 = pygame.font.Font('font/Shermlock.ttf', 36)
    
    # Biến xác định vị trí ô vuông 
    modebox = pygame.image.load('img/modebox.png').convert_alpha()
    modebox = pygame.transform.scale(modebox, (190, font_1.get_height() + 20))
    modebox_pressed = pygame.image.load('img/modeboxpressed.png').convert_alpha()
    modebox_pressed = pygame.transform.scale(modebox_pressed, (190, font_1.get_height() + 20))
    Login_rect = pygame.Rect(300, screen_height // 2 - font_1.get_height() // 2 - 50 - 10 , 190, font_1.get_height() + 20) 
    Signup_rect = pygame.Rect(300, screen_height // 2 - font_1.get_height() // 2 + 50 - 10 , 190, font_1.get_height() + 20) 

    # Hàm kiểm tra xem chuột có nằm trong ô vuông 
    def is_over_Login_box(mouse_pos):
        return Login_rect.collidepoint(mouse_pos)
    # Hàm kiểm tra xem chuột có nằm trong ô Reset hay không
    def is_over_Signup_box(mouse_pos):
        return Signup_rect.collidepoint(mouse_pos)

    # Vòng lặp chính
    running = True
    while running:
        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Thoát khỏi pygame khi nhấn nút tắt màn hình
                quit()  # Thoát khỏi chương trình
            # Bắt sự kiện nhấp chuột
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Kiểm tra xem chuột có nằm trong ô vuông bên cạnh username hay không
                if is_over_Login_box(mouse_pos):
                    click_sound.play()  # Phát âm thanh khi click vào ô Login
                    mixer.music.stop()
                    tendangnhap = login()
                if is_over_Signup_box(mouse_pos):
                    click_sound.play()  # Phát âm thanh khi click vào ô signup 
                    mixer.music.stop()
                    tendangnhap = sign_up()
                return tendangnhap   
                               
        screen.blit(background_image, (0, 0))

        # Render và vẽ các thành phần giao diện
        Login = font_1.render("Log in", True, DARK_RED, None)
        Signup = font_1.render("Sign up", True, DARK_RED, None)
        
        screen.blit(modebox,Login_rect)
        screen.blit(modebox,Signup_rect)


        #Vẽ đối tượng văn bản lên màn hình ở vị trí mong muốn
        screen.blit(Login, (screen_width // 2-240 - Login.get_width() // 2, screen_height // 2 - Login.get_height() // 2 - 50))
        screen.blit(Signup, (screen_width // 2-240 - Signup.get_width() // 2, screen_height // 2 - Signup.get_height() // 2 + 50))
      
        # Cập nhật màn hình
        pygame.display.flip()

        # Giới hạn tốc độ khung hình
        clock.tick(60)

    # Thoát khỏi Pygame
    #pygame.quit()

if __name__ == '__main__':
    pygame.init()

    #Cửa số game: chỉnh full screen: screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    screen_width = 1280
    screen_height = 720
    screen = pygame.display.set_mode((screen_width,screen_height)) 

    #Đặt tên cho cửa sổ game là Maze
    pygame.display.set_caption('Maze')
    
    #Hình ảnh tượng trưng cho game đặt bên trái tên cửa sổ game
    img = pygame.image.load('img/maze_icon.png')
    pygame.display.set_icon(img)

    #tạo biến clock truy cập vào đồng hồ trong pygame.time để xử lí về thời gian
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("white")
        ss = start_all()
        break
    pygame.quit()

    
